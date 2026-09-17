#!/usr/bin/env python3
"""RC-U1-2 示範柱 —— 全篇圖上數字的唯一來源。

示範柱：60×60 cm 矩形締箍柱，8-#9(D29) 三排 3/2/3，d' = 6 cm
        f'c = 280 kgf/cm^2、fy = 4200 kgf/cm^2、Es = 2.04e6 kgf/cm^2
改這裡的常數，所有圖與所有數字一起變。
"""
import math

# ── 輸入常數 ────────────────────────────────────────────────
B = H = 60.0            # cm
FC = 280.0              # kgf/cm^2
FY = 4200.0             # kgf/cm^2
ES = 2.04e6             # kgf/cm^2
EPS_CU = 0.003
DP = 6.0                # 保護層至鋼筋中心
AB = 6.47               # #9 (D29) 單根面積 cm^2
NBAR = (3, 2, 3)        # 上排 / 中排 / 下排 根數

LAYERS = [(DP, NBAR[0] * AB), (H / 2, NBAR[1] * AB), (H - DP, NBAR[2] * AB)]
DT = H - DP
AST = sum(a for _, a in LAYERS)
RHO = AST / (B * H)
EPS_Y = FY / ES
CB = 6120.0 / (6120.0 + FY) * DT          # kgf/cm^2 制的平衡點中性軸


def beta1(fc=FC):
    if fc <= 280.0:
        return 0.85
    return max(0.65, 0.85 - 0.05 * (fc - 280.0) / 70.0)


B1 = beta1()


def engine(c):
    """唯一計算引擎：給 c，回傳 (Pn[tf], Mn[tf-m], 各排明細, eps_t 拉應變(正值))。"""
    a = min(B1 * c, H)
    Cc = 0.85 * FC * a * B                      # kgf
    Pn, Mn = Cc, Cc * (H / 2 - a / 2)
    rows = []
    for d, A in LAYERS:
        eps = EPS_CU * (c - d) / c               # 壓為正
        fs = max(-FY, min(FY, ES * eps))
        inside = d <= a
        F = A * (fs - 0.85 * FC) if inside else A * fs
        Pn += F
        Mn += F * (H / 2 - d)
        rows.append(dict(d=d, A=A, eps=eps, fs=fs, F=F / 1000.0, inside=inside,
                         arm=H / 2 - d))
    eps_t = -EPS_CU * (c - DT) / c               # 最外排拉應變，拉為正
    if abs(eps_t) < 1e-12:
        eps_t = 0.0
    return Pn / 1000.0, Mn / 1e5, rows, eps_t    # tf, tf-m


def phi(eps_t):
    if eps_t >= 0.005:
        return 0.90
    if eps_t <= EPS_Y:
        return 0.65
    return 0.65 + (eps_t - EPS_Y) * (0.90 - 0.65) / (0.005 - EPS_Y)


def zone(eps_t):
    if eps_t >= 0.005:
        return "拉力控制"
    if eps_t <= EPS_Y:
        return "壓力控制"
    return "過渡區"


PO = (0.85 * FC * (B * H - AST) + FY * AST) / 1000.0     # tf
PN_MAX = 0.80 * PO                                        # 締箍柱


def c_for_zero_P():
    lo, hi = 1e-4, DT
    for _ in range(300):
        m = 0.5 * (lo + hi)
        if engine(m)[0] > 0:
            hi = m
        else:
            lo = m
    return 0.5 * (lo + hi)


def c_for_P(target):
    """反解：給 Pn(tf)，解出 c（入口 B）。"""
    lo, hi = 1e-4, 3 * H
    for _ in range(300):
        m = 0.5 * (lo + hi)
        if engine(m)[0] < target:
            lo = m
        else:
            hi = m
    return 0.5 * (lo + hi)


def curve(n=260):
    """標稱曲線 (M, P)：由純彎（c0）掃到全斷面受壓。"""
    c0 = c_for_zero_P()
    cs = [c0 * (1 + 0.004 * i) for i in range(0, 1)]
    cs = []
    lo, hi = c0, 3.2 * H
    for i in range(n):
        t = i / (n - 1)
        cs.append(lo * (hi / lo) ** t)
    out = []
    for c in cs:
        P, M, _, et = engine(c)
        out.append((M, min(P, PN_MAX), P, et, c))
    return out


def design_curve():
    """設計曲線 (φM, φP)，並套 φPn ≤ 0.80φPo 上限。"""
    cap = 0.65 * PN_MAX
    out = []
    for M, Pcapped, P, et, c in curve():
        f = phi(et)
        out.append((f * M, min(f * P, cap), et, c))
    return out


CONTROL = {}


def _build():
    c0 = c_for_zero_P()
    for key, c in (("pure_M", c0), ("balanced", CB), ("zero_strain", DT)):
        P, M, rows, et = engine(c)
        CONTROL[key] = dict(c=c, P=P, M=M, rows=rows, et=et, phi=phi(et),
                            zone=zone(et), a=B1 * c)
    # 拉力控制界限 eps_t = 0.005
    c005 = EPS_CU / (EPS_CU + 0.005) * DT
    P, M, rows, et = engine(c005)
    CONTROL["tc_limit"] = dict(c=c005, P=P, M=M, rows=rows, et=et, phi=phi(et),
                               zone=zone(et), a=B1 * c005)
    CONTROL["pure_P"] = dict(c=float("inf"), P=PO, M=0.0, rows=[], et=-EPS_CU,
                             phi=0.65, zone="壓力控制", a=H)


_build()

# 入口 B 示範：給定 Pu = 350 tf（φ=0.65 ⇒ Pn = 538.5 tf）
PU_DEMO = 350.0
PN_DEMO = PU_DEMO / 0.65
C_DEMO = c_for_P(PN_DEMO)
P_DEMO, M_DEMO, ROWS_DEMO, ET_DEMO = engine(C_DEMO)
PHI_DEMO = phi(ET_DEMO)
E_DEMO = M_DEMO * 100 / P_DEMO          # 偏心距 cm

if __name__ == "__main__":
    print(f"斷面 {B:.0f}x{H:.0f} cm, f'c={FC:.0f}, fy={FY:.0f}, beta1={B1:.3f}")
    print(f"Ast={AST:.2f} cm2, rho_g={RHO*100:.2f}%, dt={DT:.0f}, "
          f"eps_y={EPS_Y:.5f}, cb={CB:.2f} cm")
    print(f"Po={PO:.1f} tf, 0.80Po={PN_MAX:.1f} tf, phi*0.80Po={0.65*PN_MAX:.1f} tf")
    print("-" * 78)
    for k in ("pure_M", "tc_limit", "balanced", "zero_strain", "pure_P"):
        d = CONTROL[k]
        print(f"{k:12s} c={d['c']:7.2f} a={d['a']:6.2f} Pn={d['P']:7.1f} "
              f"Mn={d['M']:7.2f} et={d['et']:+.5f} {d['zone']:5s} phi={d['phi']:.3f} "
              f"| phiPn={d['phi']*d['P']:7.1f} phiMn={d['phi']*d['M']:6.2f}")
    print("-" * 78)
    print("平衡點各排明細：")
    for r in CONTROL["balanced"]["rows"]:
        print(f"  d={r['d']:5.1f} A={r['A']:6.2f} eps={r['eps']:+.5f} "
              f"fs={r['fs']:+8.1f} F={r['F']:+8.1f} tf arm={r['arm']:+5.1f} "
              f"{'(扣 0.85fc)' if r['inside'] else ''}")
    print("-" * 78)
    print(f"Mb / M0 = {CONTROL['balanced']['M'] / CONTROL['pure_M']['M']:.2f} 倍")
    print(f"入口B 示範: Pu={PU_DEMO:.0f} tf -> Pn={PN_DEMO:.1f}, c={C_DEMO:.2f}, "
          f"Mn={M_DEMO:.2f}, et={ET_DEMO:+.5f}, phi={PHI_DEMO:.3f}, "
          f"phiMn={PHI_DEMO*M_DEMO:.2f}, e={E_DEMO:.1f} cm")
