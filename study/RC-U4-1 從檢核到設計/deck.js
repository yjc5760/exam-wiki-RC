const pptxgen = require("pptxgenjs");
const fs = require("fs");
const N = JSON.parse(fs.readFileSync("nums.json", "utf8"));
const MJ = JSON.parse(fs.readFileSync("figs/math.json", "utf8"));
const pres = new pptxgen(); pres.layout = "LAYOUT_WIDE"; pres.title = "RC-U4-1 拼圖四：從檢核到設計";
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
const TL = [OR[0], OR[1], OR[2]];
// ───── 1 封面 ─────
{
  const s = pres.addSlide(); s.background = { color: C.dark };
  T(s, "RC-U4-1　預力梁斷面應力分析｜觀念講義・拼圖四", 0.8, 1.2, 11.5, 0.4, { fontSize: 16, color: "9FB3C8", bold: true });
  T(s, "從檢核到設計", 0.8, 1.8, 11.8, 1.0, { fontSize: 46, bold: true, color: C.white });
  T(s, "彈性語言講到開裂為止，之後換成力偶語言；把檢核式的「≤」改成「＝」，就能反解出 e、P 與最大活載", 0.8, 2.95, 11.8, 0.9, { fontSize: 21, color: "D6DEE8" });
  const dots = [["①", "開裂彎矩 M_{cr}", "8FA8F0"], ["②", "WSD ↔ LRFD 切換", "F2A65A"], ["③", "鋼腱可行區 Cable Zone", "7FC8B4"], ["④", "反算 w_L、P 與 SOP", "A58BE6"]];
  dots.forEach(([n, lab, col], i) => {
    const x = 0.8 + i * 3.0;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 4.3, w: 2.75, h: 0.85, fill: { color: "243044" }, line: { color: col, width: 2 }, rectRadius: 0.1 });
    T(s, n, x + 0.15, 4.3, 0.55, 0.85, { valign: "middle", bold: true, color: col, fontSize: 24 });
    T(s, runs(lab, { color: C.white, bold: true, fontSize: 15 }), x + 0.7, 4.3, 2.0, 0.85, { valign: "middle" });
  });
  T(s, "示範梁與拼圖一～三相同：40×80、L = 12 m、e = 25 cm、P_i = 150 t、P_e = 120 t；鋼腱 12 股 0.5\" 鋼絞線、有黏結。圖上數字全部由同一支程式算出",
    0.8, 6.2, 11.8, 0.6, { fontSize: 14, color: "9FB3C8" });
}
// ───── 2 總覽 ─────
figSlide("TOPIC MAP · 一句話貫通", "檢核是「算出來比」，設計是「令等號反解」", "fig01_map", [
  cell("本拼圖的定位", ["拼圖一～三都在回答「這根梁合不合格」；拼圖四往兩頭延伸：往上看到開裂與破壞（M_{cr}、φM_n），往回推出設計量（e、P、w_L）"], PU),
], C.le, 4.6);
// ───── 3 承接 ─────
{
  const s = newSlide();
  header(s, "承接拼圖二 · 示範梁", "同一根梁，這次要多問兩個問題：何時裂？何時垮？", C.le);
  panel(s, 0.6, 1.5, 5.9, 5.4, C.panel);
  T(s, paras([
    { t: "示範梁資料", o: { bold: true, fontSize: 17, color: C.le } },
    { t: `40×80：A = 3,200 cm²、S_t = S_b = ${cm(N.S)} cm³`, o: { fontSize: 15 } },
    { t: `e = 25 cm → d_p = ${f0(N.DP)} cm；k_t = k_b = ${f2(N.K)} cm`, o: { fontSize: 15 } },
    { t: `P_i = 150 t → P_e = 120 t（η = 0.80）`, o: { fontSize: 15 } },
    { t: `M_d = ${f3(N.MD)}、M_L = ${f2(N.ML)} → M_T = ${f3(N.MT)} t-m`, o: { fontSize: 15 } },
    { t: `f′_{ci} = 280、f′_c = 350 kgf/cm²`, o: { fontSize: 15 } },
    { t: `A_{ps} = 12 × 0.987 = ${f3(N.APS)} cm²；f_{pu} = 18,600`, o: { fontSize: 15 } },
    { t: `低鬆弛 γ_p = 0.28；有黏結（灌漿）`, o: { fontSize: 15 } },
  ]), 0.85, 1.65, 5.5, 5.1, { paraSpaceAfter: 10 });
  panel(s, 6.65, 1.5, 6.05, 2.55, C.okbg, "9CC7BC");
  T(s, paras([{ t: "拼圖二已經給了你", o: { bold: true, fontSize: 17, color: C.ok } },
    { t: `使用階段底纖維 ${s1(N.BOT[2])} ≥ −${f2(N.FTS_A)}（④ 控制，使用率 80%）`, o: { fontSize: 16 } },
    { t: `e 可行區 ${f2(N.E4)} ～ ${f2(N.E1)} cm`, o: { fontSize: 16 } }]), 6.9, 1.65, 5.6, 2.3, { paraSpaceAfter: 8 });
  panel(s, 6.65, 4.2, 6.05, 2.7, C.goldbg, "E6CFA0");
  T(s, paras([{ t: "拼圖四要回答的三件事", o: { bold: true, fontSize: 17, color: C.gold } },
    { t: "1. 再加多少彎矩，底纖維會裂開？", o: { fontSize: 16 } },
    { t: "2. 裂開以後，梁最多還能扛多少？", o: { fontSize: 16 } },
    { t: "3. 反過來：e、P、w_L 最多能給多少？", o: { fontSize: 16 } }]), 6.9, 4.35, 5.6, 2.45, { paraSpaceAfter: 8 });
  pageNo(s, pg);
}
// ───── 4 彎矩階梯 ─────
figSlide("全局 · 彎矩階梯", "把八個彎矩排在同一把尺上，語言切換點一目了然", "fig02_ladder", [
  cell("M_{cr} 是分水嶺", [`以下：全斷面有效，用 f = P/A ± Pe/S ± M/S；以上：拉側開裂，改用 C、T 力偶`], BL),
  cell("兩個「安全距離」", [`使用：M_{cr} − M_T = ${f2(N.MCR - N.MT)}（離開裂很近）；強度：φM_n − M_u = ${f2(N.PMN - N.MU)}`], TL),
], C.le, 4.6);
// ───── 5 Mcr 四狀態 ─────
figSlide("觀念 ① · 開裂彎矩 M_{cr}", "把底纖維的預壓一路「抵銷」到破裂模數為止", "fig03_mcr4", [
  cell("預力是存款", [`純預力在底纖維存下 ${s1(N.FCE)} 的壓應力；外力彎矩每加一點就提領一點`], BL),
  cell("裂開的定義", [`底纖維拉應力到達 f_r = 2.0√f′_c = ${f2(N.FR)}；對應的總彎矩就是 M_{cr}`], RD),
], C.tot, 4.55);
// ───── 6 Mcr 公式 ─────
{
  const s = newSlide();
  header(s, "M_{cr} 三條式子", "兩條式子就結束，第三條是考場陷阱", C.tot);
  eqPanel(s, 0.6, 1.45, 12.1, 1.2, "① 預力在底纖維造成的壓應力（用 P_e，不是 P_i）", "m_fce", ...BL);
  eqPanel(s, 0.6, 2.8, 5.9, 1.2, "② 破裂模數（用 f′_c）", "m_fr", ...RD);
  eqPanel(s, 6.6, 2.8, 6.1, 1.2, "③ 開裂彎矩（總彎矩）", "m_mcr", ...BL);
  eqPanel(s, 0.6, 4.15, 12.1, 1.2, "陷阱：「尚可再加多少彎矩」→ 扣掉已作用的 M_d", "m_dm", ...OR);
  panel(s, 0.6, 5.5, 12.1, 1.45, C.goldbg, "E6CFA0");
  T(s, paras([{ t: "M_{cr} 是「總」彎矩", o: { bold: true, fontSize: 16, color: C.gold } },
    { t: `S_b(f_{ce} + f_r) 算出的是從 0 開始的總彎矩，已經把自重算在內。題目問「可承受的外加活載彎矩」時，答案是 ${f2(N.DMCR)} 而不是 ${f2(N.MCR)}`, o: { fontSize: 14 } }]),
    0.85, 5.6, 11.7, 1.3, { paraSpaceAfter: 6 });
  pageNo(s, pg);
}
// ───── 7 核心點讀法 ─────
{
  const s = figSlide("M_{cr} 的另一種讀法", "預力對上核心點的力矩＋混凝土自己的抗拉", "fig04_kern", [], C.le, 4.35);
  eqPanel(s, 0.6, 5.9, 12.1, 1.15, "代入本例（k_t = S_b/A = h/6）", "m_mcrk", ...PU);
}
// ───── 8 f_ts = f_r ─────
{
  const s = newSlide();
  header(s, "為什麼 ④ 的上限剛好等於 M_{cr}？", "使用階段容許拉應力 f_{ts} = 2.0√f′_c，和 f_r 同一個數", C.tot);
  const cards = [
    ["Class U（未開裂）", `f_t ≤ 2.0√f′_c = ${f2(N.FTS_A)}\n→ 使用載重下「按定義」不開裂\n→ 反算 M_{T,max} = M_{cr} = ${f2(N.MCR)}`, BL],
    ["Class T（過渡）", "2.0√f′_c < f_t ≤ 3.2√f′_c\n→ 允許微裂，撓度要用有效慣性矩或雙線性法", GD],
    ["Class C（開裂）", "f_t > 3.2√f′_c\n→ 要檢核裂縫寬度與鋼筋應力增量，不再用全斷面應力", RD],
  ];
  cards.forEach(([hd, b, P], i) => {
    const x = 0.6 + i * 4.07;
    panel(s, x, 1.5, 3.95, 3.1, P[1], P[2]);
    T(s, paras([{ t: hd, o: { bold: true, fontSize: 18, color: P[0] } }, ...b.split("\n").map(t => ({ t, o: { fontSize: 15 } }))]), x + 0.22, 1.65, 3.55, 2.85, { paraSpaceAfter: 10 });
  });
  panel(s, 0.6, 4.8, 12.1, 2.15, C.lebg, "C9BCEB");
  T(s, paras([{ t: "連起來看", o: { bold: true, fontSize: 17, color: C.le } },
    { t: `拼圖二的「最大活載」反算 M_T ≤ ${f2(N.MT4)}，與這裡的 M_{cr} 完全相同——不是巧合，而是 Class U 的設計哲學：使用載重下不讓它裂`, o: { fontSize: 16 } },
    { t: `本例 M_T = ${f2(N.MT)}，離開裂只剩 ${f2(N.MCR - N.MT)} t-m，所以 ④ 的使用率高達 80%`, o: { fontSize: 16 } }]),
    0.85, 4.92, 11.7, 1.95, { paraSpaceAfter: 8 });
  pageNo(s, pg);
}
// ───── 9 兩種語言 ─────
figSlide("觀念 ② · 切換語言", "使用階段講「應力」，極限階段講「力偶」", "fig05_lang", [
  cell("WSD：看纖維", ["全斷面有效、未開裂；比的是每條纖維的應力與容許值"], BL),
  cell("LRFD：看力偶", ["拉側混凝土開裂不計；只剩壓力塊 C 與鋼腱 T，比的是彎矩強度"], TL),
  cell("切換時公式整組換掉", ["不要把 P/A、Pe/S 帶進極限強度——那是另一種語言"], RD),
], C.org, 4.4);
// ───── 10 力偶 ─────
figSlide("強度語言的三張圖", "應變 → 應力塊 → 力偶：與 RC 梁同一套，只是鋼筋換成鋼腱", "fig06_block", [
  cell("和 RC 梁的差別", ["鋼腱沒有明顯降伏點，f_{ps} 不是固定的 f_y，要用近似式或應變諧合求"], TL),
  cell("β_1 別忘了修正", [`f′_c = 350 > 280 → β_1 = ${f2(N.B1)}，不是 0.85`], GD),
], C.org, 4.5);
// ───── 11 fps 代數 ─────
{
  const s = newSlide();
  header(s, "極限強度逐步代數", "ρ_p → f_{ps} → a → M_n → ε_t → φM_n", C.org);
  eqPanel(s, 0.6, 1.4, 12.1, 1.05, "① 鋼腱比與 β_1", "m_rho", ...TL);
  eqPanel(s, 0.6, 2.55, 12.1, 1.2, "② 鋼腱極限應力（ACI 近似式；有黏結、f_{pe} ≥ 0.5f_{pu}）", "m_fps", ...TL);
  eqPanel(s, 0.6, 3.85, 6.0, 1.05, "③ 壓力塊深度", "m_a", ...BL);
  eqPanel(s, 6.7, 3.85, 6.0, 1.05, "④ 標稱強度", "m_mn", ...BL);
  eqPanel(s, 0.6, 5.0, 12.1, 0.95, "⑤ 淨拉應變定 φ", "m_et", ...GN);
  eqPanel(s, 0.6, 6.05, 12.1, 0.95, "⑥ 雙重強度檢核", "m_pmn", ...PU);
  pageNo(s, pg);
}
// ───── 12 鋼腱應力 ─────
figSlide("鋼腱的兩個身分", "使用時用一半強度，極限時被拉到接近 f_{pu}", "fig07_strand", [
  cell("T 從 120 t 漲到 201.63 t", [`不是預力變大，而是梁彎到裂開後，鋼腱被迫跟著伸長 → f_{ps} = ${cm(N.FPS)}`], TL),
  cell("P_e 只是起點", ["f_{ps} 近似式裡根本沒有 P_e——只要 f_{pe} ≥ 0.5f_{pu} 就能用"], BL),
], C.org, 4.5);
// ───── 13 有黏結 vs 無黏結 ─────
{
  const s = newSlide();
  header(s, "觀念盲點 · 有黏結 vs 無黏結", "「M_n 與 P_e 無關」只對有黏結鋼腱成立", C.org);
  const H = t => ({ text: runs(t, { bold: true, color: C.white, fontSize: 15, fontFace: FT }), options: { fill: { color: C.dark } } });
  const V = (t, col, b) => ({ text: runs(t, { color: col || C.ink, bold: !!b, fontSize: 15, fontFace: FT }), options: {} });
  s.addTable([
    [H("項目"), H("有黏結（灌漿）"), H("無黏結（油脂＋套管）")],
    [V("應變諧合", C.ink, 1), V("鋼腱與混凝土同應變，裂縫處局部伸長"), V("整根滑動，伸長量平均到全長")],
    [V("f_{ps} 公式", C.ink, 1), V("f_{pu}[1 − (γ_p/β_1)ρ_p f_{pu}/f′_c]", "C2570C"), V("f_{pe} + 700 + f′_c/(100ρ_p)", "C2570C")],
    [V("與 P_e 關係", C.ink, 1), V("幾乎無關", C.ok, 1), V("直接含 f_{pe}", C.ps, 1)],
    [V("本例 f_{ps}", C.ink, 1), V(`${cm(N.FPS)}`, C.tot, 1), V(`${cm(N.FPS_UB)}`, C.ps, 1)],
    [V("本例 M_n", C.ink, 1), V(`${f2(N.MN)} t-m → φM_n ${f2(N.PMN)} OK`, C.ok, 1), V(`${f2(N.MN_UB)} t-m → φM_n ${f2(0.9 * N.MN_UB)} < M_u NG`, C.ps, 1)],
  ], { x: 0.6, y: 1.5, w: 12.1, colW: [2.3, 4.9, 4.9], rowH: 0.56, border: { type: "solid", color: "D5DAE1", pt: 1 },
       fill: { color: C.white }, valign: "middle", margin: 0.1 });
  eqPanel(s, 0.6, 5.1, 12.1, 1.0, "無黏結（L/d_p ≤ 35，單位 kgf/cm²）", "m_ub", ...RD);
  panel(s, 0.6, 6.2, 12.1, 0.8, C.psbg, "EBB4AE");
  T(s, runs("同一根梁，換成無黏結 M_n 少了約 29%：讀題先看「灌漿／無灌漿」再選公式", { fontSize: 15, color: C.ps, bold: true }), 0.85, 6.2, 11.7, 0.8, { valign: "middle" });
  pageNo(s, pg);
}
// ───── 14 P_e 旋鈕 ─────
figSlide("預力決定什麼、不決定什麼", "P_e 管「何時開裂、變形多少」，不管「極限承載力」", "fig08_knob", [
  cell("P_e 從 120 降到 100 t", [`M_{cr}：${f2(N.MCR)} → ${f2(N.MCR_100)}；φM_n：${f2(N.PMN)} 不變`], BL),
  cell("P_e 太大也有事", [`超過 ${N.PE_12.toFixed(1)} t，1.2M_{cr} > φM_n → 不滿足最小強度要求`], PU),
], C.org, 4.55);
// ───── 15 1.2Mcr ─────
figSlide("為什麼要 φM_n ≥ 1.2M_{cr}", "防止「一開裂就斷」的脆性破壞", "fig09_ductile", [
  cell("物理機制", ["開裂瞬間，原本由混凝土承擔的拉力要瞬間轉給鋼腱；鋼腱太少就接不住"], RD),
  cell("NG 的處理", ["加非預力鋼筋 A_s 提高 M_n；或檢討是否預力過大（M_{cr} 太高）"], GN),
], C.ps, 4.55);
// ───── 16 反算矩陣 ─────
figSlide("觀念 ③ · 反算設計的本質", "四個檢核式不變，只是換一個當未知數", "fig10_matrix", [
  cell("口訣", ["「≤ 容許」改成「＝ 容許」→ 解出來的就是設計量的上限或下限"], GN),
  cell("先找控制式", ["拉應力 ①④ 通常控制；壓應力 ②③ 只在高預力或大偏心時才出線"], GD),
], C.ok, 4.7);
// ───── 17 e 四式 ─────
{
  const s = newSlide();
  header(s, "反算 e：四條等式", "傳遞兩式用 P_i、M_d；使用兩式用 P_e、M_T", C.ok);
  eqPanel(s, 0.6, 1.4, 12.1, 1.15, "傳遞・頂拉：−f_{ti} ≤ P_i/A − P_i e/S_t + M_d/S_t（上限，控制）", "m_e1", ...BL);
  eqPanel(s, 0.6, 2.65, 12.1, 1.15, "傳遞・底壓：P_i/A + P_i e/S_b − M_d/S_b ≤ f_{ci}（上限）", "m_e2", ...GD);
  eqPanel(s, 0.6, 3.9, 12.1, 1.15, "使用・頂壓：P_e/A − P_e e/S_t + M_T/S_t ≤ f_{cs}（下限）", "m_e3", ...GD);
  eqPanel(s, 0.6, 5.15, 12.1, 1.15, "使用・底拉：P_e/A + P_e e/S_b − M_T/S_b ≥ −f_{ts}（下限，控制）", "m_e4", ...RD);
  panel(s, 0.6, 6.4, 12.1, 0.6, C.okbg, "9CC7BC");
  T(s, runs(`交集：${f2(N.E4)} ≤ e ≤ ${f2(N.E1)} cm，採用 e = 25 OK；兩個「≤」取小、兩個「≥」取大`, { fontSize: 15, color: C.ok, bold: true }), 0.85, 6.4, 11.7, 0.6, { valign: "middle" });
  pageNo(s, pg);
}
// ───── 18 Cable zone ─────
figSlide("鋼腱可行區 Cable Zone", "把 x 當變數，e 的上下限變成兩條曲線", "fig11_zone", [
  cell("上限來自傳遞", ["e_{max}(x) 隨 M_d(x) 變：跨中有自重幫忙壓住上拱，可以放得深"], BL),
  cell("下限來自使用", ["e_{min}(x) 隨 M_T(x) 變：梁端 M_T = 0，下限為負（可以在形心以上）"], RD),
], C.ok, 4.7);
// ───── 19 梁端 ─────
figSlide("為什麼鋼腱要「彎起來」", "直線鋼腱在跨中合格，在梁端出界", "fig12_ends", [
  cell("出界範圍", ["直線 e = 25 在離梁端約 3.7 m 內超過 e_{max}：傳遞時頂纖維拉裂"], RD),
  cell("考場判斷", ["題目若給直線鋼腱，除了跨中還要檢核梁端（M_d = 0）這個斷面"], GD),
], C.ps, 4.5);
// ───── 20 w_L,max ─────
{
  const s = figSlide("反算最大活載", "底纖維的應力預算：存款扣自重，剩下全給活載", "fig14_budget", [], C.le, 4.3);
  eqPanel(s, 0.6, 5.8, 6.0, 1.2, "④ 等式解 M_T", "m_mtmax", ...RD);
  eqPanel(s, 6.7, 5.8, 6.0, 1.2, "扣自重、換成均布載重", "m_wl", ...PU);
}
// ───── 21 P window ─────
{
  const s = figSlide("反算預力", "P 也可以當未知數：④ 給下限、① 給上限", "fig15_pwin", [], C.le, 4.0);
  eqPanel(s, 0.6, 5.5, 6.0, 1.45, "④ 底拉 → 最小有效預力", "m_pemin", ...RD);
  eqPanel(s, 6.7, 5.5, 6.0, 1.45, "① 頂拉 → 最大初始預力", "m_pimax", ...BL);
}
// ───── 22 Magnel ─────
figSlide("進階 · Magnel 圖", "e 與 P 同時未知時：縱軸取 1/P，四條不等式都變直線", "fig13_magnel", [
  cell("怎麼用", ["畫出四條線 → 找綠色區 → 選最高點（最小 P）或在可用 e 下找最小 P"], GN),
  cell("本例解讀", ["偏心極限約 28.5 cm（再大，① ④ 無交集）；e = 25 時 P_i 可在 139.8～167.4 t 之間"], PU),
], C.le, 4.6);
// ───── 23 SOP ─────
figSlide("考場 SOP", "四步驟：兩步檢核、兩步反算", "fig16_sop", [
  cell("先確認 f_r 與 f_{ts} 用哪個強度", ["M_{cr}、f_{ts} 都用 f′_c；傳遞 f_{ti}、f_{ci} 用 f′_{ci}"], GD),
  cell("答案要回到題目問的量", ["「可再加的活載」要扣 M_d；「w_L」要從 M 換回 t/m"], PU),
], C.ok, 4.6);
// ───── 24 陷阱 ─────
{
  const s = newSlide();
  header(s, "高頻陷阱", "六個讓拼圖四失分的地方", C.ps);
  const cards = [
    ["M_{cr} 用了 P_i", `開裂發生在使用階段，要用 P_e；誤用 P_i 得 ${f2(N.MCR_PI)}，高估 ${f2(N.MCR_PI - N.MCR)}`, RD],
    ["忘了扣 M_d", `「尚可加多少」答 ${f2(N.MCR)} 是錯的，應為 ${f2(N.DMCR)}`, OR],
    ["f_r 用 f′_{ci}", `2.0√280 = ${f2(N.FR_WRONG)}；M_{cr} 變 ${f2(N.MCR_FRW)}`, GD],
    ["β_1 一律 0.85", `f′_c = 350 時 β_1 = ${f2(N.B1)}；影響 f_{ps} 與 c`, BL],
    ["φ 直接取 0.9", `先算 ε_t（本例 ${N.ET.toFixed(5)} ≥ 0.005）才能取 0.90`, PU],
    ["e 上下限串料", "上限（傳遞）用 P_i、M_d；下限（使用）用 P_e、M_T，不能混用", GN],
  ];
  cards.forEach(([hd, body, P], i) => {
    const x = 0.6 + (i % 3) * 4.07, y = 1.5 + Math.floor(i / 3) * 2.8;
    panel(s, x, y, 3.95, 2.6, P[1], P[2]);
    T(s, paras([{ t: hd, o: { bold: true, fontSize: 17, color: P[0] } }, { t: body, o: { fontSize: 15 } }]), x + 0.22, y + 0.15, 3.55, 2.35, { paraSpaceAfter: 8 });
  });
  pageNo(s, pg);
}
// ───── 25 速查 ─────
{
  const s = newSlide();
  header(s, "考場速查 · 本例全部數字", "一張表對完帳：檢核兩列、設計兩列", C.ok);
  const H = t => ({ text: runs(t, { bold: true, color: C.white, fontSize: 14, fontFace: FT }), options: { fill: { color: C.dark } } });
  const R = (cells, col) => cells.map((t, i) => ({ text: runs(t, { bold: i === 0, color: i === 0 ? col : C.ink, fontSize: 14, fontFace: FT }), options: {} }));
  s.addTable([
    [H("項目"), H("公式"), H("本例"), H("判定")],
    R(["開裂 M_{cr}", "S_b(f_{ce} + f_r)", `f_{ce} ${f2(N.FCE)}、f_r ${f2(N.FR)} → ${f2(N.MCR)} t-m`, `再加 ${f2(N.DMCR)}`], C.tot),
    R(["極限 f_{ps}", "f_{pu}[1 − (γ_p/β_1)ρ_p f_{pu}/f′_c]", `ρ_p ${N.RHO.toFixed(5)} → ${cm(N.FPS)}`, `f_{pe}/f_{pu} = ${f3(N.FPE / N.FPU)} ≥ 0.5`], "C2570C"),
    R(["極限 φM_n", "φA_{ps}f_{ps}(d_p − a/2)", `a ${f2(N.AA)}、ε_t ${N.ET.toFixed(4)} → ${f2(N.PMN)}`, `≥ M_u ${f2(N.MU)}、1.2M_{cr} ${f2(N.MCR12)}`], "C2570C"),
    R(["可行區 e", "① 上限、④ 下限", `${f2(N.E4)} ≤ e ≤ ${f2(N.E1)}`, "e = 25 OK"], C.ok),
    R(["梁端 e", "M_d = M_T = 0", `${f2(N.E4_END)} ≤ e ≤ ${f2(N.E1_END)}`, "直線 25 NG"], C.ok),
    R(["最大活載", "8(M_{T,max} − M_d)/L²", `M_{T,max} ${f2(N.MT4)}`, `w_{L,max} = ${f3(N.WLMAX)} t/m`], C.le),
    R(["預力範圍", "④ 下限、① 上限", `${f2(N.PI_MIN)} ≤ P_i ≤ ${f2(N.PI_MAX1)}`, `P_{e,min} = ${f2(N.PE_MIN)}`], C.le),
  ], { x: 0.6, y: 1.45, w: 12.1, colW: [1.8, 3.6, 3.9, 2.8], rowH: 0.6, border: { type: "solid", color: "D5DAE1", pt: 1 },
       fill: { color: C.white }, valign: "middle", margin: 0.08 });
  panel(s, 0.6, 6.45, 12.1, 0.55, C.lebg, "C9BCEB");
  T(s, runs("容許值：f_{ti} = 0.8√f′_{ci} = 13.39（端部 26.77）、f_{ci} = 168、f_{ts} = f_r = 37.42、f_{cs} = 210 kgf/cm²", { fontSize: 14, color: C.le, bold: true }), 0.85, 6.45, 11.7, 0.55, { valign: "middle" });
  pageNo(s, pg);
}
// ───── 26 回顧 ─────
{
  const s = pres.addSlide(); s.background = { color: C.dark };
  T(s, "重點回顧：從檢核到設計", 0.8, 0.7, 11.5, 0.8, { fontSize: 34, bold: true, color: C.white });
  const pts = [
    ["M", `M_{cr} = S_b(f_{ce} + f_r) = ${f2(N.MCR)}：預壓存款 ${f2(N.FCE)} 被提領到 −f_r；問「再加多少」要扣 M_d`, "8FA8F0"],
    ["⇄", "過了 M_{cr} 換語言：WSD 看纖維應力，LRFD 看 C–T 力偶；公式整組換掉", "F2A65A"],
    ["φ", `φM_n = ${f2(N.PMN)} ≥ M_u ${f2(N.MU)} 且 ≥ 1.2M_{cr} ${f2(N.MCR12)}；有黏結時 M_n 幾乎與 P_e 無關`, "F08A7E"],
    ["e", `≤ 改成 ＝：傳遞頂拉壓住 e_{max}、使用底拉撐起 e_{min}；梁端最緊 → 鋼腱要彎起`, "7FC8B4"],
    ["w", `同一組式子可反解 w_{L,max} = ${f3(N.WLMAX)} t/m、P_{e,min} = ${f2(N.PE_MIN)} t；e、P 同時未知用 Magnel 圖`, "A58BE6"],
  ];
  pts.forEach(([n, t, col], i) => {
    const y = 1.8 + i * 0.9;
    s.addShape(pres.shapes.OVAL, { x: 0.8, y, w: 0.58, h: 0.58, fill: { color: col }, line: { color: col } });
    T(s, n, 0.8, y, 0.58, 0.58, { fontSize: 19, bold: true, color: C.dark, align: "center", valign: "middle" });
    T(s, runs(t, { color: C.white, fontSize: 17 }), 1.6, y - 0.1, 11.2, 0.78, { valign: "middle" });
  });
  T(s, "四塊拼圖到此完成：三項應力 → 兩階段四控制點 → 斷面與施工時序 → 從檢核到設計", 0.8, 6.45, 11.8, 0.45, { fontSize: 16, bold: true, color: "F2A65A" });
}
pres.writeFile({ fileName: "RC-U4-1_從檢核到設計.pptx" }).then(() => console.log("written"));
