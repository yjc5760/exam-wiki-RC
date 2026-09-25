# ── RC-U2-1 拼圖二：三大傳力機制與桁架類比 ── 全篇唯一數據來源（kgf、cm；輸出 tf）
import math, json
sq = math.sqrt
# ═════ 材料 ═════
FC, FY = 280.0, 4200.0
SQ = sq(FC)                         # 16.733
t = lambda kgf: kgf/1000
PHI = 0.75
# ═════ 示範梁（沿用拼圖一）：bw 30、h 60、d 50 ═════
BW, H, D = 30.0, 60.0, 50.0
AG, BD = BW*H, BW*D
VC0 = t(0.53*SQ*BD)                 # 13.30 tf
VS2 = t(1.06*SQ*BD)                 # 26.61 = 2Vc（間距減半門檻）
VS_MAX = t(2.12*SQ*BD)              # 53.21 = 4Vc
VN_MAX = VC0 + VS_MAX               # 66.52 = 5Vc
PVN_MAX = PHI*VN_MAX                # 49.89
# 箍筋單肢面積（cm²）
AB = {"D10": 0.7133, "D13": 1.267, "D16": 1.986, "D19": 2.865}
AV = 2*AB["D13"]                    # 2.534（雙肢）
AV4 = 4*AB["D13"]                   # 5.068（四肢）
S15 = 15.0
N_ST = D/S15                        # 3.33 支
VS15 = t(AV*FY*D/S15)               # 35.48
VN15 = VC0 + VS15                   # 48.78
K_VS = FY*D/1000                    # Vs = (Av/s)·K_VS  → 210 tf per (cm²/cm)
X_2VC = VS2/K_VS                    # Av/s 門檻（cm²/cm）
X_CAP = VS_MAX/K_VS                 # Av/s 天花板
S_CAP = AV/X_CAP                    # D13 雙肢頂到天花板的間距 ≈ 10.0
S_2VC = AV/X_2VC                    # ≈ 20.0
# 桁架類比：斜壓桿應力 f_d = V/(bw·jd·sinθ·cosθ) = 2V/(bw·jd)，θ = 45°
JD = 0.9*D                          # 45
FD15 = 2*VN15*1000/(BW*JD)          # 72.3 kgf/cm²
FD_MAX = 2*VN_MAX*1000/(BW*JD)      # 98.6
FD_MAX_R = FD_MAX/FC                # 0.35
STRUT_D = VN15*sq(2)                # 斜桿合力（每一「格」）
# ═════ 設計示範：Vu = 40 tf ═════
VU = 40.0
PVC = PHI*VC0                       # 9.98
VS_REQ = VU/PHI - VC0               # 40.03
S_REQ = AV*FY*D/(VS_REQ*1000)       # 13.3
S_MAX = min(D/4, 30.0) if VS_REQ > VS2 else min(D/2, 60.0)   # 12.5
S_USE = min(math.floor(S_REQ*2)/2, S_MAX)                   # 12.5
VS_USE = t(AV*FY*D/S_USE)           # 42.57
PVN = PHI*(VC0 + VS_USE)            # 41.90
# ═════ STM 示範：轉換深梁 bw 40、h 100，跨中 P = 200 tf，a = 90 cm ═════
SB, SH, SA_ = 40.0, 100.0, 90.0
SP = 200.0
SR = SP/2                           # 100 tf
SD_ = 90.0                          # d
S_AD = SA_/SD_                      # 1.0
SZ = SH - 10 - 10                   # 拉桿中心距底 10、上節點中心距頂 10 → 80
STH = math.degrees(math.atan(SZ/SA_))   # 41.6°
SC = SR/math.sin(math.radians(STH))     # 壓桿 150.5 tf
ST = SR/math.tan(math.radians(STH))     # 拉桿 112.5 tf
SAS = ST*1000/(PHI*FY)              # 35.7 cm²
SAS_USE = 8*5.067                   # 8-D25 = 40.5
BS, BN = 0.75, 0.80                 # 瓶形壓桿（有配筋）、CCT 節點
FCE_S = 0.85*BS*FC                  # 178.5
FCE_N = 0.85*BN*FC                  # 190.4
SW_REQ = SC*1000/(PHI*FCE_S*SB)     # 壓桿需求寬 28.1 cm
LB_REQ = SR*1000/(PHI*FCE_N*SB)     # 支承板長 17.5 cm
# ═════ 剪力摩擦示範：施工縫 30×60，Vu = 60 tf ═════
FAC = BW*H                          # 1800
FVU = 60.0
MU_R, MU_N, MU_M = 1.0, 0.6, 1.4    # 刻意打毛／未打毛／一體澆置（λ = 1）
AVF_R = FVU*1000/(PHI*MU_R*FY)      # 19.05
AVF_N = FVU*1000/(PHI*MU_N*FY)      # 31.75
AVF_UP = (AVF_N/AVF_R - 1)*100      # +66.7 %
FVN_CAP = t(0.2*FC*FAC)             # 100.8
PFVN_CAP = PHI*FVN_CAP              # 75.6
# ═════ 對帳 ═════
assert abs(VC0 - 13.30) < 0.01 and abs(VS_MAX - 4*VC0) < 0.02 and abs(VN_MAX - 5*VC0) < 0.05
assert abs(VS15 - 35.48) < 0.01 and VS15 > VS2 and VS15 < VS_MAX
assert VS_REQ < VS_MAX and PVN >= VU and S_USE <= S_MAX
assert STH >= 25 and SW_REQ < SA_ and SAS_USE >= SAS
assert FVU <= PFVN_CAP
assert 0.3 < FD_MAX_R < 0.4
if __name__ == "__main__":
    g = {k: v for k, v in globals().items() if k.isupper() and isinstance(v, float)}
    for k, v in g.items(): print(f"{k:10s} {v:10.4f}")
    json.dump(g, open("nums.json", "w"), indent=1)
