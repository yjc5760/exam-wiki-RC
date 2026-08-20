# Wiki 操作紀錄

> append-only，請勿刪除已有紀錄

---

## 2026-05-29

- **[INIT]** 從 exam-wiki-SS 克隆，全面改寫為 RC 科目（鋼筋混凝土設計與預力）
  - 改寫 CLAUDE.md（身份層）、CLAUDE-SOLVE.md（解題規範）、CLAUDE-SPEC.md（命名規格）
  - 改寫 CLAUDE-CODE.md（Runbook）、README.md（導覽）
  - 重建 wiki/index.md（RC 七層架構）、wiki/by-year.md（2002–2025 空白表格）
  - 重建 raw/json/question_index.json（空白索引）、concepts.json（RC 核心概念）
  - 科目代碼：RC｜題目編號格式：RC-YYYY-N

## 2026-06-07

- **[INGEST-BATCH]** 批次 ingest 94 題（所有 verificationStatus=verified 且 hasSolution=true）
  - 生成 wiki/problems/ 共 94 個頁面
  - 重建 wiki/index.md（依 RC-UN-n 分類，含題目連結表格）
  - 重建 wiki/by-year.md（2002–2025 年，含題號連結）
  - 涵蓋年份：2002–2025

## 2026-06-07

- **[COMPILE-ALL]** 完整重新編譯 wiki 知識庫
  - 生成 wiki/concepts/：10 個概念頁面
  - 生成 wiki/methods/：4 個解題方法論頁面
  - 確認 wiki/queries/ 存在
  - 建立 wiki/philosophy/index.md
  - wiki/problems/（94題）已於本日批次 ingest 完成
  - 未覆蓋：diagnosis/ · failure-modes/ · materials/ · code-ref/（Cowork 直接維護）

## 2026-06-07

- **[LINT-FIX]** 修復全部 7 項 lint 問題：
  - 概念頁補充：DUCTILE-FAILURE, LONG-COLUMN-MOMENT-MAGNIFIER, LONG-TERM-DEFLECTION, CREEP-SHRINKAGE, SPECIAL-MOMENT-FRAME-BEAM, SPECIAL-MOMENT-FRAME-COLUMN（6 頁）
  - 圖說補充：RC-2024-4-fig-1、RC-2025-3-fig-1（圖說缺漏）；RC-2023-4 加入 eqn-1.png 引用與 LaTeX 圖說
  - diagnosis/ 建立：beam-flexure, column-pm, shear-torsion, prestress, deflection-crack（5 頁）
  - failure-modes/ 建立：flexure, shear, crushing, deflection, cracking（5 頁）
  - materials/ 建立：concrete-stress-strain, steel-yielding, creep-shrinkage, prestress-strand（4 頁）
  - P-M 互動圖生成：10 個柱設計題（RC-2002-2 等），更新 hasViz=true

## 2026-06-07

- **[CLEANUP]** 清除 SS 鋼結構殘留：186 個檔案（problems/98 + concepts/58 + methods/19 + traps/11）
- **[CONCEPTS]** concepts.json 新增 7 個高頻概念（SHEAR-STRENGTH、TORSION-DESIGN、PUNCHING-SHEAR、SEISMIC-DESIGN、DEVELOPMENT-LENGTH、DEFLECTION-CONTROL、CRACK-WIDTH）
- **[FIX]** RC-2012-2 verificationStatus 改回 unverified（hasSolution=false，狀態矛盾修正）
- **[QUERY]** 建立 wiki/queries/題庫缺口報告（2017整年缺失、RC-2016-3、RC-2012-2）

## 2026-06-07

- **[REINDEX+INGEST]** 題庫補齊，新增 6 題（RC-2012-2、RC-2016-3、RC-2017-1~4）
  - question_index.json：共 100 題（verified+hasSolution：100 題）
  - wiki/problems/：新增 6 個頁面
  - wiki/by-year.md、wiki/index.md：重建完成
  - 題庫缺口報告更新：無缺口

## 2026-06-07

- **[CLEANUP-2]** 清除 SS 殘留 56 個（code-ref/22、philosophy/10、diagnosis/8、failure-modes/5、materials/5、queries/6）
- **[REBUILD]** 重建各目錄 RC 版 index.md（6 個目錄）
- **[ADD]** 補建 wiki/diagnosis/seismic.md

## 2026-06-08

- **[COMPILE-ALL]** 全面重建 wiki 知識庫（compile-all + ingest 完整驗證）
  - 確認 wiki/concepts/：17 個概念頁面（BALANCED-REINFORCEMENT-RATIO 至 CRACK-WIDTH 全部存在）
  - 確認 wiki/problems/：100 個題目頁面（2002–2025 全部 verified 題目）
  - 重建 wiki/index.md：採七層知識架構 + 四單元分類導航格式，含全部 100 題連結
  - 確認 wiki/by-year.md：2002–2025 完整年份表格（無需修改）
  - **[NEW]** 建立 wiki/traps/：13 個陷阱頁面 + index.md（T形梁、φ值、耐震Ve、預力fps、預力損失、扭力門檻、衝剪、細長柱、平衡鋼筋比、雙筋梁壓力筋、梁柱接頭、剪力臨界斷面、有效慣性矩）
  - **[LINT]** 執行 16 項健檢，結果：11項PASS、2項WARNING、3項SKIP（需bash）；完整報告：wiki/queries/lint-report-2026-06-08.md
  - **[FIX-1]** 同步 STIRRUP-DESIGN 至 concepts.json（第 18 個概念）
  - **[FIX-2]** 建立 wiki/code-ref/ 實體頁面（ACI-318.md、CNS-1480.md、seismic-code.md），更新 index.md；code-ref 從 stub 升格為完整規範速查層
  - 操作者：Cowork

## 2026-06-09

- **[COMPILE-ALL]** 全面重建 wiki 知識庫（全部修正），compile-all 第二次完整執行
  - 全部 100 題 wiki/problems/ 頁面確認（2002–2025 年，100 題均 verified）
  - **[CONCEPTS]** 24 個概念頁面全部以 §7.2 完整格式重新生成：
    - BALANCED-REINFORCEMENT-RATIO、WHITNEY-STRESS-BLOCK、BETA1-FACTOR
    - PM-INTERACTION-DIAGRAM、BALANCED-POINT、EFFECTIVE-MOMENT-OF-INERTIA
    - CRACKING-MOMENT、PRESTRESS-LOSS、EFFECTIVE-PRESTRESS、STRONG-COLUMN-WEAK-BEAM
    - SHEAR-STRENGTH、TORSION-DESIGN、PUNCHING-SHEAR、SEISMIC-DESIGN
    - DEVELOPMENT-LENGTH、DEFLECTION-CONTROL、CRACK-WIDTH、STIRRUP-DESIGN
    - DUCTILE-FAILURE、LONG-COLUMN-MOMENT-MAGNIFIER、LONG-TERM-DEFLECTION
    - CREEP-SHRINKAGE、SPECIAL-MOMENT-FRAME-BEAM、SPECIAL-MOMENT-FRAME-COLUMN
  - 格式特徵：每頁含完整 LaTeX 公式（$$...$$）、定義段落、前置概念、相關概念、常見陷阱、出現題目表格
  - **[INDEX]** 重建 wiki/index.md：七層知識架構表 + 24 概念快速導覽表（依四單元分類）+ 全 100 題連結
  - **[BY-YEAR]** 重建 wiki/by-year.md：2002–2025 年全 100 題，改為 [[RC-YYYY-N]] Obsidian 連結格式
  - 操作者：Cowork

## 2026-06-09

- **[METHODS]** 建立 wiki/methods/ 完整解題方法論目錄（Layer 3）
  - 新建 index.md：列出 8 個方法論頁面
  - 新建 WHITNEY-STRESS-BLOCK-METHOD.md（等值矩形應力塊，RC-U1-1/U1-2）
  - 升級 PM-INTERACTION-DIAGRAM.md（原 stub → 完整版含 LaTeX 公式與出現題目表）
  - 新建 MOMENT-MAGNIFIER.md（長柱放大彎矩法，RC-U1-3）
  - 新建 EFFECTIVE-INERTIA.md（有效慣性矩撓度計算法，RC-U3-1）
  - 新建 PRESTRESS-LOSS-CALC.md（預力損失計算流程，RC-U4-3）
  - 新建 T-BEAM-ANALYSIS.md（T 形梁彎矩強度分析法，RC-U1-1）
  - 新建 FRICTION-LOSS-METHOD.md（摩擦損失計算法，RC-U4-3）
  - 新建 SEISMIC-CAPACITY-METHOD.md（耐震能力設計法，RC-U3-3）
  - 知識庫健康狀態：wiki/ 七層架構全部完整，無缺漏
  - 操作者：Cowork

## 2026-06-10

- **[FREQUENCY]** 執行 frequency 指令，生成 wiki/queries/frequency-20260610.md
  - 統計全 100 題（2002–2025）各 topicId 出現頻次（primary + secondary）
  - 結果：RC-U1-1=22、RC-U4-1=21、RC-U1-2=19、RC-U3-3=16、RC-U2-1=16
  - 操作者：Cowork

- **[PREDICT]** 執行 predict 指令，生成 wiki/queries/predict-2026-20260610.md
  - 基於頻次統計＋近年趨勢＋補考點分析推測 2026 高機率考題
  - 優先補考點：RC-U3-1（8 年未考）、RC-U4-3（7 年未考）、RC-U1-3（10 年未考）
  - 操作者：Cowork

- **[RAW-METHODS]** 補建 raw/solutions/methods/ 來源檔案（4 個方法論 .md）
  - 新建 raw/solutions/methods/effective-inertia-deflection/effective-inertia-deflection.md
  - 新建 raw/solutions/methods/moment-magnifier-method/moment-magnifier-method.md
  - 新建 raw/solutions/methods/prestress-loss-calculation/prestress-loss-calculation.md
  - 新建 raw/solutions/methods/pm-interaction-diagram/pm-interaction-diagram.md
  - 修正 raw/→wiki/ 單向資料流缺口，4 個 wiki/methods/ 頁面現有對應原始檔
  - 操作者：Cowork

- **[TRAPS-BACKLINKS]** 建立 traps↔problems 雙向連結
  - 讀取全部 13 個 wiki/traps/ 陷阱頁，建立完整 trap→problem 對應表
  - 在 52 個 wiki/problems/ 頁末尾加入「## 相關陷阱」反向連結區塊
  - 涵蓋陷阱：T-BEAM-EFFECTIVE-WIDTH、BALANCED-RATIO-BOUNDARY、PHI-FACTOR-TRANSITION、COMPRESSION-STEEL-YIELDING、SHEAR-CRITICAL-SECTION、TORSION-THRESHOLD、DEFLECTION-EFFECTIVE-INERTIA、PUNCHING-SHEAR-CRITICAL、SEISMIC-BEAM-VE、JOINT-SHEAR-EFFECTIVE-AREA、LONG-COLUMN-SLENDERNESS、PRESTRESS-LOSS-SEQUENCE、PRESTRESS-FPS-FORMULA
  - wiki/traps/ 雙向連結完整度：13/13 陷阱頁均建立反向連結
  - 操作者：Cowork

## 2026-06-11

- **[HEALTH-CHECK]** 知識庫一致性健檢（補完 2026-06-08 lint 報告的 4 項 SKIP 掃描）
  - hasViz 比對：索引 14 題 hasViz=true ↔ raw/solutions/ 實際 16 個 *-viz.html（RC-2014-2、RC-2014-4 各 2 個），完全一致 ✅
  - hasHandwritten 比對：索引 0 題 ↔ 實際 0 個 *hand*.png，一致 ✅
  - 圖說掃描：59 個含 fig-*.png 的解析檔全部具備「圖說：」段落 ✅
  - lint 待補清單覆核：code-ref 實體頁 ✅、STIRRUP-DESIGN 已入 concepts.json ✅、raw methods 來源 ✅（均已於 06-08~06-10 解決）
  - 結論：資料層無待修項
  - 操作者：Cowork

- **[DASHBOARD]** 建立知識庫儀表板（新增使用者入口）
  - 新建 index.html（離線單檔，雙擊即用）：題庫瀏覽（年份/單元/考點/設計法/標籤/關鍵字篩選）、考點統計圖、近5年走向、高頻標籤、讀書進度追蹤（localStorage）、七層架構導覽、16 指令速查
  - 新建 dashboard-data.js（question_index.json 快照，100 題）
  - 新增指令 REFRESH-DASHBOARD（觸發語句「更新儀表板資料」），登錄於 CLAUDE-CODE.md
  - 操作者：Cowork

- **[DASHBOARD-v2]** 儀表板新增站內解析閱讀器
  - 「完整解析」改於站內彈窗開啟：內建 Markdown 渲染器（標題/表格/清單/引用/程式碼區塊/圖片）＋ KaTeX 公式渲染（$...$ 與 $$...$$，CDN 載入、離線時顯示原始 LaTeX）
  - 因瀏覽器 file:// 安全限制，採 File System Access API：首次使用授權選擇 exam-wiki-RC 資料夾一次（儲存於 IndexedDB），即可讀取所有解析檔與附圖
  - 題目附圖以 Blob URL 載入；解析內 .md 相對連結可於閱讀器內跳轉
  - 移除題卡「wiki 題目頁」連結（依使用者要求）；知識庫導覽卡片也改走站內閱讀器
  - 操作者：Cowork

- **[DASHBOARD-v3]** 解析閱讀器新增「匯出 PDF」按鈕
  - 採瀏覽器原生列印管道（目的地選「另存為 PDF」）：向量文字、中文與 KaTeX 公式完整保留、離線可用
  - 列印樣式僅輸出解析內容＋標頭（題號、來源路徑、匯出日期）；表格/圖片/公式避免跨頁截斷
  - 匯出時自動以題號設定預設 PDF 檔名
  - 操作者：Cowork

- **[METHODS-CONSOLIDATION]** 整併 wiki/methods/ 雙命名體系（lint 後續優化）
  - 問題：methods/ 同時存在大寫頁（8 個，06-09 建立、index 引用、無 raw 來源）與 kebab 頁（3 個，06-10 raw 對應版），4 組內容重複；且多數大寫頁「出現題目」表與 question_index 不符（如 EFFECTIVE-INERTIA 原列 4 題中 3 題為剪力牆/預力/扭力題）
  - 整併為 8 個 kebab-case 方法頁（符合 CLAUDE-SPEC 命名規範）：whitney-stress-block-method、pm-interaction-diagram、moment-magnifier-method、t-beam-analysis、effective-inertia-deflection、seismic-capacity-method、prestress-loss-calculation、friction-loss-method
  - 所有「出現題目」表依 question_index.json 標籤重新核實重建
  - 補建 4 個 raw 來源：whitney-stress-block-method、t-beam-analysis、friction-loss-method、seismic-capacity-method；更新既有 4 個 raw 來源為完整版（與 wiki 頁同步）
  - 重寫 wiki/methods/index.md（8 法索引）
  - MOMENT-MAGNIFIER.md、EFFECTIVE-INERTIA.md、PRESTRESS-LOSS-CALC.md 改為廢棄轉址 stub
  - 操作者：Cowork

- **[ARCHIVE]** raw/json/ 暫存檔歸檔至 study/_archive/
  - pdf_text.txt、pdf_2016_blocks.txt、pdf_2016_text.txt 已複製到 study/_archive/（附 README 說明）
  - 操作者：Cowork

- **[PENDING-DELETE]** 待刪除清單（沙箱環境因磁碟空間不足無法啟動，刪除作業暫緩）
  - raw/json/pdf_text.txt、raw/json/pdf_2016_blocks.txt、raw/json/pdf_2016_text.txt（已歸檔至 study/_archive/）
  - wiki/methods/MOMENT-MAGNIFIER.md、EFFECTIVE-INERTIA.md、PRESTRESS-LOSS-CALC.md（廢棄轉址 stub）
  - raw/solutions/RC-2015-1 ~ RC-2015-4 等資料夾內的 .placeholder 空檔
  - 檔名大小寫正規化：PM-INTERACTION-DIAGRAM.md → pm-interaction-diagram.md 等 5 檔（Windows 大小寫不敏感，連結已可解析，僅顯示名稱待改）
  - 環境恢復後對 Cowork 說「清理待刪除檔案」即可執行
  - 操作者：Cowork
- [2026-06-29] ingest RC-2023-1: �ɥR PDF �P��s��ı�ƹϪ�

## 2026-07-01

- **[DASHBOARD-v4]** 考點統計頁籤改為 frequency 指令格式；補充筆記 PDF 改為靜態資料驅動
  - 「考點統計」頁籤重寫為 frequency 指令輸出格式：高頻考點 Top10（主＋副）、各單元命題比例、近5年趨勢動態列表；移除原「設計法分布」與「高頻標籤 Top20」兩張卡片
  - dashboard-data.js 資料格式新增第 7 個欄位 pdf（補充筆記檔名陣列）；index.html 移除「📎 掃描補充 PDF」按鈕與前端即時掃描機制（injectPdfButtons/pdfCache/listDir），改為依靜態資料直接顯示「📎 補充筆記 PDF」按鈕
  - 同步更新 CLAUDE-CODE.md（REFRESH-DASHBOARD 規格）、CLAUDE-SPEC.md（補充筆記 PDF 說明）、CLAUDE.md（CHANGELOG）
  - 操作者：Cowork

- **[REFRESH-DASHBOARD]** 重新生成 dashboard-data.js
  - 掃描 raw/json/question_index.json：100 題（無變動）
  - 掃描 raw/solutions/RC-*/*-viz.html：18 個互動圖檔（無變動，維持既有 15 題的 viz 對應）
  - 掃描 raw/solutions/RC-*/*.pdf：新發現 RC-2023-1 資料夾下 2 個補充 PDF（RC-2023-1.pdf、RC-2023-1_補充.pdf），已寫入 dashboard-data.js pdf 欄位；其餘 99 題維持 []
  - 核對 raw/json/syllabus_taxonomy.json（RC 分類樹）：window.RC_TOPICS／window.RC_UNITS 內容一致，無需更動
  - 操作者：Cowork

## 2026-07-10 STUDY（子項層級 ×5）

- 指令：`study RC-U1-1`、`study RC-U1-2`、`study RC-U2-1`、`study RC-U3-3`、`study RC-U4-1`
- 產出（七區塊互動 HTML，KaTeX 渲染、自含檔案）：
  - study/study-RC-U1-1.html — 梁彎矩強度分析與設計（主 19 題／相關 22 題，排名 1，近6年 5/6）
  - study/study-RC-U1-2.html — 柱強度分析與設計（主 12／相關 20，排名 4，近6年 3/6）
  - study/study-RC-U2-1.html — 剪力強度分析與設計（主 7／相關 16，排名 6，近6年 5/6）
  - study/study-RC-U3-3.html — 韌性要求與耐震設計（主 16／相關 18，排名 2，近6年 2/6）
  - study/study-RC-U4-1.html — 預力梁斷面應力分析（主 13／相關 21，排名 3，近6年 5/6）
- 資料來源：raw/json/question_index.json（100 題，2002–2025，全數 verified）
- 考題連結格式：`../index.html#md=raw/solutions/RC-YYYY-N/RC-YYYY-N.md&t=RC-YYYY-N`（符合 CLAUDE-CODE.md STUDY 規格）
- 驗證：五頁題數與索引一致（22/20/16/18/21）、題號全數存在且相關、JS 語法檢查通過（node --check）
- 互動計算器：U1-1 矩形梁 φMn／U1-2 柱 P-M 強度點／U2-1 梁剪力檢核／U3-3 圍束箍筋 Ash／U4-1 預力梁兩階段應力
- 操作者：Cowork

## 2026-07-19

- **[UI-UPDATE]** 於 `study/` 目錄下的 5 個 `study-RC-U*.html` 主題總覽區塊右側，新增「Keynote」按鈕，並分別連結至對應的 PDF 講義檔案。
- 操作者：Cowork

## 2026-07-25 UNIT-LECTURE（RC-U1-1 觀念講義）

- 觸發：`生成 RC-U1-1 講義`（外部 `unit-lecture` skill，非本知識庫 16 指令之一）
- 產出：
  - `study/lecture-RC-U1-1.html` — 理解導向觀念講義，13 節（§0 全景 → §12 精選 5 題），10 張內嵌 SVG 圖解
  - `study/lecture-RC-U1-1.pdf` — 21 頁 A4 可列印版（MathJax→SVG + WeasyPrint）
  - `study/assets/katex/` — 離線 KaTeX（約 600 KB），本科所有 lecture 頁共用，勿刪
- 定位：與 `study/study-RC-U1-1.html`（速查頁）**並存不覆蓋**；速查頁供練題時查，講義供練題前建立物理直覺
- 內容主軸：核心對立「強度＝力的平衡／安全＝應變的幾何」；每個規範常數追來源
  （0.85 ← Rüsch 持續載重效應；β₁=2k₂ ← 應力分布形心；6120 ← εcu·Es；3/7 ← 0.003/0.007；ρmin 的 √f'c ← 破裂模數 fr=2√f'c）
- 涵蓋題數：19 主分類 + 3 副分類 = 22 題（2002–2024），全數 verified
- 精選 5 題：RC-2023-2、RC-2011-2、RC-2007-1、RC-2015-2、RC-2016-1
  （誠實標註未涵蓋：RC-2014-1 過筋梁、RC-2014-2 M-φ 三階段、RC-2015-3 負彎矩 T 形梁、RC-2022-2 材料經濟性）
- 考題連結格式：`../index.html#md=raw/solutions/RC-YYYY-N/RC-YYYY-N.md&t=RC-YYYY-N`（同 STUDY 規格）
- 驗證：22 題號與 question_index.json 完全對齊（無缺漏／誤植／年份錯誤，解析檔皆存在）；
  29 項數值以 Python 重算吻合（β₁ 分段、φ 內插、ρb/ρmax/ρmin 比值、RC-2023-1 曲率延展比算例 μφ=3.61→4.96）；
  PDF 抽查 9 頁確認無 MathJax 黑方框、SVG 文字無溢出；節號交叉引用完整
- 連動修改：README.md（快速導航＋檔案地圖）、CLAUDE.md（資料夾結構＋CHANGELOG）、
  檔案架構索引表.md（study/ 與 assets/ 兩列）、CLAUDE-CODE.md（STUDY 段落加交叉註記，未新增指令）、
  study/study-RC-U1-1.html（新增「觀念講義」按鈕）
- 操作者：Cowork
- 2026-07-25｜FIX｜**單位係數勘誤（跨科稽核發現）**。於 exam-wiki-SS 修正一批公式單位錯誤後，回頭稽核六科知識庫，在 RC 發現兩處：
  1. `wiki/code-ref/CNS-1480.md` §混凝土彈性模數：`Ec = 4270√f'c (kgf/cm²) ≈ 15100√f'c (MPa)` —— **兩個單位標籤對調**，且 kgf/cm² 制係數誤植為 4270。正確為 `Ec = 15100√f'c (kgf/cm²) = 4700√f'c (MPa)`。原式誤差達 3.2～3.5 倍，會直接毀掉撓度與轉換斷面計算。已改正並加入驗算示例（f'c=280 kgf/cm² 時兩制應同得約 25 萬 kgf/cm²）與記憶法（係數大的配單位小的）。
  2. `f_r` 的 MPa 制係數不一致：`wiki/code-ref/CNS-1480.md` 與驗證解答 RC-2018-4 均為 `0.623√f'c`，但 `wiki/concepts/GLOSSARY.md`、`wiki/traps/DEFLECTION-EFFECTIVE-INERTIA.md`、`wiki/methods/effective-inertia-deflection.md` 寫成 `0.7√f'c`（差 12%；0.7 為 ACI 318-99 舊版值）。依規則 2 以驗證解答為準，已將 GLOSSARY 與 traps 兩檔改為 0.623。
  驗算方式：以 f'c = 280 kgf/cm² = 27.5 MPa 雙制互換確認；fr 以 2.0√f'c(kgf/cm²) 為錨點換算得 0.626 ≈ 0.623。
  ⚠️ **未完成**：`wiki/methods/effective-inertia-deflection.md` 的 `0.7` 尚未修正，因其 compile 來源在 `raw/solutions/methods/effective-inertia-deflection/`，而 RC 的規則 1 目前尚未開放 methods 例外（SS 已於同日開放）。待決定是否比照 SS 修改 RC 的 CLAUDE.md 規則 1。
  同時確認：SS 的 ASD/LTB 係數錯誤（703,000 / 1,170,000 / 1,055,000、Lp=300ry、Lr 分母、λ 138/322）**未擴散**至 RC/SA/SD/SM/MM 任一科（該類公式為鋼結構專有）。
- 2026-07-25｜HARNESS + FIX｜規則 1 例外擴充（比照 SS）：`raw/` 唯讀例外增列 `raw/solutions/methods/`，並訂三項條件（驗算／同步 wiki／記 log）；`CLAUDE.md`（規則 1、結構圖 🔒/✏️ 標記、單向資料流、CHANGELOG）與 `CLAUDE-CODE.md`（新增 FIX-METHOD 流程）同步更新。依此完成前一筆待辦：`raw/solutions/methods/effective-inertia-deflection/` 的 `f_r = 0.7√f'c (MPa)` 已改為 `0.623√f'c` 並同步覆蓋 `wiki/methods/`。至此 RC 全庫 6 處 f_r 定義一致（0.623），與驗證解答 RC-2018-4 相符。
- 2026-07-26｜FIX｜**梁柱接頭 γ 係數全庫勘誤（8 檔 15 處）**：撰寫 RC-U3-3 觀念講義時發現全庫對 `φVn = φγ√f'c·Aj` 的 γ 存在**三套互相矛盾**的數字。
  **錯在哪：**
  1. `wiki/code-ref/ACI-318.md` §18.8.4.2、`wiki/code-ref/seismic-code.md`、`wiki/traps/JOINT-SHEAR-EFFECTIVE-AREA.md`：寫成 `1.0 / 0.75 / 0.50`（另加「僅一面有梁 0.30」）—— **不對應任何常用單位制**。
  2. `wiki/diagnosis/seismic.md`：寫成 `3.2（內）/ 2.4（邊）/ 1.6（角）` —— 數字**整組往下移了一階**；3.2 實為「其他類接頭」的值，被誤標為內接頭。
  3. `wiki/code-ref/CNS-1480.md`：把差異歸因於「舊 CNS/ACI-318-99 用 4.0/3.2/2.4 vs 新 ACI-318-08 用 1.0/0.75/0.50」—— **歸因錯誤**，差異來自單位制而非規範版本；且兩欄數字皆有誤。
  4. `wiki/philosophy/seismic-philosophy.md`：RC-2018-2 標為 `γ=1.6（外接頭）`（應為 3.2）；RC-2005-3 標為 `γ=3.2（內接頭筆誤需判斷）`（該題本就是**外／角接頭**，3.2 正確，原註解反而把正確值說成筆誤）。
  5. `raw/solutions/methods/seismic-capacity-method/` 與 `wiki/methods/SEISMIC-CAPACITY-METHOD.md`：`1.7 / 1.2 / 1.0` 數值接近正確（MPa 制）但**未標單位制**，且 1.2 應為 1.25 —— 正是全庫混淆的根源。
  **改成什麼：** 八個檔案統一改為三單位制對照表 —— 四面有梁（內接頭）`psi 20 / MPa 1.7 / kgf-cm² 5.3`；三面或對面兩面（T 形）`15 / 1.25 / 4.0`；其他（外／角接頭）`12 / 1.0 / 3.2`，並註明「同一組值的三種單位制，非三套規範」與「作答須寫明單位制」。
  **怎麼驗證的（依規則 2，以 verified 解答為錨點）：**
  - `wiki/problems/RC-2005-3.md`（verified）明載「角柱（外接頭）=3.2、T 形接頭=4.0、十字形（內接頭）=5.3」，並附推導 `γ = 12 psi^0.5 × 0.265 = 3.18 ≈ 3.2`。
  - `wiki/problems/RC-2003-3.md`（verified）明載「內部接頭四面有梁圍束，γ=5.3（kgf/cm² 制，對應 ACI psi 制之 20）」。
  - 量綱換算獨立重算：psi→kgf/cm² 乘 √0.0703 = 0.2651（20→5.303、15→3.977、12→3.182）；psi→MPa 乘 √0.006895 = 0.08304（20→1.661、15→1.246、12→0.996）。三組值互相自洽。
  - 註記：RC-2018-2 內柱寫 5.4 屬換算取捨（5.303 進位），已於表下說明，不視為衝突。
  **順帶修正（同檔同性質、同樣以 verified 解答驗證）：** `wiki/diagnosis/seismic.md` 柱密箍區間距的第三條件寫成固定 `14cm`，與 RC-2013-2、RC-2012-3 兩份 verified 解答所用 `so = 10+(35-hx)/3 ≤ 15cm` 不符，已改正。
  **規則遵循：** `code-ref/`、`diagnosis/` 屬規則 4 例外，可直接維護；`raw/solutions/methods/` 依規則 1 例外修改，已完成驗算＋同步覆蓋 `wiki/methods/`＋本筆紀錄三項條件。`traps/`、`philosophy/` 雖非規則 4 例外，但經核對 CLAUDE-CODE.md 的 COMPILE-ALL 步驟，其生成清單僅含 concepts/ · methods/ · problems/ · index.md · by-year.md，**不會重新生成 traps/ 與 philosophy/**（INGEST 僅更新 traps 的「出現題目」表格），故直接修正不會被蓋回，且其內容原本即與自身來源（verified 解答）矛盾。
  **未處理／待確認：** `wiki/diagnosis/seismic.md` 梁密箍區長度寫 `lo = max(2h, ln/4, 450mm)`，但 ACI 318 §18.6.4.1 與 RC-2025-2 verified 解析均為單一條件 `2h`；因不確定 `ln/4, 450mm` 是否引自其他規範（如中等抗彎構架），暫未更動，待使用者確認。
- 2026-07-26｜FIX｜**梁密箍區長度 lo 勘誤（承前一筆待確認事項，使用者裁示依 ACI 318 §18.6.4.1 修正）**：
  **錯在哪：** `wiki/diagnosis/seismic.md` 決策樹將特殊矩形框架梁的密箍區長度寫成 `lo = max(2h, ln/4, 450mm)（梁端）`。
  ACI 318 §18.6.4.1 對**梁**只有**單一條件**：自支承構材面向跨中量起 `2h`（h 為梁全高）；
  `ln/6`、`450mm` 是**柱**的規定（§18.7.5.1 `lo ≥ max(h, lu/6, 450mm)`），`ln/4` 則不屬於任一條。
  **改成什麼：** 改為 `lo = 2h（單一條件，自柱面量起）`，並加註「梁沒有 ln/6、ln/4 或 450mm，那是柱 §18.7.5.1」；
  同檔「常見陷阱」條目由籠統的「梁和柱的密箍區定義不同」改寫為明列兩者公式與條文號。
  **怎麼驗證的：** ① 條文對照 ACI 318 §18.6.4.1（梁）vs §18.7.5.1（柱）；
  ② 驗證解答 `RC-2025-2` 明載「密箍區：自柱面算起 2h」（單一條件）；
  ③ 反向核對柱題 `RC-2012-3`、`RC-2013-2`、`RC-2009-1` 三份 verified 解答，其 `max(..., lu/6, 45cm)` 三式取大**均為柱**，證實三條件屬柱而非梁。
  **全庫掃描結果：** 修正後全庫已無 `ln/4` 記載；`code-ref/ACI-318.md` §18.6.4.4、`code-ref/seismic-code.md`、
  `concepts/SPECIAL-MOMENT-FRAME-BEAM.md`、`methods/SEISMIC-CAPACITY-METHOD.md` 對梁均已正確寫為 `≥ 2h`，無須更動。
  **⚠️ 未更動（受規則 1、2 保護，僅記錄）：** `raw/solutions/RC-2016-2/RC-2016-2.md` 第 63／140／258／353 行寫
  `lo = max(2h, ln/6, 45cm)` 並標註「ACI 318-14 §18.6.4.1」—— 條文號與三條件不符（三條件應屬 §18.7.5.1 柱）。
  惟該題實算 `max(140, 125, 45) = 140 cm` 由 `2h` 控制，**最終答案 140 cm 不受影響**，
  依規則 2（verifiedSolution 為最終答案，不可質疑或重算）不予更動；其 ingest 副本 `wiki/problems/RC-2016-2.md` 亦同步保留原樣。
  若日後決定修訂該題敘述，須經使用者確認後再動 raw 端。
- 2026-07-26｜FIX｜**剪力臨界斷面「d 偏移」判準改寫為條件式（`wiki/traps/SHEAR-CRITICAL-SECTION.md`）**：
  **錯在哪：** 原頁把「倒 T 型梁」直接列入「不可使用此有利規定（必須取支承面）」清單，寫成**構件形狀 → 結論**。
  但唯一的證據來源 `RC-2020-2`（verified）判定該題倒 T 梁**可以**採 d 偏移，理由是「均佈載重施加於梁頂部（壓力側），並非自下翼板懸吊」，
  並附完整物理說明（「若載重從拉力側懸吊進入腹板，斜壓撐機制就不成立」）與實務註記。原頁敘述與自身來源矛盾。
  另原頁「可取 d 處」只列兩個條件（支承提供壓力、支承限制開裂），與 ACI 318 §9.4.3.2 的三條件不符（漏了「無集中載重」，且第二條非規範文字）。
  **改成什麼：**
  ① 「臨界斷面規則」段改以 ACI 318 §9.4.3.2 **三條件 (a)(b)(c)** 為主體（支承反力產生壓力／載重在頂面／區間內無集中載重），
     並加註「判準是條件，不是構件名稱」；原有的構件案例改列為「典型會違反哪一條」。
  ② 倒 T 型梁改為條件式：違反的是 (b)，且明確指出「同樣是倒 T 梁，載重在頂面則仍可用」。
  ③ 「梁端搭接接頭」非 §9.4.3.2 列舉條件，標示為**實務補充考量**，保留但要求採用時註明依據（未刪除原有內容）。
  ④ 常見陷阱表同步改寫；「出現題目」表補上 RC-2023-3。
  **⚠️ 同時揭露一項知識庫內部衝突（未判定、未更動任何 raw 內容）：**
  懸臂梁能否採 d 偏移，兩份 verified 解答處理**相反** ——
  `RC-2006-1` 取固定端面不折減（理由：固定端剪力最大、無斜壓桿效應）；
  `RC-2023-3` 取距固定端 d 處（理由：ACI 9.4.3.2 固定端反力向上、端區受壓，條件 (a) 成立）。
  依**規則 2**（verifiedSolution 為最終答案，不可質疑或重算），本次修改**不判定何者為準**，
  改為在 traps 頁與講義中並陳兩者及其理由，並提示作答時須寫出條件判斷過程。
  **此項若要收斂，須由使用者裁示；在裁示前 raw/solutions/ 兩題均維持原狀。**
  **怎麼驗證的：** ① 對照 ACI 318 §9.4.3.2 三條件；② 逐字核對 RC-2020-2、RC-2006-1、RC-2023-3 三份 verified 解答的原文理由；
  ③ 全庫掃描確認無其他檔案重複「倒 T 梁一律不可」的敘述。
  **規則遵循：** `traps/` 非規則 4 例外目錄，但經核對 CLAUDE-CODE.md，COMPILE-ALL 的生成清單僅含
  concepts/ · methods/ · problems/ · index.md · by-year.md（INGEST 僅更新 traps 頁的「出現題目」表格），
  **不會重新生成 traps/ 頁面本體**，故直接修正不會被蓋回。同步更新 `study/lecture-RC-U2-1.html` §4.1。
- 2026-07-26｜FIX（**使用者單次授權修改 raw/solutions/，不含數值**）｜**懸臂梁 d 偏移判準收斂：RC-2006-1 與 RC-2023-3 論證統一為 ACI 318 §9.4.3.2 三條件**
  **背景：** 前一筆紀錄揭露兩份 verified 解答對「懸臂梁能否採 d 偏移」處理相反。經與使用者確認後裁示收斂。
  **授權範圍（使用者明示）：** 僅修改**理由文字**，兩題的**答案與所有數值一律不動** ——
  RC-2006-1 維持 $V_u = 19{,}913$ kgf、$V_s = 16{,}704$ kgf、$s = 13.2$ cm；RC-2023-3 維持 $V_u = 7.425$ tf、$e_{\max} = 10.4$ cm。
  因未更動 verifiedSolution，**規則 2 未被觸及**。
  **錯在哪（僅 RC-2006-1 的論證結構）：** 原文「懸臂梁均布載重的剪力由自由端向固定端遞增，固定端最大，且無斜壓桿效應，故臨界斷面應取在固定端面」——
  ① 「固定端剪力最大」是**事實正確但推論無效**：簡支梁 $V(x)=w(L/2-x)$ 同樣是支承面最大、向內遞減，卻可採 d 偏移；
     d 偏移規定的前提本來就是「支承面剪力最大」，此句無法區分兩者。
  ② 「無斜壓桿效應」是實質論點，但對「與柱／牆同澆、載重在頂面」的懸臂梁站不住腳（頂面載重可沿斜壓桿走到固定端底部的壓力弦，即反力交入柱之處）。
  **改成什麼：**
  ・`raw/solutions/RC-2006-1/`：第 5 節改為 §9.4.3.2 三條件對照表，結論改為「**條件 (a)（支承細節）題目未明示、無法確認 → 保守取固定端面**」；
    加註「勿用錯理由」方塊點出上述 ① 的邏輯瑕疵；並列出若 (a) 成立則 $s = 15.2$ cm（供對照，非答案）。陷阱列與計算段標註同步。
  ・`raw/solutions/RC-2023-3/`：Step 1 與 L3 知識點補上三條件逐一檢核 (a)✓(b)✓(c)✓，並註明「判準是條件不是構件名稱」。
  ・兩題互相加上交叉連結。
  **同步更新：** `wiki/problems/RC-2006-1.md`（ingest 副本敘述）、`study/problems-view/RC-2006-1.html` 與 `RC-2023-3.html`（重新產生）、
  `wiki/traps/SHEAR-CRITICAL-SECTION.md`（懸臂梁段由「兩份解答衝突」改為「條件不同」）、`study/lecture-RC-U2-1.html` §4.1 與 PDF。
  **怎麼驗證的：** ① 條文對照 ACI 318 §9.4.3.2 三條件；② 邏輯反證（簡支梁同為支承面最大卻可折減）；
  ③ 數值重算確認兩題答案未變（13.2 cm、7.425 tf、10.4 cm 皆與原解一致）；④ 全庫掃描確認舊理由字串已無殘留。
  **⚠️ 規則狀態：** 本次修改 `raw/solutions/RC-YYYY-N/` 屬**使用者單次授權**，`CLAUDE.md` 規則 1 **維持原文未擴充例外**（使用者裁示）。
  日後同類勘誤仍須逐次取得授權。

## 2026-08-08 unit-formula-map：RC-U1-1 / RC-U1-2

- 新增 `study/formula-given-RC-U1-1.html` + `.pdf`（30 條公式：必背 24 / 別賭 6 / 通常會給 0）
- 新增 `study/formula-given-RC-U1-2.html` + `.pdf`（30 條公式：必背 24 / 別賭 4 / 通常會給 2）
- 證據來源：`raw/exams/` 民國 91–114 年共 24 份考卷（pdftotext 全年份抽取 + 92 年掃描影像卷逐頁目視判讀）
- 交叉驗證：`verify.py` 卡片 ok 年份 vs 逐年矩陣 ✔，兩份皆「全部一致」
- 兩頁互相加上導覽按鈕；CLAUDE.md / README.md / 檔案架構索引表.md 同步登錄第三種教材型態

## 2026-08-08 unit-formula-map：RC-U2-1 / RC-U3-3 / RC-U4-1

- 新增 `study/formula-given-RC-U2-1.html` + `.pdf`（24 條：必背 20 / 別賭 3 / 通常會給 1）
- 新增 `study/formula-given-RC-U3-3.html` + `.pdf`（27 條：必背 17 / 別賭 4 / 通常會給 6）
- 新增 `study/formula-given-RC-U4-1.html` + `.pdf`（23 條：必背 14 / 別賭 4 / 通常會給 5）
- 92 年掃描影像卷以 200 dpi 重新逐頁目視，確認第一題鋼絞線 σ-ε 曲線、第二題 λd 詳細式、第四題剪力牆門檻／φ=0.6／λdh 的原文內容
- 交叉驗證：`verify.py` 三份皆「全部一致」；抽樣回查 93、102、107、108、112 年考卷原文確認 fps 與橫膈版 Vn 的標記
- `formula-given-RC-U1-1/U1-2` 兩頁 nav 補上指向新三頁的按鈕；U1-2 的 Ash 卡片加註「同一條在 U3-3 列為別賭（98 年說明題沒給）」

## 2026-08-08 unit-exam-intel：RC-U1-1 / RC-U1-2 舊 study 頁重構為命題情報頁

### 重構了什麼、刪了哪些重複區段

- `study/study-RC-U1-1.html`、`study/study-RC-U1-2.html` 由早期「七區段深度複習頁」改寫為
  六區塊命題情報頁（出題概況／考點結構／考點漂移／題型走向／考題清單／命題風險），**檔名不變**
  （`lecture-*`、`formula-given-*` 都連回這兩個檔名，改名要同步三處）。
- 逐區段重疊盤點後的處置：

  | 舊區段 | 重複於 | 處置 |
  |---|---|---|
  | ① 命題分析 | 無 | 保留並擴充成六區塊 |
  | ② 截面圖解 | lecture §2／§4／§5（U1-1）、§2～§5（U1-2） | 刪，改由 nav 連結 |
  | ③ 解題流程圖 | lecture §8（U1-1）、§9（U1-2） | 刪，改由 nav 連結 |
  | ④ 核心公式速查 | formula-given §二（多了逐年考卷給／背證據，是上位版） | 刪，改由按鈕連結 |
  | ⑤ 考題清單 | lecture 精選題章節（無篩選、無渲染頁連結） | 保留並補上副考點與分群篩選 |
  | ⑥ 高頻陷阱 Top 8 | lecture 陷阱總表 | 刪 |
  | ⑦ 互動計算器 | 唯一內容 | **經使用者確認後刪除** |

- 依使用者指示一併處理：移除本次兩頁的 Keynote PDF 按鈕（`RC-U1-n_*.pdf` 仍保留在 `study/`，
  只是不再從這兩頁連出）；`lecture-RC-U1-1.html` 補上缺漏的回連按鈕（命題分析／給背分界／本頁 PDF），
  `lecture-RC-U1-2.html` 的「📊 速查頁」改名為「🔍 命題分析」並以「🎯 給／背分界」取代 Keynote 鍵。
  註：`lecture-RC-U2-1/U3-3/U4-1` 與 `study-RC-U2-1/U3-3/U4-1` 的 Keynote 按鈕**本次未動**（不在本次單元範圍）。

### 過程中修正的資料錯誤

- **`study/problems-view/` 原僅 64／100 頁**，U1-1 的 22 題中有 17 題沒有渲染頁，
  舊 study 頁只好連 `../index.html#md=raw/solutions/...`（瀏覽器拿到未渲染的純文字，公式與附圖全失效）。
  已用 `outputs/build_problems_view.py`（markdown + 離線 KaTeX，與既有頁模板一致）補齊到 **100／100**，
  兩頁題號一律改連 `problems-view/XX-YYYY-N.html` 並 `target="_blank"`。
- **既有 64 頁的返回鍵是 `javascript:history.back()`**，在 `target="_blank"` 開的新分頁按了沒有反應
  （新分頁沒有上一頁歷史）。全部改為「命題分析＋講義」雙鈕靜態連結，並注入「跟隨來源單元」腳本
  （讀 `document.referrer`，來源是 `study-`／`lecture-`／`formula-given-RC-Un-m.html` 時覆寫兩鍵指向來源單元；
  無 JS 或無 referrer 時靜態 href 保底）。
- **`RC-2002-2.html`、`RC-2011-4.html` 兩頁的 `#9`（鋼筋號數）被舊轉檔器誤判為 Markdown 標題**，
  頁面出現 `<h1>9 截面積 = 6.47 cm²…</h1>`。新轉檔器在送進 markdown 前把 `#` + 數字換成佔位字元，
  轉完再還原，兩頁已重生並確認 `<h[1-6]>數字` 的誤判數為 0。
- **舊 study-RC-U1-1 頁的觀察句寫「近 5 年連續出題（2020–2024）」**，但 2025 年考卷四題（RC-2025-1～4）
  無一屬 U1-1，正確描述是「近 6 考年 5／6 年出題，2025 年整年缺席」。新頁 KPI 直接抄 `stats.py`。
- **（僅記錄、未修改）** `raw/solutions/RC-2019-1/RC-2019-1.md` 與 `RC-2019-2/RC-2019-2.md` 的表頭
  主分類寫成 `RC-U1`（缺子項號），正確應為 `RC-U1-1`、`RC-U1-2`。`question_index.json` 的
  `primaryTopicId` 是對的，統計不受影響；因受規則 1、2 保護，個別題目解析未予更動。

### 由統計得出的命題觀察（全部可由 `scripts/stats.py` 複算）

- **RC-U1-1**：主 19／副 3，佔全科 19.0%，全科排名 #1（#2 的 RC-U3-3 為 16 題）；24 考年中 14 年出現，
  空窗年段 2008–2010、2012–2013、2017–2018；近 6 考年 5／6 年共 8 題。
  漂移（前 9 題 2002–2015 → 後 10 題 2016–2024）：雙筋梁 2→3、鋼筋量限制 1→2、單筋矩形梁 2→2、
  T 形梁 3→2、彎矩–曲率韌性 1→1。重心從「認斷面型式」移向「解邊界條件」——後段雙筋梁三題
  （2022-1、2023-2、2024-2）全部是壓力筋**未**降伏，前段 2002-4 則是恰好降伏。
  設計法：19 題全為 USD，本科無 ASD／LRFD 雙軌問題，故改以問法分軸（分析／設計／韌性／鋼筋量上下限）。
- **RC-U1-2**：主 12／副 8，佔全科 12.0%，全科排名 #4（前為 RC-U4-1 13 題、後為 RC-U3-2 7 題）；
  24 考年中 11 年出現，空窗年段 2006–2007、2012–2014、2022–2023；近 6 考年僅 2／6 年共 2 題。
  漂移（前 6 題 2002–2011 → 後 6 題 2011–2024）：互制圖單點求解 2→3、細長柱 1→0，其餘四群持平。
  重心從「建整條 P-M 互制圖」收斂成「解互制圖上的一個點」；細長柱主考點已移交 RC-U1-3
  （2006-2、2016-3 的 primaryTopicId 皆為 U1-3），柱曲率韌性主考點自 2011-3 起空窗 14 年。
  設計法：USD 11 題＋概念題 1 題（2011-1），後段無概念題。
- 兩頁均以 `scripts/verify.py` 對帳通過（題號集合、主／副旗標、designMethod、篩選鈕數字、
  KPI 四項、題號連結存在性、禁用寫法七項全過）。

## 2026-08-08 unit-exam-intel：RC-U2-1 / RC-U3-3 / RC-U4-1 舊 study 頁重構為命題情報頁

### 重構了什麼、刪了哪些重複區段

- `study/study-RC-U2-1.html`、`study-RC-U3-3.html`、`study-RC-U4-1.html` 由早期「七區段深度複習頁」
  改寫為命題情報頁，**檔名不變**。處置沿用 U1-1／U1-2 這一輪已與使用者確認的原則：
  ② 截面／構造圖解 → 刪（重複於 lecture 各章）；③ 解題流程圖 → 刪（lecture §8／§9）；
  ④ 核心公式速查 → 刪（formula-given 是含逐年考卷證據的上位版）；⑥ 高頻陷阱 Top 8 → 刪（lecture 陷阱總表）；
  ⑦ 互動計算器（U2-1 梁剪力檢核／U3-3 柱 Ash 檢核／U4-1 預力兩階段應力）→ **刪**；
  ① 命題分析 → 保留並擴充；⑤ 考題清單 → 保留並補上副考點與分群篩選。
- **U2-1 主考點只有 7 題（< 8），依 skill 規定跳過「考點漂移」區塊**，改在出題概況註腳寫一行趨勢描述，
  並把該位置換成「剪力的角色：主考點 7 題 vs 副考點 9 題」表（依副考點的來源單元分類）。
  故 U2-1 只有五個區塊，nav 也不放漂移連結。
- 三份 `lecture-RC-U2-1/U3-3/U4-1.html` 的 nav：「📊 速查頁」改名「🔍 命題分析」，
  「📄 Keynote」以「🎯 給／背分界」取代。至此 `study/` 底下已無任何 Keynote 按鈕
  （`RC-U2-1_*.pdf` 等檔案仍保留在資料夾內，只是不再從教材頁連出）。

### 過程中發現的資料問題（逐項）

- **`RC-2021-4` 的 `designMethod` 記為「概念題」，但解析內容是 WSD 容許應力計算題**
  （後拉預鑄梁與場鑄板組成 T 型梁，求最大均布活載重，`raw/solutions/RC-2021-4/RC-2021-4.md`
  表頭自己寫的是「WSD 工作應力法（容許應力設計法）」）。
  本頁一律以 `question_index.json` 為準（`verify.py` 會強制比對），因此頁面上 U4-1 的
  「近 6 考年 概念題 1 題」與「後段概念題 1 題」都含這一筆。
  已在 `study-RC-U4-1.html` 的設計法區塊加上 ⚠️ 資料註記。**未逕行修改索引**，待確認後更正並重算。
- **（僅記錄、未修改）** 解析 .md 表頭主分類缺子項號者再添兩例：
  `RC-2019-3.md` 寫 `RC-U3`（應為 `RC-U3-3`）、`RC-2018-4.md` 寫 `RC-U4` 且把 `RC-U4-1` 放在副分類
  （索引記的是 `primaryTopicId = RC-U4-1`，正確）。連同前一批的 `RC-2019-1`、`RC-2019-2`，
  目前已知 4 例。索引皆正確，統計不受影響；因受規則 1、2 保護，個別題目解析未予更動。
- 舊 U2-1／U3-3／U4-1 頁的觀察句未逐句留存比對（舊頁 ① 區已整段重寫），
  但三頁的 KPI 與清單題數本次全部改由 `stats.py` 產生、`verify.py` 對帳。

### 由統計得出的命題觀察（全部可由 `scripts/stats.py` 複算）

- **RC-U2-1（剪力）**：主 7／副 9，佔全科 7.0%，排名 #6；24 考年只出現 7 年，
  **且沒有任何一年出過兩題**（2006、2009、2010、2014、2017、2020、2023 各一題），空窗年段多達七段。
  7 題主考點全為 USD。**副考點 9 題比主考點還多**，來源為 U3-3 ×5、U2-2 ×2、U1-1 ×1、U4-4 ×1
  ——剪力在本科主要是「當配角」，最大入口是耐震剪力鏈（M_pr → V_e → V_c=0 → 密箍）。
  7 題主考點沒有一題是單純配箍筋，每題都另綁一個判斷（軸力修正／STM／介面剪力／倒 T 的 d 偏移／扭力門檻）。
- **RC-U3-3（韌性與耐震）**：主 16／副 2，佔 16.0%，排名 #2；24 考年中 12 年出現，
  空窗年段 2006–2008、2014–2015、2020–2021、2023–2024。出題高度成組：2012 年一年考 3 題
  （2012-2 梁 → 2012-3 柱 → 2012-4 接頭，同一構架連環題），2003、2004 各 2 題。
  漂移（前 8 題 2003–2012 → 後 8 題 2012–2025）：耐震梁 1→2、韌性觀念與細則 2→1，
  柱圍束／接頭／牆體各持平。重心從「背耐震構造規定」移向「走完能力設計法的因果鏈」
  ——後段 8 題有 6 題要先反推一個設計力才能開始算。
  設計法：USD 12＋概念題 4；**概念題比例 25%（4／16）為全科 13 個單元最高**
  （第二名 RC-U4-3 為 1／5＝20%，RC-U1-1 為 0%），此數字由索引全表統計得出。
  柱圍束 A_sh 是本單元最高頻標籤（×3）卻自 2013-2 起空窗 12 年，是本頁風險排序第一名。
- **RC-U4-1（預力斷面應力）**：主 13／副 8，佔 13.0%，排名 #3；24 考年中 13 年出現，
  空窗年段僅 2015–2017、2019–2020、2024–2025 三段，是全科最規律的單元之一；
  **清單 21 題有 19 題是考卷的第 4 或第 5 題（其中 17 題正好是第 4 題）**。
  漂移（前 6 題 2003–2009 → 後 7 題 2011–2023）：組合斷面疊加 3→1、彈性應力與使用性 1→3、
  開裂彎矩與極限強度 2→3。重心從「把組合斷面應力疊起來」移向「選對斷面、階段與 f_ps 公式」。
  設計法：**WSD 7＋混合 4＋USD 1＋概念題 1**，是全科唯一必須準備兩套設計法的單元；
  全科 100 題裡 WSD 共 16 題，**16 題全部落在 U4 單元群**（U4-1 七、U4-2 五、U4-3 四），
  U1／U2／U3 一題都沒有；U4-1 的 8 題副考點在索引中亦全為 WSD。
- 三頁均以 `scripts/verify.py` 對帳通過；另以獨立腳本重算漂移對切、設計法分布、近 6 考年、
  副考點來源與分群唯一性，與頁面手寫表格逐格相符。

## 2026-08-20 subject-frequency-map：產出 RC 全科出題頻率熱圖 `study/frequency-RC.html`

### 產了什麼

- `study/frequency-RC.html`（單一自包含 HTML，無外部相依，25,319 字元），由
  `subject-frequency-map/scripts/build_frequency.py` 從 `raw/json/question_index.json` ＋
  `raw/json/syllabus_taxonomy.json` 產生，更新日期標記 2026-08-20。
- 頁面內容：可切換「只看主考點／主＋副考點」的 14 子項 × 24 考年熱圖、排名總表
  （主／副題數、佔全科、出現年數、最長空窗含年段、最後出現、近 6 考年、常見題號位置、現有教材）、
  各單元權重表、五種情境的讀書順序建議。
- 排名表教材欄由腳本掃描 `study/` 自動產生，本次偵測到 20 個綠色可點標籤
  ＝ RC-U1-1、U1-2、U2-1、U3-3、U4-1 五個子項各有四種教材（命題分析／講義／給背分界／記憶片）齊全；
  其餘 9 個出現過的子項四欄皆灰色（尚未製作）。
- **對帳全過**：熱圖主考點格子總和 ＝ 題庫總題數 100、每列總和 ＝ 該子項主考點題數、
  單元小計加總相符；無孤兒 `primaryTopicId`（索引與 taxonomy 的子項代碼完全對得起來），頁面未出現紅色警告框。
- 目視 QA：headless Chromium 開啟，console 乾淨無錯誤；兩個模式各重畫一次皆正常
  （主考點模式 42 顆橘點，切到主＋副後歸零並改為併入格值）；tooltip 題號格式正確
  （例：`2005：RC-2005-2、(副)RC-2005-3`）。

### 由這張表得到的命題觀察（全部由 `build_frequency.py` 算出，未手打）

- **規模**：24 考年（2002–2025）、100 題、14 個子項，其中 13 個曾當過主考點。每年題數不一致，
  故熱圖各欄總和 ＝ 該年題數。熱圖色階上限為 3（主考點與主＋副兩個模式皆同，`maxP = maxA = 3`）。
- **單元權重**：RC-U1 33 題（33.0%）＞ RC-U3 29 題（29.0%）＞ RC-U4 24 題（24.0%）＞
  RC-U2 14 題（14.0%）。最重的 U1 是最輕的 U2 的 **2.4 倍**。
- **前五名**：U1-1 梁彎矩 19、U3-3 韌性與耐震 16、U4-1 預力斷面應力 13、U1-2 柱強度 12、
  U3-2 樓版與基腳 7，**合計 67 題、佔全科 67.0%**——五個子項吃掉三分之二的題數。
  其中 U1-1、U3-3、U4-1、U1-2 四個已有完整四種教材。
- **工具型子項只有一個**：全科唯一副考點多於主考點的是 **U2-1 剪力（主 7／副 9）**。
  這與 SM 那種「一半以上子項都是工具型」的結構不同：RC 的副考點分布相對集中，
  切到「主＋副」模式後只有 U2-1 這一列明顯變深。
- **0 題子項**：**U1-4 柱設計圖之應用**，24 個考年 0 題——命題大綱有列，考卷上從沒以它為主考點出現過，
  可以直接跳過（排名表以粉紅底標示）。
- **最長空窗**：U2-3 鋼筋錨定長度與斷點計算 **22 年**（2004–2025 空窗，最後出現 2003）、
  U4-4 預力梁剪力 **20 年**（2002–2021 空窗，2022 回歸一次）、U4-3 預力損失 **10 年**（2006–2015）。
  U3-1 梁工作性要求（含撓度、裂縫）主考點 6 題但已 8 年空窗（2010–2017），最後出現 2018。
- **近 6 考年（2020–2025）共 24 題**，集中在少數幾列。
- 本頁只用於**分配時間**，不作押題；押題請看各子項 `study-RC-Un-m.html` 的「命題風險排序」。

## 2026-08-20 struct-diagram 圖解整併 RC-2015-1；發現並修正 index.html 的 KaTeX 版本問題

### 一、RC-2015-1 向量圖解整併

- `raw/solutions/RC-2015-1/files/` 內 struct-diagram 的產出整併回正本：新建 `figs/` 子資料夾，
  收入 4 組 SVG＋2× PNG 與生成腳本 `gen_RC-2015-1.py`（可重跑）。
  `files/` 殘留的已合併 md 與 `.patch` 移至 `files/_to_delete/`（device_bash 不能刪檔，待人工清除）。
- 驗證後才套用：把 `RC-2015-1-figs.patch` 套到整併前的正本，結果與 `files/RC-2015-1.md`
  **逐字元相同**，確認 patch 內容無夾帶未預期改動後才寫入。行尾維持 CRLF。
- §1 依使用者決定改為**考卷原圖與向量重繪並列**（圖 1a／圖 1b），不以重繪取代截圖。
- **數值修正（隨 patch 一併帶入，原值為四捨五入累積誤差）：**
  $C'_s$ 127,126 → **127,112** kgf；$P_{n,b}$ 430,686 → **430,672** kgf；
  $M_{n,\max}$ 13,585,411 → **13,585,103** kgf·cm；$\varphi M_{n,\max}$ 88.98 → **88.97** tf·m；
  $\varphi P_{n,\max}$ 689,134 → **689,117** kgf。四捨五入後的結論值（135.85 tf·m、89.0 tf·m）不變。
- **新增三節進階討論：** 純彎矩點補算（$c=8.60$ cm，$M_n=65.79$ tf·m，$\varphi M_n=59.21$ tf·m）；
  $\varphi M_n$ 峰值不在平衡點（右移至 $\varepsilon_t=0.005$、$c=19.50$ cm，達 **104.08 tf·m**）；
  原文「純彎矩（0, ~tf·m）」的空缺補為 59.2。
- **下游同步三處：** `wiki/problems/RC-2015-1.md`（圖形區＋解題關鍵步驟數字＋兩條進階結論）、
  `study/problems-view/RC-2015-1.html`（**由新正本完整重新渲染**，非手改）。
  渲染器設定先以整併前的正本反推驗證：python-markdown `['tables','nl2br','fenced_code']`
  ＋ 數學式遮罩／清單前補空行／圖片路徑補前綴三道處理，產出與現有 HTML 逐字元相同後才用於新版。
- `CLAUDE-SPEC.md` 新增 **§5.1 向量圖解（`figs/`）規範**：命名、SVG/PNG 成對、腳本可重跑、
  與考卷原圖並存、數值以腳本為準並同步三處；§3 允許檔案類型表與目錄同步加列。
- 驗證：15 個圖片相對路徑全部存在；舊數值全庫零殘留；四檔 CRLF 未破壞；圖 3／圖 4 目視確認數值一致。

### 二、KaTeX 版本問題（既有，非本次造成）

- 現象：`\text{}` 內的 `·`（U+00B7）被 KaTeX 轉為 `\cdotp`，而該指令在舊版**僅限數學模式**，
  於文字模式成為未定義指令。此寫法全庫 **391 處、散在 136 個檔案**（`tf·m`、`kgf·cm` 等單位）。
- 實測版本界線：**KaTeX ≤ 0.16.9 失敗，≥ 0.17.0 正常**（0.13.24／0.15.6／0.16.4／0.16.9／0.16.11
  全部失敗；0.17.0／0.18.0／0.18.1 全部正常）。以 `markdown.math.macros` 把 `\cdotp` 映射成 `\cdot`
  的偏方**實測無效**，因報錯發生在巨集展開之前。
- 影響分流：`study/assets/katex/` 是 **0.18.1**，故 `study/` 底下 11 個頁面（含 problems-view）**渲染正常**；
  **`index.html` 從 CDN 載入 `katex@0.16.11`**，落在失敗區間，且因 `throwOnError:false` 不跳錯，
  而是靜默印出字面的 `kgf\cdotpcm`、`tf\cdotpm`——主儀表板的 md 預覽長期渲染錯誤而未被察覺。
- **修正：** `index.html` 的 KaTeX 來源由 CDN 改為本機副本 `study/assets/katex/`（0.18.1），
  與 `study/` 各頁同一份；離線亦可正常渲染（原本離線是降級為不渲染），並在該段加註「不可退回 0.16.x」的原因。
  `mathHint` 提示文字同步改為「找不到 study/assets/katex/」。
- 未處理：VS Code 內建 Markdown 預覽自帶舊版 KaTeX，仍會對 `·` 報 ParseError。
  依使用者決定不處理——校稿一律以 `study/problems-view/` 與儀表板為準，VS Code 預覽僅作純文字編輯用。

### 三、既有問題（本次未動，供日後處理）

- 全庫工作目錄為 CRLF、git 內儲存為 LF，`.gitattributes` 未設 `text=auto eol=lf`，
  導致 `git status` 幾乎每個檔案都顯示 modified、diff 全檔翻紅（未經修改的 `RC-2002-1.md`
  亦顯示 410 行全異動）。檢視實際改動須用 `git diff --ignore-cr-at-eol`；
  本次真正改動為 4 檔 160 增 27 刪。修正需一次全庫規模的 commit，留待使用者決定。

## 2026-08-20（補正）KaTeX `·` 問題：巨集偏方其實有效，前一則紀錄的判斷有誤

> 本則更正同日前一則「二、KaTeX 版本問題」中「以 `markdown.math.macros` 把 `\cdotp`
> 映射成 `\cdot` 的偏方**實測無效**」的結論。該結論的**現象描述正確、歸因錯誤**：
> 巨集其實有生效，錯的是映射目標。依規則 3 不刪改既有紀錄，於此補正。

- 重測發現：套用 `macros {"\cdotp":"\cdot"}` 後，錯誤訊息由
  `Undefined control sequence: \cdotp` 變成 `Undefined control sequence: \cdot`
  ——**代表巨集確實展開了**，只是 `\cdot` 與 `\cdotp` 同為數學模式專用指令，
  在 `\text{}` 內一樣未定義，所以照樣失敗。前一則誤判為「報錯發生在巨集展開之前」。
- **可行解：把 `·` 直接映射到 Unicode `⋅`（U+22C5 DOT OPERATOR）**，即
  `"markdown.math.macros": { "·": "⋅" }`。實測：
  - KaTeX 0.16.11（VS Code 內建同級）：全部通過，輸出 `kgf⋅cm`、`tf⋅m（標稱最大彎矩）`，
    與 KaTeX 0.18.1 的**原生輸出逐字相同**。
  - KaTeX 0.18.1（本庫 `study/assets/katex/`）：同樣通過，故日後升級不會反噬。
  - 數學模式中原本就正常的 `·`（如 `5 · 3`）不受影響；表格內 `M_n (tf·m)`、
    `kN·m`、`N·mm` 一併正常。
- 其他候選皆不可用：`\textperiodcentered`、`\textbullet` 在 KaTeX 0.16.x 未定義；
  `\char"00B7` 渲染出錯字；`\raisebox{0.25em}{.}` 變成句點；映射回 `·` 本身會無限展開。
- 已產出 `.vscode/settings.json`（含完整原因註解，另關閉中文庫必然觸發的
  非 ASCII 高亮橫幅）。**該檔無法由 Cowork 寫入**——遠端工具禁止寫 `.vscode`，
  須由使用者自行建立或貼入使用者設定。
- 影響範圍不變：此為 VS Code 預覽端的修法，不動 `raw/` 任何檔案，
  `index.html` 改用本機 0.18.1 的修正仍然必要且已完成。
