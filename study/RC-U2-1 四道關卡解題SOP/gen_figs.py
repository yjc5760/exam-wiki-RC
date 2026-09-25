import math
from svglib import SVG, INK, MUTED, GRID, PANEL, measure
from params import *
RED, GRN, ORG, BLU, PUR, GLD, TEAL = "#C0392B", "#1E8449", "#B9540F", "#2F54C8", "#6D4BC2", "#B7791F", "#2E7D6B"
RBG, GBG, OBG, BBG, PBG = "#FBECEA", "#E6F2EA", "#FDF1E7", "#EEF2FB", "#F1EDFA"
HATCH = "#9AA3AE"
def f2(v): return f"{v+1e-9:.2f}"
def f1(v): return f"{v+1e-9:.1f}"
def pin(g, x, y, sc=1.0):
    g.poly([(x, y), (x-16*sc, y+26*sc), (x+16*sc, y+26*sc)], color=INK, sw=2.2, fill="#FFFFFF", closed=True)
    g.line(x-26*sc, y+26*sc, x+26*sc, y+26*sc, INK, 2)
    for i in range(5): g.line(x-22*sc+i*10*sc, y+26*sc, x-30*sc+i*10*sc, y+36*sc, INK, 1.3)
def udl(g, x1, x2, y, n=10, L=28, col=RED):
    g.line(x1, y-L, x2, y-L, col, 2)
    for i in range(n+1):
        x = x1 + (x2-x1)*i/n; g.arrow(x, y-L, x, y-2, col, 1.8, 9)
def hatch(g, x, y, w, h, step=16):
    g.rect(x, y, w, h, fill="#EEF1F5", stroke=INK, sw=2)
    k = -h
    while k < w:
        xa, ya = x+max(k,0), y+h-max(0,-k)
        xb, yb = x+min(k+h, w), y+h-(min(k+h,w)-k)
        g.line(xa, ya, xb, yb, HATCH, 0.9); k += step
def tag(g, x, y, txt, col, size=17, fg="#FFFFFF"):
    w = measure(txt, size, True) + 26
    g.rect(x, y, w, size+14, fill=col, stroke="none", rx=(size+14)/2)
    g.text(x+w/2, y+size+3, txt, size, fg, "middle", "bold"); return w
def card(g, x, y, w, h, fill=PANEL, stroke="#D5DAE1"):
    g.rect(x, y, w, h, fill=fill, stroke=stroke, sw=1.4, rx=14)

# ───────── fig01 四道關卡地圖 ─────────
def fig01():
    g = SVG(1600, 590)
    G = [("關卡 1", "V_u 取在哪？", "d 偏移能不能用", "→ 設計剪力 V_u", RED, RBG),
         ("關卡 2", "V_c 用哪張臉？", "簡化／詳細／軸壓／軸拉／耐震", "→ 混凝土貢獻 V_c", BLU, BBG),
         ("關卡 3", "V_s 落在哪一段？", "V_s 與 2V_c、4V_c 比", "→ s_{max}、斷面夠不夠", ORG, OBG),
         ("關卡 4", "間距 s 取多少？", "四取小 + 沿梁長分區", "→ D13@s 配置", GRN, GBG)]
    w, gap, y0 = 340, 52, 70
    for i, (a, b, c, d, col, bg) in enumerate(G):
        x = 40 + i*(w+gap)
        g.rect(x, y0, w, 300, fill=bg, stroke=col, sw=2.5, rx=18)
        g.rect(x, y0, w, 58, fill=col, stroke="none", rx=18); g.rect(x, y0+30, w, 28, fill=col, stroke="none")
        g.text(x+w/2, y0+40, a, 26, "#FFFFFF", "middle", "bold")
        g.text(x+w/2, y0+118, b, 27, col, "middle", "bold")
        g.text(x+w/2, y0+172, c, 19, INK, "middle")
        g.line(x+30, y0+205, x+w-30, y0+205, col, 1, "4 4")
        g.text(x+w/2, y0+255, d, 22, INK, "middle", "bold")
        if i < 3: g.arrow(x+w+6, y0+150, x+w+gap-6, y0+150, INK, 4, 18)
    y = 440
    g.rect(40, y, 1520, 110, fill="#1F2A37", stroke="none", rx=16)
    g.text(800, y+48, "順序不可顛倒：先定 V_u 的位置 → 再選 V_c → 再判 V_s 區間（檢核斷面）→ 最後才算 s", 26, "#FFFFFF", "middle", "bold")
    g.text(800, y+88, "先算間距的人，會漏掉 d 偏移的前提、選錯 V_c、跳過 V_u ≤ 5φV_c 的斷面檢核", 20, "#C9D3DE", "middle")
    g.save("figs/fig01_map.svg")

# ───────── fig02 示範案例 ─────────
def fig02():
    g = SVG(1600, 600)
    card(g, 20, 20, 470, 560)
    g.text(255, 62, "基準斷面（全篇共用）", 24, INK, "middle", "bold")
    s = 5.0; x0, y0 = 255-35*s/2, 95
    g.rect(x0, y0, 35*s, 70*s, fill="#E9EDF2", stroke=INK, sw=2.5)
    g.rect(x0+18, y0+18, 35*s-36, 70*s-36, stroke=GRN, sw=3, rx=8)
    for i in range(3): g.circle(x0+34+i*(35*s-68)/2, y0+70*s-34, 11, fill=INK, stroke=INK)
    for i in range(2): g.circle(x0+34+i*(35*s-68), y0+32, 8, fill=INK, stroke=INK)
    g.line(x0, y0+70*s+22, x0+35*s, y0+70*s+22, MUTED, 1.3); g.text(255, y0+70*s+50, "b_w = 35", 20, INK, "middle")
    g.line(x0-26, y0, x0-26, y0+70*s, MUTED, 1.3); g.text(x0-36, y0+175, "h = 70", 20, INK, "end")
    g.line(x0+35*s+26, y0, x0+35*s+26, y0+70*s-34, BLU, 1.6); g.text(x0+35*s+36, y0+175, "d = 63", 20, BLU, "start", "bold")
    g.text(255, 540, "f'_c = 280、f_{yt} = 4200、D13 雙肢 A_v = 2.534", 18, INK, "middle")
    g.text(255, 566, f"V_c = 0.53√f'_c b_w d = {f2(VC)} tf", 19, TEAL, "middle", "bold")
    # 三個例
    ex = [("例①  頂面均布、支承受壓", f"w_u = {W1:.0f} t/m、l_n = {L1:.1f} m", f"V_u：{f2(VU1_F)} → d 處 {f2(VU1_D)}", GRN, "top"),
          ("例②  詳細式", f"6-D25（ρ_w = {RHO2:.4f}）、V_u d/M_u = {VDM2:.2f}", f"V_c = {f2(VC_DET)} tf", BLU, "sec"),
          ("例③  梁吊掛在大梁側面", f"w_u = {W3:.0f} t/m、l_n = {L3:.1f} m", f"V_u = {f2(VU3)}（不可 d 偏移）", RED, "hung")]
    for i, (hd, a, b, col, kind) in enumerate(ex):
        y = 20 + i*190; x = 510
        card(g, x, y, 1070, 175)
        g.rect(x, y, 10, 175, fill=col, stroke="none")
        g.text(x+36, y+46, hd, 23, col, "start", "bold")
        g.text(x+36, y+92, a, 20, INK); g.text(x+36, y+136, b, 21, INK, "start", "bold")
        bx = x+620
        if kind == "top":
            udl(g, bx+20, bx+400, y+72, 9, 26); g.rect(bx+20, y+72, 380, 44, fill="#FFFFFF", stroke=INK, sw=2)
            pin(g, bx+30, y+116, 0.8); pin(g, bx+390, y+116, 0.8)
        elif kind == "sec":
            g.rect(bx+140, y+18, 70, 140, fill="#E9EDF2", stroke=INK, sw=2)
            for j in range(3): g.circle(bx+154+j*21, y+140, 7, fill=INK, stroke=INK); g.circle(bx+154+j*21, y+122, 7, fill=INK, stroke=INK)
            g.text(bx+240, y+80, "ρ_w = A_s/(b_w d)", 19, BLU); g.text(bx+240, y+112, f"= {AS2:.2f}/{BD:.0f}", 19, BLU)
        else:
            hatch(g, bx+20, y+20, 60, 140)
            udl(g, bx+100, bx+420, y+70, 8, 24); g.rect(bx+80, y+70, 340, 44, fill="#FFFFFF", stroke=INK, sw=2)
            g.arrow(bx+50, y+150, bx+50, y+100, RED, 3, 12); g.text(bx+100, y+150, "反力從側面把梁『吊』起來", 16, RED)
    g.save("figs/fig02_cases.svg")

# ───────── fig03 為什麼是 d ─────────
def fig03():
    g = SVG(1600, 590)
    x0, y0, Lb, hb = 170, 150, 1000, 300
    udl(g, x0, x0+Lb, y0, 16, 40)
    g.rect(x0, y0, Lb, hb, fill="#FFFFFF", stroke=INK, sw=2.5)
    hatch(g, x0-120, y0+hb, 170, 110)
    g.text(x0-35, y0+hb+132, "柱（支承）", 18, MUTED, "middle")
    xs = x0+50
    # d zone
    g.rect(xs, y0, hb, hb, fill="#F3EFFB", stroke="none")
    g.line(xs, y0-60, xs, y0+hb+20, MUTED, 1.4, "6 5"); g.text(xs, y0-68, "支承面", 17, MUTED, "middle")
    g.line(xs+hb, y0-60, xs+hb, y0+hb+20, ORG, 2.2, "8 6"); g.text(xs+hb, y0-68, "臨界斷面", 19, ORG, "middle", "bold")
    g.arrow(xs, y0+hb+45, xs+hb, y0+hb+45, ORG, 2, 12); g.arrow(xs+hb, y0+hb+45, xs, y0+hb+45, ORG, 2, 12)
    g.text(xs+hb/2, y0+hb+78, "d", 26, ORG, "middle", "bold", True)
    # crack
    g.line(xs+6, y0+hb-6, xs+hb, y0+8, RED, 5, cap="round"); g.text(xs+hb*0.50+30, y0+hb*0.60, "45° 斜裂縫", 20, RED, "start", "bold")
    # struts (fan) from top load to support
    for k in range(4):
        xt = xs+30+k*62
        g.arrow(xt, y0+14, xs+14, y0+hb-18, PUR, 2.4, 11, "10 6")
    g.text(xs+hb/2-40, y0+50, "斜壓桿", 19, PUR, "middle", "bold")
    # beyond
    g.line(xs+hb+60, y0+hb-6, xs+hb+60+hb-12, y0+8, RED, 3, "3 6")
    g.text(xs+hb+320, y0+hb*0.66, "d 以外的裂縫才會『切斷』梁", 19, INK)
    # right explanation
    card(g, 1230, 70, 350, 460, fill="#FFFFFF")
    g.rect(1230, 70, 8, 460, fill=PUR, stroke="none")
    lines = [("物理邏輯", PUR, True), ("① 最早的斜裂縫從支承面", INK, False), ("   底部出發、斜 45° 上升", INK, False),
             ("② 水平走 d 才穿到頂面", INK, False), ("③ d 以內的載重順著", INK, False), ("   斜壓桿直接進支承", INK, False),
             ("   不跨越任何斜裂縫", INK, False), ("", INK, False), ("⇒ 設計只需檢核", RED, True), ("   距支承面 d 處的 V_u", RED, True)]
    for i, (tt, c, b) in enumerate(lines):
        g.text(1260, 115+i*41, tt, 20, c, "start", "bold" if b else "normal")
    g.save("figs/fig03_crack.svg")

# ───────── fig04 三前提 × 四情境 ─────────
def fig04():
    g = SVG(1600, 720)
    P = [(20, 20), (810, 20), (20, 370), (810, 370)]; W, Hh = 770, 335
    for (x, y) in P: card(g, x, y, W, Hh)
    # A 可用
    x, y = P[0]; tag(g, x+20, y+18, "○ 可以用 d 偏移", GRN)
    g.text(x+W-20, y+40, "頂面載重＋支承受壓＋d 內無集中載重", 16, MUTED, "end")
    bx, by = x+70, y+120
    udl(g, bx, bx+620, by, 12, 30); g.rect(bx, by, 620, 120, fill="#FFFFFF", stroke=INK, sw=2.2)
    pin(g, bx+30, by+120)
    g.line(bx+30, by+116, bx+30+115, by+4, RED, 3.5); g.line(bx+145, by-10, bx+145, by+140, ORG, 2, "7 5")
    g.text(bx+155, by+30, "臨界斷面", 17, ORG, "start", "bold")
    g.text(bx+400, by+75, "反力往上頂 ⇒ 端區受壓", 17, INK, "middle")
    g.rect(x+60, y+280, W-120, 40, fill=GBG, stroke="none", rx=8); g.text(x+W/2, y+308, "取 V_u 在距支承面 d 處", 19, GRN, "middle", "bold")
    # B 吊掛
    x, y = P[1]; tag(g, x+20, y+18, "× 不能用：吊掛", RED)
    g.text(x+W-20, y+40, "梁掛在另一支大梁的側面（支承在拉力側）", 16, MUTED, "end")
    hatch(g, x+60, y+75, 80, 185); g.text(x+100, y+70, "大梁", 16, INK, "middle", "bold")
    udl(g, x+160, x+730, y+130, 10, 30); g.rect(x+140, y+130, 590, 100, fill="#FFFFFF", stroke=INK, sw=2.2)
    g.arrow(x+100, y+250, x+100, y+170, RED, 3, 13)
    g.line(x+142, y+226, x+242, y+134, RED, 3.5)
    g.text(x+260, y+260, "端部沒有壓應力，裂縫直接從支承面發展", 16, RED, "start", "bold")
    g.rect(x+60, y+280, W-120, 40, fill=RBG, stroke="none", rx=8); g.text(x+W/2, y+308, "取 V_u 在支承面", 19, RED, "middle", "bold")
    # C 倒T
    x, y = P[2]; tag(g, x+20, y+18, "× 不能用：倒 T 梁", RED)
    g.text(x+W-20, y+40, "小梁擱在翼板下緣（載重加在拉力側）", 16, MUTED, "end")
    cx = x+230
    hatch(g, cx-45, y+80, 90, 110); hatch(g, cx-150, y+190, 300, 55)
    g.arrow(cx, y+180, cx, y+95, RED, 2.2, 11, "6 4"); g.text(cx+55, y+130, "吊筋把力提到頂部", 15, RED)
    g.arrow(cx-110, y+170, cx-110, y+192, RED, 3, 12); g.arrow(cx+110, y+170, cx+110, y+192, RED, 3, 12)
    g.text(cx, y+268, "小梁反力壓在翼板上面 ↓", 14, MUTED, "middle")
    g.rect(x+430, y+80, 310, 180, fill="#FFFFFF", stroke="#D5DAE1", rx=10); g.rect(x+430, y+80, 7, 180, fill=RED, stroke="none")
    for i, tt in enumerate(["為什麼不行", "載重從腹板『下面』掛進來，", "d 內沒有從載重點直達支承", "的斜壓桿 → 不能跳過這段，", "還要另外設計吊筋。"]):
        g.text(x+455, y+115+i*33, tt, 17 if i else 19, INK, "start", "bold" if i == 0 else "normal")
    g.rect(x+60, y+280, W-120, 40, fill=RBG, stroke="none", rx=8); g.text(x+W/2, y+308, "取 V_u 在支承面", 19, RED, "middle", "bold")
    # D 集中載重
    x, y = P[3]; tag(g, x+20, y+18, "× 不能用：d 內有集中載重", RED)
    bx, by = x+80, y+110
    g.rect(bx, by, 620, 130, fill="#FFFFFF", stroke=INK, sw=2.2); pin(g, bx+30, by+130)
    g.line(bx+145, by-40, bx+145, by+150, ORG, 2, "7 5"); g.text(bx+155, by+158, "d", 20, ORG, "start", "bold", True)
    g.arrow(bx+100, by-50, bx+100, by-3, RED, 3.5, 14); g.text(bx+80, by-30, "P", 22, RED, "end", "bold")
    g.text(bx+390, by+60, "P 落在 d 以內 ⇒ 這段不再是", 17, RED, "middle", "bold")
    g.text(bx+390, by+90, "『沒有額外剪力進來』的區段", 17, RED, "middle", "bold")
    g.rect(x+60, y+280, W-120, 40, fill=RBG, stroke="none", rx=8); g.text(x+W/2, y+308, "取 V_u 在支承面", 19, RED, "middle", "bold")
    g.save("figs/fig04_prereq.svg")

# 剪力圖通用：左端支承面起，x 0~3.5 m
def vdiag(g, X0, Y0, Wd, Hd, vmax, xmax, ticks, yt):
    sx = lambda x: X0 + x/xmax*Wd; sy = lambda v: Y0 + Hd - v/vmax*Hd
    g.rect(X0, Y0, Wd, Hd, fill="#FFFFFF", stroke=GRID, sw=1)
    for v in yt:
        g.line(X0, sy(v), X0+Wd, sy(v), GRID, 1); g.text(X0-10, sy(v)+6, f"{v:g}", 15, MUTED, "end")
    for x in ticks:
        g.line(sx(x), Y0+Hd, sx(x), Y0+Hd+7, MUTED, 1.2); g.text(sx(x), Y0+Hd+28, f"{x:g}", 15, MUTED, "middle")
    return sx, sy

# ───────── fig05 例① d 偏移 ─────────
def fig05():
    g = SVG(1600, 560)
    X0, Y0, Wd, Hd = 110, 60, 900, 400
    sx, sy = vdiag(g, X0, Y0, Wd, Hd, 50, 3.5, [0, 0.63, 1, 1.5, 2, 2.5, 3, 3.5], [0, 10, 20, 30, 40, 50])
    g.text(X0-10, Y0-18, "V_u (tf)", 16, MUTED, "end"); g.text(X0+Wd, Y0+Hd+56, "距支承面 x (m)", 16, MUTED, "end")
    xd = D/100
    g.poly([(sx(0), sy(0)), (sx(0), sy(VU1_F)), (sx(3.5), sy(0))], color="none", fill=GRN, op=0.10, closed=True)
    g.poly([(sx(0), sy(VU1_D)), (sx(0), sy(VU1_F)), (sx(xd), sy(VU1_D))], color="none", fill=RED, op=0.25, closed=True)
    g.line(sx(0), sy(VU1_D), sx(xd), sy(VU1_D), RED, 2, "6 4")
    g.line(sx(0), sy(VU1_F), sx(3.5), sy(0), GRN, 4)
    g.line(sx(xd), sy(0), sx(xd), sy(VU1_D), ORG, 2, "7 5")
    g.circle(sx(0), sy(VU1_F), 8, fill=GRN); g.circle(sx(xd), sy(VU1_D), 8, fill=ORG)
    g.text(sx(0)+16, sy(VU1_F)-10, f"支承面 {f2(VU1_F)}", 19, GRN, "start", "bold")
    g.text(sx(xd)+16, sy(VU1_D)-14, f"d = 0.63 m 處 {f2(VU1_D)}", 19, ORG, "start", "bold")
    g.text(sx(0.2), sy(VU1_D)+30, "省下的", 15, RED, "start", "bold")
    # right card
    card(g, 1060, 40, 520, 460, fill="#FFFFFF")
    L = [("一行就能算", INK, 21, True), (f"V_u(d) = V_u(支承面) − w_u·d", INK, 19, False),
         (f"= {f2(VU1_F)} − {W1:.0f} × 0.63 = {f2(VU1_D)} tf", GRN, 20, True), ("", INK, 10, False),
         (f"省 {SAVE1:.1f}%  ⇒ 端部箍筋", RED, 21, True),
         (f"s_{{req}}：{f1(S1F_REQ)} cm → {f1(S1_REQ)} cm", RED, 20, True), ("", INK, 10, False),
         ("注意：只有均布載重才能用", MUTED, 17, False), ("『減 w_u·d』；有集中載重回頭", MUTED, 17, False), ("看前提 (c)", MUTED, 17, False)]
    y = 90
    for tt, c, sz, b in L:
        g.text(1090, y, tt, sz, c, "start", "bold" if b else "normal"); y += sz*1.9
    g.save("figs/fig05_ex1.svg")

# ───────── fig06 例③ 吊掛誤用 ─────────
def fig06():
    g = SVG(1600, 560)
    X0, Y0, Wd, Hd = 110, 60, 700, 400
    sx, sy = vdiag(g, X0, Y0, Wd, Hd, 70, 3.5, [0, 0.63, 1, 2, 3, 3.5], [0, 20, 40, 60, 70])
    g.text(X0-10, Y0-18, "V_u (tf)", 16, MUTED, "end")
    xd = D/100
    g.poly([(sx(0), sy(0)), (sx(0), sy(VU3)), (sx(3.5), sy(0))], color="none", fill=RED, op=0.08, closed=True)
    g.line(sx(0), sy(VU3), sx(3.5), sy(0), RED, 4)
    g.line(sx(xd), sy(0), sx(xd), sy(VU3_D), MUTED, 2, "7 5")
    g.circle(sx(0), sy(VU3), 9, fill=RED); g.circle(sx(xd), sy(VU3_D), 8, fill=MUTED)
    g.text(sx(0)+18, sy(VU3)-8, f"必須取支承面 {f2(VU3)}", 19, RED, "start", "bold")
    g.text(sx(xd)+30, sy(VU3_D)-18, f"× 誤用 d 偏移 {f2(VU3_D)}", 18, MUTED, "start", "bold", bg="#FFFFFF")
    # compare stirrups
    card(g, 860, 40, 720, 460, fill="#FFFFFF")
    g.text(1220, 82, "同一根梁、同一段 1 m，箍筋差多少？", 21, INK, "middle", "bold")
    for row, (lab, s, col, val) in enumerate([("正確 V_u = 63.00", S3_REQ, RED, VS3), ("誤用 V_u = 51.66", S3_D_REQ, MUTED, VS3_D)]):
        yy = 130 + row*165
        g.text(890, yy+10, lab, 18, col, "start", "bold")
        g.text(1550, yy+10, f"V_s = {f2(val)} → s ≤ {f2(s)} cm", 17, col, "end")
        g.rect(890, yy+30, 660, 90, fill="#F8FAFC", stroke=INK, sw=1.6)
        n = int(100/s)+1
        for i in range(n):
            xx = 900 + i*s*6.4
            if xx < 1545: g.line(xx, yy+36, xx, yy+114, col, 3)
    g.text(1220, 470, f"正確的端部箍筋量比誤算多 {AVS_UP3:.0f}%  —— 誤用不是省，是不安全", 20, RED, "middle", "bold")
    g.save("figs/fig06_ex3.svg")

# ───────── fig07 V_c 的物理：主拉應力 ─────────
def fig07():
    g = SVG(1600, 590)
    cases = [("純剪（無軸力）", 0, TEAL, "σ_1 = τ"), ("加軸壓 N_u > 0", -0.6, BLU, "σ_1 變小 ⇒ 較晚開裂 ⇒ V_c ↑"), ("加軸拉 N_u < 0", 0.8, RED, "σ_1 變大 ⇒ 提早開裂 ⇒ V_c ↓")]
    for i, (hd, sn, col, msg) in enumerate(cases):
        x = 20 + i*527; card(g, x, 20, 507, 550)
        g.text(x+253, 62, hd, 23, col, "middle", "bold")
        # element
        cx, cy, a = x+130, 210, 55
        g.rect(cx-a, cy-a, 2*a, 2*a, fill="#FFFFFF", stroke=INK, sw=2)
        for (x1, y1, x2, y2) in [(cx-a+10, cy-a-12, cx+a-10, cy-a-12), (cx+a-10, cy+a+12, cx-a+10, cy+a+12), (cx+a+12, cy+a-10, cx+a+12, cy-a+10), (cx-a-12, cy-a+10, cx-a-12, cy+a-10)]:
            g.arrow(x1, y1, x2, y2, INK, 2, 9)
        g.text(cx, cy-a-24, "τ", 18, INK, "middle", "bold", True)
        if sn < 0:
            g.arrow(cx+a+75, cy, cx+a+30, cy, BLU, 3, 12); g.arrow(cx-a-75, cy, cx-a-30, cy, BLU, 3, 12)
        elif sn > 0:
            g.arrow(cx+a+30, cy, cx+a+75, cy, RED, 3, 12); g.arrow(cx-a-30, cy, cx-a-75, cy, RED, 3, 12)
        # crack direction
        ang = 45 + 18*sn
        dx, dy = 40*math.cos(math.radians(ang)), 40*math.sin(math.radians(ang))
        g.line(cx-dx, cy+dy, cx+dx, cy-dy, RED, 3, "5 4")
        # Mohr circle
        ox, oy, sc = x+360, 210, 60
        g.line(ox-120, oy, ox+130, oy, MUTED, 1.2); g.line(ox, oy-100, ox, oy+100, MUTED, 1.2)
        g.text(ox-118, oy-8, "σ", 16, MUTED, "start", italic=True)
        c = sn/2; R = math.sqrt(c*c+1)
        g.add(f'<circle cx="{ox+c*sc:.1f}" cy="{oy}" r="{R*sc:.1f}" fill="{col}" fill-opacity="0.08" stroke="{col}" stroke-width="2.5"/>')
        s1 = c + R
        g.circle(ox+s1*sc, oy, 7, fill=col); g.text(ox+s1*sc+14, oy-14, "σ_1", 17, col, "start", "bold", bg="#FFFFFF")
        # bar of σ1
        g.text(x+30, 400, "主拉應力 σ_1（拉）", 17, INK)
        g.rect(x+30, 415, 440, 26, fill="#E8ECF1", stroke="none", rx=4)
        g.rect(x+30, 415, 440*s1/1.8, 26, fill=col, stroke="none", rx=4)
        g.text(x+253, 490, msg, 18, col, "middle", "bold")
        g.text(x+253, 530, "開裂當下：σ_1 碰到混凝土抗拉強度", 15, MUTED, "middle")
    g.save("figs/fig07_principal.svg")

# ───────── fig08 五張臉長條 ─────────
def fig08():
    g = SVG(1600, 560)
    B = [("① 簡化式 0.53√f'_c b_w d", VC, TEAL), ("② 詳細式（例②）", VC_DET, GRN), (f"③ 軸壓 N_u = +{NU:.0f}", VC_NC, BLU),
         (f"④ 軸拉 N_u = −{NU:.0f}", VC_NT, RED), ("⑤ 耐震塑鉸區", 0.0, INK)]
    X, Wb, vmax = 430, 900, 25
    for i, (lab, v, col) in enumerate(B):
        y = 40 + i*92
        g.text(X-20, y+38, lab, 21, INK, "end", "bold")
        g.rect(X, y+10, Wb, 42, fill="#E8ECF1", stroke="none", rx=6)
        if v > 0: g.rect(X, y+10, Wb*v/vmax, 42, fill=col, stroke="none", rx=6)
        else: g.rect(X, y+10, 5, 42, fill=INK, stroke="none")
        g.text(X+Wb*v/vmax+16, y+42, f"{f2(v)} tf", 23, col, "start", "bold")
    g.line(X+Wb*VC/vmax, 20, X+Wb*VC/vmax, 500, TEAL, 1.6, "6 5")
    g.text(X+Wb*VC/vmax+8, 18, "基本盤", 16, TEAL, "start", "bold")
    g.text(800, 545, "同一個 35×70 斷面：最高 23.24、最低 0 —— 選錯一張臉，箍筋量差好幾倍", 20, ORG, "middle", "bold")
    g.save("figs/fig08_faces.svg")

# ───────── fig09 V_c–N_u ─────────
def fig09():
    g = SVG(1600, 560)
    X0, Y0, Wd, Hd = 130, 40, 1000, 420
    nmin, nmax, vmax = -100, 160, 30
    sx = lambda n: X0 + (n-nmin)/(nmax-nmin)*Wd; sy = lambda v: Y0+Hd-v/vmax*Hd
    g.rect(X0, Y0, Wd, Hd, fill="#FFFFFF", stroke=GRID)
    for v in (0, 10, 20, 30): g.line(X0, sy(v), X0+Wd, sy(v), GRID, 1); g.text(X0-10, sy(v)+6, f"{v}", 15, MUTED, "end")
    for n in (-80, -40, 0, 40, 80, 120, 160): g.text(sx(n), Y0+Hd+28, f"{n}", 15, MUTED, "middle")
    g.text(X0-10, Y0-12, "V_c (tf)", 16, MUTED, "end"); g.text(X0+Wd, Y0+Hd+56, "N_u (tf)　＋壓／−拉", 16, MUTED, "end")
    g.line(sx(0), Y0, sx(0), Y0+Hd, MUTED, 1.4, "6 5")
    f = lambda n: VC*(1+n*1000/(140*AG)) if n >= 0 else max(0, VC*(1+n*1000/(35*AG)))
    g.line(sx(nmin), sy(0), sx(-NU_ZERO), sy(0), RED, 4)
    g.poly([(sx(n), sy(f(n))) for n in [-NU_ZERO, 0, 160]], color=INK, sw=4)
    for n, col, lab, dx, dy in [(0, TEAL, f"無軸力 {f2(VC)}", 16, 34), (NU, BLU, f"+{NU:.0f} → {f2(VC_NC)}", 0, -24), (-NU, RED, f"−{NU:.0f} → {f2(VC_NT)}", 16, 36), (-NU_ZERO, RED, f"N_u = −{NU_ZERO:.2f} ⇒ V_c = 0", 0, -60)]:
        g.circle(sx(n), sy(f(n)), 9, fill=col); g.text(sx(n)+dx, sy(f(n))+dy, lab, 18, col, "middle" if dx == 0 else "start", "bold")
    card(g, 1170, 40, 410, 420, fill="#FFFFFF")
    for i, (tt, c, b) in enumerate([("斜率比", INK, True), ("拉：1/35　壓：1/140", INK, False), ("⇒ 拉的殺傷力是壓的 4 倍", RED, True), ("", INK, False),
                                    (f"同為 60 tf：", INK, True), (f"軸壓 +{UP_C:.1f}%", BLU, True), (f"軸拉 −{DN_T:.1f}%", RED, True), ("", INK, False), ("記憶：怕拉不怕壓", MUTED, False)]):
        g.text(1200, 90+i*43, tt, 21, c, "start", "bold" if b else "normal")
    g.save("figs/fig09_axial.svg")

# ───────── fig10 耐震 V_c = 0 ─────────
def fig10():
    g = SVG(1600, 560)
    bx, by = 80, 110
    hatch(g, bx, by-60, 60, 260); hatch(g, bx+860, by-60, 60, 260)
    g.rect(bx+60, by, 800, 110, fill="#FFFFFF", stroke=INK, sw=2.2)
    g.rect(bx+60, by, 190, 110, fill=RED, stroke="none", op=0.15); g.rect(bx+670, by, 190, 110, fill=RED, stroke="none", op=0.15)
    g.text(bx+155, by+62, "塑鉸區", 20, RED, "middle", "bold"); g.text(bx+765, by+62, "塑鉸區", 20, RED, "middle", "bold")
    g.text(bx+155, by+150, "2h 範圍", 16, RED, "middle"); g.text(bx+460, by+62, "一般區：照常用 V_c", 18, TEAL, "middle")
    g.text(bx+460, by+215, "反覆地震下，塑鉸區的斜裂縫會來回張開、貫穿", 18, INK, "middle")
    g.text(bx+460, by+245, "骨材咬合失效 ⇒ 混凝土那一份不可靠", 18, INK, "middle")
    # decision
    x = 1060
    g.rect(x, 40, 500, 70, fill=BBG, stroke=BLU, sw=2, rx=10); g.text(x+250, 85, "特殊抗彎構架塑鉸區（2h 內）", 20, BLU, "middle", "bold")
    g.arrow(x+250, 110, x+250, 140, INK, 2.2)
    g.rect(x, 140, 500, 90, fill="#FFFFFF", stroke=INK, sw=2, rx=10)
    g.text(x+250, 178, "條件 A：地震引致剪力 ≥ ½ 設計剪力", 18, INK, "middle", "bold"); g.text(x+250, 212, "條件 B：N_u < A_g f'_c / 20", 18, INK, "middle", "bold")
    g.arrow(x+140, 230, x+140, 300, RED, 2.2); g.arrow(x+360, 230, x+360, 300, TEAL, 2.2)
    g.text(x+130, 272, "兩者皆成立", 16, RED, "end"); g.text(x+370, 272, "任一不成立", 16, TEAL)
    g.rect(x, 300, 240, 80, fill=RBG, stroke=RED, sw=2, rx=10); g.text(x+120, 350, "V_c = 0", 26, RED, "middle", "bold")
    g.rect(x+260, 300, 240, 80, fill=GBG, stroke=TEAL, sw=2, rx=10); g.text(x+380, 350, "照常算 V_c", 22, TEAL, "middle", "bold")
    g.text(x+250, 440, f"本斷面：A_g f'_c/20 = {AG*FC/20/1000:.1f} tf", 18, MUTED, "middle")
    g.text(x+250, 475, "梁軸力通常很小 ⇒ 條件 B 幾乎必成立", 18, MUTED, "middle")
    g.save("figs/fig10_seismic.svg")

# ───────── fig11 V_s 三區間數線 ─────────
def fig11():
    g = SVG(1600, 540)
    X0, X1, y = 80, 1480, 170; vmax = 95
    sx = lambda v: X0 + v/vmax*(X1-X0)
    for a, b, col, lab in [(0, VC2, GRN, "V_s ≤ 2V_c"), (VC2, VC4, ORG, "2V_c < V_s ≤ 4V_c"), (VC4, vmax, RED, "V_s > 4V_c")]:
        g.rect(sx(a)+3, y-80, sx(b)-sx(a)-6, 56, fill=col, stroke="none", rx=8)
        g.text((sx(a)+sx(b))/2, y-43, lab, 23, "#FFFFFF", "middle", "bold")
    g.arrow(X0, y, X1+60, y, INK, 3, 14); g.text(X1+60, y+36, "V_s (tf)", 17, MUTED, "end", italic=True)
    for v, lab, col in [(0, "0", INK), (VC2, f"2V_c = {f2(VC2)}", ORG), (VC4, f"4V_c = {f2(VC4)}", RED)]:
        g.line(sx(v), y-10, sx(v), y+10, col, 3); g.text(sx(v), y+38, lab, 19, col, "middle", "bold")
    for a, b, col, t1, t2 in [(0, VC2, GRN, "裂縫不密", "s_{max} = min(d/2, 60) = 31.5"), (VC2, VC4, ORG, "裂縫變密、每條裂縫要 2 支箍筋", "s_{max} = min(d/4, 30) = 15.75"), (VC4, vmax, RED, "換了破壞機制", "加箍筋無效 → 加大斷面")]:
        g.text((sx(a)+sx(b))/2, y+90, t1, 18, col, "middle", "bold"); g.text((sx(a)+sx(b))/2, y+122, t2, 19, INK, "middle", "bold")
    for v, lab, col, yy in [(VS1, f"例① V_s = {f2(VS1)}", GRN, 0), (VS1F, f"例①不偏移 {f2(VS1F)}", MUTED, 1), (VS3, f"例③ V_s = {f2(VS3)}", ORG, 0)]:
        g.arrow(sx(v), y+220+yy*70, sx(v), y+160, col, 2.6, 12)
        g.text(sx(v), y+250+yy*70, lab, 19, col, "middle", "bold")
    g.save("figs/fig11_zones.svg")

# ───────── fig12 為什麼 4V_c 是天花板 ─────────
def fig12():
    g = SVG(1600, 590)
    for i, (hd, col, dense, msg1, msg2) in enumerate([("V_s ≤ 4V_c：箍筋先降伏", GRN, 5, "斜壓桿還有餘裕", "箍筋伸長、裂縫變寬 ⇒ 有預警（延性）"),
                                                      ("V_s > 4V_c：斜壓桿先壓碎", RED, 11, "箍筋還沒降伏，混凝土先碎", "瞬間崩落 ⇒ 沒有預警（脆性）")]):
        x = 20 + i*540; card(g, x, 20, 520, 550)
        g.text(x+260, 62, hd, 22, col, "middle", "bold")
        bx, by, bw, bh = x+30, 100, 460, 230
        g.rect(bx, by, bw, bh, fill="#FFFFFF", stroke=INK, sw=2.2)
        g.add(f'<clipPath id="c{i}"><rect x="{bx}" y="{by}" width="{bw}" height="{bh}"/></clipPath>')
        st = [f'<g clip-path="url(#c{i})">']
        n = 6
        for k in range(-2, n+2):
            x0 = bx + k*bw/n
            op = 0.35 if i == 0 else 0.75
            st.append(f'<polygon points="{x0:.1f},{by+bh} {x0+30:.1f},{by+bh} {x0+30+bh*0.8:.1f},{by} {x0+bh*0.8:.1f},{by}" fill="{BLU if i==0 else RED}" fill-opacity="{op*0.5}"/>')
        st.append('</g>'); g.add("".join(st))
        for k in range(dense):
            xx = bx + 20 + k*(bw-40)/(dense-1); g.line(xx, by+8, xx, by+bh-8, col, 3)
        if i == 1:
            for k in range(4):
                xx = bx+80+k*100; g.poly([(xx, by+90), (xx+14, by+110), (xx+4, by+125), (xx+20, by+145)], RED, 2.5)
        g.text(x+260, 380, msg1, 20, INK, "middle", "bold"); g.text(x+260, 415, msg2, 18, col, "middle")
        g.text(x+260, 470, "藍／紅斜帶＝混凝土斜壓桿｜直線＝箍筋", 15, MUTED, "middle")
    # Vn–Av/s
    x = 1100; card(g, x, 20, 480, 550, fill="#FFFFFF")
    g.text(x+240, 62, "V_n 隨箍筋量的變化", 21, INK, "middle", "bold")
    X0, Y0, W, Hh = x+70, 110, 370, 330
    g.arrow(X0, Y0+Hh, X0+W+20, Y0+Hh, INK, 2, 10); g.arrow(X0, Y0+Hh, X0, Y0-20, INK, 2, 10)
    g.text(X0+W+15, Y0+Hh+30, "A_v/s", 17, MUTED, "end"); g.text(X0-8, Y0-10, "V_n", 17, MUTED, "end")
    sy = lambda v: Y0+Hh - v/(6*VC)*Hh; kx = W*0.62
    g.line(X0, sy(VC), X0+kx, sy(5*VC), GRN, 4); g.line(X0+kx, sy(5*VC), X0+W, sy(5*VC), RED, 4)
    g.line(X0+kx, sy(5*VC), X0+W, sy(6.2*VC), MUTED, 2, "6 5"); g.text(X0+W-10, sy(6.1*VC)-8, "理論（不成立）", 14, MUTED, "end")
    for v, lab in [(VC, "V_c"), (5*VC, "5V_c")]:
        g.line(X0-6, sy(v), X0+6, sy(v), INK, 2); g.text(X0-10, sy(v)+6, lab, 16, INK, "end", "bold")
    g.line(X0+kx, sy(5*VC), X0+kx, Y0+Hh, RED, 1.4, "5 4")
    g.text(X0+kx, Y0+Hh+30, "V_s = 4V_c", 15, RED, "middle", "bold")
    g.text(x+240, 500, "過了轉折點：箍筋再多，V_n 不再上升", 17, RED, "middle", "bold")
    g.text(x+240, 530, f"本斷面 5V_c = {f2(5*VC)} tf", 16, MUTED, "middle")
    g.save("figs/fig12_ceiling.svg")

# ───────── fig13 斷面使用率 ─────────
def fig13():
    g = SVG(1600, 430)
    X, Wb = 360, 1000
    g.text(800, 40, f"V_{{u,max}} = 5φV_c = 5 × 0.75 × {f2(VC)} = {f2(VU_MAX)} tf", 23, INK, "middle", "bold")
    rows = [("例①  V_u = 34.44", VU1_D, GRN), ("例③  V_u = 63.00", VU3, ORG), ("假設 V_u = 80.00", 80.0, RED)]
    for i, (lab, v, col) in enumerate(rows):
        y = 80 + i*95
        g.text(X-20, y+40, lab, 21, INK, "end", "bold")
        g.rect(X, y+12, Wb, 44, fill="#E8ECF1", stroke="none", rx=6)
        w = Wb*min(v/VU_MAX, 1.15)/1.15
        g.rect(X, y+12, w, 44, fill=col, stroke="none", rx=6)
        r = v/VU_MAX*100
        g.text(X+w+14, y+44, f"{r:.1f}%" + ("  ⇒ 斷面不足！" if r > 100 else ""), 22, col, "start", "bold")
    xl = X + Wb/1.15
    g.line(xl, 70, xl, 370, RED, 2.5, "8 6"); g.text(xl, 400, "100%＝斜壓桿壓碎線", 18, RED, "middle", "bold")
    g.save("figs/fig13_usage.svg")

# ───────── fig14 尺的陷阱：門檻用 1.06√f'c bw d ─────────
def fig14():
    g = SVG(1600, 470)
    g.text(800, 40, f"軸拉 N_u = −60 tf：V_c 掉到 {f2(VC_NT)}，但間距門檻不會跟著掉", 23, INK, "middle", "bold")
    X0, X1 = 120, 1480; vmax = 85
    sx = lambda v: X0 + v/vmax*(X1-X0)
    for row, (hd, col, t2, t4, ok) in enumerate([("× 錯：拿修正後的 V_c 當尺", MUTED, 2*VC_NT, 4*VC_NT, False),
                                                 ("○ 對：尺是 1.06√f'_c b_w d、2.12√f'_c b_w d", GRN, VS2_LIM, VS4_LIM, True)]):
        y = 150 + row*170
        g.text(X0, y-50, hd, 20, col, "start", "bold")
        g.rect(sx(0), y-30, sx(t2)-sx(0), 30, fill=GRN, stroke="none", op=0.8)
        g.rect(sx(t2), y-30, sx(t4)-sx(t2), 30, fill=ORG, stroke="none", op=0.8)
        g.rect(sx(t4), y-30, sx(vmax)-sx(t4), 30, fill=RED, stroke="none", op=0.8)
        g.line(X0, y, X1, y, INK, 2)
        g.text(sx(t2), y+30, f"{f2(t2)}", 18, ORG, "middle", "bold"); g.text(sx(t4), y+30, f"{f2(t4)}", 18, RED, "middle", "bold")
        vs = 30.0
        g.arrow(sx(vs), y+80, sx(vs), y+8, INK, 2.4, 12)
        g.text(sx(vs)+14, y+76, "假設 V_s = 30：" + ("誤判『超過天花板，斷面不足』" if not ok else "其實 ≤ 2V_c 區，s_{max} = d/2"), 18, RED if not ok else GRN, "start", "bold")
    g.save("figs/fig14_ruler.svg")

# ───────── fig15 四取小 ─────────
def fig15():
    g = SVG(1600, 560)
    groups = [("例③ A 區（支承面，V_s = 64.44）", [("① 強度需求", S3_REQ), ("② s_{max} = d/4", SMAX4), ("③ A_{v,min} 反算", S_AVMIN)], SA, RED),
              ("例①（d 處，V_s = 26.36）", [("① 強度需求", S1_REQ), ("② s_{max} = d/2", SMAX2), ("③ A_{v,min} 反算", S_AVMIN)], S1, GRN)]
    X, Wb, smax = 330, 1000, 90
    for gi, (hd, rows, use, col) in enumerate(groups):
        y0 = 20 + gi*270
        g.text(40, y0+30, hd, 21, col, "start", "bold")
        mn = min(v for _, v in rows)
        for i, (lab, v) in enumerate(rows):
            y = y0 + 48 + i*52
            g.text(X-16, y+28, lab, 18, INK, "end")
            c = col if v == mn else "#B8C0CA"
            g.rect(X, y+8, Wb*v/smax, 30, fill=c, stroke="none", rx=5)
            g.text(X+Wb*v/smax+12, y+31, f"{f2(v)} cm" + ("  ← 最小" if v == mn else ""), 18, c if v == mn else MUTED, "start", "bold")
        y = y0 + 48 + 3*52
        g.text(X-16, y+28, "④ 施工取整", 18, INK, "end", "bold")
        g.rect(X, y+8, Wb*use/smax, 30, fill=INK, stroke="none", rx=5)
        g.text(X+Wb*use/smax+12, y+31, f"採用 D13@{use:.0f} cm", 19, INK, "start", "bold")
    g.save("figs/fig15_min4.svg")

# ───────── fig16 A_v,min 兩式交叉 ─────────
def fig16():
    g = SVG(1600, 520)
    X0, Y0, W, Hh = 120, 40, 900, 400
    f0, f1_ = 200, 500; c0, c1 = 2.6, 4.6
    sx = lambda f: X0+(f-f0)/(f1_-f0)*W; sy = lambda c: Y0+Hh-(c-c0)/(c1-c0)*Hh
    g.rect(X0, Y0, W, Hh, fill="#FFFFFF", stroke=GRID)
    for c in (3.0, 3.5, 4.0, 4.5): g.line(X0, sy(c), X0+W, sy(c), GRID, 1); g.text(X0-10, sy(c)+6, f"{c:.1f}", 15, MUTED, "end")
    for f in (210, 280, 350, 420, 490): g.text(sx(f), Y0+Hh+28, f"{f}", 15, MUTED, "middle")
    g.text(X0+W, Y0+Hh+56, "f'_c (kgf/cm²)", 16, MUTED, "end"); g.text(X0-10, Y0-14, "係數", 16, MUTED, "end")
    g.poly([(sx(f), sy(max(3.5, 0.2*math.sqrt(f)))) for f in range(200, 501, 5)], "#F2B8B0", 14)
    g.text(sx(420), sy(4.1)+50, "紅色粗帶＝兩式取大（控制值）", 16, RED, "middle")
    g.poly([(sx(f), sy(0.2*math.sqrt(f))) for f in range(200, 501, 5)], BLU, 3.5)
    g.line(sx(f0), sy(3.5), sx(f1_), sy(3.5), ORG, 3.5)
    g.text(sx(470), sy(0.2*math.sqrt(470))-14, "0.2√f'_c", 19, BLU, "end", "bold"); g.text(sx(215), sy(3.5)-14, "3.5（下限）", 19, ORG, "start", "bold")
    g.line(sx(FC_X), sy(3.5), sx(FC_X), Y0+Hh, MUTED, 1.6, "6 5"); g.text(sx(FC_X)+8, Y0+Hh-12, f"f'_c = {FC_X:.0f}", 16, MUTED)
    g.circle(sx(280), sy(3.5), 9, fill=RED); g.text(sx(292), sy(3.2), f"本例 280：0.2√280 = {AVMIN_C1:.2f} < 3.5", 17, RED, "start", "bold", bg="#FFFFFF")
    card(g, 1070, 40, 510, 420, fill="#FFFFFF")
    for i, (tt, c, b) in enumerate([("A_{v,min} 兩式取大", INK, True), ("f'_c < 306：3.5 控制", ORG, True), ("f'_c > 306：0.2√f'_c 控制", BLU, True), ("", INK, False),
                                   ("反算間距：", INK, True), ("s ≤ A_v f_{yt} / (3.5 b_w)", INK, False), (f"= 2.534×4200 / (3.5×35)", INK, False), (f"= {f2(S_AVMIN)} cm", RED, True), ("", INK, False), ("考場常用的 f'_c 幾乎都是 3.5 控制", MUTED, False)]):
        g.text(1100, 90+i*38, tt, 20, c, "start", "bold" if b else "normal")
    g.save("figs/fig16_avmin.svg")

# ───────── fig17 剪力圖＋三條判準線 ─────────
def fig17():
    g = SVG(1600, 560)
    X0, Y0, Wd, Hd = 110, 60, 1320, 420
    sx, sy = vdiag(g, X0, Y0, Wd, Hd, 70, 3.5, [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5], [0, 10, 20, 30, 40, 50, 60, 70])
    g.text(X0-10, Y0-18, "V_u (tf)", 16, MUTED, "end"); g.text(X0+Wd, Y0+Hd+56, "距支承面 x (m)", 16, MUTED, "end")
    g.poly([(sx(0), sy(0)), (sx(0), sy(VU3)), (sx(3.5), sy(0))], color="none", fill=PUR, op=0.12, closed=True)
    for v, x, col, lab in [(PVC3, XA, RED, f"3φV_c = {f2(PVC3)}（V_s = 2V_c 界線）"), (PVC, XB, GRN, f"φV_c = {f2(PVC)}（以下理論上不需 V_s）"), (PVC05, XC, MUTED, f"0.5φV_c = {f2(PVC05)}（以下連最小箍筋都免）")]:
        g.line(X0, sy(v), X0+Wd, sy(v), col, 2.4, "10 6")
        g.line(sx(x), Y0, sx(x), Y0+Hd, col, 1.6, "5 4")
        g.text(sx(x), Y0-10, f"x = {f2(x)} m", 17, col, "middle", "bold")
        (g.text(X0+Wd-10, sy(v)-10, lab, 17, col, "end", "bold", bg="#FFFFFF") if v > 20 else g.text(sx(1.15), sy(v)-10, lab, 17, col, "start", "bold", bg="#FFFFFF"))
    g.line(sx(0), sy(VU3), sx(3.5), sy(0), PUR, 4.5)
    g.text(sx(0)+14, sy(VU3)-10, f"V_u = {f2(VU3)}（支承面）", 18, PUR, "start", "bold")
    for a, b, lab, col in [(0, XA, "A", RED), (XA, XB, "B", ORG), (XB, XC, "C", GRN), (XC, 3.5, "D", MUTED)]:
        g.text((sx(a)+sx(b))/2, sy(4) if lab in "AB" else sy(24), lab, 26, col, "middle", "bold")
    g.text(X0+10, Y0+Hd+56, f"x = (V_u(0) − 判準值) / w_u，例：(63.00 − {f2(PVC3)}) / 18 = {f2(XA)}", 16, MUTED)
    g.save("figs/fig17_vudiag.svg")

# ───────── fig18 箍筋配置 ─────────
def fig18():
    g = SVG(1600, 330)
    X0, W = 110, 1320; sx = lambda x: X0 + x/3.5*W
    y0, h = 90, 150
    g.rect(X0, y0, W, h, fill="#FFFFFF", stroke=INK, sw=2.4)
    pin(g, X0+10, y0+h)
    zones = [(0, XA, SA, RED, "A：D13@10"), (XA, XB, SB, ORG, "B：D13@15"), (XB, 3.5, SC, GRN, "C／D：D13@30")]
    for a, b, s, col, lab in zones:
        x = a*100 + s/2 if a == 0 else a*100 + s/2
        while x < b*100:
            g.line(sx(x/100), y0+10, sx(x/100), y0+h-10, col, 3); x += s
        if b < 3.5: g.line(sx(b), y0-10, sx(b), y0+h+10, col, 1.6, "5 4")
        tag(g, (sx(a)+sx(b))/2 - measure(lab, 19, True)/2 - 13, 22, lab, col, 19)
    g.line(sx(3.5), y0-10, sx(3.5), y0+h+10, MUTED, 1.6, "5 4"); g.text(sx(3.5), y0+h+34, "跨中（另一半對稱）", 16, MUTED, "end")
    g.text(X0+60, y0+h+34, "第一支箍筋距支承面 ≤ s/2", 16, MUTED)
    g.text(800, y0+h+72, "C 區（最小箍筋）與 D 區（可免）實務合併，全跨不小於 D13@30", 18, INK, "middle", "bold")
    g.save("figs/fig18_layout.svg")

# ───────── fig19 解題流程圖（菱形判斷）─────────
def fig19():
    g = SVG(1600, 850)
    def box(x, y, w, h, t, col, bg, sz=19, lines=None):
        g.rect(x-w/2, y-h/2, w, h, fill=bg, stroke=col, sw=2.2, rx=10)
        L = lines or [t]
        for i, tt in enumerate(L): g.text(x, y + (i-(len(L)-1)/2)*(sz*1.35) + sz*0.35, tt, sz, col if col != INK else INK, "middle", "bold")
    def dia(x, y, w, h, L, col):
        g.poly([(x, y-h/2), (x+w/2, y), (x, y+h/2), (x-w/2, y)], col, 2.4, fill="#FFFFFF", closed=True)
        for i, tt in enumerate(L): g.text(x, y + (i-(len(L)-1)/2)*24 + 7, tt, 17, col, "middle", "bold")
    # column 1: gate1
    cx = 200
    g.text(cx, 36, "關卡 1", 22, RED, "middle", "bold")
    dia(cx, 150, 300, 150, ["支承受壓？", "載重在頂面？", "d 內無集中載重？"], RED)
    g.arrow(cx, 225, cx, 295, INK, 2.2); g.text(cx+10, 265, "全是", 16, GRN)
    box(cx, 330, 280, 70, "", GRN, GBG, 18, ["V_u = V_u(支承面) − w_u d"])
    g.line(cx-150, 150, cx-175, 150, INK, 2.2); g.line(cx-175, 150, cx-175, 440, INK, 2.2); g.arrow(cx-175, 440, cx-140, 440, INK, 2.2)
    g.text(cx-165, 135, "任一否", 16, RED, "start")
    box(cx, 440, 280, 60, "", RED, RBG, 18, ["V_u = V_u(支承面)"])
    g.line(cx+140, 330, 390, 330, INK, 2.2); g.line(cx+140, 440, 390, 440, INK, 2.2)
    g.line(390, 440, 390, 130, INK, 2.2); g.arrow(390, 130, 448, 130, INK, 2.2)
    g.text(cx, 560, "V_u 定案 → 進關卡 2", 17, MUTED, "middle")
    # column 2: gate2
    cx = 590
    g.text(cx, 36, "關卡 2", 22, BLU, "middle", "bold")
    dia(cx, 130, 280, 120, ["耐震塑鉸區？", "（兩條件皆成立）"], BLU)
    g.line(cx+140, 130, cx+185, 130, INK, 2.2); g.text(cx+150, 118, "是", 16, RED)
    box(cx+260, 130, 150, 56, "V_c = 0", RED, RBG, 19)
    g.arrow(cx, 190, cx, 250, INK, 2.2); g.text(cx+10, 225, "否", 16, INK)
    dia(cx, 310, 280, 120, ["有軸力 N_u？"], BLU)
    g.line(cx+140, 310, cx+185, 310, INK, 2.2); g.text(cx+150, 298, "有", 16, BLU)
    box(cx+260, 310, 150, 80, "", BLU, BBG, 16, ["×(1+N_u/140A_g)", "或 /35A_g"])
    g.arrow(cx, 370, cx, 420, INK, 2.2); g.text(cx+10, 400, "無", 16, INK)
    dia(cx, 480, 280, 120, ["給 ρ_w、M_u？", "要求精算？"], BLU)
    g.line(cx+140, 480, cx+185, 480, INK, 2.2); g.text(cx+150, 468, "是", 16, GRN)
    box(cx+260, 480, 150, 60, "詳細式", GRN, GBG, 18)
    g.arrow(cx, 540, cx, 600, INK, 2.2); g.text(cx+10, 575, "否", 16, INK)
    box(cx, 640, 260, 70, "", TEAL, GBG, 18, ["簡化式 0.53√f'_c b_w d"])
    g.line(cx, 675, cx, 740, INK, 2.2); g.arrow(cx, 740, 1018, 740, INK, 2.2)
    for yy in (130, 310, 480): g.line(cx+335, yy, 960, yy, INK, 2)
    g.line(960, 130, 960, 740, INK, 2)
    # column 3: gate3
    cx = 1170
    g.text(cx, 836, "關卡 3（由下往上）", 20, ORG, "middle", "bold")
    box(cx, 740, 300, 60, "V_s = V_u/φ − V_c", INK, "#FFFFFF", 19)
    g.arrow(cx, 710, cx, 620, INK, 2.2)
    dia(cx, 560, 300, 120, ["V_s > 2.12√f'_c b_w d", "（4V_c）？"], ORG)
    g.line(cx+150, 560, cx+200, 560, INK, 2.2); g.text(cx+160, 548, "是", 16, RED)
    box(cx+260, 560, 120, 80, "", RED, RBG, 17, ["加大斷面", "或 f'_c"])
    g.arrow(cx, 500, cx, 440, INK, 2.2); g.text(cx+10, 475, "否", 16, INK)
    dia(cx, 380, 300, 120, ["V_s > 1.06√f'_c b_w d", "（2V_c）？"], ORG)
    g.line(cx+150, 380, cx+200, 380, INK, 2.2); g.text(cx+160, 368, "是", 16, ORG)
    box(cx+260, 380, 120, 60, "s_{max} = d/4", ORG, OBG, 17)
    g.arrow(cx, 320, cx, 270, INK, 2.2); g.text(cx+10, 300, "否", 16, INK)
    box(cx, 240, 200, 56, "s_{max} = d/2", GRN, GBG, 18)
    # gate 4
    g.text(cx, 100, "關卡 4", 22, GRN, "middle", "bold")
    g.arrow(cx, 212, cx, 180, INK, 2.2); g.line(cx+260, 350, cx+260, 150, INK, 2); g.arrow(cx+260, 150, cx+190, 150, INK, 2)
    box(cx, 150, 360, 56, "s = min(強度, s_{max}, A_{v,min}) → 取整", GRN, GBG, 17)
    g.save("figs/fig19_flow.svg")
