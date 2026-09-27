# ── RC-U4-1 拼圖二：兩階段 × 四控制點 ── 全篇唯一數據來源（kgf、cm；彎矩 t-m）
# 示範梁與拼圖一、主講義微型例題①相同，可交叉對帳
import json, math
L = 12.0; B, H = 40.0, 80.0; E = 25.0
PI_T, PE_T = 150.0, 120.0
GC = 2.4; WL = 2.5
FCI, FC = 280.0, 350.0            # kgf/cm²
A = B*H; I = B*H**3/12; ST = SB = I/(H/2); K = ST/A
WD = B*H/1e4*GC; MD = WD*L**2/8; ML = WL*L**2/8; MT = MD + ML
tm = 1e5; PI, PE = PI_T*1e3, PE_T*1e3
R = PE/PI                         # 有效預力比 0.80
# ═════ 容許應力（kgf/cm²） ═════
FCI_A = 0.60*FCI                  # 168
FTI_A = 0.80*math.sqrt(FCI)       # 13.39
FCS_A = 0.60*FC                   # 210
FTS_A = 2.0*math.sqrt(FC)         # 37.42
FCS45 = 0.45*FC                   # 157.5（持續載重）
CONV = math.sqrt(10.197)          # 3.193
# ═════ 三項 ═════
T1, T2, T3 = PI/A, PI*E/ST, MD*tm/ST
U1, U2, U3 = PE/A, PE*E/ST, MT*tm/ST
F1 = T1 - T2 + T3; F2 = T1 + T2 - T3      # ① 傳遞頂 ② 傳遞底
F3 = U1 - U2 + U3; F4 = U1 + U2 - U3      # ③ 使用頂 ④ 使用底
# 中間狀態：損失完成、尚無活載（P_e + M_d）
B1 = U1 - U2 + T3; B2 = U1 + U2 - T3
# 串料：P_i + M_T（不存在的組合）
X1 = T1 - T2 + U3; X2 = T1 + T2 - U3
# 使用率
UT = [-F1/FTI_A, F2/FCI_A, F3/FCS_A, -F4/FTS_A]
# ═════ 反算：e 可行區（跨中） ═════
E1 = K + (MD*tm + FTI_A*ST)/PI     # ① e ≤ 26.36
E2 = -K + (MD*tm + FCI_A*SB)/PI    # ② e ≤ 43.67
E3 = K + (MT*tm - FCS_A*ST)/PE     # ③ e ≥ −12.31
E4 = -K + (MT*tm - FTS_A*SB)/PE    # ④ e ≥ 22.38
# ═════ 反算：最大活載 ═════
MT3 = ST*(FCS_A - U1 + U2)/tm      # ③ M_T ≤ 103.60
MT4 = SB*(U1 + U2 + FTS_A)/tm      # ④ M_T ≤ 61.96 （= M_cr）
MTX = min(MT3, MT4); MLX = MTX - MD; WLX = 8*MLX/L**2
# ═════ 端部（直線鋼腱、M = 0） ═════
FEND_T = T1 - T2; FEND_B = T1 + T2
FTI_END = 1.6*math.sqrt(FCI); FCI_END = 0.70*FCI
# 漏自重：① 只剩預力
F1_NOMD = T1 - T2
# 容許值誤用 f′c 於傳遞
FTI_WRONG = 0.80*math.sqrt(FC)
# ═════ 對帳 ═════
assert abs(FCI_A-168) < 1e-9 and abs(FTI_A-13.39) < 0.005 and abs(FCS_A-210) < 1e-9 and abs(FTS_A-37.42) < 0.005
assert abs(F1+8.62) < 0.005 and abs(F2-102.37) < 0.005 and abs(F3-105.06) < 0.005 and abs(F4+30.06) < 0.005
assert abs(E1-26.36) < 0.005 and abs(E4-22.38) < 0.005 and abs(MT4-61.96) < 0.005
assert abs(0.25*CONV-0.80) < 0.005 and abs(0.62*CONV-1.98) < 0.005
if __name__ == "__main__":
    g = {k: v for k, v in globals().items() if k.isupper() and isinstance(v, (float, list))}
    for k, v in g.items(): print(k, v)
    json.dump(g, open("nums.json", "w"), indent=1)
