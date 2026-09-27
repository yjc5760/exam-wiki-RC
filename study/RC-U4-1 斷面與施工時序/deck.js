const pptxgen = require("pptxgenjs");
const fs = require("fs");
const N = JSON.parse(fs.readFileSync("nums.json", "utf8"));
const MJ = JSON.parse(fs.readFileSync("figs/math.json", "utf8"));
const pres = new pptxgen(); pres.layout = "LAYOUT_WIDE"; pres.title = "RC-U4-1 拼圖三：斷面與施工時序";
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
const OR = ["C2570C", "FCEEE5", "EBC3A5"];
const sgn = v => (v >= 0 ? "+" : "−") + f2(Math.abs(v));

const s2 = v => (v >= 0 ? "+" : "−") + f2(Math.abs(v));
const pct = v => Math.round(v * 100) + "%";
const s1 = v => (v >= 0 ? "+" : "−") + f2(Math.abs(v));
const cm = v => Math.round(v).toLocaleString("en-US");
// ───── 1 封面 ─────
{
  const s = pres.addSlide(); s.background = { color: C.dark };
  T(s, "RC-U4-1　預力梁斷面應力分析｜觀念講義・拼圖三", 0.8, 1.2, 11.5, 0.4, { fontSize: 16, color: "9FB3C8", bold: true });
  T(s, "斷面與施工時序", 0.8, 1.8, 11.8, 1.0, { fontSize: 46, bold: true, color: C.white });
  T(s, "此刻，只有「已經硬化」的混凝土能參與抗力——應力分階段算完再累加，絕不把總彎矩一次除以最終斷面", 0.8, 2.95, 11.8, 0.9, { fontSize: 21, color: "D6DEE8" });
  const dots = [["①", "非對稱斷面 S_t ≠ S_b", "8FA8F0"], ["②", "核心距 k_t、k_b", "A58BE6"], ["③", "濕版重與施工時序", "F08A7E"], ["④", "組合梁四步 SOP", "7FC8B4"]];
  dots.forEach(([n, lab, col], i) => {
    const x = 0.8 + i * 3.0;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 4.3, w: 2.75, h: 0.85, fill: { color: "243044" }, line: { color: col, width: 2 }, rectRadius: 0.1 });
    T(s, n, x + 0.15, 4.3, 0.55, 0.85, { valign: "middle", bold: true, color: col, fontSize: 24 });
    T(s, runs(lab, { color: C.white, bold: true, fontSize: 15 }), x + 0.7, 4.3, 2.0, 0.85, { valign: "middle" });
  });
  T(s, "示範梁與拼圖一、二相同：預鑄梁 40×80、L = 12 m、e = 25 cm、P_i = 150 t、P_e = 120 t；上方加一片 150×15 現場版（與梁同強度）。圖上數字全部由同一支程式算出",
    0.8, 6.2, 11.8, 0.6, { fontSize: 14, color: "9FB3C8" });
}
// ───── 2 總覽 ─────
figSlide("TOPIC MAP · 一句話貫通", "一個問題串起三個觀念：此刻，誰已經硬化？", "fig01_map", [
  cell("本拼圖的定位", ["拼圖一教你「一刻、一纖維」怎麼算；拼圖二決定「哪兩刻」要算；拼圖三回答：斷面本身會隨時間長大，每一刻該用哪個斷面？"], PU),
], C.le, 4.6);
// ───── 3 示範梁 ─────
{
  const s = newSlide();
  header(s, "承接拼圖二 · 示範組合梁", "同一根預鑄梁，上面多了一片現場澆置版", C.le);
  panel(s, 0.6, 1.5, 5.9, 5.4, C.panel);
  T(s, paras([
    { t: "示範組合梁資料", o: { bold: true, fontSize: 17, color: C.le } },
    { t: "預鑄梁 40×80：A_1 = 3,200 cm²、S_1 = 42,667 cm³", o: { fontSize: 15 } },
    { t: "直線鋼腱距梁底 y_{ps} = 15 cm（e_1 = 25 cm）", o: { fontSize: 15 } },
    { t: "現場版 b_e = 150、t = 15 cm；與梁同強度（n = 1）", o: { fontSize: 15 } },
    { t: `P_i = 150 t → P_e = 120 t（損失假設在澆版前完成）`, o: { fontSize: 15 } },
    { t: `梁自重 w_G = ${f3(N.WG)}、濕版 w_S = ${f3(N.WS)} t/m`, o: { fontSize: 15 } },
    { t: `組合後活載＋疊加靜載 w_L = ${f2(N.WL)} t/m；L = 12 m`, o: { fontSize: 15 } },
  ]), 0.85, 1.65, 5.5, 5.1, { paraSpaceAfter: 10 });
  panel(s, 6.65, 1.5, 6.05, 2.55, C.okbg, "9CC7BC");
  T(s, paras([{ t: "拼圖二已經給了你", o: { bold: true, fontSize: 17, color: C.ok } },
    { t: `傳遞階段 ①② 在預鑄梁上：頂 ${s1(N.S1T)}、底 ${s1(N.S1B)}`, o: { fontSize: 16 } },
    { t: "兩階段數據嚴格分開，不串料", o: { fontSize: 16 } }]), 6.9, 1.65, 5.6, 2.3, { paraSpaceAfter: 8 });
  panel(s, 6.65, 4.2, 6.05, 2.7, C.goldbg, "E6CFA0");
  T(s, paras([{ t: "拼圖三要回答的三件事", o: { bold: true, fontSize: 17, color: C.gold } },
    { t: "1. 斷面不對稱時，S 怎麼求？哪一側危險？", o: { fontSize: 16 } },
    { t: "2. 偏心到哪裡，另一側才開始受拉？", o: { fontSize: 16 } },
    { t: "3. 斷面在施工中變大，應力怎麼接力累加？", o: { fontSize: 16 } }]), 6.9, 4.35, 5.6, 2.45, { paraSpaceAfter: 8 });
  pageNo(s, pg);
}
// ───── 4 形心 ─────
figSlide("觀念 ① · 非對稱斷面", "形心不在半高：面積放在哪裡，形心就被拉向哪裡", "fig02_tsec", [
  cell("物理直覺", [`版的面積 2,250 cm² 全放在最上面 15 cm，把形心從 47.5 拉到 ${f2(N.YBC)}（距梁底）`], BL),
  cell("後果", [`梁底離形心 ${f2(N.YBC)}、版頂只有 ${f2(N.YTC_S)} → y_t ≠ y_b → S_t ≠ S_b`], RD),
], C.tot, 4.45);
// ───── 5 分割法 ─────
{
  const s = newSlide();
  header(s, "Step ① ② · 分割法＋平行軸定理", "先求形心 y_b，再用平行軸定理求 I_c", C.tot);
  const H = t => ({ text: runs(t, { bold: true, color: C.white, fontSize: 14, fontFace: FT }), options: { fill: { color: C.dark } } });
  const V = (t, b) => ({ text: runs(t, { bold: !!b, color: C.ink, fontSize: 14, fontFace: FT }), options: {} });
  s.addTable([
    [H("組成"), H("A_i (cm²)"), H("y_i (cm)"), H("A_i·y_i"), H("I_i (cm⁴)"), H("d_i (cm)"), H("A_i·d_i²")],
    [V("版 150×15", 1), V("2,250"), V("87.5"), V("196,875"), V(cm(N.IS)), V(f2(N.DS)), V(cm(N.AS * N.DS ** 2))],
    [V("梁 40×80", 1), V("3,200"), V("40.0"), V("128,000"), V(cm(N.I1)), V(f2(N.D1)), V(cm(N.A1 * N.D1 ** 2))],
    [V("Σ", 1), V("5,450", 1), V("—"), V("324,875", 1), V(cm(N.IS + N.I1)), V("—"), V(cm(N.AS * N.DS ** 2 + N.A1 * N.D1 ** 2))],
  ], { x: 0.6, y: 1.45, w: 12.1, colW: [1.9, 1.5, 1.4, 1.8, 1.9, 1.5, 2.1], rowH: 0.5, border: { type: "solid", color: "D5DAE1", pt: 1 },
       fill: { color: C.white }, valign: "middle", align: "center", margin: 0.06 });
  eqPanel(s, 0.6, 3.6, 5.9, 1.2, "① 形心", "m_ybar", ...BL);
  eqPanel(s, 6.6, 3.6, 6.1, 1.2, "② 慣性矩", "m_ic", ...BL);
  eqPanel(s, 0.6, 4.95, 12.1, 1.1, "③ 三個纖維各有一個 S", "m_sc", ...PU);
  panel(s, 0.6, 6.2, 12.1, 0.8, C.psbg, "EBB4AE");
  T(s, runs("最常漏的是 A_i·d_i²：兩塊各自的 I_i 加起來只有 1,748,854，還不到 I_c 的 4 成——移軸項才是主角", { fontSize: 15, color: C.ps, bold: true }), 0.85, 6.2, 11.7, 0.8, { valign: "middle" });
  pageNo(s, pg);
}
// ───── 6 危險面 ─────
figSlide("非對稱的後果", "同一個 M，S 小的那一側應力最大", "fig03_asym", [
  cell("絕對不可以直接用 I/(h/2)", [`I_c/47.5 = ${cm(N.S_WRONG)}：梁底被算成 ${s1(N.ML_B_WRONG)}，實際是 ${s1(N.ML_B)}——低估 ${Math.round((1 - N.ML_B_WRONG / N.ML_B) * 100)}%`], RD),
  cell("組合梁有三個「頂」", ["版頂、梁頂（介面）都要檢核：版頂是版的最外纖維，梁頂則帶著前面階段的應力"], GD),
], C.tot, 4.45);
// ───── 7 核心距 ─────
figSlide("觀念 ② · 核心距 kern", "偏心到哪裡，另一邊才開始出現拉應力", "fig04_kern", [
  cell("只有 P 作用", [`P_e = 120 t 放在矩形 40×80：e = 0 均勻 +37.50；e = k_b 頂恰為 0；e = 25 頂 ${s1(-32.8125)}`], PU),
  cell("核心區 = 完全受壓區", ["鋼腱落在核心內 → 全斷面受壓；落在核心外 → 對側受拉，但仍可在容許拉應力內"], GN),
], C.le, 4.5);
// ───── 8 推導 ─────
{
  const s = newSlide();
  header(s, "核心距推導", "令對側纖維應力 = 0，解出臨界偏心", C.le);
  eqPanel(s, 0.6, 1.45, 12.1, 1.15, "下核心距 k_b：鋼腱在形心「下方」，頂纖維恰不受拉", "m_kb", ...PU);
  eqPanel(s, 0.6, 2.75, 12.1, 1.15, "上核心距 k_t：鋼腱在形心「上方」，底纖維恰不受拉", "m_kt", ...PU);
  eqPanel(s, 0.6, 4.05, 6.4, 1.3, "換個寫法：用 k 表示應力", "m_kform", ...GN);
  eqPanel(s, 7.1, 4.05, 5.6, 1.3, "代回本例 e = 25", "m_kex", ...GN);
  panel(s, 0.6, 5.5, 12.1, 1.45, C.goldbg, "E6CFA0");
  T(s, paras([{ t: "記法：k 的下標跟 S 的下標「交叉」", o: { bold: true, fontSize: 16, color: C.gold } },
    { t: "k_b 管「頂纖維不受拉」所以用 S_t；k_t 管「底纖維不受拉」所以用 S_b。筆記裡若寫成 k_t = S_t/A 是筆誤——矩形斷面 S_t = S_b 看不出來，T 形斷面就會錯", o: { fontSize: 14 } }]),
    0.85, 5.6, 11.7, 1.3, { paraSpaceAfter: 6 });
  pageNo(s, pg);
}
// ───── 9 非對稱核心 ─────
figSlide("非對稱斷面的核心", "核心區也不對稱：矩形 h/3，T 形偏向一邊", "fig05_kernT", [
  cell("矩形", [`k_t = k_b = h/6 = ${f2(N.K1)}，核心寬 h/3——中三分之一`], BL),
  cell("組合 T 形", [`k_t = ${f2(N.KTC)}、k_b = ${f2(N.KBC)}；核心寬 ${f2(N.KTC + N.KBC)} cm`], PU),
  cell("核心距只是臨界點", ["它只描述「P 單獨作用」；真正的檢核仍要把 M/S 加進來"], GD),
], C.le, 4.35);
// ───── 10 施工三階段 ─────
figSlide("觀念 ③ · 施工時序", "每一刻，只有「已硬化並能傳力」的那部分斷面在工作", "fig06_stages", [
  cell("斷面在長大", [`A_1 = 3,200 → A_c = 5,450；形心 40.00 → ${f2(N.YBC)}`], BL),
  cell("偏心距也跟著變", [`e_1 = 25.00 → e_c = ${f2(N.EC)}；但預力施加時看到的是 e_1`], OR),
  cell("後拉法補充", ["張拉時導管還沒灌漿，要扣孔 → 淨斷面 A_n；本例忽略導管，A_n ≈ A_g"], GD),
], C.ps, 4.4);
// ───── 11 階段對照表 ─────
{
  const s = newSlide();
  header(s, "三階段數據對照", "每一段都要問四件事：斷面、預力、彎矩、強度", C.ps);
  const H = t => ({ text: runs(t, { bold: true, color: C.white, fontSize: 15, fontFace: FT }), options: { fill: { color: C.dark } } });
  const V = (t, col, b) => ({ text: runs(t, { color: col || C.ink, bold: !!b, fontSize: 15, fontFace: FT }), options: {} });
  s.addTable([
    [H("階段"), H("用哪個斷面"), H("用哪個預力"), H("該階段新增的彎矩"), H("強度")],
    [V("① 張拉／放張", C.ink, 1), V("斷面 1（後拉：淨斷面 A_n）", C.ok), V("P_i = 150 t，e_1 = 25", "C2570C"), V(`M_G = ${f3(N.MG)}`, C.ps), V("f′_{ci}", "2C6E9E")],
    [V("② 損失＋澆版", C.ink, 1), V("斷面 1（濕版不計入）", C.ok), V("ΔP = −30 t（→ P_e）", "C2570C"), V(`M_S = ${f2(N.MS)}（累加）`, C.ps), V("f′_c", "2C6E9E")],
    [V("③ 版硬化後", C.ink, 1), V("組合斷面 A_c、S_c", C.ok), V("不再新增", "C2570C"), V(`M_L = ${f2(N.ML)}`, C.ps), V("f′_c", "2C6E9E")],
  ], { x: 0.6, y: 1.5, w: 12.1, colW: [2.2, 3.1, 2.6, 2.8, 1.4], rowH: 0.7, border: { type: "solid", color: "D5DAE1", pt: 1 },
       fill: { color: C.white }, valign: "middle", margin: 0.1 });
  const cards = [
    ["預力只在斷面 1 上作用", "鋼腱在組合前就已張拉錨定，預力的 P/A、P·e/S 永遠用 A_1、S_1、e_1；e_c 只在「組合後才施預力」時才用", OR],
    ["損失為什麼算在斷面 1", "教科書簡化：假設損失在澆版前完成。若題目說部分損失發生在組合後，那一部分 ΔP 要用 A_c、e_c", GD],
  ];
  cards.forEach(([hd, b, P], i) => {
    const x = 0.6 + i * 6.1;
    panel(s, x, 4.6, 6.0, 2.35, P[1], P[2]);
    T(s, paras([{ t: hd, o: { bold: true, fontSize: 17, color: P[0] } }, { t: b, o: { fontSize: 15 } }]), x + 0.22, 4.75, 5.6, 2.1, { paraSpaceAfter: 8 });
  });
  pageNo(s, pg);
}
// ───── 12 濕版陷阱 ─────
figSlide("失分地雷 · 濕版重", "濕混凝土沒有勁度，濕版重只能由預鑄梁獨自承擔", "fig07_wet", [
  cell("為什麼會錯", ["看到最終是 T 形，就把所有彎矩都除以 S_c；但澆版那一刻，版還是液體"], RD),
  cell("判斷準則只有一句", ["「這個載重上來時，誰已經硬化？」——吊裝、拆撐、疊加靜載都用同一句判斷"], GN),
], C.ps, 4.5);
// ───── 13 支撐 ─────
figSlide("例外 · 有支撐施工", "同一片濕版，施工方法不同，M_S 就落在不同斷面", "fig08_shore", [
  cell("讀題關鍵字", ["「無支撐」「unshored」或沒提 → 預設 M_S 由斷面 1 承擔；「有臨時支撐」「shored」→ 拆撐時 M_S 由組合斷面承擔"], GD),
  cell("底層邏輯沒變", ["有支撐時，濕版重量由支撐接走；拆撐的那一刻版已硬化——仍是「誰已經硬化」這一句"], GN),
], C.gold, 4.4);
// ───── 14 SOP ─────
figSlide("組合梁解題 SOP", "四步驟：兩套幾何 → 三個彎矩 → 分段 Δf → 累加", "fig09_sop", [
  cell("Step 3 的判斷", ["每個彎矩先問：它作用時版硬化了沒？沒有 → S_1；有 → S_c。預力永遠在 S_1"], GD),
  cell("Step 4 的纖維", ["梁頂、梁底、版頂三條分開累加；版頂只從 ③ 開始有應力"], PU),
], C.le, 4.4);
// ───── 15 Step1 ─────
{
  const s = newSlide();
  header(s, "Step 1 · 兩套斷面幾何", "左邊給預力與 M_G、M_S 用；右邊只給 M_L 用", C.gold);
  const L1 = [["斷面 1（預鑄梁）", [`A_1 = 3,200 cm²`, `I_1 = ${cm(N.I1)} cm⁴`, `y_t = y_b = 40.00 cm`, `S_1 = ${cm(N.S1)} cm³`, `e_1 = 40 − 15 = 25.00 cm`, `k_t = k_b = ${f2(N.K1)} cm`], BL],
              ["組合斷面（梁＋版）", [`A_c = 5,450 cm²`, `I_c = ${cm(N.IC)} cm⁴`, `y_b = ${f2(N.YBC)}；梁頂 ${f2(N.YTC_B)}；版頂 ${f2(N.YTC_S)}`, `S_{b,c} = ${cm(N.SBC)}；S_{t,梁} = ${cm(N.STC_B)}；S_{t,版} = ${cm(N.STC_S)}`, `e_c = ${f2(N.EC)} cm`, `k_t = ${f2(N.KTC)}、k_b = ${f2(N.KBC)} cm`], GN]];
  L1.forEach(([hd, items, P], i) => {
    const x = 0.6 + i * 6.1;
    panel(s, x, 1.5, 6.0, 4.1, P[1], P[2]);
    T(s, paras([{ t: hd, o: { bold: true, fontSize: 18, color: P[0] } }, ...items.map(t => ({ t, o: { fontSize: 15 } }))]), x + 0.25, 1.65, 5.6, 3.85, { paraSpaceAfter: 9 });
  });
  eqPanel(s, 0.6, 5.75, 12.1, 1.2, "組合斷面偏心距（僅供組合後施加預力或損失時使用）", "m_ec", ...OR);
  pageNo(s, pg);
}
// ───── 16 Step2 ─────
{
  const s = newSlide();
  header(s, "Step 2 · 三個彎矩，各自對應一個時刻", "簡支梁跨中 M = wL²/8，分開算、分開放", C.gold);
  eqPanel(s, 0.6, 1.5, 12.1, 1.3, "M_G：梁自重（放張瞬間就在）→ 斷面 1", "m_mg", ...BL);
  eqPanel(s, 0.6, 2.95, 12.1, 1.3, "M_S：濕版重（w_S = 0.15×1.5×2.4）→ 斷面 1", "m_ms", ...RD);
  eqPanel(s, 0.6, 4.4, 12.1, 1.3, "M_L：活載＋疊加靜載（版硬化後才上來）→ 組合斷面", "m_ml", ...GN);
  panel(s, 0.6, 5.85, 12.1, 1.1, C.purbg, "C9BCEB");
  T(s, runs(`總彎矩 M_T = ${f3(N.MG)} + ${f2(N.MS)} + ${f2(N.ML)} = ${f3(N.MT)} t-m——這個數字「不能」拿來直接除以任何一個 S`, { fontSize: 16, bold: true, color: C.le }), 0.85, 5.85, 11.7, 1.1, { valign: "middle" });
  pageNo(s, pg);
}
// ───── 17 增量圖 ─────
figSlide("Step 3 · 分階段增量 Δf", "四段應力增量：前三段在斷面 1，最後一段在組合斷面", "fig10_inc", [
  cell("②a 預力損失是「負的預力」", ["ΔP = −30 t 代入同一條式子：頂 +8.20、底 −26.95——把原本存在底部的預壓力拿走"], OR),
  cell("③ 是唯一跨進版的應力", [`M_L 在組合斷面上呈一條直線：版頂 ${s1(N.ML_S)} → 梁底 ${s1(N.ML_B)}`], GN),
], C.gold, 4.55);
// ───── 18 增量算式 ─────
{
  const s = newSlide();
  header(s, "Step 3 · 梁底纖維逐段代數", "每一段只用那一段的 P、M 和斷面", C.gold);
  eqPanel(s, 0.6, 1.45, 6.0, 1.2, "① P_i + M_G（斷面 1）", "m_s1", ...BL);
  eqPanel(s, 6.7, 1.45, 6.0, 1.2, "②a 預力損失（斷面 1）", "m_s2a", ...OR);
  eqPanel(s, 0.6, 2.8, 6.0, 1.2, "②b 濕版 M_S（斷面 1）", "m_s2b", ...RD);
  eqPanel(s, 6.7, 2.8, 6.0, 1.2, "③ 活載 M_L（組合斷面）", "m_s3", ...GN);
  eqPanel(s, 0.6, 4.15, 12.1, 1.2, "Step 4 · 累加並比容許（使用階段）", "m_sum", ...PU);
  const cards = [["梁頂同理", `${s1(N.S1T)} + 8.20 + 22.78 + 13.97 = ${s1(N.FT_T)} ≤ +210`, BL],
                 ["版頂只有 ③", `M_L / S_{t,版} = ${s1(N.FT_S)} ≤ +210`, GD]];
  cards.forEach(([hd, b, P], i) => {
    const x = 0.6 + i * 6.1;
    panel(s, x, 5.5, 6.0, 1.45, P[1], P[2]);
    T(s, paras([{ t: hd, o: { bold: true, fontSize: 16, color: P[0] } }, { t: b, o: { fontSize: 15 } }]), x + 0.22, 5.6, 5.6, 1.3, { paraSpaceAfter: 6 });
  });
  pageNo(s, pg);
}
// ───── 19 瀑布 ─────
figSlide("Step 4 · 應力是一段一段疊上去的", "瀑布圖：看每一階段把纖維往哪個方向推", "fig11_waterfall", [
  cell("梁底一路被「提款」", [`放張時存了 ${s1(N.S1B)} 的預壓，損失、濕版、活載三次提款後剩 ${s1(N.FT_B)}`], RD),
  cell("梁頂由拉轉壓", [`放張時 ${s1(N.S1T)}（傳遞控制點 ①），之後三段都往壓的方向推到 ${s1(N.FT_T)}`], BL),
], C.gold, 4.45);
// ───── 20 最終分布 ─────
figSlide("最終應力分布", "組合梁的總應力圖在介面處「斷開」——這是分階段累加的指紋", "fig12_final", [
  cell("看到斷開就知道算對了", ["如果你的總應力是一條連續直線，代表把所有彎矩都除了同一個斷面——一次算完的錯"], PU),
], C.ok, 4.6);
// ───── 21 錯法比較 ─────
figSlide("三種常見錯法", "每一種都讓梁底「看起來更壓、更安全」", "fig13_traps", [
  cell("濕版誤用 S_c", [`多了 ${f2(N.FB_WETWRONG - N.FT_B)}：最常見`], RD),
  cell("一次算完", [`P_e 放在 e_c、M_T 全除 S_c：多了 ${f2(N.ONE_B - N.FT_B)}`], OR),
  cell("I/(h/2)", [`形心當成在半高：多了 ${f2(N.S2B + N.ML_B_WRONG - N.FT_B)}`], GD),
], C.ps, 4.4);
// ───── 22 組合紅利 ─────
{
  const s = figSlide("為什麼要做組合梁", "版一旦硬化，就把梁底的 S 放大近一倍", "fig14_bonus", [], C.ok, 4.35);
  eqPanel(s, 0.6, 5.9, 12.1, 1.15, "反算：令梁底總應力 = 容許拉，解 M_L", "m_mlx", ...GN);
}
// ───── 23 陷阱 ─────
{
  const s = newSlide();
  header(s, "高頻陷阱", "六個讓組合梁題目失分的地方", C.ps);
  const cards = [
    ["濕版除以 S_c", `梁底被低估 ${f2(N.FB_WETWRONG - N.FT_B)} kgf/cm²；濕混凝土沒有勁度`, RD],
    ["一次算完", "把 M_T 除以最終斷面、P 放在 e_c：應力歷史全部消失", OR],
    ["I/(h/2)", `T 形斷面形心不在半高：S_b 被高估 ${Math.round((N.S_WRONG / N.SBC - 1) * 100)}%`, GD],
    ["漏了移軸項", "I_c 只加 I_i 不加 A_i·d_i²，I 少了六成以上", BL],
    ["版頂也累加", "版頂只有 M_L/S_{t,版}；把 ①② 的梁頂應力加到版頂是錯的", PU],
    ["k_t、k_b 下標", "k_b = S_t/A、k_t = S_b/A（交叉）；非對稱斷面兩者不同", GN],
  ];
  cards.forEach(([hd, body, P], i) => {
    const x = 0.6 + (i % 3) * 4.07, y = 1.5 + Math.floor(i / 3) * 2.8;
    panel(s, x, y, 3.95, 2.6, P[1], P[2]);
    T(s, paras([{ t: hd, o: { bold: true, fontSize: 17, color: P[0] } }, { t: body, o: { fontSize: 15 } }]), x + 0.22, y + 0.15, 3.55, 2.35, { paraSpaceAfter: 8 });
  });
  pageNo(s, pg);
}
// ───── 24 速查 ─────
{
  const s = newSlide();
  header(s, "考場速查 · 組合梁累加表", "每一列一段、每一欄一個纖維；最後一列就是答案", C.ok);
  const H = t => ({ text: runs(t, { bold: true, color: C.white, fontSize: 14, fontFace: FT }), options: { fill: { color: C.dark } } });
  const R = (cells, b) => cells.map((t, i) => ({ text: runs(t, { bold: i === 0 || b, color: i === 0 ? C.le : C.ink, fontSize: 14, fontFace: FT }), options: b ? { fill: { color: "F1EDFA" } } : {} }));
  s.addTable([
    [H("階段"), H("斷面"), H("載重"), H("版頂"), H("梁頂"), H("梁底")],
    R(["① 放張", "S_1", "P_i、M_G", "—", s1(N.S1T), s1(N.S1B)]),
    R(["②a 損失", "S_1", "ΔP = −30 t", "—", s1(N.LOSS_T), s1(N.LOSS_B)]),
    R(["②b 澆版", "S_1", "M_S", "—", s1(N.MS_T), s1(N.MS_B)]),
    R(["③ 使用", "S_c", "M_L", s1(N.ML_S), s1(N.ML_T), s1(N.ML_B)]),
    R(["合計", "", "", s1(N.FT_S), s1(N.FT_T), s1(N.FT_B)], true),
    R(["容許", "", "", "≤ +210", "≤ +210", `≥ −${f2(N.FTS_A)}`]),
  ], { x: 0.6, y: 1.5, w: 12.1, colW: [1.9, 1.3, 2.4, 2.1, 2.2, 2.2], rowH: 0.56, border: { type: "solid", color: "D5DAE1", pt: 1 },
       fill: { color: C.white }, valign: "middle", align: "center", margin: 0.06 });
  panel(s, 0.6, 5.65, 5.95, 1.3, C.okbg, "9CC7BC");
  T(s, paras([{ t: "幾何", o: { bold: true, fontSize: 15, color: C.ok } },
    { t: `y_b = ${f2(N.YBC)}、I_c = ${cm(N.IC)}、S_{b,c} = ${cm(N.SBC)}、e_c = ${f2(N.EC)}`, o: { fontSize: 14 } }]), 0.85, 5.72, 5.5, 1.2, { paraSpaceAfter: 6 });
  panel(s, 6.75, 5.65, 5.95, 1.3, C.lebg, "C9BCEB");
  T(s, paras([{ t: "最大活載", o: { bold: true, fontSize: 15, color: C.le } },
    { t: `M_{L,max} = ${f2(N.MLX_C)} t-m → w_{L,max} = ${f2(N.WLX_C)} t/m（無組合僅 ${f2(N.WLX_N)}）`, o: { fontSize: 14 } }]), 7.0, 5.72, 5.5, 1.2, { paraSpaceAfter: 6 });
  pageNo(s, pg);
}
// ───── 25 回顧 ─────
{
  const s = pres.addSlide(); s.background = { color: C.dark };
  T(s, "重點回顧：此刻，誰已經硬化？", 0.8, 0.7, 11.5, 0.8, { fontSize: 34, bold: true, color: C.white });
  const pts = [
    ["S", `非對稱斷面先求 y_b、I（別漏 A·d²），再分別求 S_t、S_b；S 小的一側（本例梁底 ${cm(N.SBC)}）最危險`, "8FA8F0"],
    ["k", `核心距 k_b = S_t/A、k_t = S_b/A（下標交叉）；矩形 h/6，T 形 ${f2(N.KTC)}／${f2(N.KBC)}`, "A58BE6"],
    ["濕", "濕版沒有勁度：M_S 由預鑄梁 S_1 承擔（有支撐施工才改由 S_c）", "F08A7E"],
    ["Σ", `應力分階段算完再累加：梁底 ${s1(N.S1B)} → ${s1(N.FT_B)}；介面應力斷開是正確的指紋`, "F2A65A"],
    ["✓", "三條纖維分開檢核：版頂、梁頂、梁底；一次算完的答案永遠偏不保守", "7FC8B4"],
  ];
  pts.forEach(([n, t, col], i) => {
    const y = 1.8 + i * 0.9;
    s.addShape(pres.shapes.OVAL, { x: 0.8, y, w: 0.58, h: 0.58, fill: { color: col }, line: { color: col } });
    T(s, n, 0.8, y, 0.58, 0.58, { fontSize: 19, bold: true, color: C.dark, align: "center", valign: "middle" });
    T(s, runs(t, { color: C.white, fontSize: 17 }), 1.6, y - 0.1, 11.2, 0.78, { valign: "middle" });
  });
  T(s, "下一步：拼圖四——從檢核到設計：鋼腱可行區（Cable Zone）、開裂彎矩 M_{cr} 與極限強度 M_n", 0.8, 6.45, 11.8, 0.45, { fontSize: 16, bold: true, color: "F2A65A" });
}
pres.writeFile({ fileName: "RC-U4-1_斷面與施工時序.pptx" }).then(() => console.log("written"));
