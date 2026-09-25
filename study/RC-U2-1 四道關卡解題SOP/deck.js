const pptxgen = require("pptxgenjs");
const fs = require("fs");
const N = JSON.parse(fs.readFileSync("nums.json", "utf8"));
const MJ = JSON.parse(fs.readFileSync("figs/math.json", "utf8"));
const pres = new pptxgen(); pres.layout = "LAYOUT_WIDE"; pres.title = "RC-U2-1 拼圖三：四道關卡解題SOP";
const FT = "Noto Sans CJK TC";
const C = { ink: "1F2A37", muted: "6B7280", panel: "F4F6F9", line: "D5DAE1", white: "FFFFFF", dark: "1B2432",
  red: "C0392B", redbg: "FBECEA", redln: "EBB4AE", grn: "1E8449", grnbg: "E6F2EA", grnln: "A7D1B5",
  org: "B9540F", orgbg: "FDF1E7", orgln: "EFC39F", blu: "2F54C8", blubg: "EEF2FB", bluln: "B9C6EA",
  pur: "6D4BC2", purbg: "F1EDFA", purln: "C9BCEB", teal: "2E7D6B" };
const RD = [C.red, C.redbg, C.redln], GN = [C.grn, C.grnbg, C.grnln], OR = [C.org, C.orgbg, C.orgln], BL = [C.blu, C.blubg, C.bluln], PU = [C.pur, C.purbg, C.purln];
const f2 = v => (v + 1e-9).toFixed(2), f1 = v => (v + 1e-9).toFixed(1);
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
  list.forEach((p, i) => { const r = runs(p.t, p.o || {}); if (i < list.length - 1) r[r.length - 1].options.breakLine = true; out.push(...r); });
  return out;
}
function T(s, content, x, y, w, h, o = {}) {
  const base = { fontFace: FT, fontSize: 15, color: C.ink, valign: "top", margin: 0, isTextBox: true };
  const body = typeof content === "string" ? runs(content, { bold: o.bold, color: o.color || C.ink, fontSize: o.fontSize || 15 }) : content;
  s.addText(body, { ...base, ...o, x, y, w, h });
}
function vb(file) { const t = fs.readFileSync(file, "utf8"); const a = t.match(/viewBox="([\d.\s-]+)"/)[1].trim().split(/\s+/).map(Number); return [a[2], a[3]]; }
function img(s, name, x, y, W, H) {
  const f = `figs/${name}.svg`; let [w, h] = MJ[name] || vb(f);
  const k = Math.min(W / w, H / h); const iw = w * k, ih = h * k;
  s.addImage({ path: f, x: x + (W - iw) / 2, y: y + (H - ih) / 2, w: iw, h: ih, altText: name });
}
function eq(s, name, x, y, H, scale = 0.6, align = "left", maxW = 99) {
  const [w, h] = MJ[name]; let iw = w * scale, ih = h * scale;
  if (ih > H) { iw *= H / ih; ih = H; }
  if (iw > maxW) { ih *= maxW / iw; iw = maxW; }
  const ix = align === "center" ? x - iw / 2 : x;
  s.addImage({ path: `figs/${name}.svg`, x: ix, y: y + (H - ih) / 2, w: iw, h: ih, altText: name });
}
function header(s, eyebrow, title, col = C.red) {
  T(s, eyebrow, 0.6, 0.38, 11, 0.3, { fontSize: 12, bold: true, color: col, charSpacing: 2 });
  T(s, title, 0.6, 0.68, 12.2, 0.6, { fontSize: 26, bold: true });
}
function panel(s, x, y, w, h, fill = C.panel, line = C.line) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill: { color: fill }, line: { color: line, width: 1 }, rectRadius: 0.12 });
}
let pg = 1;
function pageNo(s) { T(s, `${pg}`, 12.3, 7.08, 0.5, 0.25, { fontSize: 10, color: "9AA3AE", align: "right" }); }
function newSlide() { const s = pres.addSlide(); s.background = { color: C.white }; pg++; pageNo(s); return s; }
const cell = (hd, body, P) => [hd, body, P];
function cells(s, list, y, h) {
  const n = list.length, gap = 0.15, w = (12.1 - gap * (n - 1)) / n;
  list.forEach(([hd, body, P], i) => {
    const x = 0.6 + i * (w + gap);
    panel(s, x, y, w, h, P ? P[1] : C.panel, P ? P[2] : C.line);
    T(s, paras([{ t: hd, o: { bold: true, fontSize: 14, color: P ? P[0] : C.ink } }, ...body.map(t => ({ t, o: { fontSize: 13 } }))]),
      x + 0.2, y + 0.1, w - 0.35, h - 0.15, { paraSpaceAfter: 3 });
  });
}
function figSlide(eyebrow, title, fig, list, col, figH = 4.45) {
  const s = newSlide(); header(s, eyebrow, title, col);
  img(s, fig, 0.6, 1.4, 12.1, figH);
  if (list && list.length) { const y = 1.5 + figH; cells(s, list, y, 7.0 - y); }
  return s;
}
function eqPanel(s, x, y, w, h, title, names, P, note) {
  panel(s, x, y, w, h, P ? P[1] : C.panel, P ? P[2] : C.line);
  T(s, title, x + 0.2, y + 0.1, w - 0.4, 0.32, { fontSize: 14, bold: true, color: P ? P[0] : C.ink });
  const avail = h - 0.55 - (note ? 0.42 : 0); const eh = avail / names.length;
  names.forEach((n, i) => eq(s, n, x + 0.25, y + 0.47 + i * eh, eh - 0.05, 0.6, "left", w - 0.5));
  if (note) T(s, note, x + 0.2, y + h - 0.42, w - 0.4, 0.34, { fontSize: 12, color: C.muted });
}
function section(no, title, sub, col) {
  const s = pres.addSlide(); pg++; s.background = { color: C.dark };
  s.addShape(pres.shapes.RECTANGLE, { x: 0.8, y: 2.55, w: 0.12, h: 1.9, fill: { color: col }, line: { color: col } });
  T(s, no, 1.15, 2.45, 10, 0.5, { fontSize: 20, bold: true, color: col });
  T(s, title, 1.15, 2.95, 11.5, 0.9, { fontSize: 40, bold: true, color: C.white });
  T(s, sub, 1.15, 3.95, 11.5, 0.6, { fontSize: 18, color: "C9D3DE" });
  T(s, `${pg}`, 12.3, 7.08, 0.5, 0.25, { fontSize: 10, color: "6B7A8C", align: "right" });
}

// ───── 1 封面 ─────
{
  const s = pres.addSlide(); s.background = { color: C.dark };
  T(s, "RC-U2-1　RC 剪力強度分析與設計｜觀念講義・拼圖三", 0.8, 1.2, 11.5, 0.4, { fontSize: 16, color: "9FB3C8", bold: true });
  T(s, "四道關卡：一般梁剪力設計解題 SOP", 0.8, 1.8, 11.8, 1.0, { fontSize: 44, bold: true, color: C.white });
  T(s, "先定 V_u 的位置 → 再選 V_c 的公式 → 再判 V_s 區間檢核斷面 → 最後才算間距 s", 0.8, 2.95, 11.8, 0.5, { fontSize: 20, color: "E6CFA0" });
  const G = [["1", "V_u 取在哪", C.red], ["2", "V_c 用哪張臉", C.blu], ["3", "V_s 落在哪段", C.org], ["4", "s 四取小＋分區", C.grn]];
  G.forEach(([n, t, c], i) => {
    const x = 0.8 + i * 3.0;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 4.1, w: 2.75, h: 1.2, fill: { color: "243044" }, line: { color: c, width: 2 }, rectRadius: 0.1 });
    T(s, `關卡 ${n}`, x + 0.2, 4.22, 2.4, 0.4, { fontSize: 16, bold: true, color: c });
    T(s, t, x + 0.2, 4.65, 2.4, 0.5, { fontSize: 20, bold: true, color: C.white });
  });
  T(s, `示範斷面 35×70（d = 63）、f'_c = 280、D13 雙肢；三個例題貫穿全篇，圖上數字全部可對帳`, 0.8, 5.9, 11.8, 0.4, { fontSize: 15, color: "9FB3C8" });
}
// ───── 2 地圖 ─────
figSlide("TOPIC MAP", "四道關卡：每一關的輸出，就是下一關的輸入", "fig01_map", [
  cell("為什麼要分關", ["每一關只回答一個問題，答錯的後果會一路傳下去：", "V_u 取錯 → V_s 錯 → 區間判錯 → s_{max} 錯"], RD),
  cell("最常見的偷懶順序", ["直接套 s = A_v f_{yt} d / V_s 就交卷", "漏掉 d 偏移前提、V_c 選臉、斷面天花板、A_{v,min}"], OR),
  cell("本篇怎麼讀", ["每關先講物理（為什麼），再講規範式（怎麼算），", "最後用同一組例題代數字"], GN)], C.red, 4.0);
// ───── 3 示範案例 ─────
figSlide("示範案例", "一個斷面、三根梁：全篇數字都從這裡來", "fig02_cases", [
  cell("例①：看 d 偏移『能省多少』", [`w_u = 12、l_n = 7.0 → 支承面 ${f2(N.VU1_F)}，d 處 ${f2(N.VU1_D)}`], GN),
  cell("例②：看 V_c 的『詳細式』", [`ρ_w = ${N.RHO2.toFixed(5)}、V_u d/M_u = 0.90 → V_c = ${f2(N.VC_DET)}`], BL),
  cell("例③：看吊掛『不能省』＋分區配箍", [`w_u = 18、l_n = 7.0 → V_u = ${f2(N.VU3)}，V_s = ${f2(N.VS3)}`], RD)], C.ink, 4.3);

// ═════ 關卡 1 ═════
section("關卡 1", "臨界斷面取在哪裡？", "「距支承面 d 處」不是無條件的優惠——要三個前提同時成立", C.red);
figSlide("關卡 1｜物理", "為什麼可以取距支承面 d 處？", "fig03_crack", [
  cell("裂縫幾何", ["最早的斜裂縫從支承面底部出發，約 45° 上升，水平走 d 才到頂"], PU),
  cell("d 以內的載重", ["沿斜壓桿直接壓進支承，不必跨越任何斜裂縫 → 不需要箍筋去『接』"], PU),
  cell("所以規範說", ["d 以內的斷面，可以用距支承面 d 處的 V_u 設計（同一組箍筋延伸到支承面）"], RD)], C.red);
{
  const s = newSlide(); header(s, "關卡 1｜三個前提", "三個前提要同時成立才准用 d 偏移", C.red);
  img(s, "fig04_prereq", 0.6, 1.35, 12.1, 5.1);
  T(s, paras([{ t: "(a) 支承反力提供端區壓縮　(b) 載重施加在頂面（壓力側）　(c) 臨界斷面內（d 以內）無集中載重", o: { bold: true, fontSize: 15, color: C.red } }]), 0.6, 6.55, 12.1, 0.4, { align: "center" });
}
{
  const s = figSlide("關卡 1｜例①", "例①：頂面均布、支承受壓 → 可以用 d 偏移", "fig05_ex1", [], C.grn, 4.2);
  eqPanel(s, 0.6, 5.75, 5.95, 1.25, "通式（均布載重）", ["m_d"], GN);
  eqPanel(s, 6.75, 5.75, 5.95, 1.25, "代數字", ["m_d1"], GN);
}
figSlide("關卡 1｜例③", "例③：吊掛在大梁側面 → 只能取支承面 63.00", "fig06_ex3", [
  cell("為什麼不能偏移", ["反力從梁側面把梁『吊』起來，端部沒有壓應力，斜裂縫可以直接從支承面長出來"], RD),
  cell("誤用的代價", [`V_u 從 ${f2(N.VU3)} 誤降到 ${f2(N.VU3_D)}，s 從 ${f2(N.S3_REQ)} 放寬成 ${f2(N.S3_D_REQ)} cm`], RD),
  cell("考場判斷順序", ["看支承怎麼支（壓？吊？）→ 看載重加在哪一面 → 看 d 以內有沒有集中載重"], OR)], C.red);

// ═════ 關卡 2 ═════
section("關卡 2", "V_c 的五張臉", "同一個斷面，選錯公式，答案可以差 4 倍", C.blu);
figSlide("關卡 2｜物理", "V_c 是開裂當下，混凝土抵抗主拉應力的能力", "fig07_principal", [
  cell("純剪", ["主拉應力 σ_1 = τ，碰到混凝土抗拉強度就開裂"], [C.teal, C.grnbg, C.grnln]),
  cell("軸壓", ["把莫爾圓往左推，σ_1 變小 → 要更大的剪力才開裂 → V_c ↑；裂縫也變平緩"], BL),
  cell("軸拉", ["把莫爾圓往右推，σ_1 變大 → 提早開裂 → V_c ↓；拉到一定程度 V_c 歸零"], RD)], C.blu);
figSlide("關卡 2｜量級", "五張臉的量級：同一個 35×70 斷面", "fig08_faces", [
  cell("① 簡化式", ["沒提軸力、沒要求精算時的預設值；偏保守"], [C.teal, C.grnbg, C.grnln]),
  cell("② 詳細式", ["ρ_w 越大、V_u d/M_u 越大（剪力大彎矩小）→ V_c 越高"], GN),
  cell("③④ 軸力", ["壓 +17.5%、拉 −70.0%（同為 60 tf）"], BL),
  cell("⑤ 耐震", ["塑鉸區兩條件成立 → 直接令 0"], RD)], C.blu, 4.3);
{
  const s = newSlide(); header(s, "關卡 2｜詳細式", "詳細式：題目給了 ρ_w、V_u、M_u 才用", C.blu);
  eqPanel(s, 0.6, 1.45, 6.0, 1.5, "詳細式", ["m_det"], GN);
  eqPanel(s, 0.6, 3.1, 6.0, 1.35, "兩個限制（必寫）", ["m_detlim"], OR, "V_u d/M_u 算出 > 1 時取 1.0；V_u、M_u 取同一斷面、同一組合");
  eqPanel(s, 0.6, 4.6, 6.0, 1.3, "例②代數字（6-D25、V_u d/M_u = 0.90）", ["m_det2"], GN);
  T(s, paras([{ t: `上限 0.93√f'_c b_w d = ${f2(N.VC_DET_CAP)} tf ⇒ 未超過，取 ${f2(N.VC_DET)}；比簡化式多 ${f1((N.VC_DET / N.VC - 1) * 100)}%`, o: { fontSize: 14, bold: true, color: C.grn } }]), 0.6, 6.1, 6.0, 0.8);
  panel(s, 6.8, 1.45, 5.9, 5.5, C.redbg, C.redln);
  T(s, "陷阱：有軸壓時的詳細式（M_m 版）", 7.0, 1.55, 5.5, 0.35, { fontSize: 15, bold: true, color: C.red });
  eq(s, "m_mm", 7.05, 2.0, 0.8, 0.6, "left", 5.4);
  T(s, paras([{ t: "有軸壓時，詳細式裡的 M_u 要換成 M_m（扣掉軸壓造成的有利彎矩），且 V_u d/M_m 不受 ≤ 1 的限制。", o: { fontSize: 13 } }]), 7.05, 2.9, 5.5, 0.8);
  eq(s, "m_mmcap", 7.05, 3.8, 0.85, 0.6, "left", 5.4);
  T(s, paras([{ t: "M_m ≤ 0 表示斷面幾乎全壓、公式失效：直接取上限式——", o: { fontSize: 13 } },
               { t: "注意上限本身也帶 √(1 + N_u/35A_g) 項，不是單純的 0.93√f'_c b_w d。", o: { fontSize: 13, bold: true, color: C.red } },
               { t: "考試很少考到這一步；看到『M_m』、『軸壓＋詳細計算』才需要。", o: { fontSize: 12, color: C.muted } }]), 7.05, 4.8, 5.5, 2.0, { paraSpaceAfter: 4 });
}
{
  const s = figSlide("關卡 2｜軸力修正", "軸力修正：拉的殺傷力是壓的 4 倍", "fig09_axial", [], C.blu, 3.9);
  eqPanel(s, 0.6, 5.4, 6.0, 1.6, "軸壓（N_u 取正）", ["m_nc", "m_nc2"], BL);
  eqPanel(s, 6.75, 5.4, 5.95, 1.6, "軸拉（N_u 取負；算出負值取 0）", ["m_nt", "m_nt2"], RD);
}
figSlide("關卡 2｜耐震", "耐震特例：塑鉸區直接令 V_c = 0", "fig10_seismic", [
  cell("為什麼", ["反覆載重讓斜裂縫來回張合，骨材咬合與壓力區貢獻都不可靠"], RD),
  cell("觸發條件（兩者同時）", ["地震引致剪力 ≥ ½ 最大設計剪力；且 N_u < A_g f'_c/20"], OR),
  cell("考場提示", ["題目寫『特殊抗彎構架』『塑鉸區』『容量設計剪力』→ 先想到 V_c = 0"], BL)], C.blu);
{
  const s = newSlide(); header(s, "關卡 2｜選臉表", "考場上怎麼選這五張臉", C.blu);
  const H = (t) => ({ text: t, options: { bold: true, color: C.white, fill: { color: "2A3B55" } } });
  const R = (a, b, c, col) => [{ text: runs(a) }, { text: runs(b, { color: col, bold: true }), options: { color: col, bold: true } }, { text: runs(c) }];
  const rows = [[H("情況／題目怎麼說"), H("用哪一式"), H("注意")],
    R("沒提軸力、也沒要求精算", "V_c = 0.53√f'_c b_w d", "最常見；答案偏保守", C.teal),
    R("給了 ρ_w、V_u、M_u，或寫『詳細計算』", "(0.50√f'_c + 175 ρ_w V_u d/M_u) b_w d", "V_u d/M_u ≤ 1；上限 0.93√f'_c b_w d", C.grn),
    R("柱、或梁有明顯軸壓 N_u", "× (1 + N_u / 140A_g)", "N_u 取正；A_g 為全斷面", C.blu),
    R("拉力構材、溫度收縮軸拉", "× (1 + N_u / 35A_g)", "N_u 取負；算出負值取 V_c = 0", C.red),
    R("特殊抗彎構架的塑鉸區", "V_c = 0", "地震剪力 ≥ ½ 且 N_u < A_g f'_c/20", C.red)];
  s.addTable(rows, { x: 0.6, y: 1.5, w: 12.1, colW: [3.8, 4.4, 3.9], fontFace: FT, fontSize: 15, color: C.ink, rowH: 0.7, valign: "middle",
    border: { type: "solid", color: "D5DAE1", pt: 1 }, fill: { color: "FFFFFF" }, margin: 0.1 });
  panel(s, 0.6, 6.0, 12.1, 0.9, C.orgbg, C.orgln);
  T(s, "軸力修正都乘在『簡化式』上；記憶法：怕拉不怕壓——拉的分母 35 比壓的 140 小四倍，傷害大四倍。", 0.85, 6.2, 11.6, 0.5, { fontSize: 16, bold: true, color: C.org });
}

// ═════ 關卡 3 ═════
section("關卡 3", "用 V_c 當尺，量 V_s 落在哪一段", "這一步決定 s_{max}，也決定斷面夠不夠大", C.org);
{
  const s = figSlide("關卡 3｜三個區間", "先算 V_s，再用 2V_c／4V_c 判區間", "fig11_zones", [], C.org, 4.0);
  eqPanel(s, 0.6, 5.5, 4.4, 1.5, "所需箍筋強度", ["m_vs"], OR);
  eqPanel(s, 5.15, 5.5, 7.55, 1.5, "兩條門檻（規範原文寫的是係數，不是『幾倍 V_c』）", ["m_lim"], OR);
}
figSlide("關卡 3｜天花板", "為什麼 4V_c 是天花板？斜壓桿先壓碎", "fig12_ceiling", [
  cell("機制轉換", ["箍筋越密，桁架斜壓桿分到的壓力越大；超過某個程度，混凝土斜壓桿先於箍筋降伏被壓碎"], RD),
  cell("規範的用意", ["V_s ≤ 4V_c 把破壞鎖在『箍筋先降伏』的延性側"], GN),
  cell("超過了怎麼辦", ["只有三條路：加大 b_w、加大 d、提高 f'_c——加箍筋無效"], OR)], C.org);
{
  const s = figSlide("關卡 3｜設計版", "同一句話的設計版：V_u ≤ 5φV_c", "fig13_usage", [], C.org, 3.4);
  eqPanel(s, 0.6, 5.0, 6.0, 1.95, "推導", ["m_vumax", "m_vumax2"], OR);
  panel(s, 6.75, 5.0, 5.95, 1.95, C.grnbg, C.grnln);
  T(s, paras([{ t: "先檢核、再算間距", o: { bold: true, fontSize: 15, color: C.grn } },
    { t: `例③ V_u = 63.00 ≤ ${f2(N.VU_MAX)} ⇒ 使用率 ${f1(N.USE3)}%，斷面剛好夠`, o: { fontSize: 14 } },
    { t: "在算 s 之前先比 V_u 與 5φV_c，超過就直接改斷面，不用白算", o: { fontSize: 14 } }]), 6.95, 5.12, 5.6, 1.75, { paraSpaceAfter: 4 });
}
figSlide("關卡 3｜陷阱", "尺的陷阱：門檻是 1.06√f'_c b_w d，不是『2 × 修正後的 V_c』", "fig14_ruler", [
  cell("規範原文", ["s_{max} 減半：V_s > 1.06√f'_c b_w d；天花板：V_s ≤ 2.12√f'_c b_w d"], OR),
  cell("『2V_c、4V_c』只是口訣", ["只有在 V_c 用簡化式時才剛好等於 2V_c、4V_c"], OR),
  cell("什麼時候會出事", ["軸拉、軸壓、詳細式、耐震 V_c = 0——尺都要回到係數式"], RD)], C.org, 4.3);

// ═════ 關卡 4 ═════
section("關卡 4", "間距四取小，沿梁長分區配箍", "強度需求、s_{max}、A_{v,min}、施工取整——缺一不可", C.grn);
{
  const s = figSlide("關卡 4｜四取小", "間距：四個條件同時算，取最小", "fig15_min4", [], C.grn, 3.9);
  eqPanel(s, 0.6, 5.4, 4.0, 1.6, "① 強度需求", ["m_s"], GN);
  eqPanel(s, 4.75, 5.4, 3.9, 1.6, "例③ A 區", ["m_s3"], RD);
  eqPanel(s, 8.8, 5.4, 3.9, 1.6, "例①（d 處）", ["m_s1"], GN);
}
{
  const s = figSlide("關卡 4｜最小箍筋", "A_{v,min}：V_u > 0.5φV_c 就要配", "fig16_avmin", [], C.grn, 3.9);
  eqPanel(s, 0.6, 5.4, 6.3, 1.6, "兩式取大", ["m_avmin"], GN);
  eqPanel(s, 7.05, 5.4, 5.65, 1.6, "反算間距（本例 3.5 控制）", ["m_savmin"], GN);
}
{
  const s = figSlide("關卡 4｜分區", "把『四取小』沿梁長走一遍：三條判準水平線", "fig17_vudiag", [], C.grn, 4.2);
  cells(s, [
    cell("3φV_c", ["V_s = 2V_c 的界線：以上用 d/4"], RD),
    cell("φV_c", ["以下理論上不需 V_s，只剩 A_{v,min}"], GN),
    cell("0.5φV_c", ["以下規範可免箍筋"], [C.muted, C.panel, C.line])], 5.8, 1.2);
}
{
  const s = newSlide(); header(s, "關卡 4｜配置", "例③ 的分區配箍（半跨；另一半對稱）", C.grn);
  img(s, "fig18_layout", 0.6, 1.3, 12.1, 2.55);
  const H = (t) => ({ text: t, options: { bold: true, color: C.white, fill: { color: "2A3B55" }, align: "center" } });
  const R = (z, r, v, c, u, col) => [{ text: z, options: { bold: true, color: col, align: "center" } }, { text: r, options: { align: "center" } }, { text: v, options: { align: "center" } }, { text: runs(c) }, { text: u, options: { bold: true, color: col, align: "center" } }];
  s.addTable([[H("分區"), H("範圍 (m)"), { text: runs("V_u (tf)", { bold: true, color: "FFFFFF" }), options: { fill: { color: "2A3B55" }, align: "center" } }, H("控制條件"), H("採用")],
    R("A", `0 ~ ${f2(N.XA)}`, `63.00 → ${f2(N.PVC3)}`, `2V_c < V_s ≤ 4V_c ⇒ s_{max} = d/4 = 15.75；強度需求 ${f2(N.S3_REQ)}`, "D13@10", C.red),
    R("B", `${f2(N.XA)} ~ ${f2(N.XB)}`, `${f2(N.PVC3)} → ${f2(N.PVC)}`, `V_s ≤ 2V_c ⇒ s_{max} = d/2 = 31.5；強度需求 ${f2(N.SB_REQ)}`, "D13@15", C.org),
    R("C", `${f2(N.XB)} ~ ${f2(N.XC)}`, `${f2(N.PVC)} → ${f2(N.PVC05)}`, `僅需 A_{v,min}（s ≤ ${f2(N.S_AVMIN)}）與 s_{max} = 31.5`, "D13@30", C.grn),
    R("D", `${f2(N.XC)} ~ 3.50`, `${f2(N.PVC05)} → 0`, "V_u ≤ 0.5φV_c，規範可免箍筋", "仍配 D13@30", C.muted)],
    { x: 0.6, y: 4.0, w: 12.1, colW: [0.9, 1.8, 2.0, 5.6, 1.8], fontFace: FT, fontSize: 14, color: C.ink, rowH: 0.52, valign: "middle",
      border: { type: "solid", color: "D5DAE1", pt: 1 }, fill: { color: "FFFFFF" }, margin: 0.08 });
  T(s, "B 區的強度需求取區段起點（V_u 最大處）；分區不是為了省鋼筋，而是把密箍放在真正需要的端部。題目若問『最少要配到哪裡』，答案是 0.5φV_c 的位置。", 0.6, 6.7, 12.1, 0.4, { fontSize: 12.5, color: C.muted });
}
// ───── 例① 完整走一遍（兩欄骨架） ─────
{
  const s = newSlide(); header(s, "綜合演練", "例①：四道關卡完整走一遍", C.ink);
  const L = [["關卡 1", "支承受壓、頂面均布、d 內無集中載重 ⇒ 可偏移", "m_d1", RD],
             ["關卡 2", "無軸力、未要求精算 ⇒ 簡化式", "m_vc1", BL],
             ["關卡 3", `V_s ≤ 2V_c = ${f2(N.VC2)} ⇒ s_{max} = d/2；V_u ≤ 5φV_c ✓`, "m_vs1", OR],
             ["關卡 4", `min(${f2(N.S1_REQ)}, 31.5, ${f2(N.S_AVMIN)}) = ${f2(N.S1_REQ)} → 取 D13@25`, "m_s1", GN]];
  L.forEach(([g, t, m, P], i) => {
    const y = 1.4 + i * 1.3;
    panel(s, 0.6, y, 12.1, 1.2, P[1], P[2]);
    T(s, g, 0.8, y + 0.15, 1.3, 0.4, { fontSize: 17, bold: true, color: P[0] });
    T(s, t, 0.8, y + 0.62, 5.2, 0.55, { fontSize: 13.5 });
    eq(s, m, 6.3, y + 0.1, 1.0, 0.58, "left", 6.2);
  });
  T(s, `對照：若誤判不能偏移（取 ${f2(N.VU1_F)}），V_s = ${f2(N.VS1F)}、s ≤ ${f2(N.S1F_REQ)} → 只能配 D13@18；多用約 ${f1((25 / 18 - 1) * 100)}% 箍筋。`, 0.6, 6.95 - 0.35, 12.1, 0.4, { fontSize: 13.5, bold: true, color: C.org });
}
// ───── 流程圖 ─────
{
  const s = newSlide(); header(s, "解題流程圖", "考場上照著走：四道關卡的判斷路徑", C.ink);
  img(s, "fig19_flow", 0.6, 1.35, 12.1, 5.65);
}
// ───── 陷阱 ─────
{
  const s = newSlide(); header(s, "考場陷阱", "最常扣分的六個地方", C.red);
  const cardsList = [
    ["1｜d 偏移無條件套用", "吊掛、倒 T 梁、d 內有集中載重都不能偏移；例③正確的端部箍筋量比誤用多約 31%。", RD],
    ["2｜V_c 選錯臉", "看到軸拉就要想到 /35A_g；耐震塑鉸區 V_c = 0。同一斷面可差到 4 倍。", BL],
    ["3｜忘記斷面天花板", "先比 V_u 與 5φV_c；V_s > 4V_c 時加箍筋無效，只能改斷面或 f'_c。", RD],
    ["4｜尺用錯", "間距門檻與天花板是 1.06、2.12√f'_c b_w d；V_c 被修正時不能用『2V_c、4V_c』。", OR],
    ["5｜間距只算強度就交卷", "四取小：強度需求、s_{max}、A_{v,min}、施工取整——缺一個就扣分。", GN],
    ["6｜詳細式漏限制", "V_u d/M_u ≤ 1、上限 0.93√f'_c b_w d；有軸壓用 M_m，M_m ≤ 0 取帶軸力項的上限式。", PU]];
  cardsList.forEach(([h, b, P], i) => {
    const x = 0.6 + (i % 3) * 4.08, y = 1.5 + Math.floor(i / 3) * 2.75;
    panel(s, x, y, 3.94, 2.55, P[1], P[2]);
    T(s, paras([{ t: h, o: { bold: true, fontSize: 16, color: P[0] } }, { t: b, o: { fontSize: 14 } }]), x + 0.22, y + 0.2, 3.5, 2.2, { paraSpaceAfter: 8 });
  });
}
// ───── 回顧 ─────
{
  const s = newSlide(); header(s, "回顧", "四道關卡速查", C.ink);
  const R = [["關卡 1", "V_u 取在哪", "三前提同時成立 → 取 d 處；否則取支承面", `例①：42.00 → 34.44（省 18.0%）｜例③：只能 63.00`, RD],
             ["關卡 2", "V_c 用哪張臉", "簡化／詳細／軸壓 140／軸拉 35／耐震 0", `19.56｜23.24｜22.98｜5.87｜0`, BL],
             ["關卡 3", "V_s 在哪段", "V_s = V_u/φ − V_c；門檻 1.06、2.12√f'_c b_w d", `例③ V_s = 64.44；V_u ≤ 5φV_c = 73.33（85.9%）`, OR],
             ["關卡 4", "s 取多少", "四取小；三條線 3φV_c、φV_c、0.5φV_c 分區", `例③ D13@10／@15／@30；例① D13@25`, GN]];
  R.forEach(([g, q, rule, ex, P], i) => {
    const y = 1.4 + i * 1.27;
    panel(s, 0.6, y, 12.1, 1.14, P[1], P[2]);
    T(s, g, 0.85, y + 0.18, 1.3, 0.4, { fontSize: 18, bold: true, color: P[0] });
    T(s, q, 0.85, y + 0.62, 1.8, 0.4, { fontSize: 14, color: C.muted });
    T(s, rule, 2.8, y + 0.18, 9.7, 0.4, { fontSize: 16, bold: true });
    T(s, ex, 2.8, y + 0.64, 9.7, 0.4, { fontSize: 14, color: P[0] });
  });
  T(s, "順序千萬不要顛倒：先定 V_u → 再選 V_c → 再判 V_s 區間 → 最後才算 s", 0.6, 6.95 - 0.3, 12.1, 0.4, { fontSize: 16, bold: true, align: "center" });
}
pres.writeFile({ fileName: "RC-U2-1_四道關卡解題SOP.pptx" }).then(() => console.log("done", pg));
