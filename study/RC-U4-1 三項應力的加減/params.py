# ── RC-U4-1 拼圖一：三項應力的加減 ── 全篇唯一數據來源（kgf、cm；彎矩輸出 t-m）
# 示範梁與 RC-U4-1 主講義「微型例題①」相同，可交叉對帳
import json
# ═════ 示範梁 ═════
L = 12.0                  # m，簡支
B, H = 40.0, 80.0         # cm
E = 25.0                  # 鋼腱偏心（形心下方）
PI_T, PE_T = 150.0, 120.0 # t（損失 20 %）
GC = 2.4                  # t/m³
WL = 2.5                  # t/m 活載
# ═════ 斷面性質 ═════
A = B*H                   # 3200
I = B*H**3/12             # 1 706 667
YT = YB = H/2             # 40
ST = I/YT; SB = I/YB      # 42 667
K = ST/A                  # 核心距 h/6 = 13.33
# ═════ 彎矩 ═════
WD = B*H/1e4*GC           # 0.768 t/m
MD = WD*L**2/8            # 13.824 t-m
ML = WL*L**2/8            # 45.00
MT = MD + ML              # 58.824
tm = 1e5                  # t-m → kgf-cm
PI, PE = PI_T*1e3, PE_T*1e3
# ═════ 傳遞階段三項（純數值） ═════
T1 = PI/A                 # 46.875
T2 = PI*E/ST              # 87.891
T3 = MD*tm/ST             # 32.400
FT_I = T1 - T2 + T3       # −8.62
FB_I = T1 + T2 - T3       # +102.37
T3_R = 13.82*tm/ST        # 用四捨五入後的 13.82 → 32.39（陷阱示範）
# 僅預力（未計自重）時的頂纖維
FT_P = T1 - T2            # −41.02
# 合成應力零點（離頂面）
Z0 = H*(-FT_I)/(FB_I - FT_I)   # 6.21 cm
# ═════ 使用階段三項 ═════
U1 = PE/A                 # 37.500
U2 = PE*E/ST              # 70.313
U3 = MT*tm/ST             # 137.869
FT_S = U1 - U2 + U3       # +105.06
FB_S = U1 + U2 - U3       # −30.06
# ═════ 非對稱斷面示範（主講義例題② 組合斷面，活載 ML2 = 32.40 t-m） ═════
YB3 = 59.61; I3 = 4729588.0; HB = 80.0     # 梁頂在 80 cm 處
SB3 = I3/YB3                                # 79 342
ST3 = I3/(HB - YB3)                         # 231 957（梁頂）
ML2 = 32.40
DB3 = -ML2*tm/SB3                           # −40.84
DT3 = ML2*tm/ST3                            # +13.97
# ═════ 對帳 ═════
assert abs(A - 3200) < 1e-9 and abs(ST - 42666.67) < 0.01 and abs(K - 13.333) < 0.001
assert abs(MD - 13.824) < 1e-9 and abs(MT - 58.824) < 1e-9
assert abs(T1 - 46.875) < 1e-3 and abs(T2 - 87.891) < 1e-3 and abs(T3 - 32.400) < 1e-3
assert abs(FT_I + 8.62) < 0.005 and abs(FB_I - 102.37) < 0.005
assert abs(FT_S - 105.06) < 0.005 and abs(FB_S + 30.06) < 0.005
assert abs(SB3 - 79342) < 1 and abs(ST3 - 231957) < 3 and abs(DB3 + 40.84) < 0.01 and abs(DT3 - 13.97) < 0.01
assert abs(T3_R - 32.39) < 0.005
if __name__ == "__main__":
    g = {k: v for k, v in globals().items() if k.isupper() and isinstance(v, float)}
    for k, v in g.items(): print(f"{k:6s} {v:14.4f}")
    json.dump(g, open("nums.json", "w"), indent=1)
