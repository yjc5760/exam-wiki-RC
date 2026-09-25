"""公式 → 向量 SVG（matplotlib mathtext，文字轉路徑）；數字一律取自 params.py"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, json
from PIL import Image
from params import *
plt.rcParams["svg.fonttype"] = "path"; plt.rcParams["mathtext.fontset"] = "cm"
M = {
 "m_vn": r"$V_n = V_c + V_s$",
 "m_vc": r"$V_c = 0.53\sqrt{f'_c}\,b_w\,d$",
 "m_vs": r"$V_s = n\,A_v f_{yt} = \dfrac{d}{s}\,A_v f_{yt} = \dfrac{A_v f_{yt}\,d}{s}$",
 "m_vs15": rf"$V_s = \dfrac{{(2.534)(4200)(50)}}{{15}} = {VS15:.2f}\ \mathrm{{tf}}$",
 "m_strut": r"$f_d = \dfrac{V}{b_w\,jd\,\sin\theta\cos\theta} \ =\  \dfrac{2V}{b_w\,jd}$",
 "m_strutd": rf"$f_d = \dfrac{{2\,({VN_MAX:.2f}\times 10^3)}}{{(30)(45)}} = {FD_MAX:.1f} \approx {FD_MAX_R:.2f}\,f'_c$",
 "m_vsmax": r"$V_s \leq 2.12\sqrt{f'_c}\,b_w d = 4\,V_c \ \ \Leftrightarrow\ \ V_u \leq 5\,\phi V_c$",
 "m_smax": r"$V_s \leq 2V_c:\ s \leq \min\!\left(\dfrac{d}{2},\,60\right);\qquad V_s > 2V_c:\ s \leq \min\!\left(\dfrac{d}{4},\,30\right)$",
 "m_req": r"$V_{s,req} = \dfrac{V_u}{\phi} - V_c,\qquad s \leq \dfrac{A_v f_{yt}\,d}{V_{s,req}}$",
 "m_req_d": rf"$V_{{s,req}} = \dfrac{{40}}{{0.75}} - {VC0:.2f} = {VS_REQ:.2f}\ \mathrm{{tf}}\ \ \Rightarrow\ \ s \leq {S_REQ:.1f}\ \mathrm{{cm}}$",
 "m_ad": r"$\dfrac{a}{d}\quad\mathrm{or}\quad \dfrac{M_u}{V_u\,d}$",
 "m_fce": r"$F_{ns} = f_{ce}A_{c},\qquad f_{ce} = 0.85\,\beta\,f'_c,\qquad \phi F_{ns} \geq F_u\ \ (\phi = 0.75)$",
 "m_stm_geo": rf"$\tan\theta = \dfrac{{{SZ:.0f}}}{{{SA_:.0f}}}\ \Rightarrow\ \theta = {STH:.1f}^\circ \ \geq 25^\circ$",
 "m_stm_c": rf"$C = \dfrac{{R}}{{\sin\theta}} = \dfrac{{{SR:.0f}}}{{\sin {STH:.1f}^\circ}} = {SC:.1f}\ \mathrm{{tf}}$",
 "m_stm_t": rf"$T = \dfrac{{R}}{{\tan\theta}} = {ST:.1f}\ \mathrm{{tf}}\ \Rightarrow\ A_s = \dfrac{{T}}{{\phi f_y}} = {SAS:.1f}\ \mathrm{{cm^2}}$",
 "m_stm_w": rf"$w_s = \dfrac{{C}}{{\phi\,(0.85)(0.75)f'_c\,b_w}} = {SW_REQ:.1f}\ \mathrm{{cm}}$",
 "m_sf": r"$V_n = \mu\,A_{vf}\,f_y \ \leq\ 0.2\,f'_c\,A_c\ \ (\mathrm{and\ other\ caps})$",
 "m_sf_d": rf"$A_{{vf}} = \dfrac{{V_u}}{{\phi\,\mu\,f_y}} = \dfrac{{60\times 10^3}}{{(0.75)(1.0)(4200)}} = {AVF_R:.2f}\ \mathrm{{cm^2}}$",
 "m_sf_cap": rf"$\phi\,(0.2 f'_c A_c) = 0.75\,(0.2)(280)(1800) = {PFVN_CAP:.1f}\ \mathrm{{tf}} \geq 60\ \checkmark$",
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
