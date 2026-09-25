"""公式 → 向量 SVG（matplotlib mathtext，文字轉路徑）；數字一律取自 params.py"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, json
from PIL import Image
from params import *
plt.rcParams["svg.fonttype"] = "path"; plt.rcParams["mathtext.fontset"] = "cm"
M = {
 "m_mohr": r"$\sigma_{1,3} = \dfrac{\sigma_x+\sigma_y}{2} \pm \sqrt{\left(\dfrac{\sigma_x-\sigma_y}{2}\right)^2+\tau^2}$",
 "m_ps": r"$\sigma_x=\sigma_y=0\ \Rightarrow\ \sigma_1=+\tau,\ \ \sigma_3=-\tau,\ \ \theta=45^\circ$",
 "m_ft": rf"$f_t \approx 1.06\sqrt{{f'_c}} = 1.06\sqrt{{280}} = {FT:.2f}\ \mathrm{{kgf/cm^2}}$",
 "m_vc": r"$V_c = 0.53\sqrt{f'_c}\,b_w\,d$",
 "m_vcd": rf"$V_c = 0.53\sqrt{{280}}\,(30)(50) = {int(round(VC0*1000))//1000}{{,}}{int(round(VC0*1000))%1000:03d}\ \mathrm{{kgf}} = {VC0:.2f}\ \mathrm{{tf}}$",
 "m_half": rf"$\dfrac{{V_c}}{{b_w d}} = 0.53\sqrt{{f'_c}} = {VCS:.2f} \approx \dfrac{{f_t}}{{2}}$",
 "m_axial": r"$\sigma_1 = \dfrac{\sigma}{2} + \sqrt{\left(\dfrac{\sigma}{2}\right)^2+\tau^2}$",
 "m_comp": r"$V_c = 0.53\left(1+\dfrac{N_u}{140\,A_g}\right)\sqrt{f'_c}\,b_w d$",
 "m_ten": r"$V_c = 0.53\left(1+\dfrac{N_u}{35\,A_g}\right)\sqrt{f'_c}\,b_w d \geq 0$",
 "m_det": r"$V_c = \left(0.50\sqrt{f'_c} + 176\,\rho_w\dfrac{V_u d}{M_u}\right) b_w d \leq 0.93\sqrt{f'_c}\,b_w d$",
 "m_detd": rf"$({VC_DET_S:.2f})(30)(50) = {VC_DET:.2f}\ \mathrm{{tf}}$",
 "m_vs": r"$V_s = n\,A_v f_{yt} = \dfrac{A_v f_{yt}\,d}{s}$",
 "m_vsmax": r"$V_s \leq 2.12\sqrt{f'_c}\,b_w d = 4\,(0.53\sqrt{f'_c}\,b_w d)$",
 "m_vumax": r"$V_u \leq \phi\,(2.65\sqrt{f'_c}\,b_w d),\quad \phi = 0.75$",
 "m_vu": r"$V_u \leq \phi V_n = \phi\,(V_c + V_s)$",
 "m_smax": r"$s \leq \dfrac{d}{2};\quad V_s > 1.06\sqrt{f'_c}\,b_w d\ \Rightarrow\ s \leq \dfrac{d}{4}$",
 "m_hinge": r"$V_c = 0:\ \ V_E \geq \dfrac{V_u}{2}\ \ \mathrm{and}\ \ P_u < \dfrac{A_g f'_c}{20}$",
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
