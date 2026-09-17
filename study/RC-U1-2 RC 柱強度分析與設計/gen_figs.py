#!/usr/bin/env python3
"""RC-U1-2 柱強度分析與設計 —— 觀念講義向量圖（struct-diagram / structdraw.py）

所有圖上的數值都由 column.py 的示範柱推出，改 column.py 的常數即全部重繪。
驗證：python3 <skill>/scripts/render.py . --scale=2.0
      （XML 合法性 + 溢出檢查 + 2x PNG；**改完 SVG 一定要重跑才會更新 PNG**）
"""
import os
import sys

SKILL = os.environ.get(
    "STRUCTDRAW",
    "/root/.claude/skills/synced/6983ec08-a01a-44e4-a131-56c9e592c524_"
    "ab4f317b-1625-4c71-b32d-871e33fbc9cc/struct-diagram/scripts")
sys.path.insert(0, SKILL)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from structdraw import Canvas, C, compose, esc          # noqa: E402
from recipes import bar_compare                          # noqa: E402
import column as K                                       # noqa: E402

OUT = os.path.dirname(os.path.abspath(__file__))
PRE = "rc12-fig"


# ══════════════════════════════════════════════════════════
# 像素座標輔助：Canvas 內部是數學座標（y 向上），這裡統一用
# 「左上原點、y 向下」的像素思維，再翻譯回模型座標。
# ══════════════════════════════════════════════════════════
def M_(cv, x, y):
    """像素 (x, y向下) → 模型座標（給 line/poly/polygon/dot/arrow 用）"""
    return (x, cv.h - y)


def pl(cv, a, b, **kw):
    cv.line(M_(cv, *a), M_(cv, *b), **kw)


def pp(cv, pts, **kw):
    cv.poly([M_(cv, *p) for p in pts], **kw)


def pg(cv, pts, **kw):
    cv.polygon([M_(cv, *p) for p in pts], **kw)


def pd(cv, p, **kw):
    cv.dot(M_(cv, *p), **kw)


def pa(cv, a, b, **kw):
    cv.arrow(M_(cv, *a), M_(cv, *b), **kw)


def box(cv, x, y, w, h, fill="#EDF1F6", stroke=C["border"], rx=10, sw=1.4):
    cv.rect_px(x, y, w, h, fill, rx, stroke, sw)


def cv_px(w, h, bg=None):
    """純像素畫布（sx=1，原點在左下）"""
    return Canvas(w, h, sx=1.0, ox=0.0, oy=0.0, bg=bg)


def plotbox(x0, y0, w, h, xlim, ylim):
    """資料 → 像素的線性映射（非等向），畫函數圖一律用這個。"""
    (xa, xb), (ya, yb) = xlim, ylim

    def fx(v):
        return x0 + (v - xa) / (xb - xa) * w

    def fy(v):
        return y0 + h - (v - ya) / (yb - ya) * h
    return fx, fy


def axis_frame(cv, x0, y0, w, h, xlab, ylab, xt, yt, fx, fy,
               grid=True, fmt="{:.0f}"):
    """座標框 + 刻度 + 軸標籤（全部像素座標）"""
    box(cv, x0, y0, w, h, "#FFFFFF", C["border"], 8, 1.4)
    for v in xt:
        X = fx(v)
        if grid:
            pl(cv, (X, y0), (X, y0 + h), color=C["border"], w=1.0, dash="4 4")
        pl(cv, (X, y0 + h), (X, y0 + h + 6), color=C["muted"], w=1.4)
        cv.text_px(X, y0 + h + 20, fmt.format(v), 12, C["muted"])
    for v in yt:
        Y = fy(v)
        if grid:
            pl(cv, (x0, Y), (x0 + w, Y), color=C["border"], w=1.0, dash="4 4")
        pl(cv, (x0 - 6, Y), (x0, Y), color=C["muted"], w=1.4)
        cv.text_px(x0 - 11, Y, fmt.format(v), 12, C["muted"], anchor="end")
    cv.text_px(x0 + w / 2, y0 + h + 44, xlab, 13.5, C["text"], weight="700")
    cv.text_px(x0 - 11, y0 - 16, ylab, 13.5, C["text"], weight="700", anchor="end")


# ── 示範柱的斷面小圖（共用）────────────────────────────────
def draw_section(cv, x0, y0, w, h, bars=True, label=True):
    """畫示範柱斷面（像素）。回傳 d→像素 y 的映射（深度由頂面起算）。"""
    box(cv, x0, y0, w, h, "#EDF1F6", C["member"], 6, 2.6)

    def dy(d):
        return y0 + d / K.H * h
    if bars:
        for d, A in K.LAYERS:
            n = int(round(A / K.AB))
            for i in range(n):
                bx = x0 + w * (0.18 + 0.64 * (i / (n - 1) if n > 1 else 0.5))
                pd(cv, (bx, dy(d)), r=5.0, fill=C["member"], stroke="#FFFFFF", w=1.4)
    if label:
        cv.text_px(x0 + w / 2, y0 - 12, f"{K.B:.0f} × {K.H:.0f} cm", 12, C["muted"])
    return dy


# ══════════════════════════════════════════════════════════
# 圖 1　梁 vs 柱：差在少了一條方程式
# ══════════════════════════════════════════════════════════
def fig1():
    PW, PH = 540, 470

    def panel(is_col):
        cv = cv_px(PW, PH)
        cv.panel("柱（RC-U1-2）" if is_col else "梁（RC-U1-1）",
                 "軸力 P ≠ 0：多一個未知數" if is_col else "軸力 P = 0")
        sx, sy, sh = 48, 104, 176
        sw = sh * K.B / K.H
        dy = draw_section(cv, sx, sy, sw, sh, label=False)
        # 應變圖
        ax0 = sx + sw + 116
        pl(cv, (ax0, sy), (ax0, sy + sh), color=C["ghost"], w=2, dash="5 4")
        c = K.CB if is_col else 0.30 * K.DT
        yc = dy(c)
        wc, wt = 64, 72
        pg(cv, [(ax0, sy), (ax0 + wc, sy), (ax0, yc)],
           fill=C["fill_c"], stroke=C["compr"], w=2.2)
        pg(cv, [(ax0, yc), (ax0 - wt, dy(K.DT)), (ax0, dy(K.DT))],
           fill=C["fill_t"], stroke=C["tension"], w=2.2)
        pl(cv, (ax0 - wt - 12, yc), (ax0 + wc + 16, yc),
           color=C["accent"], w=1.8, dash="6 4")
        cv.text_px(ax0 + wc + 20, yc, "N.A.", 11.5, C["accent"], anchor="start",
                   weight="700")
        cv.math_px(ax0 + wc + 6, sy + 10, "ε_{cu}=0.003", 12, C["compr"],
                   anchor="start", weight="700")
        cv.math_px(ax0 - wt, dy(K.DT) + 22, "ε_{t}", 13, C["tension"],
                   weight="700")
        # 外力
        if is_col:
            pa(cv, (sx + sw / 2, sy - 62), (sx + sw / 2, sy - 6),
               color=C["load"], w=3.6, head=11)
            cv.math_px(sx + sw / 2, sy - 74, "P_{n}", 16, C["load"], weight="700")
        else:
            cv.text_px(sx + sw / 2, sy - 34, "無軸力（P = 0）", 13.5, C["bmd"],
                       weight="700")
        # 帳本
        by = 330
        box(cv, 40, by, PW - 80, 102, "#F5F7FA", C["border"], 12, 1.4)
        if is_col:
            rows = [("未知數", "c 與 P_{n}　（2 個）", C["load"]),
                    ("方程式", "ΣF = 0　（1 條）", C["member"]),
                    ("結果", "掃描 c → 得一整條 (P_{n}, M_{n}) 軌跡", C["compr"])]
        else:
            rows = [("未知數", "只有 c　（1 個）", C["load"]),
                    ("方程式", "C_{c} = T　（1 條）", C["member"]),
                    ("結果", "c 被定死 → M_{n} 是唯一的數字", C["bmd"])]
        for i, (k, v, col) in enumerate(rows):
            yy = by + 26 + i * 27
            cv.text_px(62, yy, k, 12.5, C["muted"], anchor="start", weight="700")
            cv.text_px(140, yy, v, 13.5, col, anchor="start", weight="700")
        return cv

    compose([panel(False), panel(True)],
            title="梁與柱的差別不是「有沒有軸力」，是「少了一條方程式」",
            sub="兩者用的是同一個斷面假設：平面保持平面、混凝土極限應變 0.003",
            note="柱的未知數比方程式多一個，所以答案不是一個點，而是一條 P-M 軌跡。",
            path=f"{OUT}/{PRE}-1-beam-vs-column.svg")


# ══════════════════════════════════════════════════════════
# 圖 2　掃描 c：一條應變直線 → P-M 圖上一個點
# ══════════════════════════════════════════════════════════
def fig2():
    PW, PH = 560, 520
    cs = [K.CONTROL["pure_M"]["c"], K.CONTROL["tc_limit"]["c"], K.CB, K.DT, 1.6 * K.DT]
    cols = [C["tension"], C["bmd"], C["accent"], C["compr"], C["member"]]
    tags = ["①", "②", "③", "④", "⑤"]

    # 左：應變直線家族
    p1 = cv_px(PW, PH)
    p1.panel("同一個斷面，換不同的 c", "每一條直線 = 一種中性軸位置")
    sx, sy, sh = 54, 126, 210
    sw = sh * K.B / K.H
    dy = draw_section(p1, sx, sy, sw, sh, label=False)
    ax0 = sx + sw + 116
    pl(p1, (ax0, sy - 14), (ax0, sy + sh + 14), color=C["ghost"], w=2, dash="5 4")
    W_ = 76
    for c, col, tg in zip(cs, cols, tags):
        # 應變在深度 d 的值：eps(d) = 0.003 (c-d)/c；以 0.003 對應寬度 W_
        def ex(d, c=c):
            return ax0 + 0.003 * (c - d) / c / 0.003 * W_
        e_top, e_bot = ex(0), ex(K.H)
        e_bot = max(e_bot, ax0 - 1.45 * W_)
        pp(p1, [(e_top, sy), (e_bot, sy + sh)], color=col, w=2.6)
        yc = dy(min(c, K.H))
        if c <= K.H:
            pd(p1, (ax0, yc), r=4.6, fill=col, stroke="#FFFFFF", w=1.5)
        p1.text_px(e_bot - 10, sy + sh + 14, tg, 13.5, col, weight="700")
    pl(p1, (ax0 - 1.5 * W_, sy), (ax0 + 1.15 * W_, sy), color=C["muted"], w=1.4)
    pd(p1, (ax0 + W_, sy), r=6.4, fill=C["load"], stroke="#FFFFFF", w=2.0)
    p1.math_px(ax0 + W_ - 12, sy - 20, "\u03b5_{cu}=0.003", 12.5, C["load"],
               anchor="end", weight="700")
    p1.text_px(PW / 2, PH - 58, "所有直線都繞著頂面這一點轉 —— 這就是「掃描」的支點",
               12.5, C["load"], weight="700")
    p1.text_px(ax0 + 1.15 * W_, sy - 18, "壓", 12.5, C["compr"], weight="700")
    p1.text_px(ax0 - 1.5 * W_ + 12, sy - 18, "拉", 12.5, C["tension"], weight="700")
    p1.text_px(PW / 2, PH - 34, "中性軸愈深（c 愈大），斷面受壓的比例愈高",
               12.5, C["muted"])

    # 右：對應的 P-M 點
    p2 = cv_px(PW, PH)
    p2.panel("每一條直線 → 圖上一個點", "把所有點連起來就是 P-M 互制圖")
    x0, y0, w, h = 96, 100, 380, 330
    Mmax, Pmax = 130.0, 1150.0
    fx, fy = plotbox(x0, y0, w, h, (0, Mmax), (0, Pmax))
    axis_frame(p2, x0, y0, w, h, "M_{n}（tf·m）", "P_{n}（tf）",
               [0, 40, 80, 120], [0, 300, 600, 900], fx, fy)
    pts = [(fx(m), fy(p)) for m, pc, p, et, c in K.curve()]
    pp(p2, pts + [(fx(0), fy(K.PO))], color=C["compr"], w=2.8)
    for c, col, tg in zip(cs, cols, tags):
        P, M, _, et = K.engine(c)
        pd(p2, (fx(M), fy(P)), r=6.0, fill=col, stroke="#FFFFFF", w=1.8)
        p2.text_px(fx(M) + 12, fy(P) - 10, tg, 13.5, col, anchor="start", weight="700")
    pd(p2, (fx(0), fy(K.PO)), r=6.0, fill=C["member"], stroke="#FFFFFF", w=1.8)
    p2.text_px(fx(0) + 12, fy(K.PO) + 18, "P_{o}", 12.5, C["member"], anchor="start")

    compose([p1, p2],
            title="「掃描 c」是什麼意思：一條應變直線換一個 (Pn, Mn) 點",
            sub="① 純彎　② 拉力控制界限　③ 平衡點　④ εt = 0　⑤ 全斷面受壓",
            note="柱題所有計算都在做同一件事：假設一個 c，然後做兩次平衡。",
            path=f"{OUT}/{PRE}-2-scan-c.svg")


# ══════════════════════════════════════════════════════════
# 圖 3　唯一計算引擎（以平衡點為例，三聯圖）
# ══════════════════════════════════════════════════════════
def fig3():
    PW, PH = 420, 560
    d = K.CONTROL["balanced"]
    c, a = d["c"], d["a"]
    sy, sh = 140, 268

    # (1) 斷面
    p1 = cv_px(PW, PH)
    p1.panel("① 斷面與配筋", f"8-#9，ρ_g = {K.RHO*100:.2f}%")
    sx, sw = 76, sh * K.B / K.H
    dy = draw_section(p1, sx, sy, sw, sh, label=False)
    p1.dim(M_(p1, sx, sy + sh + 26), M_(p1, sx + sw, sy + sh + 26),
           f"b = {K.B:.0f}", off=0, label_off=-14)
    p1.dim(M_(p1, sx + sw + 26, sy + sh), M_(p1, sx + sw + 26, sy),
           f"h = {K.H:.0f}", off=0, label_off=14)
    for i, (dd, A) in enumerate(K.LAYERS):
        p1.text_px(sx - 12, dy(dd), f"d{i+1}={dd:.0f}", 11.5, C["muted"], anchor="end")
    p1.text_px(PW / 2, 468, f"f'c = {K.FC:.0f}　fy = {K.FY:.0f} kgf/cm²",
               12.5, C["text"], weight="700")
    p1.text_px(PW / 2, 492, f"β_{{1}} = {K.B1:.2f}　A_{{st}} = {K.AST:.2f} cm²",
               12.5, C["muted"])

    # (2) 應變
    p2 = cv_px(PW, PH)
    p2.panel("② 應變：幾何相似三角形", f"取 c = c_b = {c:.2f} cm")
    ax0, W_ = 256, 86
    dy2 = lambda dd: sy + dd / K.H * sh                       # noqa: E731
    pl(p2, (ax0, sy - 16), (ax0, sy + sh + 16), color=C["ghost"], w=2, dash="5 4")
    yc = dy2(c)
    pg(p2, [(ax0, sy), (ax0 + W_, sy), (ax0, yc)],
       fill=C["fill_c"], stroke=C["compr"], w=2.4)
    pg(p2, [(ax0, yc), (ax0 - W_ * (K.H - c) / c, sy + sh), (ax0, sy + sh)],
       fill=C["fill_t"], stroke=C["tension"], w=2.4)
    pl(p2, (ax0 - 120, yc), (ax0 + W_ + 26, yc), color=C["accent"], w=1.8, dash="6 4")
    p2.math_px(ax0 + W_ + 4, sy - 12, "ε_{cu}=0.003", 12, C["compr"],
               anchor="start", weight="700")
    p2.text_px(ax0 + W_ + 30, yc, "N.A.", 11.5, C["accent"], anchor="start", weight="700")
    for r in d["rows"]:
        Y = dy2(r["d"])
        X = ax0 + 0.003 * (c - r["d"]) / c / 0.003 * W_
        pl(p2, (ax0, Y), (X, Y), color=C["muted"], w=1.4, dash="3 3")
        pd(p2, (X, Y), r=4.2, fill=C["accent"], stroke="#FFFFFF", w=1.4)
        col = C["compr"] if r["eps"] > 0 else C["tension"]
        p2.math_px(30, Y, f"ε={r['eps']:+.5f}", 12, col, anchor="start", weight="700")
    p2.math_px(PW / 2, 472, "ε_{i}=0.003(c-d_{i})/c", 13.5, C["text"], weight="700")
    p2.math_px(PW / 2, 494, "f_{si}=clip(E_{s}ε_{i},−f_{y},+f_{y})",
               12.5, C["muted"])

    # (3) 力
    p3 = cv_px(PW, PH)
    p3.panel("③ 力：兩次平衡", f"a = β_{{1}}c = {a:.2f} cm")
    bx0 = 166
    dy3 = lambda dd: sy + dd / K.H * sh                       # noqa: E731
    pl(p3, (bx0, sy - 16), (bx0, sy + sh + 16), color=C["ghost"], w=2, dash="5 4")
    pg(p3, [(bx0, sy), (bx0 + 74, sy), (bx0 + 74, dy3(a)), (bx0, dy3(a))],
       fill=C["fill_c"], stroke=C["compr"], w=2.4)
    p3.math_px(bx0 + 78, sy - 12, "0.85f'_{c}", 12, C["compr"], anchor="start",
               weight="700")
    Cc = 0.85 * K.FC * a * K.B / 1000.0
    pa(p3, (bx0 + 34, dy3(a / 2)), (bx0 + 150, dy3(a / 2)), color=C["compr"],
       w=3.2, head=11)
    p3.math_px(bx0 + 152, dy3(a / 2) - 16, f"C_{{c}}={Cc:.1f}", 13, C["compr"],
               anchor="start", weight="700")
    for r in d["rows"]:
        Y = dy3(r["d"])
        col = C["compr"] if r["F"] > 0 else C["tension"]
        L = 40 + 70 * min(abs(r["F"]) / 90.0, 1.0)
        if r["F"] > 0:
            pa(p3, (bx0 - 6, Y), (bx0 + L, Y), color=col, w=2.8, head=9)
            p3.math_px(bx0 + L + 6, Y - (26 if abs(r["arm"]) < 1e-6 else 0),
                       f"{r['F']:+.1f}", 12, col, anchor="start", weight="700")
        elif r["F"] < 0:
            pa(p3, (bx0 + 6, Y), (bx0 - L, Y), color=col, w=2.8, head=9)
            p3.math_px(bx0 - L - 6, Y, f"{r['F']:+.1f}", 12, col, anchor="end",
                       weight="700")
        else:
            p3.math_px(bx0 + 40, Y, "F = 0", 12, C["muted"], anchor="start")
    pl(p3, (bx0 - 108, dy3(K.H / 2)), (bx0 + 210, dy3(K.H / 2)),
       color=C["accent"], w=1.6, dash="7 4")
    p3.text_px(bx0 - 112, dy3(K.H / 2), "形心", 11.5, C["accent"], anchor="end",
               weight="700")
    box(p3, 40, 452, PW - 80, 70, "#F5F7FA", C["border"], 10, 1.4)
    p3.math_px(PW / 2, 476, f"P_{{n}}=C_{{c}}+ΣF_{{i}}={d['P']:.1f} tf",
               14, C["compr"], weight="700")
    p3.math_px(PW / 2, 502, f"M_{{n}}=Σ(F·arm)={d['M']:.2f} tf·m",
               14, C["bmd"], weight="700")

    compose([p1, p2, p3],
            title="唯一計算引擎：給一個 c，走完這三格就得到 (Pn, Mn)",
            sub=f"示範柱 60×60 cm、8-#9、f'c={K.FC:.0f}、fy={K.FY:.0f}；此處取平衡點 cb",
            note="全單元所有題型共用這台引擎，差別只在「c 從哪裡來」。",
            path=f"{OUT}/{PRE}-3-engine.svg")


# ══════════════════════════════════════════════════════════
# 圖 4　兩個最常掉分的細節：扣 0.85f'c、力臂為零
# ══════════════════════════════════════════════════════════
def fig4():
    PW, PH = 560, 460
    d = K.CONTROL["balanced"]
    a = d["a"]

    p1 = cv_px(PW, PH)
    p1.panel("細節一：應力塊內的壓力筋要扣 0.85f'c", "同一塊面積不能算兩次")
    sx, sy, sh = 70, 112, 236
    sw = sh * K.B / K.H
    dy = draw_section(p1, sx, sy, sw, sh, bars=False, label=False)
    pg(p1, [(sx, sy), (sx + sw, sy), (sx + sw, dy(a)), (sx, dy(a))],
       fill=C["fill_c"], stroke=C["compr"], w=2.2)
    p1.text_px(sx + sw / 2, dy(a) + 20, f"a = {a:.1f} cm", 12, C["compr"], weight="700")
    for dd, A in K.LAYERS:
        n = int(round(A / K.AB))
        inside = dd <= a
        for i in range(n):
            bx = sx + sw * (0.18 + 0.64 * (i / (n - 1) if n > 1 else 0.5))
            pd(p1, (bx, dy(dd)), r=5.0,
               fill=C["load"] if inside else C["member"], stroke="#FFFFFF", w=1.5)
    p1.text_px(sx + sw + 16, dy(K.LAYERS[0][0]), "在 a 內 → 要扣", 12, C["load"],
               anchor="start", weight="700")
    p1.text_px(sx + sw + 16, dy(K.LAYERS[2][0]), "在 a 外 → 不扣", 12, C["member"],
               anchor="start", weight="700")
    box(p1, 44, 378, PW - 88, 62, "#F5F7FA", C["border"], 10, 1.4)
    p1.math_px(PW / 2, 400,
               "d_{i} ≤ a :  F_{i}=A_{si}(f_{si}−0.85f'_{c})",
               13.5, C["load"], weight="700")
    p1.math_px(PW / 2, 424, "d_{i} &gt; a :  F_{i}=A_{si}f_{si}", 13.5, C["member"])

    p2 = cv_px(PW, PH)
    p2.panel("細節二：對形心取矩，中排鋼筋力臂 = 0", "它管 Pn，但完全不管 Mn")
    bx0, by, bh = 300, 112, 250
    dy2 = lambda dd: by + dd / K.H * bh                      # noqa: E731
    pl(p2, (bx0, by - 10), (bx0, by + bh + 10), color=C["ghost"], w=2, dash="5 4")
    pl(p2, (110, dy2(K.H / 2)), (500, dy2(K.H / 2)), color=C["accent"], w=1.8,
       dash="7 4")
    p2.text_px(106, dy2(K.H / 2), "形心 h/2", 12, C["accent"], anchor="end",
               weight="700")
    for r in d["rows"]:
        Y = dy2(r["d"])
        arm = r["arm"]
        col = C["bmd"] if abs(arm) > 1e-6 else C["load"]
        pd(p2, (bx0, Y), r=5.4, fill=C["member"], stroke="#FFFFFF", w=1.5)
        if abs(arm) > 1e-6:
            p2.dim(M_(p2, bx0 + 44, Y), M_(p2, bx0 + 44, dy2(K.H / 2)),
                   f"{abs(arm):.0f} cm", off=0, label_off=16, color=col)
            p2.math_px(bx0 - 20, Y,
                       f"F={r['F']:+.1f} × {arm:+.0f} = {r['F']*arm/100:+.1f}",
                       12, col, anchor="end", weight="700")
        else:
            p2.math_px(bx0 - 20, Y - 24, f"F={r['F']:+.1f} × 0 = 0", 12.5, col,
                       anchor="end", weight="700")
            p2.text_px(bx0 - 20, Y + 24, "力臂 = 0，對 Mn 沒有貢獻", 12,
                       C["load"], anchor="end", weight="700")
    box(p2, 44, 378, PW - 88, 62, "#F5F7FA", C["border"], 10, 1.4)
    p2.math_px(PW / 2, 400,
               "M_{n}=C_{c}(h/2−a/2)+ΣF_{i}(h/2−d_{i})",
               13.5, C["bmd"], weight="700")
    p2.text_px(PW / 2, 424, "中排鋼筋拿掉，Pn 會變、Mn 一點都不變", 12.5, C["muted"])

    compose([p1, p2],
            title="柱題兩個最常掉分的細節",
            sub="這兩處算錯，(Pn, Mn) 會整組偏掉，後面的 φ 判斷也跟著錯",
            note="考場檢查法：把每排鋼筋的「在不在 a 內」與「力臂」先列成表再代。",
            path=f"{OUT}/{PRE}-4-two-details.svg")


# ══════════════════════════════════════════════════════════
# 圖 5　P-M 互制圖全貌（示範柱的四大控制點）
# ══════════════════════════════════════════════════════════
def fig5():
    W, H = 900, 620
    cv = cv_px(W, H, bg="#FFFFFF")
    cv.text_px(W / 2, 34, "示範柱的 P-M 互制圖：四個控制點決定整條曲線",
               18, C["text"], weight="700")
    cv.text_px(W / 2, 58,
               f"60×60 cm、8-#9、f'c={K.FC:.0f}、fy={K.FY:.0f} kgf/cm²",
               13, C["muted"])
    x0, y0, w, h = 110, 96, 520, 440
    fx, fy = plotbox(x0, y0, w, h, (0, 135.0), (-60.0, 1150.0))
    axis_frame(cv, x0, y0, w, h, "M_{n}（tf·m）", "P_{n}（tf）",
               [0, 30, 60, 90, 120], [0, 300, 600, 900, 1100], fx, fy)
    pts = [(fx(m), fy(p)) for m, pc, p, et, c in K.curve()]
    pg(cv, [(fx(0), fy(0))] + pts + [(fx(0), fy(K.PO))],
       fill=C["fill_c"], stroke=C["compr"], w=3.0)
    # 0.80 Po 截平線
    pl(cv, (fx(0), fy(K.PN_MAX)), (fx(135.0), fy(K.PN_MAX)),
       color=C["load"], w=2.0, dash="8 5")
    cv.text_px(fx(135.0), fy(K.PN_MAX) - 14, f"0.80P_o = {K.PN_MAX:.0f} tf",
               12.5, C["load"], anchor="end", weight="700")
    cv.text_px(fx(48), fy(430), "安全區", 15, C["compr"], weight="700")

    marks = [("pure_P", "① 純軸壓 P_o", 14, -18, "start"),
             ("zero_strain", "② ε_t = 0 (c = d_t)", 16, -6, "start"),
             ("balanced", "③ 平衡點 c_b", 18, 0, "start"),
             ("tc_limit", "④ 拉力控制界限 ε_t=0.005", 16, 4, "start"),
             ("pure_M", "⑤ 純彎矩 P_n = 0", 16, 18, "start")]
    for key, lab, dx, dyy, anc in marks:
        d = K.CONTROL[key]
        X, Y = fx(d["M"]), fy(d["P"])
        pd(cv, (X, Y), r=6.4, fill=C["accent"], stroke="#FFFFFF", w=2.0)
        cv.text_px(X + dx, Y + dyy, lab, 12.5, C["accent"], anchor=anc, weight="700")
    # 右側數值表
    tx, ty = 660, 120
    box(cv, tx, ty - 26, 214, 300, "#F5F7FA", C["border"], 12, 1.4)
    cv.text_px(tx + 107, ty - 4, "控制點數值", 13.5, C["text"], weight="700")
    rows = [("① P_o", K.PO, 0.0),
            ("② ε_t=0", K.CONTROL["zero_strain"]["P"],
             K.CONTROL["zero_strain"]["M"]),
            ("③ 平衡點", K.CONTROL["balanced"]["P"],
             K.CONTROL["balanced"]["M"]),
            ("④ ε_t=0.005", K.CONTROL["tc_limit"]["P"],
             K.CONTROL["tc_limit"]["M"]),
            ("⑤ 純彎", 0.0, K.CONTROL["pure_M"]["M"])]
    cv.text_px(tx + 14, ty + 24, "點", 11.5, C["muted"], anchor="start")
    cv.text_px(tx + 128, ty + 24, "Pn (tf)", 11.5, C["muted"], anchor="end")
    cv.text_px(tx + 200, ty + 24, "Mn (tf·m)", 11.5, C["muted"], anchor="end")
    for i, (nm, P, M) in enumerate(rows):
        yy = ty + 52 + i * 30
        cv.text_px(tx + 14, yy, nm, 12.5, C["text"], anchor="start", weight="700")
        cv.text_px(tx + 128, yy, f"{P:.1f}", 12.5, C["compr"], anchor="end")
        cv.text_px(tx + 200, yy, f"{M:.2f}", 12.5, C["bmd"], anchor="end")
    yy = ty + 52 + 5 * 30 + 6
    pl(cv, (tx + 14, yy - 12), (tx + 200, yy - 12), color=C["border"], w=1.2)
    cv.text_px(tx + 14, yy + 8, "最大 M / 純彎 M", 12, C["muted"], anchor="start")
    cv.text_px(tx + 200, yy + 8,
               f"{K.CONTROL['balanced']['M']/K.CONTROL['pure_M']['M']:.2f} 倍",
               13, C["accent"], anchor="end", weight="700")
    cv.text_px(W / 2, H - 22,
               "落在曲線內側 = 安全；落在外側 = 斷面不足。曲線本身與軸力大小無關，是斷面的身分證。",
               13.5, C["muted"])
    cv.save(f"{OUT}/{PRE}-5-pm-curve.svg")


# ══════════════════════════════════════════════════════════
# 圖 6　為什麼會鼓出來：軸力先當幫手、後當兇手
# ══════════════════════════════════════════════════════════
def fig6():
    PW, PH = 480, 520

    def mini(cv, x0, y0, w, h, c, col, cap):
        dy = lambda dd: y0 + dd / K.H * h                    # noqa: E731
        box(cv, x0, y0, w, h, "#EDF1F6", C["member"], 6, 2.2)
        a = min(K.B1 * c, K.H)
        pg(cv, [(x0, y0), (x0 + w, y0), (x0 + w, dy(a)), (x0, dy(a))],
           fill=C["fill_c"], stroke=C["compr"], w=2.0)
        if a < K.H:
            pg(cv, [(x0, dy(a)), (x0 + w, dy(a)), (x0 + w, y0 + h), (x0, y0 + h)],
               fill=C["fill_t"], stroke=C["tension"], w=1.6)
        cv.text_px(x0 + w / 2, y0 + h + 18, cap, 12, col, weight="700")

    # 左：拉力控制區（軸力是幫手）
    p1 = cv_px(PW, PH)
    p1.panel("下半段：軸力是幫手", "c &lt; c_b，斷面大半受拉")
    mini(p1, 74, 108, 124, 124, K.CONTROL["pure_M"]["c"], C["tension"],
         f"純彎 c={K.CONTROL['pure_M']['c']:.1f}")
    mini(p1, 288, 108, 124, 124, K.CB, C["accent"], f"平衡點 c={K.CB:.1f}")
    pa(p1, (216, 170), (272, 170), color=C["load"], w=3.4, head=11)
    p1.math_px(244, 146, "+P_{n}", 13.5, C["load"], weight="700")
    box(p1, 44, 316, PW - 88, 172, "#F5F7FA", C["border"], 12, 1.4)
    for i, t in enumerate([
            "軸壓把受拉區「壓回去」，拉力筋不再那麼快降伏",
            "中性軸下移 → 壓力合力 C_c 變大、力偶臂拉長",
            f"M_n 從 {K.CONTROL['pure_M']['M']:.1f} 一路升到 "
            f"{K.CONTROL['balanced']['M']:.1f} tf·m",
            "⇒ P 與 M 同時增加，曲線往右上鼓出去"]):
        p1.text_px(66, 346 + i * 34, t, 13, C["text"], anchor="start")

    # 右：壓力控制區（軸力是兇手）
    p2 = cv_px(PW, PH)
    p2.panel("上半段：軸力是兇手", "c &gt; c_b，斷面幾乎全壓")
    mini(p2, 74, 108, 124, 124, K.CB, C["accent"], f"平衡點 c={K.CB:.1f}")
    mini(p2, 288, 108, 124, 124, 1.8 * K.DT, C["compr"], "接近純壓")
    pa(p2, (216, 170), (272, 170), color=C["load"], w=3.4, head=11)
    p2.math_px(244, 146, "+P_{n}", 13.5, C["load"], weight="700")
    box(p2, 44, 316, PW - 88, 172, "#F5F7FA", C["border"], 12, 1.4)
    for i, t in enumerate([
            "混凝土的壓力容量被軸力吃掉，能留給彎矩的變少",
            "全斷面受壓 → 力偶臂縮短，拉力側幫不上忙",
            f"M_n 從 {K.CONTROL['balanced']['M']:.1f} 掉到 0（純軸壓 "
            f"P_o = {K.PO:.0f} tf）",
            "⇒ P 增、M 減，曲線收回左上角"]):
        p2.text_px(66, 346 + i * 34, t, 13, C["text"], anchor="start")

    compose([p1, p2],
            title="P-M 圖為什麼會鼓出來？因為軸力在平衡點前後換了立場",
            sub="轉折點就是平衡點：最外層拉力筋恰好降伏（εt = εy）的那一步",
            note=f"對稱配筋柱的標稱最大彎矩必在平衡點，約為純彎矩的 "
                 f"{K.CONTROL['balanced']['M']/K.CONTROL['pure_M']['M']:.1f} 倍。",
            path=f"{OUT}/{PRE}-6-why-bulge.svg")


# ══════════════════════════════════════════════════════════
# 圖 7　入口 A：兩個可以直接讀出來的 c
# ══════════════════════════════════════════════════════════
def fig7():
    PW, PH = 548, 500

    def panel(c, title, sub, formula, val, col, et_lab):
        cv = cv_px(PW, PH)
        cv.panel(title, sub)
        sx, sy, sh = 44, 118, 200
        sw = sh * K.B / K.H
        dy = draw_section(cv, sx, sy, sw, sh, label=False)
        ax0, W_ = sx + sw + 86, 72
        pl(cv, (ax0, sy - 14), (ax0, sy + sh + 14), color=C["ghost"], w=2, dash="5 4")
        yc = dy(c)
        pg(cv, [(ax0, sy), (ax0 + W_, sy), (ax0, yc)],
           fill=C["fill_c"], stroke=C["compr"], w=2.4)
        if c < K.H:
            pg(cv, [(ax0, yc), (ax0 - min(W_ * (K.H - c) / c, 88), sy + sh),
                    (ax0, sy + sh)], fill=C["fill_t"], stroke=C["tension"], w=2.4)
        pl(cv, (ax0 - 72, yc), (ax0 + W_ + 20, yc), color=col, w=2.0, dash="6 4")
        cv.text_px(ax0 + W_ + 24, yc, f"c = {c:.2f} cm", 12.5, col, anchor="start",
                   weight="700")
        pl(cv, (ax0 - 62, dy(K.DT)), (ax0 + 24, dy(K.DT)), color=C["muted"],
           w=1.2, dash="3 3")
        cv.math_px(ax0 - 62, dy(K.DT) + 22, et_lab, 13, C["tension"],
                   weight="700")
        cv.math_px(ax0 + W_ + 4, sy - 12, "ε_{cu}=0.003", 12, C["compr"],
                   anchor="start", weight="700")
        box(cv, 40, 386, PW - 80, 92, "#F5F7FA", C["border"], 12, 1.4)
        cv.math_px(PW / 2, 412, formula, 14.5, col, weight="700")
        cv.math_px(PW / 2, 444, val, 13, C["text"])
        return cv

    d1 = K.CONTROL["zero_strain"]
    d2 = K.CONTROL["balanced"]
    p1 = panel(K.DT, "條件：拉力筋應變為零", "題目說「拉力筋應力 = 0」",
               "ε_{t}=0 ⇒ c = d_{t}",
               f"c = {K.DT:.0f} ⇒ P_{{n}}={d1['P']:.1f} tf,  "
               f"M_{{n}}={d1['M']:.2f} tf·m", C["compr"], "ε_{t}=0")
    p2 = panel(K.CB, "條件：平衡點 / 求最大標稱彎矩", "題目說「拉力筋恰好降伏」",
               "c_{b}=6120/(6120+f_{y})·d_{t}",
               f"c_b = {K.CB:.2f} ⇒ P_{{n}}={d2['P']:.1f} tf,  "
               f"M_{{n}}={d2['M']:.2f} tf·m", C["accent"],
               "ε_{t}=ε_{y}")

    compose([p1, p2],
            title="入口 A：c 直接讀出來，一行就定，不用解方程式",
            sub="SI 制的平衡點公式為 cb = 600/(600+fy)·dt（kgf 制用 6120）",
            note="看到「應變為零」「恰好降伏」「直接給 c」就走這個入口，最省時間。",
            path=f"{OUT}/{PRE}-7-entry-a.svg")


# ══════════════════════════════════════════════════════════
# 圖 8　入口 B：給 Pu 或給偏心距 e，反解二次方程式
# ══════════════════════════════════════════════════════════
def fig8():
    PW, PH = 540, 500

    # 左：偏心距的幾何意義
    p1 = cv_px(PW, PH)
    p1.panel("偏心距 e 的意思：P 與 M 是同一件事", "一個偏心的 P，等於中心的 P 加一個 M")
    cx, cy, cw, ch = 150, 138, 116, 196
    box(p1, cx, cy, cw, ch, "#EDF1F6", C["member"], 6, 2.4)
    pl(p1, (cx + cw / 2, cy - 74), (cx + cw / 2, cy + ch + 14), color=C["ghost"],
       w=1.6, dash="5 4")
    ex = cx + cw / 2 + 62
    pa(p1, (ex, cy - 74), (ex, cy - 6), color=C["load"], w=3.6, head=11)
    p1.math_px(ex + 10, cy - 78, "P_{n}", 15, C["load"], anchor="start", weight="700")
    p1.dim(M_(p1, cx + cw / 2, cy - 22), M_(p1, ex, cy - 22), "e", off=0,
           label_off=-14, color=C["accent"])
    p1.text_px(cx + cw / 2, cy + ch + 26, "偏心受壓（實際受力）", 12.5, C["muted"])
    p1.text_px(306, 236, "≡", 26, C["muted"])
    cx2 = 366
    box(p1, cx2, cy, cw, ch, "#EDF1F6", C["member"], 6, 2.4)
    pa(p1, (cx2 + cw / 2, cy - 74), (cx2 + cw / 2, cy - 6), color=C["load"],
       w=3.6, head=11)
    p1.math_px(cx2 + cw / 2, cy - 86, "P_{n}", 15, C["load"], weight="700")
    p1.moment_arrow(M_(p1, cx2 + cw / 2, cy + 40), r=26, ccw=True, color=C["bmd"],
                    w=2.8, span=250, start=110)
    p1.math_px(cx2 + cw / 2 + 52, cy + 40, "M_{n}=P_{n}e", 13, C["bmd"],
               anchor="start", weight="700")
    p1.text_px(cx2 + cw / 2, cy + ch + 26, "中心壓 + 彎矩（計算模型）", 12.5, C["muted"])
    box(p1, 40, 396, PW - 80, 80, "#F5F7FA", C["border"], 12, 1.4)
    p1.math_px(PW / 2, 420, "e = M_{n}/P_{n}", 15.5, C["accent"], weight="700")
    p1.text_px(PW / 2, 452, "在 P-M 圖上，固定 e 就是一條過原點的射線", 12.5,
               C["muted"])

    # 右：Pn(c) 單調上升 → 反解
    p2 = cv_px(PW, PH)
    p2.panel("反解：令 P_n(c) = P_u/φ，解出 c", "P_n 對 c 單調上升，根唯一")
    x0, y0, w, h = 92, 108, 396, 224
    fx, fy = plotbox(x0, y0, w, h, (0, 2.0 * K.H), (0, 1150.0))
    axis_frame(p2, x0, y0, w, h, "c（cm）", "P_{n}（tf）",
               [0, 30, 60, 90, 120], [0, 300, 600, 900, 1100], fx, fy)
    cs = [0.5 + i * 0.5 for i in range(int(2.0 * K.H / 0.5))]
    pp(p2, [(fx(c), fy(K.engine(c)[0])) for c in cs], color=C["compr"], w=2.8)
    pl(p2, (fx(0), fy(K.PN_DEMO)), (fx(K.C_DEMO), fy(K.PN_DEMO)),
       color=C["load"], w=2.0, dash="7 4")
    pl(p2, (fx(K.C_DEMO), fy(K.PN_DEMO)), (fx(K.C_DEMO), fy(0)),
       color=C["load"], w=2.0, dash="7 4")
    pd(p2, (fx(K.C_DEMO), fy(K.PN_DEMO)), r=6.2, fill=C["accent"],
       stroke="#FFFFFF", w=1.9)
    p2.text_px(fx(0) + 8, fy(K.PN_DEMO) - 12,
               f"P_n = P_u/φ = {K.PN_DEMO:.1f} tf", 12.5, C["load"],
               anchor="start", weight="700")
    p2.text_px(fx(K.C_DEMO) + 8, fy(0) - 16, f"c = {K.C_DEMO:.2f} cm", 12.5,
               C["accent"], anchor="start", weight="700")
    box(p2, 40, 396, PW - 80, 80, "#F5F7FA", C["border"], 12, 1.4)
    p2.math_px(PW / 2, 420,
               f"P_{{u}}={K.PU_DEMO:.0f} tf ⇒ c={K.C_DEMO:.2f} ⇒ "
               f"M_{{n}}={K.M_DEMO:.2f} tf·m", 13.5, C["text"], weight="700")
    p2.math_px(PW / 2, 452,
               f"ε_{{t}}={K.ET_DEMO:+.5f} ⇒ φ={K.PHI_DEMO:.2f} "
               f"⇒ φM_{{n}}={K.PHI_DEMO*K.M_DEMO:.2f} tf·m",
               13, C["muted"])

    compose([p1, p2],
            title="入口 B：題目鎖住了 P 或 e，c 要反解出來",
            sub="把 Cc 與各排鋼筋力都寫成 c 的代數式，整理成 c 的二次方程式",
            note="解出 c 之後一定要回頭驗證每排鋼筋到底降伏了沒有，不可沿用假設。",
            path=f"{OUT}/{PRE}-8-entry-b.svg")


# ══════════════════════════════════════════════════════════
# 圖 9　入口 C：四控制點的應變分佈一次看完
# ══════════════════════════════════════════════════════════
def fig9():
    PW, PH = 384, 480
    keys = [("pure_P", "① 純軸壓 P_o", "全斷面均勻受壓"),
            ("zero_strain", "② ε_t = 0", "c = d_t"),
            ("balanced", "③ 平衡點", "c = c_b"),
            ("pure_M", "④ 純彎矩", "P_n = 0")]
    panels = []
    for key, title, sub in keys:
        d = K.CONTROL[key]
        cv = cv_px(PW, PH)
        cv.panel(title, sub)
        sy, sh, sx = 104, 150, 26
        sw = sh * K.B / K.H
        dy = draw_section(cv, sx, sy, sw, sh, bars=False, label=False)
        for dd, A in K.LAYERS:
            n = int(round(A / K.AB))
            for i in range(n):
                bx = sx + sw * (0.2 + 0.6 * (i / (n - 1) if n > 1 else 0.5))
                pd(cv, (bx, dy(dd)), r=3.8, fill=C["member"], stroke="#FFFFFF", w=1.2)
        ax0, W_ = 268, 54
        pl(cv, (ax0, sy - 12), (ax0, sy + sh + 12), color=C["ghost"], w=2, dash="5 4")
        if key == "pure_P":
            pg(cv, [(ax0, sy), (ax0 + W_, sy), (ax0 + W_, sy + sh), (ax0, sy + sh)],
               fill=C["fill_c"], stroke=C["compr"], w=2.2)
        else:
            c = d["c"]
            yc = dy(min(c, K.H))
            pg(cv, [(ax0, sy), (ax0 + W_, sy), (ax0, yc)],
               fill=C["fill_c"], stroke=C["compr"], w=2.2)
            wt = min(W_ * (K.H - c) / c, 1.5 * W_)
            pg(cv, [(ax0, yc), (ax0 - wt, sy + sh), (ax0, sy + sh)],
               fill=C["fill_t"], stroke=C["tension"], w=2.2)
            cv.text_px(ax0 + W_ + 4, yc, f"c={c:.1f}", 11, C["accent"],
                       anchor="start", weight="700")
        box(cv, 28, 300, PW - 56, 160, "#F5F7FA", C["border"], 12, 1.4)
        cv.math_px(PW / 2, 330, f"P_{{n}} = {d['P']:.1f} tf", 14.5, C["compr"],
                   weight="700")
        cv.math_px(PW / 2, 362, f"M_{{n}} = {d['M']:.2f} tf·m", 14.5, C["bmd"],
                   weight="700")
        if key == "pure_P":
            cv.text_px(PW / 2, 400, "設計時要乘 0.80", 12.5, C["load"], weight="700")
            cv.math_px(PW / 2, 430, f"0.80P_{{o}}={K.PN_MAX:.0f} tf", 13,
                       C["load"])
        else:
            cv.math_px(PW / 2, 400, f"ε_{{t}} = {d['et']:+.5f}", 13,
                       C["muted"])
            cv.text_px(PW / 2, 430, f"{d['zone']}　φ = {d['phi']:.2f}", 13,
                       C["accent"], weight="700")
        panels.append(cv)

    compose(panels, cols=4,
            title="入口 C：要畫 P-M 互制圖，就依序算這四個控制點",
            sub="四點連起來就是整條曲線；考觀念題時照這個順序寫就是完整答案",
            note="純軸壓要再乘 0.80（締箍柱）或 0.85（螺箍柱），保留最小偏心。",
            path=f"{OUT}/{PRE}-9-four-points.svg")


# ══════════════════════════════════════════════════════════
# 圖 10　φ 值分區與設計互制圖
# ══════════════════════════════════════════════════════════
def fig10():
    PW, PH = 560, 500

    # 左：φ 對 ε_t 的三段折線
    p1 = cv_px(PW, PH)
    p1.panel("φ 是「破壞有沒有預警」的價格標籤", "由最外層拉力筋的 ε_t 決定")
    x0, y0, w, h = 96, 116, 400, 228
    fx, fy = plotbox(x0, y0, w, h, (0, 0.008), (0.55, 0.98))
    box(p1, x0, y0, w, h, "#FFFFFF", C["border"], 8, 1.4)
    for v, lab in [(0.0, "0"), (K.EPS_Y, "ε_y"), (0.005, "0.005"),
                   (0.008, "0.008")]:
        X = fx(v)
        pl(p1, (X, y0), (X, y0 + h), color=C["border"], w=1.0, dash="4 4")
        p1.text_px(X, y0 + h + 18, lab, 12, C["muted"])
    for v in [0.65, 0.75, 0.90]:
        Y = fy(v)
        pl(p1, (x0, Y), (x0 + w, Y), color=C["border"], w=1.0, dash="4 4")
        p1.text_px(x0 - 10, Y, f"{v:.2f}", 12, C["muted"], anchor="end")
    # 分區底色
    pg(p1, [(x0, y0), (fx(K.EPS_Y), y0), (fx(K.EPS_Y), y0 + h), (x0, y0 + h)],
       fill=C["fill_c"], stroke="none")
    pg(p1, [(fx(0.005), y0), (x0 + w, y0), (x0 + w, y0 + h), (fx(0.005), y0 + h)],
       fill=C["fill_t"], stroke="none")
    pp(p1, [(fx(0), fy(0.65)), (fx(K.EPS_Y), fy(0.65)), (fx(0.005), fy(0.90)),
            (fx(0.008), fy(0.90))], color=C["accent"], w=3.2)
    pd(p1, (fx(K.EPS_Y), fy(0.65)), r=5.4, fill=C["compr"], stroke="#FFFFFF", w=1.7)
    pd(p1, (fx(0.005), fy(0.90)), r=5.4, fill=C["tension"], stroke="#FFFFFF", w=1.7)
    p1.text_px(fx(K.EPS_Y / 2), y0 + 26, "壓力控制", 12.5, C["compr"], weight="700")
    p1.text_px(fx(0.0034), y0 + 26, "過渡區", 12.5, C["accent"], weight="700")
    p1.text_px(fx(0.0065), y0 + 26, "拉力控制", 12.5, C["tension"], weight="700")
    p1.text_px(fx(0.0011), fy(0.617), "φ = 0.65", 12.5, C["compr"], weight="700")
    p1.text_px(fx(0.0069), fy(0.845), "φ = 0.90", 12.5, C["tension"], weight="700")
    p1.text_px(x0 + w / 2, y0 + h + 42, "ε_t（最外層拉力筋應變）", 13.5,
               C["text"], weight="700")
    p1.text_px(x0 - 10, y0 - 16, "φ", 14, C["text"], anchor="end", weight="700")
    box(p1, 40, 404, PW - 80, 74, "#F5F7FA", C["border"], 12, 1.4)
    p1.math_px(PW / 2, 428,
               "φ=0.65+0.25(ε_{t}−ε_{y})/(0.005−ε_{y})",
               14, C["accent"], weight="700")
    p1.text_px(PW / 2, 458,
               f"本柱 ε_y = {K.EPS_Y:.5f}；螺箍柱壓力控制端改為 0.75",
               12.5, C["muted"])

    # 右：標稱 vs 設計互制圖
    p2 = cv_px(PW, PH)
    p2.panel("標稱曲線 → 設計曲線", "φ 不是常數，曲線會被「不等比例」壓扁")
    x0, y0, w, h = 96, 112, 400, 228
    fx, fy = plotbox(x0, y0, w, h, (0, 135.0), (0, 1150.0))
    axis_frame(p2, x0, y0, w, h, "M（tf·m）", "P（tf）",
               [0, 40, 80, 120], [0, 300, 600, 900, 1100], fx, fy)
    pp(p2, [(fx(m), fy(p)) for m, pc, p, et, c in K.curve()] +
       [(fx(0), fy(K.PO))], color=C["compr"], w=2.6, dash="7 5")
    dc = K.design_curve()
    pg(p2, [(fx(0), fy(0))] + [(fx(m), fy(p)) for m, p, et, c in dc] +
       [(fx(0), fy(0.65 * K.PN_MAX))], fill=C["fill_m"], stroke=C["bmd"], w=3.0)
    p2.text_px(fx(118), fy(820), "標稱 (P_n, M_n)", 12.5, C["compr"], anchor="end",
               weight="700")
    p2.text_px(fx(46), fy(300), "設計 (φP_n, φM_n)", 12.5, C["bmd"],
               weight="700")
    box(p2, 40, 404, PW - 80, 74, "#F5F7FA", C["border"], 12, 1.4)
    p2.text_px(PW / 2, 428,
               f"φP_n 另有上限 φ·0.80P_o = {0.65*K.PN_MAX:.0f} tf",
               13, C["load"], weight="700")
    p2.text_px(PW / 2, 458, "下半段 φ=0.90、上半段 φ=0.65，形狀因此改變",
               12.5, C["muted"])

    compose([p1, p2],
            title="φ 值：先判分區，再決定設計強度",
            sub="εt ≥ 0.005 拉力控制 φ = 0.90；εt ≤ εy 壓力控制 φ = 0.65（矩形締箍柱）",
            note="φ 的判準是最外層鋼筋的 εt，不是平均應變，也不是中排鋼筋。",
            path=f"{OUT}/{PRE}-10-phi-zones.svg")


# ══════════════════════════════════════════════════════════
# 圖 11　陷阱：max(φM_n) ≠ φ·max(M_n)
# ══════════════════════════════════════════════════════════
def fig11():
    W, H = 880, 560
    cv = cv_px(W, H, bg="#FFFFFF")
    cv.text_px(W / 2, 34, "問「最大設計彎矩」時，答案不在平衡點", 18, C["text"],
               weight="700")
    cv.text_px(W / 2, 58,
               "標稱最大 M_n 在平衡點；但 φM_n 的峰值落在拉力控制界限 ε_t = 0.005",
               13, C["muted"])
    x0, y0, w, h = 100, 96, 480, 376
    fx, fy = plotbox(x0, y0, w, h, (0.0, 0.012), (0, 120.0))
    box(cv, x0, y0, w, h, "#FFFFFF", C["border"], 8, 1.4)
    for v, lab in [(0.0, "0"), (K.EPS_Y, "ε_y"), (0.005, "0.005"),
                   (0.008, "0.008"), (0.012, "0.012")]:
        X = fx(v)
        pl(cv, (X, y0), (X, y0 + h), color=C["border"], w=1.0, dash="4 4")
        cv.text_px(X, y0 + h + 18, lab, 12, C["muted"])
    for v in [0, 30, 60, 90, 120]:
        Y = fy(v)
        pl(cv, (x0, Y), (x0 + w, Y), color=C["border"], w=1.0, dash="4 4")
        cv.text_px(x0 - 10, Y, f"{v}", 12, C["muted"], anchor="end")
    cv.text_px(x0 + w / 2, y0 + h + 42, "ε_t（最外層拉力筋應變）", 13.5,
               C["text"], weight="700")
    cv.text_px(x0 - 10, y0 - 16, "彎矩（tf·m）", 13.5, C["text"], anchor="end",
               weight="700")

    samp = [(et, M, K.phi(et) * M) for M, pc, P, et, c in K.curve() if 0 < et <= 0.012]
    samp.sort()
    pp(cv, [(fx(e), fy(m)) for e, m, pm in samp], color=C["compr"], w=2.8)
    pp(cv, [(fx(e), fy(pm)) for e, m, pm in samp], color=C["load"], w=3.2)
    db, dt_ = K.CONTROL["balanced"], K.CONTROL["tc_limit"]
    pd(cv, (fx(db["et"]), fy(db["M"])), r=6.2, fill=C["compr"], stroke="#FFFFFF", w=1.9)
    cv.text_px(fx(db["et"]) + 12, fy(db["M"]) - 14,
               f"M_n 峰值 {db['M']:.1f}（平衡點）", 12.5, C["compr"], anchor="start",
               weight="700")
    pd(cv, (fx(dt_["et"]), fy(dt_["phi"] * dt_["M"])), r=6.2, fill=C["load"],
       stroke="#FFFFFF", w=1.9)
    cv.text_px(fx(dt_["et"]) + 14, fy(dt_["phi"] * dt_["M"]) - 16,
               f"φM_n 峰值 {dt_['phi']*dt_['M']:.1f}", 12.5, C["load"],
               anchor="start", weight="700")
    pd(cv, (fx(db["et"]), fy(db["phi"] * db["M"])), r=5.4, fill=C["muted"],
       stroke="#FFFFFF", w=1.6)
    cv.text_px(fx(db["et"]) + 12, fy(db["phi"] * db["M"]) + 18,
               f"平衡點的 φM_n 只有 {db['phi']*db['M']:.1f}", 12,
               C["muted"], anchor="start")
    cv.legend(x0 + 250, y0 + 28, [(C["compr"], "標稱 M_n"), (C["load"], "設計 φM_n")])

    bx = 612
    box(cv, bx, 110, 236, 330, "#F5F7FA", C["border"], 12, 1.4)
    cv.text_px(bx + 118, 136, "為什麼會這樣", 14, C["text"], weight="700")
    lines = ["過渡區裡 φ 必須走完",
             "0.65 → 0.90（相對 +38%），",
             "而 M_n 在同一段只退約 15%，",
             "乘積一路上升到 φ 觸頂被截平，",
             "形成「折點」極大值。",
             "",
             "⇒ 不能微分求，要分段判斷。",
             "⇒ 只有當軸力可「適當調整」",
             "　 時才有這個陷阱；題目給了",
             "　 P_u、e 或 ε_t 就沒有。"]
    for i, t in enumerate(lines):
        cv.text_px(bx + 18, 168 + i * 26, t, 12.5,
                   C["text"] if i < 5 else C["accent"], anchor="start")
    cv.text_px(W / 2, H - 22,
               "口訣：問「標稱 M_n」→ 平衡點；問「極限／設計彎矩」→ ε_t = 0.005。",
               13.5, C["muted"])
    cv.save(f"{OUT}/{PRE}-11-phimn-peak.svg")


# ══════════════════════════════════════════════════════════
# 圖 12　細長效應：放大彎矩，但 P-M 圖原封不動
# ══════════════════════════════════════════════════════════
def fig12():
    PW, PH = 520, 500

    p1 = cv_px(PW, PH)
    p1.panel("第一關：這根柱算不算細長？", "細長比超過門檻才要放大彎矩")
    cx, base, top = 196, 368, 146
    pl(p1, (cx, top), (cx, base), color=C["ghost"], w=6, cap="butt")
    D = 34
    pp(p1, [(cx + D * (1 - (2 * (y - top) / (base - top) - 1) ** 2), y)
            for y in [top + i * (base - top) / 40 for i in range(41)]],
       color=C["deform"], w=4.6)
    p1.support(M_(p1, cx, base), "pin")
    pa(p1, (cx, top - 58), (cx, top - 6), color=C["load"], w=3.4, head=11)
    p1.math_px(cx + 16, top - 52, "P_{u}", 15, C["load"], anchor="start",
               weight="700")
    p1.dim(M_(p1, cx, (top + base) / 2), M_(p1, cx + D, (top + base) / 2),
           "\u03b4", off=0, label_off=-14, color=C["accent"])
    p1.text_px(cx + D + 26, (top + base) / 2 + 26, "額外彎矩 = P_{u}\u00b7\u03b4",
               13, C["accent"], anchor="start", weight="700")
    p1.dim(M_(p1, cx - 62, base), M_(p1, cx - 62, top), "l_{u}", off=0,
           label_off=-16)
    box(p1, 36, 398, PW - 72, 76, "#F5F7FA", C["border"], 12, 1.4)
    p1.math_px(PW / 2, 422, "kl_{u}/r \u2264 34\u221212(M_{1}/M_{2})", 14,
               C["text"], weight="700")
    p1.text_px(PW / 2, 452, "成立 \u21d2 短柱，直接用 M_{2}；不成立 \u21d2 要放大",
               12.5, C["muted"])

    p2 = cv_px(PW, PH)
    p2.panel("第二關：放大後的 M_c 打進同一張 P-M 圖", "互制圖本身完全不改")
    x0, y0, w, h = 94, 112, 386, 214
    fx, fy = plotbox(x0, y0, w, h, (0, 135.0), (0, 1150.0))
    axis_frame(p2, x0, y0, w, h, "M（tf·m）", "P（tf）", [0, 40, 80, 120],
               [0, 300, 600, 900], fx, fy)
    dc = K.design_curve()
    pg(p2, [(fx(0), fy(0))] + [(fx(m), fy(p)) for m, p, et, c in dc] +
       [(fx(0), fy(0.65 * K.PN_MAX))], fill=C["fill_m"], stroke=C["bmd"], w=2.8)
    Pu, M2 = 300.0, 40.0
    dns = 1.35
    Mc = M2 * dns
    pd(p2, (fx(M2), fy(Pu)), r=6.0, fill=C["muted"], stroke="#FFFFFF", w=1.8)
    p2.text_px(fx(M2) - 10, fy(Pu) + 20, f"(M_2, P_u) = ({M2:.0f}, {Pu:.0f})", 12,
               C["muted"], anchor="end")
    pa(p2, (fx(M2) + 6, fy(Pu)), (fx(Mc) - 6, fy(Pu)), color=C["load"], w=3.0,
       head=10)
    pd(p2, (fx(Mc), fy(Pu)), r=6.4, fill=C["load"], stroke="#FFFFFF", w=1.9)
    p2.text_px(fx(Mc) + 10, fy(Pu) - 22,
               f"M_c = δ_ns·M_2 = {Mc:.0f}", 12.5, C["load"], anchor="start",
               weight="700")
    box(p2, 36, 396, PW - 72, 80, "#F5F7FA", C["border"], 12, 1.4)
    p2.math_px(PW / 2, 420,
               "δ_{ns}=C_{m}/(1−P_{u}/0.75P_{c}) ≥ 1.0", 14,
               C["accent"], weight="700")
    p2.text_px(PW / 2, 452, "細長效應改的是「需求」，不是「容量」", 13,
               C["text"], weight="700")

    compose([p1, p2],
            title="細長效應：只放大需求彎矩，不動 P-M 互制圖",
            sub="考場第一步永遠是先看題目有沒有給 lu、k、βd —— 有給就要檢查細長比",
            note="最常見的錯誤是把 δns 拿去折減斷面強度；它只作用在 M2 上。",
            path=f"{OUT}/{PRE}-12-slenderness.svg")


# ══════════════════════════════════════════════════════════
# 圖 13　合理性檢核尺
# ══════════════════════════════════════════════════════════
def fig13():
    b = K.CONTROL["balanced"]
    z = K.CONTROL["zero_strain"]
    m0 = K.CONTROL["pure_M"]
    bar_compare(
        [("純軸壓 P_o", "斷面軸力的絕對上限，任何 Pn 都不可超過", K.PO,
          f"{K.PO:.0f} tf", C["member"]),
         ("設計上限 0.80P_o", "締箍柱保留最小偏心後的可用軸力", K.PN_MAX,
          f"{K.PN_MAX:.0f} tf", C["load"]),
         ("ε_t = 0 時的 P_n", "全斷面受壓的分界，仍遠低於 P_o", z["P"],
          f"{z['P']:.0f} tf", C["compr"]),
         ("平衡點 P_b", "約為 P_o 的三分之一，是常見的量級", b["P"],
          f"{b['P']:.0f} tf", C["accent"])],
        title="檢核尺一：算出來的 P_n 一定要落在 P_o 之下",
        sub=f"示範柱 60×60 cm、8-#9、f'c = {K.FC:.0f} kgf/cm²",
        note="Pn 若算出比 Po 大，一定是 a 超過 h 沒截斷或鋼筋力正負號寫反。",
        path=f"{OUT}/{PRE}-13-check-axial.svg")

    bar_compare(
        [("平衡點 M_b", "對稱配筋柱的標稱最大彎矩", b["M"], f"{b['M']:.1f} tf·m",
          C["accent"]),
         ("ε_t=0.005 的 M_n", "拉力控制界限，M_n 已從峰值退下來",
          K.CONTROL["tc_limit"]["M"], f"{K.CONTROL['tc_limit']['M']:.1f} tf·m",
          C["bmd"]),
         ("純彎矩 M_0", "P_n = 0，相當於把柱當梁算", m0["M"],
          f"{m0['M']:.1f} tf·m", C["tension"]),
         ("ε_t = 0 的 M_n", "已進入壓力控制深處，彎矩容量掉回純彎水準",
          z["M"], f"{z['M']:.1f} tf·m", C["compr"])],
        title="檢核尺二：最大彎矩約為純彎矩的 2 倍",
        sub=f"本柱 M_b / M_0 = {b['M']/m0['M']:.2f}（常見範圍 1.8 – 2.2）",
        note="算出來若只有 1.1 倍或高到 3 倍以上，多半是鋼筋排數或力臂弄錯了。",
        path=f"{OUT}/{PRE}-14-check-moment.svg")


# ══════════════════════════════════════════════════════════
if __name__ == "__main__":
    for fn in (fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9, fig10,
               fig11, fig12, fig13):
        fn()
        print("ok", fn.__name__)
    print("\n── 示範數值總表 ───────────────────────────────")
    os.system(f"python3 {OUT}/column.py")
