const pptxgen = require("pptxgenjs");
const fs = require("fs");
const N = JSON.parse(fs.readFileSync("nums.json", "utf8"));
const MJ = JSON.parse(fs.readFileSync("figs/math.json", "utf8"));
const pres = new pptxgen(); pres.layout = "LAYOUT_WIDE"; pres.title = "RC-U2-1 拼圖二：三大傳力機制與桁架類比";
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
// ───── 1 封面 ─────
{
  const s = pres.addSlide(); s.background = { color: C.dark };
  T(s, "RC-U2-1　RC 剪力強度分析與設計｜觀念講義・拼圖二", 0.8, 1.2, 11.5, 0.4, { fontSize: 16, color: "9FB3C8", bold: true });
  T(s, "三大傳力機制與桁架類比", 0.8, 1.8, 11.8, 1.0, { fontSize: 46, bold: true, color: C.white });
  T(s, "認錯機制，公式必錯——先看力走哪條路，再把 V_c 與 V_s 的物理分工、V_s 與 s_{max} 的由來「數」出來", 0.8, 2.95, 11.8, 0.9, { fontSize: 21, color: "D6DEE8" });
  const dots = [["B", "桁架類比", "A58BE6"], ["D", "壓拉桿 STM", "8FA8F0"], ["μ", "剪力摩擦", "F2A65A"], ["d/s", "數箍筋", "7FC8B4"]];
  dots.forEach(([n, lab, col], i) => {
    const x = 0.8 + i * 3.0;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 4.3, w: 2.75, h: 0.85, fill: { color: "243044" }, line: { color: col, width: 2 }, rectRadius: 0.1 });
    T(s, runs(n, { bold: true, color: col, fontSize: 22 }), x + 0.15, 4.3, 0.9, 0.85, { valign: "middle" });
    T(s, runs(lab, { color: C.white, bold: true, fontSize: 15 }), x + 1.0, 4.3, 1.7, 0.85, { valign: "middle" });
  });
  T(s, "示範梁（沿用拼圖一）：b_w = 30、h = 60、d = 50 cm，f′c = 280、f_y = 4200 kgf/cm²；另附深梁與施工縫兩個示範，圖上數字全部由同一支程式算出",
    0.8, 6.3, 11.8, 0.4, { fontSize: 14, color: "9FB3C8" });
}
// ───── 2 總覽 ─────
figSlide("TOPIC MAP · 拼圖二", "進公式之前先做兩件事：認機制、懂分工", "fig01_map", [
  cell("這一份要帶走的能力", ["看到題目 30 秒內說出：這是哪一種傳力？V_c、V_s 各在擋什麼？間距和上限為什麼長這樣？"], null),
], C.le, 4.4);
// ───── 3 三機制 ─────
figSlide("第一步 · 同樣叫「剪力」", "三種傳力機制，三套完全不同的公式", "fig02_three", [
  cell("桁架：靠箍筋", ["裂縫出現後，箍筋當豎桿把剪力一格一格往支承傳"], PU),
  cell("STM：靠拱", ["載重與支承之間直接形成混凝土壓桿，縱筋當繫桿"], BL),
  cell("剪力摩擦：靠夾緊", ["介面滑動要先爬過鋸齒，把鋼筋拉長，產生夾緊力"], GD),
], C.le, 4.45);
// ───── 4 B/D ─────
figSlide("第一步 · B 區與 D 區", "擾動約在 1 倍梁深內消散：D 區只存在支承與載重附近", "fig03_bd", [
  cell("B 區（Bernoulli）", ["平截面假設成立 → 斷面法：V_n = V_c + V_s"], PU),
  cell("D 區（Discontinuity）", ["應力在支承、集中載重、開孔附近亂掉；範圍約 h → 用 STM"], GD),
  cell("關鍵判斷", ["兩個 D 區接在一起 = 沒有 B 區可用 → 整段剪跨都是深梁行為"], RD),
], C.org, 4.3);
// ───── 5 a/d ─────
figSlide("第一步 · 判準 a/d", "剪力跨深比一條數線，決定你打開哪個工具箱", "fig04_ad", [
  cell("規範判準（深梁）", ["淨跨 l_n ≤ 4h，或集中載重距支承面 ≤ 2h（約 a/d ≤ 2）→ STM"], BL),
  cell("為什麼 a/d 小反而強", ["拱作用讓力直接斜傳到支承；用 V_c + V_s 算會嚴重低估，還配了一堆沒用的箍筋"], GN),
  cell("反過來更危險", ["把細長梁當深梁用 STM，會高估強度"], RD),
], C.tot, 4.4);
// ───── 6 流程 ─────
figSlide("第一步 · 考場三問", "先看名稱、再看幾何、最後看介面", "fig05_flow", [
  cell("讀題順序有道理", ["名稱最快（出題者已經告訴你）；幾何要算 a/d；介面最容易漏看——施工縫、新舊混凝土、預鑄接合都是剪力摩擦的暗示"], null),
], C.le, 4.8);
// ───── 7 桁架 ─────
figSlide("第二步 · 桁架類比", "把開裂的梁看成桁架：誰拉、誰壓一目了然", "fig06_truss", [
  cell("斜桿為何是壓", ["裂縫把混凝土切成一條條斜向長條，長條之間只能傳壓力"], BL),
  cell("豎桿為何是拉", ["斜壓桿的垂直分量要靠箍筋往上「吊」回上弦，所以箍筋受拉"], RD),
  cell("這就是 V_s", ["V_s = 所有穿過斜裂縫的豎桿（箍筋）拉力的總和"], GN),
], C.tot, 4.4);
// ───── 8 分工表 ─────
{
  const s = newSlide();
  header(s, "第二步 · V_c 與 V_s 的物理分工", "兩個量、兩種物理：V_c 是抗拉的故事，V_s 的天花板是抗壓的故事", C.ok);
  const H = (t) => ({ text: runs(t, { bold: true, color: C.white, fontSize: 15, fontFace: FT }), options: { fill: { color: C.dark } } });
  const R = (a, b, c, cb, cc) => [
    { text: runs(a, { bold: true, color: C.ink, fontSize: 15, fontFace: FT }), options: { fill: { color: C.panel } } },
    { text: runs(b, { fontSize: 15, fontFace: FT, color: cb || C.ink, bold: !!cb }), options: {} },
    { text: runs(c, { fontSize: 15, fontFace: FT, color: cc || C.ink, bold: !!cc }), options: {} }];
  s.addTable([
    [H(""), H("V_c 混凝土剪力強度"), H("V_s 箍筋剪力強度")],
    R("物理意義", "斜裂縫「出現」那一刻的剪力", "裂縫出現「之後」箍筋縫住裂縫的能力"),
    R("材料問題", "抗拉 → ∝ √f′c", "鋼筋降伏 → ∝ A_v f_{yt}", "2E7D6B", "6D4BC2"),
    R("公式", "0.53√f′c b_w d", "A_v f_{yt} d / s"),
    R("上限來自", "無（本身就是試驗下限）", "混凝土斜壓桿壓碎 → V_s ≤ 4V_c", null, "C0392B"),
    R("加大的方法", "加大斷面、提高 f′c（開根號，效益低）", "加密箍筋、加大箍筋（線性，但有天花板）"),
    R("歸零時機", "耐震塑鉸區（兩條件）、大軸拉", "不會歸零（= 0 表示不需箍筋）", "C0392B"),
  ], { x: 0.6, y: 1.5, w: 12.1, colW: [2.1, 5.0, 5.0], rowH: 0.62, border: { type: "solid", color: "D5DAE1", pt: 1 },
       fill: { color: C.white }, valign: "middle", margin: 0.1 });
  panel(s, 0.6, 6.05, 12.1, 0.95, C.goldbg, "E6CFA0");
  T(s, runs(`示範梁：V_c = ${f2n("VC0")} tf；D13 雙肢 s = 15 → V_s = ${f2n("VS15")} tf；天花板 4V_c = ${f2n("VS_MAX")} tf`, { fontSize: 16, bold: true, color: C.gold }),
    0.85, 6.1, 11.6, 0.85, { valign: "middle" });
  pageNo(s, pg);
}
// ───── 9 V_c 來源 ─────
figSlide("第二步 · V_c 到底是誰在撐", "沿斜裂縫切開：混凝土還有三條路，加上短剪跨的拱作用", "fig08_sources", [
  cell("骨材互鎖最大宗", ["裂縫越寬，互鎖越弱：這就是為什麼要用箍筋把裂縫「夾住」"], GN),
  cell("塑鉸區 V_c = 0", ["反覆載重使裂縫貫穿全深、裂面磨平 → 四項一起消失（須 V_E ≥ V_u/2 且 P_u < A_g f′c/20）"], RD),
], C.ok, 4.45);
// ───── 10 V_s ─────
{
  const s = figSlide("第三步 · V_s 是數出來的", "畫一條 45° 裂縫，數它穿過幾支箍筋", "fig09_vs", [], C.ok, 4.3);
  eqPanel(s, 0.6, 5.85, 6.4, 1.2, "推導（n = d/s 支，每支 A_v f_{yt}）", "m_vs", ...GN);
  eqPanel(s, 7.15, 5.85, 5.55, 1.2, "示範梁：D13 雙肢、s = 15 cm", "m_vs15", ...PU);
}
// ───── 11 A_v ─────
figSlide("第三步 · A_v 是「一組」箍筋的總面積", "數裂縫面切到幾根腿，再乘單肢面積", "fig10_av", [
  cell("單位對好", ["A_v（cm²）、f_{yt}（kgf/cm²）、d 與 s（cm）→ V_s 單位 kgf，÷1000 得 tf"], BL),
  cell("加肢比加密有時更好", [`D13 四肢 s = 20 與雙肢 s = 10 的 A_v/s 相同（${f3(N.AV4 / 20)} cm²/cm），但施工空間大得多`], GN),
], C.tot, 4.45);
// ───── 12 s_max ─────
{
  const s = figSlide("第三步 · s_{max} 的由來", "不讓任何一條裂縫「漏網」：拉桿要真的存在", "fig11_smax", [], C.gold, 4.35);
  eqPanel(s, 0.6, 5.9, 12.1, 1.15, "規範間距上限（kgf、cm 制；2V_c = 1.06√f′c b_w d）", "m_smax", ...GD);
}
// ───── 13 斜壓桿 ─────
{
  const s = figSlide("第三步 · 天花板從哪來", "斜壓桿的壓應力 ≈ 2V/(b_w jd)：剪力越大，壓桿越吃緊", "fig07_strut", [], C.ps, 4.3);
  eqPanel(s, 0.6, 5.85, 6.0, 1.2, "由垂直切面的力平衡（θ 為斜桿角）", "m_strut", ...BL);
  eqPanel(s, 6.75, 5.85, 5.95, 1.2, "示範梁 V_{n,max}（jd ≈ 0.9d = 45 cm）", "m_strutd", ...RD);
}
// ───── 14 天花板 ─────
{
  const s = figSlide("第三步 · 天花板：V_s ≤ 4V_c", "箍筋越密 V_n 越大——直到斜壓桿先壓碎", "fig12_ceiling", [], C.ps, 4.3);
  eqPanel(s, 0.6, 5.85, 7.2, 1.2, "上限（用基本式 V_c；兩式等價）", "m_vsmax", ...RD);
  panel(s, 7.95, 5.85, 4.75, 1.2, C.panel);
  T(s, paras([
    { t: "為什麼要封頂", o: { bold: true, fontSize: 14 } },
    { t: "箍筋降伏 = 有預警的韌性破壞；斜壓桿壓碎 = 脆性。上限確保先發生前者", o: { fontSize: 13 } },
  ]), 8.15, 5.93, 4.4, 1.05, { paraSpaceAfter: 3 });
}
// ───── 15 STM 示範 ─────
figSlide("D 區工具箱 · STM 示範", `轉換深梁 a/d = ${f1(N.S_AD)}：力走「一個三角形」`, "fig13_stm", [
  cell("解題順序", ["定節點 → 畫桁架 → 節點平衡求 C、T → 拉桿配筋 → 壓桿與節點應力"], BL),
  cell("為什麼不用 V_c + V_s", ["這裡的剪力是壓桿的垂直分量直接送到支承，箍筋主要是控制裂縫寬度（最少分佈筋）"], GN),
], C.tot, 4.45);
// ───── 16 STM 三件事 ─────
{
  const s = newSlide();
  header(s, "D 區工具箱 · 三件事都要驗", "壓桿、拉桿、節點——強度都寫成 φF_n ≥ F_u", C.tot);
  eqPanel(s, 0.6, 1.5, 12.1, 1.2, "壓桿與節點的有效抗壓強度", "m_fce", ...BL);
  const H = (t) => ({ text: runs(t, { bold: true, color: C.white, fontSize: 14, fontFace: FT }), options: { fill: { color: C.dark } } });
  const R = (a, b, c) => [{ text: runs(a, { fontSize: 14, fontFace: FT, bold: true }), options: {} },
    { text: runs(b, { fontSize: 14, fontFace: FT, color: C.tot, bold: true }), options: { align: "center" } },
    { text: runs(c, { fontSize: 13, fontFace: FT, color: C.muted }), options: {} }];
  s.addTable([[H("壓桿 β_s"), H("值"), H("說明")],
    R("稜柱形（寬度均勻）", "1.00", "如深梁頂部壓力區"),
    R("瓶形，有足夠分佈筋", "0.75", "本例採用"),
    R("瓶形，無分佈筋", "0.60λ", "壓桿中段會劈裂"),
    R("位於受拉構材", "0.40", "")],
    { x: 0.6, y: 2.9, w: 6.0, colW: [2.5, 0.9, 2.6], rowH: 0.5, border: { type: "solid", color: "D5DAE1", pt: 1 }, valign: "middle", margin: 0.08 });
  s.addTable([[H("節點 β_n"), H("值"), H("說明")],
    R("C-C-C（全受壓）", "1.00", "載重點下方"),
    R("C-C-T（錨一根拉桿）", "0.80", "本例支承節點"),
    R("C-T-T", "0.60", "錨兩根以上拉桿")],
    { x: 6.75, y: 2.9, w: 5.95, colW: [2.5, 0.9, 2.55], rowH: 0.5, border: { type: "solid", color: "D5DAE1", pt: 1 }, valign: "middle", margin: 0.08 });
  panel(s, 6.75, 5.0, 5.95, 0.5, C.panel);
  T(s, "拉桿：F_nt = A_s f_y；拉桿鋼筋必須錨定在節點外", 6.95, 5.0, 5.6, 0.5, { fontSize: 13, valign: "middle" });
  panel(s, 0.6, 5.65, 12.1, 1.4, C.dark, C.dark);
  T(s, paras([
    { t: "示範深梁三件事", o: { bold: true, fontSize: 16, color: "F2A65A" } },
    { t: `拉桿 A_s ≥ ${f1(N.SAS)} cm² → 8-D25（${f1(N.SAS_USE)}）；壓桿 f_{ce} = ${f1(N.FCE_S)} → 需寬 ${f1(N.SW_REQ)} cm；支承節點 f_{ce} = ${f1(N.FCE_N)} → 支承板 ≥ ${f1(N.LB_REQ)} cm`, o: { fontSize: 15, color: C.white } },
    { t: "壓桿與拉桿夾角不得小於 25°（本例 41.6°）；深梁另有 V_u ≤ φ(2.65√f′c b_w d) 的斷面上限", o: { fontSize: 13, color: "D6DEE8" } },
  ]), 0.9, 5.72, 11.6, 1.3, { paraSpaceAfter: 5 });
  pageNo(s, pg);
}
// ───── 17 剪力摩擦 ─────
figSlide("滑動面工具箱 · 剪力摩擦", "鋸齒爬坡把介面撐開 → 鋼筋受拉 → 夾緊力 × μ = 抗剪", "fig14_friction", [
  cell("關鍵在「張開」", ["沒有張開就沒有拉長；所以鋼筋一定要跨過介面、兩側都錨定"], GD),
  cell("μ 反映粗糙度", ["一體澆置 1.4 ＞ 打毛 1.0 ＞ 未打毛 0.6：施工縫打毛是在賺 μ"], BL),
], C.gold, 4.45);
// ───── 18 剪力摩擦示範 ─────
{
  const s = newSlide();
  header(s, "滑動面工具箱 · 示範：施工縫", `介面 30 × 60 cm，V_u = ${f0(N.FVU)} tf，f_y = 4200`, C.gold);
  eqPanel(s, 0.6, 1.5, 12.1, 1.3, "強度式與上限（上限另有與 f′c、A_c 相關的條款，依規範查）", "m_sf", ...GD);
  eqPanel(s, 0.6, 2.95, 6.0, 1.45, "① 打毛（μ = 1.0）所需鋼筋", "m_sf_d", ...BL, `→ 10-D16（${f2(10 * 1.986)} cm²）`);
  eqPanel(s, 6.75, 2.95, 5.95, 1.45, "② 檢查上限", "m_sf_cap", ...GN, "上限代表介面混凝土本身會先壓碎／剪壞");
  panel(s, 0.6, 4.6, 12.1, 2.45, C.dark, C.dark);
  T(s, paras([
    { t: "打毛的價值", o: { bold: true, fontSize: 17, color: "F2A65A" } },
    { t: `若施工縫沒打毛（μ = 0.6）：A_{vf} = ${f2n("AVF_N")} cm²，比打毛多 ${f1(N.AVF_UP)}%`, o: { fontSize: 17, color: C.white } },
    { t: "考場提醒：題目只要出現「新舊混凝土」「施工縫」「預鑄接合面」，先想剪力摩擦，不要直接代 V_c + V_s", o: { fontSize: 15, color: "D6DEE8" } },
    { t: "永久淨壓力可視為額外的夾緊力；介面上的淨拉力則要另配鋼筋抵銷", o: { fontSize: 14, color: "9FB3C8" } },
  ]), 0.9, 4.72, 11.5, 2.25, { paraSpaceAfter: 8 });
  pageNo(s, pg);
}
// ───── 19 考場四步 ─────
figSlide("串起來 · 考場四步", "認機制 → 反算 V_s → 查天花板 → 定間距", "fig15_steps", [
  cell("s 取兩者較小", ["強度要求的 s（13.3）與規範 s_{max}（d/4 = 12.5）都要滿足：這題由 s_{max} 控制"], GD),
  cell("實務會取整", ["s = 12.5 cm 施工上可行；若算出 12.8 之類，通常往下取 12 或 12.5"], null),
], C.ok, 4.45);
// ───── 20 V_u 數線 ─────
figSlide("串起來 · V_u 落在哪一區", "所有分界點都是 V_c 的倍數", "fig16_zones", [
  cell("記法", ["½、1、3、5：φV_c 乘上這四個數，就是四個分界點"], PU),
  cell("示範梁", [`V_u = 40 落在 φ3V_c（${f2(0.75 * 3 * N.VC0)}）與 φ5V_c（${f2n("PVN_MAX")}）之間 → s ≤ d/4`], GD),
], C.le, 4.3);
// ───── 21 速查表 ─────
{
  const s = newSlide();
  header(s, "考場速查 · 讀題 → 選工具箱", "看到關鍵字，直接鎖定機制與公式", C.le);
  const H = (t) => ({ text: runs(t, { bold: true, color: C.white, fontSize: 14, fontFace: FT }), options: { fill: { color: C.dark } } });
  const R = (a, b, c, col) => [
    { text: runs(a, { bold: true, color: col, fontSize: 14, fontFace: FT }), options: {} },
    { text: runs(b, { fontSize: 14, fontFace: FT, color: C.ink }), options: {} },
    { text: runs(c, { fontSize: 13, fontFace: FT, color: C.muted }), options: {} }];
  s.addTable([
    [H("題目線索"), H("機制／公式"), H("計算注意")],
    R("一般梁、均佈載重、a/d > 2.5", "桁架類比：V_u ≤ φ(V_c + V_s)", "φ = 0.75；V_s = A_v f_{yt} d/s", "6D4BC2"),
    R("深梁、托架、牛腿、接頭", "STM：壓桿 β_s、拉桿、節點 β_n", "f_{ce} = 0.85βf′c；夾角 ≥ 25°", "2F54C8"),
    R("集中載重距支承 ≤ 2h、l_n ≤ 4h", "STM（D 區連成一片）", "不要算 V_c + V_s", "2F54C8"),
    R("施工縫、新舊混凝土、預鑄接合", "剪力摩擦：V_n = μA_{vf}f_y", "μ：1.4／1.0／0.6；檢查上限", "B7791F"),
    R("V_s ≤ 2V_c", "s ≤ min(d/2, 60 cm)", "2V_c = 1.06√f′c b_w d", "2E7D6B"),
    R("2V_c < V_s ≤ 4V_c", "s ≤ min(d/4, 30 cm)", "高剪力：裂縫密、角度緩", "B7791F"),
    R("V_s > 4V_c", "加大斷面", "箍筋再多也沒用", "C0392B"),
  ], { x: 0.6, y: 1.5, w: 12.1, colW: [3.9, 4.3, 3.9], rowH: 0.64, border: { type: "solid", color: "D5DAE1", pt: 1 },
       fill: { color: C.white }, valign: "middle", margin: 0.08 });
  T(s, "表中 kgf、cm 制", 0.6, 6.85, 12.1, 0.3, { fontSize: 12, color: C.muted, align: "right" });
  pageNo(s, pg);
}
// ───── 22 陷阱 ─────
{
  const s = newSlide();
  header(s, "高頻陷阱", "六個最常掉分的地方", C.ps);
  const cards = [
    ["深梁代 V_c + V_s", "嚴重低估強度、白配一堆箍筋；看到深梁、托架、牛腿先換 STM", BL],
    ["A_v 只算一根", `雙肢箍 A_v = 2 × 單肢；D13 雙肢是 ${f3(N.AV)}，不是 1.267`, RD],
    ["4V_c 的 V_c 用基本式", "上限寫死 2.12√f′c b_w d；軸拉或精算後的 V_c 不能拿來 ×4", PU],
    ["s 只看強度", `強度算出 ${f1(N.S_REQ)} cm 還不夠：V_s > 2V_c 時 s_{max} = d/4 = 12.5 才是答案`, GD],
    ["施工縫當一般梁", "有明確滑動面就用剪力摩擦；μ 依表面處理選，別忘了上限", GD],
    ["超過天花板還加箍筋", "V_s > 4V_c 時加箍筋無效：斜壓桿先碎 → 加大 b_w 或 d", RD],
  ];
  cards.forEach(([hd, body, P], i) => {
    const x = 0.6 + (i % 3) * 4.07, y = 1.5 + Math.floor(i / 3) * 2.8;
    panel(s, x, y, 3.95, 2.6, P[1], P[2]);
    T(s, paras([{ t: hd, o: { bold: true, fontSize: 17, color: P[0] } }, { t: body, o: { fontSize: 15 } }]), x + 0.22, y + 0.15, 3.55, 2.35, { paraSpaceAfter: 8 });
  });
  pageNo(s, pg);
}
// ───── 23 回顧 ─────
{
  const s = pres.addSlide(); s.background = { color: C.dark };
  T(s, "重點回顧：先認路，再數箍筋", 0.8, 0.7, 11, 0.8, { fontSize: 34, bold: true, color: C.white });
  const pts = [
    ["1", "三種傳力：桁架（B 區）、STM（D 區）、剪力摩擦（滑動面）；a/d 與關鍵字決定工具箱", "A58BE6"],
    ["2", "桁架類比：上弦壓、下弦拉、箍筋是受拉豎桿、裂縫間混凝土是受壓斜桿", "8FA8F0"],
    ["3", "V_c = 開裂瞬間的抗拉故事（四個來源）；塑鉸區兩條件成立時歸零", "7FC8B4"],
    ["4", "V_s = (d/s) 支 × A_v f_{yt}；s_{max} = d/2 讓中深度以下的裂縫至少碰到 1 支", "F2A65A"],
    ["5", "天花板 V_s ≤ 4V_c 是抗壓的故事：斜壓桿先碎就是脆性破壞 → 加大斷面", "F08A7E"],
  ];
  pts.forEach(([n, t, col], i) => {
    const y = 1.8 + i * 0.9;
    s.addShape(pres.shapes.OVAL, { x: 0.8, y, w: 0.58, h: 0.58, fill: { color: col }, line: { color: col } });
    T(s, n, 0.8, y, 0.58, 0.58, { fontSize: 19, bold: true, color: C.dark, align: "center", valign: "middle" });
    T(s, runs(t, { color: C.white, fontSize: 17 }), 1.6, y - 0.1, 11.2, 0.78, { valign: "middle" });
  });
  T(s, "下一步：拼圖三——一般梁四道關卡（最少箍筋 → 強度 → 天花板 → 間距），用歷屆考題把流程跑一遍", 0.8, 6.45, 11.8, 0.45, { fontSize: 16, bold: true, color: "F2A65A" });
}
pres.writeFile({ fileName: "RC-U2-1_三大傳力機制與桁架類比.pptx" }).then(() => console.log("written"));
