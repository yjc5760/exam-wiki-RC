import math
from svglib import SVG, INK, MUTED, GRID, PANEL, measure
from params import *
RED, GRN, ORG, BLU, PUR, GLD, TEAL = "#C0392B", "#1E8449", "#B9540F", "#2F54C8", "#6D4BC2", "#B7791F", "#2E7D6B"
RBG, GBG, OBG, BBG, PBG = "#FBECEA", "#E6F2EA", "#FDF1E7", "#EEF2FB", "#F1EDFA"
SBAND = "#BCC8EE"; HATCH = "#9AA3AE"
def f2(v): return f"{v+1e-9:.2f}"
def f1(v): return f"{v+1e-9:.1f}"
def pin(g, x, y, sc=1.0):
    g.poly([(x, y), (x-16*sc, y+26*sc), (x+16*sc, y+26*sc)], color=INK, sw=2.2, fill="#FFFFFF", closed=True)
    g.line(x-26*sc, y+26*sc, x+26*sc, y+26*sc, INK, 2)
    for i in range(5): g.line(x-22*sc+i*10*sc, y+26*sc, x-30*sc+i*10*sc, y+36*sc, INK, 1.3)
def roller(g, x, y, sc=1.0):
    g.poly([(x, y), (x-16*sc, y+22*sc), (x+16*sc, y+22*sc)], color=INK, sw=2.2, fill="#FFFFFF", closed=True)
    for dx in (-9, 0, 9): g.circle(x+dx*sc, y+27*sc, 4*sc, fill="#FFFFFF", stroke=INK, sw=1.6)
    g.line(x-26*sc, y+32*sc, x+26*sc, y+32*sc, INK, 2)
    for i in range(5): g.line(x-22*sc+i*10*sc, y+32*sc, x-30*sc+i*10*sc, y+42*sc, INK, 1.3)
def hatch(g, x, y, w, h, step=16, fill="#EEF1F5"):
    g.rect(x, y, w, h, fill=fill, stroke=INK, sw=2)
    k = -h
    while k < w:
        xa, ya = x+max(k, 0), y+h-max(0, -k)
        xb, yb = x+min(k+h, w), y+h-(min(k+h, w)-k)
        g.line(xa, ya, xb, yb, HATCH, 0.9); k += step
def tag(g, x, y, txt, col, size=17, fg="#FFFFFF", center=False):
    w = measure(txt, size, True) + 26
    if center: x -= w/2
    g.rect(x, y, w, size+14, fill=col, stroke="none", rx=(size+14)/2)
    g.text(x+w/2, y+size+3, txt, size, fg, "middle", "bold"); return w
def card(g, x, y, w, h, fill=PANEL, stroke="#D5DAE1"):
    g.rect(x, y, w, h, fill=fill, stroke=stroke, sw=1.4, rx=14)
def diamond(g, cx, cy, hw, hh, col, bg):
    g.poly([(cx, cy-hh), (cx+hw, cy), (cx, cy+hh), (cx-hw, cy)], color=col, sw=2.5, fill=bg, closed=True)
def band(g, p1, p2, w1, w2=None, fill=SBAND, op=0.85):
    """p1→p2 的帶狀區（兩端寬 w1、w2，垂直於軸線量）"""
    w2 = w1 if w2 is None else w2
    a = math.atan2(p2[1]-p1[1], p2[0]-p1[0]); nx, ny = -math.sin(a), math.cos(a)
    P = [(p1[0]+nx*w1/2, p1[1]+ny*w1/2), (p2[0]+nx*w2/2, p2[1]+ny*w2/2), (p2[0]-nx*w2/2, p2[1]-ny*w2/2), (p1[0]-nx*w1/2, p1[1]-ny*w1/2)]
    g.poly(P, color="none", sw=0, fill=fill, closed=True, op=op)
def bottle(g, p1, p2, we, wm, fill=SBAND, op=0.85, n=24):
    a = math.atan2(p2[1]-p1[1], p2[0]-p1[0]); nx, ny = -math.sin(a), math.cos(a)
    L, R = [], []
    for i in range(n+1):
        u = i/n; w = we + (wm-we)*math.sin(math.pi*u)
        x, y = p1[0]+(p2[0]-p1[0])*u, p1[1]+(p2[1]-p1[1])*u
        L.append((x+nx*w/2, y+ny*w/2)); R.append((x-nx*w/2, y-ny*w/2))
    g.poly(L+R[::-1], color="none", sw=0, fill=fill, closed=True, op=op)
def dimh(g, x1, x2, y, txt, col=MUTED, size=18, up=True):
    g.line(x1, y, x2, y, col, 1.4); g.line(x1, y-7, x1, y+7, col, 1.4); g.line(x2, y-7, x2, y+7, col, 1.4)
    g.text((x1+x2)/2, y-8 if up else y+24, txt, size, col, "middle", "bold", bg="#FFFFFF")
def dimv(g, x, y1, y2, txt, col=MUTED, size=18, side="left"):
    g.line(x, y1, x, y2, col, 1.4); g.line(x-7, y1, x+7, y1, col, 1.4); g.line(x-7, y2, x+7, y2, col, 1.4)
    if side == "left": g.text(x-10, (y1+y2)/2+6, txt, size, col, "end", "bold")
    else: g.text(x+10, (y1+y2)/2+6, txt, size, col, "start", "bold")

# ───────── fig01 識別地圖 ─────────
def fig01():
    g = SVG(1600, 560)
    g.rect(20, 140, 220, 110, fill="#1F2A37", stroke="none", rx=16)
    g.text(130, 188, "拿到一題", 22, "#FFFFFF", "middle", "bold"); g.text(130, 222, "剪力題", 22, "#FFFFFF", "middle", "bold")
    g.arrow(240, 195, 292, 195, INK, 3, 14)
    diamond(g, 490, 195, 196, 110, ORG, OBG)
    g.text(490, 182, "有既有滑動介面？", 23, ORG, "middle", "bold")
    g.text(490, 216, "施工縫／新舊混凝土／預鑄接縫", 16, INK, "middle")
    g.arrow(686, 195, 742, 195, INK, 3, 14); g.text(714, 182, "否", 19, MUTED, "middle", "bold")
    diamond(g, 940, 195, 196, 110, BLU, BBG)
    g.text(940, 182, "a/d ≤ 2 或 D 區？", 23, BLU, "middle", "bold")
    g.text(940, 216, "深梁／牛腿／托架／樁帽", 16, INK, "middle")
    g.arrow(1136, 195, 1192, 195, INK, 3, 14); g.text(1164, 182, "否", 19, MUTED, "middle", "bold")
    g.rect(1195, 125, 385, 140, fill=PBG, stroke=PUR, sw=2.5, rx=16)
    g.text(1387, 170, "桁架類比（B 區）", 24, PUR, "middle", "bold")
    g.text(1387, 207, "V_n = V_c + V_s", 21, INK, "middle")
    g.text(1387, 242, "→ 拼圖三：四道關卡", 18, MUTED, "middle")
    for cx, col, bg, t1, t2, t3 in [(490, ORG, OBG, "邊界主題 ②：剪力摩擦", "V_n = μ (A_{vf} f_y + P_c)", "鋼筋「夾住」介面"),
                                    (940, BLU, BBG, "邊界主題 ①：壓拉桿 STM", "壓桿／拉桿／節點 三種驗算", "力「走直線」進支承")]:
        g.arrow(cx, 305, cx, 368, INK, 3, 14); g.text(cx+14, 345, "是", 19, col, "start", "bold")
        g.rect(cx-200, 372, 400, 150, fill=bg, stroke=col, sw=2.5, rx=16)
        g.text(cx, 414, t1, 23, col, "middle", "bold"); g.text(cx, 456, t2, 21, INK, "middle"); g.text(cx, 496, t3, 18, MUTED, "middle")
    g.rect(1195, 372, 385, 150, fill=PANEL, stroke="#6B7280", sw=2, rx=16, dash="8 6")
    g.text(1387, 414, "附帶：同時有 T_u？", 23, "#4B5563", "middle", "bold")
    g.text(1387, 456, "T_u ≤ φT_{th} → 可忽略", 20, INK, "middle")
    g.text(1387, 496, "門檻用 A_{cp}、p_{cp}（外緣）", 18, MUTED, "middle")
    g.text(800, 60, "先問「公式認對了沒」，再代數字：這兩個特例一旦套 V_c + V_s，整題必錯", 24, INK, "middle", "bold")
    g.save("figs/fig01_map.svg")

# ───────── fig02 示範案例 ─────────
def fig02():
    g = SVG(1600, 590)
    W = 505
    for i, (hd, col) in enumerate([("例⑤ 深梁（STM）", BLU), ("例④ 新舊混凝土介面（剪力摩擦）", ORG), ("基準斷面（扭力門檻）", "#4B5563")]):
        x = 20 + i*(W+25); card(g, x, 20, W, 555); g.rect(x, 20, W, 10, fill=col, stroke="none")
        g.text(x+W/2, 72, hd, 24, col, "middle", "bold")
    # 例⑤
    x = 20; s = 1.15; L = 360; bx = x + (W-L*s)/2; by = 170
    g.rect(bx, by, L*s, H5*s, fill="#E9EDF2", stroke=INK, sw=2.5)
    xs1, xs2, xp = bx+30*s, bx+330*s, bx+180*s
    g.arrow(xp, by-70, xp, by-4, RED, 3.5, 16); g.text(xp+10, by-48, f"P_u = {PU5:.0f} tf", 19, RED, "start", "bold")
    pin(g, xs1, by+H5*s, 0.8); roller(g, xs2, by+H5*s, 0.8)
    dimh(g, xs1, xp, by+H5*s+64, f"a = {A5:.0f}", BLU, 17)
    dimv(g, bx+L*s+14, by, by+H5*s, f"h = {H5:.0f}", MUTED, 16, "right")
    g.text(x+W/2, 462, f"b = {B5:.0f}、h = {H5:.0f}、d = {D5:.0f} cm", 19, INK, "middle")
    g.text(x+W/2, 496, f"a/d = {A5:.0f}/{D5:.0f} = {AD5:.2f} ≤ 2 → D 區", 20, BLU, "middle", "bold")
    g.text(x+W/2, 530, f"R = {R5:.0f} tf；壓桿／拉桿／節點一次驗完", 17, MUTED, "middle")
    # 例④
    x = 545; ox = x+80; oy = 290
    hatch(g, ox, oy, 345, 110)
    g.text(ox+172, oy+68, "既有（硬固）混凝土", 18, INK, "middle", "bold", bg="#EEF1F5")
    g.rect(ox, oy-120, 345, 120, fill="#FFFFFF", stroke=INK, sw=2)
    g.text(ox+172, oy-72, "後澆混凝土", 18, INK, "middle", "bold")
    zz = [(ox+i*11.5, oy + (4 if i % 2 else -4)) for i in range(31)]
    g.poly(zz, ORG, 2.4)
    for k in range(5):
        xx = ox+45+k*63; g.line(xx, oy-85, xx, oy+80, BLU, 3.2)
    g.arrow(ox+345+50, oy-26, ox+345+6, oy-26, RED, 3.5, 15); g.text(ox+345+26, oy-40, "V_u", 20, RED, "middle", "bold")
    g.text(x+W/2, 462, f"V_u = {VU4:.0f} tf、A_c = 35 × 60 = {AC4:.0f} cm²", 19, INK, "middle")
    g.text(x+W/2, 496, "粗糙化 μ = 1.0 vs 未粗糙 μ = 0.6", 20, ORG, "middle", "bold")
    g.text(x+W/2, 530, "藍線：垂直穿過介面的 A_{vf}", 17, MUTED, "middle")
    # 扭力
    x = 1070; s = 3.3; sx = x + W/2 - BW*s/2; sy = 110
    g.rect(sx, sy, BW*s, H*s, fill="#E9EDF2", stroke=INK, sw=2.5)
    g.rect(sx+C_STIR*s, sy+C_STIR*s, X1*s, Y1*s, stroke=GRN, sw=2.6, dash="8 5")
    dimh(g, sx, sx+BW*s, sy+H*s+26, "35", MUTED, 16, up=False)
    dimv(g, sx-14, sy, sy+H*s, "70", MUTED, 16)
    g.text(sx+BW*s+16, sy+40, "A_{cp}：外緣", 17, INK); g.text(sx+BW*s+16, sy+H*s/2, "A_{oh}：箍筋中心線", 17, GRN, "start", "bold")
    g.text(x+W/2, 462, f"A_{{cp}} = {ACP:.0f} cm²、p_{{cp}} = {PCP:.0f} cm", 19, INK, "middle")
    g.text(x+W/2, 496, f"φT_{{th}} = {PTTH:.3f} t-m", 20, "#4B5563", "middle", "bold")
    g.text(x+W/2, 530, "35×70、f'_c = 280（沿用拼圖三）", 17, MUTED, "middle")
    g.save("figs/fig02_cases.svg")

# ───────── fig03 B 區 vs D 區 ─────────
def fig03():
    g = SVG(1600, 540)
    x0, x1, y0, hh = 100, 1500, 110, 140
    xs1, xs2, xp = 190, 1410, 700
    for a, b_, col in [(x0, xs1+hh, BBG), (xp-hh, xp+hh, BBG), (xs2-hh, x1, BBG), (xs1+hh, xp-hh, PBG), (xp+hh, xs2-hh, PBG)]:
        g.rect(a, y0, b_-a, hh, fill=col, stroke="none")
    g.rect(x0, y0, x1-x0, hh, stroke=INK, sw=2.5)
    for a, b_ in [(xs1+hh, None), (xp-hh, xp+hh), (xs2-hh, None)]:
        g.line(a, y0-10, a, y0+hh+10, BLU, 1.6, "6 5")
        if b_: g.line(b_, y0-10, b_, y0+hh+10, BLU, 1.6, "6 5")
    g.arrow(xp, y0-70, xp, y0-4, RED, 3.5, 16); g.text(xp+10, y0-46, "P", 22, RED, "start", "bold")
    pin(g, xs1, y0+hh); roller(g, xs2, y0+hh)
    for cx, t_ in [((x0+xs1+hh)/2, "D 區"), (xp, "D 區"), ((xs2-hh+x1)/2, "D 區")]:
        g.text(cx, y0+hh/2+9, t_, 24, BLU, "middle", "bold")
    for cx in [(xs1+hh+xp-hh)/2, (xp+hh+xs2-hh)/2]:
        g.text(cx, y0+hh/2+9, "B 區", 24, PUR, "middle", "bold")
    dimh(g, xp, xp+hh, y0-22, "≈ h", BLU, 18)
    dimh(g, xs1, xs1+hh, y0+hh+70, "≈ h", BLU, 18, up=False)
    # 應變分佈
    by = 360; bh = 130
    for cx, lin, col, t1, t2 in [(1040, True, PUR, "B 區：應變直線分佈", "平截面假設成立 → 梁理論、V_c + V_s"),
                                  (470, False, BLU, "D 區：應變非線性", "平截面假設失效 → 改用 STM")]:
        g.line(cx, by, cx, by+bh, INK, 2)
        if lin: pts = [(cx+70, by), (cx-50, by+bh)]
        else: pts = [(cx+18*math.sin(math.pi*u)+70*(1-u)**3 - 60*u**2, by+bh*u) for u in [i/20 for i in range(21)]]
        g.poly([(cx, by)] + pts + [(cx, by+bh)], color=col, sw=2.5, fill=col, closed=True, op=0.18) if lin else g.poly(pts, color=col, sw=3)
        if not lin:
            for (px, py) in pts[::4]: g.line(cx, py, px, py, col, 1.2)
        g.text(cx+120, by+48, t1, 22, col, "start", "bold"); g.text(cx+120, by+86, t2, 18, INK)
    g.save("figs/fig03_bd.svg")

# ───────── fig04 a/d 改變力流 ─────────
def fig04():
    g = SVG(1600, 470)
    specs = [(0.7, BLU, "a/d ≈ 0.7｜拱作用", "壓桿直達支承"), (2.0, ORG, "a/d ≈ 2.0｜過渡", "兩者並存"), (4.0, PUR, "a/d ≈ 4.0｜桁架類比", "靠箍筋接力")]
    for i, (ad, col, lab, note) in enumerate(specs):
        x = 30 + i*525; bw_, bh = 440, 170; bx, by = x+20, 110; dd = 150
        g.rect(bx, by, bw_, bh, fill="#FFFFFF", stroke=INK, sw=2.5)
        xs = bx+25; xp = xs + ad*dd*0.6 if ad > 1 else xs + ad*dd*0.6
        a_px = ad*0.6*dd if ad <= 2 else 360
        xp = xs + a_px
        g.arrow(xp, by-62, xp, by-3, RED, 3, 14); g.text(xp, by-70, "P", 20, RED, "middle", "bold")
        g.line(xs, by-28, xp, by-28, MUTED, 1.3); g.text((xs+xp)/2, by-34, "a", 18, MUTED, "middle", "bold", italic=True)
        ty = by+bh-22
        g.line(bx+12, ty, bx+bw_-12, ty, RED, 3.5)
        if ad < 1:
            band(g, (xp, by+4), (xs, ty), 34, 44, SBAND); g.line(xp, by+4, xs, ty, BLU, 4)
        elif ad < 3:
            g.line(xp, by+4, xs, ty, BLU, 3.5, "10 7")
            for k in range(3): xx = xs+45+k*70; g.line(xx, by+18, xx, ty, RED, 2.6)
        else:
            n = 5; st = (xp-xs)/n
            for k in range(n):
                xa = xs + k*st; g.line(xa+st, by+18, xa+st, ty, RED, 2.6); g.line(xa+st, by+18, xa, ty, BLU, 2.6)
        g.text(bx+bw_/2+40, by+bh/2+4, note, 19, col, "middle", "bold", bg="#FFFFFF")
        pin(g, xs, by+bh, 0.9); roller(g, bx+bw_-25, by+bh, 0.9)
        tag(g, bx+bw_/2, by+bh+58, lab, col, 20, center=True)
    g.text(800, 440, "a 越短 → 壓桿越陡、越直接 → 同樣的 P 所需的斜壓力越小 → 強度反而越高", 22, INK, "middle", "bold")
    g.save("figs/fig04_ad3.svg")

# ───────── fig05 強度 vs a/d ─────────
def fig05():
    g = SVG(1600, 520)
    X0, Y0, Wd, Hd = 130, 450, 860, 380
    xm, ym = 6.0, 5.0
    X = lambda v: X0 + v/xm*Wd; Y = lambda v: Y0 - v/ym*Hd
    g.rect(X(0), Y(ym), X(2.0)-X(0), Hd, fill=BBG, stroke="none")
    g.rect(X(2.0), Y(ym), X(2.5)-X(2.0), Hd, fill=OBG, stroke="none")
    g.rect(X(2.5), Y(ym), X(xm)-X(2.5), Hd, fill=PBG, stroke="none")
    for v in range(1, 6): g.line(X0, Y(v), X0+Wd, Y(v), GRID, 1); g.text(X0-12, Y(v)+6, str(v), 16, MUTED, "end")
    for v in range(0, 7): g.text(X(v), Y0+28, str(v), 16, MUTED, "middle")
    g.arrow(X0, Y0, X0+Wd+20, Y0, INK, 2, 12); g.arrow(X0, Y0, X0, Y(ym)-20, INK, 2, 12)
    g.text(X0+Wd+30, Y0+8, "a/d", 20, INK, "start", "bold")
    g.text(X0+8, Y(ym)-20, "剪力強度（相對值，示意）", 17, MUTED)
    f = lambda v: 1 + 3.7*((2.5-v)/2)**2 if v < 2.5 else 1.0
    g.poly([(X(v), Y(f(v))) for v in [0.5+i*0.05 for i in range(111)]], INK, 3.5)
    g.text(X(1.0), Y(4.6), "拱作用區", 21, BLU, "middle", "bold"); g.text(X(2.25), Y(4.6), "過渡", 18, ORG, "middle", "bold")
    g.text(X(4.2), Y(4.6), "桁架區（趨於定值）", 21, PUR, "middle", "bold")
    v5 = AD5; g.circle(X(v5), Y(f(v5)), 9, fill=BLU)
    g.text(X(v5)+16, Y(f(v5))-8, f"例⑤ a/d = {AD5:.2f}", 18, BLU, "start", "bold", bg="#FFFFFF")
    # 右側
    cx = 1040
    card(g, cx, 70, 530, 175, fill=RBG, stroke="#EBB4AE")
    g.text(cx+24, 112, "用桁架類比算深梁", 22, RED, "start", "bold")
    g.text(cx+24, 152, "⇒ 低估 2 ~ 4 倍：配出一堆無效箍筋", 19, INK)
    g.text(cx+24, 188, "（力根本不走箍筋，而是走斜壓桿）", 17, MUTED)
    card(g, cx, 270, 530, 175, fill=OBG, stroke="#EFC39F")
    g.text(cx+24, 312, "用 STM 算細長梁", 22, ORG, "start", "bold")
    g.text(cx+24, 352, "⇒ 高估且不安全", 19, INK)
    g.text(cx+24, 388, "（斜壓桿太平、會被斜裂縫切斷）", 17, MUTED)
    g.save("figs/fig05_curve.svg")

# ───────── fig06 STM 三元件 ─────────
def fig06():
    g = SVG(1600, 540)
    bx, by, bw_, bh = 60, 110, 900, 360
    g.rect(bx, by, bw_, bh, fill="#FFFFFF", stroke=INK, sw=2.5)
    xs1, xs2, xp = bx+90, bx+bw_-90, bx+bw_/2
    yt, yb = by+30, by+bh-30
    bottle(g, (xp-40, yt), (xs1, yb), 46, 110); bottle(g, (xp+40, yt), (xs2, yb), 46, 110)
    band(g, (xp-40, yt), (xp+40, yt), 40, 40)
    g.line(xp-40, yt, xs1, yb, BLU, 4); g.line(xp+40, yt, xs2, yb, BLU, 4); g.line(xp-40, yt, xp+40, yt, BLU, 4)
    g.rect(bx+20, yb-20, bw_-40, 40, fill=RBG, stroke="none"); g.line(bx+20, yb, bx+bw_-20, yb, RED, 5)
    for (nx, ny) in [(xp-40, yt), (xp+40, yt), (xs1, yb), (xs2, yb)]: g.circle(nx, ny, 12, fill=ORG)
    g.arrow(xp, by-80, xp, by-4, RED, 3.5, 16); g.text(xp+12, by-50, "P_u", 22, RED, "start", "bold")
    pin(g, xs1, by+bh); roller(g, xs2, by+bh)
    g.text(xs1+120, by+180, "壓桿", 24, BLU, "start", "bold", bg="#FFFFFF")
    g.text(xp, yb+48, "拉桿（縱向鋼筋）", 22, RED, "middle", "bold", bg="#FFFFFF")
    g.text(xp+60, yt+10, "節點 CCC", 20, ORG, "start", "bold", bg="#FFFFFF")
    g.text(xs1+30, yb-30, "節點 CCT", 20, ORG, "start", "bold", bg="#FFFFFF")
    L = [("壓桿 Strut（C）", "混凝土斜壓力帶；中段會鼓成瓶形", BLU, BBG), ("拉桿 Tie（T）", "縱向鋼筋；要能在節點外錨定", RED, RBG), ("節點 Node（N）", "壓桿與拉桿交會的區域", ORG, OBG)]
    for i, (a, b_, col, bg) in enumerate(L):
        y = 40 + i*150; card(g, 1010, y, 560, 132, fill=bg, stroke=col)
        g.rect(1010, y, 10, 132, fill=col, stroke="none")
        g.text(1045, y+52, a, 25, col, "start", "bold"); g.text(1045, y+96, b_, 19, INK)
    g.text(1290, 522, "三種元件都用同一個 φ = 0.75", 20, INK, "middle", "bold")
    g.save("figs/fig06_stm.svg")

# ───────── fig07 壓桿 βs ─────────
def fig07():
    g = SVG(1600, 470)
    specs = [("稜柱形", "β_s = 1.0", "寬度一路不變（如上方壓力區）", TEAL, "prism"),
             ("瓶形＋橫向鋼筋", "β_s = 0.75", "橫筋撐住劈裂，仍可用", GRN, "bottle_r"),
             ("瓶形、無橫筋", "β_s = 0.60λ", "中段橫向拉力 → 縱向劈裂", ORG, "bottle"),
             ("拉力構材中的壓桿", "β_s = 0.40", "被拉力裂縫橫切，最弱", RED, "tens")]
    for i, (hd, bv, note, col, kind) in enumerate(specs):
        x = 20 + i*395; card(g, x, 20, 375, 430)
        g.text(x+187, 62, hd, 22, col, "middle", "bold")
        cx, y1, y2 = x+187, 95, 315
        if kind == "prism":
            g.rect(cx-38, y1, 76, y2-y1, fill=SBAND, stroke="none")
            for yy in range(y1+20, y2, 40): g.line(cx-38, yy, cx+38, yy, BLU, 1, "3 4")
        else:
            bottle(g, (cx, y1), (cx, y2), 60, 170)
            if kind == "bottle_r":
                for yy in range(y1+30, y2-10, 34): g.line(cx-95, yy, cx+95, yy, GRN, 2.6)
                for xx in (cx-55, cx+55): g.line(xx, y1+10, xx, y2-10, GRN, 2.6)
            if kind == "bottle":
                g.line(cx, y1+40, cx, y2-40, RED, 3, "10 6")
                g.arrow(cx-10, 205, cx-85, 205, RED, 2.4, 12); g.arrow(cx+10, 205, cx+85, 205, RED, 2.4, 12)
            if kind == "tens":
                for yy in (150, 200, 250):
                    g.poly([(cx-100, yy), (cx-50, yy+8), (cx, yy-6), (cx+50, yy+6), (cx+100, yy-4)], RED, 2.4)
        g.arrow(cx, y1-28+10, cx, y1+2, BLU, 3, 12); g.arrow(cx, y2+28-10, cx, y2-2, BLU, 3, 12)
        g.text(cx, 370, bv, 26, col, "middle", "bold"); g.text(cx, 412, note, 17, INK, "middle")
    g.save("figs/fig07_struts.svg")

# ───────── fig08 節點 βn ─────────
def fig08():
    g = SVG(1600, 460)
    specs = [("CCC", "三面受壓", "β_n = 1.0", GRN, ["C", "C", "C"]), ("CCT", "一根拉桿錨入", "β_n = 0.80", ORG, ["C", "C", "T"]), ("CTT", "兩根以上拉桿", "β_n = 0.60", RED, ["C", "T", "T"])]
    angs = [90, 215, 325]
    for i, (hd, sub, bv, col, kinds) in enumerate(specs):
        x = 30 + i*525; card(g, x, 20, 505, 420)
        g.text(x+252, 64, f"{hd}：{sub}", 24, col, "middle", "bold")
        cx, cy, r = x+252, 250, 44
        g.poly([(cx+r*math.cos(math.radians(a)), cy-r*math.sin(math.radians(a))) for a in range(30, 390, 60)], ORG, 2.5, fill=OBG, closed=True)
        for a, k in zip(angs, kinds):
            ca, sa = math.cos(math.radians(a)), -math.sin(math.radians(a))
            if k == "C":
                g.arrow(cx+ca*125, cy+sa*125, cx+ca*(r+6), cy+sa*(r+6), BLU, 5, 18)
                g.text(cx+ca*148, cy+sa*148+8, "C", 22, BLU, "middle", "bold")
            else:
                g.line(cx-ca*r*0.9, cy-sa*r*0.9, cx+ca*140, cy+sa*140, RED, 6)
                g.rect(cx-ca*r*1.05-6, cy-sa*r*1.05-6, 12, 12, fill=RED, stroke="none")
                g.arrow(cx+ca*100, cy+sa*100, cx+ca*145, cy+sa*145, RED, 3, 14)
                g.text(cx+ca*165, cy+sa*165+8, "T", 22, RED, "middle", "bold")
        g.text(cx, 400, bv, 28, col, "middle", "bold")
    g.save("figs/fig08_nodes.svg")

# ───────── fig09 拉桿錨定 ─────────
def fig09():
    g = SVG(1600, 540)
    th = math.radians(TH_DEG); c, sn = math.cos(th), math.sin(th)
    g.rect(40, 40, 880, 360, fill="#FFFFFF", stroke=INK, sw=2.5)
    xs, lb, wt, yb = 250, 160, 80, 400
    xl, xr, yt = xs-lb/2, xs+lb/2, yb-wt
    L = 330
    # 壓桿帶：上緣過 (xl, yt)，下緣過 (xr, yb)
    g.poly([(xl, yt), (xr, yb), (xr+L*c, yb-L*sn), (xl+L*c, yt-L*sn)], color="none", sw=0, fill=SBAND, closed=True, op=0.85)
    g.rect(40, yt, 880, wt, fill=RBG, stroke="none", op=0.8)
    xe = xr + wt/sn*c         # 壓桿下緣與拉桿帶上緣交點
    g.poly([(xl, yt), (xl, yb), (xr, yb), (xe, yt)], color=ORG, sw=2, fill="#F6C99E", closed=True, op=0.75)
    g.rect(xl, yt, lb, wt, fill="none", stroke=ORG, sw=2.4)
    g.line(xs, yb-wt/2, xs+(L+20)*c, yb-wt/2-(L+20)*sn, BLU, 3.5)
    g.line(62, yb-wt/2, 915, yb-wt/2, RED, 5); g.line(62, yb-wt/2, 62, yb-wt/2-70, RED, 5)
    xcrit = xr + (wt/2)/sn*c
    g.line(xcrit, 150, xcrit, yb+10, RED, 2, "8 5"); g.circle(xcrit, yb-wt/2, 9, fill=RED)
    g.text(xcrit+10, 144, "拉桿重心離開延伸節點區處（錨定起算點）", 19, RED, "start", "bold", bg="#FFFFFF")
    g.rect(xl, yb, lb, 14, fill="#6B7280", stroke="none"); pin(g, xs, yb+14)
    g.text(xs, yb-wt/2+6, "節點區", 17, ORG, "middle", "bold", bg="#FFFFFF")
    g.text(xe+40, yt-8, "延伸節點區", 17, ORG, "start", "bold", bg="#FFFFFF")
    g.text(xs+170*c+40, yb-wt/2-170*sn+10, "壓桿", 20, BLU, "start", "bold", bg="#FFFFFF")
    g.text(700, yb-wt/2+30, "拉桿（縱筋）", 18, RED, "middle", "bold")
    g.line(62, yb+62, xcrit, yb+62, GRN, 2.2); g.line(62, yb+52, 62, yb+72, GRN, 2); g.line(xcrit, yb+52, xcrit, yb+72, GRN, 2)
    g.text((62+xcrit)/2+60, yb+100, "可用錨定長度 ≥ ℓ_d（彎鉤則 ℓ_{dh}）", 19, GRN, "middle", "bold")
    cx = 970
    cards_ = [("起算點不是支承中心", "錨定長度從拉桿重心「離開延伸節點區」處", "往梁端量；不是從支承面或節點中心", RED, RBG),
              ("長度不夠怎麼辦", "加彎鉤（ℓ_{dh}）、錨定板／機械式錨頭，", "或加長支承板讓節點區變大", GRN, GBG),
              ("拉桿強度", "φF_{nt} = φ A_{ts} f_y（φ = 0.75）", f"鋼筋要分布在高度 w_t 內（例⑤ w_t = {WT:.0f} cm）", ORG, OBG)]
    for i, (hd, l1, l2, col, bg) in enumerate(cards_):
        y = 30 + i*165; card(g, cx, y, 610, 148, fill=bg, stroke=col)
        g.text(cx+24, y+44, hd, 22, col, "start", "bold"); g.text(cx+24, y+86, l1, 18, INK); g.text(cx+24, y+120, l2, 18, INK)
    g.save("figs/fig09_anchor.svg")

# ───────── fig10 例⑤ 建模 ─────────
def fig10():
    g = SVG(1200, 680)
    s = 2.55; ov = 30; Lt = L5 + 2*ov
    bx, by = 120, 120
    Wd, Hd = Lt*s, H5*s
    g.rect(bx, by, Wd, Hd, fill="#FFFFFF", stroke=INK, sw=2.5)
    X = lambda cm: bx + cm*s; Yd = lambda cm: by + cm*s
    xs1, xs2, xp = X(ov), X(ov+L5), X(ov+A5)
    ytie = Yd(H5 - WT/2); ytop = Yd(WTOP/2)
    n1, n2 = (xp - LB_P/4*s, ytop), (xp + LB_P/4*s, ytop)
    # 帶狀
    g.rect(bx+6, Yd(H5-WT), Wd-12, WT*s, fill=RBG, stroke="none")
    g.rect(n1[0], Yd(0), n2[0]-n1[0], WTOP*s, fill=SBAND, stroke="none", op=0.9)
    bottle(g, n1, (xs1, ytie), WS_T*s, WS_B*s*1.6, op=0.55); bottle(g, n2, (xs2, ytie), WS_T*s, WS_B*s*1.6, op=0.55)
    band(g, n1, (xs1, ytie), WS_T*s, WS_B*s, SBAND, 0.9); band(g, n2, (xs2, ytie), WS_T*s, WS_B*s, SBAND, 0.9)
    g.line(n1[0], n1[1], xs1, ytie, BLU, 3.5); g.line(n2[0], n2[1], xs2, ytie, BLU, 3.5); g.line(n1[0], n1[1], n2[0], n2[1], BLU, 3.5)
    g.line(bx+6, ytie, bx+Wd-6, ytie, RED, 4.5)
    for p in (n1, n2, (xs1, ytie), (xs2, ytie)): g.circle(p[0], p[1], 9, fill=ORG)
    # 承壓板與載重
    g.rect(xp-LB_P/2*s, by-12, LB_P*s, 12, fill="#6B7280", stroke="none")
    for xx in (xp-LB_P/4*s, xp+LB_P/4*s): g.arrow(xx, by-72, xx, by-14, RED, 3, 13)
    g.text(xp, by-82, f"P_u = {PU5:.0f} tf（拆成兩個 {PU5/2:.0f}，作用在承壓板 1/4 點）", 18, RED, "middle", "bold")
    for xx, f_ in ((xs1, pin), (xs2, roller)):
        g.rect(xx-LB_S/2*s, by+Hd, LB_S*s, 12, fill="#6B7280", stroke="none"); f_(g, xx, by+Hd+12, 0.9)
    # 尺寸
    dimh(g, xs1, n1[0], by+Hd+80, f"{A5-LB_P/4:.0f}（= a − 板寬/4）", BLU, 17, up=False)
    dimh(g, xs1, xp, by+Hd+135, f"a = {A5:.0f}", MUTED, 17, up=False)
    dimv(g, bx-16, by, by+Hd, f"h = {H5:.0f}", MUTED, 17)
    dimv(g, bx+Wd+30, ytop, ytie, f"z = {Z5:.1f}", PUR, 18, "right")
    g.arc(xs1, ytie, 70, 0, TH_DEG, BLU, 2); g.text(xs1+80, ytie-22, f"θ = {TH_DEG:.1f}°", 19, BLU, "start", "bold", bg="#FFFFFF")
    g.text(xp, ytop+WTOP*s+30, f"水平壓桿 C = {T5:.1f} tf（w = {WTOP:.1f}）", 17, BLU, "middle", "bold", bg="#FFFFFF")
    g.text(xp, ytie-18, f"拉桿 T = {T5:.1f} tf（w_t = {WT:.0f}）", 18, RED, "middle", "bold", bg="#FFFFFF")
    mx, my = (n1[0]+xs1)/2, (n1[1]+ytie)/2
    g.text(mx-20, my-20, f"F = {F5:.1f} tf", 19, BLU, "end", "bold", bg="#FFFFFF")
    g.save("figs/fig10_ex5.svg")

# ───────── fig11 例⑤ 使用率 ─────────
def fig11():
    g = SVG(1600, 520)
    rows = [("斜壓桿・下端（β_s 0.75 vs β_n 0.80 取小）", F5, CAP_SB, BLU),
            ("斜壓桿・上端（β_s 0.75 控制）", F5, CAP_ST, BLU),
            ("支承節點承壓面（CCT，β_n 0.80）", R5, CAP_NS, ORG),
            ("載重節點承壓面（CCC，β_n 1.0）", PU5, CAP_NP, ORG),
            (f"拉桿 {N25}-D25（A_{{ts}} = {AS5:.2f}）", T5, CAP_T, RED),
            ("深梁總上限 φ2.65√f'_c b d", R5, PVLIM5, "#4B5563")]
    X0, W = 560, 760
    for i, (lab, dem, cap, col) in enumerate(rows):
        y = 40 + i*75; u = dem/cap
        g.text(X0-20, y+30, lab, 19, INK, "end", "bold")
        g.rect(X0, y+8, W, 32, fill="#E8EBEF", stroke="none", rx=6)
        g.rect(X0, y+8, W*u, 32, fill=col, stroke="none", rx=6)
        g.text(X0+W*u+12, y+32, f"{u*100:.1f}%", 19, col, "start", "bold")
        g.text(X0+W+120, y+32, f"{dem:.1f} / {cap:.1f}", 17, MUTED, "start")
    g.line(X0+W, 30, X0+W, 490, RED, 2, "6 5"); g.text(X0+W, 505, "100%", 16, RED, "middle", "bold")
    g.save("figs/fig11_ex5chk.svg")

# ───────── fig12 上限同一精神 ─────────
def fig12():
    g = SVG(1600, 470)
    card(g, 20, 20, 760, 430); card(g, 820, 20, 760, 430)
    g.text(400, 66, "桁架類比：V_s ≤ 4V_c → V_n ≤ 5V_c", 23, PUR, "middle", "bold")
    g.text(1200, 66, "深梁：V_n ≤ 2.65√f'_c b_w d", 23, BLU, "middle", "bold")
    for x0, col, segs in [(80, PUR, [("V_c", 1, "#A89BD6"), ("4V_c", 4, PUR)]), (880, BLU, [("2.65√f'_c b_w d", 5, BLU)])]:
        xx = x0; unit = 124
        for lab, n, c in segs:
            g.rect(xx, 140, n*unit, 70, fill=c, stroke="#FFFFFF", sw=2)
            g.text(xx+n*unit/2, 184, lab, 21, "#FFFFFF", "middle", "bold"); xx += n*unit
    g.text(400, 262, "5 × 0.53 = 2.65", 30, INK, "middle", "bold")
    g.text(1200, 262, f"基準斷面：5V_c = {VC5:.2f} tf", 22, INK, "middle", "bold")
    g.text(400, 310, "同一個係數：兩者都是「混凝土斜壓桿壓碎」的天花板", 19, INK, "middle")
    g.text(1200, 310, f"例⑤：φV_{{n,max}} = {PVLIM5:.1f} tf ≥ R = {R5:.0f}（{U_LIM:.1f}%）", 19, INK, "middle")
    g.text(400, 380, "超過 → 加鋼筋無效，只能加大斷面或 f'_c", 19, RED, "middle", "bold")
    g.text(1200, 380, "STM 通過了，也要回頭看這條總上限", 19, RED, "middle", "bold")
    g.save("figs/fig12_limit.svg")

# ───────── fig13 剪力摩擦機制 ─────────
def fig13():
    g = SVG(1600, 520)
    labels = [("① 介面上有滑動需求", "V_u 想讓兩塊沿介面錯動"), ("② 鋸齒爬升 ⇒ 張開 δ", "粗糙面錯動時必然互相頂開（dilatancy）"), ("③ 鋼筋降伏 ⇒ 夾緊力", "張開把 A_{vf} 拉到降伏 → A_{vf} f_y 夾緊介面")]
    for i, (hd, sub) in enumerate(labels):
        x = 20 + i*525; card(g, x, 20, 505, 480)
        g.text(x+252, 64, hd, 23, ORG if i < 2 else BLU, "middle", "bold")
        cx, cy = x+252, 250
        dy = 0 if i == 0 else -16
        dx = 0 if i == 0 else 14
        # 下塊（固定）與上塊
        g.rect(cx-190, cy, 380, 110, fill="#EEF1F5", stroke=INK, sw=2)
        teeth = [(cx-190+k*20, cy + (0 if k % 2 == 0 else -12)) for k in range(20)]
        g.rect(cx-190+dx, cy-110+dy, 380, 110, fill="#FFFFFF", stroke=INK, sw=2)
        g.poly(teeth, ORG, 2.4)
        g.poly([(px+dx+10, py+dy) for px, py in teeth[:-1]], ORG, 2.4, dash="5 3") if i > 0 else None
        if i == 0: g.arrow(cx+250, cy-55, cx+196, cy-55, RED, 3.5, 15); g.arrow(cx-250, cy+55, cx-196, cy+55, RED, 3.5, 15)
        if i >= 1:
            g.arrow(cx+215, cy+10, cx+215, cy-40, RED, 3, 13); g.text(cx+228, cy-12, "δ", 22, RED, "start", "bold")
        if i == 2:
            for xx in (cx-110, cx, cx+110):
                g.line(xx, cy+80, xx, cy-80+dy, BLU, 4)
                g.arrow(xx-26, cy-120, xx-26, cy-72, BLU, 2.4, 11); g.arrow(xx-26, cy+130, xx-26, cy+82, BLU, 2.4, 11)
            g.text(cx-190, cy-135, "夾緊 A_{vf} f_y", 19, BLU, "start", "bold")
        g.text(cx, 440, sub, 18, INK, "middle")
    g.save("figs/fig13_sfmech.svg")

# ───────── fig14 μ 四種介面 ─────────
def fig14():
    g = SVG(1600, 440)
    specs = [("單體澆置", "μ = 1.4λ", "最好：沒有介面", GRN, "mono"), ("硬固面粗糙化 ≥ 6 mm", "μ = 1.0λ", "考題最常出現", ORG, "rough"),
             ("硬固面未粗糙化", "μ = 0.6λ", "最差：幾乎沒有齒", RED, "smooth"), ("混凝土＋輥軋鋼板（剪力釘）", "μ = 0.7λ", "組合構材", BLU, "steel")]
    for i, (hd, mu, note, col, kind) in enumerate(specs):
        x = 20 + i*395; card(g, x, 20, 375, 400)
        g.text(x+187, 62, hd, 20, col, "middle", "bold")
        cx, cy = x+187, 200; w = 280
        if kind == "mono":
            g.rect(cx-w/2, cy-80, w, 160, fill="#EEF1F5", stroke=INK, sw=2)
            g.line(cx-w/2, cy, cx+w/2, cy, MUTED, 1.4, "8 6"); g.text(cx, cy-10, "（潛在滑動面）", 16, MUTED, "middle")
        else:
            if kind == "steel":
                g.rect(cx-w/2, cy, w, 22, fill="#6B7280", stroke=INK, sw=2)
                for k in range(4): xx = cx-w/2+40+k*67; g.line(xx, cy, xx, cy-50, INK, 5); g.rect(xx-11, cy-56, 22, 8, fill=INK, stroke="none")
                g.rect(cx-w/2, cy-80, w, 80, fill="#FFFFFF", stroke=INK, sw=2)
                for k in range(4): xx = cx-w/2+40+k*67; g.line(xx, cy, xx, cy-50, INK, 5); g.rect(xx-11, cy-56, 22, 8, fill=INK, stroke="none")
            else:
                hatch(g, cx-w/2, cy, w, 80); g.rect(cx-w/2, cy-80, w, 80, fill="#FFFFFF", stroke=INK, sw=2)
                if kind == "rough": g.poly([(cx-w/2+k*14, cy + (0 if k % 2 == 0 else -10)) for k in range(21)], col, 2.6)
                else: g.line(cx-w/2, cy, cx+w/2, cy, col, 2.6)
        g.text(cx, 340, mu, 30, col, "middle", "bold"); g.text(cx, 385, note, 18, INK, "middle")
    g.save("figs/fig14_mu.svg")

# ───────── fig15 例④ 粗糙與否 ─────────
def fig15():
    g = SVG(1600, 470)
    X0, W, vmax = 60, 900, 36.0
    for i, (lab, v, col, res) in enumerate([("粗糙化 μ = 1.0", AVF_R, GRN, f"{AVF_R:.2f} cm² → {N19}-D19（{AVF_USE:.2f}）"),
                                            ("未粗糙 μ = 0.6", AVF_S, RED, f"{AVF_S:.2f} cm² → {N19S}-D19（多 {MORE4:.1f}%）")]):
        y = 40 + i*140
        g.text(X0, y+26, lab, 22, INK, "start", "bold")
        g.rect(X0, y+44, W, 50, fill="#E8EBEF", stroke="none", rx=8)
        g.rect(X0, y+44, W*v/vmax, 50, fill=col, stroke="none", rx=8)
        g.text(X0+W*v/vmax+16, y+78, res, 21, col, "start", "bold")
    # 右：介面平面配筋
    cx, cy, s = 1250, 160, 5.2
    for k, (n, col, yoff) in enumerate([(N19, GRN, 0), (N19S, RED, 170)]):
        x0, y0 = cx - 60*s/2, 40 + yoff
        g.rect(x0, y0, 60*s, 35*s*0.55, fill="#EEF1F5", stroke=INK, sw=2)
        for j in range(n):
            g.circle(x0 + 20 + j*(60*s-40)/(n-1), y0 + 35*s*0.55/2, 9, fill=col, stroke="#FFFFFF")
    g.text(cx, 400, "介面平面（35 × 60）上的 A_{vf} 根數", 18, MUTED, "middle")
    g.rect(60, 330, 900, 100, fill=OBG, stroke="#EFC39F", sw=1.4, rx=12)
    g.text(80, 372, f"上限：φV_{{n,max}} = 0.75 × {VLIM_UNIT:.0f} × {AC4:.0f} = {PVN4_MAX:.2f} tf ≥ V_u = {VU4:.2f}（{USE4:.1f}%）", 20, ORG, "start", "bold")
    g.text(80, 410, "上限不夠時，加鋼筋也沒用——只能加大介面面積 A_c", 18, INK)
    g.save("figs/fig15_ex4.svg")

# ───────── fig16 A_vf 不是箍筋 ─────────
def fig16():
    g = SVG(1600, 480)
    card(g, 20, 20, 760, 440, fill=GBG, stroke="#A7D1B5"); card(g, 820, 20, 760, 440, fill=RBG, stroke="#EBB4AE")
    g.text(400, 64, "✓ A_{vf}：垂直穿過「介面」", 24, GRN, "middle", "bold")
    g.text(1200, 64, "× 拿梁箍筋 A_v 來代", 24, RED, "middle", "bold")
    # 左：牛腿式 — 柱面垂直介面
    hatch(g, 110, 100, 150, 320)
    g.rect(260, 180, 330, 150, fill="#FFFFFF", stroke=INK, sw=2)
    g.line(260, 100, 260, 420, ORG, 3.5, "10 6"); g.text(268, 118, "介面", 18, ORG, "start", "bold")
    for yy in (215, 255, 295): g.line(150, yy, 560, yy, BLU, 4)
    g.arrow(520, 110, 520, 176, RED, 3.5, 15); g.text(530, 140, "V_u", 20, RED, "start", "bold")
    g.text(420, 380, "介面鉛直 → A_{vf} 水平穿過", 19, INK, "middle", "bold")
    g.text(420, 418, "兩側都要錨定（ℓ_d）", 17, MUTED, "middle")
    # 右：梁箍筋平行介面
    g.rect(920, 150, 560, 170, fill="#FFFFFF", stroke=INK, sw=2)
    for k in range(7): xx = 960+k*80; g.line(xx, 165, xx, 305, BLU, 3)
    g.line(1200, 120, 1200, 350, RED, 3.5, "10 6"); g.text(1210, 118, "鉛直介面", 18, RED, "start", "bold")
    g.text(1200, 400, "箍筋與鉛直介面平行 → 完全沒有夾緊作用", 19, INK, "middle", "bold")
    g.text(1200, 436, "（只有水平施工縫時，箍筋才剛好垂直穿過介面）", 17, MUTED, "middle")
    g.save("figs/fig16_avf.svg")

# ───────── fig17 扭力門檻 ─────────
def fig17():
    g = SVG(1600, 520)
    s = 5.4; sx, sy = 70, 70
    g.rect(sx, sy, BW*s, H*s, fill="#DCE3EC", stroke=INK, sw=2.5)
    g.rect(sx+C_STIR*s, sy+C_STIR*s, X1*s, Y1*s, fill=GBG, stroke=GRN, sw=3)
    for (px, py) in [(sx+C_STIR*s, sy+C_STIR*s), (sx+(C_STIR+X1)*s, sy+C_STIR*s), (sx+C_STIR*s, sy+(C_STIR+Y1)*s), (sx+(C_STIR+X1)*s, sy+(C_STIR+Y1)*s)]:
        g.circle(px, py, 8, fill=INK, stroke=INK)
    g.text(sx+BW*s/2, sy+H*s/2-10, "A_{oh}", 24, GRN, "middle", "bold"); g.text(sx+BW*s/2, sy+H*s/2+24, f"{X1:.0f}×{Y1:.0f}", 18, GRN, "middle")
    g.text(sx+BW*s+18, sy+22, "A_{cp}（外緣）", 19, INK, "start", "bold")
    dimh(g, sx, sx+BW*s, sy+H*s+30, "35", MUTED, 17, up=False); dimv(g, sx-16, sy, sy+H*s, "70", MUTED, 17)
    cx = 420
    rows = [("門檻判定（能不能忽略）", f"A_{{cp}} = 35×70 = {ACP:.0f}、p_{{cp}} = 2(35+70) = {PCP:.0f}", f"φT_{{th}} = {PTTH:.3f} t-m", "#4B5563", PANEL),
            ("超過門檻才進入扭力設計", f"A_{{oh}} = {X1:.0f}×{Y1:.0f} = {AOH:.0f}、p_h = {PH:.0f}、A_o = 0.85A_{{oh}} = {AO:.0f}", "閉合箍＋縱筋", GRN, GBG),
            ("誤把 A_{oh}、p_h 代進門檻", f"(A_{{oh}}²/p_h) 只有 (A_{{cp}}²/p_{{cp}}) 的 {100-DROP_T:.1f}%", f"門檻被算成 {PTTH_WRONG:.3f}（低 {DROP_T:.1f}%）", RED, RBG)]
    for i, (hd, a, b_, col, bg) in enumerate(rows):
        y = 40 + i*140; card(g, cx, y, 1150, 122, fill=bg, stroke=col)
        g.rect(cx, y, 10, 122, fill=col, stroke="none")
        g.text(cx+34, y+44, hd, 22, col, "start", "bold"); g.text(cx+34, y+88, a, 19, INK)
        g.text(cx+1130, y+44, b_, 21, col, "end", "bold")
    g.text(cx+575, 490, f"門檻 = ¼ × 開裂扭矩：φ × ¼ × 1.06√f'_c A_{{cp}}²/p_{{cp}} = 0.75 × ¼ × {TCR:.2f} = {PTTH:.3f} t-m", 19, INK, "middle", "bold")
    g.save("figs/fig17_torsion.svg")

# ───────── fig18 識別流程圖 ─────────
def fig18():
    g = SVG(1600, 640)
    def box(cx, cy, w, h, t1, t2, col, bg):
        g.rect(cx-w/2, cy-h/2, w, h, fill=bg, stroke=col, sw=2.4, rx=12)
        g.text(cx, cy-4 if t2 else cy+8, t1, 20, col, "middle", "bold")
        if t2: g.text(cx, cy+26, t2, 16, INK, "middle")
    box(170, 70, 280, 80, "讀題：幾何＋載重位置", "有沒有介面？a、d、h？", INK, PANEL)
    g.arrow(310, 70, 380, 70, INK, 2.6, 12)
    diamond(g, 560, 70, 175, 62, ORG, OBG); g.text(560, 64, "既有滑動介面？", 20, ORG, "middle", "bold"); g.text(560, 90, "施工縫／新舊／預鑄", 15, INK, "middle")
    g.arrow(560, 132, 560, 190, INK, 2.6, 12); g.text(572, 168, "是", 18, ORG, "start", "bold")
    box(560, 240, 330, 96, "A_{vf} = V_u /(φ μ f_y)", "μ：1.4／1.0／0.6／0.7（× λ）", ORG, OBG)
    g.arrow(560, 288, 560, 340, INK, 2.6, 12)
    box(560, 385, 330, 86, "檢核 V_n 上限（× A_c）", "min(0.2f'_c, 34+0.08f'_c, 112)", ORG, OBG)
    g.arrow(560, 428, 560, 480, INK, 2.6, 12)
    box(560, 520, 330, 76, "A_{vf} 垂直介面、兩側錨定", "有淨拉力另加鋼筋", ORG, OBG)
    g.arrow(735, 70, 815, 70, INK, 2.6, 12); g.text(775, 58, "否", 18, MUTED, "middle", "bold")
    diamond(g, 1000, 70, 185, 62, BLU, BBG); g.text(1000, 64, "a/d ≤ 2 或 D 區？", 20, BLU, "middle", "bold"); g.text(1000, 90, "深梁／牛腿／樁帽", 15, INK, "middle")
    g.arrow(1000, 132, 1000, 190, INK, 2.6, 12); g.text(1012, 168, "是", 18, BLU, "start", "bold")
    box(1000, 235, 350, 86, "畫桁架：定 z、θ（≥ 25°）", "節點平衡 → F（壓桿）、T（拉桿）", BLU, BBG)
    g.arrow(1000, 278, 1000, 326, INK, 2.6, 12)
    box(1000, 370, 350, 86, "壓桿 β_s／節點 β_n／拉桿 A_{ts}", "f_{ce} = 0.85βf'_c；φ = 0.75", BLU, BBG)
    g.arrow(1000, 413, 1000, 460, INK, 2.6, 12)
    box(1000, 505, 350, 86, "拉桿錨定＋深梁總上限", "V_u ≤ φ2.65√f'_c b_w d", BLU, BBG)
    g.arrow(1185, 70, 1265, 70, INK, 2.6, 12); g.text(1225, 58, "否", 18, MUTED, "middle", "bold")
    box(1420, 70, 300, 80, "桁架類比 V_c + V_s", "→ 拼圖三 四道關卡", PUR, PBG)
    g.line(1420, 110, 1420, 200, INK, 2.6); g.arrow(1420, 200, 1420, 206, INK, 2.6, 12)
    diamond(g, 1420, 270, 155, 62, "#4B5563", PANEL); g.text(1420, 264, "有 T_u？", 20, "#4B5563", "middle", "bold"); g.text(1420, 290, "T_u 與 φT_{th} 比", 15, INK, "middle")
    g.arrow(1420, 332, 1420, 380, INK, 2.6, 12); g.text(1432, 362, "超過", 16, RED, "start", "bold")
    box(1420, 425, 300, 86, "扭力設計", "改用 A_{oh}、A_o、p_h", GRN, GBG)
    g.text(1420, 520, "未超過 → 忽略扭力", 18, MUTED, "middle", "bold")
    g.text(800, 615, "判斷順序：先找介面 → 再看 a/d → 都不是才走 V_c + V_s；扭力門檻在任何一條路上都要先比", 20, INK, "middle", "bold")
    g.save("figs/fig18_flow.svg")

for f in [fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10, fig11, fig12, fig13, fig14, fig15, fig16, fig17, fig18]: f()
print("figs ok")
