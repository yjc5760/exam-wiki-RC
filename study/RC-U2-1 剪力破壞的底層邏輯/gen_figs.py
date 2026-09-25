"""RC-U2-1 拼圖一：剪力破壞的底層邏輯 — 向量圖（所有數值由 params.py 算出）"""
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


# ───────── fig01 總覽：一句話 → 四個推論 ─────────
def fig01():
    g = SVG(1200, 400)
    card(g, 20, 10, 1160, 150, NAVY, NAVY, 14)
    g.text(600, 48, "底層邏輯：混凝土沒有「抗剪強度」這回事", 22, W, anchor="middle", weight="bold")
    chain = [("剪應力 τ", PUR), ("45° 方向主拉 σ_1 = τ", RED), ("σ_1 > f_t", ORG), ("斜向拉裂", GREEN)]
    x = 70; ws = [190, 300, 170, 170]
    for (t, c), w in zip(chain, ws):
        pill(g, x, 78, w, 52, c, t, 19)
        x2 = x + w
        if t != "斜向拉裂": g.arrow(x2 + 8, 104, x2 + 62, 104, W, 2.6, 12)
        x = x2 + 72
    g.text(600, 150, "", 1)
    items = [
        ("①", "為什麼開根號", ["f_t 正比於 √f'c", "→ V_c = 0.53√f'c b_w d", "加斷面比加強度有效"], PUR, PURBG),
        ("②", "軸拉為何 4 倍狠", ["拉力把主拉應力推高", "修正分母 35 vs 140", "N_u = −35A_g 時 V_c = 0"], BLUE, BLUEBG),
        ("③", "塑鉸區 V_c = 0", ["反覆載重裂縫貫穿", "V_c 的來源全數失效", "（須同時符合兩條件）"], RED, REDBG),
        ("④", "V_c／V_s 分工與上限", ["V_c：開裂瞬間抗拉", "V_s：裂後數箍筋", "上限：斜壓桿別壓碎"], GREEN, GREENBG),
    ]
    for i, (n, hd, lines, c, bg) in enumerate(items):
        X = 20 + i*292
        g.arrow(X + 136, 162, X + 136, 188, INK, 2, 9)
        card(g, X, 192, 280, 200, bg, c, 12, 2)
        g.circle(X + 34, 228, 20, fill=c, stroke=c, sw=1)
        g.text(X + 34, 235, n, 19, W, anchor="middle", weight="bold")
        g.text(X + 64, 236, hd, 19, c, weight="bold")
        for k, t in enumerate(lines):
            g.text(X + 22, 292 + k*42, t, 17, INK if k else c, weight="bold" if k == 0 else "normal")
    g.save("figs/fig01_map.svg")


# ───────── fig02 梁 → 微元素 → 旋轉 45° ─────────
def fig02():
    g = SVG(1200, 440)
    # 梁
    bx, by, bw_, bh = 30, 150, 330, 90
    udl(g, bx, bx + bw_, by)
    beam(g, bx, by, bw_, bh)
    pin(g, bx + 18, by + bh); roller(g, bx + bw_ - 18, by + bh)
    cx = bx + 95
    g.line(bx, by + bh/2, bx + bw_, by + bh/2, ORG, 1.6, "7 5")
    g.rect(cx - 12, by + bh/2 - 12, 24, 24, fill=PURBG, stroke=PUR, sw=2.2)
    g.text(cx, by + bh + 72, "近支承、中性軸處取微元素", 16, PUR, anchor="middle", weight="bold")
    g.text(bx + bw_ - 6, by + bh/2 - 8, "中性軸", 14, ORG, anchor="end", weight="bold")
    g.text(bx + bw_/2, by + bh + 110, "該處 σ_x = σ_y = 0（彎曲應力為零）", 15, MUTED, anchor="middle")
    g.arrow(cx + 14, by + bh/2, 470, 210, MUTED, 1.6, 10, dash="5 4")
    # 純剪元素
    ex, ey, s = 540, 210, 110
    g.rect(ex - s/2, ey - s/2, s, s, fill=W, stroke=INK, sw=2.6, rx=3)
    g.text(ex, ey + 9, "τ", 28, PUR, anchor="middle", weight="bold")
    o = 16
    g.arrow(ex - 40, ey - s/2 - o, ex + 44, ey - s/2 - o, PUR, 3, 12)
    g.arrow(ex + 40, ey + s/2 + o, ex - 44, ey + s/2 + o, PUR, 3, 12)
    g.arrow(ex + s/2 + o, ey + 40, ex + s/2 + o, ey - 44, PUR, 3, 12)
    g.arrow(ex - s/2 - o, ey - 40, ex - s/2 - o, ey + 44, PUR, 3, 12)
    g.text(ex, 330, "純剪狀態", 19, PUR, anchor="middle", weight="bold")
    g.text(ex, 356, "只有剪應力 τ", 15, MUTED, anchor="middle")
    g.arrow(640, 210, 720, 210, INK, 2.6, 13)
    g.text(680, 196, "轉 45°", 16, INK, anchor="middle", weight="bold")
    # 旋轉 45° 元素
    rx, ry, a = 880, 210, 55
    pts = [rot(rx, ry, rx + dx, ry + dy, 45) for dx, dy in [(-a, -a), (a, -a), (a, a), (-a, a)]]
    g.poly(pts, INK, 2.6, fill=W, closed=True)
    # σ1 方向：與水平夾 45°（右上／左下）拉；σ3 左上／右下 壓
    L = a*1.414
    u1 = (math.cos(R_(45)), -math.sin(R_(45)))
    u3 = (math.cos(R_(135)), -math.sin(R_(135)))
    for sg in (1, -1):
        # 主拉：由面向外
        x0, y0 = rx + sg*u1[0]*(L*0.72), ry + sg*u1[1]*(L*0.72)
        g.arrow(x0, y0, x0 + sg*u1[0]*52, y0 + sg*u1[1]*52, RED, 3.4, 14)
        # 主壓：指向面
        x0, y0 = rx + sg*u3[0]*(L*0.72 + 54), ry + sg*u3[1]*(L*0.72 + 54)
        g.arrow(x0, y0, rx + sg*u3[0]*(L*0.72 + 2), ry + sg*u3[1]*(L*0.72 + 2), BLUE, 3.4, 14)
    g.text(rx + 80, ry - 88, "σ_1 = +τ（拉）", 18, RED, weight="bold")
    g.text(rx - 84, ry - 88, "σ_3 = −τ（壓）", 18, BLUE, anchor="end", weight="bold")
    g.line(rx - 90, ry, rx + 90, ry, MUTED, 1.2, "4 4")
    g.arc(rx, ry, 40, 0, 45, ORG, 2)
    g.text(rx + 62, ry + 20, "45°", 15, ORG, weight="bold")
    g.text(rx, 330, "主應力狀態", 19, RED, anchor="middle", weight="bold")
    g.text(rx, 356, "同一個應力，換個方向看", 15, MUTED, anchor="middle")
    card(g, 20, 385, 1160, 48, REDBG, "#EBB4AE", 10)
    g.text(600, 416, "剪應力 τ 不是新的破壞模式：它在 45° 方向就是一個大小相等的拉應力 σ_1 = τ", 18, RED, anchor="middle", weight="bold")
    g.save("figs/fig02_element.svg")


# ───────── fig03 純剪莫爾圓 ─────────
def fig03():
    g = SVG(1200, 440)
    ax = Ax(g, 330, 225, 15)
    tau = 10.0
    g.arrow(ax.X(-16), ax.y0, ax.X(15), ax.y0, INK, 2, 10)
    g.arrow(ax.x0, ax.Y(-13), ax.x0, ax.Y(13.5), INK, 2, 10)
    g.text(ax.X(15) + 8, ax.y0 + 6, "σ", 18, INK, weight="bold")
    g.text(ax.X(15), ax.y0 + 28, "拉為正", 13, MUTED, anchor="end")
    g.text(ax.x0 + 10, ax.Y(13.5) + 6, "τ", 18, INK, weight="bold")
    r = tau*ax.kx
    g.add(f'<circle cx="{ax.x0}" cy="{ax.y0}" r="{r}" fill="{PURBG}" fill-opacity="0.5" stroke="{INK}" stroke-width="2.6"/>')
    dot(g, ax.x0, ax.Y(tau), PUR, 8); dot(g, ax.x0, ax.Y(-tau), PUR, 8)
    g.text(ax.x0 + 14, ax.Y(tau) - 8, "X 面 (0, τ)", 16, PUR, weight="bold")
    g.text(ax.x0 + 14, ax.Y(-tau) + 22, "Y 面 (0, −τ)", 16, PUR, weight="bold")
    dot(g, ax.X(tau), ax.y0, RED, 9); dot(g, ax.X(-tau), ax.y0, BLUE, 9)
    g.text(ax.X(tau) + 12, ax.y0 - 14, "σ_1 = +τ", 19, RED, weight="bold")
    g.text(ax.X(-tau) - 12, ax.y0 - 14, "σ_3 = −τ", 19, BLUE, anchor="end", weight="bold")
    g.arc(ax.x0, ax.y0, 58, 90, 0, ORG, 2.4)
    g.arrow(ax.x0 + 58*math.cos(R_(12)), ax.y0 - 58*math.sin(R_(12)), ax.x0 + 58, ax.y0 - 2, ORG, 2.4, 10)
    g.text(ax.x0 + 52, ax.y0 - 58, "2θ = 90°", 17, ORG, weight="bold")
    dot(g, ax.x0, ax.y0, INK, 5)
    g.text(ax.x0 - 10, ax.y0 + 22, "圓心 = 原點", 14, MUTED, anchor="end")
    # 右側推論
    X = 640
    steps = [("1", "圓心 C = (σ_x + σ_y)/2 = 0", INK),
             ("2", "半徑 R = τ", INK),
             ("3", "σ_1 = C + R = +τ　σ_3 = C − R = −τ", RED),
             ("4", "圓上轉 90° → 實體轉 45°", ORG)]
    card(g, X, 40, 540, 250, W, "#D5DAE1", 12)
    g.text(X + 24, 76, "莫爾圓三步讀出主應力", 19, INK, weight="bold")
    for i, (n, t, c) in enumerate(steps):
        y = 118 + i*44
        g.circle(X + 38, y - 6, 14, fill=c, stroke=c, sw=1)
        g.text(X + 38, y, n, 15, W, anchor="middle", weight="bold")
        g.text(X + 64, y, t, 17, c, weight="bold" if c != INK else "normal")
    card(g, X, 306, 540, 110, GOLDBG, "#E6CFA0", 12)
    g.text(X + 24, 342, "所以：", 17, GOLD, weight="bold")
    g.text(X + 24, 374, "主拉與主壓一樣大；混凝土怕的是那個拉", 17, INK)
    g.text(X + 24, 402, "抗壓 280 撐得住 τ，抗拉只有 17.7 撐不住", 17, INK)
    g.save("figs/fig03_mohr.svg")


# ───────── fig04 斜裂縫的走向 ─────────
def fig04():
    g = SVG(1200, 440)
    bx, by, bw_, bh = 60, 90, 1080, 150
    udl(g, bx, bx + bw_, by, 15)
    beam(g, bx, by, bw_, bh)
    pin(g, bx + 30, by + bh); roller(g, bx + bw_ - 30, by + bh)
    # 主拉應力軌跡（示意）：近支承在中性軸處 45°，梁底接近水平
    for side in (1, -1):
        for k in range(3):
            x0 = (bx + 150 + k*120) if side == 1 else (bx + bw_ - 150 - k*120)
            pts = []
            for j in range(21):
                tt = j/20
                yy = by + bh - tt*bh
                # 底部水平、往上逐漸轉 45° 以上
                xx = x0 - side*(bh*(tt**1.6))*0.95
                pts.append((xx, yy))
            g.poly(pts, BLUE, 1.6, dash="6 5")
    # 斜裂縫（垂直主拉）
    for side in (1, -1):
        for k in range(3):
            xb = (bx + 130 + k*95) if side == 1 else (bx + bw_ - 130 - k*95)
            g.line(xb, by + bh - 8, xb + side*95, by + 45, RED, 3.2, cap="round")
    # 跨中撓曲裂縫
    for k in range(5):
        xx = bx + bw_/2 + (k - 2)*55
        g.line(xx, by + bh - 4, xx, by + bh - 60 + abs(k - 2)*12, GOLD, 3, cap="round")
    g.text(bx + 220, by + bh + 58, "支承附近：剪力大 → 斜張裂縫（約 45°）", 16, RED, anchor="middle", weight="bold")
    g.text(bx + bw_ - 220, by + bh + 58, "斜張裂縫（方向對稱）", 16, RED, anchor="middle", weight="bold")
    g.text(bx + bw_/2, by + bh + 58, "跨中：彎矩大 → 垂直撓曲裂縫", 16, GOLD, anchor="middle", weight="bold")
    # 圖例
    card(g, 60, 340, 1080, 88, PANEL, "#D5DAE1", 10)
    g.line(90, 372, 150, 372, BLUE, 2, "6 5"); g.text(162, 378, "主拉應力軌跡（示意）", 16, BLUE, weight="bold")
    g.line(410, 372, 470, 372, RED, 3.2); g.text(482, 378, "裂縫 ⊥ 主拉方向", 16, RED, weight="bold")
    g.text(720, 378, "裂縫永遠沿著「垂直主拉」的方向打開", 16, INK, weight="bold")
    g.text(90, 412, "中性軸處為純剪 → 主拉 45° → 裂縫 45°；往梁底彎曲拉應力變大，裂縫轉為垂直 → 「撓剪裂縫」", 15, MUTED)
    g.save("figs/fig04_cracks.svg")


# ───────── fig05 強度比較：6.3% 與 3.2% ─────────
def fig05():
    g = SVG(1200, 440)
    # 左：全尺度
    ax = Ax(g, 200, 0, 1.45)
    rows = [("抗壓 f'c", FC, INK, "100 %"), ("直接抗拉 f_t ≈ 1.06√f'c", FT, ORG, f"{FT_R:.1f} %"),
            ("開裂剪應力 0.53√f'c", VCS, GREEN, f"{VCS_R:.1f} %")]
    g.text(20, 34, "① 全尺度（kgf/cm²）", 18, INK, weight="bold")
    for i, (lab, v, c, p) in enumerate(rows):
        y = 70 + i*62
        g.text(20, y + 26, lab, 15, c, weight="bold")
        g.rect(ax.X(0), y, v*ax.kx, 36, fill=c, stroke="none", rx=4)
        g.text(ax.X(v) + 10, y + 25, f"{v:.1f}（{p}）", 16, c, weight="bold")
    g.line(ax.X(0), 60, ax.X(0), 262, INK, 1.6)
    card(g, 20, 285, 600, 140, REDBG, "#EBB4AE", 12)
    g.text(40, 320, "混凝土怕拉不怕壓", 19, RED, weight="bold")
    g.text(40, 354, f"f_t 只有 f'c 的 {FT_R:.1f} %：", 17, INK)
    g.text(40, 386, "剪力破壞比的是「拉」，不是「壓」", 17, INK, weight="bold")
    g.text(40, 414, f"（f'c = {FC:.0f}，√f'c = {SQ:.3f}）", 14, MUTED)
    # 右：放大 0–20
    X0 = 690
    g.text(X0, 34, "② 放大到 0～20", 18, INK, weight="bold")
    az = Ax(g, X0 + 30, 300, 23, 1)
    g.line(az.X(0), 300, az.X(20), 300, INK, 1.6)
    for v in (0, 5, 10, 15, 20): az.xt(v, f"{v}")
    bars = [(FT, ORG, "f_t", 150), (VCS, GREEN, "0.53√f'c", 150)]
    for i, (v, c, lab, h) in enumerate(bars):
        x = az.X(0); y = 90 + i*95
        g.rect(x, y, v*az.kx, 56, fill=c, stroke="none", rx=4)
        g.text(x + 10, y + 36, f"{lab} = {v:.2f}", 17, W, weight="bold")
    # 一半標記
    g.line(az.X(FT/2), 70, az.X(FT/2), 300, RED, 1.8, "6 4")
    g.text(az.X(FT/2) + 6, 72, "f_t 的一半", 14, RED, weight="bold")
    card(g, X0, 340, 490, 86, GREENBG, "#9CC7BC", 12)
    g.text(X0 + 20, 372, "0.53 ≈ 1.06 / 2：規範取試驗下限", 17, GREEN, weight="bold")
    g.text(X0 + 20, 404, "V/(b_w d) 是名目平均剪應力，只用到約一半 f_t", 15, INK)
    g.save("figs/fig05_strength.svg")


# ───────── fig06 開根號的效益 ─────────
def fig06():
    g = SVG(1200, 440)
    ax = Ax(g, 90, 360, 1.25, 12.5, xmin=140, ymin=0)
    g.arrow(ax.X(140), ax.y0, ax.X(600), ax.y0, INK, 2, 10)
    g.arrow(ax.x0, ax.y0 + 4, ax.x0, ax.Y(26), INK, 2, 10)
    g.text(ax.X(600) - 10, ax.y0 + 46, "f'c（kgf/cm²）", 15, INK, anchor="end", weight="bold")
    g.text(ax.x0 + 10, ax.Y(26) + 4, "V_c（tf）", 15, INK, weight="bold")
    for v in (210, 280, 350, 420, 490, 560): ax.xt(v, f"{v}")
    for v in (5, 10, 15, 20, 25): ax.yt(v, f"{v}")
    vc = lambda fc: 0.53*math.sqrt(fc)*BD/1000
    lin = lambda fc: VC0*fc/FC
    ax.curve([(f, lin(f)) for f in range(160, 581, 10) if lin(f) < 26], color=MUTED, sw=2, dash="7 5")
    ax.curve([(f, vc(f)) for f in range(150, 581, 5)], color=PUR, sw=3.4)
    v560 = vc(560)
    dot(g, ax.X(280), ax.Y(VC0), PUR, 8); dot(g, ax.X(560), ax.Y(v560), PUR, 8)
    g.text(ax.X(280) - 8, ax.Y(VC0) - 14, f"{VC0:.2f}", 16, PUR, anchor="end", weight="bold")
    g.text(ax.X(560) + 10, ax.Y(v560) + 22, f"{v560:.2f}（+{(v560/VC0-1)*100:.0f} %）", 16, PUR, weight="bold")
    g.text(ax.X(430), ax.Y(24.5), "若是一次方：翻倍 → +100 %", 14, MUTED, anchor="middle")
    g.text(ax.X(350), ax.Y(8.5), "V_c ∝ √f'c", 18, PUR, weight="bold")
    # 右：三種加強方式
    X0 = 720
    g.text(X0, 40, f"示範梁 b_w = {BW:.0f}、d = {D:.0f}、f'c = {FC:.0f}", 16, INK, weight="bold")
    opts = [("f'c 翻倍（280 → 560）", v560, PUR), ("b_w 翻倍（30 → 60）", 2*VC0, GREEN), ("d 翻倍（50 → 100）", 2*VC0, GREEN)]
    k = 11.5
    for i, (lab, v, c) in enumerate(opts):
        y = 76 + i*88
        g.text(X0, y + 4, lab, 16, c, weight="bold")
        g.rect(X0, y + 14, VC0*k, 34, fill="#CBD2DC", stroke="none", rx=3)
        g.rect(X0 + VC0*k, y + 14, (v - VC0)*k, 34, fill=c, stroke="none", rx=3)
        g.text(X0 + v*k + 8, y + 38, f"{v:.1f} tf（+{(v/VC0-1)*100:.0f} %）", 15, c, weight="bold")
    g.text(X0, 346, f"灰色 = 原本的 {VC0:.2f} tf", 13, MUTED)
    card(g, X0 - 10, 362, 470, 66, GREENBG, "#9CC7BC", 12)
    g.text(X0 + 10, 402, "剪力不足：優先加大斷面 b_w d，而不是提高 f'c", 17, GREEN, weight="bold")
    g.save("figs/fig06_sqrt.svg")


# ───────── fig07 軸力讓莫爾圓平移 ─────────
def fig07():
    g = SVG(1200, 440)
    tau = VCS
    ax = Ax(g, 560, 250, 17, xmin=0)
    g.arrow(ax.X(-30), ax.y0, ax.X(30), ax.y0, INK, 2, 10)
    g.arrow(ax.x0, ax.y0 + 4, ax.x0, ax.Y(12.5), INK, 2, 10)
    g.text(ax.X(30) + 8, ax.y0 + 6, "σ", 18, INK, weight="bold")
    g.text(ax.X(30), ax.y0 + 30, "拉為正（kgf/cm²）", 13, MUTED, anchor="end")
    g.text(ax.x0 + 10, ax.Y(12.5) + 6, "τ", 18, INK, weight="bold")
    # f_t 線
    g.line(ax.X(FT), ax.Y(12), ax.X(FT), ax.y0 + 36, ORG, 2.4, "8 5")
    g.text(ax.X(FT) - 8, ax.Y(11.6), f"f_t = {FT:.1f}", 16, ORG, anchor="end", weight="bold")
    cases = [(-S_30, BLUE, "軸壓 30 tf"), (0.0, PUR, "純剪"), (S_30, RED, "軸拉 30 tf")]
    res = []
    for sx, c, lab in cases:
        C = sx/2; Rr = math.sqrt(C*C + tau*tau); s1 = C + Rr
        x1, x2 = ax.X(C - Rr), ax.X(C + Rr); rr = Rr*ax.kx
        g.add(f'<path d="M{x1:.1f},{ax.y0:.1f} A{rr:.1f},{rr:.1f} 0 0 1 {x2:.1f},{ax.y0:.1f}" fill="{c}" fill-opacity="0.06" stroke="{c}" stroke-width="2.6"/>')
        dot(g, ax.X(sx), ax.Y(tau), c, 6)
        dot(g, ax.X(s1), ax.y0, c, 8)
        res.append((sx, s1, c, lab))
    ys = {BLUE: 290, PUR: 316, RED: 342}
    for sx, s1, c, lab in res:
        g.line(ax.X(s1), ax.y0 + 8, ax.X(s1), ys[c] - 14, c, 1.2, "3 3")
        g.text(ax.X(s1) + 4, ys[c], f"σ_1 = {s1:.1f}", 14, c, weight="bold")
    g.text(ax.X(-30), ax.Y(tau) + 5, f"三個圓 τ 都 = {tau:.2f}", 13, MUTED)
    ax.seg(-30, tau, 16.67, tau, color=GRID, sw=1.2, dash="3 3")
    # 左側說明
    card(g, 936, 30, 248, 210, W, "#D5DAE1", 12)
    g.text(950, 64, "同一個 τ，加上軸向應力", 16, INK, weight="bold")
    g.text(950, 96, "圓心 = σ/2 跟著平移", 16, INK)
    g.text(950, 128, "σ_1 = σ/2 + √((σ/2)² + τ²)", 14, INK)
    g.text(950, 166, "軸壓：圓往左 → σ_1 變小", 16, BLUE, weight="bold")
    g.text(950, 198, "軸拉：圓往右 → σ_1 變大", 16, RED, weight="bold")
    g.text(950, 226, f"|N_u| = 30 tf → |σ| = {S_30:.2f}", 13, MUTED)
    card(g, 16, 372, 1168, 58, REDBG, "#EBB4AE", 10)
    g.text(600, 408, f"軸拉 30 tf 讓 σ_1 從 {res[1][1]:.1f} 衝到 {res[2][1]:.1f}，越過 f_t = {FT:.1f}：同樣的 τ 就能拉裂", 18, RED, anchor="middle", weight="bold")
    g.save("figs/fig07_axial_mohr.svg")


# ───────── fig08 軸力修正倍率 ─────────
def fig08():
    g = SVG(1200, 440)
    ax = Ax(g, 90, 330, 5.3, 150, xmin=-45, ymin=0)
    g.arrow(ax.X(-45), ax.y0, ax.X(80), ax.y0, INK, 2, 10)
    g.arrow(ax.X(0), ax.y0 + 4, ax.X(0), ax.Y(1.95), INK, 2, 10)
    g.text(ax.X(80) - 4, ax.y0 + 50, "N_u / A_g（kgf/cm²，壓為正）", 15, INK, anchor="end", weight="bold")
    g.text(ax.X(0) + 10, ax.Y(1.95) + 4, "V_c 修正倍率", 15, INK, weight="bold")
    for v in (-35, -16.67, 0, 16.67, 55.56): ax.xt(v, f"{v:g}" if v in (-35, 0) else f"{v:.1f}")
    ax.seg(-45, 1, 80, 1, color=GRID, sw=1.4)
    for v in (0.5, 1.0, 1.5):
        ax.seg(-45, v, 80, v, color=GRID, sw=1.1)
        g.text(ax.X(-45) - 8, ax.Y(v) + 5, f"{v:.1f}", 13, MUTED, anchor="end")
    ax.seg(-45, 0, -35, 0, color=RED, sw=3.4)
    ax.seg(-35, 0, 0, 1, color=RED, sw=3.4)
    ax.seg(0, 1, 80, 1 + 80/140, color=BLUE, sw=3.4)
    g.text(ax.X(-30), ax.Y(0.6), "斜率 1/35", 16, RED, weight="bold")
    g.text(ax.X(40), ax.Y(1.52), "斜率 1/140", 16, BLUE, weight="bold")
    # 同樣 16.67 的三角形
    for sx, f, c in [(S_30, F_C30, BLUE), (-S_30, F_T30, RED)]:
        ax.seg(0, 1, sx, 1, color=c, sw=1.6, dash="4 3")
        ax.seg(sx, 1, sx, f, color=c, sw=2.4)
        dot(g, ax.X(sx), ax.Y(f), c, 7)
    g.text(ax.X(S_30) + 8, ax.Y(F_C30) + 22, f"{F_C30:.3f}（+{GAIN30:.1f} %）", 14, BLUE, weight="bold")
    g.text(ax.X(-S_30) + 10, ax.Y(F_T30) + 24, f"{F_T30:.3f}（−{LOSS30:.1f} %）", 14, RED, weight="bold")
    dot(g, ax.X(S_C100), ax.Y(F_C100), BLUE, 7)
    g.text(ax.X(S_C100) + 8, ax.Y(F_C100) + 22, f"壓 100 tf：{F_C100:.3f}", 14, BLUE, weight="bold")
    dot(g, ax.X(-35), ax.Y(0), RED, 8)
    g.text(ax.X(-35), ax.Y(0) - 16, "V_c = 0", 15, RED, anchor="middle", weight="bold")
    # 右側
    X0 = 760
    card(g, X0, 30, 424, 190, W, "#D5DAE1", 12)
    g.text(X0 + 20, 64, f"示範梁 A_g = {BW:.0f}×{H:.0f} = {AG:.0f} cm²", 16, INK, weight="bold")
    g.text(X0 + 20, 100, f"±30 tf → N_u/A_g = ±{S_30:.2f}", 16, INK)
    g.text(X0 + 20, 136, f"壓：V_c × {F_C30:.3f} = {VC_C30:.2f} tf", 16, BLUE, weight="bold")
    g.text(X0 + 20, 170, f"拉：V_c × {F_T30:.3f} = {VC_T30:.2f} tf", 16, RED, weight="bold")
    g.text(X0 + 20, 204, f"拉力 {NT_ZERO:.0f} tf（= 35 A_g）時 V_c 歸零", 14, MUTED)
    card(g, X0, 236, 424, 120, GOLDBG, "#E6CFA0", 12)
    g.text(X0 + 20, 270, "同樣大小的軸力", 16, GOLD, weight="bold")
    g.text(X0 + 20, 302, f"拉的扣減 {LOSS30:.1f} % ≈ 壓的增益 {GAIN30:.1f} % × 4", 16, INK)
    g.text(X0 + 20, 334, "莫爾圓給方向，140／35 來自試驗回歸", 14, MUTED)
    g.save("figs/fig08_axial_factor.svg")


# ───────── fig09 V_c 的四個來源（自由體）─────────
def fig09():
    g = SVG(1200, 440)
    bx, by, bh = 60, 60, 190
    # 裂縫左側自由體：梁左段，裂縫由底部 x=470 斜上至 x=300 壓力區下緣
    top_c = 60   # 壓力區深度
    crack = [(470, by + bh), (300, by + top_c)]
    pts = [(bx, by), (300, by), (300, by + top_c), (470, by + bh), (bx, by + bh)]
    g.poly(pts, INK, 2.4, fill=CONC, closed=True)
    g.line(300, by + top_c, 470, by + bh, RED, 4, cap="round")
    g.rect(bx, by, 240, top_c, fill="none", stroke="none")
    # 縱筋
    g.line(bx + 5, by + bh - 22, 520, by + bh - 22, INK, 5)
    # 箍筋（穿過裂縫的兩支）
    for xs in (150, 350, 420):
        yb = by + bh - 10
        g.line(xs, by + 10, xs, yb, GREEN if xs > 300 else "#8FA0B3", 3)
    # 外力 V
    g.arrow(bx + 20, by + bh + 56, bx + 20, by + bh + 4, INK, 3, 13)
    g.text(bx + 34, by + bh + 48, "V（支承反力）", 16, INK, weight="bold")
    # 四個來源
    g.arrow(282, by + top_c + 70, 282, by + 12, PUR, 3.4, 13)
    g.text(262, by + top_c + 64, "① V_{cz}", 17, PUR, anchor="end", weight="bold")
    mx, my = 385, by + (top_c + bh)/2 + 5
    ang = math.atan2(-(bh - top_c), -170)
    g.arrow(mx - 30*math.cos(ang), my - 30*math.sin(ang), mx + 40*math.cos(ang), my + 40*math.sin(ang), ORG, 3.2, 13)
    g.text(mx - 44, my - 14, "② V_a", 17, ORG, anchor="end", weight="bold")
    g.arrow(495, by + bh + 36, 495, by + bh - 20, BLUE, 3.4, 13)
    g.text(510, by + bh + 36, "③ V_d", 17, BLUE, weight="bold")
    for xs in (350, 420):
        g.arrow(xs, by + bh - 60, xs, by + 30 + (xs - 300)*0.2, GREEN, 3, 12)
    g.text(430, by + 40, "V_s（箍筋）", 16, GREEN, weight="bold")
    g.text(300, 36, "斜裂縫左側自由體", 17, INK, anchor="middle", weight="bold")
    # 右：清單
    X0 = 620
    rows = [("①", "未開裂壓力區 V_{cz}", "裂縫上方混凝土直接傳剪", PUR),
            ("②", "骨材互鎖 V_a", "粗糙裂縫面咬合、摩擦", ORG),
            ("③", "縱筋銷栓 V_d", "主筋像插銷橫向頂住", BLUE),
            ("④", "拱作用", "短剪跨時壓桿直接傳到支承", GOLD)]
    card(g, X0, 20, 564, 300, W, "#D5DAE1", 12)
    g.text(X0 + 20, 54, "V_c = 以上混凝土貢獻的總和（試驗打包成一條式）", 16, INK, weight="bold")
    for i, (n, hd, ex, c) in enumerate(rows):
        y = 100 + i*56
        g.circle(X0 + 38, y - 6, 15, fill=c, stroke=c, sw=1)
        g.text(X0 + 38, y, n, 15, W, anchor="middle", weight="bold")
        g.text(X0 + 64, y, hd, 17, c, weight="bold")
        g.text(X0 + 64, y + 22, ex, 14, MUTED)
    card(g, X0, 334, 564, 96, REDBG, "#EBB4AE", 12)
    g.text(X0 + 20, 368, "塑鉸區反覆載重：裂縫交叉、張開、貫穿全深", 16, RED, weight="bold")
    g.text(X0 + 20, 400, "壓力區破碎、裂面磨平、保護層剝落 → 四項同時失效", 15, INK)
    card(g, 16, 334, 580, 96, GREENBG, "#9CC7BC", 12)
    g.text(36, 368, "V_c：開裂那一刻混凝土能撐多少（抗拉的故事）", 16, GREEN, weight="bold")
    g.text(36, 400, "V_s：裂開以後，靠箍筋把裂縫縫住（數箍筋的故事）", 15, INK)
    g.save("figs/fig09_sources.svg")


# ───────── fig10 塑鉸區 V_c = 0 ─────────
def fig10():
    g = SVG(1200, 440)
    # 柱－梁－柱
    cl, cr, cw = 60, 700, 60
    yb0, yb1 = 150, 240
    for x in (cl, cr):
        g.rect(x, 30, cw, 330, fill=CONC, stroke=INK, sw=2.4)
    beam(g, cl + cw, yb0, cr - cl - cw, yb1 - yb0)
    Hh = yb1 - yb0
    for x0, sgn in ((cl + cw, 1), (cr, -1)):
        xa, xb = x0, x0 + sgn*2*Hh
        g.rect(min(xa, xb), yb0, 2*Hh, Hh, fill=RED, stroke="none", op=0.14)
        g.rect(min(xa, xb), yb0, 2*Hh, Hh, fill="none", stroke=RED, sw=2, dash="7 4")
        # X 形裂縫
        for k in range(3):
            xs = min(xa, xb) + 25 + k*52
            g.line(xs, yb0 + 12, xs + 40, yb1 - 12, RED, 2.4, cap="round")
            g.line(xs + 40, yb0 + 12, xs, yb1 - 12, RED, 2.4, cap="round")
        # 尺寸
        g.line(xa, yb1 + 30, xb, yb1 + 30, INK, 1.4)
        for x in (xa, xb): g.line(x, yb1 + 22, x, yb1 + 38, INK, 1.4)
        g.text((xa + xb)/2, yb1 + 58, "2h", 17, RED, anchor="middle", weight="bold")
    g.text((cl + cr + cw)/2, yb1 + 58, "中段：V_c 照算", 16, GREEN, anchor="middle", weight="bold")
    # 反覆地震
    g.arrow(380, 70, 470, 70, INK, 2.6, 12); g.arrow(380, 100, 290, 100, INK, 2.6, 12)
    g.text(380, 56, "地震力反覆往復", 16, INK, anchor="middle", weight="bold")
    g.text(200, yb0 - 14, "塑鉸區", 16, RED, anchor="middle", weight="bold")
    g.text(cr - 90, yb0 - 14, "塑鉸區", 16, RED, anchor="middle", weight="bold")
    card(g, 60, 370, 700, 58, REDBG, "#EBB4AE", 10)
    g.text(410, 406, "兩個方向的斜裂縫交叉成 X，混凝土被磨碎 → 不再算 V_c", 17, RED, anchor="middle", weight="bold")
    # 條件
    X0 = 800
    card(g, X0, 30, 384, 398, W, RED, 14, 2)
    g.text(X0 + 20, 66, "令 V_c = 0 的條件", 19, RED, weight="bold")
    g.text(X0 + 20, 96, "（特殊抗彎矩構架，兩條同時成立）", 14, MUTED)
    g.circle(X0 + 36, 136, 15, fill=RED, stroke=RED, sw=1); g.text(X0 + 36, 142, "1", 15, W, anchor="middle", weight="bold")
    g.text(X0 + 62, 142, "地震引致之剪力", 16, INK, weight="bold")
    g.text(X0 + 62, 168, "≥ 該區最大設計剪力的 1/2", 16, INK)
    g.circle(X0 + 36, 214, 15, fill=RED, stroke=RED, sw=1); g.text(X0 + 36, 220, "2", 15, W, anchor="middle", weight="bold")
    g.text(X0 + 62, 220, "設計軸壓力（含地震）", 16, INK, weight="bold")
    g.text(X0 + 62, 246, "< A_g f'c / 20", 16, INK)
    g.line(X0 + 20, 280, X0 + 364, 280, GRID, 1.4)
    g.text(X0 + 20, 314, "→ 梁端 2h 範圍內 V_c = 0", 17, RED, weight="bold")
    g.text(X0 + 20, 346, "全部剪力由箍筋 V_s 承擔", 16, INK)
    g.text(X0 + 20, 378, "條件不成立 → V_c 照一般式計算", 15, MUTED)
    g.text(X0 + 20, 406, "（軸壓夠大時裂縫會被壓住）", 14, MUTED)
    g.save("figs/fig10_hinge.svg")


# ───────── fig11 V_s：數箍筋 ─────────
def fig11():
    g = SVG(1200, 440)
    bx, by, bw_, bh = 40, 30, 700, 300
    beam(g, bx, by, bw_, bh)
    top, bot = by + 22, by + bh - 22
    sp = 75                   # 像素 / s（s = 15 cm）
    kpx = sp/S15              # px per cm
    dpx = D*kpx               # d = 50 cm → 250 px
    xs0 = bx + 60
    stir = [xs0 + i*sp for i in range(9)]
    x_crack0 = xs0 + 110
    x_crack1 = x_crack0 + dpx
    crossing = [x for x in stir if x_crack0 < x < x_crack1]
    for x in stir:
        c = GREEN if x in crossing else "#8FA0B3"
        g.line(x, top, x, bot, c, 4 if x in crossing else 2.4)
    g.line(bx + 10, bot + 4, bx + bw_ - 10, bot + 4, INK, 6)
    g.line(x_crack0, bot + 10, x_crack1, bot + 10 - dpx, RED, 4, cap="round")
    for x in crossing:
        yc = bot + 10 - (x - x_crack0)
        g.arrow(x, yc + 36, x, yc - 30, GREEN, 3, 12)
        dot(g, x, yc, RED, 6)
    # 尺寸 d
    g.line(x_crack0, bot + 44, x_crack1, bot + 44, INK, 1.6)
    for x in (x_crack0, x_crack1): g.line(x, bot + 36, x, bot + 52, INK, 1.6)
    g.text((x_crack0 + x_crack1)/2, bot + 72, "水平投影 ≈ d = 50 cm（45° 裂縫）", 16, RED, anchor="middle", weight="bold")
    # 尺寸 s
    g.line(stir[6], top - 14, stir[7], top - 14, INK, 1.6)
    for x in (stir[6], stir[7]): g.line(x, top - 22, x, top - 6, INK, 1.6)
    g.text((stir[6] + stir[7])/2, top - 22, "s = 15", 15, INK, anchor="middle", weight="bold")
    g.text(bx + bw_ - 20, by + bh + 80, "", 1)
    # 右
    X0 = 770
    card(g, X0, 30, 414, 250, W, "#D5DAE1", 12)
    g.text(X0 + 20, 64, "V_s 是「數」出來的", 19, GREEN, weight="bold")
    g.text(X0 + 20, 102, "跨越裂縫的箍筋支數 n = d / s", 16, INK)
    g.text(X0 + 20, 134, "每支提供 A_v f_{yt}（降伏）", 16, INK)
    g.text(X0 + 20, 172, "V_s = n · A_v f_{yt} = A_v f_{yt} d / s", 17, GREEN, weight="bold")
    g.line(X0 + 20, 192, X0 + 394, 192, GRID, 1.4)
    g.text(X0 + 20, 222, f"D13 雙肢 A_v = {AV:.3f} cm²", 15, MUTED)
    g.text(X0 + 20, 250, f"n = {D:.0f}/{S15:.0f} = {N_ST:.2f} 支 → V_s = {VS15:.2f} tf", 16, INK, weight="bold")
    card(g, X0, 294, 414, 136, GOLDBG, "#E6CFA0", 12)
    g.text(X0 + 20, 328, "所以 s 不能太大", 17, GOLD, weight="bold")
    g.text(X0 + 20, 360, "s > d 時一條 45° 裂縫可能一支都沒穿到", 15, INK)
    g.text(X0 + 20, 390, "→ s_{max} = d/2（高剪力區 d/4）", 16, INK, weight="bold")
    g.text(X0 + 20, 418, "圖中穿過裂縫的綠色箍筋共 3 支（n ≈ 3.33）", 13, MUTED)
    g.save("figs/fig11_vs.svg")


# ───────── fig12 上限：斜壓桿壓碎 ─────────
def fig12():
    g = SVG(1200, 440)
    def truss(x0, y0, wdt, hgt, n, heavy, title, col, sub):
        g.text(x0 + wdt/2, y0 - 22, title, 18, col, anchor="middle", weight="bold")
        g.line(x0, y0, x0 + wdt, y0, BLUE, 5)
        g.line(x0, y0 + hgt, x0 + wdt, y0 + hgt, RED, 5)
        step = wdt/n
        for i in range(n + 1):
            x = x0 + i*step
            g.line(x, y0, x, y0 + hgt, RED, 5 if heavy else 2.6)
        for i in range(n):
            x = x0 + i*step
            g.line(x, y0 + hgt, x + step, y0, BLUE, 7 if heavy else 4)
        if heavy:
            for i in range(n):
                x = x0 + i*step + step/2; y = y0 + hgt/2
                g.line(x - 11, y - 11, x + 11, y + 11, RED, 4, cap="round"); g.line(x - 11, y + 11, x + 11, y - 11, RED, 4, cap="round")
        g.text(x0 + wdt/2, y0 + hgt + 38, sub, 15, INK, anchor="middle")
    truss(40, 90, 330, 140, 3, False, "箍筋適量", GREEN, "箍筋先降伏 → 有預警（韌性）")
    truss(430, 90, 330, 140, 3, True, "箍筋過多", RED, "斜壓桿先壓碎 → 突然崩（脆性）")
    g.line(40, 300, 110, 300, RED, 4); g.text(118, 306, "拉桿（箍筋、主筋）", 14, RED, weight="bold")
    g.line(300, 300, 370, 300, BLUE, 6); g.text(378, 306, "壓桿（裂縫間混凝土）", 14, BLUE, weight="bold")
    card(g, 40, 330, 720, 98, REDBG, "#EBB4AE", 12)
    g.text(60, 366, "上限是「抗壓的故事」：箍筋再多，混凝土斜壓桿也只撐得住這麼多", 16, RED, weight="bold")
    g.text(60, 398, "超過上限不能靠加箍筋解決 → 必須加大斷面 b_w d（或提高 f'c）", 16, INK)
    # 右：堆疊條
    X0, Y0 = 830, 60
    k = 5.2
    g.text(X0, 40, f"示範梁（tf）", 16, INK, weight="bold")
    bars = [("V_c", VC0, GREEN), ("V_{s,max} = 2.12√f'c b_w d", VS_MAX, PUR)]
    y = Y0
    g.rect(X0, y, 60, VC0*k, fill=GREEN, stroke="none")
    g.rect(X0, y + VC0*k, 60, VS_MAX*k, fill=PUR, stroke="none", op=0.75)
    for i in range(1, 5):
        g.line(X0, y + VC0*k*(i + 1), X0 + 60, y + VC0*k*(i + 1), W, 1.4, "4 3")
    g.text(X0 + 72, y + VC0*k/2 + 6, f"V_c = {VC0:.2f}", 15, GREEN, weight="bold")
    g.text(X0 + 72, y + VC0*k + VS_MAX*k/2 - 4, f"V_s ≤ {VS_MAX:.2f}", 15, PUR, weight="bold")
    g.text(X0 + 72, y + VC0*k + VS_MAX*k/2 + 20, "= 4 × 13.30", 14, PUR)
    g.line(X0 - 8, y + (VC0 + VS_MAX)*k, X0 + 330, y + (VC0 + VS_MAX)*k, RED, 2, "7 4")
    g.text(X0 + 72, y + (VC0 + VS_MAX)*k - 8, f"V_{{n,max}} = {VN_MAX:.2f} = 5 V_c", 15, RED, weight="bold")
    g.text(X0 + 72, y + (VC0 + VS_MAX)*k + 22, f"φV_{{n,max}} = {PHI*VN_MAX:.2f}", 15, RED)
    g.save("figs/fig12_limit.svg")


# ───────── fig13 V_c 四張臉：選式流程 ─────────
def fig13():
    g = SVG(1200, 440)
    def dia(cx, cy, w, h, t1, t2=None):
        g.poly([(cx, cy - h/2), (cx + w/2, cy), (cx, cy + h/2), (cx - w/2, cy)], NAVY, 2.4, fill=W, closed=True)
        g.text(cx, cy + (-4 if t2 else 6), t1, 16, NAVY, anchor="middle", weight="bold")
        if t2: g.text(cx, cy + 18, t2, 14, NAVY, anchor="middle")
    ys = 80
    xs = [150, 450, 750]
    dia(xs[0], ys, 250, 100, "塑鉸區？", "兩條件都成立")
    dia(xs[1], ys, 250, 100, "有軸力 N_u？")
    dia(xs[2], ys, 250, 100, "給了 ρ_w、M_u", "或要求精算？")
    for a, b in ((xs[0], xs[1]), (xs[1], xs[2])):
        g.arrow(a + 125, ys, b - 127, ys, INK, 2.2, 10)
        g.text((a + b)/2, ys - 10, "否", 15, MUTED, anchor="middle", weight="bold")
    g.arrow(xs[2] + 125, ys, 1000, ys, INK, 2.2, 10)
    g.text(xs[2] + 150, ys - 10, "否", 15, MUTED, anchor="middle", weight="bold")
    boxes = [
        (20, 170, 260, "V_c = 0", ["全靠箍筋 V_s"], "0", RED, REDBG, xs[0]),
        (300, 170, 300, "軸壓：× (1 + N_u/140A_g)", ["軸拉：× (1 + N_u/35A_g) ≥ 0", "N_u 壓正拉負"], f"壓 100 tf：{VC_C100:.2f}｜拉 30 tf：{VC_T30:.2f}", BLUE, BLUEBG, xs[1]),
        (620, 170, 290, "精算式", ["(0.50√f'c + 176ρ_w V_u d/M_u) b_w d", "V_u d/M_u ≤ 1、≤ 0.93√f'c b_w d"], f"ρ_w = 0.02、V_u d/M_u = 0.5：{VC_DET:.2f}", GOLD, GOLDBG, xs[2]),
    ]
    for x, y, w, hd, lines, demo, c, bg, cx in boxes:
        g.arrow(cx, ys + 50, cx, y - 2, c, 2.2, 10)
        g.text(cx + 8, ys + 80, "是", 15, c, weight="bold")
        card(g, x, y, w, 250, bg, c, 12, 2)
        g.text(x + 16, y + 34, hd, 17, c, weight="bold")
        for i, t in enumerate(lines):
            g.text(x + 16, y + 70 + i*30, t, 14 if len(t) > 22 else 15, INK)
        g.line(x + 16, y + 176, x + w - 16, y + 176, GRID, 1.4)
        g.text(x + 16, y + 206, "示範梁（tf）", 13, MUTED)
        g.text(x + 16, y + 232, demo, 14, c, weight="bold")
    card(g, 930, 30, 254, 390, GREENBG, GREEN, 12, 2)
    g.text(950, 66, "基本式", 19, GREEN, weight="bold")
    g.text(950, 104, "V_c = 0.53√f'c b_w d", 16, INK, weight="bold")
    g.text(950, 142, "一般梁、無軸力", 15, INK)
    g.text(950, 170, "未要求精算：最常用", 15, INK)
    g.text(950, 198, "答案偏保守", 15, MUTED)
    g.line(950, 346, 1164, 346, GRID, 1.4)
    g.text(950, 376, "示範梁（tf）", 13, MUTED)
    g.text(950, 402, f"{VC0:.2f}", 18, GREEN, weight="bold")
    g.save("figs/fig13_flow.svg")


# ───────── fig14 示範梁五種 V_c ─────────
def fig14():
    g = SVG(1200, 400)
    rows = [("基本式", VC0, GREEN, "1.00"), ("精算式（ρ_w 0.02、V_u d/M_u 0.5）", VC_DET, GOLD, f"{VC_DET/VC0:.2f}"),
            ("軸壓 100 tf", VC_C100, BLUE, f"{F_C100:.2f}"), ("軸拉 30 tf", VC_T30, RED, f"{F_T30:.2f}"),
            ("塑鉸區（兩條件成立）", 0.0, "#8B1E14", "0")]
    ax = Ax(g, 380, 0, 29)
    for i, (lab, v, c, r) in enumerate(rows):
        y = 30 + i*64
        g.text(360, y + 30, lab, 16, c, anchor="end", weight="bold")
        if v > 0: g.rect(ax.X(0), y + 6, v*ax.kx, 38, fill=c, stroke="none", rx=4)
        g.text(ax.X(v) + 10, y + 32, f"{v:.2f} tf（× {r}）", 16, c, weight="bold")
    g.line(ax.X(0), 26, ax.X(0), 350, INK, 1.8)
    g.line(ax.X(VC0), 26, ax.X(VC0), 350, GREEN, 1.4, "5 4")
    g.line(ax.X(VC_DET_CAP), 26, ax.X(VC_DET_CAP), 350, GOLD, 1.4, "5 4")
    g.text(ax.X(VC_DET_CAP), 372, f"精算上限 0.93√f'c b_w d = {VC_DET_CAP:.2f}", 14, GOLD, anchor="end", weight="bold")
    g.text(ax.X(VC0), 372, "基本式", 14, GREEN, anchor="middle", weight="bold")
    g.save("figs/fig14_faces.svg")


# ───────── fig15 精算式：兩項的物理意義 ─────────
def fig15():
    g = SVG(1200, 420)
    ax = Ax(g, 90, 340, 560, 17, xmin=0, ymin=0)
    g.arrow(ax.X(0), ax.y0, ax.X(1.1), ax.y0, INK, 2, 10)
    g.arrow(ax.X(0), ax.y0 + 4, ax.X(0), ax.Y(17.5), INK, 2, 10)
    g.text(ax.X(1.1) - 4, ax.y0 + 46, "V_u d / M_u", 16, INK, anchor="end", weight="bold")
    g.text(ax.X(0) + 10, ax.Y(17.5) + 4, "V_c / (b_w d)（kgf/cm²）", 15, INK, weight="bold")
    for v in (0, 0.25, 0.5, 0.75, 1.0): ax.xt(v, f"{v:g}")
    for v in (5, 10, 15): ax.yt(v, f"{v}")
    cap = 0.93*SQ; base = 0.53*SQ
    ax.seg(0, cap, 1.05, cap, color=RED, sw=2.2, dash="8 5")
    g.text(ax.X(1.05), ax.Y(cap) - 10, f"上限 0.93√f'c = {cap:.2f}", 15, RED, anchor="end", weight="bold")
    ax.seg(0, base, 1.05, base, color=GREEN, sw=2.2, dash="8 5")
    g.text(ax.X(1.0) - 8, ax.Y(base) + 22, f"基本式 0.53√f'c = {base:.2f}", 15, GREEN, anchor="end", weight="bold")
    for rho, c in ((0.01, "#A08BD8"), (0.02, PUR), (0.03, "#4B2F99")):
        f = lambda x: 0.5*SQ + 176*rho*x
        ax.seg(0, f(0), 1.0, f(1.0), color=c, sw=3)
        g.text(ax.X(1.0) + 8, ax.Y(f(1.0)) + 5, f"ρ_w = {rho}", 14, c, weight="bold")
    ax.seg(1.0, 0, 1.0, cap, color=MUTED, sw=1.4, dash="3 3")
    g.text(ax.X(1.0) - 6, ax.Y(2), "≤ 1.0", 13, MUTED, anchor="end")
    dot(g, ax.X(VDM), ax.Y(VC_DET_S), PUR, 8)
    g.line(ax.X(VDM), ax.Y(VC_DET_S), ax.X(0.36), ax.Y(13.2), PUR, 1.4)
    g.text(ax.X(0.36), ax.Y(13.2) - 6, f"示範：{VC_DET_S:.2f}", 15, PUR, anchor="end", weight="bold")
    g.text(ax.X(0) + 10, ax.Y(0.5*SQ) + 22, f"起點 0.50√f'c = {0.5*SQ:.2f}", 13, MUTED)
    X0 = 790
    card(g, X0, 30, 394, 170, W, "#D5DAE1", 12)
    g.text(X0 + 20, 64, "第二項 176 ρ_w V_u d / M_u", 17, PUR, weight="bold")
    g.text(X0 + 20, 98, "ρ_w 大：銷栓作用強、裂縫窄", 15, INK)
    g.text(X0 + 20, 128, "V_u d/M_u 大：剪力為主、彎矩小", 15, INK)
    g.text(X0 + 20, 158, "→ 裂縫較晚出現，V_c 可以多算", 15, INK, weight="bold")
    g.text(X0 + 20, 186, "V_u、M_u 取同一斷面、同一載重組合", 13, MUTED)
    card(g, X0, 214, 394, 130, GOLDBG, "#E6CFA0", 12)
    g.text(X0 + 20, 248, "係數：規範 176（2500 psi 換算）", 16, GOLD, weight="bold")
    g.text(X0 + 20, 280, "部分教材寫 175，差 0.6 %，不影響答案", 14, INK)
    g.text(X0 + 20, 310, "精算式最多比基本式多 75 %（0.93/0.53）", 14, INK)
    g.save("figs/fig15_detail.svg")


# ───────── fig16 V_u 落在哪一區 ─────────
def fig16():
    g = SVG(1200, 420)
    z = [0, PHI*VC0/2, PHI*VC0, PHI*(VC0 + VS_HALF), PHI*VN_MAX, 58]
    ax = Ax(g, 50, 170, 1090/58)
    cols = ["#9AA3AE", GREEN, BLUE, PUR, RED]
    labs = [("不需箍筋", ""), ("最少箍筋", ""), ("計算 V_s", "s ≤ d/2"), ("計算 V_s", "s ≤ d/4"), ("加大斷面", "")]
    for i in range(5):
        x1, x2 = ax.X(z[i]), ax.X(z[i + 1])
        g.rect(x1, 110, x2 - x1, 60, fill=cols[i], stroke=W, sw=2, op=0.85)
        cx = (x1 + x2)/2
        g.text(cx, 138, labs[i][0], 15 if x2 - x1 > 80 else 12, W, anchor="middle", weight="bold")
        if labs[i][1]: g.text(cx, 160, labs[i][1], 14, W, anchor="middle")
    names = ["0", "φV_c/2", "φV_c", "φ(V_c + 1.06√f'c b_w d)", "φ(V_c + 2.12√f'c b_w d)"]
    for i in range(5):
        x = ax.X(z[i])
        g.line(x, 172, x, 196, INK, 1.6)
        g.text(x, 216, f"{z[i]:.2f}", 15, INK, anchor="middle", weight="bold")
        if i:
            g.text(x, 88 - (i % 2)*26, names[i], 14, cols[i], anchor="middle", weight="bold")
    g.text(ax.X(58), 216, "V_u（tf）", 14, MUTED, anchor="end")
    xv = ax.X(VU)
    g.arrow(xv, 270, xv, 176, ORG, 3, 13)
    g.text(xv, 292, f"V_u = {VU:.0f} tf", 17, ORG, anchor="middle", weight="bold")
    card(g, 40, 312, 1120, 100, PANEL, "#D5DAE1", 12)
    g.text(60, 346, f"示範梁 V_u = {VU:.0f}：V_{{s,req}} = {VU:.0f}/{PHI} − {VC0:.2f} = {VS_REQ:.2f} tf > 1.06√f'c b_w d = {VS_HALF:.2f} → s_{{max}} = d/4 = {S_MAX:.1f} cm", 16, INK, weight="bold")
    g.text(60, 380, f"計算需求 s = {S_REQ:.1f} cm，但上限 {S_MAX:.1f} 控制 → 用 s = {S_USE:.1f}：V_s = {VS_USE:.2f}，φV_n = {PVN:.2f} ≥ {VU:.0f} ✓", 16, INK)
    g.text(60, 404, "區間界線都是 V_c 與 √f'c b_w d 的倍數：先算 φV_c，就能一眼定位", 13, MUTED)
    g.save("figs/fig16_zones.svg")


if __name__ == "__main__":
    for f in [fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10, fig11, fig12, fig13, fig14, fig15, fig16]:
        f()
    print("figs ok")
