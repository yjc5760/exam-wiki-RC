"""RC-U2-1 拼圖二：三大傳力機制與桁架類比 — 向量圖（所有數值由 params.py 算出）"""
import math
from svglib import SVG, measure, INK, MUTED, GRID, PANEL
from params import *
R_ = math.radians

PUR, PURBG = "#6D4BC2", "#F1EDFA"
RED, REDBG = "#C0392B", "#FBECEA"
BLUE, BLUEBG = "#2F54C8", "#EEF2FB"
GOLD, GOLDBG = "#B7791F", "#FBF3E4"
GREEN, GREENBG = "#2E7D6B", "#E6F2EF"
ORG = "#D9661F"
NAVY = "#1B2432"
CONC, HATCH = "#EEF1F5", "#C9D0DA"
W = "#FFFFFF"


def card(g, x, y, w, h, fill=PANEL, stroke="#D5DAE1", rx=12, sw=1.2):
    g.rect(x, y, w, h, fill=fill, stroke=stroke, sw=sw, rx=rx)


def dot(g, x, y, c, r=7): g.circle(x, y, r, fill=c, stroke=W, sw=2)


def pill(g, x, y, w, h, fill, txt, size=17, col=W):
    g.rect(x, y, w, h, fill=fill, stroke="none", rx=h/2)
    g.text(x + w/2, y + h/2 + size*0.36, txt, size, col, anchor="middle", weight="bold")


def hatch(g, x, y, w, h, step=16):
    """混凝土斜線填充（裁在矩形內）"""
    g.rect(x, y, w, h, fill=CONC, stroke="none")
    k = -h
    while k < w:
        x1, y1 = x + k, y + h
        x2, y2 = x + k + h, y
        # 裁切
        if x1 < x: y1 -= (x - x1); x1 = x
        if x2 > x + w: y2 += (x2 - (x + w)); x2 = x + w
        if x2 > x1: g.line(x1, y1, x2, y2, HATCH, 1)
        k += step


def beam(g, x, y, w, h, sw=2.4):
    hatch(g, x, y, w, h)
    g.rect(x, y, w, h, fill="none", stroke=INK, sw=sw)


def pin(g, x, y, s=16):
    g.poly([(x, y), (x - s, y + s*1.4), (x + s, y + s*1.4)], INK, 2, fill=W, closed=True)
    g.line(x - s - 8, y + s*1.4 + 2, x + s + 8, y + s*1.4 + 2, INK, 2)


def roller(g, x, y, s=16):
    g.poly([(x, y), (x - s, y + s*1.2), (x + s, y + s*1.2)], INK, 2, fill=W, closed=True)
    for dx in (-9, 0, 9): g.circle(x + dx, y + s*1.2 + 5, 4, fill=W, stroke=INK, sw=1.6)
    g.line(x - s - 8, y + s*1.2 + 10, x + s + 8, y + s*1.2 + 10, INK, 2)


def udl(g, x1, x2, y, n=9, col=RED, lab="w"):
    g.line(x1, y - 34, x2, y - 34, col, 2.4)
    for i in range(n):
        xx = x1 + (x2 - x1)*i/(n - 1)
        g.arrow(xx, y - 34, xx, y - 3, col, 2, 9)
    g.text((x1 + x2)/2, y - 42, lab, 18, col, anchor="middle", weight="bold")


def rot(cx, cy, x, y, a):
    c, s = math.cos(R_(a)), math.sin(R_(a))
    dx, dy = x - cx, y - cy
    return (cx + dx*c + dy*s, cy - dx*s + dy*c)   # 數學方向逆時針（SVG y 向下）


class Ax:
    def __init__(s, g, x0, y0, kx, ky=None, xmin=0, ymin=0):
        s.g, s.x0, s.y0, s.kx, s.ky, s.xmin, s.ymin = g, x0, y0, kx, ky or kx, xmin, ymin
    def X(s, v): return s.x0 + (v - s.xmin)*s.kx
    def Y(s, v): return s.y0 - (v - s.ymin)*s.ky
    def P(s, a, b): return (s.X(a), s.Y(b))
    def seg(s, a, b, c, d, **kw): s.g.line(s.X(a), s.Y(b), s.X(c), s.Y(d), **kw)
    def curve(s, pts, **kw): s.g.poly([s.P(a, b) for a, b in pts], **kw)
    def xt(s, v, lab, color=MUTED, size=14, dy=24, weight="normal"):
        s.g.line(s.X(v), s.y0, s.X(v), s.y0 + 6, INK, 1.4)
        s.g.text(s.X(v), s.y0 + dy, lab, size, color, anchor="middle", weight=weight)
    def yt(s, v, lab, color=MUTED, size=14, weight="normal"):
        s.g.line(s.x0 - 6, s.Y(v), s.x0, s.Y(v), INK, 1.4)
        s.g.text(s.x0 - 10, s.Y(v) + 5, lab, size, color, anchor="end", weight=weight)




def node(g, x, y, r=9, c=ORG): g.circle(x, y, r, fill=c, stroke=W, sw=2.4)


def sawtooth(g, x, y0, y1, amp=10, n=8, col=ORG, sw=3):
    pts = []; h = (y1 - y0)/n
    for i in range(n + 1):
        pts.append((x + (amp if i % 2 else -amp), y0 + i*h))
    g.poly(pts, col, sw)


def dim_h(g, x1, x2, y, lab, col=INK, size=15, up=True):
    g.line(x1, y, x2, y, col, 1.5)
    for x in (x1, x2): g.line(x, y - 7, x, y + 7, col, 1.5)
    g.text((x1 + x2)/2, y - 10 if up else y + 24, lab, size, col, anchor="middle", weight="bold")


def dim_v(g, x, y1, y2, lab, col=INK, size=15, left=True):
    g.line(x, y1, x, y2, col, 1.5)
    for y in (y1, y2): g.line(x - 7, y, x + 7, y, col, 1.5)
    g.text(x - 10 if left else x + 10, (y1 + y2)/2 + 5, lab, size, col, anchor="end" if left else "start", weight="bold")


# ───────── fig01 總覽 ─────────
def fig01():
    g = SVG(1200, 420)
    card(g, 20, 10, 1160, 150, NAVY, NAVY, 14)
    g.text(600, 48, "拼圖二：先認出「力走哪條路」，再決定用哪一套公式", 22, W, anchor="middle", weight="bold")
    chain = [("讀題", PUR, 120), ("認機制：關鍵字・a/d・介面", RED, 330), ("桁架類比 V_n = V_c + V_s", ORG, 310), ("數箍筋 → s", GREEN, 180)]
    x = 45
    for i, (tx, c, w) in enumerate(chain):
        pill(g, x, 78, w, 52, c, tx, 19)
        if i < 3: g.arrow(x + w + 8, 104, x + w + 50, 104, W, 2.6, 12)
        x += w + 60
    items = [
        ("①", "三大傳力機制", ["桁架類比（B 區）", "壓拉桿 STM（D 區）", "剪力摩擦（滑動面）"], PUR, PURBG),
        ("②", "桁架類比", ["上弦 = 混凝土壓力區", "下弦 = 縱向拉力筋", "豎桿 = 箍筋；斜桿 = 混凝土"], BLUE, BLUEBG),
        ("③", "V_c／V_s 分工", ["V_c：開裂瞬間（抗拉）", "V_s：開裂之後（縫裂縫）", "上限 4V_c：斜壓桿（抗壓）"], RED, REDBG),
        ("④", "用「數」的推公式", ["45° 裂縫跨 d → n = d/s", "V_s = A_v f_{yt} d / s", "s_{max}：裂縫不能漏網"], GREEN, GREENBG),
    ]
    for i, (n, hd, lines, c, bg) in enumerate(items):
        X = 20 + i*292
        g.arrow(X + 136, 164, X + 136, 190, INK, 2, 9)
        card(g, X, 194, 280, 214, bg, c, 12, 2)
        g.circle(X + 34, 230, 20, fill=c, stroke=c, sw=1)
        g.text(X + 34, 237, n, 19, W, anchor="middle", weight="bold")
        g.text(X + 64, 238, hd, 19, c, weight="bold")
        for k, tx in enumerate(lines):
            g.text(X + 22, 294 + k*40, tx, 17, INK)
    g.save("figs/fig01_map.svg")


# ───────── fig02 三大機制並列 ─────────
def fig02():
    g = SVG(1200, 440)
    P = [(10, "A 桁架類比（B 區）", PUR, PURBG), (410, "B 壓拉桿 STM（D 區）", BLUE, BLUEBG), (810, "C 剪力摩擦", GOLD, GOLDBG)]
    for x, tt, c, bg in P:
        card(g, x, 10, 380, 420, W, "#D5DAE1", 14)
        g.text(x + 190, 44, tt, 19, c, anchor="middle", weight="bold")
    # A
    x0, y0, w_, h_ = 40, 110, 320, 110
    g.rect(x0, y0, w_, h_, fill=W, stroke=INK, sw=2)
    g.line(x0, y0 + 12, x0 + w_, y0 + 12, BLUE, 5)
    g.line(x0, y0 + h_ - 12, x0 + w_, y0 + h_ - 12, RED, 5)
    st = (w_)/4
    for i in range(5):
        g.line(x0 + i*st, y0 + 12, x0 + i*st, y0 + h_ - 12, RED, 3)
    for i in range(4):
        g.line(x0 + i*st, y0 + h_ - 12, x0 + (i + 1)*st, y0 + 12, BLUE, 3.4)
    g.text(x0 + w_/2, y0 - 14, "上弦＝混凝土壓力區", 14, BLUE, anchor="middle", weight="bold")
    g.text(x0 + w_/2, y0 + h_ + 26, "下弦＝縱筋（拉）｜豎桿＝箍筋｜斜桿＝混凝土", 13, MUTED, anchor="middle")
    pill(g, 60, 270, 280, 46, PUR, "V_n = V_c + V_s", 20)
    g.text(200, 350, "適用：一般梁（a/d 大）", 16, INK, anchor="middle", weight="bold")
    g.text(200, 380, "箍筋把斜裂縫「縫」住", 15, MUTED, anchor="middle")
    g.text(200, 408, "本單元八成考題在這裡", 15, ORG, anchor="middle", weight="bold")
    # B
    x0, y0, w_, h_ = 450, 90, 300, 150
    g.rect(x0, y0, w_, h_, fill=W, stroke=INK, sw=2)
    A = (x0 + w_/2, y0 + 18); L = (x0 + 30, y0 + h_ - 18); R = (x0 + w_ - 30, y0 + h_ - 18)
    for Q in (L, R):
        g.line(A[0], A[1], Q[0], Q[1], "#B9C6EA", 22, cap="round")
        g.line(A[0], A[1], Q[0], Q[1], BLUE, 4)
    g.line(L[0], L[1], R[0], R[1], RED, 5)
    for Q in (A, L, R): node(g, *Q)
    g.arrow(A[0], y0 - 44, A[0], y0 - 4, RED, 3, 12); g.text(A[0] + 10, y0 - 26, "P", 17, RED, weight="bold")
    pin(g, L[0], y0 + h_, 12); roller(g, R[0], y0 + h_, 12)
    g.text(x0 + 70, y0 + 72, "壓桿", 14, BLUE, weight="bold")
    g.text(x0 + w_/2, y0 + h_ - 26, "拉桿", 14, RED, anchor="middle", weight="bold")
    pill(g, 460, 290, 280, 46, BLUE, "驗壓桿・拉桿・節點", 19)
    g.text(600, 370, "適用：深梁、托架、牛腿、接頭", 16, INK, anchor="middle", weight="bold")
    g.text(600, 400, "拱作用直達支承，不靠箍筋縫裂縫", 15, MUTED, anchor="middle")
    # C
    x0, y0 = 850, 90
    g.rect(x0, y0, 140, 170, fill=CONC, stroke=INK, sw=2)
    g.rect(x0 + 160, y0, 140, 170, fill="#E3E7EC", stroke=INK, sw=2)
    sawtooth(g, x0 + 150, y0, y0 + 170, 9, 10, ORG, 3)
    for k in range(3):
        y = y0 + 40 + k*45
        g.line(x0 + 40, y, x0 + 260, y, BLUE, 4); dot(g, x0 + 40, y, BLUE, 5)
    g.arrow(x0 + 70, y0 - 44, x0 + 70, y0 - 4, RED, 3, 12); g.text(x0 + 82, y0 - 26, "V", 17, RED, weight="bold")
    g.arrow(x0 + 230, y0 + 214, x0 + 230, y0 + 174, RED, 3, 12)
    pill(g, 860, 290, 280, 46, GOLD, "V_n = μ A_{vf} f_y", 20)
    g.text(1000, 370, "適用：施工縫、新舊混凝土介面", 16, INK, anchor="middle", weight="bold")
    g.text(1000, 400, "滑動＋張開 → 鋼筋受拉 → 夾緊力", 15, MUTED, anchor="middle")
    g.save("figs/fig02_three.svg")


# ───────── fig03 B 區與 D 區 ─────────
def fig03():
    g = SVG(1200, 440)
    def row(y, a_h, title):
        x0, L, hp = 60, 1080, 90          # hp：梁深（像素）
        g.text(x0, y - 58, title, 17, INK, weight="bold")
        xl, xr = x0 + 20, x0 + L - 20
        xp = xl + a_h*hp
        # 區域：支承、載重兩側各 h
        dz = [(xl - 20, xl + hp), (xp - hp, xp + hp), (xr - hp, xr + 20)]
        g.rect(x0, y, L, hp, fill=PURBG, stroke="none")
        for a, b in dz:
            g.rect(a, y, b - a, hp, fill=ORG, stroke="none", op=0.22)
        g.rect(x0, y, L, hp, fill="none", stroke=INK, sw=2.2)
        # 合併判斷
        if xp - hp <= xl + hp:
            g.rect(xl - 20, y, xp + hp - xl + 20, hp, fill="none", stroke=ORG, sw=2.4, dash="7 4")
            g.text((xl + xp)/2, y + hp/2 + 6, "整段剪跨都是 D 區", 16, ORG, anchor="middle", weight="bold")
        else:
            g.text((xl + hp + xp - hp)/2, y + hp/2 + 6, "B 區（平截面成立）", 16, PUR, anchor="middle", weight="bold")
            for a, b in dz[:2]: g.text((a + b)/2, y + hp/2 + 6, "D", 18, ORG, anchor="middle", weight="bold")
        g.text((xp + hp + xr - hp)/2, y + hp/2 + 6, "B 區", 16, PUR, anchor="middle", weight="bold")
        g.text((dz[2][0] + dz[2][1])/2, y + hp/2 + 6, "D", 18, ORG, anchor="middle", weight="bold")
        pin(g, xl, y + hp, 12); roller(g, xr, y + hp, 12)
        g.arrow(xp, y - 44, xp, y - 4, RED, 3, 12); g.text(xp + 10, y - 26, "P", 17, RED, weight="bold")
        yy = y + hp + 34
        g.line(xl, yy, xp, yy, INK, 1.5)
        for x in (xl, xp): g.line(x, yy - 7, x, yy + 7, INK, 1.5)
        g.text(xp + 12, yy + 5, f"a = {a_h:g}h", 15, INK, weight="bold")
    row(84, 4.0, "載重離支承遠（a = 4h）：兩端 D 區中間夾著 B 區")
    row(306, 1.5, "載重離支承近（a = 1.5h ≤ 2h）：兩個 D 區連在一起 → 深梁行為")
    g.save("figs/fig03_bd.svg")


# ───────── fig04 a/d 數線與剪力谷（示意） ─────────
def fig04():
    g = SVG(1200, 440)
    ax = Ax(g, 110, 350, 140, 230, 0, 0)
    zones = [(0, 1, BLUE, "深梁：拱作用主控"), (1, 2.5, ORG, "短剪跨：拱＋桁架"), (2.5, 6, PUR, "細長梁：桁架類比"), (6, 7.3, GREEN, "很細長：彎矩控制")]
    for a, b, c, tx in zones:
        g.rect(ax.X(a) + 2, 20, ax.X(b) - ax.X(a) - 4, 40, fill=c, stroke="none", rx=8)
        g.text((ax.X(a) + ax.X(b))/2, 47, tx, 15 if b - a < 1.3 else 17, W, anchor="middle", weight="bold")
    # 曲線（示意）
    pts = [(0.4, 1.0), (1, 0.94), (1.5, 0.80), (2, 0.66), (2.5, 0.58), (3, 0.60), (4, 0.70), (5, 0.84), (6, 0.97), (6.5, 1.0), (7.3, 1.0)]
    # 平滑：Catmull-Rom
    sm = []
    for i in range(len(pts) - 1):
        p0 = pts[max(i - 1, 0)]; p1 = pts[i]; p2 = pts[i + 1]; p3 = pts[min(i + 2, len(pts) - 1)]
        for k in range(12):
            u = k/12
            sm.append(tuple(0.5*((2*p1[j]) + (-p0[j] + p2[j])*u + (2*p0[j] - 5*p1[j] + 4*p2[j] - p3[j])*u*u + (-p0[j] + 3*p1[j] - 3*p2[j] + p3[j])*u**3) for j in (0, 1)))
    sm.append(pts[-1])
    ax.seg(0, 1.0, 7.3, 1.0, color=MUTED, sw=1.4, dash="6 5")
    g.text(ax.X(7.3), ax.Y(1.0) - 8, "彎矩強度 M_{fl}", 14, MUTED, anchor="end")
    ax.curve(sm, color=RED, sw=4)
    g.circle(ax.X(2.5), ax.Y(0.58), 8, fill=RED)
    g.text(ax.X(2.5), ax.Y(0.58) + 34, "最弱點 a/d ≈ 2.5（剪力谷）", 15, RED, anchor="middle", weight="bold")
    g.line(ax.x0, ax.y0, ax.X(7.4), ax.y0, INK, 2); g.line(ax.x0, ax.y0, ax.x0, ax.Y(1.12), INK, 2)
    for v in (0, 1, 2, 2.5, 4, 6, 7): ax.xt(v, f"{v:g}", INK, 15)
    g.text(ax.X(7.4) + 8, ax.y0 + 5, "a/d", 17, INK, weight="bold", italic=True)
    g.text(ax.x0 - 12, ax.Y(1.0) + 5, "1.0", 14, MUTED, anchor="end")
    g.text(ax.x0 - 12, ax.Y(0.5) + 5, "0.5", 14, MUTED, anchor="end"); g.line(ax.x0 - 6, ax.Y(0.5), ax.x0, ax.Y(0.5), INK, 1.4)
    g.text(30, 200, "M_u / M_{fl}", 15, INK, weight="bold", rot=-90)
    g.text(ax.X(4.6), ax.Y(0.42), "（Kani 剪力谷：形狀示意，非規範值）", 14, MUTED, anchor="middle")
    g.text(ax.X(0.75), ax.Y(0.80), "拱作用", 15, BLUE, anchor="middle", weight="bold")
    g.text(ax.X(0.75), ax.Y(0.80) + 22, "撐回強度", 15, BLUE, anchor="middle", weight="bold")
    g.text(600, 428, "a = 剪力跨（集中載重到支承面）；均佈載重時以 M_u/(V_u d) 代替", 15, MUTED, anchor="middle")
    g.save("figs/fig04_ad.svg")


# ───────── fig05 認機制三問 ─────────
def fig05():
    g = SVG(1200, 440)
    def diamond(cx, cy, w, h, c, lines):
        g.poly([(cx, cy - h/2), (cx + w/2, cy), (cx, cy + h/2), (cx - w/2, cy)], c, 2.4, fill=W, closed=True)
        for k, tx in enumerate(lines):
            g.text(cx, cy - (len(lines) - 1)*11 + k*22 + 6, tx, 15, c, anchor="middle", weight="bold")
    qs = [(170, BLUE, ["Q1 構件名稱是", "深梁／托架／牛腿／接頭？"]),
          (470, BLUE, ["Q2 集中載重距支承", "≤ 2h 或 l_n ≤ 4h？"]),
          (770, GOLD, ["Q3 有明確滑動面？", "施工縫／新舊介面"])]
    for cx, c, lines in qs:
        diamond(cx, 120, 270, 150, c, lines)
    for a, b in ((305, 335), (605, 635)):
        g.arrow(a, 120, b, 120, INK, 2.4, 11); g.text((a + b)/2, 108, "否", 14, MUTED, anchor="middle", weight="bold")
    g.arrow(905, 120, 960, 120, INK, 2.4, 11); g.text(932, 108, "否", 14, MUTED, anchor="middle", weight="bold")
    card(g, 965, 60, 220, 120, PURBG, PUR, 12, 2)
    g.text(1075, 100, "桁架類比", 19, PUR, anchor="middle", weight="bold")
    g.text(1075, 134, "V_n = V_c + V_s", 17, PUR, anchor="middle", weight="bold")
    g.text(1075, 162, "（B 區，一般梁）", 14, MUTED, anchor="middle")
    res = [(170, BLUE, BLUEBG, "壓拉桿 STM", "不要算 V_c + V_s"),
           (470, BLUE, BLUEBG, "壓拉桿 STM", "拱作用已成形"),
           (770, GOLD, GOLDBG, "剪力摩擦", "V_n = μ A_{vf} f_y")]
    for cx, c, bg, t1, t2 in res:
        g.arrow(cx, 196, cx, 250, INK, 2.4, 11); g.text(cx + 10, 228, "是", 14, c, weight="bold")
        card(g, cx - 120, 254, 240, 96, bg, c, 12, 2)
        g.text(cx, 292, t1, 19, c, anchor="middle", weight="bold")
        g.text(cx, 326, t2, 15, INK, anchor="middle")
    card(g, 20, 372, 1160, 56, REDBG, "#EBB4AE", 10)
    g.text(600, 408, "同一根梁可能同時有 B 區與 D 區：支承與集中載重附近是 D 區，中段是 B 區", 17, RED, anchor="middle", weight="bold")
    g.save("figs/fig05_flow.svg")


# ───────── fig06 桁架類比 ─────────
def fig06():
    g = SVG(1200, 440)
    x0, y0, L, hp = 40, 44, 760, 270
    beam(g, x0, y0, L, hp)
    yt_, yb_ = y0 + 25, y0 + hp - 25        # jd = 220 = 2 格
    xs = [x0 + 50 + i*110 for i in range(7)]
    # 裂縫（與斜壓桿平行）
    for x in xs[:-2]:
        g.line(x + 55, yb_ - 4, x + 55 + 190, yb_ - 194, "#E7A79F", 2, "5 5")
    g.line(x0 + 10, yt_, x0 + L - 10, yt_, BLUE, 9)
    g.line(x0 + 10, yb_, x0 + L - 10, yb_, RED, 7)
    for x in xs: g.line(x, yt_, x, yb_, RED, 4)
    for a, b in zip(xs[:-1], xs[1:]):
        pass
    for x in xs[:-2]:
        g.line(x, yb_, x + (yb_ - yt_), yt_, BLUE, 5)   # 45°：每支斜桿跨 2 格
    for x in xs: dot(g, x, yt_, INK, 5); dot(g, x, yb_, INK, 5)
    pin(g, x0 + 30, y0 + hp, 14)
    g.text(x0 + L/2 + 60, y0 + hp + 80, "箍筋間距 s < jd：一支斜桿跨過好幾支箍筋", 14, MUTED, anchor="middle")
    g.text(x0 + L - 10, y0 - 12, "→ 往跨中（載重側）", 14, MUTED, anchor="end")
    g.arrow(x0 + 30, y0 + hp + 92, x0 + 30, y0 + hp + 40, INK, 3, 12)
    g.text(x0 + 46, y0 + hp + 86, "支承反力 V", 15, INK, weight="bold")
    g.text(x0 + L/2 + 60, y0 + hp + 50, "淡紅虛線 = 斜裂縫，與混凝土斜壓桿同方向", 14, MUTED, anchor="middle")
    X0 = 830
    card(g, X0, 20, 354, 410, W, "#D5DAE1", 12)
    g.text(X0 + 20, 56, "梁 ＝ 一座看不見的桁架", 19, INK, weight="bold")
    rows = [(BLUE, 9, "上弦（壓）", "混凝土壓力區"), (RED, 7, "下弦（拉）", "縱向拉力筋"),
            (RED, 4, "豎桿（拉）", "箍筋 → V_s"), (BLUE, 5, "斜桿（壓）", "裂縫間混凝土")]
    for i, (c, w, a, b) in enumerate(rows):
        y = 100 + i*62
        if i == 2: g.line(X0 + 40, y - 20, X0 + 40, y + 12, c, w)
        elif i == 3: g.line(X0 + 26, y + 10, X0 + 56, y - 20, c, w)
        else: g.line(X0 + 22, y - 5, X0 + 60, y - 5, c, w)
        g.text(X0 + 80, y - 6, a, 17, c, weight="bold")
        g.text(X0 + 80, y + 18, b, 15, INK)
    g.line(X0 + 20, 346, X0 + 334, 346, GRID, 1.4)
    g.text(X0 + 20, 378, "Ritter–Mörsch：斜桿取 45°", 15, MUTED)
    g.text(X0 + 20, 408, "豎桿拉 → 箍筋降伏 = V_s 的來源", 15, GREEN, weight="bold")
    g.save("figs/fig06_truss.svg")


# ───────── fig07 斜壓桿應力 ─────────
def fig07():
    g = SVG(1200, 440)
    # 垂直切面：高度 jd，斜壓桿帶 45°
    cx, yt_, yb_ = 330, 70, 330
    jd = yb_ - yt_
    g.line(cx - 280, yt_, cx + 40, yt_, BLUE, 8); g.line(cx - 280, yb_, cx + 40, yb_, RED, 6)
    # 壓桿帶：與切面相交的全部斜桿
    band = [(cx - jd, yb_), (cx, yb_), (cx, yt_), (cx - jd + 0, yt_)]
    for k in range(0, int(jd) + 1, 26):
        g.line(cx - jd + k - 40, yb_, cx + k - 40 - jd + jd, yt_, "#B9C6EA", 10) if False else None
    for k in range(-int(jd), 1, 26):
        x1 = cx + k; x2 = x1 + jd
        a1 = max(x1, cx - jd); 
        # 只畫在切面左側的部分
        xa, ya = x1, yb_
        xb, yb2 = min(x2, cx), yb_ - (min(x2, cx) - x1)
        if xb > xa: g.line(xa, ya, xb, yb2, BLUE, 3)
    g.line(cx, yt_ - 30, cx, yb_ + 30, INK, 2.4, "8 5")
    g.text(cx, yt_ - 38, "垂直切面", 15, INK, anchor="middle", weight="bold")
    dim_v(g, cx + 70, yt_, yb_, "jd", INK, 17, left=False)
    # 垂直於壓桿的寬度 = jd cos45
    fx, fy = cx - jd/2, yt_ + jd/2
    g.line(cx, yb_, fx, fy, PUR, 4, "7 4")
    dot(g, fx, fy, PUR, 5)
    g.text(cx - jd/2 - 10, yb_ + 34, "紫虛線 ⊥ 壓桿：帶寬 = jd·cos θ", 15, PUR, anchor="middle", weight="bold")
    # 合力 D
    g.arrow(cx - 250, yt_ + 90, cx - 170, yt_ + 10, BLUE, 6, 18)
    g.text(cx - 280, yt_ + 60, "D", 22, BLUE, weight="bold", bg=W)
    # 分量
    ox, oy = 700, 290
    g.arrow(ox, oy, ox + 120, oy - 120, BLUE, 4, 14); g.text(ox + 128, oy - 128, "D", 18, BLUE, weight="bold")
    g.arrow(ox + 120, oy, ox + 120, oy - 116, RED, 3, 12); g.text(ox + 130, oy - 50, "V = D sin θ", 16, RED, weight="bold")
    g.arrow(ox, oy, ox + 116, oy, MUTED, 3, 12); g.text(ox + 60, oy + 26, "N = D cos θ", 15, MUTED, anchor="middle", weight="bold")
    g.arc(ox, oy, 42, 0, 45, INK, 1.6); g.text(ox + 50, oy - 12, "θ", 16, INK, weight="bold")
    g.text(ox + 60, oy + 70, "N 由上、下弦承擔（主筋多受拉）", 14, MUTED, anchor="middle")
    X0 = 930
    card(g, X0, 30, 254, 400, W, "#D5DAE1", 12)
    g.text(X0 + 18, 64, "斜壓桿應力", 18, BLUE, weight="bold")
    g.text(X0 + 18, 98, "f_d = D / (b_w·jd·cos θ)", 15, INK)
    g.text(X0 + 18, 126, "= V / (b_w·jd·sin θ cos θ)", 15, INK)
    g.text(X0 + 18, 160, "θ = 45° → 2V / (b_w·jd)", 16, BLUE, weight="bold")
    g.line(X0 + 18, 180, X0 + 236, 180, GRID, 1.4)
    g.text(X0 + 18, 210, "示範梁 V_{n,max} 時", 15, MUTED)
    g.text(X0 + 18, 240, f"f_d ≈ {FD_MAX:.1f} kgf/cm²", 16, INK, weight="bold")
    g.text(X0 + 18, 268, f"≈ {FD_MAX_R:.2f} f'c", 16, RED, weight="bold")
    g.text(X0 + 18, 306, "看似不大？開裂的混凝土", 15, INK)
    g.text(X0 + 18, 332, "同時被箍筋橫向拉開，", 15, INK)
    g.text(X0 + 18, 358, "抗壓強度明顯「軟化」", 15, INK)
    g.text(X0 + 18, 394, "→ 規範用 V_s ≤ 4V_c 封頂", 15, RED, weight="bold")
    g.save("figs/fig07_strut.svg")


# ───────── fig08 V_c 四來源（比例） ─────────
def fig08():
    g = SVG(1200, 440)
    bx, by, bh = 40, 70, 210
    top_c = 60
    xt, xb = 470, 300                         # 裂縫頂（壓力區下緣）、裂縫底
    k = (bh - top_c)/(xt - xb)
    ycr = lambda x: by + bh - (x - xb)*k      # 裂縫上的 y
    g.poly([(bx, by), (xt, by), (xt, by + top_c), (xb, by + bh), (bx, by + bh)], INK, 2.4, fill=CONC, closed=True)
    g.line(xb, by + bh, xt, by + top_c, RED, 4, cap="round")
    yb = by + bh - 22; xbar = xb + 22/k
    g.line(bx + 5, yb, xbar + 30, yb, INK, 5)
    g.line(130, by + 10, 130, by + bh - 10, "#8FA0B3", 3)
    for xs in (360, 420):
        g.line(xs, by + 10, xs, ycr(xs), GREEN, 3)
        g.arrow(xs, ycr(xs), xs, ycr(xs) - 70, RED, 3, 12)
        g.circle(xs, ycr(xs), 6, fill=RED, stroke=W, sw=2)
    g.text(345, by + 150, "V_s（箍筋）", 16, RED, anchor="end", weight="bold")
    g.arrow(bx + 20, by + bh + 60, bx + 20, by + bh + 4, INK, 3, 13)
    g.text(bx + 34, by + bh + 50, "V（支承反力）", 16, INK, weight="bold")
    g.arrow(xt + 18, by + top_c + 10, xt + 18, by - 6, BLUE, 3.4, 13)
    g.text(xt + 30, by + 30, "① V_{cz}", 17, BLUE, weight="bold")
    mx = 395; my = ycr(mx)
    ux, uy = (xt - xb), -(bh - top_c); L_ = math.hypot(ux, uy); ux, uy = ux/L_, uy/L_
    ox, oy = -14, -14
    g.arrow(mx - 36*ux + ox, my - 36*uy + oy, mx + 40*ux + ox, my + 40*uy + oy, GREEN, 3.4, 13)
    g.text(mx - 50, my - 12, "② V_a", 17, GREEN, anchor="end", weight="bold")
    g.arrow(xbar + 4, yb + 50, xbar + 4, yb + 6, PUR, 3.4, 13)
    g.text(xbar + 16, yb + 48, "③ V_d", 17, PUR, weight="bold")
    g.text(280, 36, "沿斜裂縫切開：裂縫左側自由體", 17, INK, anchor="middle", weight="bold")
    g.text(280, 420, "④ 拱作用：短剪跨時壓力直接斜傳到支承（隨 a/d 變化）", 15, ORG, anchor="middle", weight="bold")
    X0 = 610
    card(g, X0, 20, 574, 410, W, "#D5DAE1", 12)
    g.text(X0 + 20, 56, "無腹筋梁開裂後的剪力分擔（試驗統計）", 17, INK, weight="bold")
    rows = [("① 未裂壓力區", 20, 40, BLUE), ("② 骨材互鎖", 33, 50, GREEN), ("③ 縱筋銷栓", 15, 25, PUR)]
    ax0, axw = X0 + 190, 340
    for i, (lab, a, b, c) in enumerate(rows):
        y = 100 + i*62
        g.text(X0 + 20, y + 20, lab, 17, c, weight="bold")
        g.rect(ax0, y, axw, 28, fill=PANEL, stroke="none", rx=4)
        g.rect(ax0 + axw*a/60, y, axw*(b - a)/60, 28, fill=c, stroke="none", rx=4)
        g.text(ax0 + axw*b/60 + 8, y + 21, f"{a}～{b}%", 15, c, weight="bold")
    for v in (0, 20, 40, 60):
        g.text(ax0 + axw*v/60, 300, f"{v}%", 12, MUTED, anchor="middle")
    g.line(X0 + 20, 318, X0 + 554, 318, GRID, 1.4)
    g.text(X0 + 20, 350, "規範不分項計算：四項打包成 0.53√f'c b_w d", 16, INK, weight="bold")
    g.text(X0 + 20, 382, "塑鉸區反覆載重 → 四項同時失效 → V_c = 0", 16, RED, weight="bold")
    g.text(X0 + 20, 412, "（比例出自 ACI-ASCE 426 對無腹筋梁的整理）", 13, MUTED)
    g.save("figs/fig08_sources.svg")


# ───────── fig09 V_s：數箍筋 ─────────
def fig09():
    g = SVG(1200, 440)
    bx, by, bw_, bh = 40, 30, 700, 300
    beam(g, bx, by, bw_, bh)
    top, bot = by + 22, by + bh - 22
    sp = 75; kpx = sp/S15; dpx = D*kpx
    xs0 = bx + 60
    stir = [xs0 + i*sp for i in range(9)]
    x_crack0 = xs0 + 110; x_crack1 = x_crack0 + dpx
    crossing = [x for x in stir if x_crack0 < x < x_crack1]
    for x in stir:
        g.line(x, top, x, bot, GREEN if x in crossing else "#8FA0B3", 4 if x in crossing else 2.4)
    g.line(bx + 10, bot + 4, bx + bw_ - 10, bot + 4, INK, 6)
    g.line(x_crack0, bot + 10, x_crack1, bot + 10 - dpx, RED, 4, cap="round")
    for x in crossing:
        yc = bot + 10 - (x - x_crack0)
        g.arrow(x, yc + 36, x, yc - 30, GREEN, 3, 12)
        dot(g, x, yc, RED, 6)
    g.line(x_crack0, bot + 44, x_crack1, bot + 44, INK, 1.6)
    for x in (x_crack0, x_crack1): g.line(x, bot + 36, x, bot + 52, INK, 1.6)
    g.text((x_crack0 + x_crack1)/2, bot + 74, "水平投影 = d = 50 cm（45° 裂縫）", 16, RED, anchor="middle", weight="bold")
    g.line(stir[6], top - 14, stir[7], top - 14, INK, 1.6)
    for x in (stir[6], stir[7]): g.line(x, top - 22, x, top - 6, INK, 1.6)
    g.text((stir[6] + stir[7])/2, top - 22, "s = 15", 15, INK, anchor="middle", weight="bold")
    X0 = 770
    card(g, X0, 30, 414, 250, W, "#D5DAE1", 12)
    g.text(X0 + 20, 64, "三步數出 V_s", 19, GREEN, weight="bold")
    g.text(X0 + 20, 102, "① 裂縫跨過的箍筋支數 n = d / s", 16, INK)
    g.text(X0 + 20, 134, "② 每支降伏提供 A_v f_{yt}", 16, INK)
    g.text(X0 + 20, 172, "③ V_s = n · A_v f_{yt} = A_v f_{yt} d / s", 17, GREEN, weight="bold")
    g.line(X0 + 20, 192, X0 + 394, 192, GRID, 1.4)
    g.text(X0 + 20, 222, f"示範梁：D13 雙肢 A_v = {AV:.3f} cm²", 15, MUTED)
    g.text(X0 + 20, 252, f"n = {D:.0f}/{S15:.0f} = {N_ST:.2f} 支 → V_s = {VS15:.2f} tf", 16, INK, weight="bold")
    card(g, X0, 294, 414, 136, GOLDBG, "#E6CFA0", 12)
    g.text(X0 + 20, 328, "兩個隱藏假設", 17, GOLD, weight="bold")
    g.text(X0 + 20, 360, "裂縫角取 45°（水平投影 = d）", 15, INK)
    g.text(X0 + 20, 390, "穿過裂縫的箍筋全部降伏", 15, INK)
    g.text(X0 + 20, 418, "n 可以不是整數：這是「平均」的支數", 13, MUTED)
    g.save("figs/fig09_vs.svg")


# ───────── fig10 A_v：數肢數 ─────────
def fig10():
    g = SVG(1200, 440)
    def sec(x0, title, legs, sub):
        w_, h_ = 190, 260; y0 = 70
        g.text(x0 + w_/2, 40, title, 18, INK, anchor="middle", weight="bold")
        hatch(g, x0, y0, w_, h_); g.rect(x0, y0, w_, h_, fill="none", stroke=INK, sw=2.2)
        c = 22
        g.rect(x0 + c, y0 + c, w_ - 2*c, h_ - 2*c, fill="none", stroke=BLUE, sw=4, rx=8)
        xs = [x0 + c + 16 + k*(w_ - 2*c - 32)/3 for k in range(4)]
        if legs == 3:
            g.line(x0 + w_/2, y0 + c, x0 + w_/2, y0 + h_ - c, BLUE, 4)
        if legs == 4:
            g.rect(x0 + c + 38, y0 + c, w_ - 2*c - 76, h_ - 2*c, fill="none", stroke=BLUE, sw=4, rx=6)
        for x in xs:
            dot(g, x, y0 + c + 14, INK, 7); dot(g, x, y0 + h_ - c - 14, INK, 7)
        # 水平切線（裂縫面）
        yc = y0 + h_/2
        g.line(x0 - 30, yc, x0 + w_ + 30, yc, RED, 2.4, "8 5")
        cx = [x0 + c, x0 + w_ - c]
        if legs == 3: cx.append(x0 + w_/2)
        if legs == 4: cx += [x0 + c + 38, x0 + w_ - c - 38]
        for x in cx: g.circle(x, yc, 7, fill=RED, stroke=W, sw=2)
        g.text(x0 + w_/2, y0 + h_ + 36, sub, 17, RED, anchor="middle", weight="bold")
        g.text(x0 + w_/2, y0 + h_ + 62, f"D13：A_v = {legs*AB['D13']:.3f} cm²", 15, INK, anchor="middle")
    sec(30, "閉合箍", 2, "切到 2 肢")
    sec(270, "箍＋繫筋", 3, "切到 3 肢")
    sec(510, "外箍＋內箍", 4, "切到 4 肢")
    X0 = 760
    card(g, X0, 30, 424, 250, W, "#D5DAE1", 12)
    g.text(X0 + 20, 66, "A_v ＝ 肢數 × 單肢面積", 19, BLUE, weight="bold")
    g.text(X0 + 20, 96, "數「一組」箍筋被裂縫切到幾根腿", 15, MUTED)
    for i, (k, v) in enumerate(AB.items()):
        y = 136 + i*34
        g.text(X0 + 40, y, k, 17, INK, weight="bold")
        g.text(X0 + 130, y, f"{v:.3f} cm²", 17, INK)
        g.text(X0 + 270, y, f"雙肢 {2*v:.3f}", 15, MUTED)
    card(g, X0, 294, 424, 136, REDBG, "#EBB4AE", 12)
    g.text(X0 + 20, 328, "紅虛線 = 裂縫面（水平切過梁腹）", 16, RED, weight="bold")
    g.text(X0 + 20, 360, "被切到的每一根垂直腿都在「縫」裂縫", 15, INK)
    g.text(X0 + 20, 390, "繫筋只勾一側也算一肢（須勾住縱筋）", 15, INK)
    g.text(X0 + 20, 418, "常見錯誤：雙肢箍只算 1 根的面積", 14, MUTED)
    g.save("figs/fig10_av.svg")


# ───────── fig11 s_max：不讓裂縫漏網 ─────────
def fig11():
    g = SVG(1200, 440)
    d = 200
    def panel(x0, s_frac, title, c, crack, sub):
        w_ = 370; y0 = 70; top = y0 + 10; bot = y0 + 10 + d
        g.text(x0 + w_/2, 42, title, 18, c, anchor="middle", weight="bold")
        g.rect(x0, y0 - 6, w_, d + 36, fill=CONC, stroke=INK, sw=2)
        g.line(x0 + 4, bot, x0 + w_ - 4, bot, INK, 5)
        g.line(x0 + 4, top + d/2, x0 + w_ - 4, top + d/2, MUTED, 1.2, "4 4")
        sp = s_frac*d
        xs = []; x = x0 + 26
        while x < x0 + w_ - 10: xs.append(x); x += sp
        cx0, cy0, cx1, cy1 = crack
        hit = [x for x in xs if min(cx0, cx1) < x < max(cx0, cx1)]
        for x in xs: g.line(x, top, x, bot, GREEN if x in hit else "#8FA0B3", 4 if x in hit else 2.6)
        g.line(x0 + cx0, top + cy0, x0 + cx1, top + cy1, RED, 4, cap="round") if False else None
        return xs, x0, top
    # ① s > d：整條 45° 裂縫（水平投影 d）落在兩支箍筋之間
    xs, x0, top = panel(20, 1.6, "s = 1.6d：裂縫整條漏網", RED, (0, 0, 0, 0), "")
    ca = xs[0] + 60; g.line(ca, top + d, ca + d, top, RED, 4, cap="round")
    pill(g, 20 + 90, 330, 190, 40, RED, "跨過 0 支 ×", 17)
    # ② s = d/2：中深度以下的裂縫段（投影 d/2）至少碰到 1 支
    xs, x0, top = panel(415, 0.5, "s = d/2：至少 1 支", GREEN, (0, 0, 0, 0), "")
    ca = xs[1] + 12
    g.line(ca, top + d, ca + d, top, "#E7A79F", 3, "6 5")
    g.line(ca, top + d, ca + d/2, top + d/2, RED, 5, cap="round")
    for x in xs:
        if ca < x < ca + d/2: g.circle(x, top + d - (x - ca), 7, fill=RED, stroke=W, sw=2)
    pill(g, 415 + 90, 330, 190, 40, GREEN, "跨過 ≥ 1 支 ✓", 17)
    # ③ s = d/4
    xs, x0, top = panel(810, 0.25, "s = d/4：至少 2 支", BLUE, (0, 0, 0, 0), "")
    ca = xs[2] + 8
    g.line(ca, top + d, ca + d, top, "#E7A79F", 3, "6 5")
    g.line(ca, top + d, ca + d/2, top + d/2, RED, 5, cap="round")
    for x in xs:
        if ca < x < ca + d/2: g.circle(x, top + d - (x - ca), 7, fill=RED, stroke=W, sw=2)
    pill(g, 810 + 90, 330, 190, 40, BLUE, "跨過 ≥ 2 支 ✓", 17)
    g.text(600, 398, "深紅實線 = 從中深度（d/2）延伸到拉力筋的裂縫段，水平投影 d/2；箍筋要在裂縫兩側都有錨定長度才有效", 15, INK, anchor="middle")
    g.text(600, 426, "s ≤ d/2 保證這一段必碰到 1 支；V_s > 2V_c（高剪力、裂縫多）時再砍半成 d/4 → 至少 2 支", 15, RED, anchor="middle", weight="bold")
    g.save("figs/fig11_smax.svg")


# ───────── fig12 天花板：V_n vs A_v/s ─────────
def fig12():
    g = SVG(1200, 440)
    ax = Ax(g, 100, 390, 1800, 4.3, 0, 0)       # x: A_v/s (cm²/cm)，y: tf
    xm = 0.36
    # 區域
    g.rect(ax.X(0), ax.Y(80), ax.X(X_2VC) - ax.X(0), ax.Y(0) - ax.Y(80), fill=GREENBG, stroke="none")
    g.rect(ax.X(X_2VC), ax.Y(80), ax.X(X_CAP) - ax.X(X_2VC), ax.Y(0) - ax.Y(80), fill=GOLDBG, stroke="none")
    g.rect(ax.X(X_CAP), ax.Y(80), ax.X(xm) - ax.X(X_CAP), ax.Y(0) - ax.Y(80), fill=REDBG, stroke="none")
    g.text((ax.X(0) + ax.X(X_2VC))/2, ax.Y(73), "s ≤ d/2", 16, GREEN, anchor="middle", weight="bold")
    g.text((ax.X(X_2VC) + ax.X(X_CAP))/2, ax.Y(73), "s ≤ d/4", 16, GOLD, anchor="middle", weight="bold")
    g.text((ax.X(X_CAP) + ax.X(xm))/2, ax.Y(73), "斜壓桿壓碎區", 16, RED, anchor="middle", weight="bold")
    # 曲線
    ax.seg(0, VC0, X_CAP, VN_MAX, color=PUR, sw=4.5)
    ax.seg(X_CAP, VN_MAX, xm, VN_MAX, color=RED, sw=4.5)
    ax.seg(X_CAP, VN_MAX, xm, VC0 + K_VS*xm, color=MUTED, sw=2, dash="7 5")
    g.text(ax.X(xm) - 4, ax.Y(VC0 + K_VS*xm) + 22, "公式照算（無效）", 14, MUTED, anchor="end")
    ax.seg(0, VC0, xm, VC0, color=GREEN, sw=1.6, dash="5 4")
    g.text(ax.X(xm) - 4, ax.Y(VC0) - 8, f"V_c = {VC0:.2f}", 14, GREEN, anchor="end", weight="bold")
    g.line(ax.x0, ax.y0, ax.X(xm), ax.y0, INK, 2); g.line(ax.x0, ax.y0, ax.x0, ax.Y(80), INK, 2)
    for v in (0, 20, 40, 60, 80): ax.yt(v, f"{v}")
    for v in (0, 0.1, 0.2, 0.3): ax.xt(v, f"{v:g}")
    g.text(ax.X(xm) + 6, ax.y0 + 5, "A_v/s", 15, INK, weight="bold")
    g.text(ax.x0 + 8, ax.Y(80) - 8, "V_n（tf）", 15, INK, weight="bold")
    for s_ in (25.0, 15.0, 12.5):
        x = AV/s_; v = VC0 + K_VS*x
        g.circle(ax.X(x), ax.Y(v), 7, fill=PUR)
        g.text(ax.X(x) + 10, ax.Y(v) + 20, f"s = {s_:g}：{v:.2f}", 14, PUR, weight="bold")
    g.circle(ax.X(X_CAP), ax.Y(VN_MAX), 8, fill=RED)
    g.text(ax.X(X_CAP) + 10, ax.Y(VN_MAX) + 26, f"V_{{n,max}} = 5V_c", 15, RED, weight="bold")
    g.text(ax.X(X_CAP) + 10, ax.Y(VN_MAX) + 48, f"= {VN_MAX:.2f} tf", 15, RED, weight="bold")
    X0 = 800
    card(g, X0, 20, 384, 410, W, "#D5DAE1", 12)
    g.text(X0 + 20, 56, "示範梁（D13 雙肢）", 18, INK, weight="bold")
    g.text(X0 + 20, 90, f"V_s = (A_v/s)·f_{{yt}} d = {K_VS:.0f}·(A_v/s) tf", 15, INK)
    g.text(X0 + 20, 124, f"V_s = 2V_c = {VS2:.2f} → s ≈ {S_2VC:.0f} cm", 15, GOLD, weight="bold")
    g.text(X0 + 20, 154, f"V_s = 4V_c = {VS_MAX:.2f} → s ≈ {S_CAP:.0f} cm", 15, RED, weight="bold")
    g.line(X0 + 20, 176, X0 + 364, 176, GRID, 1.4)
    g.text(X0 + 20, 208, "紫線：箍筋越密 V_n 線性上升", 15, PUR, weight="bold")
    g.text(X0 + 20, 238, "紅線：到了天花板就平了", 15, RED, weight="bold")
    g.text(X0 + 20, 272, "再加箍筋只是浪費鋼筋，", 15, INK)
    g.text(X0 + 20, 300, "破壞改由混凝土斜壓桿壓碎", 15, INK)
    g.text(X0 + 20, 328, "控制 → 脆性、無預警", 15, INK)
    card(g, X0 + 16, 350, 352, 64, REDBG, "#EBB4AE", 10)
    g.text(X0 + 192, 390, "V_s > 4V_c ⇒ 加大斷面", 18, RED, anchor="middle", weight="bold")
    g.save("figs/fig12_ceiling.svg")


# ───────── fig13 STM 示範深梁 ─────────
def fig13():
    g = SVG(1200, 440)
    k = 2.6                                   # px/cm
    x0, y0 = 70, 90
    over = 25
    Lb = 2*SA_ + 2*over
    g.rect(x0, y0, Lb*k, SH*k, fill=CONC, stroke=INK, sw=2.4)
    xl, xr = x0 + over*k, x0 + (over + 2*SA_)*k
    xm = (xl + xr)/2
    yt_n, yb_n = y0 + 10*k, y0 + (SH - 10)*k
    for Q in ((xl, yb_n), (xr, yb_n)):
        g.line(xm, yt_n, Q[0], Q[1], "#B9C6EA", SW_REQ*k, cap="butt")
    for Q in ((xl, yb_n), (xr, yb_n)):
        g.line(xm, yt_n, Q[0], Q[1], BLUE, 4.5)
    g.line(xl - 10, yb_n, xr + 10, yb_n, RED, 6)
    for Q in ((xm, yt_n), (xl, yb_n), (xr, yb_n)): node(g, *Q, 11)
    pin(g, xl, y0 + SH*k, 14); roller(g, xr, y0 + SH*k, 14)
    g.arrow(xm, y0 - 60, xm, y0 - 4, RED, 3.4, 14)
    g.text(xm + 12, y0 - 34, f"P = {SP:.0f} tf", 17, RED, weight="bold")
    g.arc(xl, yb_n, 60, 0, STH, INK, 1.8)
    g.text(xl + 66, yb_n - 18, f"θ = {STH:.1f}°", 15, INK, weight="bold", bg=W)
    g.text((xl + xm)/2 - 56, (yt_n + yb_n)/2 - 4, f"C = {SC:.1f}", 16, BLUE, anchor="end", weight="bold", bg=W)
    g.text(xm, yb_n - 14, f"T = {ST:.1f} tf", 16, RED, anchor="middle", weight="bold", bg=W)
    g.arrow(xl, y0 + SH*k + 80, xl, y0 + SH*k + 36, INK, 3, 12)
    g.text(xl + 12, y0 + SH*k + 72, f"R = {SR:.0f} tf", 15, INK, weight="bold")
    dim_v(g, x0 + Lb*k + 30, yt_n, yb_n, f"z = {SZ:.0f}", INK, 15, left=False)
    yd = y0 - 20
    g.line(xl, yd, xm, yd, INK, 1.4); g.text((xl + xm)/2, yd - 8, f"a = {SA_:.0f} cm", 14, INK, anchor="middle", weight="bold")
    for x in (xl, xm): g.line(x, yd - 6, x, yd + 6, INK, 1.4)
    g.text(xm, y0 + SH*k + 44, f"b_w = {SB:.0f}、h = {SH:.0f}、d ≈ {SD_:.0f} cm", 15, MUTED, anchor="middle")
    X0 = 760
    card(g, X0, 20, 424, 410, W, "#D5DAE1", 12)
    g.text(X0 + 20, 56, f"a/d = {SA_:.0f}/{SD_:.0f} = {S_AD:.1f} → D 區，用 STM", 17, BLUE, weight="bold")
    items = [("① 幾何", f"tan θ = {SZ:.0f}/{SA_:.0f} → θ = {STH:.1f}° ≥ 25° ✓", INK),
             ("② 節點平衡", f"C = R/sin θ = {SC:.1f} tf；T = R/tan θ = {ST:.1f} tf", INK),
             ("③ 拉桿", f"A_s = T/(φ f_y) = {SAS:.1f} cm² → 8-D25（{SAS_USE:.1f}）", RED),
             ("④ 壓桿（瓶形 β_s = 0.75）", f"f_{{ce}} = {FCE_S:.1f} → 需寬 {SW_REQ:.1f} cm", BLUE),
             ("⑤ 支承節點（CCT β_n = 0.80）", f"f_{{ce}} = {FCE_N:.1f} → 支承板長 ≥ {LB_REQ:.1f} cm", ORG)]
    for i, (h1, h2, c) in enumerate(items):
        y = 100 + i*64
        g.text(X0 + 20, y, h1, 16, c, weight="bold")
        g.text(X0 + 20, y + 26, h2, 15, INK)
    g.text(X0 + 20, 418, "淺藍色帶 = 壓桿寬；橘點 = 節點", 13, MUTED)
    g.save("figs/fig13_stm.svg")


# ───────── fig14 剪力摩擦 ─────────
def fig14():
    g = SVG(1200, 440)
    def step(x0, title, opened, stretched, clamp):
        g.text(x0 + 120, 36, title, 17, INK, anchor="middle", weight="bold")
        gap = 12 if opened else 0
        g.rect(x0, 60, 100, 220, fill=CONC, stroke=INK, sw=2)
        # 右塊的鋸齒邊
        n = 8; hh = 220/n
        pts = [(x0 + 100 + (8 if i % 2 else -8), 60 + i*hh) for i in range(n + 1)]
        dy = 14 if opened else 0
        R = [(x + gap + 20, y + dy) for x, y in pts]
        g.poly([(x0 + 100 + 8 + gap + 20 + 100, 60 + dy)] + [(x0 + 100 + gap + 20, 60 + dy)] + R + [(x0 + 100 + gap + 20 + 108, 280 + dy)], INK, 2, fill="#E3E7EC", closed=True)
        L = [(x + 20 - 20, y) for x, y in pts]
        g.poly(L, ORG, 3)
        for k in range(3):
            y = 110 + k*60
            c = RED if stretched else BLUE
            g.line(x0 + 30, y, x0 + 210 + gap, y, c, 4 if not stretched else 5)
            dot(g, x0 + 30, y, c, 5)
        if clamp:
            g.arrow(x0 - 30, 170, x0 - 2, 170, RED, 3, 12); g.arrow(x0 + 260 + gap, 170, x0 + 232 + gap, 170, RED, 3, 12)
    step(30, "① 介面受剪 V", False, False, False)
    g.arrow(90, 330, 90, 290, INK, 3, 12); g.arrow(210, 296, 210, 336, INK, 3, 12)
    g.text(150, 372, "兩塊想沿介面滑動", 15, INK, anchor="middle")
    g.arrow(300, 170, 340, 170, INK, 2.6, 12)
    step(370, "② 鋸齒爬坡 → 張開 w", True, True, False)
    g.text(490, 332, "張開量把鋼筋拉長（dilatancy）", 15, INK, anchor="middle")
    g.text(490, 358, "鋼筋受拉 → 反作用 = 夾緊力", 15, RED, anchor="middle", weight="bold")
    g.arrow(650, 170, 690, 170, INK, 2.6, 12)
    g.text(760, 130, "N = A_{vf} f_y", 18, RED, anchor="middle", weight="bold")
    g.text(760, 170, "×  μ", 20, INK, anchor="middle", weight="bold")
    g.text(760, 214, "V_n = μ A_{vf} f_y", 18, GOLD, anchor="middle", weight="bold")
    g.text(760, 250, "（摩擦力）", 15, MUTED, anchor="middle")
    X0 = 850
    card(g, X0, 20, 334, 410, W, "#D5DAE1", 12)
    g.text(X0 + 20, 56, "摩擦係數 μ（常重混凝土 λ = 1）", 16, INK, weight="bold")
    rows = [("一體澆置", "1.4", GREEN), ("刻意打毛（約 6 mm）", "1.0", BLUE), ("未刻意打毛", "0.6", RED), ("混凝土 vs 軋製鋼材", "0.7", MUTED)]
    for i, (a, b, c) in enumerate(rows):
        y = 100 + i*44
        g.text(X0 + 20, y, a, 16, INK); g.text(X0 + 300, y, b, 18, c, anchor="end", weight="bold")
    g.line(X0 + 20, 282, X0 + 314, 282, GRID, 1.4)
    g.text(X0 + 20, 312, "鋼筋須垂直介面、兩側都錨定", 15, INK)
    g.text(X0 + 20, 340, "才能真的產生夾緊力", 15, INK)
    g.text(X0 + 20, 374, "永久淨壓力可加入夾緊力；", 15, MUTED)
    g.text(X0 + 20, 400, "淨拉力要另配鋼筋抵銷", 15, MUTED)
    g.save("figs/fig14_friction.svg")


# ───────── fig15 考場四步流程（示範梁 V_u = 40 tf） ─────────
def fig15():
    g = SVG(1200, 440)
    def box(x, y, w, h, c, bg, t1, t2, t3=None):
        card(g, x, y, w, h, bg, c, 12, 2)
        g.text(x + w/2, y + 32, t1, 17, c, anchor="middle", weight="bold")
        g.text(x + w/2, y + 64, t2, 16, INK, anchor="middle", weight="bold")
        if t3: g.text(x + w/2, y + 92, t3, 14, MUTED, anchor="middle")
    Y = 40; H_ = 110; W_ = 262; G_ = 30
    xs = [20 + i*(W_ + G_) for i in range(4)]
    box(xs[0], Y, W_, H_, GREEN, GREENBG, "① 認機制", "一般梁 → V_c + V_s", f"φ = 0.75，V_c = {VC0:.2f} tf")
    box(xs[1], Y, W_, H_, PUR, PURBG, "② 反算 V_{s,req}", f"40/0.75 − {VC0:.2f} = {VS_REQ:.2f}", "V_{s,req} = V_u/φ − V_c")
    box(xs[2], Y, W_, H_, RED, REDBG, "③ 檢查天花板", f"{VS_REQ:.2f} ≤ 4V_c = {VS_MAX:.2f} ✓", "超過 → 加大斷面")
    box(xs[3], Y, W_, H_, GOLD, GOLDBG, "④ 定間距", f"s ≤ {S_REQ:.1f}（強度）", f"V_s > 2V_c = {VS2:.2f} → s ≤ d/4")
    for i in range(3):
        g.arrow(xs[i] + W_ + 4, Y + H_/2, xs[i + 1] - 4, Y + H_/2, INK, 2.4, 11)
    # 下排：分支
    g.arrow(xs[2] + W_/2, Y + H_ + 4, xs[2] + W_/2, 214, RED, 2.2, 10)
    card(g, xs[2] + 10, 218, W_ - 20, 56, W, RED, 10, 2)
    g.text(xs[2] + W_/2, 252, "若 V_s > 4V_c：斜壓桿壓碎", 15, RED, anchor="middle", weight="bold")
    g.arrow(xs[3] + W_/2, Y + H_ + 4, xs[3] + W_/2, 214, GOLD, 2.2, 10)
    card(g, xs[3] + 10, 218, W_ - 20, 56, W, GOLD, 10, 2)
    g.text(xs[3] + W_/2, 252, f"取 s = min({S_REQ:.1f}, {S_MAX:.1f}) = {S_USE:.1f}", 15, GOLD, anchor="middle", weight="bold")
    card(g, 20, 300, 1160, 128, NAVY, NAVY, 14)
    g.text(600, 342, f"驗算：V_s = 2.534 × 4200 × 50 / {S_USE:.1f} = {VS_USE:.2f} tf", 19, W, anchor="middle", weight="bold")
    g.text(600, 380, f"φV_n = 0.75 × ({VC0:.2f} + {VS_USE:.2f}) = {PVN:.2f} tf ≥ V_u = 40 tf ✓", 19, "#7FC8B4", anchor="middle", weight="bold")
    g.text(600, 412, "示範梁：b_w 30、d 50 cm，f′c 280、f_{yt} 4200 kgf/cm²，D13 雙肢箍", 14, "#9FB3C8", anchor="middle")
    g.save("figs/fig15_steps.svg")


# ───────── fig16 V_u 數線：五個區段 ─────────
def fig16():
    g = SVG(1200, 400)
    ax = Ax(g, 60, 190, 1080/60, 1, 0, 0)
    bps = [0, PVC/2, PVC, PHI*(VC0 + VS2), PVN_MAX, 60]
    labs = [("不需箍筋", MUTED), ("最少箍筋", GREEN), ("s ≤ d/2", BLUE), ("s ≤ d/4", GOLD), ("加大斷面", RED)]
    for (a, b), (tx, c) in zip(zip(bps[:-1], bps[1:]), labs):
        g.rect(ax.X(a) + 1, 120, ax.X(b) - ax.X(a) - 2, 50, fill=c, stroke="none", rx=6, op=0.9)
        if b - a > 6: g.text((ax.X(a) + ax.X(b))/2, 152, tx, 17, W, anchor="middle", weight="bold")
    g.text((ax.X(0) + ax.X(PVC/2))/2, 104, "不需", 14, MUTED, anchor="middle", weight="bold")
    g.text((ax.X(PVC/2) + ax.X(PVC))/2, 104, "最少", 14, GREEN, anchor="middle", weight="bold")
    g.line(ax.x0, ax.y0, ax.X(60), ax.y0, INK, 2)
    names = ["0", "φV_c/2", "φV_c", "φ(3V_c)", "φ(5V_c)"]
    for v, n in zip(bps[:-1], names):
        g.line(ax.X(v), ax.y0 - 6, ax.X(v), ax.y0 + 6, INK, 1.6)
        g.text(ax.X(v), ax.y0 + 28, n, 15, INK, anchor="middle", weight="bold")
        g.text(ax.X(v), ax.y0 + 50, f"{v:.2f}", 14, MUTED, anchor="middle")
    g.text(ax.X(60), ax.y0 + 28, "V_u（tf）", 15, INK, anchor="end", weight="bold")
    g.arrow(ax.X(VU), 40, ax.X(VU), 116, NAVY, 3, 12)
    g.text(ax.X(VU), 32, "示範 V_u = 40", 16, NAVY, anchor="middle", weight="bold")
    card(g, 20, 270, 1160, 118, PANEL, "#D5DAE1", 12)
    g.text(40, 306, "分界點全部由 V_c 的倍數組成：", 17, INK, weight="bold")
    g.text(40, 340, "V_s = 2V_c ⇔ V_u = φ(V_c + 2V_c) = φ·3V_c（間距減半）；V_s = 4V_c ⇔ V_u = φ·5V_c（天花板）", 16, INK)
    g.text(40, 372, "最少箍筋的細節（A_{v,min}）屬於拼圖三「一般梁四道關卡」", 15, MUTED)
    g.save("figs/fig16_zones.svg")


if __name__ == "__main__":
    for f in [f"fig{i:02d}" for i in range(1, 17)]:
        globals()[f]()
    print("figs done")
