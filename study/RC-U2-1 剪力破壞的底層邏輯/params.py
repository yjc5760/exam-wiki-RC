# ── RC-U2-1 拼圖一：剪力破壞的底層邏輯 ── 全篇唯一數據來源（kgf、cm；輸出 tf）
import math, json
sq = math.sqrt
# ═════ 材料 ═════
FC, FY = 280.0, 4200.0
SQ = sq(FC)                       # √f'c = 16.733
FT = 1.06*SQ                      # 直接抗拉 ≈ 17.74
VCS = 0.53*SQ                     # 開裂剪應力（名目） 8.87
FT_R, VCS_R = FT/FC*100, VCS/FC*100          # 6.3 %、3.2 %
# ═════ 示範梁：bw = 30、h = 60、d = 50 ═════
BW, H, D = 30.0, 60.0, 50.0
AG = BW*H                          # 1800
BD = BW*D                          # 1500
t = lambda kgf: kgf/1000
VC0 = t(VCS*BD)                    # 基本式 13.30 tf
# 精算式：ρw = 0.02、Vu d/Mu = 0.5
RHO, VDM = 0.02, 0.5
VC_DET_S = 0.50*SQ + 176*RHO*VDM   # 應力
VC_DET = t(VC_DET_S*BD)            # 15.19
VC_DET_CAP = t(0.93*SQ*BD)         # 23.34
# 軸力：壓 100 tf、±30 tf
def fac(Nu_tf):                    # Nu 以 tf，壓為正
    s = Nu_tf*1000/AG
    return max(0.0, 1 + s/(140 if s >= 0 else 35))
NC100, N30 = 100.0, 30.0
F_C100, F_C30, F_T30 = fac(NC100), fac(N30), fac(-N30)
VC_C100, VC_C30, VC_T30 = VC0*F_C100, VC0*F_C30, VC0*F_T30
S_C100, S_30 = NC100*1000/AG, N30*1000/AG     # 55.56、16.67 kgf/cm²
GAIN30, LOSS30 = (F_C30-1)*100, (1-F_T30)*100   # +11.9 %、−47.6 %
NT_ZERO = t(35*AG)                 # 軸拉 63.0 tf → Vc = 0
# ═════ Vs：D13 雙肢、s = 15 ═════
AV, S15 = 2*1.267, 15.0
N_ST = D/S15                       # 3.33 支
VS15 = t(AV*FY*D/S15)              # 35.48
VS_MAX = t(2.12*SQ*BD)             # 53.21 = 4 Vc0
VS_HALF = t(1.06*SQ*BD)            # 26.61（間距減半門檻）
VN_MAX = VC0 + VS_MAX              # 66.52 = 5 Vc0
PHI = 0.75
# ═════ 設計示範：Vu = 40 tf ═════
VU = 40.0
PVC = PHI*VC0                      # 9.98
VS_REQ = VU/PHI - VC0              # 40.03
S_REQ = AV*FY*D/(VS_REQ*1000)      # 13.3 cm
S_MAX = D/4 if VS_REQ > VS_HALF else D/2   # 12.5
S_USE = min(math.floor(S_REQ*2)/2, S_MAX)  # 12.5
VS_USE = t(AV*FY*D/S_USE)          # 42.57
PVN = PHI*(VC0 + VS_USE)           # 41.90
# ═════ 陷阱：軸拉時的上限 ═════
WRONG_CAP = 4*VC_T30               # 27.9（錯）
# ═════ 對帳 ═════
assert abs(VC0 - 13.30) < 0.01 and abs(VS_MAX - 4*VC0) < 0.01 and abs(VN_MAX - 5*VC0) < 0.01
assert abs(FT - 17.74) < 0.01 and abs(VCS - 8.87) < 0.01
assert VC_DET <= VC_DET_CAP and VS_REQ < VS_MAX and PVN >= VU
assert abs(fac(-63.0)) < 1e-9
if __name__ == "__main__":
    g = {k: v for k, v in globals().items() if k.isupper() and isinstance(v, float)}
    for k, v in g.items(): print(f"{k:12s} {v:10.4f}")
    json.dump(g, open("nums.json", "w"), indent=1)
