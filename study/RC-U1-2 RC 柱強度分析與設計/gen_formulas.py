#!/usr/bin/env python3
"""RC-U1-2 觀念講義 —— 公式 PNG 渲染（matplotlib mathtext）

踩過的坑：
  * mathtext 只支援 LaTeX 子集：\\frac \\sqrt ^ _ \\sum \\left \\right 希臘字母
    \\leq \\geq \\times \\cdot \\quad；**不支援** \\le \\ge \\tfrac \\text \\begin。
  * `$...$` 內絕對不能放中文 —— cm 字型無 CJK 字面。
    中文一律寫在 deck.js 的 label / note / insights。
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt          # noqa: E402
import json, os, re                       # noqa: E402

OUT_DIR = "formula_imgs"
os.makedirs(OUT_DIR, exist_ok=True)

NAVY = "#1B2A41"
DPI, FONTSIZE = 400, 30
plt.rcParams["mathtext.fontset"] = "cm"
plt.rcParams["text.color"] = NAVY

FORMULAS = {
    # ── 引擎 ① 應變與鋼筋應力 ───────────────────────────
    "f_eps":   r"$\varepsilon_i = 0.003 \, \frac{c - d_i}{c} \qquad (+ \; \mathrm{compression})$",
    "f_fs":    r"$f_{si} = \mathrm{clip}(E_s \varepsilon_i , \; -f_y , \; +f_y)$",
    "f_ey":    r"$\varepsilon_y = f_y / E_s \qquad (SD420 : \; 4200/2.04 \times 10^6 = 0.00206)$",
    # ── 引擎 ② 軸力平衡 ─────────────────────────────────
    "f_a":     r"$a = \beta_1 c \quad , \quad \beta_1 = 0.85 - 0.05 \, \frac{f'_c - 280}{70} \geq 0.65$",
    "f_cc":    r"$C_c = 0.85 f'_c \, a \, b$",
    "f_fin":   r"$d_i \leq a : \quad F_i = A_{si}(f_{si} - 0.85 f'_c)$",
    "f_fout":  r"$d_i > a : \quad F_i = A_{si} f_{si}$",
    "f_fi":    r"$F_i = A_{si}(f_{si} - 0.85 f'_c) \;\; [d_i \leq a] \qquad F_i = A_{si} f_{si} \;\; [d_i > a]$",
    "f_pn":    r"$P_n = C_c + \sum F_i$",
    # ── 引擎 ③ 彎矩平衡 ─────────────────────────────────
    "f_mn":    r"$M_n = C_c \left( \frac{h}{2} - \frac{a}{2} \right) + \sum F_i \left( \frac{h}{2} - d_i \right)$",
    "f_arm":   r"$d_i = h/2 \; \Rightarrow \; \mathrm{arm} = 0 \; \Rightarrow \; \Delta M_n = 0$",
    # ── 入口 A ──────────────────────────────────────────
    "f_cdt":   r"$\varepsilon_t = 0 \quad \Rightarrow \quad c = d_t$",
    "f_cb":    r"$c_b = \frac{6120}{6120 + f_y} \, d_t \qquad (SI : \; \frac{600}{600 + f_y} d_t)$",
    # ── 入口 B ──────────────────────────────────────────
    "f_e":     r"$e = M_n / P_n \qquad M_n = P_n e$",
    "f_quad":  r"$P_n(c) = 0.85 f'_c \beta_1 b \, c + \sum A_{si} f_{si}(c) = P_u / \phi$",
    # ── 入口 C：控制點 ──────────────────────────────────
    "f_po":    r"$P_o = 0.85 f'_c (A_g - A_{st}) + f_y A_{st}$",
    "f_pnmax": r"$P_{n,max} = 0.80 P_o \;\; (tied) \quad ; \quad 0.85 P_o \;\; (spiral)$",
    "f_rho":   r"$\rho_g = A_{st} / A_g \qquad 0.01 \leq \rho_g \leq 0.08$",
    # ── φ 與設計 ────────────────────────────────────────
    "f_et":    r"$\varepsilon_t = 0.003 \, \frac{d_t - c}{c}$",
    "f_phi":   r"$\phi = 0.65 + 0.25 \, \frac{\varepsilon_t - \varepsilon_y}{0.005 - \varepsilon_y}$",
    "f_phiz":  r"$\varepsilon_t \geq 0.005 : \phi = 0.90 \quad ; \quad \varepsilon_t \leq \varepsilon_y : \phi = 0.65$",
    "f_design": r"$\phi P_n \geq P_u \quad , \quad \phi M_n \geq M_u$",
    "f_peak":  r"$\max_c [\phi M_n] \neq \phi \cdot \max_c [M_n]$",
    # ── 細長效應 ────────────────────────────────────────
    "f_slend": r"$\frac{k l_u}{r} \leq 34 - 12 \frac{M_1}{M_2} \qquad (r \approx 0.3h)$",
    "f_cm":    r"$C_m = 0.6 + 0.4 \, \frac{M_1}{M_2} \geq 0.4$",
    "f_pc":    r"$P_c = \frac{\pi^2 EI}{(k l_u)^2} \quad , \quad EI = \frac{0.4 E_c I_g}{1 + \beta_d}$",
    "f_dns":   r"$\delta_{ns} = \frac{C_m}{1 - P_u / 0.75 P_c} \geq 1.0$",
    "f_mc":    r"$M_c = \delta_{ns} M_2$",
}

CJK = re.compile(r"[　-〿一-鿿＀-￯]")
bad = {k: v for k, v in FORMULAS.items() if CJK.search(v)}
if bad:
    raise SystemExit(f"CJK leaked into mathtext: {list(bad)}")
for k, v in FORMULAS.items():
    if re.search(r"\\le[^qf]|\\ge[^q]|\\tfrac", v):
        raise SystemExit(f"unsupported macro in {k}: {v}")

manifest, errors = {}, []
for fid, latex in FORMULAS.items():
    fig = plt.figure(figsize=(0.1, 0.1), dpi=DPI)
    try:
        fig.text(0, 0, latex, fontsize=FONTSIZE, color=NAVY)
        path = os.path.join(OUT_DIR, f"{fid}.png")
        fig.savefig(path, dpi=DPI, transparent=True, bbox_inches="tight",
                    pad_inches=0.08)
        plt.close(fig)
        from PIL import Image
        w, h = Image.open(path).size
        manifest[fid] = {"file": path, "ar": w / h}
    except Exception as e:
        errors.append((fid, str(e)))
        plt.close(fig)

with open("formula_manifest.json", "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

print(f"Rendered {len(manifest)} formulas, {len(errors)} errors")
for fid, err in errors:
    print("ERROR", fid, err)
