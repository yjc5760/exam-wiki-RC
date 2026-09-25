const pptxgen = require("pptxgenjs");
const fs = require("fs");
const N = JSON.parse(fs.readFileSync("nums.json", "utf8"));
const MJ = JSON.parse(fs.readFileSync("figs/math.json", "utf8"));
const pres = new pptxgen(); pres.layout = "LAYOUT_WIDE"; pres.title = "RC-U2-1 拼圖一：剪力破壞的底層邏輯";
const FT = "Noto Sans CJK TC";
const C = { ink: "1F2A37", muted: "6B7280", panel: "F4F6F9", line: "D5DAE1", eff: "E4572E", tot: "2F54C8", le: "6D4BC2",
            ps: "C0392B", ok: "2E7D6B", dark: "1B2432", white: "FFFFFF", gold: "B7791F",
            effbg: "FDEDE8", totbg: "EEF2FB", psbg: "FBECEA", okbg: "E6F2EF", lebg: "F1EDFA", goldbg: "FBF3E4" };
const f1 = v => (v + 1e-9).toFixed(1), f2 = v => (v + 1e-9).toFixed(2), f3 = v => (v + 1e-9).toFixed(3), f4 = v => (v + 1e-9).toFixed(4);
const f0 = v => Math.round(v).toString();
const sg = v => (v < 0 ? "−" + f0(-v) : "+" + f0(v));

function runs(str, o = {}) {
  const out = []; const re = /(_\{[^}]*\}|_.)/g; let last = 0, m;
  str = str.replace(/'/g, "′");
  while ((m = re.exec(str))) {
    if (m.index > last) out.push({ text: str.slice(last, m.index), options: { ...o } });
    const t = m[0].startsWith("_{") ? m[0].slice(2, -1) : m[0].slice(1);
    out.push({ text: t, options: { ...o, subscript: true } }); last = re.lastIndex;
  }
  if (last < str.length) out.push({ text: str.slice(last), options: { ...o } });
  return out;
}
function paras(list) {
  const out = [];
  list.forEach((p, i) => {
    const r = runs(p.t, p.o || {});
    if (i < list.length - 1) r[r.length - 1].options.breakLine = true;
    out.push(...r);
  });
  return out;
}
function T(s, content, x, y, w, h, o = {}) {
  const base = { fontFace: FT, fontSize: 15, color: C.ink, valign: "top", margin: 0, isTextBox: true };
  const opts = { ...base, ...o, x, y, w, h };
  const body = typeof content === "string" ? runs(content, { bold: o.bold, color: o.color || C.ink, fontSize: o.fontSize || 15 }) : content;
  s.addText(body, opts);
}
function vb(file) {
  const t = fs.readFileSync(file, "utf8"); const m = t.match(/viewBox="([\d.\s-]+)"/);
  const a = m[1].trim().split(/\s+/).map(Number); return [a[2], a[3]];
}
function img(s, name, x, y, W, H, align = "center") {
  const f = `figs/${name}.svg`; let w, h;
  if (MJ[name]) [w, h] = MJ[name]; else [w, h] = vb(f);
  const k = Math.min(W / w, H / h); const iw = w * k, ih = h * k;
  const ix = align === "left" ? x : x + (W - iw) / 2;
  s.addImage({ path: f, x: ix, y: y + (H - ih) / 2, w: iw, h: ih, altText: name });
  return { x: ix, y: y + (H - ih) / 2, w: iw, h: ih };
}
function eq(s, name, x, y, H, scale = 0.72, align = "left", maxW = 99) {
  const [w, h] = MJ[name]; let iw = w * scale, ih = h * scale;
  if (ih > H) { iw *= H / ih; ih = H; }
  if (iw > maxW) { ih *= maxW / iw; iw = maxW; }
  const ix = align === "center" ? x - iw / 2 : x;
  s.addImage({ path: `figs/${name}.svg`, x: ix, y: y + (H - ih) / 2, w: iw, h: ih, altText: name });
  return iw;
}
function header(s, eyebrow, title, col = C.eff) {
  T(s, eyebrow, 0.6, 0.38, 11, 0.3, { fontSize: 12, bold: true, color: col, charSpacing: 2 });
  T(s, title, 0.6, 0.68, 12.2, 0.6, { fontSize: 26, bold: true });
}
function panel(s, x, y, w, h, fill = C.panel, line = C.line) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill: { color: fill }, line: { color: line, width: 1 }, rectRadius: 0.12 });
}
function bar(s, x, y, h, col) { s.addShape(pres.shapes.RECTANGLE, { x, y, w: 0.08, h, fill: { color: col }, line: { color: col } }); }
function pageNo(s, n) { T(s, `${n}`, 12.3, 7.08, 0.5, 0.25, { fontSize: 10, color: "9AA3AE", align: "right" }); }
Object.assign(C, { uu: "C0392B", cu: "E07B39", cd: "2E7D6B", uubg: "FBECEA", cubg: "FDF1E7", cdbg: "E6F2EF", pur: "6D4BC2", purbg: "F1EDFA", water: "2C6E9E" });
let pg = 1;
function newSlide() { const s = pres.addSlide(); s.background = { color: C.white }; pg++; return s; }
// 圖＋底部 1～3 格說明
function figSlide(eyebrow, title, fig, cells, col = C.eff, figH = 4.45) {
  const s = newSlide();
  header(s, eyebrow, title, col);
  img(s, fig, 0.6, 1.4, 12.1, figH);
  const n = cells.length, gap = 0.15, w = (12.1 - gap * (n - 1)) / n, y = 1.5 + figH, h = 7.05 - y;
  cells.forEach(([hd, body, c, bg, ln], i) => {
    const x = 0.6 + i * (w + gap);
    panel(s, x, y, w, h, bg || C.panel, ln || C.line);
    T(s, paras([{ t: hd, o: { bold: true, fontSize: 14, color: c || C.ink } }, ...body.map(t => ({ t, o: { fontSize: 13 } }))]),
      x + 0.2, y + 0.08, w - 0.35, h - 0.12, { paraSpaceAfter: 2 });
  });
  pageNo(s, pg);
  return s;
}


// 公式面板：標題＋一條公式
function eqPanel(s, x, y, w, h, title, name, col, bg, ln, note) {
  panel(s, x, y, w, h, bg || C.panel, ln || C.line);
  T(s, title, x + 0.2, y + 0.1, w - 0.4, 0.32, { fontSize: 14, bold: true, color: col || C.ink });
  const eh = note ? h - 0.95 : h - 0.55;
  eq(s, name, x + 0.2, y + 0.45, eh, 0.6, "left", w - 0.4);
  if (note) T(s, note, x + 0.2, y + h - 0.42, w - 0.4, 0.34, { fontSize: 12, color: C.muted });
}
const n2 = v => f2(v);
Object.assign(C, { pur: "6D4BC2", purbg: "F1EDFA", blue: "2F54C8", bluebg: "EEF2FB", org: "D9661F" });
const f2n = k => f2(N[k]);
const PU = [C.le, C.lebg, "C9BCEB"], RD = [C.ps, C.psbg, "EBB4AE"], BL = [C.tot, C.totbg, "B9C6EA"],
      GD = [C.gold, C.goldbg, "E6CFA0"], GN = [C.ok, C.okbg, "9CC7BC"];
const cell = (hd, body, P) => [hd, body, P ? P[0] : C.ink, P ? P[1] : null, P ? P[2] : null];
// ───── 1 封面 ─────
{
  const s = pres.addSlide(); s.background = { color: C.dark };
  T(s, "RC-U2-1　RC 剪力強度分析與設計｜觀念講義・拼圖一", 0.8, 1.2, 11.5, 0.4, { fontSize: 16, color: "9FB3C8", bold: true });
  T(s, "剪力破壞的底層邏輯", 0.8, 1.8, 11.8, 1.0, { fontSize: 46, bold: true, color: C.white });
  T(s, "混凝土沒有「抗剪強度」這回事——剪應力在 45° 方向變成主拉應力，把混凝土拉裂", 0.8, 2.95, 11.8, 0.9, { fontSize: 21, color: "D6DEE8" });
  const dots = [["τ", "剪應力", "A58BE6"], ["σ₁", "45° 主拉 = τ", "F08A7E"], ["f_t", "超過就裂", "F2A65A"], ["V_c", "∝ √f′c", "7FC8B4"]];
  dots.forEach(([n, lab, col], i) => {
    const x = 0.8 + i * 3.0;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 4.3, w: 2.75, h: 0.85, fill: { color: "243044" }, line: { color: col, width: 2 }, rectRadius: 0.1 });
    T(s, runs(n, { bold: true, color: col, fontSize: 22 }), x + 0.15, 4.3, 0.9, 0.85, { valign: "middle" });
    T(s, runs(lab, { color: C.white, bold: true, fontSize: 15 }), x + 1.0, 4.3, 1.7, 0.85, { valign: "middle" });
  });
  T(s, `示範梁：b_w = 30、h = 60、d = 50 cm，f′c = 280、f_y = 4200 kgf/cm²；圖上數字全部由同一支程式算出，可逐一對帳`,
    0.8, 6.3, 11.8, 0.4, { fontSize: 14, color: "9FB3C8" });
}
// ───── 2 總覽 ─────
figSlide("TOPIC MAP · 一句話貫通", "記住一句話，本單元四大公式一口氣推出來", "fig01_map", [
  cell("讀題時先問自己", ["這題的 V_c 是在講「開裂那一刻的抗拉」，還是 V_s「裂後數箍筋」，還是上限「斜壓桿別壓碎」？"], null),
], C.le, 4.4);
// ───── 3 純剪 ─────
figSlide("底層物理 ① · 從梁到微元素", "中性軸處是純剪；轉 45°，它就是一拉一壓", "fig02_element", [
  cell("為什麼挑中性軸", ["τ = VQ/Ib 在中性軸最大，而該處彎曲應力 σ_x = 0：最乾淨的純剪狀態"], PU),
  cell("剪力不會壓碎混凝土", ["它換個方向就是等量的拉應力；壓的那一側（抗壓 280）根本不是問題"], RD),
], C.le);
// ───── 4 莫爾圓 ─────
{
  const s = figSlide("底層物理 ② · 純剪莫爾圓", "圓心在原點，半徑 = τ：主拉與主壓等值，方向差 45°", "fig03_mohr", [], C.le, 4.3);
  eqPanel(s, 0.6, 5.85, 6.6, 1.2, "主應力通式", "m_mohr", C.ink);
  eqPanel(s, 7.35, 5.85, 5.35, 1.2, "代入純剪", "m_ps", ...RD);
}
// ───── 5 裂縫 ─────
figSlide("底層物理 ③ · 裂縫長什麼樣", "裂縫垂直主拉方向：支承附近斜 45°，跨中垂直", "fig04_cracks", [
  cell("腹剪裂縫", ["腹板中段先裂，典型出現在短剪跨、薄腹板（如 I 形、預力梁）"], RD),
  cell("撓剪裂縫", ["先有撓曲垂直裂縫，再往上彎成斜裂縫：一般 RC 梁最常見的形式"], GD),
], C.ps, 4.45);
// ───── 6 強度 ─────
figSlide("底層物理 ④ · 怕拉不怕壓", `抗拉只有抗壓的 ${f1(N.FT_R)}%，規範開裂剪應力只用 ${f1(N.VCS_R)}%`, "fig05_strength", [
  cell("所以題目說「剪力破壞」", ["請在心裡翻譯成「斜向拉力破壞」：比的是 f_t，不是 f′c"], RD),
  cell("0.53 為什麼是 1.06 的一半", ["V/(b_w d) 是名目平均值，撓剪交互作用讓裂縫更早出現；規範取試驗資料的下限"], GN),
], C.org);
// ───── 7 公式 ① ─────
{
  const s = newSlide();
  header(s, "公式 ① · V_c 基本式從哪來", "f_t ∝ √f′c → V_c ∝ √f′c", C.ok);
  eqPanel(s, 0.6, 1.5, 6.0, 1.45, "① 抗拉強度的經驗式（直接抗拉）", "m_ft", ...GD, "材料試驗：f_t 正比於 √f′c，不是 f′c 一次方");
  eqPanel(s, 6.75, 1.5, 5.95, 1.45, "② 規範開裂剪力（kgf、cm 制）", "m_vc", ...GN, "b_w d：腹板寬 × 有效深度");
  eqPanel(s, 0.6, 3.15, 6.0, 1.45, "③ 名目剪應力 ≈ 抗拉的一半", "m_half", ...PU, "試驗下限 → 偏保守");
  eqPanel(s, 6.75, 3.15, 5.95, 1.45, "④ 示範梁", "m_vcd", ...BL, "後面每一頁的 V_c 都從這個 13.30 出發");
  panel(s, 0.6, 4.8, 12.1, 2.25, C.dark, C.dark);
  T(s, paras([
    { t: "物理連結", o: { bold: true, fontSize: 17, color: "F2A65A" } },
    { t: "剪應力在 45° 方向製造 σ_1 = τ → 要擋住的是「拉」 → 抗拉強度跟 √f′c 走 → 所以 V_c 公式裡是 √f′c", o: { fontSize: 16, color: C.white } },
    { t: "考場提醒：√f′c 的單位是 kgf/cm²，代 f′c = 280 得 16.733；SI 制係數不同（0.17√f′c，MPa），別混用", o: { fontSize: 14, color: "D6DEE8" } },
  ]), 0.9, 4.95, 11.5, 2.0, { paraSpaceAfter: 8 });
  pageNo(s, pg);
}
// ───── 8 √ ─────
figSlide("推論 ① · 開根號的代價", "f′c 翻倍，V_c 只多 41%；斷面翻倍，V_c 直接翻倍", "fig06_sqrt", [
  cell("解題啟示", ["題目問「如何提高剪力強度」：加大 b_w 或 d 最有效，其次加箍筋；提高 f′c 效益最低"], GN),
  cell("附帶效應", ["加大 d 同時提高 V_s（= A_v f_{yt} d/s）與上限 2.12√f′c b_w d，一石三鳥"], PU),
], C.ok);
// ───── 9 軸力莫爾圓 ─────
{
  const s = figSlide("推論 ② · 軸力讓莫爾圓平移", "拉為正時：軸壓把圓往左推、軸拉把圓往右推", "fig07_axial_mohr", [], C.tot, 4.3);
  eqPanel(s, 0.6, 5.85, 5.2, 1.2, "中性軸處（σ = N/A_g，τ 不變）", "m_axial", C.ink);
  panel(s, 5.95, 5.85, 6.75, 1.2, C.goldbg, "E6CFA0");
  T(s, paras([
    { t: "方向別記反", o: { bold: true, fontSize: 14, color: C.gold } },
    { t: "以「拉為正」畫圖時，軸壓讓圓心移到負側（左）；若你的教材以壓為正，左右會對調——看的是 σ_1 變大還是變小", o: { fontSize: 13 } },
  ]), 6.15, 5.93, 6.4, 1.05, { paraSpaceAfter: 3 });
}
// ───── 10 軸力倍率 ─────
{
  const s = figSlide("推論 ② · 規範的軸力修正", "同樣大小的軸力，拉力的殺傷力是壓力幫助的 4 倍", "fig08_axial_factor", [], C.tot, 4.3);
  eqPanel(s, 0.6, 5.85, 6.0, 1.2, "軸壓（N_u 代正值）", "m_comp", ...BL);
  eqPanel(s, 6.75, 5.85, 5.95, 1.2, "軸拉（N_u 代負值，算出負值取 0）", "m_ten", ...RD);
}
// ───── 11 V_c 來源 ─────
figSlide("推論 ③ 前置 · V_c 到底是誰在撐", "斜裂縫出現後，混凝土還有四條傳剪路徑", "fig09_sources", [
  cell("規範不分項計算", ["四項難以分開量測，試驗把它們打包成 0.53√f′c b_w d 一條式"], GN),
], C.ok, 4.85);
// ───── 12 塑鉸 ─────
{
  const s = figSlide("推論 ③ · 耐震塑鉸區 V_c = 0", "反覆載重把四個來源一起磨掉：保守地整個不算", "fig10_hinge", [], C.ps, 4.3);
  eqPanel(s, 0.6, 5.85, 6.4, 1.2, "兩條件同時成立才令 V_c = 0", "m_hinge", ...RD);
  panel(s, 7.15, 5.85, 5.55, 1.2, C.panel);
  T(s, paras([
    { t: "V_E：地震引致之剪力；P_u：含地震的設計軸壓力", o: { fontSize: 13 } },
    { t: "範圍：梁自柱面起 2h（柱為 l_o 範圍）", o: { fontSize: 13 } },
    { t: "題目只說「塑鉸區」時，先檢查這兩個條件", o: { fontSize: 13, bold: true, color: C.ps } },
  ]), 7.35, 5.93, 5.2, 1.05, { paraSpaceAfter: 3 });
}
// ───── 13 V_s ─────
{
  const s = figSlide("推論 ④ · V_s 是數箍筋", "一條 45° 裂縫水平跨 d，間距 s → 穿過 d/s 支箍筋", "fig11_vs", [], C.ok, 4.3);
  eqPanel(s, 0.6, 5.85, 5.0, 1.2, "箍筋貢獻", "m_vs", ...GN);
  panel(s, 5.75, 5.85, 6.95, 1.2, C.panel);
  T(s, paras([
    { t: "兩個假設", o: { bold: true, fontSize: 14 } },
    { t: "裂縫角 45°（水平投影 = d）；穿越裂縫的箍筋全部降伏（f_{yt}）", o: { fontSize: 13 } },
    { t: `示範：D13 雙肢、s = 15 → V_s = ${f2n("VS15")} tf`, o: { fontSize: 13, bold: true, color: C.ok } },
  ]), 5.95, 5.93, 6.6, 1.05, { paraSpaceAfter: 3 });
}
// ───── 14 上限 ─────
{
  const s = figSlide("推論 ④ · 上限天花板", "箍筋加太多，斜壓桿會先壓碎：這是「抗壓的故事」", "fig12_limit", [], C.ps, 4.3);
  eqPanel(s, 0.6, 5.85, 6.4, 1.2, "V_s 上限", "m_vsmax", ...PU);
  eqPanel(s, 7.15, 5.85, 5.55, 1.2, "等價的設計剪力上限", "m_vumax", ...RD);
}
// ───── 15 公式 ② ─────
{
  const s = newSlide();
  header(s, "公式 ② · 把分工寫成設計式", "V_c 抗拉、V_s 縫裂、上限防壓碎、s_{max} 保證穿到", C.ok);
  eqPanel(s, 0.6, 1.5, 6.0, 1.45, "① 強度需求", "m_vu", ...GN, "φ = 0.75（剪力）");
  eqPanel(s, 6.75, 1.5, 5.95, 1.45, "② 箍筋貢獻", "m_vs", ...PU, "數出來的：n = d/s 支 × A_v f_{yt}");
  eqPanel(s, 0.6, 3.15, 6.0, 1.45, "③ 斜壓桿上限", "m_vsmax", ...RD, "超過 → 加大斷面，不是加箍筋");
  eqPanel(s, 6.75, 3.15, 5.95, 1.45, "④ 間距上限", "m_smax", ...GD, "另有 60 cm／30 cm 絕對上限");
  const rows = [["V_c", "開裂瞬間混凝土抗拉", "√f′c、軸力、塑鉸", C.ok], ["V_s", "開裂後箍筋縫住裂縫", "A_v、f_{yt}、d/s", C.le], ["上限", "斜壓桿不可先壓碎", "2.12√f′c b_w d", C.ps]];
  rows.forEach(([a, b, c, col], i) => {
    const x = 0.6 + i * 4.07;
    panel(s, x, 4.8, 3.95, 2.25, C.white, col);
    T(s, a, x + 0.25, 4.95, 3.5, 0.5, { fontSize: 22, bold: true, color: col });
    T(s, b, x + 0.25, 5.55, 3.5, 0.5, { fontSize: 16, bold: true });
    T(s, runs("看的參數：" + c, { fontSize: 14, color: C.muted }), x + 0.25, 6.15, 3.5, 0.7);
  });
  pageNo(s, pg);
}
// ───── 16 精算式 ─────
{
  const s = figSlide("V_c 的第二張臉 · 精算式", "縱筋多、剪力相對彎矩大 → 可以多算一點 V_c", "fig15_detail", [], C.gold, 4.3);
  eqPanel(s, 0.6, 5.85, 7.6, 1.2, "精算式（V_u d/M_u ≤ 1.0）", "m_det", ...GD);
  eqPanel(s, 8.35, 5.85, 4.35, 1.2, "示範梁（kgf ÷ 1000 → tf）", "m_detd", ...PU);
}
// ───── 17 四張臉 ─────
figSlide("考場選式 · V_c 的四張臉", "由上而下三個問題，決定用哪一條 V_c", "fig13_flow", [
  cell("判斷順序有道理", ["塑鉸（直接歸零）最優先；軸力改變主拉應力其次；最後才看要不要精算"], null),
], C.le, 4.85);
// ───── 18 示範梁對照 ─────
figSlide("示範梁 · 同一根梁的五個 V_c", "條件一變，V_c 可以差到 0 ～ 18.58 tf", "fig14_faces", [
  cell("軸拉 30 tf", [`V_c 從 ${f2n("VC0")} 砍到 ${f2n("VC_T30")}：少掉 ${f1(N.LOSS30)}%`], RD),
  cell("軸壓 100 tf", [`V_c 增為 ${f2n("VC_C100")}：+${f1((N.F_C100 - 1) * 100)}%`], BL),
  cell("精算式", [`${f2n("VC_DET")}（+${f1((N.VC_DET / N.VC0 - 1) * 100)}%），上限 ${f2n("VC_DET_CAP")}`], GD),
], C.le, 4.2);
// ───── 19 分區 ─────
figSlide("串起來 · V_u 落在哪一區", "先算 φV_c，V_u 在數線上的位置就決定了箍筋怎麼配", "fig16_zones", [
  cell("示範梁 V_u = 40 tf 的四步", [`① φV_c = ${f2n("PVC")} ② V_{s,req} = ${f2n("VS_REQ")} ≤ ${f2n("VS_MAX")} ✓ ③ > ${f2n("VS_HALF")} → s ≤ d/4 ④ s = ${f1(N.S_USE)}，φV_n = ${f2n("PVN")} ≥ 40 ✓`], GN),
], C.ok, 4.6);
// ───── 20 速查表 ─────
{
  const s = newSlide();
  header(s, "考場速查 · 讀題 → 選式", "看到關鍵字，直接鎖定 V_c 的那一張臉", C.le);
  const H = (t) => ({ text: runs(t, { bold: true, color: C.white, fontSize: 14, fontFace: FT }), options: { bold: true, color: C.white, fill: { color: C.dark }, fontSize: 14, fontFace: FT } });
  const R = (a, b, c, col) => [
    { text: runs(a, { bold: true, color: col, fontSize: 15, fontFace: FT }), options: {} },
    { text: runs(b, { fontSize: 15, fontFace: FT, color: C.ink }), options: {} },
    { text: runs(c, { fontSize: 14, fontFace: FT, color: C.muted }), options: {} }];
  s.addTable([
    [H("題目情境／關鍵字"), H("V_{c} 採用"), H("計算注意")],
    R("一般梁，無軸力、未要求精算", "0.53√f′c b_w d", "最常用；偏保守", "2E7D6B"),
    R("給了 ρ_w、V_u、M_u 或要求精算", "(0.50√f′c + 176 ρ_w V_u d/M_u) b_w d", "V_u d/M_u ≤ 1；≤ 0.93√f′c b_w d", "B7791F"),
    R("柱或梁受軸壓 N_u", "0.53(1 + N_u/140A_g)√f′c b_w d", "N_u 代正值；A_g 用全斷面", "2F54C8"),
    R("構材受軸拉 N_u", "0.53(1 + N_u/35A_g)√f′c b_w d", "N_u 代負值；負值取 0", "C0392B"),
    R("特殊抗彎矩構架塑鉸區", "V_c = 0", "兩條件同時成立：V_E ≥ V_u/2、P_u < A_g f′c/20", "8B1E14"),
    R("任何情況的上限", "V_s ≤ 2.12√f′c b_w d", "用基本式的 4 倍，不是修正後 V_c 的 4 倍", "6D4BC2"),
  ], { x: 0.6, y: 1.5, w: 12.1, colW: [3.6, 4.6, 3.9], rowH: 0.72, border: { type: "solid", color: "D5DAE1", pt: 1 },
       fill: { color: C.white }, valign: "middle", margin: 0.08 });
  T(s, "表中 kgf、cm 制；φ = 0.75", 0.6, 6.7, 12.1, 0.3, { fontSize: 12, color: C.muted, align: "right" });
  pageNo(s, pg);
}
// ───── 21 陷阱 ─────
{
  const s = newSlide();
  header(s, "高頻陷阱", "六個最常掉分的地方", C.ps);
  const cards = [
    ["「V_s ≤ 4V_c」的 V_c 是基本式", `上限寫死 2.12√f′c b_w d。軸拉 30 tf 時若拿 4 × ${f2n("VC_T30")} = ${f2n("WRONG_CAP")}，會把上限低估一半（正解 ${f2n("VS_MAX")}）`, RD],
    ["軸拉 N_u 要代負號", "拉力代負值、壓力代正值；算出倍率小於 0 時取 0，不是負的 V_c", BL],
    ["塑鉸區 V_c = 0 有條件", "地震剪力 ≥ 一半 且 軸壓 < A_g f′c/20，兩條件同時成立才歸零", RD],
    ["精算式的兩個上限", "V_u d/M_u 超過 1 取 1；結果不得大於 0.93√f′c b_w d", GD],
    ["b_w、d 不是 b、h", "V_c、V_s 都用腹板寬 b_w 與有效深度 d；軸力修正才用全斷面 A_g", GN],
    ["超過上限別加箍筋", "V_u > φ(2.65√f′c b_w d) 時，箍筋再多也沒用：斜壓桿先碎 → 加大斷面", PU],
  ];
  cards.forEach(([hd, body, P], i) => {
    const x = 0.6 + (i % 3) * 4.07, y = 1.5 + Math.floor(i / 3) * 2.8;
    panel(s, x, y, 3.95, 2.6, P[1], P[2]);
    T(s, paras([{ t: hd, o: { bold: true, fontSize: 16, color: P[0] } }, { t: body, o: { fontSize: 15 } }]), x + 0.22, y + 0.15, 3.55, 2.35, { paraSpaceAfter: 8 });
  });
  pageNo(s, pg);
}
// ───── 22 回顧 ─────
{
  const s = pres.addSlide(); s.background = { color: C.dark };
  T(s, "重點回顧：一句話推出四件事", 0.8, 0.7, 11, 0.8, { fontSize: 34, bold: true, color: C.white });
  const pts = [
    ["0", "底層：剪應力 τ 在 45° 方向就是主拉 σ_1 = τ；超過 f_t 就斜向拉裂", "A58BE6"],
    ["1", "f_t ∝ √f′c → V_c = 0.53√f′c b_w d；剪力不足先加大斷面", "7FC8B4"],
    ["2", "軸力平移莫爾圓：壓幫忙（÷140）、拉殺傷（÷35），同樣大小差 4 倍", "8FA8F0"],
    ["3", "塑鉸區反覆載重磨掉 V_c 的四個來源 → 兩條件成立時 V_c = 0", "F08A7E"],
    ["4", "V_c 抗拉、V_s 數箍筋（d/s 支）、上限 2.12√f′c b_w d 防斜壓桿壓碎", "F2A65A"],
  ];
  pts.forEach(([n, t, col], i) => {
    const y = 1.8 + i * 0.9;
    s.addShape(pres.shapes.OVAL, { x: 0.8, y, w: 0.58, h: 0.58, fill: { color: col }, line: { color: col } });
    T(s, n, 0.8, y, 0.58, 0.58, { fontSize: 19, bold: true, color: C.dark, align: "center", valign: "middle" });
    T(s, runs(t, { color: C.white, fontSize: 17 }), 1.6, y - 0.1, 11.2, 0.78, { valign: "middle" });
  });
  T(s, "下一步：拼圖二——拿含軸力修正或精算式的歷屆考題，按「選式 → V_s → 上限 → s_{max}」四關代數字", 0.8, 6.45, 11.8, 0.45, { fontSize: 16, bold: true, color: "F2A65A" });
}
pres.writeFile({ fileName: "RC-U2-1_剪力破壞的底層邏輯.pptx" }).then(() => console.log("written"));
