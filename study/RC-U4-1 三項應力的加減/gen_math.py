"""公式 → 向量 SVG（matplotlib mathtext，文字轉路徑）；數字一律取自 params.py"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, json
from PIL import Image
from params import *
plt.rcParams["svg.fonttype"] = "path"; plt.rcParams["mathtext.fontset"] = "cm"
c = lambda v: f"{v:,.0f}".replace(",", "{,}")
M = {
 "m_gen": r"$f = +\dfrac{P}{A} \ \pm\ \dfrac{P\,e}{S} \ \mp\ \dfrac{M}{S}$",
 "m_top": r"$f_{\mathrm{t}} = +\dfrac{P}{A} - \dfrac{P\,e}{S_t} + \dfrac{M}{S_t}$",
 "m_bot": r"$f_{\mathrm{b}} = +\dfrac{P}{A} + \dfrac{P\,e}{S_b} - \dfrac{M}{S_b}$",
 "m_S": r"$S_t = \dfrac{I}{y_t},\qquad S_b = \dfrac{I}{y_b}$",
 "m_Srect": r"$\mathrm{rectangle:}\ \ S_t = S_b = \dfrac{b\,h^2}{6}$",
 "m_A": rf"$A = 40\times 80 = {c(A)}\ \mathrm{{cm^2}},\quad S = \dfrac{{40\times 80^2}}{{6}} = {c(ST)}\ \mathrm{{cm^3}}$",
 "m_Md": rf"$M_d = \dfrac{{w_d L^2}}{{8}} = \dfrac{{0.768\times 12^2}}{{8}} = {MD:.3f}\ \mathrm{{t\!\cdot\!m}}$",
 "m_wd": r"$w_d = 0.40\times 0.80\times 2.4 = 0.768\ \mathrm{t/m}$",
 "m_t1": rf"$\dfrac{{P_i}}{{A}} = \dfrac{{150{{,}}000}}{{3{{,}}200}} = {T1:.3f}$",
 "m_t2": rf"$\dfrac{{P_i\,e}}{{S}} = \dfrac{{150{{,}}000\times 25}}{{42{{,}}667}} = {T2:.3f}$",
 "m_t3": rf"$\dfrac{{M_d}}{{S}} = \dfrac{{13.824\times 10^5}}{{42{{,}}667}} = {T3:.3f}$",
 "m_ft": rf"$f_{{\mathrm{{t}}}} = +46.875 - 87.891 + 32.400 = {FT_I:.2f}\ \ \mathrm{{(tension)}}$",
 "m_fb": rf"$f_{{\mathrm{{b}}}} = +46.875 + 87.891 - 32.400 = +{FB_I:.2f}\ \ \mathrm{{(compression)}}$",
 "m_kern": r"$k = \dfrac{S}{A}\ \ \left(=\dfrac{h}{6}\ \mathrm{rect.}\right),\qquad f_{\mathrm{t}}(P\ \mathrm{only}) = \dfrac{P}{A}\left(1-\dfrac{e}{k}\right)$",
 "m_fts": rf"$f_{{\mathrm{{t}}}} = +{U1:.3f} - {U2+1e-9:.3f} + {U3:.3f} = +{FT_S:.2f}$",
 "m_fbs": rf"$f_{{\mathrm{{b}}}} = +{U1:.3f} + {U2+1e-9:.3f} - {U3:.3f} = {FB_S:.2f}$",
 "m_z0": rf"$z_0 = h\,\dfrac{{|f_{{\mathrm{{t}}}}|}}{{|f_{{\mathrm{{t}}}}|+f_{{\mathrm{{b}}}}}} = 80\times\dfrac{{8.62}}{{110.98}} = {Z0:.2f}\ \mathrm{{cm}}$",
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
