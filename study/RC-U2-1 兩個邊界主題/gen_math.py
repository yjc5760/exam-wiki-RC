"""公式 → 向量 SVG（matplotlib mathtext，文字轉路徑）；數字一律取自 params.py"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, json
from PIL import Image
from params import *
plt.rcParams["svg.fonttype"] = "path"; plt.rcParams["mathtext.fontset"] = "cm"
M = {
 "m_ns": r"$\phi F_{ns} = \phi\, f_{ce} A_{cs},\qquad f_{ce} = 0.85\,\beta_s f'_c$",
 "m_nt": r"$\phi F_{nt} = \phi\, A_{ts} f_y$",
 "m_nn": r"$\phi F_{nn} = \phi\, f_{ce} A_{nz},\qquad f_{ce} = 0.85\,\beta_n f'_c$",
 "m_z": rf"$z = h - \dfrac{{w_t}}{{2}} - \dfrac{{w_{{top}}}}{{2}} = 150 - 10 - {WTOP/2:.1f} = {Z5:.1f}\ \mathrm{{cm}}$",
 "m_wtop": rf"$w_{{top}} = \dfrac{{T}}{{\phi\,(0.85 f'_c)\, b}} = \dfrac{{{T5*1000:.0f}}}{{0.75\,(238)(40)}} = {WTOP:.1f}\ \mathrm{{cm}}$",
 "m_th": rf"$\theta = \tan^{{-1}}\dfrac{{z}}{{a - l_b/4}} = \tan^{{-1}}\dfrac{{{Z5:.1f}}}{{{A5-LB_P/4:.0f}}} = {TH_DEG:.1f}^\circ \geq 25^\circ$",
 "m_f": rf"$F = \dfrac{{R}}{{\sin\theta}} = {F5:.1f}\ \mathrm{{tf}},\qquad T = \dfrac{{R}}{{\tan\theta}} = {T5:.1f}\ \mathrm{{tf}}$",
 "m_ws": rf"$w_s = l_b \sin\theta + w_t \cos\theta = 40\sin{TH_DEG:.1f}^\circ + 20\cos{TH_DEG:.1f}^\circ = {WS_B:.1f}\ \mathrm{{cm}}$",
 "m_sb": rf"$\phi F_{{ns}} = 0.75\,(178.5)({WS_B:.1f})(40) = {CAP_SB:.1f} \geq {F5:.1f}\ \mathrm{{tf}}$",
 "m_st": rf"$\phi F_{{ns}} = 0.75\,(178.5)({WS_T:.1f})(40) = {CAP_ST:.1f} \geq {F5:.1f}\ \mathrm{{tf}}$",
 "m_ats": rf"$A_{{ts}} = \dfrac{{T}}{{\phi f_y}} = \dfrac{{{T5*1000:.0f}}}{{0.75\,(4200)}} = {AS5_REQ:.2f}\ \rightarrow\ {N25}\text{{-}}D25\ ({AS5:.2f})$",
 "m_dlim": rf"$\phi V_n \leq \phi\,2.65\sqrt{{f'_c}}\,b\,d = 0.75\,(2.65)\sqrt{{280}}\,(40)(140) = {PVLIM5:.1f}\ \mathrm{{tf}}$",
 "m_5vc": r"$5V_c = 5\,(0.53)\sqrt{f'_c}\,b_w d = 2.65\sqrt{f'_c}\,b_w d$",
 "m_sf": r"$V_n = \mu\,(A_{vf} f_y + P_c)$",
 "m_avf": r"$A_{vf} = \dfrac{V_u}{\phi\,\mu\,f_y}\qquad (\phi = 0.75)$",
 "m_avf1": rf"$\mu = 1.0:\ \ A_{{vf}} = \dfrac{{45000}}{{0.75\,(1.0)(4200)}} = {AVF_R:.2f}\ \mathrm{{cm^2}}$",
 "m_avf2": rf"$\mu = 0.6:\ \ A_{{vf}} = \dfrac{{45000}}{{0.75\,(0.6)(4200)}} = {AVF_S:.2f}\ \mathrm{{cm^2}}$",
 "m_sflim": r"$V_n \leq \min\left(0.2 f'_c,\ 34 + 0.08 f'_c,\ 112\right) A_c$",
 "m_sflim1": rf"$\phi V_{{n,\max}} = 0.75\,(56)(2100) = {PVN4_MAX:.2f}\ \mathrm{{tf}} \geq {VU4:.2f}$",
 "m_tth": r"$T_u \leq \phi\,0.265\sqrt{f'_c}\,\dfrac{A_{cp}^2}{p_{cp}}$",
 "m_tth1": rf"$\phi T_{{th}} = 0.75\,(0.265)\sqrt{{280}}\,\dfrac{{2450^2}}{{210}} = {PTTH:.3f}\ \mathrm{{t\text{{-}}m}}$",
 "m_tcr": r"$T_{cr} = 1.06\sqrt{f'_c}\,\dfrac{A_{cp}^2}{p_{cp}}\qquad \phi T_{th} = \phi\,\dfrac{T_{cr}}{4}$",
}
man = {}
for k, v in M.items():
    fig = plt.figure(figsize=(0.01, 0.01))
    fig.text(0, 0, v, fontsize=28, color="#1F2A37")
    fig.savefig(f"figs/{k}.svg", bbox_inches="tight", pad_inches=0.06, transparent=True)
    fig.savefig(f"figs/{k}.png", bbox_inches="tight", pad_inches=0.06, transparent=True, dpi=200)
    plt.close(fig)
    w, h = Image.open(f"figs/{k}.png").size; man[k] = [w / 200, h / 200]
json.dump(man, open("figs/math.json", "w"), indent=1); print(len(man))
