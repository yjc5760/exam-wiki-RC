const pptxgen = require("pptxgenjs");
const fs = require("fs");
const N = JSON.parse(fs.readFileSync("nums.json", "utf8"));
const MJ = JSON.parse(fs.readFileSync("figs/math.json", "utf8"));
const pres = new pptxgen(); pres.layout = "LAYOUT_WIDE"; pres.title = "RC-U4-1 拼圖一：三項應力的加減";
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
// ───── 1 封面 ─────
{
  const s = pres.addSlide(); s.background = { color: C.dark };
  T(s, "RC-U4-1　預力梁斷面應力分析｜觀念講義・拼圖一", 0.8, 1.2, 11.5, 0.4, { fontSize: 16, color: "9FB3C8", bold: true });
  T(s, "三項應力的加減", 0.8, 1.8, 11.8, 1.0, { fontSize: 46, bold: true, color: C.white });
  T(s, "斷面上的應力分佈，只是三張基本應力圖的簡單加減——大小由 P、e、M、A、S 決定，正負由變形方向決定", 0.8, 2.95, 11.8, 0.9, { fontSize: 21, color: "D6DEE8" });
  const dots = [["①", "P/A 矩形恆壓", "8FA8F0"], ["②", "P·e/S 上拉下壓", "F2A65A"], ["③", "M/S 上壓下拉", "F08A7E"], ["④", "三步 SOP", "7FC8B4"]];
  dots.forEach(([n, lab, col], i) => {
    const x = 0.8 + i * 3.0;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 4.3, w: 2.75, h: 0.85, fill: { color: "243044" }, line: { color: col, width: 2 }, rectRadius: 0.1 });
    T(s, n, x + 0.15, 4.3, 0.55, 0.85, { valign: "middle", bold: true, color: col, fontSize: 24 });
    T(s, lab, x + 0.7, 4.3, 2.0, 0.85, { valign: "middle", color: C.white, bold: true, fontSize: 15 });
  });
  T(s, "示範梁：40×80 cm 矩形、L = 12 m、e = 25 cm、P_i = 150 t、P_e = 120 t（與主講義微型例題①相同）；圖上數字全部由同一支程式算出，可逐一對帳",
    0.8, 6.2, 11.8, 0.6, { fontSize: 14, color: "9FB3C8" });
}
// ───── 2 總覽 ─────
figSlide("TOPIC MAP · 一句話貫通", "斷面上永遠只有三項應力，解題永遠只有三個步驟", "fig01_map", [
  cell("本拼圖的定位", ["拼圖一只做一件事：把「任一時刻、任一纖維」的應力算對。拼圖二再把它放進「兩階段 × 四控制點」去比容許應力。"], PU),
], C.le, 4.6);
// ───── 3 示範梁 ─────
figSlide("示範梁 · 全篇貫穿", "一根 40×80 的簡支預力梁，所有數字都從它算出來", "fig02_beam", [
  cell("斷面性質", [`A = 40×80 = 3,200 cm²`, `S_t = S_b = bh²/6 = 42,667 cm³`], BL),
  cell("自重彎矩（傳遞階段）", [`w_d = 0.40×0.80×2.4 = 0.768 t/m`, `M_d = 0.768×12²/8 = ${f3(N.MD)} t-m`], RD),
  cell("預力", [`傳遞 P_i = 150 t、使用 P_e = 120 t（損失 20%）`, `直線鋼腱，偏心 e = 25 cm（形心下方）`], OR),
], C.le, 4.1);
// ───── 4 約定與通式 ─────
{
  const s = newSlide();
  header(s, "約定 · 一條通式", "先寫下約定：壓應力為正（+）、拉應力為負（−）", C.le);
  panel(s, 0.6, 1.5, 3.6, 1.55, C.dark, C.dark);
  T(s, paras([{ t: "答題第一行就寫", o: { fontSize: 14, color: "9FB3C8", bold: true } },
              { t: "壓 ＋、拉 −", o: { fontSize: 30, bold: true, color: C.white } }]), 0.85, 1.65, 3.2, 1.3);
  eqPanel(s, 4.35, 1.5, 8.35, 1.55, "通式：任一纖維 = ① 軸壓 ± ② 偏心 ∓ ③ 外力", "m_gen", ...PU);
  eqPanel(s, 0.6, 3.2, 6.0, 1.75, "頂纖維（t = top）", "m_top", ...RD, null);
  eqPanel(s, 6.7, 3.2, 6.0, 1.75, "底纖維（b = bottom）", "m_bot", ...BL, null);
  eqPanel(s, 0.6, 5.1, 6.0, 1.3, "斷面模數：到「該纖維」的距離", "m_S", ...GD);
  eqPanel(s, 6.7, 5.1, 6.0, 1.3, "矩形（對稱）斷面", "m_Srect", ...GN);
  T(s, "這兩條不必背：下一頁起逐項拆開，符號會從變形方向自己跑出來", 0.6, 6.6, 12.1, 0.35, { fontSize: 14, color: C.muted });
  pageNo(s, pg);
}
// ───── 5 ① 軸壓 ─────
figSlide("三項拆解 ① · 軸壓項 P/A", "把預力移到形心推梁：全斷面均勻受壓，永遠是 ＋", "fig03_axial", [
  cell("物理意義", ["預力合力通過形心的那一份：只「推」、不「彎」，每條纖維縮短一樣多 → 矩形分佈"], BL),
  cell("為什麼恆為正", ["鋼腱拉緊、反力推混凝土 → 預力對混凝土永遠是壓；不管在頂在底、傳遞或使用，符號都不必想"], GN),
], C.tot);
// ───── 6 ② 偏心 ─────
figSlide("三項拆解 ② · 偏心項 P·e/S", "鋼腱不在形心 → 搬回形心要補一個力偶 P·e", "fig04_ecc", [
  cell("力偶的方向", ["鋼腱在形心下方：左端逆時針、右端順時針 → 梁被往上彎（上拱）→ 頂拉、底壓"], OR),
  cell("「上下等值反號」的前提", ["只在對稱斷面成立（S_t = S_b）；T 形、I 形或組合梁要分開除 S_t 與 S_b"], PU),
], C.org);
// ───── 7 ③ 外力 ─────
figSlide("三項拆解 ③ · 外力項 M/S", "載重把梁往下彎：頂壓、底拉，方向恰好與 ② 相反", "fig05_ext", [
  cell("M 代哪一個", ["傳遞階段：只有自重 M_d；使用階段：M_T = M_d + M_L。M 用跨中（或題目指定斷面）的值"], RD),
  cell("與 ② 反向，正是預力的目的", ["② 事先在底纖維「存」了壓應力，③ 把它用掉；存得夠多，底纖維就不會被拉裂"], GN),
], C.ps);
// ───── 8 變形直覺 ─────
figSlide("符號判定 · 不背公式看變形", "問一句話：誰把梁頂上去、誰把梁壓下來？", "fig06_deform", [
  cell("口訣只要一句", ["往上彎 → 凸面在頂 → 頂被拉開（−）；往下彎 → 凸面在底 → 底被拉開（−）"], PU),
  cell("P/A 不參與判斷", ["軸壓項全斷面同號，永遠 ＋；只有 ② 和 ③ 要看變形決定符號"], BL),
], C.le, 4.5);
// ───── 9 符號總表 ─────
{
  const s = newSlide();
  header(s, "符號總表 · 三項 × 兩纖維", "把變形直覺填進表格，就得到頂／底兩條通式", C.le);
  const H = t => ({ text: runs(t, { bold: true, color: C.white, fontSize: 15, fontFace: FT }), options: { fill: { color: C.dark } } });
  const P = (t, col) => ({ text: runs(t, { bold: true, color: col, fontSize: 16, fontFace: FT }), options: { align: "center" } });
  const L = (t, col) => ({ text: runs(t, { bold: true, color: col || C.ink, fontSize: 16, fontFace: FT }), options: {} });
  const M = t => ({ text: runs(t, { fontSize: 14, color: C.muted, fontFace: FT }), options: {} });
  s.addTable([
    [H("項目"), H("頂纖維"), H("底纖維"), H("誰決定符號")],
    [L("① 軸壓 P/A", "2F54C8"), P("＋（壓）", "2F54C8"), P("＋（壓）", "2F54C8"), M("恆為壓，不必判斷")],
    [L("② 偏心 P·e/S", "C2570C"), P("−（拉）", "C0392B"), P("＋（壓）", "2F54C8"), M("鋼腱在形心下方 → 上拱")],
    [L("③ 外力 M/S", "C0392B"), P("＋（壓）", "2F54C8"), P("−（拉）", "C0392B"), M("正彎矩（載重向下）→ 下垂")],
  ], { x: 0.6, y: 1.5, w: 12.1, colW: [3.0, 2.4, 2.4, 4.3], rowH: 0.62, border: { type: "solid", color: "D5DAE1", pt: 1 },
       fill: { color: C.white }, valign: "middle", margin: 0.1 });
  eqPanel(s, 0.6, 4.25, 6.0, 1.75, "縱向讀「頂纖維」欄", "m_top", ...RD);
  eqPanel(s, 6.7, 4.25, 6.0, 1.75, "縱向讀「底纖維」欄", "m_bot", ...BL);
  T(s, "表格是「變形直覺」的結果，不是要背的東西；鋼腱若在形心上方（連續梁支承處），② 的兩格整個對調", 0.6, 6.25, 12.1, 0.5, { fontSize: 14, color: C.muted });
  pageNo(s, pg);
}
// ───── 10 非對稱 ─────
figSlide("延伸 · 非對稱斷面", "S_t ≠ S_b 時：零點在形心，頂、底大小不再相同", "fig07_asym", [
  cell("做法不變", ["一樣三項、一樣看變形定符號；只是頂纖維除 S_t = I/y_t、底纖維除 S_b = I/y_b"], PU),
  cell("S 小的那側應力大", [`本例 S_b 只有 S_t 的 ${f1(N.SB3 / N.ST3 * 100)}%：同一個 M，底緣 ${f2(-N.DB3)} 是梁頂 ${f2(N.DT3)} 的 ${f1(N.DB3 / -N.DT3)} 倍`], RD),
], C.le, 4.4);
// ───── 11 Step 1 ─────
{
  const s = newSlide();
  header(s, "SOP Step 1 · 算純數值", "先把三項的大小算出來，一個符號都不要寫", C.gold);
  eqPanel(s, 0.6, 1.5, 3.95, 1.9, "① 軸壓", "m_t1", ...BL, "kgf/cm²");
  eqPanel(s, 4.675, 1.5, 3.95, 1.9, "② 偏心", "m_t2", ...OR, "kgf/cm²");
  eqPanel(s, 8.75, 1.5, 3.95, 1.9, "③ 外力（自重）", "m_t3", ...RD, "kgf/cm²");
  eqPanel(s, 0.6, 3.6, 6.0, 1.3, "自重彎矩", "m_Md", ...GD);
  eqPanel(s, 6.7, 3.6, 6.0, 1.3, "斷面性質", "m_A", ...GN);
  const cards = [
    ["單位一次換好", "P 用 kgf（t × 1000）、M 用 kgf-cm（t-m × 10⁵）、e 與 S 用 cm；應力就直接是 kgf/cm²", PU],
    ["M 不要先四捨五入", `M_d = 13.824 → ${f3(N.T3)}；若先寫成 13.82 → ${f2(N.T3_R)}，末位就對不上答案`, RD],
  ];
  cards.forEach(([hd, b, P], i) => {
    const x = 0.6 + i * 6.1;
    panel(s, x, 5.1, 6.0, 1.85, P[1], P[2]);
    T(s, paras([{ t: hd, o: { bold: true, fontSize: 16, color: P[0] } }, { t: b, o: { fontSize: 14 } }]), x + 0.22, 5.22, 5.6, 1.65, { paraSpaceAfter: 6 });
  });
  pageNo(s, pg);
}
// ───── 12 Step 2 ─────
figSlide("SOP Step 2 · 看變形定符號", "每一項各問一次：頂纖維被拉開還是壓緊？", "fig08_steps", [
  cell("頂纖維", ["軸壓 (+)、偏心拉 (−)、外力壓 (+)"], RD),
  cell("底纖維", ["軸壓 (+)、偏心壓 (+)、外力拉 (−)"], BL),
], C.le, 4.3);
// ───── 13 Step 3 ─────
{
  const s = figSlide("SOP Step 3 · 加減得合成應力", "三張圖逐點相加：頂纖維小拉、底纖維大壓", "fig09_transfer", [], C.ok, 4.35);
  eqPanel(s, 0.6, 5.9, 6.0, 1.15, "頂纖維", "m_ft", ...RD);
  eqPanel(s, 6.7, 5.9, 6.0, 1.15, "底纖維", "m_fb", ...BL);
}
// ───── 14 瀑布圖 ─────
figSlide("Step 3 的另一種看法 · 數線上走三步", "從 0 出發：往右是壓、往左是拉，走完三步就是答案", "fig10_waterfall", [
  cell("頂纖維在打拉鋸戰", [`偏心項 ${f2(N.T2)} 比軸壓 ${f2(N.T1)} 大，單靠預力頂纖維已被拉到 ${sgn(N.FT_P)}；傳遞階段靠自重救回到 ${sgn(N.FT_I)}`], RD),
  cell("底纖維是一路累積壓", [`① ② 同向疊到 ${sgn(N.T1 + N.T2)}，③ 只拿走 ${f2(N.T3)} → ${sgn(N.FB_I)}：傳遞階段底纖維要擔心的是「壓太大」`], BL),
], C.ok, 4.4);
// ───── 15 核心距 ─────
{
  const s = figSlide("延伸 · 頂纖維什麼時候會出現拉？", "偏心超過核心距 k = S/A，單靠預力頂纖維就會受拉", "fig12_kern", [], C.le, 4.3);
  eqPanel(s, 0.6, 5.85, 7.0, 1.2, "核心距與「僅預力」頂纖維應力", "m_kern", ...GN);
  panel(s, 7.75, 5.85, 4.95, 1.2, C.purbg, "C9BCEB");
  T(s, paras([{ t: "自重是傳遞階段的幫手", o: { bold: true, fontSize: 14, color: C.le } },
              { t: `e = 25 > k = ${f2(N.K)}，頂纖維 ${sgn(N.FT_P)}；自重 +${f2(N.T3)} 把它拉回 ${sgn(N.FT_I)}。所以傳遞階段一定要把 M_d 算進去`, o: { fontSize: 13 } }]),
    7.95, 5.93, 4.6, 1.1, { paraSpaceAfter: 2 });
}
// ───── 16 換階段 ─────
{
  const s = figSlide("同一條式子 · 換階段只換 P 與 M", "使用階段：P 變小、M 變大，危險點從頂纖維換到底纖維", "fig11_service", [], C.le, 4.35);
  eqPanel(s, 0.6, 5.9, 6.0, 1.15, "頂纖維（P_e = 120 t、M_T = 58.824 t-m）", "m_fts", ...BL);
  eqPanel(s, 6.7, 5.9, 6.0, 1.15, "底纖維", "m_fbs", ...RD);
}
// ───── 17 陷阱 ─────
{
  const s = newSlide();
  header(s, "高頻陷阱", "六個最常把正負號或數值弄錯的地方", C.ps);
  const cards = [
    ["P/A 永遠是 ＋", "不管頂底、不管階段；會出錯通常是把它跟偏心項綁在一起一起變號", BL],
    ["非對稱斷面分開除 S", `頂用 S_t = I/y_t、底用 S_b = I/y_b；T 形、組合梁 S_t 與 S_b 可差到 ${f1(N.ST3 / N.SB3)} 倍`, PU],
    ["單位：t-m × 10⁵", "M 從 t-m 換成 kgf-cm 要乘 10⁵，P 從 t 換 kgf 乘 10³；兩個倍數不同，最容易漏", GD],
    ["P_i 還是 P_e？", "傳遞階段用 P_i（未損失），使用階段用 P_e；換階段三項中有兩項跟著變", OR],
    ["M 代自重還是全載", `傳遞只有 M_d = ${f3(N.MD)}；使用是 M_T = ${f3(N.MT)} t-m。傳遞階段漏掉自重，頂纖維會多算出 ${f2(N.T3)} 的拉`, RD],
    ["鋼腱在形心上方", "連續梁支承處、懸臂梁鋼腱在上方：力偶把梁往下彎，② 的符號整個對調；照樣「看變形」就不會錯", GN],
  ];
  cards.forEach(([hd, body, P], i) => {
    const x = 0.6 + (i % 3) * 4.07, y = 1.5 + Math.floor(i / 3) * 2.8;
    panel(s, x, y, 3.95, 2.6, P[1], P[2]);
    T(s, paras([{ t: hd, o: { bold: true, fontSize: 16, color: P[0] } }, { t: body, o: { fontSize: 15 } }]), x + 0.22, y + 0.15, 3.55, 2.35, { paraSpaceAfter: 8 });
  });
  pageNo(s, pg);
}
// ───── 18 速查卡 ─────
{
  const s = newSlide();
  header(s, "考場速查 · 三步 SOP", "算純數字 → 看變形定符號 → 加減；每一步都附示範梁的答案", C.ok);
  const H = t => ({ text: runs(t, { bold: true, color: C.white, fontSize: 14, fontFace: FT }), options: { fill: { color: C.dark } } });
  const R = (a, b, c, d, col) => [
    { text: runs(a, { bold: true, color: col, fontSize: 15, fontFace: FT }), options: {} },
    { text: runs(b, { fontSize: 14, fontFace: FT, color: C.ink }), options: {} },
    { text: runs(c, { fontSize: 14, fontFace: FT, color: C.ink }), options: {} },
    { text: runs(d, { fontSize: 14, fontFace: FT, color: C.ink }), options: {} }];
  s.addTable([
    [H("步驟"), H("做什麼"), H("傳遞（P_i = 150 t、M_d）"), H("使用（P_e = 120 t、M_T）")],
    R("0 斷面", "A、I、y_t、y_b → S_t、S_b、e", "A = 3,200、S = 42,667", "同左", "6D4BC2"),
    R("1 純數值", "P/A、P·e/S、M/S（先不寫正負）", `${f3(N.T1)}、${f3(N.T2)}、${f3(N.T3)}`, `${f3(N.U1)}、${f3(N.U2)}、${f3(N.U3)}`, "B7791F"),
    R("2 定符號", "頂：+ − +　底：+ + −（鋼腱在形心下方）", "上拱 vs 下垂", "同左", "6D4BC2"),
    R("3 加減", "頂、底各加一次", `頂 ${sgn(N.FT_I)}　底 ${sgn(N.FB_I)}`, `頂 ${sgn(N.FT_S)}　底 ${sgn(N.FB_S)}`, "2E7D6B"),
    R("4 讀結果", "哪一緣受拉？哪一緣壓最大？", "頂小拉、底大壓", "頂大壓、底受拉", "C0392B"),
  ], { x: 0.6, y: 1.5, w: 12.1, colW: [1.7, 4.2, 3.1, 3.1], rowH: 0.72, border: { type: "solid", color: "D5DAE1", pt: 1 },
       fill: { color: C.white }, valign: "middle", margin: 0.08 });
  T(s, "單位 kgf/cm²；壓為正、拉為負。拿到結果後的「合不合格」是拼圖二的工作：傳遞比 f′_{ci} 的容許值、使用比 f′_c 的容許值", 0.6, 6.4, 12.1, 0.5, { fontSize: 13, color: C.muted });
  pageNo(s, pg);
}
// ───── 19 回顧 ─────
{
  const s = pres.addSlide(); s.background = { color: C.dark };
  T(s, "重點回顧：三項、三步、一句話", 0.8, 0.7, 11, 0.8, { fontSize: 34, bold: true, color: C.white });
  const pts = [
    ["①", "P/A：預力移到形心推梁，矩形分佈，永遠是壓（＋）", "8FA8F0"],
    ["②", "P·e/S：搬回形心補的力偶，鋼腱在下方 → 上拱 → 頂拉底壓", "F2A65A"],
    ["③", "M/S：載重把梁壓下來 → 下垂 → 頂壓底拉，恰與 ② 反向", "F08A7E"],
    ["S", "頂除 S_t、底除 S_b；對稱斷面才相等，零點永遠在形心", "A58BE6"],
    ["✓", `三步 SOP：算純數字 → 看變形定符號 → 加減（示範梁 ${sgn(N.FT_I)} ／ ${sgn(N.FB_I)}）`, "7FC8B4"],
  ];
  pts.forEach(([n, t, col], i) => {
    const y = 1.8 + i * 0.9;
    s.addShape(pres.shapes.OVAL, { x: 0.8, y, w: 0.58, h: 0.58, fill: { color: col }, line: { color: col } });
    T(s, n, 0.8, y, 0.58, 0.58, { fontSize: 19, bold: true, color: C.dark, align: "center", valign: "middle" });
    T(s, runs(t, { color: C.white, fontSize: 17 }), 1.6, y - 0.1, 11.2, 0.78, { valign: "middle" });
  });
  T(s, "下一步：拼圖二——同一條式子放進「傳遞／使用 × 頂／底」四個控制點，逐點比對容許應力", 0.8, 6.45, 11.8, 0.45, { fontSize: 16, bold: true, color: "F2A65A" });
}
pres.writeFile({ fileName: "RC-U4-1_三項應力的加減.pptx" }).then(() => console.log("written"));
