#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
apply_figs.py — 把六題的向量圖解插回解題正本，並重建 problems-view

用法（在知識庫根目錄執行）：
    python3 apply_figs.py .            # 實際寫入
    python3 apply_figs.py . --dry      # 只列出會做什麼，不寫檔

做四件事：
  1. 檢查 raw/solutions/<題號>/figs/ 下的 SVG 是否齊全
  2. 把「圖 1」插到 §2 之前（緊接在題目重述之後），其餘各圖插到 §5 之前
  3. 檔尾日期行補記產圖腳本
  4. 對每一題呼叫 scripts/gen_problems_view.py 重建渲染頁

特性：**冪等**。同一題重跑不會插第二次（偵測到圖片路徑已存在就跳過）。
行尾一律沿用原檔（本庫 .md 為 CRLF）。
"""
import os, re, sys, subprocess

DRY = "--dry" in sys.argv
ROOT = sys.argv[1] if len(sys.argv) > 1 else "."

# (檔名尾碼, 圖號, alt 文字, 圖說)  ——  圖說第二句一定要說出「它攔什麼錯」
FIGS = {
"RC-2010-1": [
 ("1-section", 1,
  "RC-2010-1 圓形螺旋柱斷面：外徑 75 cm，螺旋筋外緣直徑 68 cm，12-#10 主筋環排，外環為蓋層、內圈為圍束核心",
  "圓形螺旋柱斷面（向量重繪）。$A_{ch}$ 用的是螺旋筋外緣直徑 $D_c = 68$ cm 而非全斷面 $D = 75$ cm——誤用 $D$ 會把核心高估 22%、蓋層直接消失，$P_u$ 與 $P_y$ 的比較就整個失去意義。"),
 ("2-loss-gain", 2,
  "RC-2010-1 Py 與 Pu 的三段分解長條圖：兩者共有核心素混凝土與鋼筋，差別只在蓋層 233.9 tf 與圍束增益 233.6 tf，第三條為漏乘 0.85 的錯誤式",
  "$P_y$ 與 $P_u$ 的三段分解。兩者只差中間那一塊——把蓋層換成圍束增益。長度幾乎相同（233.9 vs 233.6 tf），這就是「剛好打平、零餘裕」的視覺版；第三條顯示漏掉 $0.85$ 會憑空多出 179 tf，且過不了 $\\rho_s = 0$ 的檢驗。"),
 ("3-rho-s", 3,
  "RC-2010-1 螺旋筋比隨間距變化的曲線，標出規範最小值 0.00812 與 Pu=Py 的理論門檻 0.00748，以及假設的 s=10 cm 工作點",
  "$\\rho_s$ 與兩條門檻。假設的 $s = 10$ cm 落在兩條線之下，需縮到 $s \\le 9.20$ cm；兩條門檻之間那道縫（0.45 vs 0.4146）就是「理論剛好夠、規範還不夠」的來源，可攔下把 $\\rho_s$ 不足與 $P_u > P_y$ 同時寫出而不覺矛盾。"),
],
"RC-2004-3": [
 ("1-section", 1,
  "RC-2004-3 柱斷面 50×50 cm，外箍加兩支繫筋，標示核心尺寸 hc=42 cm、繫筋水平間距 hx=18.46 cm 與每方向有效三腿",
  "柱斷面與圍束幾何。$h_c$ 與 $A_{ch}$ 都量到箍筋**外緣**（同一基準才可寫 $A_{ch} = h_c^2$）；圖上把兩支繫筋分色，可攔下「把斷面全部 6 腿算給同一方向」這個常見錯。"),
 ("2-spacing", 2,
  "RC-2004-3 五個間距上限的長條比較：公式一 7.36 cm 控制，公式二 10.24、b/4 為 12.5、6db 為 15.24、sx 為 15 cm，並標出 7.4 與 7.5 已越線",
  "五個間距上限與最終控制值。$s_x$ 那一列提醒它不是固定 15 cm 而要由 $h_x$ 算；下方三格把「寫 7.4」「取 7.5」「取 7」並排，可攔下把 7.36 進位後仍自認合格的錯誤。"),
],
"RC-2017-1": [
 ("1-section", 1,
  "RC-2017-1 加大柱斷面 40×70 cm，中央虛線為原 40×40 舊核心，兩翼各配 4 支 D25",
  "加大柱斷面（向量重繪）。彎曲方向是 70 cm 全深、8 支 D25 集中在兩翼各成一直行——這是題目與原圖都講明的條件，不是假設；排列一改，Part (c) 的 $M_{n,b}$ 會掉 23%。"),
 ("2-bilinear", 2,
  "RC-2017-1 題目指定的雙折線應力應變關係：0 到 0.002 線性升至 1.0f'c，0.002 到 0.003 線性降至 0.8f'c",
  "題目指定的本構關係。這條線上根本沒有 $0.85f'_c$ 這個值，可攔下「看到 $\\beta_1$ 就順手寫 Whitney」的反射動作。"),
 ("3-stress-block", 3,
  "RC-2017-1 平衡點壓力區的應力分佈：藍色為雙折線分區積分的真實分佈，灰虛線為 Whitney 矩形，右側列出兩者的 Cc、形心、Pn,b、Mn,b 差距",
  "平衡點壓力區：雙折線分區積分 vs Whitney 近似。兩者疊在同一張圖上，$C_c$ 差 14.1%、$P_{n,b}$ 差 14.5%——這正是本題設計來抓的錯，而 $M_{n,b}$ 只差 1.8%，所以光看彎矩答案還察覺不出來。"),
 ("4-axial", 4,
  "RC-2017-1 e=0 時軸力隨應變變化的曲線，峰值 745 tf 在應變 0.002，本解採用的 634 tf 在應變 0.003",
  "$e = 0$ 時軸力隨應變的變化。雙折線下軸力是應變的函數，峰值在 $\\varepsilon = 0.002$（745 tf）而非 $\\varepsilon_{cu} = 0.003$（634 tf）；本解取後者以與 P-M 曲線端點共用假設，但作答時必須說明取的是哪一個定義。"),
],
"RC-2006-2": [
 ("1-section", 1,
  "RC-2006-2 柱斷面 50×50 cm，8-#10 呈 3×3 扣中心排列，繞 Y 軸彎曲時 6 根力臂 18 cm、2 根力臂為零",
  "柱斷面與 $I_{se}$ 的力臂。8 根不是「每排 4 根」而是 3×3 扣掉正中心；繞 Y 軸時只有 6 根有 18 cm 力臂，可攔下 $I_{se}$ 數錯根數。"),
 ("2-curvature", 2,
  "RC-2006-2 單曲率與雙曲率的挫屈變形與端點彎矩圖對照，單曲率 Cm=0.822、雙曲率 Cm 取 0.4 下限",
  "單曲率 vs 雙曲率的 $C_m$。單曲率時最大彎矩與挫屈變形疊在一起，$C_m$ 趨近 1.0 最不利；圖下方註明本頁採 318-02 慣例，可攔下把新慣例（單曲率取負）配舊公式而得出「不需放大」的相反結論。"),
 ("3-magnifier", 3,
  "RC-2006-2 放大係數隨軸力比變化的曲線，標出本題工作點 δns=1.352 與精確 EI 式的 1.266，右側列出各中間量與 M2,min 檢核",
  "$\\delta_{ns}$ 隨 $P_u/(0.75P_c)$ 的變化。曲線在接近 1 時陡升，說明 0.75 折減與 $\\delta_{ns} \\ge 1.0$ 下限都不能漏；右下角把 $M_{2,\\min} = 12.0$ tf·m 的檢核標出來，那是本題原本完全缺席的規範步驟。"),
],
"RC-2011-3": [
 ("1-section", 1,
  "RC-2011-3 矩形柱斷面 40×60 cm，6-#10 分三排在 6/30/54 cm，中排恰在塑性形心上",
  "矩形柱斷面與三排鋼筋。橘色中排恰在塑性形心（$d_m = h/2 = 30$ cm）：對彎矩力臂為零完全不貢獻，但軸力照樣要算——這一排的兩面性是本題最常被忽略的地方。"),
 ("2-balanced", 2,
  "RC-2011-3 在 0.9Pb 軸力下的斷面、應變分佈與合力三聯圖，c=29.61 cm、a=23.69 cm，中排落在應力塊之外且受微拉",
  "$P_n = 0.9P_b$ 的斷面／應變／合力。三格垂直比例共用，$a = 23.69 < d_m = 30$ 的相對關係是真的——中排落在等值應力塊**之外**就不扣 $0.85f'_c$ 占位，而且此時它其實受微拉，兩件事一起錯會讓軸力差一截。"),
 ("3-curvature", 3,
  "RC-2011-3 降伏狀態（彈性中性軸 24.95 cm）與極限狀態（Whitney 中性軸 24.92 cm）的應變分佈對照，曲率延展比 1.70",
  "曲率延展比的兩個狀態。左圖用彈性三角形應力分佈求 $\\phi_y$、右圖用 Whitney 矩形求 $\\phi_u$，兩者本構不同不可混用；兩個中性軸幾乎重合（24.95 vs 24.92 cm）正是 $\\mu_\\phi$ 只有 1.70 的原因。"),
],
"RC-2008-2": [
 ("1-section", 1,
  "RC-2008-2 方形柱斷面 56×56 cm，8-#8 分三排在距壓力面 8/28/48 cm，分別為 3、2、3 根",
  "方形柱斷面與三排鋼筋。最下排（$d = 48$ cm）就是題目設定應變為零的那一排——這個條件直接把中性軸鎖死，本題根本沒有「解方程求 $c$」這一步。"),
 ("2-strain", 2,
  "RC-2008-2 拉力側應變為零時的斷面、應變分佈與合力三聯圖，c=48 cm、a=38.4 cm，上兩排在應力塊內要扣占位、最下排在塊外不扣",
  "$\\varepsilon_t = 0$ 的斷面／應變／合力。三排的處理各不相同：上排降伏且在應力塊內要扣占位、中排未降伏但仍在塊內也要扣、最下排在塊外且應力為零——把三排一律同樣處理是本題最常見的錯。"),
 ("3-pm", 3,
  "RC-2008-2 的 P-M 交互曲線，標出純軸壓、本題點、平衡點、純彎矩四個關鍵點，以及設計曲線的彎矩峰值在 εt=0.005",
  "本題點在 P-M 圖上的位置。本題點遠在平衡點之上屬壓力控制區；圖上同時標出**標稱** $M_n$ 峰值（平衡點 87.68）與**設計** $\\varphi M_n$ 峰值（$\\varepsilon_t = 0.005$ 處 64.90），可攔下把「$\\varphi \\times$ 標稱峰值」當成最大設計彎矩的錯誤（那只有 56.99）。"),
],
}


def apply_one(mid, entries):
    md = os.path.join(ROOT, "raw", "solutions", mid, mid + ".md")
    figdir = os.path.join(ROOT, "raw", "solutions", mid, "figs")
    if not os.path.exists(md):
        print(f"  跳過 {mid}：找不到 {md}")
        return False
    missing = [e[0] for e in entries
               if not os.path.exists(os.path.join(figdir, f"{mid}-fig-{e[0]}.svg"))]
    if missing:
        print(f"  跳過 {mid}：figs/ 缺少 {missing}")
        return False

    raw = open(md, "rb").read()
    crlf = raw.count(b"\r\n") > 0 and raw.count(b"\r\n") == raw.count(b"\n")
    s = raw.decode("utf-8").replace("\r\n", "\n")

    if f"figs/{mid}-fig-{entries[0][0]}.svg" in s:
        print(f"  跳過 {mid}：圖片連結已存在（冪等）")
        return False

    def block(e):
        suffix, num, alt, cap = e
        return (f"![{alt}](figs/{mid}-fig-{suffix}.svg)\n\n"
                f"*圖 {num}　{cap}*\n\n")

    # 圖 1 插到 §2 之前；其餘插到 §5 之前
    m2 = re.search(r"^## 2\.", s, flags=re.M)
    m5 = re.search(r"^## 5\.", s, flags=re.M)
    if not m2 or not m5:
        print(f"  跳過 {mid}：找不到 §2 或 §5 標題")
        return False

    rest = "".join(block(e) for e in entries[1:])
    s = s[:m5.start()] + rest + s[m5.start():]
    m2 = re.search(r"^## 2\.", s, flags=re.M)          # 位置已變，重找
    s = s[:m2.start()] + block(entries[0]) + s[m2.start():]

    # 檔尾補記
    tail = (f"\n*圖解補繪：2026-08-21（向量圖 {len(entries)} 張，"
            f"腳本 `figs/gen_{mid}.py`，可重跑；腳本檔尾對 §4 公佈值做 assert）*\n")
    s = s.rstrip("\n") + "\n" + tail

    if DRY:
        print(f"  [dry] {mid}：會插入 {len(entries)} 張圖")
        return True
    open(md, "wb").write((s.replace("\n", "\r\n") if crlf else s).encode("utf-8"))
    print(f"  已插入 {mid}：{len(entries)} 張圖")
    return True


def main():
    print("── 插入圖解 ──")
    done = [mid for mid, e in FIGS.items() if apply_one(mid, e)]
    if DRY or not done:
        return
    gen = os.path.join(ROOT, "scripts", "gen_problems_view.py")
    if os.path.exists(gen):
        print("\n── 重建 problems-view ──")
        subprocess.run([sys.executable, gen, ROOT] + done, check=False)
    else:
        print(f"\n找不到 {gen}，請自行重建 problems-view")


if __name__ == "__main__":
    main()
