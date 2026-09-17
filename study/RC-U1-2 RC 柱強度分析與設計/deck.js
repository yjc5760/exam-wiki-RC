const { newPres, titleSlide, topicMapSlide, formulaSlide, flowchartSlide, flowMapSlide,
        diagramSlide, cheatSheetSlide, trapSlide, tableSlide, closingSlide } = require("./lib.js");

const pres = newPres();
const FOOT = "鋼筋混凝土「柱強度分析與設計」觀念講義｜原理 · 公式 · 向量圖解";

/* 1 */
titleSlide(pres, {
  kicker: "RC-U1-2 · 鋼筋混凝土｜觀念講義",
  title: "RC 柱強度分析與設計",
  subtitle: "柱不是「加了軸力的梁」—— 它少了一條方程式，所以答案是一條曲線",
  tag: "全篇貫穿同一根示範柱：60×60 cm、8-#9、f'c 280、fy 4200",
  footer: FOOT,
});

/* 2 */
topicMapSlide(pres, {
  eyebrow: "TOPIC MAP",
  title: "一個底層邏輯、一台計算引擎、三個入口、一個 φ",
  topics: [
    { title: "底層邏輯：為什麼是曲線", desc: "柱有 c 與 P 兩個未知數，力平衡只有一條式子。少一條方程式，所以只能掃描 c，得到一整條 (Pn, Mn) 軌跡。" },
    { title: "唯一計算引擎", desc: "假設一個 c → 用「應變是直線」算每排鋼筋應力 → 做軸力平衡得 Pn、做彎矩平衡得 Mn。全單元只有這一台引擎。" },
    { title: "三大入口：c 從哪裡來", desc: "A 條件直讀（εt=0、平衡點）；B 反解二次式（給 Pu 或給 e）；C 掃描四控制點（要畫互制圖）。" },
    { title: "φ 值與破壞預警", desc: "由最外層拉力筋的 εt 決定：拉力控制 0.90、壓力控制 0.65、過渡區內插。φ 不是常數，會改變曲線形狀。" },
  ],
});

/* 3 */
diagramSlide(pres, {
  eyebrow: "DIAGRAM · 底層邏輯",
  title: "梁與柱的差別，不在「有沒有軸力」，在「少了一條方程式」",
  diagram: "rc12-fig-1-beam-vs-column",
  insights: [
    "梁：軸力 P = 0，未知數只有 c。力平衡 Cc = T 一條式子就把 c 定死，答案是唯一的 Mn。",
    "柱：未知數有 c 與 Pn 兩個，方程式只有 ΣF = 0 一條 —— 系統是不定的。",
    "少的那一條，題目會用別的方式補上：給 εt、給 Pu、給 e，或叫你自己掃描。",
    "所以柱題第一件事永遠是：先找出「c 從哪裡來」，而不是急著代公式。",
  ],
  note: "兩者共用完全相同的斷面假設：平面保持平面、混凝土極限應變 0.003、等值應力塊。",
});

/* 4 */
formulaSlide(pres, {
  eyebrow: "FORMULA · 引擎第一步",
  title: "應變是直線，鋼筋應力被 ±fy 截斷",
  formulas: [
    { label: "各排鋼筋應變 —— 幾何相似三角形，壓為正、拉為負", math: "f_eps" },
    { label: "換算鋼筋應力 —— 先用彈性式，再被 ±fy 截頂", math: "f_fs" },
    { label: "降伏應變（判斷截不截頂的門檻）", math: "f_ey" },
    { label: "最外層拉力筋應變（φ 值的唯一判準）", math: "f_et" },
  ],
  note: "最常見的錯誤是「假設鋼筋都降伏」就直接代 fy。中排鋼筋在平衡點附近幾乎一定沒降伏（本示範柱只有 386.7 kgf/cm²，不到 fy 的 1/10）。",
});

/* 5 */
diagramSlide(pres, {
  eyebrow: "DIAGRAM · 掃描的意思",
  title: "「掃描 c」到底在掃什麼？一條應變直線，換一個點",
  diagram: "rc12-fig-2-scan-c",
  insights: [
    "所有應變直線都繞著同一個支點轉 —— 頂面 εcu = 0.003 那一點，因為那是混凝土壓碎的定義。",
    "c 愈大 → 中性軸愈深 → 受壓面積愈大 → Pn 愈大，但力偶臂與拉力側的貢獻同時被犧牲。",
    "把每個 c 算出的 (Pn, Mn) 點在圖上連起來，就是 P-M 互制圖 —— 不是背來的，是掃出來的。",
    "互制曲線是斷面的身分證：一旦配筋定了，曲線就定了，與實際作用的軸力大小無關。",
  ],
});

/* 6 */
formulaSlide(pres, {
  eyebrow: "FORMULA · 引擎第二步",
  title: "軸力平衡：混凝土合力加上每一排鋼筋",
  formulas: [
    { label: "等值應力塊深度（f'c > 280 時 β1 要折減）", math: "f_a" },
    { label: "混凝土壓力合力", math: "f_cc" },
    { label: "鋼筋力：在應力塊 a 內要扣掉被占位的混凝土，在 a 外不扣", math: "f_fi" },
    { label: "軸力平衡", math: "f_pn" },
  ],
  note: "扣 0.85f'c 是因為那塊混凝土面積已經被 Cc 算過一次；漏扣會讓 Pn 偏高，整條互制曲線往外膨脹。",
});

/* 7 */
diagramSlide(pres, {
  eyebrow: "DIAGRAM · 唯一計算引擎",
  title: "給一個 c，走完這三格就得到 (Pn, Mn)",
  diagram: "rc12-fig-3-engine",
  insights: [
    "① 斷面：把每排鋼筋的深度 di 與面積 Asi 先列成表，這一步花 30 秒，後面不會亂。",
    "② 應變：εi = 0.003(c − di)/c，然後 fsi = Es·εi 但被 ±fy 截斷。",
    "③ 力：Cc 加上各排鋼筋力得 Pn；各力對形心取矩得 Mn。兩次平衡，一次都不能少。",
    "本例取平衡點 c = 32.02 cm：上排 +76.9、中排 +5.0、下排 −81.5 tf，Cc = 388.7 tf。",
  ],
  note: "全單元所有題型共用這台引擎，差別只在「c 從哪裡來」。",
});

/* 8 */
formulaSlide(pres, {
  eyebrow: "FORMULA · 引擎第三步",
  title: "彎矩平衡：對斷面形心取矩",
  formulas: [
    { label: "對形心（對稱配筋即 h/2）取矩", math: "f_mn" },
    { label: "大絕招：位於形心處的中排鋼筋，力臂為零", math: "f_arm" },
  ],
  note: "中排鋼筋會影響 Pn，但完全不貢獻 Mn。把它拿掉，Pn 會變、Mn 一點都不變 —— 這是快速檢查自己有沒有算錯的好方法。取矩點選形心而不是拉力筋，是因為柱有軸力，選形心才能讓 e = Mn/Pn 直接對應偏心距。",
});

/* 9 */
diagramSlide(pres, {
  eyebrow: "DIAGRAM · 掉分細節",
  title: "兩個最常掉分的細節：扣 0.85f'c、力臂為零",
  diagram: "rc12-fig-4-two-details",
  insights: [
    "細節一：只有落在應力塊 a 範圍「內」的壓力筋要扣 0.85f'c，在 a 外的不扣。",
    "本示範柱 a = 27.2 cm，只有上排（d = 6）在 a 內；中排 d = 30 已經在 a 外了。",
    "細節二：對形心取矩時，中排鋼筋的力臂 (h/2 − di) = 0，貢獻的彎矩是 0 不是小數。",
    "考場檢查法：把每排鋼筋的「在不在 a 內」與「力臂」先列成兩欄表格，再開始代數字。",
  ],
});

/* 10 */
diagramSlide(pres, {
  eyebrow: "DIAGRAM · 全貌",
  title: "示範柱的 P-M 互制圖：四個控制點決定整條曲線",
  diagram: "rc12-fig-5-pm-curve",
  insights: [
    "純軸壓 Po = 1062 tf 是整個斷面的軸力上限，設計時還要再乘 0.80 保留最小偏心。",
    "平衡點 (389, 101.7) 是曲線最右端 —— 標稱最大彎矩發生在這裡，不是在純彎。",
    "純彎矩 M0 = 54.6 tf·m，相當於把這根柱當梁算；平衡點是它的 1.86 倍。",
    "需求點落在曲線內側就安全，落在外側就是斷面不足 —— 這就是柱的「檢核」動作。",
  ],
  note: "四個控制點的數值全部由同一台引擎算出，沒有任何一個是查表得來的。",
});

/* 11 */
diagramSlide(pres, {
  eyebrow: "DIAGRAM · 物理機制",
  title: "P-M 圖為什麼會「鼓」出來？因為軸力在平衡點前後換了立場",
  diagram: "rc12-fig-6-why-bulge",
  insights: [
    "下半段（c < cb，拉力控制）：軸壓把受拉區壓回去，中性軸下移、力偶臂拉長 —— 軸力是幫手，P 與 M 同時增加。",
    "上半段（c > cb，壓力控制）：混凝土容量被軸力吃掉，能留給彎矩的變少 —— 軸力是兇手，P 增、M 減。",
    "轉折點就是平衡點：最外層拉力筋恰好降伏（εt = εy）的那一步。",
    "對稱配筋柱的標稱最大彎矩必在平衡點，數值約為純彎矩的 1.8 ～ 2.2 倍（本柱 1.86）。",
  ],
});

/* 12 */
tableSlide(pres, {
  eyebrow: "KNOWLEDGE CARD · 三大入口",
  title: "拿到柱題第一件事：判斷屬於哪一個入口",
  header: ["入口", "觸發關鍵字／題目條件", "c 的決定方式", "代公式難易度"],
  colW: [1.9, 3.9, 3.9, 2.4],
  rows: [
    ["A 條件直讀",
     "拉力筋應變為零／平衡點／求最大標稱彎矩／直接給 c",
     "εt = 0 ⇒ c = dt；εt = εy ⇒ cb = 6120/(6120+fy)·dt",
     "最簡單：免解方程式，直接代引擎"],
    ["B 反解方程式",
     "給定 Pu（如 Pu = 0.9Pb）／給定偏心距 e",
     "把 Pn(c) 寫成代數式，令 Pn = Pu/φ，整理成 c 的二次方程式",
     "費時但機械化：解出 c 後必須驗證降伏狀態"],
    ["C 掃描控制點",
     "要求繪製 P-M 互制圖／步驟說明的觀念題",
     "依序算 ① Po（再乘 0.80）② c = dt ③ cb ④ Pn = 0",
     "觀念題：依序代入引擎產生四個點"],
  ],
});

/* 13 */
diagramSlide(pres, {
  eyebrow: "DIAGRAM · 入口 A",
  title: "入口 A：c 直接讀出來，一行就定",
  diagram: "rc12-fig-7-entry-a",
  insights: [
    "「拉力筋應力為零」= 拉力筋應變為零 = 中性軸剛好落在最外排鋼筋上 ⇒ c = dt，不必推導。",
    "「恰好降伏」「求最大標稱彎矩」⇒ 平衡點，cb 由相似三角形直接寫出，代 fy = 4200 得 cb = 0.593dt。",
    "本柱 dt = 54 cm：εt = 0 給 (764.5, 64.67)；平衡點給 (389.1, 101.73)。",
    "這一類是柱題裡最省時間的送分題，先掃一遍考卷把它們挑出來寫。",
  ],
  note: "SI 制的常數是 600（600/(600+fy)·dt），kgf 制是 6120。用錯單位制會差約 2%，通常還是會被扣分。",
});

/* 14 */
formulaSlide(pres, {
  eyebrow: "FORMULA · 入口 A",
  title: "兩個可以直接讀出來的 c",
  formulas: [
    { label: "條件一：拉力筋應變為零", math: "f_cdt" },
    { label: "條件二：平衡點（最外層拉力筋恰好降伏）", math: "f_cb" },
  ],
  note: "cb 的推導就是相似三角形：混凝土 0.003 對應 c，鋼筋 εy 對應 (dt − c)，把 εy = fy/Es 代進去整理即得。記公式不如記這條推導，考場忘了也推得回來。",
});

/* 15 */
diagramSlide(pres, {
  eyebrow: "DIAGRAM · 入口 B",
  title: "入口 B：題目鎖住了 P 或 e，c 必須反解",
  diagram: "rc12-fig-8-entry-b",
  insights: [
    "偏心距 e 的物理意義：一個偏心 e 的軸力 Pn，等於「中心軸力 Pn」加上「彎矩 Mn = Pn·e」。",
    "在 P-M 圖上，固定 e 就是一條通過原點、斜率 1/e 的射線；它與互制曲線的交點就是斷面的容量。",
    "Pn 對 c 單調上升，所以 Pn(c) = Pu/φ 的根是唯一的，不會有「另一個解」的困擾。",
    "解出 c 之後一定要回頭驗證每排鋼筋到底降伏了沒有 —— 二次式是用某個假設整理出來的。",
  ],
  note: "φ 值一開始是未知的（它取決於 εt，而 εt 又取決於 c）。實務上先假設壓力控制 φ = 0.65 解一次，再用解出的 εt 回頭確認分區是否一致。",
});

/* 16 */
flowMapSlide(pres, {
  eyebrow: "SOLUTION FLOW",
  badge: "解",
  title: "示範柱完整走一遍：給 Pu = 350 tf，求 φMn",
  subtitle: "同一台引擎，從假設 φ 到收尾驗證",
  tag: "RC-U1-2",
  cols: 5,
  nodes: [
    { text: "Pu = 350 tf\n60×60、8-#9", type: "start" },
    { text: "假設壓力控制\nφ = 0.65", type: "decision" },
    { text: "Pn = Pu/φ\n= 538.5 tf", type: "step" },
    { text: "反解 Pn(c)\n⇒ c = 40.05 cm", type: "step" },
    { text: "a = β1c\n= 34.04 cm", type: "step" },
    { text: "各排 εi、fsi\n（上排降伏、\n中下排未降伏）", type: "step" },
    { text: "在 a 內的壓力筋\n扣 0.85f'c", type: "step" },
    { text: "對形心取矩\nMn = 91.48 tf·m", type: "step" },
    { text: "εt = +0.00104\n< εy", type: "decision" },
    { text: "確認壓力控制\nφ = 0.65 ✓", type: "step" },
  ],
  result: { text: "φMn = 0.65 × 91.48\n= 59.46 tf·m" },
  sideNote: {
    title: "假設錯了怎麼辦",
    text: "若算出的 εt 落在過渡區或拉力控制區，代表一開始假設的 φ 錯了：用新的 φ 重算 Pn = Pu/φ，再解一次 c，通常兩輪就收斂。",
    color: "pink",
  },
  checklist: {
    title: "三個必做的驗證",
    items: [
      { label: "鋼筋降伏狀態", detail: "每排都要回頭驗 εi，不可全部代 fy" },
      { label: "應力塊扣除", detail: "di ≤ a 的壓力筋要扣 0.85f'c" },
      { label: "φ 分區一致", detail: "算出的 εt 要與假設的 φ 相符" },
    ],
  },
});

/* 17 */
diagramSlide(pres, {
  eyebrow: "DIAGRAM · 入口 C",
  title: "入口 C：要畫互制圖，就依序算這四個控制點",
  diagram: "rc12-fig-9-four-points",
  insights: [
    "① 純軸壓 Po：全斷面均勻受壓，εt = −0.003；設計時再乘 0.80（締箍）或 0.85（螺箍）。",
    "② εt = 0（c = dt）：全斷面受壓的分界，最外排鋼筋應力剛好為零。",
    "③ 平衡點（c = cb）：曲線最右端，標稱彎矩的峰值。",
    "④ 純彎矩（Pn = 0）：把柱當梁算，本柱 c 只剩 8.61 cm、εt 高達 0.0158，φ = 0.90。",
  ],
  note: "答觀念題時照這四點的順序寫，每點附上 (Pn, Mn) 與 εt，就是一份完整答案。",
});

/* 18 */
formulaSlide(pres, {
  eyebrow: "FORMULA · 控制點與配筋限制",
  title: "純軸壓上限與配筋率規定",
  formulas: [
    { label: "理論純軸壓強度（扣掉鋼筋占位的混凝土）", math: "f_po" },
    { label: "設計用上限 —— 強制保留最小偏心", math: "f_pnmax" },
    { label: "主筋配筋率上下限", math: "f_rho" },
  ],
  note: "0.80 / 0.85 這個折減不是安全係數，而是規範替你保留了「施工偏差一定會造成的最小偏心」。本示範柱 Po = 1062 tf，0.80Po = 849 tf，再乘 φ = 0.65 後設計上限只剩 552 tf。",
});

/* 19 */
diagramSlide(pres, {
  eyebrow: "DIAGRAM · φ 值",
  title: "φ 是「破壞前有沒有預警」的價格標籤",
  diagram: "rc12-fig-10-phi-zones",
  insights: [
    "拉力控制（εt ≥ 0.005）：鋼筋先降伏、大變形、裂縫明顯 —— 有預警，φ = 0.90。",
    "壓力控制（εt ≤ εy）：混凝土突然壓碎、幾乎沒有前兆 —— 無預警，矩形締箍柱 φ = 0.65（螺箍 0.75）。",
    "過渡區按 εt 線性內插；分母 (0.005 − εy) 是 SD420 專用，高強度鋼筋要改成 0.003。",
    "因為 φ 在上下半段不同，設計曲線不是標稱曲線等比例縮小，形狀會改變。",
  ],
  note: "φ 的判準是「最外層」拉力筋的 εt —— 不是平均應變，也不是中排鋼筋。",
});

/* 20 */
formulaSlide(pres, {
  eyebrow: "FORMULA · φ 與設計要求",
  title: "先判分區，再決定設計強度",
  formulas: [
    { label: "分區判準（兩端點）", math: "f_phiz" },
    { label: "過渡區內插（全庫統一用現行式）", math: "f_phi" },
    { label: "設計檢核", math: "f_design" },
    { label: "高頻陷阱：最大值不能先乘再取", math: "f_peak" },
  ],
  note: "不要再用舊式 0.65 + (εt − 0.002)/0.003 × 0.25。fy = 4200 時平衡點 εt = εy = 0.00206 恰在壓力控制界限上，現行式得 φ = 0.650（不內插），舊式會得 0.655。",
});

/* 21 */
diagramSlide(pres, {
  eyebrow: "DIAGRAM · 高頻陷阱",
  title: "問「最大設計彎矩」時，答案不在平衡點",
  diagram: "rc12-fig-11-phimn-peak",
  insights: [
    "標稱最大 Mn 在平衡點（本柱 101.7 tf·m），但那裡 φ 只有 0.65，φMn = 66.1。",
    "φMn 的峰值落在拉力控制界限 εt = 0.005（c = 0.375dt），本柱 81.5 tf·m —— 高出 23%。",
    "原因：過渡區裡 φ 必須走完 0.65 → 0.90（相對 +38%），而 Mn 同區間只退約 15%。",
    "這是「折點」極大值，不是導數為零的平滑極值，所以不能微分求，要分段判斷。",
  ],
  note: "只有當軸力「可適當調整」時才有這個陷阱。題目已經給了 Pu、e 或 εt，就沒有峰值位置的問題，只要 φ 分區判對即可。",
});

/* 22 */
diagramSlide(pres, {
  eyebrow: "DIAGRAM · 細長效應",
  title: "細長效應只放大需求彎矩，不動 P-M 互制圖",
  diagram: "rc12-fig-12-slenderness",
  insights: [
    "柱受壓後會側向撓曲 δ，軸力沿著變形後的位置作用，產生額外的 Pu·δ —— 這就是二階效應。",
    "第一關：算細長比 klu/r，不超過 34 − 12(M1/M2) 就是短柱，直接用 M2。",
    "第二關：超過門檻就算放大係數 δns，把 Mc = δns·M2 送進「原封不動」的 P-M 圖檢核。",
    "最常見的錯誤是把 δns 拿去折減斷面強度 —— 它改的是需求，不是容量。",
  ],
  note: "題目一給 lu、k、βd 這三個字眼，就是在提醒你要先檢查細長比。",
});

/* 23 */
formulaSlide(pres, {
  eyebrow: "FORMULA · 細長效應",
  title: "細長比門檻與彎矩放大係數",
  formulas: [
    { label: "無側移構架的細長比門檻（矩形柱 r ≈ 0.3h）", math: "f_slend" },
    { label: "等值均佈彎矩係數（單曲率 M1/M2 為負）", math: "f_cm" },
    { label: "臨界挫屈載重（0.75 為勁度折減）", math: "f_pc" },
    { label: "彎矩放大係數 —— 放大後送進互制圖的設計彎矩為 Mc = δns·M2", math: "f_dns" },
  ],
  note: "βd 是持續載重造成的潛變效應：長期載重比例愈高，EI 折得愈多、Pc 愈小、δns 愈大。",
});

/* 24 */
flowchartSlide(pres, {
  eyebrow: "OVERVIEW · 考場作答流程",
  title: "柱題四步 SOP：先看細長，再鎖入口，最後判 φ",
  stages: [
    { type: "step", text: "① 先檢查細長效應：題目有給 lu、k、βd？有就算 klu/r，超過門檻則求 δns，得 Mc = δns·M2" },
    {
      type: "decision", question: "c 從哪裡來？（鎖定入口）",
      branches: [
        { label: "A", text: "條件直讀\nεt=0 ⇒ c=dt\nεt=εy ⇒ c=cb" },
        { label: "B", text: "反解二次式\n令 Pn(c)=Pu/φ\n或用 e=Mn/Pn" },
        { label: "C", text: "掃描四控制點\nPo → c=dt\n→ cb → 純彎" },
      ],
    },
    { type: "result", text: "執行引擎得 (Pn, Mn) → 用 dt 求 εt 判 φ → 設計強度 (φPn, φMn)，再與需求比較" },
  ],
  note: "步驟順序不能顛倒：細長效應在最前面（它改的是需求），φ 值在最後面（它要等 c 算完才知道）。",
});

/* 25 */
diagramSlide(pres, {
  eyebrow: "DIAGRAM · 合理性檢核",
  title: "檢核尺一：算出來的 Pn 一定要落在 Po 之下",
  diagram: "rc12-fig-13-check-axial",
  insights: [
    "Po 是斷面軸力的絕對上限（混凝土全斷面 + 全部鋼筋降伏），任何 Pn 都不可能超過它。",
    "平衡點的 Pb 通常落在 Po 的三分之一左右 —— 這是很好用的量級感。",
    "算出 Pn 比 Po 大，最常見的兩個原因：a 超過 h 沒有截斷、或鋼筋力的正負號寫反。",
    "設計上限 0.80Po 是給「需求」比的，不是斷面的真實容量，兩者不要混用。",
  ],
});

/* 26 */
diagramSlide(pres, {
  eyebrow: "DIAGRAM · 合理性檢核",
  title: "檢核尺二：最大彎矩約為純彎矩的 2 倍",
  diagram: "rc12-fig-14-check-moment",
  insights: [
    "對稱配筋柱，平衡點的 Mb 約為純彎矩 M0 的 1.8 ～ 2.2 倍（本柱 101.7 / 54.6 = 1.86）。",
    "算出來只有 1.1 倍，多半是漏算了某一排鋼筋，或把中排鋼筋算進了彎矩。",
    "算出來高到 3 倍以上，多半是力臂用錯（例如對拉力筋取矩卻沒補軸力的偏移項）。",
    "εt = 0 時的 Mn 會掉回純彎矩的水準 —— 這時斷面已經幾乎全壓，力偶臂所剩無幾。",
  ],
  note: "這兩把尺花不到十秒，卻能抓出絕大多數的代數錯誤。答案寫完一定要回頭量一次。",
});

/* 27 */
cheatSheetSlide(pres, {
  eyebrow: "CHEAT SHEET · 考前速查（一）",
  title: "RC 柱｜計算引擎與三大入口",
  cols: 3,
  items: [
    { label: "應變相容", math: "f_eps" },
    { label: "鋼筋應力截斷", math: "f_fs" },
    { label: "降伏應變", math: "f_ey" },
    { label: "應力塊深度 / β1", math: "f_a" },
    { label: "混凝土合力", math: "f_cc" },
    { label: "a 內：扣 0.85f'c", math: "f_fin" },
    { label: "a 外：不扣", math: "f_fout" },
    { label: "軸力平衡", math: "f_pn" },
    { label: "彎矩平衡（對形心）", math: "f_mn" },
    { label: "形心處力臂為零", math: "f_arm" },
    { label: "入口 A：εt = 0", math: "f_cdt" },
    { label: "入口 A：平衡點", math: "f_cb" },
    { label: "入口 B：偏心距", math: "f_e" },
    { label: "入口 B：反解式", math: "f_quad" },
  ],
});

/* 28 */
cheatSheetSlide(pres, {
  eyebrow: "CHEAT SHEET · 考前速查（二）",
  title: "RC 柱｜控制點、φ 值與細長效應",
  cols: 3,
  items: [
    { label: "純軸壓 Po", math: "f_po" },
    { label: "設計軸力上限", math: "f_pnmax" },
    { label: "配筋率限制", math: "f_rho" },
    { label: "最外層拉應變", math: "f_et" },
    { label: "φ 分區", math: "f_phiz" },
    { label: "φ 過渡區內插", math: "f_phi" },
    { label: "設計檢核", math: "f_design" },
    { label: "峰值陷阱", math: "f_peak" },
    { label: "細長比門檻", math: "f_slend" },
    { label: "Cm 係數", math: "f_cm" },
    { label: "臨界挫屈載重", math: "f_pc" },
    { label: "彎矩放大係數", math: "f_dns" },
    { label: "設計彎矩", math: "f_mc" },
  ],
});

/* 29 */
trapSlide(pres, {
  eyebrow: "REVIEW",
  title: "高頻陷阱精選",
  traps: [
    { title: "假設所有鋼筋都降伏", desc: "中排鋼筋在平衡點附近幾乎一定沒降伏（本柱只有 386.7 kgf/cm²）。每排都要用 fsi = Es·εi 算，再看要不要截到 fy。" },
    { title: "應力塊內的壓力筋漏扣 0.85f'c", desc: "落在 a 範圍內的壓力筋，那塊混凝土已經被 Cc 算過一次。漏扣會讓 Pn 偏高，整條互制曲線向外膨脹。" },
    { title: "把中排鋼筋算進彎矩", desc: "對稱配筋柱的中排鋼筋位於形心，力臂 (h/2 − di) = 0。它影響 Pn，但對 Mn 的貢獻是 0，不是小數。" },
    { title: "問「最大設計彎矩」卻答平衡點", desc: "標稱最大 Mn 在平衡點，但 φMn 的峰值在 εt = 0.005（c = 0.375dt）。max(φMn) ≠ φ·max(Mn)，本柱差了 23%。" },
    { title: "φ 值用中排或平均應變判斷", desc: "φ 的判準只有一個：最外層拉力筋的 εt。而且要用現行式 φ = 0.65 + 0.25(εt − εy)/(0.005 − εy)，不是舊式。" },
    { title: "把 δns 拿去折減斷面強度", desc: "細長效應改的是「需求」：Mc = δns·M2。P-M 互制圖本身完全不動 —— 那是斷面的容量，與柱多長無關。" },
  ],
});

/* 30 */
closingSlide(pres, {
  title: "RC 柱強度分析與設計｜重點回顧",
  points: [
    "柱比梁少一條方程式，所以答案是一條 (Pn, Mn) 軌跡，不是一個數字。",
    "全單元只有一台引擎：假設 c → 算各排 εi、fsi → 軸力平衡得 Pn、對形心取矩得 Mn。",
    "拿到題目先鎖入口：A 直讀、B 反解二次式、C 掃描四控制點。",
    "φ 由最外層 εt 決定；問「標稱 Mn」找平衡點，問「設計彎矩」找 εt = 0.005。",
    "細長效應放大的是需求彎矩 Mc = δns·M2，互制圖原封不動。",
    "收尾兩把尺：Pn 必須小於 Po；最大彎矩約為純彎矩的 2 倍。",
  ],
});

pres.writeFile({ fileName: "RC-U1-2 RC 柱強度分析與設計.pptx" })
    .then(() => console.log("done"));
