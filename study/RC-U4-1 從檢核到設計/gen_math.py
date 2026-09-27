"""公式 → 向量 SVG（matplotlib mathtext）；數字一律取自 params.py"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, json
from PIL import Image
from params import *
plt.rcParams["svg.fonttype"] = "path"; plt.rcParams["mathtext.fontset"] = "cm"
c = lambda v: f"{v:,.0f}".replace(",", "{,}")
M = {
 "m_fce": rf"$f_{{ce}} = \dfrac{{P_e}}{{A}} + \dfrac{{P_e\,e}}{{S_b}} = \dfrac{{120{{,}}000}}{{3{{,}}200}} + \dfrac{{120{{,}}000\times25}}{{{c(S)}}} = {FPA:.2f} + {FPE_S:.2f} = {FCE:.2f}$",
 "m_fr": rf"$f_r = 2.0\sqrt{{f_c^{{\prime}}}} = 2.0\sqrt{{350}} = {FR:.2f}\ \mathrm{{kgf/cm^2}}$",
 "m_mcr": rf"$M_{{cr}} = S_b\,(f_{{ce}} + f_r) = {c(S)}\times({FCE:.2f} + {FR:.2f}) = {MCR:.2f}\ \mathrm{{t\!\cdot\!m}}$",
 "m_dm": rf"$\Delta M = M_{{cr}} - M_d = {MCR:.2f} - {MD:.2f} = {DMCR:.2f}\ \mathrm{{t\!\cdot\!m}}$",
 "m_mcrk": rf"$M_{{cr}} = P_e\,(e + k_t) + f_r S_b = 120\times\dfrac{{{E+K:.2f}}}{{100}} + {MCR_R:.2f} = {M0:.2f} + {MCR_R:.2f} = {MCR:.2f}$",
 "m_rho": rf"$\rho_p = \dfrac{{A_{{ps}}}}{{b\,d_p}} = \dfrac{{{APS:.3f}}}{{40\times{DP:.0f}}} = {RHO:.5f},\qquad \beta_1 = 0.85 - 0.05\times\dfrac{{350-280}}{{70}} = {B1:.2f}$",
 "m_fps": rf"$f_{{ps}} = f_{{pu}}\left[1 - \dfrac{{\gamma_p}}{{\beta_1}}\,\dfrac{{\rho_p f_{{pu}}}}{{f_c^{{\prime}}}}\right] = 18{{,}}600\left[1 - \dfrac{{0.28}}{{{B1:.2f}}}\times\dfrac{{{RHO:.5f}\times18{{,}}600}}{{350}}\right] = {c(FPS)}$",
 "m_a": rf"$a = \dfrac{{A_{{ps}} f_{{ps}}}}{{0.85 f_c^{{\prime}}\, b}} = \dfrac{{{APS:.3f}\times{c(FPS)}}}{{0.85\times350\times40}} = {AA:.2f}\ \mathrm{{cm}},\quad c = \dfrac{{a}}{{\beta_1}} = {CC:.2f}$",
 "m_mn": rf"$M_n = A_{{ps}} f_{{ps}}\left(d_p - \dfrac{{a}}{{2}}\right) = {c(T)}\times{ARM:.2f} = {MN:.2f}\ \mathrm{{t\!\cdot\!m}}$",
 "m_et": rf"$\varepsilon_t = 0.003\,\dfrac{{d_t - c}}{{c}} = 0.003\times\dfrac{{{DP:.0f} - {CC:.2f}}}{{{CC:.2f}}} = {ET:.5f}\ \geq 0.005\ \Rightarrow\ \phi = 0.90$",
 "m_pmn": rf"$\phi M_n = {PMN:.2f}\ \geq\ M_u = 1.2({MD:.2f}) + 1.6({ML:.2f}) = {MU:.2f}\qquad \phi M_n\ \geq\ 1.2M_{{cr}} = {MCR12:.2f}$",
 "m_ub": rf"$f_{{ps}} = f_{{pe}} + 700 + \dfrac{{f_c^{{\prime}}}}{{100\rho_p}} = {c(FPE)} + 700 + {FC/(100*RHO):.0f} = {c(FPS_UB)}\ \Rightarrow\ M_n = {MN_UB:.2f}$",
 "m_e1": rf"$\text{{①}}\ \ e \leq \left(\dfrac{{P_i}}{{A}} + \dfrac{{M_d}}{{S_t}} + f_{{ti}}\right)\dfrac{{S_t}}{{P_i}} = ({PI/A:.2f} + {MD*tm/S:.2f} + {FTI_A:.2f})\times{S/PI:.4f} = {E1:.2f}$",
 "m_e2": rf"$\text{{②}}\ \ e \leq \left(f_{{ci}} - \dfrac{{P_i}}{{A}} + \dfrac{{M_d}}{{S_b}}\right)\dfrac{{S_b}}{{P_i}} = ({FCI_A:.0f} - {PI/A:.2f} + {MD*tm/S:.2f})\times{S/PI:.4f} = {E2:.2f}$",
 "m_e3": rf"$\text{{③}}\ \ e \geq \left(\dfrac{{P_e}}{{A}} + \dfrac{{M_T}}{{S_t}} - f_{{cs}}\right)\dfrac{{S_t}}{{P_e}} = ({FPA:.2f} + {MT*tm/S:.2f} - {FCS_A:.0f})\times{S/PE:.4f} = {E3:.2f}$",
 "m_e4": rf"$\text{{④}}\ \ e \geq \left(\dfrac{{M_T}}{{S_b}} - \dfrac{{P_e}}{{A}} - f_{{ts}}\right)\dfrac{{S_b}}{{P_e}} = ({MT*tm/S:.2f} - {FPA:.2f} - {FTS_A:.2f})\times{S/PE:.4f} = {E4:.2f}$",
 "m_mtmax": rf"$M_{{T,\max}} = S_b\left(\dfrac{{P_e}}{{A}} + \dfrac{{P_e e}}{{S_b}} + f_{{ts}}\right) = {c(S)}\times({FCE:.2f} + {FTS_A:.2f}) = {MT4:.2f}\ \mathrm{{t\!\cdot\!m}}$",
 "m_wl": rf"$w_{{L,\max}} = \dfrac{{8\,(M_{{T,\max}} - M_d)}}{{L^2}} = \dfrac{{8\times({MT4:.2f} - {MD:.2f})}}{{12^2}} = {WLMAX:.3f}\ \mathrm{{t/m}}$",
 "m_pemin": rf"$P_{{e,\min}} = \dfrac{{M_T/S_b - f_{{ts}}}}{{1/A + e/S_b}} = \dfrac{{{MT*tm/S:.2f} - {FTS_A:.2f}}}{{1/3{{,}}200 + 25/{c(S)}}} = {PE_MIN:.2f}\ \mathrm{{t}}$",
 "m_pimax": rf"$P_{{i,\max}} = \dfrac{{M_d/S_t + f_{{ti}}}}{{e/S_t - 1/A}} = \dfrac{{{MD*tm/S:.2f} + {FTI_A:.2f}}}{{25/{c(S)} - 1/3{{,}}200}} = {PI_MAX1:.2f}\ \mathrm{{t}}$",
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
