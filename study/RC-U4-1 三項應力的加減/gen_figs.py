"""RC-U4-1 拼圖一：三項應力的加減 — 向量圖（所有數值由 params.py 算出）"""
import math
from svglib import SVG, measure, INK, MUTED, GRID, PANEL
from params import *

BLUE, BLUEF = "#2F54C8", "#D6DFF7"      # 壓（+）
RED, REDF = "#C0392B", "#F4D9D6"        # 拉（−）
ORG = "#C2570C"                          # 鋼腱／預力
GOLD, GOLDBG = "#B7791F", "#FBF3E4"
GREEN, GREENBG = "#2E7D6B", "#E6F2EF"
PUR, PURBG = "#6D4BC2", "#F1EDFA"
BLUEBG, REDBG = "#EEF2FB", "#FBECEA"
NAVY = "#1B2432"
CONC, HATCH = "#EEF1F5", "#C9D0DA"
W = "#FFFFFF"
AX = "#5B6573"


def sg(v, d=2):
    v = v + (1e-9 if v >= 0 else -1e-9)
    return (f"+{v:.{d}f}" if v >= 0 else f"−{-v:.{d}f}")


def card(g, x, y, w, h, fill=PANEL, stroke="#D5DAE1", rx=12, sw=1.2):
    g.rect(x, y, w, h, fill=fill, stroke=stroke, sw=sw, rx=rx)


def pill(g, x, y, w, h, fill, txt, size=17, col=W):
    g.rect(x, y, w, h, fill=fill, stroke="none", rx=h/2)
    g.text(x + w/2, y + h/2 + size*0.36, txt, size, col, anchor="middle", weight="bold")


def hatch(g, x, y, w, h, step=16):
    g.rect(x, y, w, h, fill=CONC, stroke="none")
    k = -h
    while k < w:
        x1, y1, x2, y2 = x + k, y + h, x + k + h, y
        if x1 < x: y1 -= (x - x1); x1 = x
        if x2 > x + w: y2 += (x2 - (x + w)); x2 = x + w
        if x2 > x1: g.line(x1, y1, x2, y2, HATCH, 1)
        k += step


def block(g, x, y, w, h, sw=2.2):
    hatch(g, x, y, w, h)
    g.rect(x, y, w, h, fill="none", stroke=INK, sw=sw)


def pin(g, x, y, s=14):
    g.poly([(x, y), (x - s, y + s*1.4), (x + s, y + s*1.4)], INK, 2, fill=W, closed=True)
    g.line(x - s - 8, y + s*1.4 + 2, x + s + 8, y + s*1.4 + 2, INK, 2)


def roller(g, x, y, s=14):
    g.poly([(x, y), (x - s, y + s*1.2), (x + s, y + s*1.2)], INK, 2, fill=W, closed=True)
    for dx in (-8, 0, 8): g.circle(x + dx, y + s*1.2 + 5, 4, fill=W, stroke=INK, sw=1.6)
    g.line(x - s - 8, y + s*1.2 + 10, x + s + 8, y + s*1.2 + 10, INK, 2)


def udl(g, x1, x2, y, n=9, col=RED, lab=None, size=17):
    g.line(x1, y - 34, x2, y - 34, col, 2.2)
    for i in range(n):
        xx = x1 + (x2 - x1)*i/(n - 1)
        g.arrow(xx, y - 34, xx, y - 3, col, 1.8, 9)
    if lab: g.text((x1 + x2)/2, y - 44, lab, size, col, anchor="middle", weight="bold")


def curl(g, cx, cy, r, a1, a2, col, sw=2.6, head=12):
    """圓弧箭頭（數學角度，a1→a2）"""
    g.arc(cx, cy, r, a1, a2, col, sw)
    a = math.radians(a2)
    ex, ey = cx + r*math.cos(a), cy - r*math.sin(a)
    sgn = 1 if a2 > a1 else -1
    tx, ty = -math.sin(a)*sgn, -math.cos(a)*sgn        # SVG 切線方向
    bx, by = ex - tx*head, ey - ty*head
    nx, ny = -ty, tx
    g.poly([(ex, ey), (bx + nx*head*0.5, by + ny*head*0.5), (bx - nx*head*0.5, by - ny*head*0.5)],
           col, 1, fill=col, closed=True)


def stress(g, x, yt, yb, ft, fb, s, sw=2.4, zero=True):
    """應力圖：壓（+）畫在軸右側藍色、拉（−）畫在左側紅色"""
    col = lambda v: (BLUE, BLUEF) if v >= 0 else (RED, REDF)
    if ft*fb >= 0:
        c, f = col(ft if ft != 0 else fb)
        g.poly([(x, yt), (x + ft*s, yt), (x + fb*s, yb), (x, yb)], c, sw, fill=f, closed=True)
        y0 = None
    else:
        y0 = yt + (yb - yt)*ft/(ft - fb)
        c, f = col(ft); g.poly([(x, yt), (x + ft*s, yt), (x, y0)], c, sw, fill=f, closed=True)
        c, f = col(fb); g.poly([(x, y0), (x + fb*s, yb), (x, yb)], c, sw, fill=f, closed=True)
    g.line(x, yt - 6, x, yb + 6, AX, 2)
    if y0 is not None and zero: g.circle(x, y0, 5.5, fill=W, stroke=ORG, sw=2.4)
    return y0


def vlab(g, x, y, v, pre="", size=17, anchor="middle"):
    c = BLUE if v >= 0 else RED
    g.text(x, y, f"{pre}{sg(v)}", size, c, anchor=anchor, weight="bold")


def legend(g, x, y, size=15):
    g.line(x, y, x + 34, y, BLUE, 6, cap="round"); g.text(x + 44, y + 5, "壓應力（＋）", size, INK)
    g.line(x + 170, y, x + 204, y, RED, 6, cap="round"); g.text(x + 214, y + 5, "拉應力（−）", size, INK)


# ───────── fig01 總覽 ─────────
def fig01():
    g = SVG(1200, 430)
    card(g, 20, 10, 1160, 150, NAVY, NAVY, 14)
    g.text(600, 50, "斷面上任一點的應力 = 三張基本應力圖的加減", 23, W, anchor="middle", weight="bold")
    steps = [("Step 1　算純數值（先不管正負）", GOLD), ("Step 2　看變形定符號", PUR), ("Step 3　加減得合成應力", GREEN)]
    x = 55
    for i, (t, c) in enumerate(steps):
        w = measure(t, 19, True) + 56
        pill(g, x, 80, w, 52, c, t, 19)
        if i < 2: g.arrow(x + w + 10, 106, x + w + 58, 106, W, 2.6, 12)
        x += w + 68
    items = [
        ("①", "軸壓 P/A", "矩形", "全斷面同號（恆為壓）", (T1, T1), BLUE, BLUEBG),
        ("②", "偏心 P·e/S", "三角形", "上拉下壓（上下反號）", (-T2, T2), ORG, "#FCEEE5"),
        ("③", "外力 M/S", "三角形", "上壓下拉（與②反向）", (T3, -T3), RED, REDBG),
        ("④", "合成應力", "梯形", "三張圖逐點相加", (FT_I, FB_I), GREEN, GREENBG),
    ]
    for i, (n, hd, shape, desc, (a, b), c, bg) in enumerate(items):
        X = 20 + i*298
        card(g, X, 185, 268, 235, bg, c, 12, 2)
        g.circle(X + 32, 220, 19, fill=c, stroke=c, sw=1)
        g.text(X + 32, 227, n, 19, W, anchor="middle", weight="bold")
        g.text(X + 60, 228, hd, 20, c, weight="bold")
        stress(g, X + 70, 262, 402, a, b, 0.52, 2)
        g.text(X + 140, 300, shape, 20, INK, weight="bold")
        for k, t in enumerate([desc[:desc.find("（")] if "（" in desc else desc,
                               desc[desc.find("（"):] if "（" in desc else ""]):
            if t: g.text(X + 140, 336 + k*30, t, 15, MUTED)
        if i < 3:
            g.text(X + 283, 312, "+" if i < 2 else "=", 26, INK, anchor="middle", weight="bold")
    g.save("figs/fig01_map.svg")


# ───────── fig02 示範梁 ─────────
def fig02():
    g = SVG(1200, 440)
    x1, x2, yT, hB = 70, 740, 150, 64
    ycg = yT + hB/2; yten = ycg + E/H*hB
    udl(g, x1, x2, yT, 13, RED, f"自重 w_d = {WD:.3f} t/m", 17)
    block(g, x1, yT, x2 - x1, hB)
    g.line(x1 - 20, ycg, x2 + 20, ycg, AX, 1.4, dash="7 5"); g.text(x2 + 26, ycg + 5, "c.g.", 14, MUTED)
    g.line(x1, yten, x2, yten, ORG, 3.2)
    g.text(x1 + 130, yten + 2 + 22, "鋼腱（直線，形心下方 e = 25 cm）", 14, ORG, weight="bold")
    pin(g, x1 + 20, yT + hB); roller(g, x2 - 20, yT + hB)
    ya = yT + hB + 40
    g.arrow((x1 + x2)/2, ya, x1 + 20, ya, MUTED, 1.4, 9); g.arrow((x1 + x2)/2, ya, x2 - 20, ya, MUTED, 1.4, 9)
    g.text((x1 + x2)/2, ya - 6, f"L = {L:.0f} m（簡支）", 15, MUTED, anchor="middle", bg=W)
    # 彎矩圖
    y0 = 300; amp = 92; xs = [x1 + 20 + (x2 - x1 - 40)*i/40 for i in range(41)]
    pts = [(xx, y0 + amp*4*((xx - x1 - 20)/(x2 - x1 - 40))*(1 - (xx - x1 - 20)/(x2 - x1 - 40))) for xx in xs]
    g.poly([(x1 + 20, y0)] + pts + [(x2 - 20, y0)], "#8B98A9", 2, fill="#E9EDF2", closed=True)
    g.line(x1 + 20, y0, x2 - 20, y0, AX, 1.6)
    xm = (x1 + x2)/2
    g.line(xm, yT - 6, xm, y0 + amp + 8, PUR, 1.6, dash="6 4")
    g.text(xm + 10, y0 + amp - 8, f"M_d = w_d L²/8 = {MD:.3f} t-m", 16, INK, weight="bold")
    g.text(x2 - 20, y0 - 8, "自重彎矩圖（下垂為正）", 14, MUTED, anchor="end")
    g.text(xm, y0 + amp + 30, "檢核斷面：跨中", 15, PUR, anchor="middle", weight="bold")
    # 斷面
    k = 3.6; sx = 900; sy = 60; bw, hh = B*k, H*k
    block(g, sx, sy, bw, hh)
    cy = sy + hh/2; ty = cy + E*k
    g.line(sx - 30, cy, sx + bw + 26, cy, AX, 1.4, dash="7 5"); g.text(sx + bw + 30, cy + 5, "c.g.", 14, MUTED)
    g.circle(sx + bw/2, ty, 9, fill=ORG, stroke=W)
    g.text(sx + bw/2 + 16, ty + 6, "A_{ps}", 16, ORG, weight="bold")
    g.arrow(sx - 18, cy + 4, sx - 18, ty, MUTED, 1.4, 8); g.text(sx - 26, (cy + ty)/2 + 5, "e = 25", 14, MUTED, anchor="end")
    g.line(sx, sy + hh + 10, sx, sy + hh + 30, MUTED, 1); g.line(sx + bw, sy + hh + 10, sx + bw, sy + hh + 30, MUTED, 1)
    g.arrow(sx + bw/2, sy + hh + 22, sx, sy + hh + 22, MUTED, 1.3, 8); g.arrow(sx + bw/2, sy + hh + 22, sx + bw, sy + hh + 22, MUTED, 1.3, 8)
    g.text(sx + bw/2, sy + hh + 45, "b = 40", 14, MUTED, anchor="middle")
    g.line(sx + bw + 70, sy, sx + bw + 70, sy + hh, MUTED, 1.3)
    g.text(sx + bw + 78, sy + hh/2 - 40, "h = 80", 14, MUTED)
    g.text(sx + bw + 12, sy + 20, "頂纖維", 15, INK, weight="bold")
    g.text(sx + bw + 12, sy + hh - 8, "底纖維", 15, INK, weight="bold")
    g.text(sx + bw/2, sy - 14, "跨中斷面 40×80 cm", 17, INK, anchor="middle", weight="bold")
    g.save("figs/fig02_beam.svg")


# ───────── fig03 軸壓項 ─────────
def fig03():
    g = SVG(1200, 440)
    bx, by, bw, bh = 150, 110, 430, 240
    block(g, bx, by, bw, bh)
    cy = by + bh/2
    g.line(bx - 40, cy, bx + bw + 40, cy, AX, 1.4, dash="7 5"); g.text(bx + bw + 50, cy + 26, "c.g.", 14, MUTED)
    g.arrow(bx - 110, cy, bx - 4, cy, ORG, 4, 18); g.text(bx - 60, cy - 16, "P", 24, ORG, anchor="middle", weight="bold")
    g.arrow(bx + bw + 110, cy, bx + bw + 4, cy, ORG, 4, 18); g.text(bx + bw + 60, cy - 16, "P", 24, ORG, anchor="middle", weight="bold")
    for i in range(7):
        yy = by + 20 + (bh - 40)*i/6
        g.arrow(bx + 60, yy, bx + 110, yy, BLUE, 2, 9); g.arrow(bx + bw - 60, yy, bx + bw - 110, yy, BLUE, 2, 9)
    g.text(bx + bw/2, cy - 6, "每一條纖維", 18, INK, anchor="middle", weight="bold", bg=W)
    g.text(bx + bw/2, cy + 24, "被推短同樣多", 18, INK, anchor="middle", weight="bold", bg=W)
    g.text(bx + bw/2, by - 22, "假想：預力合力移到形心 c.g. 推梁", 19, INK, anchor="middle", weight="bold")
    g.text(bx + bw/2, by + bh + 42, "只有「推」、沒有「彎」→ 應變均勻 → 應力均勻", 16, MUTED, anchor="middle")
    # 應力圖
    ax = 880; s = 2.2
    g.text(ax + T1*s/2, by - 22, "① 軸壓項：矩形", 19, BLUE, anchor="middle", weight="bold")
    stress(g, ax, by, by + bh, T1, T1, s, 2.6)
    g.text(ax - 12, by + 6, "頂", 16, INK, anchor="end", weight="bold"); g.text(ax - 12, by + bh + 6, "底", 16, INK, anchor="end", weight="bold")
    vlab(g, ax + T1*s + 12, by + 6, T1, size=18, anchor="start"); vlab(g, ax + T1*s + 12, by + bh + 6, T1, size=18, anchor="start")
    g.text(ax + T1*s/2, by + bh + 42, f"P_i/A = 150 000 / 3 200 = {T1:.3f}", 16, INK, anchor="middle")
    legend(g, 800, 30)
    g.save("figs/fig03_axial.svg")


# ───────── fig04 偏心項 ─────────
def fig04():
    g = SVG(1200, 440)
    bw, bh, by = 170, 130, 150
    cy = by + bh/2; ey = cy + 42
    cols = [30, 360, 700]
    heads = ["實際：P 作用在鋼腱", "① 搬到形心的 P", "② 補上的力偶 P·e"]
    for i, X in enumerate(cols):
        block(g, X + 30, by, bw, bh)
        g.line(X + 14, cy, X + bw + 46, cy, AX, 1.2, dash="6 4")
        g.text(X + 30 + bw/2, by - 50, heads[i], 18, [ORG, BLUE, ORG][i], anchor="middle", weight="bold")
    X = cols[0]
    g.arrow(X - 12, ey, X + 28, ey, ORG, 3.4, 14); g.arrow(X + bw + 72, ey, X + bw + 32, ey, ORG, 3.4, 14)
    g.line(X + 30, ey, X + 30 + bw, ey, ORG, 2.6, dash="8 5")
    g.text(X + 30 + bw/2, by + bh + 34, "鋼腱在形心下方 e", 14, ORG, anchor="middle")
    g.arrow(X + 30 + bw/2 - 60, cy, X + 30 + bw/2 - 60, ey, MUTED, 1.2, 7)
    g.text(X + 30 + bw/2 - 66, (cy + ey)/2 + 5, "e", 15, MUTED, anchor="end", italic=True)
    g.text(cols[1] - 39, cy + 10, "=", 34, INK, anchor="middle", weight="bold")
    g.text(cols[2] - 59, cy + 10, "+", 34, INK, anchor="middle", weight="bold")
    X = cols[1]
    g.arrow(X - 12, cy, X + 28, cy, BLUE, 3.4, 14); g.arrow(X + bw + 72, cy, X + bw + 32, cy, BLUE, 3.4, 14)
    g.text(X + 30 + bw/2, by + bh + 34, "→ 就是上一頁的 P/A", 14, BLUE, anchor="middle")
    X = cols[2]
    curl(g, X + 30, cy, 48, 250, 110, ORG)          # 左端：逆時針
    curl(g, X + 30 + bw, cy, 48, -70, 70, ORG)      # 右端：順時針
    # 上拱示意
    g.text(X + 30 + bw/2, by + bh + 34, "兩端力偶把梁往上彎（上拱）", 14, ORG, anchor="middle")
    g.text(X + 18, by - 12, "P·e", 16, ORG, anchor="middle", weight="bold")
    g.text(X + 42 + bw, by - 12, "P·e", 16, ORG, anchor="middle", weight="bold")
    # 應力三角形
    ax = 1080; s = 1.05; yt, yb = 110, 370
    g.text(ax, 70, "② 偏心項：三角形", 19, ORG, anchor="middle", weight="bold")
    stress(g, ax, yt, yb, -T2, T2, s, 2.6)
    vlab(g, ax - 10, yt - 12, -T2, "頂 ", 17); vlab(g, ax + 10, yb + 28, T2, "底 ", 17)
    g.text(ax - 60, (yt + yb)/2 + 5, "中性軸", 13, MUTED, anchor="end")
    g.text(600, 420, f"P·e/S = 150 000 × 25 / 42 667 = {T2:.3f}　上下兩緣等值反號（對稱斷面 S_t = S_b）", 16, INK, anchor="middle")
    g.save("figs/fig04_ecc.svg")


# ───────── fig05 外力項 ─────────
def fig05():
    g = SVG(1200, 440)
    x1, x2, yT, hB = 70, 690, 120, 56
    udl(g, x1, x2, yT, 12, RED, "外載重（傳遞階段只有自重 w_d）", 17)
    block(g, x1, yT, x2 - x1, hB)
    pin(g, x1 + 20, yT + hB); roller(g, x2 - 20, yT + hB)
    y0 = 250; amp = 110
    xs = [x1 + 20 + (x2 - x1 - 40)*i/40 for i in range(41)]
    t = lambda xx: (xx - x1 - 20)/(x2 - x1 - 40)
    g.poly([(x1 + 20, y0)] + [(xx, y0 + amp*4*t(xx)*(1 - t(xx))) for xx in xs] + [(x2 - 20, y0)], "#8B98A9", 2, fill="#E9EDF2", closed=True)
    g.line(x1 + 20, y0, x2 - 20, y0, AX, 1.6)
    xm = (x1 + x2)/2
    g.line(xm, yT - 20, xm, y0 + amp, PUR, 1.8, dash="6 4")
    g.text(xm + 10, y0 + amp - 10, f"M_d = {MD:.3f} t-m", 17, INK, weight="bold")
    g.text(x1 + 20, y0 + 26, "M 圖", 14, MUTED)
    g.arrow(x2 + 30, 240, 930, 240, PUR, 2.4, 12)
    g.text((x2 + 960)/2, 228, "切開跨中斷面", 15, PUR, anchor="middle", weight="bold")
    ax = 1010; s = 2.2; yt, yb = 110, 370
    g.text(ax, 70, "③ 外力項：三角形", 19, RED, anchor="middle", weight="bold")
    stress(g, ax, yt, yb, T3, -T3, s, 2.6)
    vlab(g, ax + 10, yt - 12, T3, "頂 ", 17); vlab(g, ax - 10, yb + 28, -T3, "底 ", 17)
    g.text(ax + 16, (yt + yb)/2 + 5, "中性軸", 13, MUTED)
    g.text(600, 420, f"M_d/S = 13.824 × 10^5 / 42 667 = {T3:.3f}　方向恰好與②相反 → 預力「抵銷」載重", 16, INK, anchor="middle")
    g.save("figs/fig05_ext.svg")


# ───────── fig06 變形直覺 ─────────
def band(g, x1, x2, ym, amp, th, up):
    n = 40; top, bot = [], []
    for i in range(n + 1):
        t = i/n; d = amp*math.sin(math.pi*t)*(-1 if up else 1)
        xx = x1 + (x2 - x1)*t
        top.append((xx, ym - th/2 + d)); bot.append((xx, ym + th/2 + d))
    g.poly(top + bot[::-1], INK, 2, fill=CONC, closed=True)
    g.line(x1, ym, x2, ym, "#AEB6C2", 1.4, dash="7 5")


def fig06():
    g = SVG(1200, 440)
    P = [(20, "偏心項 P·e/S：鋼腱把梁「頂」上去", ORG, True, "#FDF3EC"),
         (610, "外力項 M/S：載重把梁「壓」下來", RED, False, REDBG)]
    for X, hd, c, up, bg in P:
        card(g, X, 10, 570, 420, bg, "#E3D6CC" if up else "#EBC3BE", 14, 1.4)
        g.text(X + 285, 50, hd, 20, c, anchor="middle", weight="bold")
        x1, x2, ym = X + 50, X + 400, 190
        if up:
            n = 5
            for i in range(n):
                xx = x1 + 60 + (x2 - x1 - 120)*i/(n - 1)
                g.arrow(xx, ym + 80, xx, ym + 38, ORG, 2.4, 10)
            g.text((x1 + x2)/2, ym + 104, "鋼腱在形心下方 → 反拱力向上頂", 14, ORG, anchor="middle")
        else:
            udl(g, x1, x2, ym - 42, 9, RED, None)
            g.text((x1 + x2)/2, 96, "外載重（含自重）向下壓", 14, RED, anchor="middle")
        band(g, x1, x2, ym, 26, 34, up)
        pin(g, x1, ym + 17, 11); roller(g, x2, ym + 17, 11)
        xm = (x1 + x2)/2; d = -26 if up else 26
        ytop, ybot = ym - 17 + d, ym + 17 + d
        if up:   # 頂拉開、底壓緊
            g.arrow(xm - 10, ytop - 14, xm - 62, ytop - 14, RED, 2.6, 11); g.arrow(xm + 10, ytop - 14, xm + 62, ytop - 14, RED, 2.6, 11)
            g.arrow(xm - 62, ybot + 14, xm - 16, ybot + 14, BLUE, 2.6, 11); g.arrow(xm + 62, ybot + 14, xm + 16, ybot + 14, BLUE, 2.6, 11)
        else:
            g.arrow(xm - 62, ytop - 14, xm - 16, ytop - 14, BLUE, 2.6, 11); g.arrow(xm + 62, ytop - 14, xm + 16, ytop - 14, BLUE, 2.6, 11)
            g.arrow(xm - 10, ybot + 14, xm - 62, ybot + 14, RED, 2.6, 11); g.arrow(xm + 10, ybot + 14, xm + 62, ybot + 14, RED, 2.6, 11)
        # 小應力圖
        ax = X + 490; yt, yb = 110, 290
        a, b = (-T2, T2) if up else (T3, -T3)
        stress(g, ax, yt, yb, a, b, 0.62 if up else 1.4, 2.2)
        g.text(ax, 92, "應力圖", 14, MUTED, anchor="middle")
        # 結論
        g.text(X + 285, 345, "梁上拱 ⇒ 頂面被拉開、底面被壓緊" if up else "梁下垂 ⇒ 頂面被壓緊、底面被拉開", 17, INK, anchor="middle", weight="bold")
        tl, tc = ("頂 受拉（−）", RED) if up else ("頂 受壓（＋）", BLUE)
        bl, bc = ("底 受壓（＋）", BLUE) if up else ("底 受拉（−）", RED)
        pill(g, X + 70, 370, 200, 42, tc, tl, 17); pill(g, X + 300, 370, 200, 42, bc, bl, 17)
    g.save("figs/fig06_deform.svg")


# ───────── fig07 非對稱斷面 ─────────
def fig07():
    g = SVG(1200, 440)
    k = 3.0; top = 60; bx = 260
    slab_w, slab_t = 150*k, 15*k
    ybot = top + slab_t + 80*k
    ycg = ybot - YB3*k
    sx = bx - slab_w/2 + 60
    block(g, sx, top, slab_w, slab_t)
    block(g, bx - B*k/2 + 60, top + slab_t, B*k, 80*k)
    cx = bx + 60
    g.line(sx - 20, ycg, 1150, ycg, AX, 1.4, dash="7 5"); g.text(sx - 26, ycg + 5, "組合 c.g.", 14, MUTED, anchor="end")
    g.line(sx - 20, top + slab_t + 40*k, cx - 70, top + slab_t + 40*k, "#AEB6C2", 1.2, dash="3 4")
    g.text(sx - 26, top + slab_t + 40*k + 5, "梁半高", 13, "#9AA3AE", anchor="end")
    g.arrow(cx + 90, ycg, cx + 90, ybot, MUTED, 1.3, 8); g.text(cx + 98, (ycg + ybot)/2 + 5, f"y_b = {YB3:.2f}", 15, MUTED)
    g.arrow(cx + 90, ycg, cx + 90, top + slab_t, MUTED, 1.3, 8); g.text(cx + 98, (ycg + top + slab_t)/2 + 10, f"y_t = {HB - YB3:.2f}（梁頂）", 15, MUTED)
    g.text(cx, top - 16, "組合斷面（主講義例題②）", 17, INK, anchor="middle", weight="bold")
    # 應力：ΔM = 32.40 t-m
    ax = 840; s = 3.0
    f_slab = ML2*tm*(95 - YB3)/I3
    yt_beam = top + slab_t
    stress(g, ax, top, ybot, f_slab, DB3, s, 2.6)
    g.line(ax - 10, yt_beam, ax + DT3*s + 10, yt_beam, BLUE, 1.6, dash="4 3")
    vlab(g, ax + f_slab*s + 10, top + 6, f_slab, "板頂 ", 16, "start")
    vlab(g, ax + DT3*s + 14, yt_beam + 24, DT3, "梁頂 ", 16, "start")
    vlab(g, ax + DB3*s - 10, ybot + 6, DB3, "底 ", 17, "end")
    g.text(ax + 150, 200, f"梁頂：S_t = I/y_t = {ST3:,.0f} cm³", 15, INK)
    g.text(ax + 150, 228, f"底緣：S_b = I/y_b = {SB3:,.0f} cm³", 15, INK)
    g.text(ax + 150, 256, f"S_t ≈ {ST3/SB3:.1f} × S_b", 15, PUR, weight="bold")
    g.text(ax + 40, top - 16, f"同一個 M = {ML2:.2f} t-m 的外力項", 17, RED, anchor="middle", weight="bold")
    g.text(700, 420, "零點在「形心」而不在半高；離形心越遠應力越大 → 頂、底必須分開除 S_t、S_b", 16, INK, anchor="middle")
    g.save("figs/fig07_asym.svg")


# ───────── fig08 Step 1 + Step 2 ─────────
def fig08():
    g = SVG(1200, 420)
    hx = [30, 470, 700, 900]; hw = [430, 220, 190, 270]
    heads = ["Step 1　純數值（kgf/cm²）", "Step 2　頂纖維", "底纖維", "判斷依據"]
    for x, w, t in zip(hx, hw, heads):
        g.rect(x, 20, w, 50, fill=NAVY, stroke="none", rx=8)
        g.text(x + w/2, 52, t, 18, W, anchor="middle", weight="bold")
    rows = [("① P/A", T1, (+1, +1), "全斷面同號，恆壓", BLUE),
            ("② P·e/S", T2, (-1, +1), "鋼腱頂上去 → 上拱", ORG),
            ("③ M_d/S", T3, (+1, -1), "載重壓下來 → 下垂", RED)]
    s = 2.6
    for i, (lab, v, (st, sb), why, c) in enumerate(rows):
        y = 90 + i*105
        g.rect(30, y, 1140, 92, fill=PANEL if i % 2 == 0 else W, stroke="#E3E7EC", rx=8)
        g.text(50, y + 55, lab, 19, c, weight="bold")
        g.rect(160, y + 30, v*s*0.95, 32, fill=GOLDBG, stroke=GOLD, sw=1.6, rx=4)
        g.text(160 + v*s*0.95 + 10, y + 54, f"{v:.3f}", 19, GOLD, weight="bold")
        for x, w, sgn in ((470, 220, st), (700, 190, sb)):
            cc = BLUE if sgn > 0 else RED
            pill(g, x + w/2 - 70, y + 24, 140, 44, cc, "＋（壓）" if sgn > 0 else "−（拉）", 18)
        g.text(920, y + 54, why, 17, INK)
    g.text(600, 408, "Step 1 只寫大小、不寫符號；Step 2 才依變形逐項加上 ＋／−，兩步分開就不會亂", 16, MUTED, anchor="middle")
    g.save("figs/fig08_steps.svg")


# ───────── fig09 / fig11 疊加 ─────────
def superpose(fn, t1, t2, t3, title_stage, s):
    g = SVG(1200, 450)
    yt, yb = 110, 350
    ft, fb = t1 - t2 + t3, t1 + t2 - t3
    # 斷面
    k = (yb - yt)/H; sx = 40; bw = B*k
    block(g, sx, yt, bw, yb - yt)
    cy = (yt + yb)/2; g.line(sx - 10, cy, sx + bw + 20, cy, AX, 1.2, dash="6 4")
    g.circle(sx + bw/2, cy + E*k, 7, fill=ORG, stroke=W)
    g.text(sx + bw/2, yt - 16, "斷面", 17, INK, anchor="middle", weight="bold")
    g.text(sx + bw/2, 34, title_stage, 18, PUR, anchor="start", weight="bold")
    cols = [(300, "① P/A", t1, t1, "start"), (520, "② P·e/S", -t2, t2, "mid"), (760, "③ M/S", t3, -t3, "mid"), (1010, "④ 合成", ft, fb, "start")]
    ops = ["+", "+", "="]
    for i, (x, hd, a, b, mode) in enumerate(cols):
        ax = x - 40 if mode == "start" else x
        if i == 3: ax = x - 50
        y0 = stress(g, ax, yt, yb, a, b, s, 2.6)
        g.text(x, yt - 44, hd, 19, [BLUE, ORG, RED, GREEN][i], anchor="middle", weight="bold")
        vlab(g, x, yb + 40, a, "頂 ", 17); vlab(g, x, yb + 68, b, "底 ", 17)
        if i < 3: g.text((x + cols[i + 1][0])/2 + (10 if i == 2 else 0), cy + 12, ops[i], 34, "#7A8594", anchor="middle", weight="bold")
        if i == 3 and y0 is not None:
            z = (y0 - yt)/k
            g.line(ax, y0, ax + 90, y0, ORG, 1.2, dash="4 3")
            g.text(ax + 96, y0 + 5, f"零點離頂 {z:.2f} cm" if z < H/2 else f"零點離底 {H - z:.2f} cm", 14, ORG)
    legend(g, 40, 430, 14)
    fs = f"f_頂 = {t1:.3f} − {t2+1e-9:.3f} + {t3:.3f} = {sg(ft)}　｜　f_底 = {t1:.3f} + {t2+1e-9:.3f} − {t3:.3f} = {sg(fb)}"
    g.save(f"figs/{fn}.svg")


# ───────── fig10 瀑布圖 ─────────
def fig10():
    g = SVG(1200, 440)
    P = [(20, "頂纖維", [(T1, "① +P/A"), (-T2, "② −P·e/S"), (T3, "③ +M/S")], -70, 70),
         (610, "底纖維", [(T1, "① +P/A"), (T2, "② +P·e/S"), (-T3, "③ −M/S")], -10, 150)]
    for X, hd, terms, lo, hi in P:
        card(g, X, 10, 570, 420, PANEL, "#E3E7EC", 14)
        g.text(X + 24, 46, hd, 21, INK, weight="bold")
        x0, x1 = X + 150, X + 540
        sx = (x1 - x0)/(hi - lo); XV = lambda v: x0 + (v - lo)*sx
        rows_y = [90, 150, 210, 300]
        g.line(XV(0), 70, XV(0), 350, AX, 2)
        g.text(XV(0), 372, "0", 14, MUTED, anchor="middle")
        cum = 0.0
        for j, (v, lab) in enumerate(terms):
            a, b = cum, cum + v; y = rows_y[j]
            c, f = (BLUE, BLUEF) if v > 0 else (RED, REDF)
            g.rect(min(XV(a), XV(b)), y, abs(XV(b) - XV(a)), 36, fill=f, stroke=c, sw=2, rx=4)
            g.arrow(XV(a), y + 18, XV(b), y + 18, c, 2.2, 10)
            g.text(X + 24, y + 25, lab, 16, c, weight="bold")
            g.text(XV(b) + (8 if v > 0 else -8), y + 25, f"{sg(b)}", 15, INK, anchor="start" if v > 0 else "end", weight="bold")
            if j < 2: g.line(XV(b), y + 36, XV(b), rows_y[j + 1], "#9AA3AE", 1.2, dash="4 3")
            cum = b
        y = rows_y[3]; c, f = (BLUE, BLUEF) if cum > 0 else (RED, REDF)
        g.line(XV(cum), rows_y[2] + 36, XV(cum), y, "#9AA3AE", 1.2, dash="4 3")
        g.rect(min(XV(0), XV(cum)), y, abs(XV(cum) - XV(0)), 40, fill=c, stroke=c, rx=4)
        g.text(X + 24, y + 27, "④ 合成", 17, GREEN, weight="bold")
        g.text(XV(cum) + (10 if cum > 0 else -10), y + 27, f"{sg(cum)}" + ("（壓）" if cum > 0 else "（拉）"), 17, c, anchor="start" if cum > 0 else "end", weight="bold")
        for v in range(int(lo/20)*20, hi + 1, 20 if hi - lo < 150 else 50):
            if v != 0 and lo <= v <= hi:
                g.line(XV(v), 346, XV(v), 352, AX, 1); g.text(XV(v), 372, f"{v}", 13, MUTED, anchor="middle")
        note = (f"只有預力時已到 {sg(FT_P)}；自重把它拉回 {sg(FT_I)}" if hd == "頂纖維"
                else f"預力疊到 {sg(T1 + T2)}；自重減掉 {T3:.2f}")
        g.text(X + 285, 408, note, 15, PUR, anchor="middle", weight="bold")
        g.text(x1, 392, "kgf/cm²", 12, MUTED, anchor="end")
    g.save("figs/fig10_waterfall.svg")


# ───────── fig12 核心距 ─────────
def fig12():
    g = SVG(1200, 440)
    x0, x1, y0, y1 = 110, 780, 390, 40      # 圖框
    emax, flo, fhi = 30, -70, 150
    X = lambda e: x0 + e/emax*(x1 - x0)
    Y = lambda f: y0 - (f - flo)/(fhi - flo)*(y0 - y1)
    g.rect(X(0), y1, X(K) - X(0), y0 - y1, fill=GREENBG, stroke="none")
    g.text((X(0) + X(K))/2, y1 + 22, "e ≤ k：頂纖維不出現拉", 14, GREEN, anchor="middle", weight="bold")
    g.line(x0, Y(0), x1, Y(0), AX, 1.6)
    g.line(x0, y1, x0, y0, AX, 1.6)
    for f in range(-60, 151, 30):
        g.line(x0 - 5, Y(f), x0, Y(f), AX, 1); g.text(x0 - 9, Y(f) + 5, f"{f}", 13, MUTED, anchor="end")
    for e in range(0, 31, 5):
        g.line(X(e), y0, X(e), y0 + 5, AX, 1); g.text(X(e), y0 + 20, f"{e}", 13, MUTED, anchor="middle")
    g.line(x0, y0, x1, y0, AX, 1.4); g.text(x1, y0 + 40, "偏心距 e（cm）", 14, MUTED, anchor="end")
    g.text(x0 - 60, y1 - 12, "應力（kgf/cm²）", 14, MUTED)
    fb = lambda e: T1*(1 + e/K); ft = lambda e: T1*(1 - e/K)
    g.line(X(0), Y(fb(0)), X(emax), Y(fb(emax)), BLUE, 2.4, dash="8 5")
    g.text(X(emax) - 4, Y(fb(emax)) - 10, "底纖維 P/A(1+e/k)", 14, BLUE, anchor="end")
    g.line(X(0), Y(ft(0)), X(emax), Y(ft(emax)), RED, 3)
    g.text(X(28), Y(ft(28)) + 30, "頂纖維 P/A(1−e/k)", 14, RED, anchor="end", weight="bold")
    g.circle(X(K), Y(0), 7, fill=GREEN, stroke=W)
    g.text(X(K) + 10, Y(0) - 12, f"k = S/A = {K:.2f} = h/6", 15, GREEN, weight="bold")
    g.line(X(E), y1 + 30, X(E), y0, "#9AA3AE", 1.2, dash="4 3")
    g.circle(X(E), Y(FT_P), 7, fill=RED, stroke=W)
    g.text(X(E) + 12, Y(FT_P) + 6, f"只有預力 {sg(FT_P)}", 15, RED, weight="bold", bg=W)
    g.arrow(X(E) - 16, Y(FT_P) - 4, X(E) - 16, Y(FT_I) + 8, PUR, 2.6, 11)
    g.text(X(E) + 12, (Y(FT_P) + Y(FT_I))/2 + 5, f"+自重 {T3:.2f}", 15, PUR, weight="bold", bg=W)
    g.circle(X(E), Y(FT_I), 7, fill=PUR, stroke=W)
    g.text(X(E) + 12, Y(FT_I) - 4, f"傳遞階段 {sg(FT_I)}", 15, PUR, weight="bold", bg=W)
    g.circle(X(E), Y(fb(E)), 6, fill=BLUE, stroke=W)
    g.text(X(E) + 12, Y(fb(E)) + 5, f"{sg(fb(E))}", 14, BLUE)
    # 斷面核心
    k = 3.3; sx, sy = 920, 50; bw, hh = B*k, H*k
    block(g, sx, sy, bw, hh)
    cy = sy + hh/2
    g.rect(sx, cy - K*k, bw, 2*K*k, fill=GREEN, stroke=GREEN, sw=1.5, op=0.25)
    g.text(sx + bw + 10, cy + 5, "核心（中 1/3）", 14, GREEN, weight="bold")
    g.line(sx - 10, cy, sx + bw + 6, cy, AX, 1.2, dash="6 4")
    g.circle(sx + bw/2, cy + E*k, 8, fill=ORG, stroke=W)
    g.text(sx + bw + 10, cy + E*k + 5, "e = 25 > k", 14, ORG, weight="bold")
    g.text(sx + bw/2, sy - 14, "40×80 斷面", 15, INK, anchor="middle", weight="bold")
    g.text(sx + bw/2, sy + hh + 30, "鋼腱在核心外 → 頂纖維必出現拉", 13, MUTED, anchor="middle")
    g.save("figs/fig12_kern.svg")


if __name__ == "__main__":
    fig01(); fig02(); fig03(); fig04(); fig05(); fig06(); fig07(); fig08()
    superpose("fig09_transfer", T1, T2, T3, "傳遞階段：P_i = 150 t、M_d = 13.824 t-m", 0.95)
    fig10()
    superpose("fig11_service", U1, U2, U3, "使用階段：P_e = 120 t、M_T = 58.824 t-m", 0.62)
    fig12()
    print("figs ok")
