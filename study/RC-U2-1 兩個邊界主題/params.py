# ── RC-U2-1 拼圖四：兩個邊界主題（STM／剪力摩擦）＋扭力門檻 ── 全篇唯一數據來源（kgf、cm；輸出 tf）
import math, json
sq = math.sqrt
t = lambda kgf: kgf/1000
FC, FY = 280.0, 4200.0
SQ = sq(FC)
PHI = 0.75
# ═════ 基準斷面（沿用拼圖三）35×70、d 63 ═════
BW, H, D = 35.0, 70.0, 63.0
VC = t(0.53*SQ*BW*D)                 # 19.56
VC5 = 5*VC                           # 97.78 = 2.65√f'c bw d
# ═════ 例⑤ 深梁 STM ═════
B5, H5, A5 = 40.0, 150.0, 150.0      # 寬、深、剪跨（支承中心到載重中心）
L5 = 2*A5                            # 支承中心距 300
LB_S, LB_P = 40.0, 60.0              # 支承承壓板、載重承壓板（沿梁長）
WT = 20.0                            # 拉桿有效高度（鋼筋重心離底 10 cm 的兩倍）
D5 = H5 - WT/2                       # 140
AD5 = A5/D5                          # 1.07
PU5 = 200.0; R5 = PU5/2              # 100
FCE_CCC = 0.85*1.0*FC                # 238
FCE_CCT = 0.85*0.80*FC               # 190.4
FCE_S75 = 0.85*0.75*FC               # 178.5（瓶形、含橫向鋼筋）
FCE_S60 = 0.85*0.60*FC               # 142.8
AH5 = A5 - LB_P/4                    # 斜壓桿水平投影：載重板分成兩半，節點在 1/4 點
WTOP = 15.0
for _ in range(60):                  # 上節點高度 ↔ 力臂 迭代
    Z5 = H5 - WT/2 - WTOP/2
    TH = math.atan(Z5/AH5)
    T5 = R5/math.tan(TH)             # 拉桿力 = 上方水平壓桿力
    WTOP = T5*1000/(PHI*FCE_CCC*B5)  # 上方水平壓桿（稜柱形）剛好滿應力的最小高度
TH_DEG = math.degrees(TH)
F5 = R5/math.sin(TH)                 # 斜壓桿力
WS_B = LB_S*math.sin(TH) + WT*math.cos(TH)          # 壓桿下端寬
WS_T = LB_P/2*math.sin(TH) + WTOP*math.cos(TH)      # 壓桿上端寬（載重板一半給一支壓桿）
CAP_SB = t(PHI*min(FCE_S75, FCE_CCT)*WS_B*B5)       # 壓桿下端（βs 0.75 vs βn 0.80 取小）
CAP_ST = t(PHI*min(FCE_S75, FCE_CCC)*WS_T*B5)       # 壓桿上端
CAP_NS = t(PHI*FCE_CCT*LB_S*B5)                     # 支承節點承壓面 CCT
CAP_NP = t(PHI*FCE_CCC*LB_P*B5)                     # 載重節點承壓面 CCC
AS5_REQ = T5*1000/(PHI*FY)
AB25 = 5.067; N25 = math.ceil(AS5_REQ/AB25); AS5 = N25*AB25
CAP_T = t(PHI*AS5*FY)
VLIM5 = t(2.65*SQ*B5*D5); PVLIM5 = PHI*VLIM5
U_SB, U_ST, U_NS, U_NP, U_T, U_LIM = [x*100 for x in (F5/CAP_SB, F5/CAP_ST, R5/CAP_NS, PU5/CAP_NP, T5/CAP_T, R5/PVLIM5)]
# 若誤用 βs = 0.60（瓶形無橫筋）
CAP_ST60 = t(PHI*FCE_S60*WS_T*B5)
# ═════ 例④ 剪力摩擦：Vu 45、Ac 35×60 ═════
VU4 = 45.0; AC4 = 35.0*60.0
MU_R, MU_S, MU_M, MU_P = 1.0, 0.6, 1.4, 0.7
AVF_R = VU4*1000/(PHI*MU_R*FY)       # 14.29
AVF_S = VU4*1000/(PHI*MU_S*FY)       # 23.81
MORE4 = (AVF_S/AVF_R - 1)*100        # 66.7
AB19 = 2.865; N19 = math.ceil(AVF_R/AB19); AVF_USE = N19*AB19   # 5-D19 14.33
N19S = math.ceil(AVF_S/AB19)         # 9-D19
VLIM_UNIT = min(0.2*FC, 34+0.08*FC, 112)   # 56
VLIM_UNIT_S = min(0.2*FC, 56)              # 未粗糙面上限
PVN4_MAX = t(PHI*VLIM_UNIT*AC4)      # 88.20
USE4 = VU4/PVN4_MAX*100              # 51.0
AC4_MIN = VU4*1000/(PHI*VLIM_UNIT)   # 所需最小介面面積
# ═════ 扭力門檻（基準斷面）═════
ACP = BW*H; PCP = 2*(BW+H)           # 2450、210
PTTH = t(PHI*0.265*SQ*ACP**2/PCP)/100    # t-m：0.951
TCR = t(1.06*SQ*ACP**2/PCP)/100          # 開裂扭矩（門檻 = 1/4 Tcr）
C_STIR = 5.0                              # 外緣到箍筋中心
X1, Y1 = BW-2*C_STIR, H-2*C_STIR          # 25、60
AOH = X1*Y1; PH = 2*(X1+Y1); AO = 0.85*AOH
PTTH_WRONG = t(PHI*0.265*SQ*AOH**2/PH)/100   # 誤用 Aoh、ph
DROP_T = (1 - PTTH_WRONG/PTTH)*100
# ═════ 對帳 ═════
assert abs(VC-19.56)<0.005 and abs(VC5 - t(2.65*SQ*BW*D))<0.05
assert AD5 <= 2 and TH_DEG >= 25
assert max(U_SB, U_ST, U_NS, U_NP, U_T, U_LIM) <= 100
assert CAP_ST60 < F5               # 誤用 0.60 會判不足 → 教學點
assert abs(AVF_R-14.29)<0.005 and abs(AVF_S-23.81)<0.005 and abs(MORE4-66.67)<0.01
assert N19 == 5 and abs(AVF_USE-14.33)<0.01 and abs(VLIM_UNIT-56)<1e-9
assert abs(PVN4_MAX-88.20)<0.005 and abs(USE4-51.0)<0.05
assert abs(PTTH-0.951)<0.0005
if __name__ == "__main__":
    g = {k: v for k, v in globals().items() if k.isupper() and isinstance(v, (float, int))}
    for k, v in g.items(): print(f"{k:10s} {v:10.4f}")
    json.dump(g, open("nums.json", "w"), indent=1)
