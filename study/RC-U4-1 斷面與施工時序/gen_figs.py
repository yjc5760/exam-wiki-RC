"""RC-U4-1 拼圖三：斷面與施工時序 — 向量圖（所有數值由 params.py 算出）"""
import math
from helpers import *
from params import *

TEAL = "#2C6E9E"
SLABF, SLABH = "#F5EBDD", "#E0CDB0"      # 硬化版
WETF = "#F3EFE6"                          # 濕版
LIM = "#7A3E9D"


def hatch2(g, x, y, w, h, fill=CONC, hc=HATCH, step=16):
    g.rect(x, y, w, h, fill=fill, stroke="none")
    k = -h
    while k < w:
        x1, y1, x2, y2 = x + k, y + h, x + k + h, y
        if x1 < x: y1 -= (x - x1); x1 = x
        if x2 > x + w: y2 += (x2 - (x + w)); x2 = x + w
        if x2 > x1: g.line(x1, y1, x2, y2, hc, 1)
        k += step


def beam(g, x, y, w, h, sw=2.2):
    hatch2(g, x, y, w, h); g.rect(x, y, w, h, fill="none", stroke=INK, sw=sw)


def slab(g, x, y, w, h, state="hard", sw=2.2):
    if state == "hard":
        hatch2(g, x, y, w, h, SLABF, SLABH); g.rect(x, y, w, h, fill="none", stroke=INK, sw=sw)
    else:
        g.rect(x, y, w, h, fill=WETF, stroke="#8C96A3", sw=2, dash="9 6")


def tendon(g, x, y, r=7): g.circle(x, y, r, fill=ORG, stroke=W, sw=2)


def cline(g, x1, x2, y, lab=None, col=ORG, size=16, side="end"):
    g.line(x1, y, x2, y, col, 2.4, dash="12 7")
    if lab:
        if side == "end": g.text(x2 + 8, y + 6, lab, size, col, weight="bold")
        else: g.text(x1 - 8, y + 6, lab, size, col, anchor="end", weight="bold")


def dimv(g, x, y1, y2, lab, col=MUTED, size=15, side="left"):
    g.line(x, y1, x, y2, col, 1.4)
    for yy in (y1, y2): g.line(x - 7, yy, x + 7, yy, col, 1.4)
    ym = (y1 + y2)/2
    if side == "left": g.text(x - 10, ym + 5, lab, size, col, anchor="end", weight="bold")
    else: g.text(x + 10, ym + 5, lab, size, col, weight="bold")


def dimh(g, x1, x2, y, lab, col=MUTED, size=15):
    g.line(x1, y, x2, y, col, 1.4)
    for xx in (x1, x2): g.line(xx, y - 7, xx, y + 7, col, 1.4)
    g.text((x1 + x2)/2, y - 9, lab, size, col, anchor="middle", weight="bold")


def f2(v): return f"{v:,.2f}"
def f0(v): return f"{v:,.0f}"


# ───────── fig01 總覽 ─────────
def fig01():
    g = SVG(1200, 440)
    card(g, 400, 20, 400, 130, NAVY, NAVY, 14)
    g.text(600, 62, "核心心法", 17, "#9FB3C8", anchor="middle", weight="bold")
    g.text(600, 98, "此刻，誰已經硬化？", 26, W, anchor="middle", weight="bold")
    g.text(600, 130, "應力分階段算完，再累加", 17, "#F2A65A", anchor="middle", weight="bold")
    cols = [("① 非對稱斷面", "S_t ≠ S_b", ["形心不在半高", "先求形心 y_b、I，再分頂底", "S 小的一側是危險面"], BLUE, BLUEBG),
            ("② 核心距", "k_t = S_b/A、k_b = S_t/A", ["P 單獨作用的臨界 e", "e 落在核心內 → 全斷面受壓", "非對稱斷面上下不等"], PUR, PURBG),
            ("③ 施工時序", "S_1 → S_c", ["濕版沒有勁度", "每階段用自己的斷面", "增量 Δf 一段段累加"], RED, REDBG)]
    for i, (t, f, items, c, bg) in enumerate(cols):
        x = 20 + i*395
        g.line(600, 150, x + 180, 190, "#AEB6C2", 2)
        card(g, x, 190, 370, 235, bg, c, 14, 2)
        g.text(x + 185, 228, t, 22, c, anchor="middle", weight="bold")
        g.text(x + 185, 264, f, 18, INK, anchor="middle", weight="bold")
        for j, it in enumerate(items):
            g.circle(x + 34, 305 + j*38, 5, fill=c, stroke="none")
            g.text(x + 50, 311 + j*38, it, 17, INK)
    g.save("figs/fig01_map.svg")


# ───────── fig02 T 形斷面幾何＋槓桿 ─────────
def fig02():
    g = SVG(1200, 460)
    s = 3.6; x0 = 150; ybot = 410
    Y = lambda y: ybot - y*s
    bw = BE*s; xl = x0; xb = x0 + (bw - B*s)/2
    slab(g, xl, Y(HC), bw, TS*s)
    beam(g, xb, Y(H), B*s, H*s)
    # 分件形心
    g.circle(xl + bw/2, Y(YS), 7, fill=TEAL); g.text(xl + bw - 10, Y(YS) + 6, "版形心 87.5", 15, TEAL, anchor="end", weight="bold")
    g.circle(xb + B*s/2, Y(YB1), 7, fill=TEAL); g.text(xb + B*s + 10, Y(YB1) + 6, "梁形心 40.0", 15, TEAL, weight="bold")
    cline(g, 60, xl + bw + 20, Y(YBC), f"組合形心 y_b = {YBC:.2f}")
    dimv(g, 110, Y(0), Y(YBC), f"{YBC:.2f}", ORG)
    dimv(g, 110, Y(YBC), Y(HC), f"{YTC_S:.2f}", ORG)
    dimv(g, xb - 20, Y(YB1), Y(YBC), f"d_1 = {D1:.2f}", TEAL, 14)
    dimv(g, xb + B*s + 70, Y(YBC), Y(YS), f"d_s = {DS:.2f}", TEAL, 14, "right")
    dimh(g, xl, xl + bw, Y(HC) - 16, f"b_e = {BE:.0f}")
    g.text(xb + B*s/2, ybot + 30, f"預鑄梁 {B:.0f}×{H:.0f}　版 {BE:.0f}×{TS:.0f}", 15, MUTED, anchor="middle")
    # 右：槓桿
    X0, X1, yl = 760, 1160, 260
    g.text(960, 50, "形心 = 面積的平衡點", 22, INK, anchor="middle", weight="bold")
    g.text(960, 82, "把斷面高度攤平成一根槓桿，面積就是砝碼", 16, MUTED, anchor="middle")
    Xp = lambda y: X0 + y/HC*(X1 - X0)
    g.line(X0, yl, X1, yl, INK, 4, cap="round")
    for y in (0, 40, 80, 95):
        g.line(Xp(y), yl, Xp(y), yl + 10, INK, 1.5); g.text(Xp(y), yl + 30, f"{y}", 14, MUTED, anchor="middle")
    for yy, a, c, lab in [(YB1, A1, BLUE, "梁"), (YS, AS, "#B7791F", "版")]:
        hgt = a/3200*110; wd = 52
        g.rect(Xp(yy) - wd/2, yl - hgt, wd, hgt, fill=c, stroke="none", rx=4, op=0.85)
        g.text(Xp(yy), yl - hgt - 12, f"{lab} A = {a:.0f}", 16, c, anchor="middle", weight="bold")
    xf = Xp(YBC)
    g.poly([(xf, yl + 2), (xf - 18, yl + 34), (xf + 18, yl + 34)], ORG, 2, fill=ORG, closed=True)
    g.text(xf, yl + 62, f"支點 {YBC:.2f}（距梁底）", 17, ORG, anchor="middle", weight="bold")
    card(g, 760, 350, 400, 90, ORGBG if False else "#FCEEE5", "#EBC3A5", 10)
    g.text(960, 385, f"比半高 {HC/2:.1f} 高 {YBC - HC/2:.2f} cm", 18, ORG, anchor="middle", weight="bold")
    g.text(960, 418, "版的面積被放在最上面 → 形心被往上拉", 16, INK, anchor="middle")
    g.save("figs/fig02_tsec.svg")


# ───────── fig03 非對稱 → 三個 S、三個應力 ─────────
def fig03():
    g = SVG(1200, 460)
    s = 3.6; x0 = 60; ybot = 420
    Y = lambda y: ybot - y*s
    bw = BE*s*0.62; xb = x0 + (bw - B*s)/2
    slab(g, x0, Y(HC), bw, TS*s); beam(g, xb, Y(H), B*s, H*s)
    cline(g, x0 - 10, x0 + bw + 10, Y(YBC))
    g.text(x0 + bw/2, Y(YBC) - 10, "形心", 15, ORG, anchor="middle", weight="bold")
    # 應力圖
    xs, sc = 520, 3.0
    g.text(xs, Y(HC) - 22, f"M_L = {ML:.1f} t-m 單獨作用", 17, INK, anchor="middle", weight="bold")
    stress(g, xs, Y(HC), Y(0), ML_S, ML_B, sc)
    g.line(xs - 10, Y(H), xs + ML_T*sc + 8, Y(H), MUTED, 1.2, dash="4 3")
    g.text(xs + ML_S*sc + 10, Y(HC) + 6, f"版頂 {sg(ML_S)}", 16, BLUE, weight="bold")
    g.text(xs + ML_T*sc + 12, Y(H) + 6, f"梁頂 {sg(ML_T)}", 16, BLUE, weight="bold")
    g.text(xs + ML_B*sc - 10, Y(0) + 6, f"底 {sg(ML_B)}", 17, RED, anchor="end", weight="bold")
    # S 橫條
    X = 730
    g.text(X, 56, "三個纖維、三個斷面模數", 20, INK, weight="bold")
    rows = [("版頂 S_t = I / 35.39", STC_S, ML_S, BLUE), ("梁頂 S_t = I / 20.39", STC_B, ML_T, BLUE),
            ("梁底 S_b = I / 59.61", SBC, ML_B, RED)]
    for i, (lab, S, f, c) in enumerate(rows):
        y = 95 + i*78
        g.text(X, y, lab, 16, INK, weight="bold")
        w = S/STC_B*300
        g.rect(X, y + 12, w, 26, fill=c, stroke="none", rx=4, op=0.75)
        g.text(X + w + 10, y + 32, f"{f0(S)} cm³", 15, INK, weight="bold")
    card(g, X, 340, 440, 100, REDBG, RED, 10, 1.6)
    g.text(X + 20, 374, "S 最小 → 應力最大 → 梁底是危險面", 18, RED, weight="bold")
    g.text(X + 20, 408, f"S_b 只有梁頂 S_t 的 1/{STC_B/SBC:.1f}；距形心最遠的纖維", 15, INK)
    g.text(X + 20, 430, "y 最大、S = I/y 最小", 15, INK)
    g.save("figs/fig03_asym.svg")


# ───────── fig04 核心距（矩形） ─────────
def fig04():
    g = SVG(1200, 470)
    yt, yb = 90, 390; s = (yb - yt)/H
    Y = lambda y: yb - y*s
    # 斷面＋核心
    x0 = 90; w = 150
    beam(g, x0, yt, w, yb - yt)
    g.rect(x0, Y(YB1 + K1), w, 2*K1*s, fill=ORG, stroke="none", op=0.18)
    g.line(x0, Y(YB1 + K1), x0 + w, Y(YB1 + K1), ORG, 2, dash="7 5")
    g.line(x0, Y(YB1 - K1), x0 + w, Y(YB1 - K1), ORG, 2, dash="7 5")
    g.text(x0 + w/2, Y(YB1) + 6, "核心區", 17, ORG, anchor="middle", weight="bold")
    g.text(x0 + w/2, Y(YB1 + K1) - 8, f"k_t = {K1:.2f}", 15, ORG, anchor="middle", weight="bold")
    g.text(x0 + w/2, Y(YB1 - K1) + 22, f"k_b = {K1:.2f}", 15, ORG, anchor="middle", weight="bold")
    g.text(x0 + w/2, 60, f"斷面 {B:.0f}×{H:.0f}", 18, INK, anchor="middle", weight="bold")
    g.text(x0 + w/2, 425, "中三分之一（h/6 上下）", 15, MUTED, anchor="middle")
    sc = 1.15
    cases = [(0.0, "e = 0", "全斷面均勻受壓"), (K1, "e = k_b = 13.33", "頂纖維恰為 0"), (E1, "e = 25（本例）", "頂纖維出現拉應力")]
    for i, (e, t, sub) in enumerate(cases):
        xc = 380 + i*280
        g.text(xc + 50, 50, t, 18, INK, anchor="middle", weight="bold")
        g.text(xc + 50, 76, sub, 15, MUTED, anchor="middle")
        beam(g, xc - 40, yt, 34, yb - yt, 1.6)
        g.line(xc - 52, Y(YB1), xc + 6, Y(YB1), AX, 1.4, dash="5 4")
        tendon(g, xc - 23, Y(YB1 - e), 6)
        ft, fb = KERN[e]
        stress(g, xc + 20, yt, yb, ft, fb, sc)
        vlab(g, xc + 50, 425, ft, "頂 ", 16); vlab(g, xc + 50, 452, fb, "底 ", 16)
    g.save("figs/fig04_kern.svg")


# ───────── fig05 核心距（矩形 vs T） ─────────
def fig05():
    g = SVG(1200, 460)
    s = 3.5; ybot = 400
    Y = lambda y: ybot - y*s
    # 矩形
    xr = 170
    g.text(xr + B*s/2, 50, "矩形 40×80：上下對稱", 19, INK, anchor="middle", weight="bold")
    beam(g, xr, Y(H), B*s, H*s)
    g.rect(xr, Y(YB1 + K1), B*s, 2*K1*s, fill=ORG, stroke="none", op=0.2)
    cline(g, xr - 30, xr + B*s + 30, Y(YB1))
    dimv(g, xr + B*s + 40, Y(YB1), Y(YB1 + K1), f"k_t {K1:.2f}", ORG, 15, "right")
    dimv(g, xr + B*s + 40, Y(YB1 - K1), Y(YB1), f"k_b {K1:.2f}", ORG, 15, "right")
    tendon(g, xr + B*s/2, Y(YPS))
    g.text(xr + B*s/2, Y(YPS) + 34, f"e_1 = {E1:.0f} > k_b", 15, RED, anchor="middle", weight="bold")
    # T
    xt = 560; bw = BE*s*0.55; xb = xt + (bw - B*s)/2
    g.text(xt + bw/2, 50, "組合 T 形：核心偏向寬的一邊", 19, INK, anchor="middle", weight="bold")
    slab(g, xt, Y(HC), bw, TS*s); beam(g, xb, Y(H), B*s, H*s)
    g.rect(xt, Y(YBC + KTC), bw, (KTC + KBC)*s, fill=ORG, stroke="none", op=0.2)
    cline(g, xt - 20, xt + bw + 20, Y(YBC))
    dimv(g, xt + bw + 30, Y(YBC), Y(YBC + KTC), f"k_t = S_b/A = {KTC:.2f}", ORG, 15, "right")
    dimv(g, xt + bw + 30, Y(YBC - KBC), Y(YBC), f"k_b = S_t/A = {KBC:.2f}", ORG, 15, "right")
    tendon(g, xb + B*s/2, Y(YPS))
    g.text(xb + B*s/2, Y(YPS) + 34, f"e_c = {EC:.2f} > k_b", 15, RED, anchor="middle", weight="bold")
    card(g, 930, 300, 250, 140, PURBG, "#C9BCEB", 10)
    g.text(1055, 332, "為什麼 k_b 較大？", 16, PUR, anchor="middle", weight="bold")
    for j, t in enumerate([f"頂纖維離形心近（{YTC_S:.2f} < {YBC:.2f}）", "y_t 小 → S_t = I/y_t 大", "→ k_b = S_t/A 大", "鋼腱要放更低才讓頂纖維受拉"]):
        g.text(1055, 362 + j*22, t, 14, INK, anchor="middle")
    g.save("figs/fig05_kernT.svg")


# ───────── fig06 施工三階段 ─────────
def fig06():
    g = SVG(1200, 450)
    s = 2.35
    data = [("① 張拉／放張", "預鑄梁獨自受力", None, YB1, "斷面 1：A_1、S_1", f"P_i ＋ 梁自重 M_G", E1),
            ("② 澆置現場版", "濕版只是重量", "wet", YB1, "斷面 1：A_1、S_1", "P_e ＋ 濕版重 M_S 累加", E1),
            ("③ 版硬化後", "梁版共同作用", "hard", YBC, "組合斷面：A_c、S_c", "只再承受 M_L", EC)]
    for i, (t, sub, st, yc, sec, load, e) in enumerate(data):
        x = 20 + i*395
        card(g, x, 20, 370, 410, PANEL, "#D5DAE1", 12)
        g.text(x + 185, 58, t, 21, INK, anchor="middle", weight="bold")
        g.text(x + 185, 86, sub, 15, MUTED, anchor="middle")
        ybot = 325; Y = lambda y: ybot - y*s
        bw = BE*s*0.85; xs = x + 185 - bw/2; xb = x + 185 - B*s/2
        if st: slab(g, xs, Y(HC), bw, TS*s, st)
        if st == "wet": g.text(x + 185, Y(HC) + TS*s/2 + 5, "濕版（無勁度，不計入）", 14, MUTED, anchor="middle")
        beam(g, xb, Y(H), B*s, H*s)
        tendon(g, x + 185, Y(YPS), 6)
        cline(g, x + 40, x + 330, Y(yc))
        g.text(x + 330, Y(yc) - 8, f"y_b = {yc:.2f}", 14, ORG, anchor="end", weight="bold")
        g.text(x + 185, 355, sec, 17, GREEN, anchor="middle", weight="bold")
        g.text(x + 185, 383, load, 16, INK, anchor="middle")
        g.text(x + 185, 410, f"e = {e:.2f} cm", 16, ORG, anchor="middle", weight="bold")
        if i < 2: g.arrow(x + 374, 220, x + 392, 220, MUTED, 3, 12)
    g.save("figs/fig06_stages.svg")


# ───────── fig07 濕版重陷阱 ─────────
def fig07():
    g = SVG(1200, 460)
    s = 1.75
    for i, (ok, t, sub, S, v) in enumerate([(True, "正確：用預鑄梁 S_1", "梁已硬化，濕版只是掛在梁上的重量", S1, MS_B),
                                          (False, "錯誤：用組合斷面 S_{b,c}", "版還是液體，根本無法參與抗彎", SBC, MS_B_WRONG)]):
        x = 20 + i*600; c = GREEN if ok else RED; bg = GREENBG if ok else REDBG
        card(g, x, 15, 560, 320, bg, c, 12, 1.6)
        g.text(x + 280, 50, ("○ " if ok else "× ") + t, 20, c, anchor="middle", weight="bold")
        g.text(x + 280, 78, sub, 15, MUTED, anchor="middle")
        ybot = 315; Y = lambda y: ybot - y*s; bw = BE*s*0.8; xs = x + 200 - bw/2; xb = x + 200 - B*s/2
        slab(g, xs, Y(HC), bw, TS*s, "wet"); beam(g, xb, Y(H), B*s, H*s); tendon(g, x + 200, Y(YPS), 5)
        for k in range(5):
            xx = xs + 15 + k*(bw - 30)/4
            g.arrow(xx, Y(HC) - 36, xx, Y(HC) - 4, RED, 1.8, 9)
        g.text(x + 200, Y(HC) - 44, f"w_S = {WS*1000:.0f} kgf/m", 14, RED, anchor="middle", weight="bold")
        # 有效斷面標示
        if ok: g.line(xb - 14, Y(H), xb - 14, Y(0), GREEN, 5, cap="round")
        else: g.line(xs - 14, Y(HC), xs - 14, Y(0), RED, 5, cap="round")
        g.text(x + 390, 150, "Δf_底 = −M_S / S", 16, INK, weight="bold")
        g.text(x + 390, 178, f"S = {f0(S)}", 16, INK)
        g.text(x + 390, 222, f"{sg(v)}", 30, c, weight="bold")
        g.text(x + 390, 248, "kgf/cm²", 15, MUTED)
    # 比較條
    x0, sc = 330, 15
    g.text(60, 400, "梁底應力貢獻", 18, INK, weight="bold")
    for j, (v, c, lab) in enumerate([(MS_B, GREEN, "正確"), (MS_B_WRONG, RED, "錯誤")]):
        y = 355 + j*48
        g.rect(x0, y, -v*sc, 32, fill=c, stroke="none", rx=5, op=0.6)
        g.text(x0 - v*sc + 12, y + 23, f"{sg(v)}（{lab}）", 16, c, weight="bold")
    g.line(x0 - MS_B_WRONG*sc, 340, x0 - MS_B_WRONG*sc, 440, ORG, 2, dash="5 4")
    g.text(860, 395, f"差 {MS_B_WRONG - MS_B:.2f} kgf/cm²", 20, ORG, weight="bold")
    g.text(860, 425, "→ 低估梁底拉應力（偏不保守）", 16, ORG, weight="bold")
    g.save("figs/fig07_wet.svg")


# ───────── fig08 有無支撐 ─────────
def fig08():
    g = SVG(1200, 440)
    for i, (t, sub, v, S, note) in enumerate([
            ("無支撐施工（預設）", "濕版重量全由預鑄梁承擔", MS_B, "S_1", "M_S → 斷面 1"),
            ("有支撐施工（shored）", "濕版先由臨時支撐頂住；硬化後拆撐", MS_B_WRONG, "S_c", "M_S → 組合斷面")]):
        x = 20 + i*600; c = RED if i == 0 else GREEN
        card(g, x, 20, 560, 400, PANEL, "#D5DAE1", 12)
        g.text(x + 280, 58, t, 21, INK, anchor="middle", weight="bold")
        g.text(x + 280, 86, sub, 15, MUTED, anchor="middle")
        x1, x2, yb = x + 50, x + 510, 200
        g.rect(x1, yb - 20, x2 - x1, 12, fill=WETF, stroke="#8C96A3", sw=1.6, dash="6 4")
        g.rect(x1, yb - 8, x2 - x1, 38, fill=CONC, stroke=INK, sw=2)
        pin(g, x1 + 12, yb + 30); roller(g, x2 - 12, yb + 30)
        for k in range(7):
            xx = x1 + 30 + k*(x2 - x1 - 60)/6
            g.arrow(xx, yb - 58, xx, yb - 22, RED, 1.8, 9)
        if i == 1:
            for k in range(1, 5):
                xx = x1 + k*(x2 - x1)/5
                g.line(xx, yb + 30, xx, yb + 80, GOLD, 5)
                g.line(xx - 12, yb + 82, xx + 12, yb + 82, GOLD, 3)
            g.text(x + 280, yb + 108, "臨時支撐（拆除時把 M_S 釋放給組合斷面）", 14, GOLD, anchor="middle", weight="bold")
        else:
            g.text(x + 280, yb + 108, "梁在兩端支承下直接承受濕版", 14, MUTED, anchor="middle")
        g.text(x + 280, 345, f"{note}：梁底 Δf = −M_S / {S}", 17, INK, anchor="middle", weight="bold")
        g.text(x + 280, 390, f"{sg(v)} kgf/cm²", 26, c, anchor="middle", weight="bold")
    g.save("figs/fig08_shore.svg")


# ───────── fig09 SOP 流程 ─────────
def fig09():
    g = SVG(1200, 440)
    steps = [("Step 1", "兩套幾何", ["斷面 1：A_1、S_1、e_1", "組合：y_{b,c}、I_c、S_c、e_c"]),
             ("Step 2", "三個彎矩", ["M_G：梁自重", "M_S：濕版重", "M_L：活載＋疊加靜載"]),
             ("Step 3", "每段算 Δf", ["依右下判斷選斷面", "P、M 各配各的", "頂、底分開寫"]),
             ("Step 4", "累加比容許", ["f = Σ Δf", "梁頂、梁底、版頂", "三條分開比"])]
    for i, (a, b, items) in enumerate(steps):
        x = 20 + i*295
        card(g, x, 20, 265, 210, PURBG if i != 2 else GOLDBG, PUR if i != 2 else GOLD, 12, 2)
        g.text(x + 132, 55, a, 15, PUR if i != 2 else GOLD, anchor="middle", weight="bold")
        g.text(x + 132, 88, b, 22, INK, anchor="middle", weight="bold")
        for j, t in enumerate(items): g.text(x + 132, 128 + j*30, t, 15, INK, anchor="middle")
        if i < 3: g.arrow(x + 268, 125, x + 292, 125, MUTED, 3, 12)
    # 決策菱形
    cx, cy = 460, 340
    g.line(20 + 2*295 + 132, 230, 20 + 2*295 + 132, 262, GOLD, 2.4)
    g.arrow(20 + 2*295 + 132, 262, cx + 110, 300, GOLD, 2.4, 11)
    g.poly([(cx, cy - 70), (cx + 170, cy), (cx, cy + 70), (cx - 170, cy)], GOLD, 2.4, fill=GOLDBG, closed=True)
    g.text(cx, cy - 8, "這個載重作用時", 16, INK, anchor="middle", weight="bold")
    g.text(cx, cy + 18, "版已經硬化？", 18, INK, anchor="middle", weight="bold")
    g.arrow(cx - 170, cy, cx - 230, cy, RED, 2.6, 12); g.text(cx - 200, cy - 12, "否", 16, RED, anchor="middle", weight="bold")
    card(g, 20, cy - 45, 210, 90, REDBG, RED, 10, 1.6)
    g.text(125, cy - 10, "用斷面 1", 18, RED, anchor="middle", weight="bold")
    g.text(125, cy + 20, "P、M_G、M_S", 15, INK, anchor="middle")
    g.arrow(cx + 170, cy, cx + 230, cy, GREEN, 2.6, 12); g.text(cx + 200, cy - 12, "是", 16, GREEN, anchor="middle", weight="bold")
    card(g, cx + 235, cy - 45, 210, 90, GREENBG, GREEN, 10, 1.6)
    g.text(cx + 340, cy - 10, "用組合斷面", 18, GREEN, anchor="middle", weight="bold")
    g.text(cx + 340, cy + 20, "M_L（有支撐時含 M_S）", 15, INK, anchor="middle")
    card(g, 950, 280, 230, 120, PANEL, "#D5DAE1", 10)
    g.text(1065, 312, "版的應力只從", 15, INK, anchor="middle")
    g.text(1065, 338, "它硬化那一刻開始算", 15, INK, anchor="middle", weight="bold")
    g.text(1065, 370, "→ 版頂只有 M_L/S_t", 15, TEAL, anchor="middle", weight="bold")
    g.save("figs/fig09_sop.svg")


# ───────── fig10 分階段增量 ─────────
def fig10():
    g = SVG(1200, 470)
    s = 3.0; ybot = 395; Y = lambda y: ybot - y*s; sc = 0.95
    cols = [("① P_i ＋ M_G", "斷面 1", S1T, S1B, False),
            ("②a 預力損失", "ΔP = −30 t · 斷面 1", LOSS_T, LOSS_B, False),
            ("②b 濕版 M_S", "斷面 1", MS_T, MS_B, False),
            ("③ 活載 M_L", "組合斷面", ML_T, ML_B, True)]
    for i, (t, sub, ft, fb, comp) in enumerate(cols):
        xc = 110 + i*235
        g.text(xc + 40, 38, t, 17, INK, anchor="middle", weight="bold")
        g.text(xc + 40, 62, sub, 14, GREEN if comp else MUTED, anchor="middle", weight="bold")
        g.rect(xc - 40, Y(HC), 26, TS*s, fill=SLABF if comp else "none", stroke="#8C96A3" if not comp else INK, sw=1.4, dash=None if comp else "5 4")
        hatch2(g, xc - 40, Y(H), 26, H*s); g.rect(xc - 40, Y(H), 26, H*s, fill="none", stroke=INK, sw=1.6)
        if comp:
            stress(g, xc + 40, Y(HC), Y(0), ML_S, fb, sc)
            g.line(xc + 30, Y(H), xc + 40 + ft*sc + 6, Y(H), MUTED, 1, dash="4 3")
            g.text(xc + 40 + ML_S*sc + 6, Y(HC) + 5, f"版頂 {sg(ML_S)}", 13, BLUE, weight="bold")
            g.text(xc + 40 + ft*sc + 8, Y(H) + 18, f"{sg(ft)}", 13, BLUE, weight="bold")
        else:
            stress(g, xc + 40, Y(H), Y(0), ft, fb, sc)
        vlab(g, xc + 40, 430, ft, "梁頂 ", 15); vlab(g, xc + 40, 456, fb, "梁底 ", 15)
        g.text(xc + 157, 250, "＋" if i < 3 else "＝", 26, MUTED, anchor="middle", weight="bold")
    # 總和
    xc = 110 + 4*235 - 20
    g.text(xc + 40, 38, "總應力", 18, PUR, anchor="middle", weight="bold")
    g.text(xc + 40, 62, "Σ Δf", 14, PUR, anchor="middle", weight="bold")
    x = xc + 20
    g.poly([(x, Y(HC)), (x + FT_S*sc, Y(HC)), (x + ML_T*sc, Y(H)), (x, Y(H))], BLUE, 2.2, fill=BLUEF, closed=True)
    g.poly([(x, Y(H)), (x + FT_T*sc, Y(H)), (x + FT_B*sc, Y(0)), (x, Y(0))], BLUE, 2.2, fill=BLUEF, closed=True)
    g.line(x, Y(HC) - 6, x, Y(0) + 6, AX, 2)
    g.text(x + FT_S*sc + 6, Y(HC) + 5, f"{sg(FT_S)}", 13, BLUE, weight="bold")
    g.text(x + FT_T*sc + 6, Y(H) + 5, f"{sg(FT_T)}", 13, BLUE, weight="bold")
    vlab(g, xc + 40, 430, FT_T, "梁頂 ", 15); vlab(g, xc + 40, 456, FT_B, "梁底 ", 15)
    g.save("figs/fig10_inc.svg")


# ───────── fig11 瀑布圖：梁頂與梁底 ─────────
def fig11():
    g = SVG(1200, 460)
    for p, (t, vals, lims) in enumerate([("梁底纖維", [S1B, LOSS_B, MS_B, ML_B], (FCS_A, -FTS_A)),
                                         ("梁頂纖維", [S1T, LOSS_T, MS_T, ML_T], (FCS_A, -FTS_A))]):
        x0 = 30 + p*600; w = 560
        card(g, x0, 15, w, 430, PANEL, "#D5DAE1", 12)
        g.text(x0 + 24, 50, t, 20, INK, weight="bold")
        y0 = 290 if p == 0 else 330; sc = 2.0
        Yv = lambda v: y0 - v*sc
        g.line(x0 + 30, y0, x0 + w - 20, y0, AX, 1.6); g.text(x0 + 26, y0 + 5, "0", 13, MUTED, anchor="end")
        g.line(x0 + 30, Yv(-FTS_A), x0 + w - 20, Yv(-FTS_A), LIM, 1.6, dash="7 5")
        g.text(x0 + 40, Yv(-FTS_A) - 8, f"容許拉 −{FTS_A:.2f}", 13, LIM, weight="bold")
        labs = ["①", "損失", "濕版", "活載", "合計"]
        cum = 0; bw = 70
        for j, v in enumerate(vals + [None]):
            xb = x0 + 60 + j*96
            if v is None:
                a, b, c = 0, cum, PUR
            else:
                a, b = cum, cum + v; c = BLUE if v >= 0 else RED; cum = b
            top, bot = max(Yv(a), Yv(b)), min(Yv(a), Yv(b))
            g.rect(xb, bot, bw, top - bot, fill=c, stroke="none", rx=3, op=0.8 if v is None else 0.65)
            if v is not None and j < 4:
                g.line(xb + bw, Yv(b), xb + 96, Yv(b), MUTED, 1.2, dash="3 3")
            txt = sg(v if v is not None else cum)
            g.text(xb + bw/2, bot - 8, txt, 14, c, anchor="middle", weight="bold")
            g.text(xb + bw/2, 425, labs[j], 15, INK, anchor="middle", weight="bold")
    g.save("figs/fig11_waterfall.svg")


# ───────── fig12 總應力分布：介面不連續 ─────────
def fig12():
    g = SVG(1200, 450)
    s = 3.9; ybot = 410; Y = lambda y: ybot - y*s
    x0 = 80; bw = BE*s*0.45; xb = x0 + (bw - B*s)/2
    slab(g, x0, Y(HC), bw, TS*s); beam(g, xb, Y(H), B*s, H*s)
    x = 420; sc = 4.0
    g.poly([(x, Y(HC)), (x + FT_S*sc, Y(HC)), (x + ML_T*sc, Y(H)), (x, Y(H))], "#B7791F", 2.4, fill=SLABF, closed=True)
    g.poly([(x, Y(H)), (x + FT_T*sc, Y(H)), (x + FT_B*sc, Y(0)), (x, Y(0))], BLUE, 2.4, fill=BLUEF, closed=True)
    g.line(x, Y(HC) - 8, x, Y(0) + 8, AX, 2)
    for yy in (Y(HC), Y(H), Y(0)): g.line(xb + B*s + 10, yy, x - 6, yy, "#C3C9D2", 1, dash="3 4")
    g.text(x + FT_S*sc + 10, Y(HC) + 6, f"版頂 {sg(FT_S)}", 16, "#B7791F", weight="bold")
    g.text(x - 10, Y(H) - 8, f"版底 {sg(ML_T)}", 15, "#B7791F", anchor="end", weight="bold", bg=W)
    g.text(x + FT_T*sc + 10, Y(H) + 16, f"梁頂 {sg(FT_T)}", 16, BLUE, weight="bold")
    g.text(x + FT_B*sc + 10, Y(0) + 6, f"梁底 {sg(FT_B)}", 16, BLUE, weight="bold")
    g.arrow(x + 250, Y(H) - 62, x + (ML_T + FT_T)/2*sc, Y(H) - 3, ORG, 2.2, 11)
    g.text(x + 256, Y(H) - 66, "介面應力跳一階", 16, ORG, weight="bold")
    # 右側檢核卡
    X = 850
    g.text(X, 50, "使用階段檢核（kgf/cm²）", 19, INK, weight="bold")
    rows = [("版頂", FT_S, f"≤ +{FCS_A:.0f}"), ("梁頂", FT_T, f"≤ +{FCS_A:.0f}"), ("梁底", FT_B, f"≥ −{FTS_A:.2f}")]
    for i, (a, v, lim) in enumerate(rows):
        y = 80 + i*70
        card(g, X, y, 330, 58, W, "#D5DAE1", 8)
        g.text(X + 18, y + 37, a, 17, INK, weight="bold")
        g.text(X + 80, y + 37, sg(v), 18, BLUE, weight="bold")
        g.text(X + 190, y + 37, lim, 15, GREEN, weight="bold")
        g.text(X + 312, y + 37, "OK", 16, GREEN, anchor="end", weight="bold")
    card(g, X, 300, 330, 120, GOLDBG, "#E6CFA0", 10)
    g.text(X + 18, 332, "為什麼會跳？", 17, GOLD, weight="bold")
    g.text(X + 18, 362, "版底只記得 M_L；梁頂還帶著", 15, INK)
    g.text(X + 18, 388, "①② 階段累積的應力歷史", 15, INK)
    g.save("figs/fig12_final.svg")


# ───────── fig13 各種錯法的梁底總應力 ─────────
def fig13():
    g = SVG(1200, 420)
    rows = [("正確：分階段、各用各的斷面", FT_B, GREEN),
            ("濕版 M_S 誤用組合斷面", FB_WETWRONG, RED),
            ("一次算完：P_e、M_T 全放組合斷面", ONE_B, RED),
            ("M_L 用 I/(h/2) 當 S_b", S2B + ML_B_WRONG, RED)]
    x0, sc = 470, 18
    g.text(40, 40, "梁底最終應力（壓 ＋）：錯法全部「看起來更安全」", 20, INK, weight="bold")
    g.line(x0, 60, x0, 360, AX, 2)
    for i, (lab, v, c) in enumerate(rows):
        y = 80 + i*70
        g.text(x0 - 16, y + 30, lab, 16, c if i else GREEN, anchor="end", weight="bold")
        g.rect(x0, y + 8, v*sc, 34, fill=c, stroke="none", rx=5, op=0.7 if i else 0.85)
        g.text(x0 + v*sc + 12, y + 32, f"{sg(v)}", 18, c, weight="bold")
        if i: g.text(x0 + v*sc + 90, y + 32, f"多了 {v - FT_B:.2f} 的虛假壓應力", 15, ORG, weight="bold")
    g.line(x0 + FT_B*sc, 70, x0 + FT_B*sc, 370, GREEN, 2, dash="6 4")
    g.text(600, 405, "壓應力被高估 = 拉應力被低估 → 把會開裂的梁判成合格", 17, ORG, anchor="middle", weight="bold")
    g.save("figs/fig13_traps.svg")


# ───────── fig14 組合作用的紅利 ─────────
def fig14():
    g = SVG(1200, 420)
    g.text(40, 42, f"梁底由 {sg(S2B)}（③ 之前）開始，最多還能被拉到 −{FTS_A:.2f}", 19, INK, weight="bold")
    g.text(40, 72, f"可用應力空間 = {S2B:.2f} + {FTS_A:.2f} = {S2B + FTS_A:.2f} kgf/cm²，乘上 S_b 就是 M_L 上限", 16, MUTED)
    x0, sc = 330, 5.5
    for i, (lab, S, M, w, c) in enumerate([("沒有組合作用（S_1）", S1, MLX_N, WLX_N, MUTED),
                                         ("有組合作用（S_{b,c}）", SBC, MLX_C, WLX_C, GREEN)]):
        y = 120 + i*110
        g.text(x0 - 16, y + 30, lab, 17, c if i else INK, anchor="end", weight="bold")
        g.text(x0 - 16, y + 56, f"S = {f0(S)} cm³", 14, MUTED, anchor="end")
        g.rect(x0, y + 8, M*sc, 46, fill=c, stroke="none", rx=6, op=0.75)
        g.text(x0 + M*sc + 14, y + 30, f"M_L ≤ {M:.2f} t-m", 18, c if i else INK, weight="bold")
        g.text(x0 + M*sc + 14, y + 54, f"w_L ≤ {w:.2f} t/m", 15, INK)
    card(g, 330, 345, 620, 60, GREENBG, "#9CC7BC", 10)
    g.text(640, 383, f"同一根預鑄梁，加上一片版 → 可承受活載增加 {(MLX_C/MLX_N - 1)*100:.0f}%", 18, GREEN, anchor="middle", weight="bold")
    g.save("figs/fig14_bonus.svg")


if __name__ == "__main__":
    import os; os.makedirs("figs", exist_ok=True)
    for f in [fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10, fig11, fig12, fig13, fig14]: f()
    print("figs ok")
