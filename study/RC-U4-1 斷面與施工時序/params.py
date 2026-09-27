# ── RC-U4-1 拼圖三：斷面與施工時序 ── 全篇唯一數據來源（kgf、cm；彎矩 t-m）
# 示範梁與拼圖一、二相同（40×80、L=12、e=25、P_i=150、P_e=120），上方加 150×15 現場版
import json, math
L = 12.0; B, H = 40.0, 80.0; E1 = 25.0
BE, TS = 150.0, 15.0              # 有效翼寬、版厚（與梁同強度，n = 1）
PI_T, PE_T = 150.0, 120.0
GC = 2.4; WL = 1.8                # 組合後活載＋疊加靜載 t/m
FCI, FC = 280.0, 350.0
tm = 1e5; PI, PE = PI_T*1e3, PE_T*1e3
YPS = H/2 - E1                    # 鋼腱距梁底 15 cm
# ═════ 預鑄梁（斷面 1） ═════
A1 = B*H; I1 = B*H**3/12; YB1 = H/2; YT1 = H - YB1; S1 = I1/YB1   # S_t1 = S_b1
K1 = S1/A1                        # 13.33
# ═════ 組合斷面（斷面 c） ═════
AS = BE*TS; YS = H + TS/2
AC = A1 + AS
YBC = (A1*YB1 + AS*YS)/AC         # 59.61
HC = H + TS
YTC_B = H - YBC                   # 梁頂距 20.39
YTC_S = HC - YBC                  # 版頂距 35.39
IS = BE*TS**3/12
D1 = YBC - YB1; DS = YS - YBC
IC = I1 + A1*D1**2 + IS + AS*DS**2
SBC = IC/YBC; STC_B = IC/YTC_B; STC_S = IC/YTC_S
EC = YBC - YPS                    # 44.61
KTC = SBC/AC; KBC = STC_S/AC      # 上核心距、下核心距（以版頂為頂纖維）
S_WRONG = IC/(HC/2)               # 錯用 I/(h/2)
# ═════ 彎矩 ═════
WG = A1/1e4*GC; WS = AS/1e4*GC
MG = WG*L**2/8; MS = WS*L**2/8; ML = WL*L**2/8
MT = MG + MS + ML
# ═════ 核心距示意：P_e 單獨作用 ═════
KERN = {e: (PE/A1 - PE*e/S1, PE/A1 + PE*e/S1) for e in (0.0, K1, E1)}
# ═════ 分階段（壓 +、拉 −）═════
# 階段①：P_i + M_G 於預鑄梁
S1T = PI/A1 - PI*E1/S1 + MG*tm/S1
S1B = PI/A1 + PI*E1/S1 - MG*tm/S1
# 階段②增量：預力損失（ΔP = P_e − P_i）與濕版重 M_S，仍在預鑄梁
DP = PE - PI
LOSS_T = DP/A1 - DP*E1/S1; LOSS_B = DP/A1 + DP*E1/S1
MS_T = MS*tm/S1; MS_B = -MS*tm/S1
S2T = S1T + LOSS_T + MS_T; S2B = S1B + LOSS_B + MS_B
# 階段③增量：M_L 於組合斷面
ML_S = ML*tm/STC_S; ML_T = ML*tm/STC_B; ML_B = -ML*tm/SBC
FT_S = ML_S; FT_T = S2T + ML_T; FT_B = S2B + ML_B      # 總應力
# ═════ 陷阱 ═════
MS_B_WRONG = -MS*tm/SBC                                 # 濕版重誤用組合斷面
FB_WETWRONG = S2B - MS_B + MS_B_WRONG + ML_B
# 一次算完：P_e 放在組合斷面 e_c、總彎矩 M_T 全除組合斷面
ONE_B = PE/AC + PE*EC/SBC - MT*tm/SBC
ONE_T = PE/AC - PE*EC/STC_B + MT*tm/STC_B
ML_B_WRONG = -ML*tm/S_WRONG
# ═════ 容許 ═════
FCI_A = 0.60*FCI; FTI_A = 0.80*math.sqrt(FCI)
FCS_A = 0.60*FC; FTS_A = 2.0*math.sqrt(FC)
# ═════ 組合的紅利：最大 M_L ═════
MLX_C = (S2B + FTS_A)*SBC/tm          # 組合斷面承受 M_L
MLX_N = (S2B + FTS_A)*S1/tm           # 假設沒有組合作用
WLX_C = 8*MLX_C/L**2; WLX_N = 8*MLX_N/L**2
# ═════ 對帳（與主講義 d4～d7 圖一致） ═════
assert abs(YBC-59.61) < 0.005 and abs(IC-4729588) < 1 and abs(SBC-79342) < 1
assert abs(STC_B-231957) < 1 and abs(STC_S-133642) < 1 and abs(EC-44.61) < 0.005
assert abs(MS-9.72) < 1e-9 and abs(MS_T-22.78) < 0.005 and abs(MS_B_WRONG+12.25) < 0.005
assert abs(ML*tm/SBC-40.84) < 0.005 and abs(KERN[E1][0]+32.81) < 0.005 and abs(KERN[E1][1]-107.81) < 0.005
assert abs(S1T+8.62) < 0.005 and abs(S1B-102.37) < 0.005
if __name__ == "__main__":
    g = {k: v for k, v in globals().items() if k.isupper() and isinstance(v, float)}
    for k, v in g.items(): print(f"{k:12s} {v:14.4f}")
    json.dump(g, open("nums.json", "w"), indent=1)
