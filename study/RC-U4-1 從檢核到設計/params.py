# ── RC-U4-1 拼圖四：從檢核到設計 ── 全篇唯一數據來源（kgf、cm；彎矩 t-m）
# 示範梁與拼圖一～三相同：40×80、L = 12 m、e = 25、P_i = 150 t、P_e = 120 t
# 鋼腱：12 股 0.5" 七線鋼絞線（每股 0.987 cm²），f_pu = 18,600 kgf/cm²，有黏結、低鬆弛
import json, math
L = 12.0; B, H = 40.0, 80.0; E = 25.0
PI_T, PE_T = 150.0, 120.0
FCI, FC = 280.0, 350.0
MD = 13.824; MT = 58.824                 # 自重、使用總彎矩（同拼圖二）
tm = 1e5; PI, PE = PI_T*1e3, PE_T*1e3
ETA = PE/PI
A = B*H; I = B*H**3/12; S = I/(H/2); K = S/A          # S_t = S_b；核心距 h/6
ML = MT - MD; WD = 8*MD/L**2; WL = 8*ML/L**2
# ═════ 容許應力 ═════
FCI_A = 0.60*FCI; FTI_A = 0.80*math.sqrt(FCI); FTI_END = 1.6*math.sqrt(FCI)
FCS_A = 0.60*FC; FTS_A = 2.0*math.sqrt(FC)
FR = 2.0*math.sqrt(FC)                   # 破裂模數
# ═════ 一、開裂彎矩 ═════
FPA = PE/A; FPE_S = PE*E/S
FCE = FPA + FPE_S                        # 107.81
M0 = S*FCE/tm                            # 消壓彎矩（底纖維應力歸零）
MCR = S*(FCE + FR)/tm                    # 61.96
DMCR = MCR - MD                          # 48.14
MCR_E = PE*E/tm; MCR_K = PE*K/tm; MCR_R = FR*S/tm      # 三段拆解
# 四個狀態的底纖維應力（示意 d8）
BOT = [FCE, FCE - MD*tm/S, FCE - MT*tm/S, FCE - MCR*tm/S]
TOP = [FPA - FPE_S, FPA - FPE_S + MD*tm/S, FPA - FPE_S + MT*tm/S, FPA - FPE_S + MCR*tm/S]
# 陷阱：用 P_i 算 M_cr、忘了扣 M_d、f_r 誤用 f′ci
MCR_PI = S*(PI/A + PI*E/S + FR)/tm
FR_WRONG = 2.0*math.sqrt(FCI); MCR_FRW = S*(FCE + FR_WRONG)/tm
# ═════ 二、極限強度 ═════
NS, AS1 = 12, 0.987
APS = NS*AS1                             # 11.844
FPU = 18600.0; FPY = 0.90*FPU
DP = H/2 + E                             # 65
FPE = PE/APS                             # 10,132
RHO = APS/(B*DP)
GP = 0.28
B1 = 0.85 - 0.05*(FC - 280)/70
FPS = FPU*(1 - GP/B1*RHO*FPU/FC)         # 17,024
T = APS*FPS
AA = T/(0.85*FC*B)                       # a
CC = AA/B1                               # c
ARM = DP - AA/2
MN = T*ARM/tm                            # 113.98
ET = 0.003*(DP - CC)/CC                  # ε_t
PHI = 0.90 if ET >= 0.005 else 0.65 + 0.25*(ET - 0.002)/0.003
PMN = PHI*MN                             # 102.58
MU = 1.2*MD + 1.6*ML                     # 88.59
MCR12 = 1.2*MCR
EPS_PE = FPE/1.97e6                      # 有效預應變（示意）
# P_e 旋鈕：M_n 不動、M_cr 會動
def mcr_of(pe_t): return S*(pe_t*1e3/A + pe_t*1e3*E/S + FR)/tm
PE_12 = (PMN*tm/(1.2*S) - FR)/(1/A + E/S)/1e3          # 1.2M_cr = φM_n 時的 P_e
MCR_100 = mcr_of(100.0)
# 若是無黏結（ACI，L/d ≤ 35）：f_ps = f_pe + 700 + f′c/(100ρ)
FPS_UB = min(FPE + 700 + FC/(100*RHO), FPY, FPE + 4200)
MN_UB = APS*FPS_UB*(DP - APS*FPS_UB/(0.85*FC*B)/2)/tm
# ═════ 三、反算設计 ═════
MDX = lambda x: 4*MD*x*(L - x)/L**2
MTX = lambda x: 4*MT*x*(L - x)/L**2
def e1(x): return (PI/A + MDX(x)*tm/S + FTI_A)*S/PI          # 傳遞頂拉 → 上限
def e2(x): return (FCI_A - PI/A + MDX(x)*tm/S)*S/PI          # 傳遞底壓 → 上限
def e3(x): return (PE/A + MTX(x)*tm/S - FCS_A)*S/PE          # 使用頂壓 → 下限
def e4(x): return (MTX(x)*tm/S - PE/A - FTS_A)*S/PE          # 使用底拉 → 下限
E1, E2, E3, E4 = e1(6), e2(6), e3(6), e4(6)
E1_END, E4_END = e1(0), e4(0)
E1_END2 = (PI/A + FTI_END)*S/PI                              # 端部放寬 1.6√f′ci
# 直線鋼腱在梁端：頂纖維
F1_END_STRAIGHT = PI/A - PI*E/S
# 最大活載
MT4 = S*(PE/A + PE*E/S + FTS_A)/tm       # = M_cr（本例 f_ts = f_r）
MT3 = S*(FCS_A - PE/A + PE*E/S)/tm
MTMAX = min(MT3, MT4); MLMAX = MTMAX - MD; WLMAX = 8*MLMAX/L**2
# 反算預力
PE_MIN = (MT*tm/S - FTS_A)/(1/A + E/S)/1e3                  # ④
PI_MAX1 = (MD*tm/S + FTI_A)/(E/S - 1/A)/1e3                 # ①
PI_MAX2 = (FCI_A + MD*tm/S)/(1/A + E/S)/1e3                 # ②
PI_MIN = PE_MIN/ETA
# Magnel：1000/P_i（1/t）對 e
def mg1(e): return 1e6*(e/S - 1/A)/(MD*tm/S + FTI_A)                 # 1/P ≥（e > k 時）
def mg2(e): return 1e6*(1/A + e/S)/(FCI_A + MD*tm/S)                 # 1/P ≥
def mg3(e): return 1e6*ETA*(1/A - e/S)/(FCS_A - MT*tm/S)             # 1/P ≥
def mg4(e): return 1e6*ETA*(1/A + e/S)/(MT*tm/S - FTS_A)             # 1/P ≤
INVP = 1000/PI_T
# ═════ 對帳（主講義 d8、d9、d10；拼圖二 e 可行區與最大活載） ═════
assert abs(FCE - 107.81) < 0.005 and abs(FR - 37.42) < 0.005 and abs(MCR - 61.96) < 0.005 and abs(DMCR - 48.14) < 0.005
assert abs(BOT[1] - 75.41) < 0.005 and abs(BOT[2] + 30.06) < 0.005 and abs(TOP[2] - 105.06) < 0.005
assert abs(FPS - 17024) < 1 and abs(T - 201632) < 2 and abs(CC - 21.18) < 0.005 and abs(ARM - 56.53) < 0.005
assert abs(MN - 113.98) < 0.005 and abs(PMN - 102.58) < 0.005 and abs(MU - 88.59) < 0.005 and abs(FPE - 10132) < 1
assert abs(E1 - 26.36) < 0.005 and abs(E4 - 22.38) < 0.005 and abs(E2 - 43.67) < 0.005 and abs(E3 + 12.31) < 0.005
assert abs(MT4 - MCR) < 1e-6 and abs(WLMAX - 2.674) < 0.0005 and abs(MT3 - 103.60) < 0.005
assert abs(MCR_E + MCR_K + MCR_R - MCR) < 1e-9
if __name__ == "__main__":
    g = {k: v for k, v in globals().items() if k.isupper() and isinstance(v, (float, int)) and not isinstance(v, bool)}
    g["BOT"] = BOT; g["TOP"] = TOP
    for k, v in g.items(): print(f"{k:14s} {v}")
    json.dump(g, open("nums.json", "w"), indent=1)
