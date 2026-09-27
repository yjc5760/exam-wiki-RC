"""RC-U4-1 拼圖四：從檢核到設計 — 向量圖（所有數值由 params.py 算出）"""
import math, os
from helpers import *
from params import *

TEAL = "#2C6E9E"
ORGBG = "#FCEEE5"
LIM = "#7A3E9D"
os.makedirs("figs", exist_ok=True)


def badge(g, cx, cy, n, col, r=19, size=19):
    g.circle(cx, cy, r, fill=col, stroke=W, sw=2)
    g.text(cx, cy + size*0.36, n, size, W, anchor="middle", weight="bold")


def f2(v): return f"{v:.2f}"
def cm(v): return f"{v:,.0f}"


def section(g, x, y, w, h, tendon=None, cen=True, sw=2.2):
    block(g, x, y, w, h, sw)
    if cen: g.line(x - 18, y + h/2, x + w + 18, y + h/2, "#8A94A3", 1.4, dash="7 5")
    if tendon is not None: g.circle(x + w/2, tendon, 8, fill=ORG, stroke=W, sw=2)


# ───────── fig01 總覽 ─────────
def fig01():
    g = SVG(1200, 440)
    cols = [("①", "開裂彎矩 M_{cr}", "彈性語言的終點", BLUE, BLUEBG),
            ("②", "極限強度 φM_n", "換成力偶語言", ORG, ORGBG),
            ("③", "反算設計", "不等式 → 等式", GREEN, GREENBG)]
    for i, (n, t, sub, c, bg) in enumerate(cols):
        x = 20 + i*395
        card(g, x, 20, 370, 330, bg, c, 14, 2)
        badge(g, x + 38, 58, n, c)
        g.text(x + 68, 66, t, 22, c, weight="bold")
        g.text(x + 185, 102, sub, 17, INK, anchor="middle", weight="bold")
        if i < 2: g.arrow(x + 374, 185, x + 391, 185, MUTED, 2.6, 11)
    # ① 迷你應力圖：底纖維從 + 推到 −f_r
    x0, yt, yb = 120, 140, 300
    stress(g, x0, yt, yb, TOP[0], BOT[0], 0.9)
    g.circle(x0 + BOT[0]*0.9, yb, 6, fill=BLUE)
    g.arrow(x0 + BOT[0]*0.9 - 6, yb + 18, x0 - FR*0.9, yb + 18, RED, 2.6, 11)
    g.line(x0 - FR*0.9, yb - 12, x0 - FR*0.9, yb + 26, RED, 2.2)
    g.text(x0 + 40, yb + 44, "底：+107.81 → −f_r", 15, RED, anchor="middle", weight="bold")
    g.text(285, 170, "M_{cr}", 26, BLUE, anchor="middle", weight="bold")
    g.text(285, 205, f"= {MCR:.2f} t-m", 18, BLUE, anchor="middle", weight="bold")
    g.text(285, 250, "預力決定", 16, INK, anchor="middle")
    g.text(285, 274, "「何時開裂」", 16, INK, anchor="middle", weight="bold")
    # ② 迷你力偶
    x = 20 + 395
    block(g, x + 50, 140, 110, 170)
    g.rect(x + 50, 140, 110, 35, fill=BLUE, stroke=BLUE, sw=2, op=0.35)
    g.circle(x + 105, 280, 7, fill=ORG)
    g.arrow(x + 250, 157, x + 175, 157, BLUE, 3, 12); g.text(x + 258, 162, "C", 20, BLUE, weight="bold")
    g.arrow(x + 175, 280, x + 250, 280, RED, 3, 12); g.text(x + 258, 285, "T", 20, RED, weight="bold")
    g.line(x + 215, 170, x + 215, 268, INK, 1.4, dash="4 3")
    g.text(x + 300, 222, "力偶臂", 15, MUTED, anchor="middle")
    g.text(x + 185, 332, f"φM_n = {PMN:.2f} ≥ M_u、1.2M_{{cr}}", 16, ORG, anchor="middle", weight="bold")
    # ③ 迷你可行區
    x = 20 + 790
    X = lambda xx: x + 40 + xx/12*290
    Y = lambda e: 300 - e*5
    up = [(X(t/2), Y(e1(t/2))) for t in range(25)]
    lo = [(X(t/2), Y(max(0, e4(t/2)))) for t in range(25)]
    g.poly(up + lo[::-1], GREEN, 0, fill=GREENBG, closed=True)
    g.poly(up, BLUE, 3); g.poly(lo, RED, 3)
    g.poly([(X(t/2), Y(E*4*(t/2)*(12 - t/2)/144)) for t in range(25)], ORG, 3, dash="7 5")
    g.line(X(0), Y(0), X(12), Y(0), AX, 1.6)
    g.text(x + 185, 332, f"{E4:.2f} ≤ e ≤ {E1:.2f} cm", 16, GREEN, anchor="middle", weight="bold")
    g.text(X(6), Y(E1) - 12, "e_{max}", 15, BLUE, anchor="middle", weight="bold")
    # 底部主軸
    g.rect(20, 370, 1160, 56, fill=NAVY, stroke="none", rx=12)
    g.text(600, 406, "檢核：已知 e、P、w → 算應力比容許　｜　設計：令應力 = 容許 → 反解 e、P、w", 19, W, anchor="middle", weight="bold")
    g.save("figs/fig01_map.svg")


# ───────── fig02 彎矩階梯（M–Δ 示意） ─────────
def fig02():
    g = SVG(1200, 470)
    x0, y0 = 120, 430
    Y = lambda m: y0 - m*3.3
    # 區帶
    g.rect(x0, Y(MCR), 560, Y(0) - Y(MCR), fill=BLUEBG, stroke="none")
    g.rect(x0, Y(MN), 560, Y(MCR) - Y(MN), fill=ORGBG, stroke="none")
    g.text(x0 + 290, Y(MCR) + 110, "未開裂：WSD 應力語言", 18, BLUE, weight="bold")
    g.text(x0 + 330, Y(MCR) - 60, "開裂後：LRFD 力偶語言", 18, ORG, weight="bold")
    g.line(x0, y0, x0 + 580, y0, AX, 2); g.line(x0, y0, x0, Y(125), AX, 2)
    g.arrow(x0, Y(118), x0, Y(126), AX, 2, 10); g.arrow(x0 + 570, y0, x0 + 585, y0, AX, 2, 10)
    g.text(x0 - 10, Y(124) + 6, "M（t-m）", 15, INK, anchor="end", weight="bold")
    g.text(x0 + 580, y0 + 28, "撓度 Δ（示意）", 15, MUTED, anchor="end")
    # M–Δ 曲線（示意）：線性至 M_cr，之後變軟，至 M_n 平台
    kx = 4.1
    pts = [(x0, Y(0)), (x0 + MCR*kx*0.5, Y(MCR))]
    xa = x0 + MCR*kx*0.5
    for i in range(1, 31):
        t = i/30; m = MCR + (MN*0.97 - MCR)*(1 - (1 - t)**2.2)
        pts.append((xa + t*230, Y(m)))
    pts.append((pts[-1][0] + 120, Y(MN)))
    g.poly(pts, INK, 3.4)
    g.circle(xa, Y(MCR), 8, fill=W, stroke=BLUE, sw=3)
    lines = [(MD, "M_d 自重", MUTED, False), (M0, "M_0 消壓（底 = 0）", PUR, False),
             (MT, "M_T 使用總彎矩", RED, False), (MCR, "M_{cr} 開裂", BLUE, True),
             (MCR12, "1.2M_{cr} 最小強度", LIM, False), (MU, "M_u 設計需求", RED, True),
             (PMN, "φM_n 設計強度", ORG, True), (MN, "M_n 標稱強度", ORG, False)]
    ly = {MD: 0, M0: -8, MT: 8, MCR: -9, MCR12: 0, MU: 0, PMN: 0, MN: 0}
    for m, t, c, bold in lines:
        g.line(x0, Y(m), 760, Y(m), c, 2.4 if bold else 1.4, dash=None if bold else "6 4")
        yy = Y(m) + 6 + ly[m]
        g.text(772, yy, f"{m:6.2f}", 17, c, weight="bold")
        g.text(850, yy, t, 17, c, weight="bold" if bold else "normal")
    g.text(600, 26, "同一根梁，彎矩一路往上加：先過 M_{cr} 換語言，最後由 φM_n 收尾", 19, INK, anchor="middle", weight="bold")
    g.save("figs/fig02_ladder.svg")


# ───────── fig03 M_cr 四個狀態 ─────────
def fig03():
    g = SVG(1200, 470)
    yt, yb, s = 110, 310, 0.95
    Ms = [0.0, MD, MT, MCR]
    heads = ["① 只有 P_e", "② 加自重 M_d", "③ 加使用載重", "④ 到 M = M_{cr}"]
    for i in range(4):
        x = 150 + i*290
        g.text(x, 40, heads[i], 19, INK, anchor="middle", weight="bold")
        g.text(x, 66, f"M = {Ms[i]:.2f} t-m" if i else "M = 0", 15, MUTED, anchor="middle")
        stress(g, x, yt, yb, TOP[i], BOT[i], s)
        vlab(g, x, yb + 34, BOT[i], "底 ", 18)
        if i == 3: g.text(x, yb + 58, "= −f_r → 開裂", 16, RED, anchor="middle", weight="bold")
    # 數線
    y = 425
    X = lambda f: 1080 - (f + 45)/(160)*900 if False else 150 + (112 - f)*6.0
    g.rect(X(0), y - 16, X(-45) - X(0), 32, fill=REDBG, stroke="none")
    g.line(X(112), y, X(-45), y, AX, 2)
    g.line(X(0), y - 22, X(0), y + 22, AX, 1.6, dash="4 3"); g.text(X(0), y + 40, "0", 14, MUTED, anchor="middle")
    g.text(X(112) - 10, y + 6, "壓", 15, BLUE, anchor="end", weight="bold")
    g.text(X(-45) + 10, y + 6, "拉", 15, RED, weight="bold")
    for i, v in enumerate(BOT):
        c = BLUE if v >= 0 else RED
        g.circle(X(v), y, 9, fill=c)
        g.text(X(v), y - 22, "①②③④"[i], 15, c, anchor="middle", weight="bold")
    g.text(X(-FR), y + 40, f"−f_r = −{FR:.2f}", 14, RED, anchor="middle", weight="bold")
    g.save("figs/fig03_mcr4.svg")


# ───────── fig04 M_cr 拆成三段（核心點力矩） ─────────
def fig04():
    g = SVG(1200, 440)
    # 左：斷面與核心點
    x, y, w, h = 90, 60, 150, 300; sc = h/80
    section(g, x, y, w, h)
    yc = y + h/2; ykt = yc - K*sc; yps = yc + E*sc
    g.rect(x, yc - K*sc, w, 2*K*sc, fill=PUR, stroke=PUR, sw=1.2, op=0.12, dash="5 4")
    g.circle(x + w/2, ykt, 7, fill=PUR); g.circle(x + w/2, yps, 9, fill=ORG)
    g.text(x - 12, ykt + 6, "上核心點", 15, PUR, anchor="end", weight="bold")
    g.text(x - 12, yps + 6, "鋼腱", 15, ORG, anchor="end", weight="bold")
    g.line(x + w + 30, ykt, x + w + 30, yps, INK, 1.6)
    for yy in (ykt, yps): g.line(x + w + 22, yy, x + w + 38, yy, INK, 1.6)
    g.text(x + w + 42, (ykt + yc)/2 + 6, f"k_t = {K:.2f}", 15, PUR, weight="bold")
    g.text(x + w + 42, (yc + yps)/2 + 6, f"e = {E:.0f}", 15, ORG, weight="bold")
    g.text(x + w/2, y + h + 40, f"力臂 e + k_t = {E + K:.2f} cm", 16, INK, anchor="middle", weight="bold")
    # 右：堆疊條
    bx, by, bh = 470, 170, 70; ks = 10.2
    parts = [(MCR_E, "P_e·e", ORG, ORGBG), (MCR_K, "P_e·k_t", PUR, PURBG), (MCR_R, "f_r·S_b", RED, REDBG)]
    xx = bx
    for v, t, c, bg in parts:
        g.rect(xx, by, v*ks, bh, fill=bg, stroke=c, sw=2)
        g.text(xx + v*ks/2, by + 32, t, 17, c, anchor="middle", weight="bold")
        g.text(xx + v*ks/2, by + 58, f"{v:.2f}", 17, c, anchor="middle", weight="bold")
        xx += v*ks
    g.line(bx, by - 30, bx, by + bh + 30, AX, 1.4)
    xm0 = bx + M0*ks
    g.line(xm0, by - 50, xm0, by + bh + 16, PUR, 2.2, dash="6 4")
    g.text(xm0, by - 58, f"M_0 = P_e(e + k_t) = {M0:.2f}", 16, PUR, anchor="middle", weight="bold")
    g.line(xx, by - 18, xx, by + bh + 50, BLUE, 3)
    g.text(xx, by + bh + 74, f"M_{{cr}} = {MCR:.2f}", 19, BLUE, anchor="middle", weight="bold")
    g.text(bx + (M0*ks)/2, by + bh + 50, "消壓：底纖維預壓剛好歸零", 15, PUR, anchor="middle")
    g.text(xm0 + MCR_R*ks/2, by + bh + 104, "再拉到 f_r 才開裂", 15, RED, anchor="middle")
    g.text(700, 50, "M_{cr} = P_e(e + k_t) + f_r S_b：預力對「上核心點」的力矩 ＋ 混凝土自己的抗拉", 18, INK, anchor="middle", weight="bold")
    g.text(700, 410, "e 每多 1 cm，M_{cr} 就多 P_e × 1 cm = 1.2 t-m", 16, MUTED, anchor="middle")
    g.save("figs/fig04_kern.svg")


# ───────── fig05 兩種語言 ─────────
def fig05():
    g = SVG(1200, 440)
    for i, (t, sub, c, bg) in enumerate([("彈性語言 WSD｜使用載重", "全斷面有效、應力線性", BLUE, BLUEBG),
                                          ("強度語言 LRFD｜極限狀態", "拉側開裂不計、壓力塊＋鋼腱力偶", ORG, ORGBG)]):
        x = 20 + i*600
        card(g, x, 20, 560, 400, bg, c, 14, 1.6)
        g.rect(x, 20, 560, 52, fill=c, stroke="none", rx=14, op=0.18)
        g.text(x + 280, 54, t, 20, c, anchor="middle", weight="bold")
        g.text(x + 280, 100, sub, 16, MUTED, anchor="middle")
    # 左
    x, y, w, h = 90, 150, 130, 205
    section(g, x, y, w, h, y + h/2 + E*h/80)
    stress(g, 330, y, y + h, TOP[2], BOT[2], 0.95)
    vlab(g, 330, y - 12, TOP[2], "頂 ", 16); vlab(g, 330, y + h + 26, BOT[2], "底 ", 16)
    g.text(300, 405, "檢核：纖維應力 ≤ 容許應力", 17, BLUE, anchor="middle", weight="bold")
    g.text(470, 190, "鋼腱", 15, MUTED, anchor="middle")
    g.text(470, 214, f"f_{{pe}} = {FPE:,.0f}", 16, ORG, anchor="middle", weight="bold")
    g.text(470, 238, f"≈ {FPE/FPU:.3f} f_{{pu}}", 15, ORG, anchor="middle")
    g.arrow(575, 250, 640, 250, MUTED, 3, 14)
    # 右
    x = 700; sc = h/80
    section(g, x, y, w, h, y + DP*sc, cen=False)
    g.rect(x, y, w, AA*sc, fill=BLUE, stroke=BLUE, sw=2, op=0.35)
    g.line(x - 14, y + CC*sc, x + w + 14, y + CC*sc, ORG, 1.8, dash="7 5")
    g.text(x + w + 18, y + CC*sc + 5, f"c = {CC:.2f}", 14, ORG, weight="bold")
    for k in range(4):
        cx, cy = x + 25 + k*28, y + h - 20 - k*22
        g.poly([(cx, cy), (cx + 8, cy - 12), (cx + 2, cy - 24)], RED, 2)
    yC, yT = y + AA*sc/2, y + DP*sc
    g.arrow(1080, yC, 960, yC, BLUE, 3, 14); g.text(1085, yC + 6, f"C = {T/1e3:.2f} t", 16, BLUE, weight="bold")
    g.arrow(960, yT, 1080, yT, RED, 3, 14); g.text(1085, yT + 6, f"T = {T/1e3:.2f} t", 16, RED, weight="bold")
    g.line(935, yC, 935, yT, INK, 1.6)
    for yy in (yC, yT): g.line(927, yy, 943, yy, INK, 1.6)
    g.text(925, (yC + yT)/2 - 4, "d_p − a/2", 15, INK, anchor="end", weight="bold")
    g.text(925, (yC + yT)/2 + 20, f"= {ARM:.2f} cm", 15, INK, anchor="end")
    g.text(900, 405, "檢核：φM_n ≥ M_u 且 φM_n ≥ 1.2M_{cr}", 17, ORG, anchor="middle", weight="bold")
    g.save("figs/fig05_lang.svg")


# ───────── fig06 應變、壓力塊、力偶 ─────────
def fig06():
    g = SVG(1200, 440)
    y, h = 60, 320; sc = h/80
    x, w = 90, 160
    section(g, x, y, w, h, y + DP*sc, cen=False)
    g.text(x + w/2, y - 16, "斷面 40×80", 16, INK, anchor="middle", weight="bold")
    g.line(x + w + 12, y, x + w + 12, y + DP*sc, MUTED, 1.2); g.text(x + w + 18, y + DP*sc/2, f"d_p = {DP:.0f}", 14, MUTED)
    # 應變
    xs = 420; es = 7000
    yc = y + CC*sc
    g.line(xs, y - 10, xs, y + h + 10, AX, 2)
    g.poly([(xs, y), (xs - 0.003*es, y), (xs, yc)], BLUE, 2.2, fill=BLUEF, closed=True)
    ydp = y + DP*sc
    g.poly([(xs, yc), (xs + ET*es, ydp), (xs, ydp)], RED, 2.2, fill=REDF, closed=True)
    g.line(xs - 40, yc, xs + 60, yc, ORG, 1.8, dash="7 5")
    g.text(xs - 0.003*es - 6, y + 6, "ε_{cu} = 0.003", 15, BLUE, anchor="end", weight="bold")
    g.text(xs + ET*es + 8, ydp + 6, f"ε_t = {ET:.5f}", 15, RED, weight="bold")
    g.text(xs + ET*es + 8, ydp + 30, "≥ 0.005 → 拉力控制 φ = 0.90", 14, GREEN, weight="bold")
    g.text(xs + 66, yc + 5, f"c = {CC:.2f}", 15, ORG, weight="bold")
    g.text(xs, y - 18, "應變", 17, INK, anchor="middle", weight="bold")
    # 壓力塊
    xb = 720; bw = 110
    g.line(xb, y - 10, xb, y + h + 10, AX, 2)
    g.rect(xb, y, bw, AA*sc, fill=BLUEF, stroke=BLUE, sw=2.2)
    g.text(xb + bw + 8, y + 20, "0.85f′_c", 15, BLUE, weight="bold")
    g.text(xb + bw + 8, y + AA*sc - 4, f"a = β_1 c = {AA:.2f}", 15, BLUE, weight="bold")
    g.text(xb, y - 18, "等值應力塊", 17, INK, anchor="middle", weight="bold")
    # 力
    yC, yT = y + AA*sc/2, ydp
    g.arrow(1120, yC, 1000, yC, BLUE, 3.4, 14); g.text(1060, yC - 14, f"C = {T/1e3:.2f} t", 16, BLUE, anchor="middle", weight="bold")
    g.arrow(1000, yT, 1120, yT, RED, 3.4, 14); g.text(1060, yT - 14, f"T = A_{{ps}}f_{{ps}} = {T/1e3:.2f} t", 16, RED, anchor="middle", weight="bold")
    g.line(975, yC, 975, yT, INK, 1.8)
    for yy in (yC, yT): g.line(967, yy, 983, yy, INK, 1.8)
    g.text(965, (yC + yT)/2 + 6, f"{ARM:.2f}", 16, INK, anchor="end", weight="bold")
    g.text(600, 420, f"C = T 求 a；M_n = T(d_p − a/2) = {MN:.2f} t-m；β_1 = {B1:.2f}（f′_c = 350）", 17, INK, anchor="middle", weight="bold")
    g.save("figs/fig06_block.svg")


# ───────── fig07 鋼腱應力–應變 ─────────
def fig07():
    g = SVG(1200, 440)
    x0, y0 = 110, 380
    X = lambda e: x0 + e/0.04*640
    Y = lambda f: y0 - f/20000*330
    Ep = 1.97e6
    def fs(e): return min(FPU, e*Ep*(0.025 + 0.975/(1 + (118*e)**10)**0.1))
    pts = [(X(i*0.0004), Y(fs(i*0.0004))) for i in range(101)]
    g.line(x0, y0, X(0.042), y0, AX, 2); g.line(x0, y0, x0, Y(20500), AX, 2)
    g.text(X(0.042), y0 + 30, "ε_{ps}", 16, INK, anchor="end", weight="bold")
    g.text(x0 - 10, Y(20000), "f_{ps}", 16, INK, anchor="end", weight="bold")
    for v, t, c in [(FPU, "f_{pu}", RED), (FPS, "f_{ps}", ORG), (FPE, "f_{pe}", BLUE)]:
        g.line(x0, Y(v), X(0.04), Y(v), c, 1.2, dash="5 4")
        g.text(x0 - 10, Y(v) + 5, f"{v:,.0f}", 14, c, anchor="end", weight="bold")
    g.poly(pts, INK, 3.2)
    # 找 f_pe、f_ps 在曲線上的點
    def inv(f):
        lo, hi = 0, 0.04
        for _ in range(60):
            m = (lo + hi)/2
            lo, hi = (m, hi) if fs(m) < f else (lo, m)
        return lo
    for v, c, lab in [(FPE, BLUE, "使用：f_{pe}"), (FPS, ORG, "極限：f_{ps}")]:
        g.circle(X(inv(v)), Y(v), 9, fill=c)
        g.text(X(inv(v)) + 16, Y(v) + 24, lab, 16, c, weight="bold")
    g.arrow(X(inv(FPE)) + 14, Y(FPE) - 14, X(inv(FPS)) - 12, Y(FPS) + 12, PUR, 2.4, 11)
    # 右側說明
    card(g, 800, 60, 380, 320, PANEL, "#D5DAE1")
    rows = [("A_{ps}", f"12 × 0.987 = {APS:.3f} cm²", INK),
            ("f_{pe} / f_{pu}", f"{FPE:,.0f} / {FPU:,.0f} = {FPE/FPU:.3f}", BLUE),
            ("f_{ps} / f_{pu}", f"{FPS:,.0f} / {FPU:,.0f} = {FPS/FPU:.3f}", ORG),
            ("T_{使用} = P_e", f"{PE_T:.0f} t", BLUE),
            ("T_{極限}", f"{T/1e3:.2f} t（× {T/PE:.2f}）", ORG)]
    for i, (a, b, c) in enumerate(rows):
        g.text(825, 110 + i*56, a, 17, c, weight="bold")
        g.text(825, 136 + i*56, b, 16, INK)
    g.text(600, 30, "同一束鋼腱：使用時只用到一半強度，極限時被拉到接近 f_{pu}", 18, INK, anchor="middle", weight="bold")
    g.text(450, 425, "f_{pe} ≥ 0.5f_{pu} 是 ACI 近似式的適用前提", 15, MUTED, anchor="middle")
    g.save("figs/fig07_strand.svg")


# ───────── fig08 P_e 旋鈕：M_cr 動、M_n 不動 ─────────
def fig08():
    g = SVG(1200, 440)
    x0, y0 = 120, 380
    X = lambda p: x0 + (p - 60)/150*820
    Y = lambda m: y0 - m/140*340
    g.rect(X(60), Y(140), X(0.5*FPU*APS/1e3) - X(60), y0 - Y(140), fill="#EEF0F3", stroke="none")
    g.text((X(60) + X(0.5*FPU*APS/1e3))/2, Y(132), "f_{pe} < 0.5f_{pu}", 14, MUTED, anchor="middle")
    g.text((X(60) + X(0.5*FPU*APS/1e3))/2, Y(124), "近似式不適用", 14, MUTED, anchor="middle")
    g.line(x0, y0, X(212), y0, AX, 2); g.line(x0, y0, x0, Y(142), AX, 2)
    for p in range(60, 211, 30):
        g.line(X(p), y0, X(p), y0 + 6, AX, 1.4); g.text(X(p), y0 + 26, f"{p}", 14, MUTED, anchor="middle")
    for m in range(0, 141, 20):
        g.line(x0 - 6, Y(m), x0, Y(m), AX, 1.4); g.text(x0 - 10, Y(m) + 5, f"{m}", 14, MUTED, anchor="end")
    g.text(X(212), y0 + 52, "P_e（t）", 15, INK, anchor="end", weight="bold")
    g.text(x0 - 10, Y(142) - 6, "M（t-m）", 15, INK, anchor="end", weight="bold")
    p1, p2 = 110.0, 210.0
    g.line(X(p1), Y(PMN), X(p2), Y(PMN), ORG, 3.6)
    g.line(X(p1), Y(MU), X(p2), Y(MU), RED, 2, dash="8 5")
    g.line(X(p1), Y(mcr_of(p1)), X(p2), Y(mcr_of(p2)), BLUE, 3.2)
    g.line(X(p1), Y(1.2*mcr_of(p1)), X(p2), Y(1.2*mcr_of(p2)), LIM, 2.4, dash="8 5")
    g.text(X(p2) + 8, Y(PMN) + 6, f"φM_n = {PMN:.2f}（不動）", 15, ORG, weight="bold")
    g.text(X(p2) + 8, Y(MU) + 6, f"M_u = {MU:.2f}", 15, RED, weight="bold")
    g.text(X(168), Y(mcr_of(168)) + 26, "M_{cr}", 17, BLUE, weight="bold")
    g.text(X(126), Y(1.2*mcr_of(126)) - 10, "1.2M_{cr}", 17, LIM, weight="bold")
    g.line(X(PE_T), Y(0), X(PE_T), Y(PMN), AX, 1.4, dash="4 3")
    g.circle(X(PE_T), Y(MCR), 8, fill=BLUE); g.circle(X(PE_T), Y(PMN), 8, fill=ORG)
    g.text(X(PE_T) + 12, Y(MCR) + 22, f"本例 M_{{cr}} = {MCR:.2f}", 15, BLUE, weight="bold")
    g.circle(X(PE_12), Y(PMN), 9, fill=W, stroke=LIM, sw=3)
    g.line(X(PE_12), Y(PMN), X(PE_12), y0, LIM, 1.4, dash="4 3")
    g.text(X(PE_12), Y(PMN) - 18, f"P_e = {PE_12:.1f} t", 15, LIM, anchor="middle", weight="bold")
    g.text(X(PE_12) + 10, Y(40), "超過這裡：", 14, LIM, weight="bold")
    g.text(X(PE_12) + 10, Y(40) + 22, "1.2M_{cr} > φM_n", 14, LIM, weight="bold")
    g.text(600, 30, "旋鈕 P_e：開裂彎矩跟著轉，極限強度幾乎不動（有黏結）", 19, INK, anchor="middle", weight="bold")
    g.save("figs/fig08_knob.svg")


# ───────── fig09 1.2M_cr：延性 vs 脆性 ─────────
def fig09():
    g = SVG(1200, 440)
    for i, (t, c, good) in enumerate([("φM_n ≥ 1.2M_{cr}：開裂後還撐得住", GREEN, True),
                                       ("M_n < M_{cr}：一開裂就斷", RED, False)]):
        x0 = 90 + i*580; y0 = 360
        X = lambda d: x0 + d*4.4
        Y = lambda m: y0 - m*2.4
        g.line(x0, y0, X(105), y0, AX, 2); g.line(x0, y0, x0, Y(125), AX, 2)
        g.text(X(105), y0 + 26, "Δ", 16, INK, anchor="end", weight="bold")
        g.text(x0 - 8, Y(122), "M", 16, INK, anchor="end", weight="bold")
        g.text(x0 + 230, 34, t, 19, c, anchor="middle", weight="bold")
        mcr = MCR
        g.line(x0, Y(mcr), X(100), Y(mcr), BLUE, 1.4, dash="6 4")
        g.text(X(100), Y(mcr) - 8, "M_{cr}", 15, BLUE, anchor="end", weight="bold")
        if good:
            pts = [(x0, y0), (X(15), Y(mcr))]
            for k in range(1, 21):
                t_ = k/20; pts.append((X(15 + 45*t_), Y(mcr + (MN - mcr)*(1 - (1 - t_)**2))))
            pts.append((X(95), Y(MN)))
            g.poly(pts, GREEN, 3.6)
            g.line(x0, Y(MN), X(100), Y(MN), ORG, 1.4, dash="6 4")
            g.text(X(100), Y(MN) - 8, "M_n", 15, ORG, anchor="end", weight="bold")
            g.text(X(60), Y(40), "裂縫多、撓度大", 16, GREEN, anchor="middle", weight="bold")
            g.text(X(60), Y(40) + 24, "→ 有預警", 16, GREEN, anchor="middle", weight="bold")
        else:
            mn = mcr*0.8
            g.poly([(x0, y0), (X(15), Y(mcr))], RED, 3.6)
            g.poly([(X(15), Y(mcr)), (X(17), Y(mn*0.45)), (X(26), Y(mn*0.2))], RED, 3.6, dash="7 5")
            g.line(x0, Y(mn), X(100), Y(mn), ORG, 1.4, dash="6 4")
            g.text(X(100), Y(mn) + 22, "M_n（鋼腱太少）", 15, ORG, anchor="end", weight="bold")
            g.text(X(32), Y(18), "裂縫處混凝土的拉力", 15, RED, weight="bold")
            g.text(X(32), Y(18) + 24, "瞬間丟給鋼腱 → 接不住", 15, RED, weight="bold")
            g.text(X(32), Y(18) - 30, "無預警、突然斷裂", 16, RED, weight="bold")
    g.text(600, 428, f"本例：φM_n = {PMN:.2f} ≥ 1.2M_{{cr}} = {MCR12:.2f}（比值 {PMN/MCR:.2f}）OK", 17, INK, anchor="middle", weight="bold")
    g.save("figs/fig09_ductile.svg")


# ───────── fig10 反算矩陣 ─────────
def fig10():
    g = SVG(1200, 460)
    cx = [230, 520, 790, 1060]
    heads = [("控制點", INK), ("解 e（P、M 已知）", GREEN), ("解 P（e、M 已知）", ORG), ("解 M_T（e、P 已知）", RED)]
    g.rect(20, 20, 1160, 56, fill=NAVY, stroke="none", rx=10)
    for (t, c), x in zip(heads, cx):
        g.text(x, 56, t, 18, W, anchor="middle", weight="bold")
    rows = [("①", "傳遞・頂拉", f"e ≤ {E1:.2f}", f"P_i ≤ {PI_MAX1:.2f} t", "（M_d 已固定）", True, True, False),
            ("②", "傳遞・底壓", f"e ≤ {E2:.2f}", f"P_i ≤ {PI_MAX2:.2f} t", "（M_d 已固定）", False, False, False),
            ("③", "使用・頂壓", f"e ≥ {E3:.2f}", "本例恆成立", f"M_T ≤ {MT3:.2f}", False, False, False),
            ("④", "使用・底拉", f"e ≥ {E4:.2f}", f"P_e ≥ {PE_MIN:.2f} t", f"M_T ≤ {MT4:.2f}", True, True, True)]
    for i, (n, lab, a, b, c, ca, cb, cc) in enumerate(rows):
        y = 90 + i*80
        card(g, 20, y, 1160, 70, PANEL if i % 2 == 0 else W, "#D5DAE1", 10)
        badge(g, 90, y + 35, n, ORG, 17, 17)
        g.text(130, y + 42, lab, 18, INK, weight="bold")
        for x, t, ctrl, col in [(cx[1], a, ca, GREEN), (cx[2], b, cb, ORG), (cx[3], c, cc, RED)]:
            if ctrl: g.rect(x - 112, y + 12, 224, 46, fill=W, stroke=col, sw=2.4, rx=8)
            g.text(x, y + 42, t, 18, col if ctrl else MUTED, anchor="middle", weight="bold" if ctrl else "normal")
    g.text(600, 440, "框起來的就是控制值：拉應力的 ①④ 幾乎包辦所有反算；④ 反算 M_T 的上限剛好就是 M_{cr}", 17, INK, anchor="middle", weight="bold")
    g.save("figs/fig10_matrix.svg")


# ───────── fig11 鋼腱可行區 ─────────
def fig11():
    g = SVG(1200, 460)
    x0, y0 = 110, 380
    X = lambda x: x0 + x/12*760
    Y = lambda e: y0 - e*10
    xs = [i*0.1 for i in range(121)]
    up = [(X(x), Y(e1(x))) for x in xs]
    lo = [(X(x), Y(max(0, e4(x)))) for x in xs]
    g.poly(up + lo[::-1], GREEN, 0, fill=GREENBG, closed=True)
    g.line(x0, y0, X(12.5), y0, AX, 2); g.line(x0, Y(-3), x0, Y(33), AX, 2)
    for x in range(0, 13, 2):
        g.line(X(x), y0, X(x), y0 + 6, AX, 1.4); g.text(X(x), y0 + 26, f"{x}", 14, MUTED, anchor="middle")
    for e in range(0, 33, 8):
        g.line(x0 - 6, Y(e), x0, Y(e), AX, 1.4); g.text(x0 - 10, Y(e) + 5, f"{e}", 14, MUTED, anchor="end")
    g.text(X(12.5), y0 + 50, "x（m）", 15, INK, anchor="end", weight="bold")
    g.text(x0 - 10, Y(33) - 8, "e（cm，形心以下為正）", 15, INK, weight="bold")
    g.poly(up, BLUE, 3.4); g.poly(lo, RED, 3.4)
    g.poly([(X(x), Y(E*4*x*(12 - x)/144)) for x in xs], ORG, 3.4, dash="9 6")
    g.line(X(6), Y(0), X(6), Y(31), AX, 1.2, dash="4 3")
    g.circle(X(6), Y(E1), 7, fill=BLUE); g.circle(X(6), Y(E4), 7, fill=RED); g.circle(X(6), Y(E), 7, fill=ORG)
    g.text(X(2.4), Y(e1(2.4)) - 14, "e_{max}(x)：傳遞・頂拉 ①", 16, BLUE, anchor="middle", weight="bold")
    g.text(X(6.8), Y(9), "e_{min}(x)", 16, RED, weight="bold")
    g.text(X(6.8), Y(9) + 24, "使用・底拉 ④", 16, RED, weight="bold")
    g.line(X(9.4), Y(E*4*9.4*2.6/144), X(10.0), Y(29), ORG, 1.4)
    g.text(X(10.0), Y(29) - 6, "實際鋼腱（拋物線）", 15, ORG, anchor="middle", weight="bold")
    g.text(X(0) + 8, Y(E1_END) - 10, f"{E1_END:.2f}", 15, BLUE, weight="bold")
    # 右側表
    card(g, 930, 40, 250, 340, PANEL, "#D5DAE1")
    g.text(1055, 76, "跨中 x = 6 m", 17, INK, anchor="middle", weight="bold")
    for i, (a, b, c) in enumerate([("e_{max}", f"{E1:.2f}", BLUE), ("e_{min}", f"{E4:.2f}", RED), ("採用 e", f"{E:.2f}", ORG)]):
        g.text(955, 122 + i*44, a, 17, c, weight="bold"); g.text(1160, 122 + i*44, b, 17, c, anchor="end", weight="bold")
    g.line(950, 238, 1160, 238, "#D5DAE1", 1.2)
    g.text(1055, 272, "梁端 x = 0", 17, INK, anchor="middle", weight="bold")
    g.text(955, 310, "e_{max}", 17, BLUE, weight="bold"); g.text(1160, 310, f"{E1_END:.2f}", 17, BLUE, anchor="end", weight="bold")
    g.text(955, 350, "e_{min}", 17, RED, weight="bold"); g.text(1160, 350, f"{E4_END:.2f}", 17, RED, anchor="end", weight="bold")
    g.text(560, 26, "沿跨度每一點都做一次反算，連成兩條曲線，中間就是可行區", 18, INK, anchor="middle", weight="bold")
    g.text(500, 446, "M 是拋物線 → e 的上下限也是拋物線：跨中最寬、梁端上限最緊", 16, MUTED, anchor="middle")
    g.save("figs/fig11_zone.svg")


# ───────── fig12 直線鋼腱在梁端出界 ─────────
def fig12():
    g = SVG(1200, 440)
    x0, y0 = 90, 330
    X = lambda x: x0 + x/12*640
    Y = lambda e: y0 - e*8.5
    xs = [i*0.1 for i in range(121)]
    up = [(X(x), Y(e1(x))) for x in xs]
    lo = [(X(x), Y(max(0, e4(x)))) for x in xs]
    g.poly(up + lo[::-1], GREEN, 0, fill=GREENBG, closed=True)
    g.poly(up, BLUE, 3); g.poly(lo, RED, 3)
    g.line(x0, y0, X(12), y0, AX, 2)
    # 直線 e = 25
    xb = 6 - math.sqrt(36 - (((E*PI/S) - PI/A - FTI_A)*S/tm)/MD*36)
    g.line(X(0), Y(E), X(12), Y(E), INK, 3)
    g.line(X(0), Y(E), X(xb), Y(E), RED, 6, cap="round"); g.line(X(12 - xb), Y(E), X(12), Y(E), RED, 6, cap="round")
    g.text(X(6), Y(E) - 14, f"直線鋼腱 e = {E:.0f}", 16, INK, anchor="middle", weight="bold")
    g.text(X(xb/2), Y(E) - 14, f"出界 {xb:.2f} m", 15, RED, anchor="middle", weight="bold")
    g.line(X(xb), Y(E) + 8, X(xb), y0, RED, 1.2, dash="4 3")
    g.text(X(0), y0 + 30, "梁端", 15, MUTED, anchor="middle"); g.text(X(12), y0 + 30, "梁端", 15, MUTED, anchor="middle")
    g.text(X(6), y0 + 30, "跨中", 15, MUTED, anchor="middle")
    g.text(X(6), y0 + 62, f"梁端頂纖維（傳遞）= {F1_END_STRAIGHT:.2f} < −{FTI_END:.2f}（端部放寬值）仍 NG", 16, RED, anchor="middle", weight="bold")
    # 右：三種對策
    fixes = [("拋物線（後拉）", "e 跟著 M 走，梁端回到形心附近", ORG),
             ("折線 harped（先拉）", "在 1/3 點下壓，兩端上抬", PUR),
             ("去黏結 debond", "梁端部分鋼絞線包套，不傳力", TEAL)]
    for i, (t, d, c) in enumerate(fixes):
        y = 50 + i*110
        card(g, 790, y, 390, 96, PANEL, c, 10, 1.8)
        g.text(812, y + 36, t, 18, c, weight="bold")
        g.text(812, y + 70, d, 15, INK)
    g.text(400, 30, "梁端 M_d = 0：沒有自重去抵銷預力的上拱力矩", 18, INK, anchor="middle", weight="bold")
    g.save("figs/fig12_ends.svg")


# ───────── fig13 Magnel 圖 ─────────
def fig13():
    g = SVG(1200, 460)
    x0, y0 = 110, 400
    X = lambda e: x0 + (e - 0)/45*720
    Y = lambda v: y0 - v/12*330
    es = [i*0.25 for i in range(181)]
    # 可行域
    feas = []
    for e in es:
        lo = max(mg1(e), mg2(e), mg3(e), 0); hi = mg4(e)
        if hi >= lo: feas.append((e, lo, hi))
    poly = [(X(e), Y(lo)) for e, lo, hi in feas] + [(X(e), Y(hi)) for e, lo, hi in feas[::-1]]
    g.poly(poly, GREEN, 0, fill=GREENBG, closed=True)
    g.line(x0, y0, X(46), y0, AX, 2); g.line(x0, y0, x0, Y(12.5), AX, 2)
    for e in range(0, 46, 10):
        g.line(X(e), y0, X(e), y0 + 6, AX, 1.4); g.text(X(e), y0 + 26, f"{e}", 14, MUTED, anchor="middle")
    for v in range(0, 13, 2):
        g.line(x0 - 6, Y(v), x0, Y(v), AX, 1.4); g.text(x0 - 10, Y(v) + 5, f"{v}", 14, MUTED, anchor="end")
    g.text(X(46), y0 + 26, "e（cm）", 15, INK, weight="bold")
    g.text(x0 + 10, Y(12.5) + 4, "1000 / P_i（1/t）", 15, INK, weight="bold")
    def clipline(fn, c, lab, pos, dash=None, dy=-8):
        pts = [(X(e), Y(fn(e))) for e in es if 0 <= fn(e) <= 11.2]
        g.poly(pts, c, 2.8, dash=dash)
        e = pos; g.text(X(e) + 8, Y(fn(e)) + dy, lab, 15, c, weight="bold")
    clipline(mg1, BLUE, "① 1/P ≥", 33, None)
    clipline(mg2, BLUE, "② 1/P ≥", 38, "7 5")
    clipline(mg3, RED, "③ 1/P ≥", 2, "7 5")
    clipline(mg4, RED, "④ 1/P ≤", 38, None, 26)
    g.circle(X(E), Y(INVP), 9, fill=ORG)
    g.text(X(E) - 14, Y(INVP) - 12, f"本例 e = 25、P_i = 150", 15, ORG, anchor="end", weight="bold")
    emax = feas[-1][0]
    g.circle(X(emax), Y(feas[-1][1]), 7, fill=W, stroke=PUR, sw=3)
    g.text(X(emax) + 10, Y(feas[-1][1]) + 24, f"e 的極限 ≈ {emax:.1f}", 15, PUR, weight="bold")
    card(g, 870, 50, 310, 330, PANEL, "#D5DAE1")
    for i, t in enumerate(["縱軸取 1/P，", "四個不等式全變成直線", "（對 e 線性）", "", "綠色區任一點 (e, P)", "都同時通過四個控制點", "", "最高點 = 最小預力", "最右點 = 最大偏心"]):
        g.text(895, 88 + i*32, t, 16, INK if i < 3 else GREEN if i < 6 else PUR, weight="bold" if i in (0, 4, 7, 8) else "normal")
    g.text(560, 26, "Magnel 圖：把 e 與 P 一起反算（P_e = 0.8P_i）", 19, INK, anchor="middle", weight="bold")
    g.save("figs/fig13_magnel.svg")


# ───────── fig14 最大活載：底纖維預算 ─────────
def fig14():
    g = SVG(1200, 440)
    x0 = 150; s = 3.6
    X = lambda f: x0 + (f + 45)*s
    rows = [("預力存款 f_{ce}", 0, FCE, BLUE), ("自重 M_d/S", FCE, FCE - MD*tm/S, RED),
            ("活載 M_{L,max}/S", FCE - MD*tm/S, -FTS_A, RED)]
    g.rect(X(-45), 60, X(0) - X(-45), 280, fill=REDBG, stroke="none")
    g.line(X(0), 50, X(0), 350, AX, 1.8)
    g.line(X(-FTS_A), 50, X(-FTS_A), 350, RED, 2.4, dash="7 5")
    g.text(X(-FTS_A), 372, f"−f_{{ts}} = −{FTS_A:.2f}", 15, RED, anchor="middle", weight="bold")
    g.text(X(0), 372, "0", 15, MUTED, anchor="middle")
    for i, (t, a, b, c) in enumerate(rows):
        y = 80 + i*88
        g.rect(min(X(a), X(b)), y, abs(X(b) - X(a)), 52, fill=BLUEF if c == BLUE else REDF, stroke=c, sw=2)
        g.text(x0 - 10 + 0, y + 32, "", 10)
        g.text(X(max(a, b)) + 12, y + 33, f"{t}　{sg(b - a)}", 17, c, weight="bold")
        if i: g.line(X(a), y - 36, X(a), y, AX, 1.2, dash="4 3")
    tot = FCE - MD*tm/S + FTS_A
    g.text(600, 30, "底纖維的「應力預算」：預壓存款扣掉自重，剩下的都能給活載用，扣到 −f_{ts} 為止", 18, INK, anchor="middle", weight="bold")
    g.text(600, 412, f"可用額度 {FCE - MD*tm/S:.2f} + {FTS_A:.2f} = {tot:.2f} kgf/cm² → M_{{L,max}} = {tot:.2f} × S = {MLMAX:.2f} t-m → w_{{L,max}} = {WLMAX:.3f} t/m", 16, PUR, anchor="middle", weight="bold")
    g.save("figs/fig14_budget.svg")


# ───────── fig15 P 的可行窗 ─────────
def fig15():
    g = SVG(1200, 400)
    x0, s = 100, 5.0
    X = lambda p: x0 + (p - 90)*s
    y = 220
    g.line(X(90), y, X(235), y, AX, 2.4)
    for p in range(90, 231, 20):
        g.line(X(p), y - 6, X(p), y + 6, AX, 1.4); g.text(X(p), y + 30, f"{p}", 14, MUTED, anchor="middle")
    g.text(X(235) + 8, y + 6, "P_i（t）", 16, INK, weight="bold")
    g.rect(X(PI_MIN), y - 28, X(PI_MAX1) - X(PI_MIN), 56, fill=GREENBG, stroke=GREEN, sw=2, rx=6)
    for n, v, op, c, h, ctrl, sub in [("④", PI_MIN, "≥", RED, 120, True, f"P_e ≥ {PE_MIN:.2f} ÷ 0.8"),
                                       ("①", PI_MAX1, "≤", BLUE, 120, True, "傳遞頂拉"),
                                       ("②", PI_MAX2, "≤", BLUE, 80, False, "傳遞底壓")]:
        g.line(X(v), y - h, X(v), y, c, 3 if ctrl else 1.8, dash=None if ctrl else "6 4")
        g.arrow(X(v), y - h, X(v) + (40 if op == "≥" else -40), y - h, c, 2.6, 11)
        badge(g, X(v), y - h - 26, n, ORG, 15, 15)
        side = -1 if n == "④" else 1
        g.text(X(v) + 22*side, y - h - 20, f"P_i {op} {v:.2f}", 16, c, anchor="start" if side > 0 else "end", weight="bold")
        g.text(X(v) + 22*side, y - h + 4, sub, 14, MUTED, anchor="start" if side > 0 else "end")
    g.line(X(PI_T), y - 34, X(PI_T), y + 34, ORG, 4)
    g.text(X(PI_T), y + 62, f"採用 P_i = {PI_T:.0f}（OK）", 17, ORG, anchor="middle", weight="bold")
    g.text(600, 30, "同一組式子把 P 當未知數：④ 撐起下限、① 壓住上限", 18, INK, anchor="middle", weight="bold")
    g.text(600, 380, f"可行窗 {PI_MIN:.2f} ≤ P_i ≤ {PI_MAX1:.2f} t（e = 25 固定）；③ 在 e > k 時恆成立", 16, GREEN, anchor="middle", weight="bold")
    g.save("figs/fig15_pwin.svg")


# ───────── fig16 SOP ─────────
def fig16():
    g = SVG(1200, 460)
    steps = [("Step 1", "開裂彎矩", ["f_{ce} = P_e/A + P_e e/S_b", "f_r = 2.0√f′_c", "M_{cr} = S_b(f_{ce} + f_r)"], BLUE, BLUEBG),
             ("Step 2", "極限強度", ["ρ_p → f_{ps} → a", "ε_t 定 φ", "φM_n ≥ M_u、1.2M_{cr}"], ORG, ORGBG),
             ("Step 3", "反算 e", ["① 等式 → e_{max}", "④ 等式 → e_{min}", "e_{min} ≤ e ≤ e_{max}"], GREEN, GREENBG),
             ("Step 4", "反算 w_L／P", ["M_{T,max} = S_b(f_{ce} + f_{ts})", "w_{L,max} = 8(M_T − M_d)/L²", "P_{e,min} 由 ④"], PUR, PURBG)]
    for i, (a, b, items, c, bg) in enumerate(steps):
        x = 20 + i*295
        card(g, x, 30, 270, 250, bg, c, 14, 2)
        g.text(x + 135, 68, a, 16, c, anchor="middle", weight="bold")
        g.text(x + 135, 102, b, 22, c, anchor="middle", weight="bold")
        for k, t in enumerate(items): g.text(x + 20, 152 + k*38, t, 16, INK)
        if i < 3: g.arrow(x + 272, 155, x + 292, 155, MUTED, 2.6, 10)
    # 決策
    dec = [(160, "1.2M_{cr} > φM_n？", "加非預力筋 A_s 或減 P_e"),
           (455, "ε_t < 0.005？", "φ 內插，或加壓筋"),
           (750, "e_{min} > e_{max}？", "加大斷面或調 P")]
    for x, q, a in dec:
        g.poly([(x, 300), (x + 120, 340), (x, 380), (x - 120, 340)], RED, 2, fill=REDBG, closed=True)
        g.text(x, 346, q, 15, RED, anchor="middle", weight="bold")
        g.text(x, 412, "是 → " + a, 15, RED, anchor="middle", weight="bold")
    g.text(1032, 346, "全部通過", 18, GREEN, anchor="middle", weight="bold")
    g.text(1032, 376, "→ 設計完成", 18, GREEN, anchor="middle", weight="bold")
    g.text(600, 448, "Step 1、2 是檢核（算出來比），Step 3、4 是設計（令等號反解）", 16, MUTED, anchor="middle")
    g.save("figs/fig16_sop.svg")


for f in [fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10, fig11, fig12, fig13, fig14, fig15, fig16]:
    f()
print("figs done")
