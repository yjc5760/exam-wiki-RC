# ── RC-U2-1 拼圖三：四道關卡 ── 全篇唯一數據來源（kgf、cm；輸出 tf）
import math, json
sq = math.sqrt
t = lambda kgf: kgf/1000
FC, FY = 280.0, 4200.0
SQ = sq(FC)
PHI = 0.75
# ═════ 基準斷面 35×70，d = 63 ═════
BW, H, D = 35.0, 70.0, 63.0
AG, BD = BW*H, BW*D
VC = t(0.53*SQ*BD)                  # 19.56
VC2, VC4 = 2*VC, 4*VC               # 39.11 / 78.22
VS2_LIM = t(1.06*SQ*BD)             # 規範門檻本身（= 2Vc 簡化式）
VS4_LIM = t(2.12*SQ*BD)
PVC = PHI*VC                        # 14.67
PVC3 = 3*PVC                        # 44.00
PVC05 = 0.5*PVC                     # 7.33
VU_MAX = 5*PHI*VC                   # 73.33
AV = 2*1.267                        # D13 雙肢 2.534
K = AV*FY*D                         # s·Vs 常數（kgf·cm）
SMAX2, SMAX4 = min(D/2, 60), min(D/4, 30)   # 31.5 / 15.75
AVMIN_C1, AVMIN_C2 = 0.2*SQ, 3.5    # 3.35 < 3.5
S_AVMIN = AV*FY/(max(AVMIN_C1, AVMIN_C2)*BW)   # 86.88
FC_X = (3.5/0.2)**2                 # 306.25：0.2√f'c 超過 3.5 的交叉點
# ═════ 例① 頂面均布、端部受壓：wu 12，ln 7.0 ═════
L1, W1 = 7.0, 12.0
VU1_F = W1*L1/2                     # 42.00
VU1_D = VU1_F - W1*D/100            # 34.44
SAVE1 = (1 - VU1_D/VU1_F)*100       # 18.0
VS1 = VU1_D/PHI - VC                # 26.36
S1_REQ = K/(VS1*1000)               # 25.4
S1_MAX = SMAX2 if VS1 <= VC2 else SMAX4
S1 = 25.0
VS1F = VU1_F/PHI - VC               # 不用 d 偏移時
S1F_REQ = K/(VS1F*1000)
# ═════ 例② 詳細式：6-D25 拉力筋，Vu d/Mu = 0.90 ═════
AS2 = 6*5.067
RHO2 = AS2/BD                       # 0.01379
VDM2 = 0.90
VC_DET = t((0.50*SQ + 175*RHO2*VDM2)*BD)   # 23.24
VC_DET_CAP = t(0.93*SQ*BD)                 # 34.31
# ═════ 軸力 ±60 tf ═════
NU = 60.0
VC_NC = VC*(1 + NU*1000/(140*AG))   # 22.98
VC_NT = max(0.0, VC*(1 - NU*1000/(35*AG)))  # 5.87
NU_ZERO = 35*AG/1000                # 85.75
UP_C = (VC_NC/VC - 1)*100           # +17.5
DN_T = (1 - VC_NT/VC)*100           # −70.0
# ═════ 例③ 吊掛（支承在拉力側）：wu 18，ln 7.0 ═════
L3, W3 = 7.0, 18.0
VU3 = W3*L3/2                       # 63.00
VS3 = VU3/PHI - VC                  # 64.44
USE3 = VU3/VU_MAX*100               # 85.9
S3_REQ = K/(VS3*1000)               # 10.40
VU3_D = VU3 - W3*D/100              # 51.66（若誤用 d 偏移）
VS3_D = VU3_D/PHI - VC              # 49.32
S3_D_REQ = K/(VS3_D*1000)           # 13.6
AVS_UP3 = (S3_D_REQ/S3_REQ - 1)*100 # 端部箍筋量多 ≈ 30.7 %
XA = (VU3 - PVC3)/W3                # 1.06
XB = (VU3 - PVC)/W3                 # 2.69
XC = (VU3 - PVC05)/W3               # 3.09
VS_B = PVC3/PHI - VC                # 39.11（B 區起點）
SB_REQ = K/(VS_B*1000)              # 17.14
SA, SB, SC = 10.0, 15.0, 30.0
# 拉力構材的「尺」陷阱：Nu = −60 時 Vc = 5.87，但間距門檻仍是 1.06√f'c bw d = 39.11
TRAP_WRONG2 = 2*VC_NT               # 11.74（錯把 2×修正後 Vc 當門檻）
# ═════ 對帳 ═════
assert abs(VC-19.56)<0.005 and abs(VC2-39.11)<0.01 and abs(VC4-78.22)<0.01
assert abs(VU1_D-34.44)<0.005 and abs(SAVE1-18.0)<0.05 and abs(VS1-26.36)<0.01
assert abs(VC_DET-23.24)<0.01 and VDM2<=1 and VC_DET<VC_DET_CAP
assert abs(VC_NC-22.98)<0.01 and abs(VC_NT-5.87)<0.01 and abs(NU_ZERO-85.75)<0.01
assert abs(VS3-64.44)<0.01 and abs(USE3-85.9)<0.05 and abs(S3_REQ-10.40)<0.01
assert abs(XA-1.06)<0.005 and abs(XB-2.69)<0.005 and abs(XC-3.09)<0.005
assert abs(SB_REQ-17.14)<0.01 and abs(S_AVMIN-86.88)<0.01
assert VC2 < VS3 <= VC4 and VS1 <= VC2 and SA<=min(S3_REQ,SMAX4) and SB<=min(SB_REQ,SMAX2) and SC<=SMAX2
assert S1 <= min(S1_REQ, S1_MAX, S_AVMIN) and VU3 <= VU_MAX
assert abs(VS2_LIM-VC2)<0.01
if __name__ == "__main__":
    g = {k: v for k, v in globals().items() if k.isupper() and isinstance(v, float)}
    for k, v in g.items(): print(f"{k:10s} {v:10.4f}")
    json.dump(g, open("nums.json", "w"), indent=1)
