"""RC-U4-1 拼圖二：兩階段 × 四控制點 — 向量圖（所有數值由 params.py 算出）"""
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


