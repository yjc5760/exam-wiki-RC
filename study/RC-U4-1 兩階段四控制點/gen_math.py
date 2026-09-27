"""公式 → 向量 SVG（matplotlib mathtext）；數字一律取自 params.py"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, json
from PIL import Image
from params import *
plt.rcParams["svg.fonttype"] = "path"; plt.rcParams["mathtext.fontset"] = "cm"
M = {
 "m_top": r"$f_{\mathrm{t}} = +\dfrac{P}{A} - \dfrac{P\,e}{S_t} + \dfrac{M}{S_t}$",
 "m_bot": r"$f_{\mathrm{b}} = +\dfrac{P}{A} + \dfrac{P\,e}{S_b} - \dfrac{M}{S_b}$",
 "m_t3": rf"$\dfrac{{P_i}}{{A}} = {T1:.3f},\quad \dfrac{{P_i\,e}}{{S}} = {T2:.3f},\quad \dfrac{{M_d}}{{S}} = {T3:.3f}$",
 "m_u3": rf"$\dfrac{{P_e}}{{A}} = {U1:.3f},\quad \dfrac{{P_e\,e}}{{S}} = {U2+1e-9:.3f},\quad \dfrac{{M_T}}{{S}} = {U3:.3f}$",
 "m_f1": rf"$f_{{\mathrm{{t}}}} = +{T1:.2f} - {T2:.2f} + {T3:.2f} = {F1:.2f} \ \geq\ -{FTI_A:.2f}$",
 "m_f2": rf"$f_{{\mathrm{{b}}}} = +{T1:.2f} + {T2:.2f} - {T3:.2f} = +{F2:.2f} \ \leq\ +{FCI_A:.0f}$",
 "m_f3": rf"$f_{{\mathrm{{t}}}} = +{U1:.2f} - {U2+1e-9:.2f} + {U3:.2f} = +{F3:.2f} \ \leq\ +{FCS_A:.0f}$",
 "m_f4": rf"$f_{{\mathrm{{b}}}} = +{U1:.2f} + {U2+1e-9:.2f} - {U3:.2f} = {F4:.2f} \ \geq\ -{FTS_A:.2f}$",
 "m_conv": r"$0.25\sqrt{f'_{ci}\,[\mathrm{MPa}]} = 0.25\sqrt{\dfrac{f'_{ci}\,[\mathrm{kgf/cm^2}]}{10.197}}\times 10.197 = 0.25\sqrt{10.197}\,\sqrt{f'_{ci}} \approx 0.80\sqrt{f'_{ci}}$",
 "m_e1": rf"$e \leq \dfrac{{S}}{{A}} + \dfrac{{M_d + f_{{ti}}\,S}}{{P_i}} = {K:.2f} + \dfrac{{13.824\times10^5 + {FTI_A:.2f}\times 42{{,}}667}}{{150{{,}}000}} = {E1:.2f}\ \mathrm{{cm}}$",
 "m_e4": rf"$e \geq -\dfrac{{S}}{{A}} + \dfrac{{M_T - f_{{ts}}\,S}}{{P_e}} = -{K:.2f} + \dfrac{{58.824\times10^5 - {FTS_A:.2f}\times 42{{,}}667}}{{120{{,}}000}} = {E4:.2f}\ \mathrm{{cm}}$",
 "m_mt4": rf"$M_T \leq S_b\left(\dfrac{{P_e}}{{A}} + \dfrac{{P_e\,e}}{{S_b}} + f_{{ts}}\right) = 42{{,}}667\,({U1:.2f} + {U2+1e-9:.2f} + {FTS_A:.2f}) = {MT4:.2f}\ \mathrm{{t\!\cdot\!m}}$",
 "m_wl": rf"$w_{{L,\max}} = \dfrac{{8\,(M_{{T,\max}} - M_d)}}{{L^2}} = \dfrac{{8\,({MT4:.2f} - {MD:.3f})}}{{12^2}} = {WLX:.3f}\ \mathrm{{t/m}}$",
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
