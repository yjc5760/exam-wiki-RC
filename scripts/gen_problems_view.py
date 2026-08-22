#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_problems_view.py — 由解題正本重新產生 study/problems-view/ 的渲染頁

用途
----
`raw/solutions/XX-YYYY-N/XX-YYYY-N.md` 是解題內容的**唯一正本**；
`study/problems-view/XX-YYYY-N.html` 只是它的渲染顯示。
改完正本後跑這支腳本，把 HTML 的 <main> 區塊重新產生，
head / header / footer / 頁尾跟隨來源單元的 script 一律原樣保留。

用法
----
    python3 gen_problems_view.py . RC-2015-1              # 只重建指定題（常用）
    python3 gen_problems_view.py . RC-2015-1 RC-2011-3
    python3 gen_problems_view.py . RC-2015-1 --check      # 只比對不寫檔
    python3 gen_problems_view.py . --all --check          # 掃全庫，只比對不寫檔
    python3 gen_problems_view.py . --all                  # 全庫重建（會動到很多頁，先讀下面那段）

旗標請放在題號**後面**（argparse 的 nargs='*' 特性：`. --check A B` 會解析失敗）。

**預設不吃全庫**——不給題號就什麼都不做。要全庫請明寫 --all。

--check 的意義
--------------
用**現有的** .md 重新產生 HTML，跟磁碟上的 HTML 逐位元組比對。
identical 表示這支腳本的管線與當初產生該頁的管線一致，可以放心拿去套改過的 .md。

⚠ 已知現況（2026-08-21 實測，100 頁）：**只有 20 頁 identical**。
問題不在這支腳本，而在既有 problems-view 是歷次不同管線產出的混合體：

  20 頁  本管線（遮罩數學式 + nl2br + 清單補空行）
  34 頁  同上但未補清單空行 → 清單被 nl2br 壓成 <br /> 行，沒有 <ul>/<ol>
   2 頁  連 nl2br 都沒開
  44 頁  以上皆非；其中 **35 頁的數學式沒有遮罩就送進 markdown**，
         `&` `<` `>` 被轉義成 &amp; &lt; &gt;、`\\` 被吃掉
         → 這些頁的 KaTeX 實際上渲染失敗（\begin{cases} 首當其衝）

也就是說 differ 不必然代表這支腳本有問題，多半是那一頁本來就該重建。
但**全庫重建會一次改動 80 頁**，請當成一次獨立、可審閱的批次作業，不要順手做。
單題重建（改完某題正本後）則沒有這個顧慮。

為何是這套管線
--------------
python-markdown，extensions=['tables','nl2br','fenced_code']，外加四道前後處理：

  (a) 先把 $$...$$ 與 $...$ 遮罩成 placeholder 再交給 markdown，還原後貼回。
      不遮罩的話：`\\#`、`\\!` 的跳脫會被吃掉，`f'_c` 的底線會被當成強調，
      數學式內的 `<` `>` 會被轉義成 &lt; &gt; 而 KaTeX 讀不到。
  (b) 清單前若缺空行補一行（CommonMark 要求，但庫內 .md 常省略）。
  (c) 圖片 src 補上 ../../raw/solutions/XX-YYYY-N/ 前綴
      （HTML 在 study/problems-view/，圖在 raw/solutions/ 底下）。
  (d) 只替換 <main>...</main>，其餘一個位元組都不動。

行尾：problems-view 的 HTML 全庫是 LF，正本 .md 是 CRLF。
本腳本一律以 LF 寫出 HTML，不受執行平台影響（newline='' + 明確 \\n）。

依賴：pip install markdown
"""

import argparse
import os
import re
import sys

try:
    import markdown
except ImportError:
    sys.exit("需要 markdown 套件：pip install markdown")

MODULE_RE = re.compile(r'^[A-Z]{2}-\d{4}-\d+$')


def render_main(md_text, module_id):
    """把正本 .md 的內容轉成 <main> 內部的 HTML（不含 <main> 標籤本身）。"""
    store = []

    def mask(m):
        store.append(m.group(0))
        return f"\x00MATH{len(store) - 1}\x00"

    s = md_text.replace('\r\n', '\n')

    # (a) 遮罩數學式：先 $$…$$（含跨行），再單一 $…$
    s = re.sub(r'\$\$.*?\$\$', mask, s, flags=re.S)
    s = re.sub(r'(?<!\$)\$(?!\$).*?(?<!\$)\$(?!\$)', mask, s, flags=re.S)

    # (b) 清單前補空行
    out, prev = [], None
    is_item = lambda ln: re.match(r'^\s*([-*+]|\d+\.)\s+', ln) is not None
    for line in s.split('\n'):
        if is_item(line) and prev is not None and prev.strip() != '' and not is_item(prev):
            out.append('')
        out.append(line)
        prev = line
    s = '\n'.join(out)

    html = markdown.markdown(s, extensions=['tables', 'nl2br', 'fenced_code'])

    # 還原數學式
    html = re.sub(r'\x00MATH(\d+)\x00', lambda m: store[int(m.group(1))], html)

    # (c) 圖片路徑前綴（已是相對上層或絕對網址的不動）
    html = re.sub(r'src="(?!\.\./|https?:|data:)',
                  f'src="../../raw/solutions/{module_id}/', html)
    return html


def rebuild(repo, module_id, check_only=False):
    """回傳 (status, message)。status ∈ {'same','written','differs','skip'}"""
    md_path = os.path.join(repo, 'raw', 'solutions', module_id, module_id + '.md')
    html_path = os.path.join(repo, 'study', 'problems-view', module_id + '.html')
    if not os.path.exists(md_path):
        return 'skip', '缺正本 .md'
    if not os.path.exists(html_path):
        return 'skip', '缺渲染頁 .html（本腳本只更新既有頁面，不建新頁）'

    md_text = open(md_path, encoding='utf-8').read()
    old = open(html_path, encoding='utf-8', newline='').read().replace('\r\n', '\n')

    i = old.find('<main')
    j = old.find('</main>')
    if i < 0 or j < 0:
        return 'skip', '找不到 <main> 區塊'
    j += len('</main>')

    new = old[:i] + '<main>' + render_main(md_text, module_id) + '</main>' + old[j:]

    if new == old:
        return 'same', ''
    if check_only:
        return 'differs', f'{len(old)} → {len(new)} bytes'
    with open(html_path, 'w', encoding='utf-8', newline='') as f:
        f.write(new)
    return 'written', f'{len(old)} → {len(new)} bytes'


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('repo', help='知識庫根目錄')
    ap.add_argument('modules', nargs='*', help='題號（如 RC-2015-1）')
    ap.add_argument('--check', action='store_true',
                    help='只比對不寫檔；有差異時以 exit code 1 結束')
    ap.add_argument('--all', action='store_true',
                    help='對 study/problems-view/ 下所有題目作業（不給題號時必須明寫）')
    args = ap.parse_args()

    if not args.modules and not args.all:
        sys.exit('請指定題號，或明寫 --all 對全庫作業（見檔頭說明：全庫重建會改動約 80 頁）')

    view_dir = os.path.join(args.repo, 'study', 'problems-view')
    if not os.path.isdir(view_dir):
        sys.exit(f'找不到 {view_dir}')

    mods = args.modules or sorted(
        f[:-5] for f in os.listdir(view_dir)
        if f.endswith('.html') and MODULE_RE.match(f[:-5]))
    if args.modules and args.all:
        sys.exit('--all 與指定題號不可並用')

    for m in mods:
        if not MODULE_RE.match(m):
            sys.exit(f'題號格式不合：{m}（應為 XX-YYYY-N）')

    tally = {}
    for m in mods:
        status, msg = rebuild(args.repo, m, args.check)
        tally[status] = tally.get(status, 0) + 1
        if status != 'same':
            print(f'{status:8s} {m}  {msg}')

    print(f'\n共 {len(mods)} 題：' +
          '  '.join(f'{k}={v}' for k, v in sorted(tally.items())))
    if args.check and tally.get('differs'):
        print('\n有差異——請先確認是「正本改過」還是「該頁本來就是舊管線產物」再重建。')
        sys.exit(1)


if __name__ == '__main__':
    main()
