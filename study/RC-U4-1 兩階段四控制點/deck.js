const pptxgen = require("pptxgenjs");
const fs = require("fs");
const N = JSON.parse(fs.readFileSync("nums.json", "utf8"));
const MJ = JSON.parse(fs.readFileSync("figs/math.json", "utf8"));
const pres = new pptxgen(); pres.layout = "LAYOUT_WIDE"; pres.title = "RC-U4-1 拼圖二：兩階段 × 四控制點";
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
// ───── 1 封面 ─────
{
  const s = pres.addSlide(); s.background = { color: C.dark };
  T(s, "RC-U4-1　預力梁斷面應力分析｜觀念講義・拼圖二", 0.8, 1.2, 11.5, 0.4, { fontSize: 16, color: "9FB3C8", bold: true });
  T(s, "兩階段 × 四控制點", 0.8, 1.8, 11.8, 1.0, { fontSize: 46, bold: true, color: C.white });
  T(s, "預力一路變小、載重一路變大——只要抓住時間軸上的兩個極端時刻，代公式就不會把數據拿錯", 0.8, 2.95, 11.8, 0.9, { fontSize: 21, color: "D6DEE8" });
  const dots = [["①", "傳遞 · 頂拉", "F08A7E"], ["②", "傳遞 · 底壓", "8FA8F0"], ["③", "使用 · 頂壓", "8FA8F0"], ["④", "使用 · 底拉", "F08A7E"]];
  dots.forEach(([n, lab, col], i) => {
    const x = 0.8 + i * 3.0;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 4.3, w: 2.75, h: 0.85, fill: { color: "243044" }, line: { color: col, width: 2 }, rectRadius: 0.1 });
    T(s, n, x + 0.15, 4.3, 0.55, 0.85, { valign: "middle", bold: true, color: col, fontSize: 24 });
    T(s, lab, x + 0.7, 4.3, 2.0, 0.85, { valign: "middle", color: C.white, bold: true, fontSize: 15 });
  });
  T(s, "示範梁與拼圖一相同：40×80 cm 矩形、L = 12 m、e = 25 cm、P_i = 150 t、P_e = 120 t、f′_{ci} = 280、f′_c = 350 kgf/cm²；圖上數字全部由同一支程式算出",
    0.8, 6.2, 11.8, 0.6, { fontSize: 14, color: "9FB3C8" });
}
// ───── 2 總覽 ─────
figSlide("TOPIC MAP · 一句話貫通", "兩個反向趨勢 → 兩個極端時刻 → 四個控制點", "fig01_map", [
  cell("本拼圖的定位", ["拼圖一教你把「某一刻、某一纖維」的應力算對；拼圖二決定「哪兩刻、哪兩纖維」要算，並拿去比容許應力。"], PU),
], C.le, 4.6);
// ───── 3 銜接拼圖一 ─────
{
  const s = newSlide();
  header(s, "承接拼圖一 · 示範梁", "同一根梁、同一條式子，這次要放進時間軸", C.le);
  panel(s, 0.6, 1.5, 5.9, 5.4, C.panel);
  T(s, paras([
    { t: "示範梁資料", o: { bold: true, fontSize: 17, color: C.le } },
    { t: "斷面 40×80 cm：A = 3,200 cm²、S_t = S_b = 42,667 cm³", o: { fontSize: 15 } },
    { t: "簡支 L = 12 m；直線鋼腱 e = 25 cm（形心下方）", o: { fontSize: 15 } },
    { t: `預力：P_i = 150 t → P_e = 120 t（有效比 R = ${f2(N.R)}）`, o: { fontSize: 15 } },
    { t: `自重 w_d = ${f3(N.WD)} t/m → M_d = ${f3(N.MD)} t-m`, o: { fontSize: 15 } },
    { t: `活載 w_L = 2.5 t/m → M_L = ${f2(N.ML)} t-m；M_T = ${f3(N.MT)} t-m`, o: { fontSize: 15 } },
    { t: `強度：放張 f′_{ci} = 280、28 天 f′_c = 350 kgf/cm²`, o: { fontSize: 15 } },
  ]), 0.85, 1.65, 5.5, 5.1, { paraSpaceAfter: 10 });
  panel(s, 6.65, 1.5, 6.05, 2.55, C.okbg, "9CC7BC");
  T(s, paras([{ t: "拼圖一已經給了你", o: { bold: true, fontSize: 17, color: C.ok } },
    { t: `傳遞：頂 ${s2(N.F1)}、底 ${s2(N.F2)}`, o: { fontSize: 16 } },
    { t: `使用：頂 ${s2(N.F3)}、底 ${s2(N.F4)}（kgf/cm²）`, o: { fontSize: 16 } }]), 6.9, 1.65, 5.6, 2.3, { paraSpaceAfter: 8 });
  panel(s, 6.65, 4.2, 6.05, 2.7, C.goldbg, "E6CFA0");
  T(s, paras([{ t: "拼圖二要回答的三件事", o: { bold: true, fontSize: 17, color: C.gold } },
    { t: "1. 為什麼只算這兩個時刻？", o: { fontSize: 16 } },
    { t: "2. 每個時刻該配哪一組 P、M、容許值？", o: { fontSize: 16 } },
    { t: "3. 四個數字都過了，代表什麼？沒過怎麼改？", o: { fontSize: 16 } }]), 6.9, 4.35, 5.6, 2.45, { paraSpaceAfter: 8 });
  pageNo(s, pg);
}
// ───── 4 時間軸 ─────
figSlide("底層邏輯 · 時間軸", "梁的一生裡有三條曲線同時在變：P 往下、M 往上、強度往上", "fig02_timeline", [
  cell("預力一路變小", ["彈性縮短、潛變、乾縮、鬆弛陸續吃掉預力；本例損失 20%"], OR),
  cell("載重一路變大", ["放張當下只有自重；樓版、裝修、活載要到使用階段才全部上來"], RD),
  cell("強度一路變大", ["放張時只有 f′_{ci}（本例 280），28 天後才到 f′_c = 350——容許值也跟著變"], BL),
], C.le, 4.3);
// ───── 5 應力路徑 ─────
figSlide("為什麼只挑兩個時刻", "把應力沿時間畫出來：極值一定落在兩端", "fig03_paths", [
  cell("頂纖維一路往壓走", [`${s2(N.F1)} → ${s2(N.B1)} → ${s2(N.F3)}：最拉在開頭（①）、最壓在結尾（③）`], PU),
  cell("底纖維一路往拉走", [`${s2(N.F2)} → ${s2(N.B2)} → ${s2(N.F4)}：最壓在開頭（②）、最拉在結尾（④）`], OR),
  cell("中間狀態不必算", ["P 單調變小、M 單調變大 → 應力單調變化 → 兩端包住中間所有時刻"], GN),
], C.le, 4.3);
// ───── 6 傳遞物理 ─────
figSlide("極端一 · 傳遞階段 Transfer", "剛放張：預力最大、載重最小、混凝土最嫩", "fig04_transfer", [
  cell("為什麼頂纖維最危險", ["預力力偶 P_i·e 把梁往上頂，自重又最小、抵銷不了 → 凸面在頂 → 頂纖維被拉開"], RD),
  cell("底纖維也要看", ["同一時刻底纖維被 P/A 和 P·e/S 疊加壓得最緊，而 f′_{ci} 還沒長大 → 可能壓碎"], BL),
], C.tot, 4.4);
// ───── 7 使用物理 ─────
figSlide("極端二 · 使用階段 Service", "長期後：預力已衰減、載重全上、混凝土已達設計強度", "fig05_service", [
  cell("為什麼底纖維最危險", ["M_T 把梁往下壓，而原本「存」在底纖維的預壓力又已損失 20% → 凸面在底 → 底纖維被拉開"], RD),
  cell("頂纖維也要看", ["M_T/S 在頂纖維全是壓，P_e·e/S 又變小、幫不上忙 → 頂纖維壓應力最大"], BL),
], C.ps, 4.4);
// ───── 8 四控制點矩陣 ─────
figSlide("四個控制點", "兩個時刻 × 兩個纖維 = 四個檢核點，關係是「且」", "fig06_matrix", [
  cell("每一格的敵人不同", ["①④ 怕拉裂：比 √f′ 的容許拉；②③ 怕壓碎：比 0.60 f′ 的容許壓"], PU),
  cell("任何一格超限就是不合格", ["四點全部通過才算合格；不能因為「主要控制點」過了就跳過其他三點"], RD),
], C.le, 4.5);
// ───── 9 兩階段對照表 ─────
{
  const s = newSlide();
  header(s, "兩階段數據嚴格獨立", "每個時刻都有自己的 P、自己的 M、自己的 f′", C.le);
  const H = t => ({ text: runs(t, { bold: true, color: C.white, fontSize: 15, fontFace: FT }), options: { fill: { color: C.dark } } });
  const L = (t, col) => ({ text: runs(t, { bold: true, color: col || C.ink, fontSize: 16, fontFace: FT }), options: {} });
  const V = (t, col) => ({ text: runs(t, { color: col || C.ink, fontSize: 16, fontFace: FT }), options: {} });
  s.addTable([
    [H("項目"), H("傳遞階段（Transfer）"), H("使用階段（Service）")],
    [L("預力"), V("P_i = 150 t（初始，未扣損失）", "C2570C"), V("P_e = 120 t（有效，已扣損失）", "C2570C")],
    [L("彎矩"), V(`M_d = ${f3(N.MD)} t-m（僅自重）`, C.ps), V(`M_T = M_d + M_L = ${f3(N.MT)} t-m`, C.ps)],
    [L("混凝土強度"), V("f′_{ci} = 280（放張齡期）", "2C6E9E"), V("f′_c = 350（28 天）", "2C6E9E")],
    [L("容許壓應力"), V(`+f_{ci} = +0.60 f′_{ci} = +${f0(N.FCI_A)}`, C.tot), V(`+f_{cs} = +0.60 f′_c = +${f0(N.FCS_A)}`, C.tot)],
    [L("容許拉應力"), V(`−f_{ti} = −0.80√f′_{ci} = −${f2(N.FTI_A)}`, C.ps), V(`−f_{ts} = −2.0√f′_c = −${f2(N.FTS_A)}`, C.ps)],
    [L("檢核點"), V("① 頂（拉）、② 底（壓）"), V("③ 頂（壓）、④ 底（拉）")],
  ], { x: 0.6, y: 1.5, w: 12.1, colW: [2.4, 4.85, 4.85], rowH: 0.62, border: { type: "solid", color: "D5DAE1", pt: 1 },
       fill: { color: C.white }, valign: "middle", margin: 0.1 });
  panel(s, 0.6, 6.05, 12.1, 0.9, C.psbg, "EBB4AE");
  T(s, paras([{ t: "口訣：同一欄的東西一起用，絕不跨欄", o: { bold: true, fontSize: 16, color: C.ps } },
    { t: "最常見的錯：把 P_e 代進傳遞階段、或拿 f′_c 算傳遞的容許值——兩者都會讓結果看起來「比較安全」", o: { fontSize: 14 } }]),
    0.85, 6.1, 11.7, 0.8);
  pageNo(s, pg);
}
// ───── 10 容許應力細節 ─────
{
  const s = newSlide();
  header(s, "容許應力 · 規範值與適用條件", "同一階段也有例外：端部放寬、持續載重收緊", C.ok);
  const cards = [
    ["傳遞 · 壓", `一般斷面 0.60 f′_{ci} = ${f0(N.FCI_A)}`, `簡支構材端部 0.70 f′_{ci} = ${f0(N.FCI_END)}`, BL],
    ["傳遞 · 拉", `一般斷面 0.80√f′_{ci} = ${f2(N.FTI_A)}`, `簡支構材端部 1.6√f′_{ci} = ${f2(N.FTI_END)}；超過要配輔助鋼筋`, RD],
    ["使用 · 壓", `全部載重 0.60 f′_c = ${f0(N.FCS_A)}`, `持續載重（預力＋持續荷重）0.45 f′_c = ${f1(N.FCS45)}`, BL],
    ["使用 · 拉", `未開裂（Class U）上限 2.0√f′_c = ${f2(N.FTS_A)}`, "超過即進入 Class T／C，要改用開裂斷面檢核撓度與裂縫", RD],
  ];
  cards.forEach(([hd, a, b, P], i) => {
    const x = 0.6 + (i % 2) * 6.1, y = 1.5 + Math.floor(i / 2) * 2.15;
    panel(s, x, y, 6.0, 2.0, P[1], P[2]);
    T(s, paras([{ t: hd, o: { bold: true, fontSize: 17, color: P[0] } }, { t: a, o: { fontSize: 16, bold: true } }, { t: b, o: { fontSize: 14, color: C.muted } }]),
      x + 0.25, y + 0.15, 5.55, 1.75, { paraSpaceAfter: 8 });
  });
  panel(s, 0.6, 5.9, 12.1, 1.05, C.goldbg, "E6CFA0");
  T(s, paras([{ t: "考場讀題", o: { bold: true, fontSize: 15, color: C.gold } },
    { t: "題目若直接給容許值就照用；沒給時，本講義用「一般斷面、全部載重、Class U」這組最常考的值（與示範梁四張卡片一致）", o: { fontSize: 14 } }]), 0.85, 5.97, 11.7, 0.95);
  pageNo(s, pg);
}
// ───── 11 單位 ─────
{
  const s = figSlide("ACI 單位制地雷", "MPa 制的 0.25、0.62 不能直接搬到 kgf/cm² 題目", "fig07_units", [], C.ps, 4.35);
  eqPanel(s, 0.6, 5.9, 12.1, 1.15, "推導：只有開根號的項需要把 √10.197 吸進係數", "m_conv", ...GD);
}
// ───── 12 Step 1 ─────
{
  const s = newSlide();
  header(s, "代公式 SOP · Step 1", "兩個階段各算三項純數值，兩排數字分開寫", C.gold);
  eqPanel(s, 0.6, 1.5, 12.1, 1.45, "傳遞三項（P_i、M_d）　單位 kgf/cm²", "m_t3", ...BL);
  eqPanel(s, 0.6, 3.1, 12.1, 1.45, "使用三項（P_e、M_T）　單位 kgf/cm²", "m_u3", ...RD);
  const cards = [
    ["P/A、P·e/S 按 P 的比例縮", `P_e/P_i = ${f2(N.R)} → ${f3(N.T1)}×0.8 = ${f3(N.U1)}、${f3(N.T2)}×0.8 = ${f3(N.U2)}；可拿來驗算`, OR],
    ["M/S 用的是不同的 M", `傳遞只有 M_d → ${f3(N.T3)}；使用是 M_T → ${f3(N.U3)}，差了 ${f1(N.U3 / N.T3)} 倍`, RD],
  ];
  cards.forEach(([hd, b, P], i) => {
    const x = 0.6 + i * 6.1;
    panel(s, x, 4.75, 6.0, 2.2, P[1], P[2]);
    T(s, paras([{ t: hd, o: { bold: true, fontSize: 17, color: P[0] } }, { t: b, o: { fontSize: 15 } }]), x + 0.22, 4.9, 5.6, 1.95, { paraSpaceAfter: 8 });
  });
  pageNo(s, pg);
}
// ───── 13 Step 2 ─────
{
  const s = newSlide();
  header(s, "代公式 SOP · Step 2", "正負號由變形決定，兩階段用同一組通式", C.le);
  eqPanel(s, 0.6, 1.5, 6.0, 1.8, "頂纖維通式", "m_top", ...RD);
  eqPanel(s, 6.7, 1.5, 6.0, 1.8, "底纖維通式", "m_bot", ...BL);
  const cards = [
    ["P/A 永遠 ＋", "預力對混凝土只會推，不分頂底、不分階段", BL],
    ["P·e/S：頂 −、底 ＋", "鋼腱在形心下方 → 上拱 → 頂拉底壓", OR],
    ["M/S：頂 ＋、底 −", "正彎矩（載重向下）→ 下垂 → 頂壓底拉", RD],
  ];
  cards.forEach(([hd, b, P], i) => {
    const x = 0.6 + i * 4.07;
    panel(s, x, 3.5, 3.95, 1.9, P[1], P[2]);
    T(s, paras([{ t: hd, o: { bold: true, fontSize: 17, color: P[0] } }, { t: b, o: { fontSize: 15 } }]), x + 0.22, 3.65, 3.55, 1.65, { paraSpaceAfter: 8 });
  });
  panel(s, 0.6, 5.6, 12.1, 1.35, C.purbg, "C9BCEB");
  T(s, paras([{ t: "約定：壓為 ＋、拉為 −；檢核寫成不等式", o: { bold: true, fontSize: 16, color: C.le } },
    { t: "壓應力檢核 f ≤ +f_c（不能太壓）；拉應力檢核 f ≥ −f_t（不能比容許拉更負）。不等號方向由「數線」決定，不必背", o: { fontSize: 15 } }]),
    0.85, 5.7, 11.7, 1.2, { paraSpaceAfter: 6 });
  pageNo(s, pg);
}
// ───── 14 傳遞檢核 ─────
{
  const s = figSlide("Step 3 · 傳遞階段 ①②", "頂纖維小拉、底纖維大壓，兩者都在容許範圍內", "fig08_checkT", [], C.tot, 4.35);
  eqPanel(s, 0.6, 5.9, 6.0, 1.15, "① 頂纖維（拉裂控制點）", "m_f1", ...RD);
  eqPanel(s, 6.7, 5.9, 6.0, 1.15, "② 底纖維（壓應力檢核）", "m_f2", ...BL);
}
// ───── 15 使用檢核 ─────
{
  const s = figSlide("Step 3 · 使用階段 ③④", "角色對調：頂纖維大壓、底纖維受拉", "fig09_checkS", [], C.ps, 4.35);
  eqPanel(s, 0.6, 5.9, 6.0, 1.15, "③ 頂纖維（壓應力檢核）", "m_f3", ...BL);
  eqPanel(s, 6.7, 5.9, 6.0, 1.15, "④ 底纖維（拉裂控制點）", "m_f4", ...RD);
}
// ───── 16 容許窗 ─────
figSlide("另一種看法 · 容許窗", "把容許應力畫成一扇窗：四個點都要落在窗內", "fig10_window", [
  cell("傳遞的窗較窄", [`f′_{ci} 還小：窗從 −${f2(N.FTI_A)} 到 +${f0(N.FCI_A)}`], BL),
  cell("使用的窗較寬", [`f′_c 長大：窗從 −${f2(N.FTS_A)} 到 +${f0(N.FCS_A)}`], RD),
  cell("拉側最先頂到邊", ["拉側寬度只有壓側的 1/6～1/13 → 大多數題目由 ① 或 ④ 控制"], GN),
], C.ok, 4.5);
// ───── 17 串料 ─────
figSlide("絕對不串料", "P 與 M 的四種配法，只有兩種是真的要檢核", "fig11_mix", [
  cell("把 P_i 帶進使用階段", [`底纖維只剩 ${s2(N.X2)}，看不出 ④ 其實已用掉 ${pct(N.UT[3])}——少算 ${f2(N.X2 - N.F4)}`], RD),
  cell("把 P_e 帶進傳遞階段", [`頂纖維變成 ${s2(N.B1)}，① 的拉應力幾乎消失——實際是 ${s2(N.F1)}`], OR),
], C.ps, 4.55);
// ───── 18 使用率 ─────
figSlide("誰在控制？", "把四點都換成「使用率」＝ 算得 ÷ 容許，最高的就是控制點", "fig12_util", [
  cell("本例由 ④ 控制", [`使用階段底纖維拉 ${pct(N.UT[3])} 最高：要加活載，先撞到的是 ④`], RD),
  cell("① 是第二名", [`${pct(N.UT[0])}：如果想加大 e 或 P 來救 ④，① 會立刻變緊`], OR),
  cell("②③ 餘裕大", [`${pct(N.UT[1])}、${pct(N.UT[2])}：壓應力很少控制，但仍要寫出來`], BL),
], C.ok, 4.1);
// ───── 19 SOP 流程 ─────
figSlide("考場 SOP · 一張流程圖", "切時刻 → 寫四格 → 三項 → 加減 → 比容許", "fig16_sop", [
  cell("「四格」是什麼", ["每個時刻先寫：用哪個斷面、哪個 P、哪個 M、哪組容許值。四格填好，錯誤就不會發生在代數裡"], PU),
  cell("組合梁也一樣", ["時刻變多（張拉、灌漿、澆版、硬化、使用），每刻的斷面不同；但每一刻的做法跟本頁完全相同"], GD),
], C.le, 4.35);
// ───── 20 旋鈕 ─────
figSlide("沒過怎麼改", "四個旋鈕對四個控制點的影響方向", "fig13_knobs", [
  cell("預力的兩難", ["P 與 e 讓梁上拱：幫使用階段、害傳遞階段。設計就是在 ① 與 ④ 之間找平衡"], RD),
  cell("晚一點放張", ["等 f′_{ci} 長大：只放寬 ①② 的窗，對使用階段沒有影響"], BL),
], C.le, 4.45);
// ───── 21 e 可行區 ─────
{
  const s = figSlide("反算 ① · 鋼腱可行區", "把四個檢核式改寫成 e 的不等式，交集就是可行區", "fig14_ezone", [], C.le, 4.35);
  eqPanel(s, 0.6, 5.9, 6.0, 1.15, "① 給上限（傳遞頂拉）", "m_e1", ...RD);
  eqPanel(s, 6.7, 5.9, 6.0, 1.15, "④ 給下限（使用底拉）", "m_e4", ...RD);
}
// ───── 22 最大活載 ─────
{
  const s = figSlide("反算 ② · 最大活載", "未知數換成 M_T：③④ 各給一個上限，取小者", "fig15_wL", [], C.le, 4.35);
  eqPanel(s, 0.6, 5.9, 6.6, 1.15, "④ 控制（剛好等於開裂彎矩 M_{cr}）", "m_mt4", ...RD);
  eqPanel(s, 7.3, 5.9, 5.4, 1.15, "換回均布活載", "m_wl", ...PU);
}
// ───── 23 陷阱 ─────
{
  const s = newSlide();
  header(s, "高頻陷阱", "六個讓四控制點「看起來過了」其實沒過的地方", C.ps);
  const cards = [
    ["串料", `P_i 代進使用：④ 由 ${s2(N.F4)} 被算成 ${s2(N.X2)}；錯誤永遠偏不保守`, RD],
    ["傳遞漏了自重", `只算預力：① = ${s2(N.F1_NOMD)}，超過 −${f2(N.FTI_A)} 判成 NG；自重是傳遞階段的幫手`, OR],
    ["單位制", "kgf/cm² 題目用 0.80√f′_{ci}、2.0√f′_c；直接用 MPa 的 0.25、0.62 會把容許拉低估 3.19 倍", GD],
    ["傳遞容許值用錯強度", `誤用 f′_c：容許拉 −${f2(N.FTI_A)} 變 −${f2(N.FTI_WRONG)}、容許壓 ${f0(N.FCI_A)} 變 ${f0(N.FCS_A)}`, BL],
    ["只查跨中", `直線鋼腱在端部 M = 0：① = ${s2(N.FEND_T)} 超過端部容許 −${f2(N.FTI_END)} → 實務要把鋼腱彎起或脫黏`, PU],
    ["不等號方向", "拉應力是負數：−8.62 ≥ −13.39 才是 OK；比絕對值時要把 ≥ 改成 ≤，寫法要一致", GN],
  ];
  cards.forEach(([hd, body, P], i) => {
    const x = 0.6 + (i % 3) * 4.07, y = 1.5 + Math.floor(i / 3) * 2.8;
    panel(s, x, y, 3.95, 2.6, P[1], P[2]);
    T(s, paras([{ t: hd, o: { bold: true, fontSize: 16, color: P[0] } }, { t: body, o: { fontSize: 15 } }]), x + 0.22, y + 0.15, 3.55, 2.35, { paraSpaceAfter: 8 });
  });
  pageNo(s, pg);
}
// ───── 24 速查卡 ─────
{
  const s = newSlide();
  header(s, "考場速查 · 四控制點一張表", "每一列就是一條檢核式；示範梁的答案一併列出", C.ok);
  const H = t => ({ text: runs(t, { bold: true, color: C.white, fontSize: 14, fontFace: FT }), options: { fill: { color: C.dark } } });
  const R = (cells, col) => cells.map((t, i) => ({ text: runs(t, { bold: i === 0, color: i === 0 ? col : C.ink, fontSize: 14, fontFace: FT }), options: {} }));
  s.addTable([
    [H("控制點"), H("P、M"), H("三項組合"), H("示範梁"), H("容許"), H("使用率")],
    R(["① 傳遞 · 頂", "P_i、M_d", "+P/A − P·e/S + M/S", s2(N.F1), `≥ −0.80√f′_{ci} = −${f2(N.FTI_A)}`, pct(N.UT[0])], C.ps),
    R(["② 傳遞 · 底", "P_i、M_d", "+P/A + P·e/S − M/S", s2(N.F2), `≤ +0.60 f′_{ci} = +${f0(N.FCI_A)}`, pct(N.UT[1])], C.tot),
    R(["③ 使用 · 頂", "P_e、M_T", "+P/A − P·e/S + M/S", s2(N.F3), `≤ +0.60 f′_c = +${f0(N.FCS_A)}`, pct(N.UT[2])], C.tot),
    R(["④ 使用 · 底", "P_e、M_T", "+P/A + P·e/S − M/S", s2(N.F4), `≥ −2.0√f′_c = −${f2(N.FTS_A)}`, pct(N.UT[3])], C.ps),
  ], { x: 0.6, y: 1.5, w: 12.1, colW: [1.9, 1.6, 2.9, 1.5, 3.1, 1.1], rowH: 0.72, border: { type: "solid", color: "D5DAE1", pt: 1 },
       fill: { color: C.white }, valign: "middle", margin: 0.08 });
  panel(s, 0.6, 5.3, 5.95, 1.65, C.okbg, "9CC7BC");
  T(s, paras([{ t: "反算 e", o: { bold: true, fontSize: 15, color: C.ok } },
    { t: `① → e ≤ ${f2(N.E1)}；④ → e ≥ ${f2(N.E4)}（本例 e = 25 落在區間內）`, o: { fontSize: 14 } }]), 0.85, 5.4, 5.5, 1.5, { paraSpaceAfter: 6 });
  panel(s, 6.75, 5.3, 5.95, 1.65, C.lebg, "C9BCEB");
  T(s, paras([{ t: "反算活載", o: { bold: true, fontSize: 15, color: C.le } },
    { t: `④ → M_T ≤ ${f2(N.MT4)}；③ → M_T ≤ ${f2(N.MT3)} → w_{L,max} = ${f3(N.WLX)} t/m`, o: { fontSize: 14 } }]), 7.0, 5.4, 5.5, 1.5, { paraSpaceAfter: 6 });
  pageNo(s, pg);
}
// ───── 25 回顧 ─────
{
  const s = pres.addSlide(); s.background = { color: C.dark };
  T(s, "重點回顧：兩個時刻、四個點、一條式子", 0.8, 0.7, 11.5, 0.8, { fontSize: 34, bold: true, color: C.white });
  const pts = [
    ["↘", "預力一路變小、載重一路變大、強度一路變大——應力單調變化，極值落在兩端", "F2A65A"],
    ["T", `傳遞：P_i＋M_d＋f′_{ci}；頂拉 ①（${s2(N.F1)}）、底壓 ②（${s2(N.F2)}）`, "8FA8F0"],
    ["S", `使用：P_e＋M_T＋f′_c；頂壓 ③（${s2(N.F3)}）、底拉 ④（${s2(N.F4)}）`, "F08A7E"],
    ["≠", "兩階段數據絕不串料；kgf/cm² 題目用 0.80√f′_{ci}、2.0√f′_c", "A58BE6"],
    ["✓", `四點是「且」；把不等式改成等式，就能反算 e（${f2(N.E4)}～${f2(N.E1)}）與最大活載`, "7FC8B4"],
  ];
  pts.forEach(([n, t, col], i) => {
    const y = 1.8 + i * 0.9;
    s.addShape(pres.shapes.OVAL, { x: 0.8, y, w: 0.58, h: 0.58, fill: { color: col }, line: { color: col } });
    T(s, n, 0.8, y, 0.58, 0.58, { fontSize: 19, bold: true, color: C.dark, align: "center", valign: "middle" });
    T(s, runs(t, { color: C.white, fontSize: 17 }), 1.6, y - 0.1, 11.2, 0.78, { valign: "middle" });
  });
  T(s, "下一步：拼圖三——開裂彎矩 M_{cr} 與極限強度 φM_n ≥ 1.2 M_{cr}，把使用階段接到極限狀態", 0.8, 6.45, 11.8, 0.45, { fontSize: 16, bold: true, color: "F2A65A" });
}
pres.writeFile({ fileName: "RC-U4-1_兩階段四控制點.pptx" }).then(() => console.log("written"));
