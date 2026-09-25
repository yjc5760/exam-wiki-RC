"""公式 → 向量 SVG（matplotlib mathtext，文字轉路徑）；數字一律取自 params.py"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, json
from PIL import Image
from params import *
plt.rcParams["svg.fonttype"] = "path"; plt.rcParams["mathtext.fontset"] = "cm"
M = {
 "m_d": r"$V_u(d) = V_{u,\mathrm{face}} - w_u\,d$",
 "m_d1": rf"$V_u(d) = {VU1_F:.2f} - {W1:.0f}\,(0.63) = {VU1_D:.2f}\ \mathrm{{tf}}$",
 "m_vc": r"$V_c = 0.53\sqrt{f'_c}\,b_w\,d$",
 "m_vc1": rf"$V_c = 0.53\sqrt{{280}}\,(35)(63) = {VC:.2f}\ \mathrm{{tf}}$",
 "m_det": r"$V_c = \left(0.50\sqrt{f'_c} + 175\,\rho_w\,\dfrac{V_u d}{M_u}\right) b_w d$",
 "m_detlim": r"$\dfrac{V_u d}{M_u} \leq 1.0,\qquad V_c \leq 0.93\sqrt{f'_c}\,b_w d$",
 "m_det2": rf"$V_c = \left(0.50\sqrt{{280}} + 175\,({RHO2:.5f})({VDM2:.2f})\right)(35)(63) = {VC_DET:.2f}\ \mathrm{{tf}}$",
 "m_nc": r"$V_c = 0.53\left(1 + \dfrac{N_u}{140\,A_g}\right)\sqrt{f'_c}\,b_w d$",
 "m_nt": r"$V_c = 0.53\left(1 + \dfrac{N_u}{35\,A_g}\right)\sqrt{f'_c}\,b_w d \ \geq 0$",
 "m_nc2": rf"$V_c = {VC:.2f}\left(1 + \dfrac{{60000}}{{140\,(2450)}}\right) = {VC_NC:.2f}\ \mathrm{{tf}}$",
 "m_nt2": rf"$V_c = {VC:.2f}\left(1 - \dfrac{{60000}}{{35\,(2450)}}\right) = {VC_NT:.2f}\ \mathrm{{tf}}$",
 "m_mm": r"$M_m = M_u - N_u\,\dfrac{4h - d}{8}$",
 "m_mmcap": r"$M_m \leq 0:\ \ V_c = 0.93\sqrt{f'_c}\,b_w d\,\sqrt{1 + \dfrac{N_u}{35\,A_g}}$",
 "m_vs": r"$V_s = \dfrac{V_u}{\phi} - V_c\qquad (\phi = 0.75)$",
 "m_vs3": rf"$V_s = \dfrac{{{VU3:.2f}}}{{0.75}} - {VC:.2f} = {VS3:.2f}\ \mathrm{{tf}}$",
 "m_vs1": rf"$V_s = \dfrac{{{VU1_D:.2f}}}{{0.75}} - {VC:.2f} = {VS1:.2f}\ \mathrm{{tf}}$",
 "m_lim": r"$V_s \leq 1.06\sqrt{f'_c}\,b_w d\ (=2V_c)\qquad V_s \leq 2.12\sqrt{f'_c}\,b_w d\ (=4V_c)$",
 "m_vumax": r"$V_n \leq V_c + 4V_c = 5V_c\ \ \Rightarrow\ \ V_u \leq 5\,\phi V_c$",
 "m_vumax2": rf"$5\,\phi V_c = 5\,(0.75)({VC:.2f}) = {VU_MAX:.2f}\ \mathrm{{tf}}$",
 "m_s": r"$s \leq \dfrac{A_v\,f_{yt}\,d}{V_s}$",
 "m_s3": rf"$s \leq \dfrac{{(2.534)(4200)(63)}}{{{VS3*1000:.0f}}} = {S3_REQ:.2f}\ \mathrm{{cm}}$",
 "m_s1": rf"$s \leq \dfrac{{(2.534)(4200)(63)}}{{{VS1*1000:.0f}}} = {S1_REQ:.2f}\ \mathrm{{cm}}$",
 "m_avmin": r"$A_{v,\min} = \max\left(0.2\sqrt{f'_c}\,\dfrac{b_w s}{f_{yt}},\ 3.5\,\dfrac{b_w s}{f_{yt}}\right)$",
 "m_savmin": rf"$s \leq \dfrac{{A_v f_{{yt}}}}{{3.5\,b_w}} = \dfrac{{(2.534)(4200)}}{{3.5\,(35)}} = {S_AVMIN:.2f}\ \mathrm{{cm}}$",
 "m_x": r"$x = \dfrac{V_{u,0} - V_{\mathrm{line}}}{w_u}$",
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
