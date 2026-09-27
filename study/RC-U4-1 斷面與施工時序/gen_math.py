"""公式 → 向量 SVG（matplotlib mathtext）；數字一律取自 params.py"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, json
from PIL import Image
from params import *
plt.rcParams["svg.fonttype"] = "path"; plt.rcParams["mathtext.fontset"] = "cm"
c = lambda v: f"{v:,.0f}".replace(",", "{,}")
M = {
 "m_ybar": rf"$y_b = \dfrac{{\Sigma A_i\,y_i}}{{\Sigma A_i}} = \dfrac{{{c(AS)}\times{YS} + {c(A1)}\times{YB1:.0f}}}{{{c(AC)}}} = {YBC:.2f}\ \mathrm{{cm}}$",
 "m_ic": rf"$I_c = \Sigma I_i + \Sigma A_i d_i^2 = {c(I1+IS)} + {c(A1*D1**2+AS*DS**2)} = {c(IC)}\ \mathrm{{cm^4}}$",
 "m_sc": rf"$S_{{b}} = \dfrac{{I_c}}{{{YBC:.2f}}} = {c(SBC)},\quad S_{{t,\mathrm{{beam}}}} = \dfrac{{I_c}}{{{YTC_B:.2f}}} = {c(STC_B)},\quad S_{{t,\mathrm{{slab}}}} = \dfrac{{I_c}}{{{YTC_S:.2f}}} = {c(STC_S)}$",
 "m_kb": r"$f_{\mathrm{top}} = \dfrac{P}{A} - \dfrac{P\,e}{S_t} = 0 \ \Rightarrow\ e = \dfrac{S_t}{A} = k_b\ \ (\mathrm{below\ centroid})$",
 "m_kt": r"$f_{\mathrm{bot}} = \dfrac{P}{A} - \dfrac{P\,e'}{S_b} = 0 \ \Rightarrow\ e' = \dfrac{S_b}{A} = k_t\ \ (\mathrm{above\ centroid})$",
 "m_kform": r"$f_{\mathrm{top}} = \dfrac{P}{A}\left(1 - \dfrac{e}{k_b}\right),\qquad f_{\mathrm{bot}} = \dfrac{P}{A}\left(1 + \dfrac{e}{k_t}\right)$",
 "m_kex": rf"$f_{{\mathrm{{top}}}} = {PE/A1:.2f}\left(1 - \dfrac{{25}}{{{K1:.2f}}}\right) = {KERN[E1][0]:.2f}\ \mathrm{{kgf/cm^2}}$",
 "m_ec": rf"$e_c = y_{{b,c}} - y_{{ps}} = {YBC:.2f} - {YPS:.0f} = {EC:.2f}\ \mathrm{{cm}}$",
 "m_mg": rf"$M_G = \dfrac{{w_G L^2}}{{8}} = \dfrac{{{WG:.3f}\times 12^2}}{{8}} = {MG:.3f}\ \mathrm{{t\!\cdot\!m}}$",
 "m_ms": rf"$M_S = \dfrac{{w_S L^2}}{{8}} = \dfrac{{{WS:.3f}\times 12^2}}{{8}} = {MS:.3f}\ \mathrm{{t\!\cdot\!m}}$",
 "m_ml": rf"$M_L = \dfrac{{w_L L^2}}{{8}} = \dfrac{{{WL:.2f}\times 12^2}}{{8}} = {ML:.2f}\ \mathrm{{t\!\cdot\!m}}$",
 "m_s1": rf"$\Delta f_{{b,1}} = +\dfrac{{P_i}}{{A_1}} + \dfrac{{P_i e}}{{S_1}} - \dfrac{{M_G}}{{S_1}} = {PI/A1:.2f} + {PI*E1/S1:.2f} - {MG*tm/S1:.2f} = +{S1B:.2f}$",
 "m_s2a": rf"$\Delta f_{{b,2a}} = \dfrac{{\Delta P}}{{A_1}} + \dfrac{{\Delta P\,e}}{{S_1}} = \dfrac{{-30{{,}}000}}{{{c(A1)}}} + \dfrac{{-30{{,}}000\times25}}{{{c(S1)}}} = {LOSS_B:.2f}$",
 "m_s2b": rf"$\Delta f_{{b,2b}} = -\dfrac{{M_S}}{{S_1}} = -\dfrac{{{MS:.2f}\times10^5}}{{{c(S1)}}} = {MS_B:.2f}$",
 "m_s3": rf"$\Delta f_{{b,3}} = -\dfrac{{M_L}}{{S_{{b,c}}}} = -\dfrac{{{ML:.1f}\times10^5}}{{{c(SBC)}}} = {ML_B:.2f}$",
 "m_sum": rf"$f_b = {S1B:.2f} {LOSS_B:.2f} {MS_B:.2f} {ML_B:.2f} = +{FT_B:.2f}\ \geq\ -{FTS_A:.2f}\quad \mathrm{{OK}}$",
 "m_mlx": rf"$M_{{L,\max}} = (f_{{b,2}} + f_{{ts}})\,S_{{b,c}} = ({S2B:.2f} + {FTS_A:.2f})\times {c(SBC)} = {MLX_C:.2f}\ \mathrm{{t\!\cdot\!m}}$",
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
