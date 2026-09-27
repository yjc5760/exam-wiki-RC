"""RC-U4-1 拼圖二：兩階段 × 四控制點 — 向量圖（所有數值由 params.py 算出）"""
import math
from helpers import *
from params import *

TEAL = "#2C6E9E"
ORGBG = "#FCEEE5"
LIM = "#7A3E9D"          # 容許線顏色


def band(g, x1, x2, ym, amp, th, up):
    n = 40; top, bot = [], []
    for i in range(n + 1):
        t = i/n; d = amp*math.sin(math.pi*t)*(-1 if up else 1)
        xx = x1 + (x2 - x1)*t
        top.append((xx, ym - th/2 + d)); bot.append((xx, ym + th/2 + d))
    g.poly(top + bot[::-1], INK, 2, fill=CONC, closed=True)
    g.line(x1, ym, x2, ym, "#AEB6C2", 1.4, dash="7 5")
    return top, bot


def badge(g, cx, cy, n, col, r=19, size=19):
    g.circle(cx, cy, r, fill=col, stroke=W, sw=2)
    g.text(cx, cy + size*0.36, n, size, W, anchor="middle", weight="bold")


def mark(g, x, y, kind, r=12, sw=3.6):
    """kind: ok / ng / dash ; (x,y) 為中心"""
    if kind == "ok":
        g.poly([(x - r, y), (x - r*0.3, y + r*0.75), (x + r, y - r*0.8)], GREEN, sw)
    elif kind == "ng":
        g.line(x - r*0.8, y - r*0.8, x + r*0.8, y + r*0.8, RED, sw, cap="round")
        g.line(x - r*0.8, y + r*0.8, x + r*0.8, y - r*0.8, RED, sw, cap="round")
    else:
        g.line(x - r*0.7, y, x + r*0.7, y, MUTED, sw, cap="round")


# ───────── fig01 總覽 ─────────
def fig01():
    g = SVG(1200, 440)
    # 左：兩個趨勢
    card(g, 20, 20, 330, 400, PANEL, "#D5DAE1")
    g.text(185, 58, "兩個反向的趨勢", 20, INK, anchor="middle", weight="bold")
    g.arrow(60, 110, 300, 170, ORG, 4, 16)
    g.text(60, 98, f"預力 P：{PI_T:.0f} → {PE_T:.0f} t", 17, ORG, weight="bold")
    g.text(300, 195, "一路變小（損失）", 15, ORG, anchor="end")
    g.arrow(60, 320, 300, 250, RED, 4, 16)
    g.text(60, 350, f"彎矩 M：{MD:.2f} → {MT:.2f} t-m", 17, RED, weight="bold")
    g.text(60, 376, "一路變大（加載）", 15, RED)
    g.text(185, 405, f"強度 f′：{FCI:.0f} → {FC:.0f}（變強）", 15, TEAL, anchor="middle", weight="bold")
    g.arrow(360, 220, 410, 220, MUTED, 2.6, 13)
    # 中：兩個時刻
    for i, (t, sub, c, bg) in enumerate([("傳遞 Transfer", "P_i 最大 ＋ 只有 M_d", BLUE, BLUEBG),
                                          ("使用 Service", "P_e 最小 ＋ M_T 最大", RED, REDBG)]):
        y = 40 + i*200
        card(g, 420, y, 330, 160, bg, c, 12, 2)
        g.text(585, y + 50, t, 22, c, anchor="middle", weight="bold")
        g.text(585, y + 92, sub, 17, INK, anchor="middle")
        g.text(585, y + 128, "梁被頂成上拱" if i == 0 else "梁被壓成下垂", 16, MUTED, anchor="middle")
    g.text(585, 222, "兩個最不利的時刻", 16, PUR, anchor="middle", weight="bold")
    g.arrow(760, 120, 810, 120, MUTED, 2.6, 13); g.arrow(760, 320, 810, 320, MUTED, 2.6, 13)
    # 右：四控制點
    pts = [("①", "頂纖維", "拉", F1, 40, BLUEBG, RED), ("②", "底纖維", "壓", F2, 130, BLUEBG, BLUE),
           ("③", "頂纖維", "壓", F3, 240, REDBG, BLUE), ("④", "底纖維", "拉", F4, 330, REDBG, RED)]
    for n, fib, kind, v, y, bg, c in pts:
        card(g, 820, y, 360, 78, bg, "#D5DAE1", 10)
        badge(g, 856, y + 39, n, ORG)
        g.text(890, y + 34, f"{fib}　怕{'拉裂' if kind == '拉' else '壓碎'}", 18, INK, weight="bold")
        g.text(890, y + 62, f"本例 {sg(v)} kgf/cm²", 15, c, weight="bold")
    g.text(1000, 432, "四點是「且」：全部通過才算合格", 15, PUR, anchor="middle", weight="bold")
    g.save("figs/fig01_map.svg")


# ───────── fig02 時間軸：三條曲線 ─────────
def fig02():
    g = SVG(1200, 470)
    x0, x1 = 170, 1080
    xs = [x0, 560, x1]           # 放張、損失完成、加活載
    labs = ["放張（傳遞）", "長期損失完成", "加上活載（使用）"]
    rows = [("預力 P（t）", ORG, 30), ("彎矩 M（t-m）", RED, 170), ("混凝土強度（kgf/cm²）", TEAL, 310)]
    for t, c, y in rows:
        g.rect(x0 - 10, y, x1 - x0 + 20, 118, fill=PANEL, stroke="none", rx=8)
        g.text(20, y + 64, t, 16, c, weight="bold")
    # 兩個時刻高亮
    for x, c in [(x0, BLUE), (x1, RED)]:
        g.rect(x - 26, 18, 52, 418, fill=c, stroke="none", rx=10, op=0.10)
    # P：先快後慢衰減
    yP = lambda p: 30 + 20 + (150 - p)/40*80
    pts = [(x0 + (xs[1] - x0)*i/30, yP(PE_T + (PI_T - PE_T)*math.exp(-4*i/30*1.2))) for i in range(31)]
    pts[-1] = (xs[1], yP(PE_T)); pts += [(x1, yP(PE_T))]
    g.poly(pts, ORG, 4)
    g.text(x0 + 30, yP(PI_T) - 4, f"P_i = {PI_T:.0f}", 17, ORG, weight="bold")
    g.text(x1 - 8, yP(PE_T) - 10, f"P_e = {PE_T:.0f}（{R*100:.0f}%）", 17, ORG, anchor="end", weight="bold")
    # M：先平再跳
    yM = lambda m: 170 + 105 - m/60*90
    g.poly([(x0, yM(MD)), (xs[1] + 200, yM(MD)), (xs[1] + 260, yM(MT)), (x1, yM(MT))], RED, 4)
    g.text(x0 + 30, yM(MD) - 10, f"M_d = {MD:.2f}", 17, RED, weight="bold")
    g.text(x1 - 8, yM(MT) + 26, f"M_T = M_d + M_L = {MT:.2f}", 17, RED, anchor="end", weight="bold")
    # 強度
    yF = lambda f: 310 + 100 - (f - 260)/100*85
    pts = [(x0 + (x1 - x0)*i/30, yF(FC - (FC - FCI)*math.exp(-5*i/30))) for i in range(31)]
    g.poly(pts, TEAL, 4)
    g.text(x0 + 30, yF(FCI) + 4, f"f′_{{ci}} = {FCI:.0f}", 17, TEAL, weight="bold")
    g.text(x1 - 8, yF(FC) + 30, f"f′_c = {FC:.0f}（28 天）", 17, TEAL, anchor="end", weight="bold")
    for x, t in zip(xs, labs):
        g.line(x, 24, x, 432, AX, 1.2, dash="5 4")
        g.text(x, 458, t, 16, INK, anchor="middle", weight="bold")
    g.text(x0, 14 + 0, "", 10)
    g.save("figs/fig02_timeline.svg")


# ───────── fig03 應力路徑：極值在兩端 ─────────
def fig03():
    g = SVG(1200, 470)
    X = [250, 600, 950]; s = 1.35
    Y = lambda f: 330 - f*s
    # 容許帶（傳遞：放張當下；之後混凝土已達 f′c）
    g.rect(X[0] - 110, Y(FCI_A), 220, Y(-FTI_A) - Y(FCI_A), fill=GREENBG, stroke=GREEN, sw=1.2, rx=6)
    g.rect(X[1] - 110, Y(FCS_A), 460, Y(-FTS_A) - Y(FCS_A), fill=GREENBG, stroke=GREEN, sw=1.2, rx=6)
    for x, (hi, lo) in [(X[0], (FCI_A, -FTI_A)), (X[1] + 175, (FCS_A, -FTS_A))]:
        g.text(x, Y(hi) - 8, f"容許壓 +{hi:.0f}", 14, GREEN, anchor="middle", weight="bold")
        g.text(x, Y(lo) + 22, f"容許拉 −{-lo:.2f}", 14, GREEN, anchor="middle", weight="bold")
    g.line(130, Y(0), 1110, Y(0), AX, 1.6)
    g.text(126, Y(0) + 5, "0", 14, MUTED, anchor="end")
    top = [F1, B1, F3]; bot = [F2, B2, F4]
    g.poly([(X[i], Y(top[i])) for i in range(3)], PUR, 3.2)
    g.poly([(X[i], Y(bot[i])) for i in range(3)], ORG, 3.2)
    for i in range(3):
        for v, c in [(top[i], PUR), (bot[i], ORG)]:
            g.circle(X[i], Y(v), 7, fill=c)
    g.text(X[0] - 18, Y(F1) + 6, f"頂 {sg(F1)}", 16, PUR, anchor="end", weight="bold")
    g.text(X[0] - 18, Y(F2) + 6, f"底 {sg(F2)}", 16, ORG, anchor="end", weight="bold")
    g.text(X[1], Y(B1) + 26, f"頂 {sg(B1)}", 15, PUR, anchor="middle")
    g.text(X[1], Y(B2) - 14, f"底 {sg(B2)}", 15, ORG, anchor="middle")
    g.text(X[2] + 18, Y(F3) + 6, f"頂 {sg(F3)}", 16, PUR, weight="bold")
    g.text(X[2] + 18, Y(F4) + 6, f"底 {sg(F4)}", 16, ORG, weight="bold")
    for n, x, v in [("①", X[0], F1), ("②", X[0], F2), ("③", X[2], F3), ("④", X[2], F4)]:
        badge(g, x + (48 if x == X[0] else -44), Y(v) + (-22 if (v > 0 or x == X[0]) else 22), n, ORG, 15, 15)
    labs = [("P_i ＋ M_d", "傳遞（極端一）"), ("P_e ＋ M_d", "損失完成、無活載"), ("P_e ＋ M_T", "使用（極端二）")]
    for x, (a, b) in zip(X, labs):
        g.text(x, 440, a, 17, INK, anchor="middle", weight="bold")
        g.text(x, 464, b, 15, MUTED, anchor="middle")
    g.text(1150, 400, "頂纖維", 16, PUR, anchor="end", weight="bold"); g.line(1070, 394, 1094, 394, PUR, 4)
    g.text(1150, 424, "底纖維", 16, ORG, anchor="end", weight="bold"); g.line(1070, 418, 1094, 418, ORG, 4)
    g.save("figs/fig03_paths.svg")


# ───────── fig04 / fig05 兩階段物理 ─────────
def stage_phys(fn, up):
    g = SVG(1200, 420)
    x1, x2, ym = 60, 640, 200
    top, bot = band(g, x1, x2, ym, 34, 46, up)
    pin(g, x1 + 12, ym + 23); roller(g, x2 - 12, ym + 23)
    # 鋼腱
    xt = [x1 + (x2 - x1)*i/40 for i in range(41)]
    d = lambda t: 34*math.sin(math.pi*t)*(-1 if up else 1)
    g.poly([(x, ym + 14 + d((x - x1)/(x2 - x1))) for x in xt], ORG, 3)
    P = "P_i" if up else "P_e"
    g.arrow(x1 - 10, ym + 14, x1 - 55, ym + 14, ORG, 3, 13); g.arrow(x2 + 10, ym + 14, x2 + 55, ym + 14, ORG, 3, 13)
    g.text(x2 + 30, ym - 4, P, 20, ORG, anchor="middle", weight="bold", italic=True)
    if up:
        yl = ym - 23 - 34 - 44
        g.line(x1 + 20, yl, x2 - 20, yl, "#8C96A3", 2)
        for i in range(11):
            xx = x1 + 20 + (x2 - x1 - 40)*i/10
            g.arrow(xx, yl, xx, ym - 23 + d((xx - x1)/(x2 - x1)) - 3, "#8C96A3", 1.8, 9)
        g.text(350, yl - 12, f"僅自重 w_d = {WD:.3f} t/m", 16, "#6B7280", anchor="middle", weight="bold")
        g.text(350, 350, "預力主導 → 梁被頂成上拱", 19, BLUE, anchor="middle", weight="bold")
        danger = [("頂纖維", "被拉開（−）", RED, ym - 23 - 34 - 70), ("底纖維", "被壓緊（＋）", BLUE, ym + 23 - 34 + 130)]
    else:
        udl(g, x1 + 40, x2 - 40, ym - 23 + 34 - 50, 11, RED, f"全載重 w_d + w_L = {WD + WL:.3f} t/m", 16)
        g.text(350, 350, "載重主導 → 梁被壓成下垂", 19, RED, anchor="middle", weight="bold")
        danger = []
    # 右側資訊卡
    X = 700
    rows = ([("預力", f"P_i = {PI_T:.0f} t（最大，尚未損失）", ORG),
             ("彎矩", f"M_d = {MD:.3f} t-m（只有自重）", RED),
             ("強度", f"f′_{{ci}} = {FCI:.0f}（放張齡期，還嫩）", TEAL),
             ("危險", "頂纖維受拉 ①；底纖維受壓 ②", PUR)] if up else
            [("預力", f"P_e = {PE_T:.0f} t（已扣 {100 - R*100:.0f}% 損失）", ORG),
             ("彎矩", f"M_T = M_d + M_L = {MT:.3f} t-m", RED),
             ("強度", f"f′_c = {FC:.0f}（28 天設計強度）", TEAL),
             ("危險", "底纖維受拉 ④；頂纖維受壓 ③", PUR)])
    for i, (a, b, c) in enumerate(rows):
        y = 40 + i*88
        card(g, X, y, 480, 74, W if i < 3 else PURBG, "#D5DAE1" if i < 3 else "#C9BCEB", 10)
        g.text(X + 20, y + 46, a, 18, c, weight="bold")
        g.text(X + 80, y + 46, b, 17, INK, weight="bold" if i == 3 else "normal")
    # 凸面標示
    if up:
        g.text(350, 40, "凸面在頂 → 頂纖維被拉開", 16, RED, anchor="middle", weight="bold")
    else:
        g.text(350, ym + 115, "凸面在底 → 底纖維被拉開", 16, RED, anchor="middle", weight="bold")
    g.save(f"figs/{fn}.svg")


# ───────── fig06 四控制點矩陣 ─────────
def fig06():
    g = SVG(1200, 440)
    cx = [360, 800]; cy = [110, 290]
    g.text(360, 40, "頂纖維", 21, INK, anchor="middle", weight="bold")
    g.text(800, 40, "底纖維", 21, INK, anchor="middle", weight="bold")
    g.text(80, 115, "傳遞", 22, BLUE, anchor="middle", weight="bold")
    g.text(80, 143, "P_i、M_d、f′_{ci}", 15, MUTED, anchor="middle")
    g.text(80, 295, "使用", 22, RED, anchor="middle", weight="bold")
    g.text(80, 323, "P_e、M_T、f′_c", 15, MUTED, anchor="middle")
    cells = [
        (0, 0, "①", "拉", F1, -FTI_A, "−0.80√f′_{ci}", True),
        (0, 1, "②", "壓", F2, FCI_A, "+0.60 f′_{ci}", False),
        (1, 0, "③", "壓", F3, FCS_A, "+0.60 f′_c", False),
        (1, 1, "④", "拉", F4, -FTS_A, "−2.0√f′_c", True),
    ]
    for r, c, n, kind, v, lim, ftxt, tens in cells:
        x, y = cx[c] - 200, cy[r] - 62
        bg, bd = (REDBG, RED) if tens else (BLUEBG, BLUE)
        card(g, x, y, 400, 150, bg, bd, 14, 2.2 if tens else 1.4)
        badge(g, x + 38, y + 40, n, ORG, 21, 21)
        g.text(x + 72, y + 48, f"怕{'拉裂' if tens else '壓碎'}", 20, bd, weight="bold")
        g.text(x + 380, y + 48, "拉力控制點" if tens else "壓力檢核點", 14, MUTED, anchor="end")
        g.text(x + 30, y + 95, f"算得 {sg(v)}", 20, INK, weight="bold")
        g.text(x + 30, y + 130, f"容許 {sg(lim)}（{ftxt}）", 17, GREEN, weight="bold")
        g.text(x + 380, y + 130, "OK", 20, GREEN, anchor="end", weight="bold")
    g.text(580, 432, "紅框（拉）通常是控制點；藍框（壓）在 P_i 很大或 f′_{ci} 很低時也會爆", 16, MUTED, anchor="middle")
    g.save("figs/fig06_matrix.svg")


# ───────── fig07 單位換算 ─────────
def fig07():
    g = SVG(1200, 400)
    card(g, 20, 20, 1160, 110, PANEL, "#D5DAE1", 12)
    g.text(50, 62, "為什麼只有 √f′ 的係數要換？", 20, INK, weight="bold")
    g.text(50, 100, "0.60 f′_c 是「倍數」：單位跟著 f′_c 走，換不換制都是 0.60；√f′_c 開根號後單位變成 √(應力)，係數必須吸收換算。", 16, MUTED)
    # 換算鏈
    boxes = [("ACI（MPa 制）", "f_t = 0.25√f′_{ci}", BLUE, BLUEBG),
             ("代入 1 MPa = 10.197 kgf/cm²", "×√10.197 = ×3.193", GOLD, GOLDBG),
             ("土木 401（kgf/cm² 制）", "f_t = 0.80√f′_{ci}", GREEN, GREENBG)]
    for i, (a, b, c, bg) in enumerate(boxes):
        x = 40 + i*390
        card(g, x, 160, 340, 110, bg, c, 12, 2)
        g.text(x + 170, 198, a, 17, c, anchor="middle", weight="bold")
        g.text(x + 170, 245, b, 23, INK, anchor="middle", weight="bold")
        if i < 2: g.arrow(x + 348, 215, x + 382, 215, MUTED, 2.6, 12)
    rows = [("傳遞拉（跨中）", "0.25", f"{0.25*CONV:.2f}", "0.80"),
            ("傳遞拉（簡支端部）", "0.50", f"{0.50*CONV:.2f}", "1.6"),
            ("使用拉（Class U 上限）", "0.62", f"{0.62*CONV:.2f}", "2.0")]
    g.text(60, 312, "係數對照", 17, INK, weight="bold")
    for i, (a, m, k, r) in enumerate(rows):
        x = 180 + i*335
        g.text(x, 312, a, 15, MUTED)
        g.text(x, 344, f"{m} × 3.193 = {k} → {r}", 18, INK, weight="bold")
    g.text(600, 388, "直接把 MPa 的 0.62 用在 kgf/cm² 題目 → 容許拉應力只剩 1/3.19，嚴重低估", 16, RED, anchor="middle", weight="bold")
    g.save("figs/fig07_units.svg")


# ───────── fig08 / fig09 疊加 + 容許線 ─────────
def check_fig(fn, t1, t2, t3, lim_c, lim_t, tag, nums):
    g = SVG(1200, 460)
    yt, yb = 110, 350
    ft, fb = t1 - t2 + t3, t1 + t2 - t3
    s = 0.62
    k = (yb - yt)/H; sx = 40; bw = B*k
    block(g, sx, yt, bw, yb - yt)
    cy = (yt + yb)/2; g.line(sx - 10, cy, sx + bw + 20, cy, AX, 1.2, dash="6 4")
    g.circle(sx + bw/2, cy + E*k, 7, fill=ORG, stroke=W)
    g.text(sx + bw/2, yt - 16, "跨中", 17, INK, anchor="middle", weight="bold")
    g.text(40, 34, tag, 19, PUR, weight="bold")
    cols = [(250, "P/A", t1, t1), (430, "P·e/S", -t2, t2), (620, "M/S", t3, -t3)]
    for i, (x, hd, a, b) in enumerate(cols):
        ax = x - 30 if i == 0 else x
        stress(g, ax, yt, yb, a, b, s*0.8, 2.2)
        g.text(x, yt - 44, hd, 18, [BLUE, ORG, RED][i], anchor="middle", weight="bold")
        vlab(g, x, yb + 36, a, "頂 ", 15); vlab(g, x, yb + 62, b, "底 ", 15)
        g.text(x + 95, cy + 12, "+" if i < 2 else "=", 30, "#7A8594", anchor="middle", weight="bold")
    # 合成 + 容許線
    ax = 860
    g.rect(ax - lim_t*s, yt - 12, (lim_c + lim_t)*s, yb - yt + 24, fill=GREENBG, stroke="none")
    for v, t in [(lim_c, f"+{lim_c:.0f}"), (-lim_t, f"−{lim_t:.2f}")]:
        g.line(ax + v*s, yt - 20, ax + v*s, yb + 20, GREEN, 2, dash="6 4")
        g.text(ax + v*s, yb + 40, t, 14, GREEN, anchor="middle", weight="bold")
    stress(g, ax, yt, yb, ft, fb, s, 2.8)
    g.text(ax + 40, yt - 44, "合成 vs 容許", 18, GREEN, anchor="middle", weight="bold")
    # 右側兩張結果卡
    for i, (n, fib, v, lim) in enumerate(nums):
        y = 60 + i*170
        card(g, 1000, y, 190, 150, W, "#D5DAE1", 12)
        badge(g, 1030, y + 34, n, ORG, 18, 18)
        g.text(1058, y + 41, fib, 17, INK, weight="bold")
        vlab(g, 1095, y + 84, v, "", 24)
        g.text(1095, y + 112, f"容許 {sg(lim)}", 14, GREEN, anchor="middle", weight="bold")
        g.text(1095, y + 136, f"使用率 {abs(v/lim)*100:.0f}%　OK", 14, GREEN, anchor="middle")
        g.line(1000, y + 75 if False else y + 0, 1000, y, W, 0)
    legend(g, 40, 445, 14)
    g.save(f"figs/{fn}.svg")


# ───────── fig10 容許窗 ─────────
def fig10():
    g = SVG(1200, 400)
    x0, s = 330, 3.5    # f=0 位置、px/unit
    X = lambda f: x0 + f*s
    for r, (tag, lo, hi, a, b, c1, c2, sub) in enumerate([
            ("傳遞", -FTI_A, FCI_A, F1, F2, "①", "②", "f′_{ci} = 280"),
            ("使用", -FTS_A, FCS_A, F4, F3, "④", "③", "f′_c = 350")]):
        y = 110 + r*170
        g.text(40, y + 6, tag, 22, BLUE if r == 0 else RED, weight="bold")
        g.text(40, y + 34, sub, 14, MUTED)
        g.line(X(-50), y, X(222), y, AX, 2)
        g.rect(X(lo), y - 22, X(hi) - X(lo), 44, fill=GREENBG, stroke=GREEN, sw=1.6, rx=6)
        g.text(X(lo), y + 48, f"−{-lo:.2f}", 15, GREEN, anchor="middle", weight="bold")
        g.text(X(hi), y + 48, f"+{hi:.0f}", 15, GREEN, anchor="middle", weight="bold")
        g.line(X(0), y - 30, X(0), y + 30, AX, 1.4)
        g.text(X(0), y + 48, "0", 14, MUTED, anchor="middle")
        for n, v, up in [(c1, a, True), (c2, b, False)]:
            g.line(X(v), y - 22, X(v), y + 22, RED if v < 0 else BLUE, 4)
            yy = y - 50 if up else y - 50
            badge(g, X(v), yy, n, ORG, 15, 15)
            g.text(X(v) + (22 if v > 0 else -22), yy + 6, sg(v), 16, RED if v < 0 else BLUE,
                   anchor="start" if v > 0 else "end", weight="bold")
        g.text(X(222) + 10, y + 6, "壓 →", 15, BLUE, weight="bold")
        g.text(X(-50) - 10, y + 6, "← 拉", 15, RED, anchor="end", weight="bold")
    g.text(600, 30, "綠色窗 = 規範允許的應力範圍；兩個纖維的應力都要落在窗內", 18, INK, anchor="middle", weight="bold")
    g.text(600, 390, "拉側的窗很窄（拉側寬度只有壓側的 1/6～1/13）→ 拉力控制點最容易先出界", 16, RED, anchor="middle", weight="bold")
    g.save("figs/fig10_window.svg")


# ───────── fig11 串料的後果 ─────────
def fig11():
    g = SVG(1200, 470)
    g.text(330, 36, "M_d（只有自重）", 19, INK, anchor="middle", weight="bold")
    g.text(830, 36, "M_T（全載重）", 19, INK, anchor="middle", weight="bold")
    g.text(60, 145, "P_i", 24, ORG, anchor="middle", weight="bold", italic=True)
    g.text(60, 340, "P_e", 24, ORG, anchor="middle", weight="bold", italic=True)
    cells = [
        (0, 0, "ok|傳遞階段", F1, F2, GREEN, GREENBG, "①②：這才是傳遞要檢核的組合"),
        (0, 1, "ng|串料（不存在的組合）", X1, X2, RED, REDBG, f"底只有 {sg(X2)}：把 ④ 少算 {X2 - F4:.2f}"),
        (1, 0, "dash|中間狀態", B1, B2, GOLD, GOLDBG, "長期無活載：不是極端，不控制"),
        (1, 1, "ok|使用階段", F3, F4, GREEN, GREENBG, "③④：這才是使用要檢核的組合"),
    ]
    for r, c, t, a, b, col, bg, note in cells:
        x, y = 110 + c*500, 60 + r*195
        card(g, x, y, 460, 180, bg, col, 14, 2)
        mk, t = t.split("|")
        mark(g, x + 36, y + 31, mk, 11)
        g.text(x + 58, y + 38, t, 20, col, weight="bold")
        stress(g, x + 120, y + 58, y + 146, a, b, 0.55, 2)
        vlab(g, x + 250, y + 90, a, "頂 ", 18, "start"); vlab(g, x + 250, y + 132, b, "底 ", 18, "start")
        g.text(x + 24, y + 172, note, 14, INK)
    g.text(600, 462, "拿錯 P 或 M，數字看起來都「很安全」——串料的錯誤永遠是偏不保守", 17, RED, anchor="middle", weight="bold")
    g.save("figs/fig11_mix.svg")


# ───────── fig12 使用率 ─────────
def fig12():
    g = SVG(1200, 380)
    x0, wmax = 330, 690
    rows = [("①", "傳遞 · 頂（拉）", -F1, FTI_A, RED), ("②", "傳遞 · 底（壓）", F2, FCI_A, BLUE),
            ("③", "使用 · 頂（壓）", F3, FCS_A, BLUE), ("④", "使用 · 底（拉）", -F4, FTS_A, RED)]
    for i, (n, t, v, lim, c) in enumerate(rows):
        y = 40 + i*78
        badge(g, 50, y + 22, n, ORG, 18, 18)
        g.text(80, y + 29, t, 18, INK, weight="bold")
        g.rect(x0, y, wmax, 44, fill=PANEL, stroke="#D5DAE1", sw=1, rx=6)
        u = v/lim
        g.rect(x0, y, wmax*u, 44, fill=c, stroke="none", rx=6, op=0.85 if i == 3 else 0.55)
        g.text(x0 + wmax*u - 12, y + 29, f"{u*100:.0f}%", 18, W, anchor="end", weight="bold")
        g.text(x0 + wmax + 16, y + 29, f"{v:.2f} / {lim:.2f}", 16, MUTED)
    g.line(x0 + wmax, 30, x0 + wmax, 350, GREEN, 2.4, dash="6 4")
    g.text(x0 + wmax, 370, "100%＝剛好達容許", 14, GREEN, anchor="middle", weight="bold")
    g.text(x0, 370, "0", 14, MUTED, anchor="middle")
    g.save("figs/fig12_util.svg")


# ───────── fig13 NG 時的四個旋鈕 ─────────
def fig13():
    g = SVG(1200, 430)
    heads = ["①傳遞頂拉", "②傳遞底壓", "③使用頂壓", "④使用底拉"]
    knobs = [("加大 P", ["✘", "✘", "✔", "✔"], "頂更拉、底更壓；只救 ③④"),
             ("加大 e", ["✘", "✘", "✔", "✔"], "同上，且不必多花鋼腱"),
             ("加大斷面 S", ["✔", "✔", "✔", "✔"], "全部變好，但自重跟著增加"),
             ("提高 f′_{ci}（晚放張）", ["✔", "✔", "—", "—"], "只放寬傳遞階段的容許值")]
    x0 = 330
    for j, h in enumerate(heads):
        g.text(x0 + 90 + j*150, 40, h, 16, INK, anchor="middle", weight="bold")
    for i, (k, marks, note) in enumerate(knobs):
        y = 62 + i*88
        card(g, 20, y, 1160, 74, PANEL if i % 2 == 0 else W, "#D5DAE1", 10)
        g.text(40, y + 45, k, 19, PUR, weight="bold")
        for j, m in enumerate(marks):
            mark(g, x0 + 90 + j*150, y + 38, {"✔": "ok", "✘": "ng"}.get(m, "dash"), 13)
        g.text(930, y + 45, note, 15, MUTED)
    g.text(600, 420, "①④ 是一對冤家：想救 ④ 就加 P、加 e，但 ① 立刻變緊 → 這就是「鋼腱可行區」的由來", 16, RED, anchor="middle", weight="bold")
    g.save("figs/fig13_knobs.svg")


# ───────── fig14 e 可行區 ─────────
def fig14():
    g = SVG(1200, 420)
    x0, s = 420, 14.0
    X = lambda e: x0 + e*s
    y = 250
    g.line(X(-20), y, X(50), y, AX, 2.4)
    for v in range(-20, 51, 10):
        g.line(X(v), y - 6, X(v), y + 6, AX, 1.6); g.text(X(v), y + 28, f"{v}", 14, MUTED, anchor="middle")
    g.text(X(50) + 12, y + 6, "e（cm）", 16, INK, weight="bold")
    g.rect(X(E4), y - 30, X(E1) - X(E4), 60, fill=GREENBG, stroke=GREEN, sw=2, rx=6)
    lims = [("①", E1, "≤", RED, 165, True, 1), ("②", E2, "≤", BLUE, 130, False, -1),
            ("③", E3, "≥", BLUE, 130, False, 1), ("④", E4, "≥", RED, 85, True, -1)]
    for n, v, op, c, h, ctrl, side in lims:
        g.line(X(v), y - h, X(v), y, c, 3 if ctrl else 1.8, dash=None if ctrl else "6 4")
        dx = -45 if op == "≤" else 45
        g.arrow(X(v), y - h, X(v) + dx, y - h, c, 2.6, 11)
        badge(g, X(v), y - h - 26, n, ORG, 15, 15)
        g.text(X(v) + 20*side, y - h - 20, f"e {op} {v:.2f}", 16, c,
               anchor="start" if side > 0 else "end", weight="bold")
    g.line(X(E), y - 34, X(E), y + 34, ORG, 4)
    g.text(X(E), y + 60, f"採用 e = {E:.0f}（OK）", 17, ORG, anchor="middle", weight="bold")
    g.text(X((E1 + E4)/2), y + 90, f"可行區 {E4:.2f} ≤ e ≤ {E1:.2f}", 18, GREEN, anchor="middle", weight="bold")
    g.text(600, 30, "把四個不等式都解成「e 的範圍」：≤ 是上限、≥ 是下限，交集就是可行區", 18, INK, anchor="middle", weight="bold")
    g.text(600, 405, "拉力的 ① 壓住上限、④ 撐起下限；壓力的 ②③ 離很遠，本例不控制", 16, MUTED, anchor="middle")
    g.save("figs/fig14_ezone.svg")


# ───────── fig15 最大活載 ─────────
def fig15():
    g = SVG(1200, 400)
    x0, s = 90, 8.6
    X = lambda m: x0 + m*s
    y = 230
    g.line(X(0), y, X(112), y, AX, 2.4)
    for v in range(0, 111, 20):
        g.line(X(v), y - 6, X(v), y + 6, AX, 1.6); g.text(X(v), y + 46, f"{v}", 14, MUTED, anchor="middle")
    g.text(X(112) + 10, y + 6, "M_T（t-m）", 16, INK, weight="bold")
    g.rect(X(0), y - 26, X(MTX) - X(0), 52, fill=GREENBG, stroke=GREEN, sw=1.6, rx=6)
    for n, v, c, h, ctrl in [("④", MT4, RED, 90, True), ("③", MT3, BLUE, 90, False)]:
        g.line(X(v), y - h, X(v), y, c, 3 if ctrl else 1.8, dash=None if ctrl else "6 4")
        g.arrow(X(v), y - h, X(v) - 60, y - h, c, 2.6, 11)
        badge(g, X(v), y - h - 26, n, ORG, 15, 15)
        g.text(X(v) + 22, y - h - 20, f"M_T ≤ {v:.2f}", 16, c, weight="bold")
    g.line(X(MD), y - 30, X(MD), y + 30, AX, 3)
    g.text(X(MD), y + 74, f"M_d = {MD:.2f}", 15, INK, anchor="middle", weight="bold")
    g.line(X(MT), y - 30, X(MT), y + 30, ORG, 4)
    g.text(X(MT) - 8, y + 74, f"現況 {MT:.2f}", 15, ORG, anchor="end", weight="bold")
    g.arrow(X(MD), y + 100, X(MTX), y + 100, PUR, 2.6, 11); g.arrow(X(MTX), y + 100, X(MD), y + 100, PUR, 2.6, 11)
    g.text((X(MD) + X(MTX))/2, y + 130, f"M_{{L,max}} = {MTX:.2f} − {MD:.2f} = {MLX:.2f} t-m", 17, PUR, anchor="middle", weight="bold")
    g.text(X(MTX) + 30, y + 100, f"→ w_{{L,max}} = 8M_L/L² = {WLX:.3f} t/m", 17, PUR, weight="bold")
    g.text(600, 34, "把 M_T 當未知數：③ 給上限、④ 也給上限，取較小者", 18, INK, anchor="middle", weight="bold")
    g.save("figs/fig15_wL.svg")


# ───────── fig16 SOP 流程圖 ─────────
def fig16():
    g = SVG(1200, 420)
    steps = [("1 切時刻", "傳遞／使用", GOLD, GOLDBG), ("2 每刻寫四格", "斷面、P、M、容許", PUR, PURBG),
             ("3 三項純數值", "P/A、P·e/S、M/S", BLUE, BLUEBG), ("4 定號加減", "頂 +−+　底 ++−", ORG, ORGBG)]
    for i, (a, b, c, bg) in enumerate(steps):
        x = 20 + i*232
        card(g, x, 60, 205, 110, bg, c, 12, 2)
        g.text(x + 102, 102, a, 19, c, anchor="middle", weight="bold")
        g.text(x + 102, 140, b, 15, INK, anchor="middle")
        if i < 3: g.arrow(x + 208, 115, x + 229, 115, MUTED, 2.4, 10)
    g.arrow(20 + 3*232 + 208, 115, 990, 115, MUTED, 2.4, 10)
    # 判斷菱形
    cx, cy = 1080, 115
    g.poly([(cx, cy - 70), (cx + 95, cy), (cx, cy + 70), (cx - 95, cy)], GREEN, 2.4, fill=GREENBG, closed=True)
    g.text(cx, cy - 4, "四點都在", 16, GREEN, anchor="middle", weight="bold")
    g.text(cx, cy + 20, "容許內？", 16, GREEN, anchor="middle", weight="bold")
    g.arrow(cx, cy + 70, cx, 280, GREEN, 2.4, 11); g.text(cx + 12, 230, "是", 16, GREEN, weight="bold")
    card(g, 990, 282, 180, 70, GREEN, GREEN, 12)
    g.text(1080, 325, "合格 → 下一題", 17, W, anchor="middle", weight="bold")
    g.poly([(cx - 47, cy + 35), (cx - 47, 215), (900, 215), (900, 325), (790, 325)], RED, 2.4)
    g.arrow(790, 325, 762, 325, RED, 2.4, 11); g.text(cx - 70, 240, "否", 16, RED, weight="bold")
    card(g, 330, 270, 430, 110, REDBG, RED, 12, 2)
    g.text(545, 310, "找出超限的那一點，調整旋鈕", 18, RED, anchor="middle", weight="bold")
    g.text(545, 348, "P、e、斷面 S、f′_{ci}（見旋鈕表）", 16, INK, anchor="middle")
    g.poly([(330, 325), (120, 325), (120, 175)], RED, 2.4, dash="6 4")
    g.arrow(120, 200, 120, 173, RED, 2.4, 11)
    g.text(600, 30, "把題目先切成「時刻」，每個時刻寫下四格，剩下的就只是代數", 19, INK, anchor="middle", weight="bold")
    g.save("figs/fig16_sop.svg")


if __name__ == "__main__":
    fig01(); fig02(); fig03()
    stage_phys("fig04_transfer", True); stage_phys("fig05_service", False)
    fig06(); fig07()
    check_fig("fig08_checkT", T1, T2, T3, FCI_A, FTI_A, "傳遞階段：P_i = 150 t、M_d = 13.824 t-m、容許值用 f′_{ci} = 280",
              [("①", "頂纖維", F1, -FTI_A), ("②", "底纖維", F2, FCI_A)])
    check_fig("fig09_checkS", U1, U2, U3, FCS_A, FTS_A, "使用階段：P_e = 120 t、M_T = 58.824 t-m、容許值用 f′_c = 350",
              [("③", "頂纖維", F3, FCS_A), ("④", "底纖維", F4, -FTS_A)])
    fig10(); fig11(); fig12(); fig13(); fig14(); fig15(); fig16()
    print("figs done")
