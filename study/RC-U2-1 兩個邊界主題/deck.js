const pptxgen = require("pptxgenjs");
const fs = require("fs");
const N = JSON.parse(fs.readFileSync("nums.json", "utf8"));
const MJ = JSON.parse(fs.readFileSync("figs/math.json", "utf8"));
const pres = new pptxgen(); pres.layout = "LAYOUT_WIDE"; pres.title = "RC-U2-1 拼圖四：兩個邊界主題（STM・剪力摩擦）";
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

const f0 = v => (v + 1e-9).toFixed(0);
// ───── 1 封面 ─────
{
  const s = pres.addSlide(); s.background = { color: C.dark };
  T(s, "RC-U2-1　RC 剪力強度分析與設計｜觀念講義・拼圖四", 0.8, 1.2, 11.5, 0.4, { fontSize: 16, color: "9FB3C8", bold: true });
  T(s, "兩個邊界主題：公式認錯，整題必錯", 0.8, 1.8, 11.8, 1.0, { fontSize: 44, bold: true, color: C.white });
  T(s, "平截面假設失效 → 壓拉桿模式 STM；存在明確滑動介面 → 剪力摩擦；附帶：扭力何時可忽略", 0.8, 2.95, 11.8, 0.5, { fontSize: 20, color: "E6CFA0" });
  const G = [["邊界①", "深梁・STM", C.blu], ["邊界②", "剪力摩擦", C.org], ["附帶", "扭力門檻", "9AA3AE"]];
  G.forEach(([n, t, c], i) => {
    const x = 0.8 + i * 3.6;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 4.1, w: 3.35, h: 1.2, fill: { color: "243044" }, line: { color: c, width: 2 }, rectRadius: 0.1 });
    T(s, n, x + 0.2, 4.22, 3.0, 0.4, { fontSize: 16, bold: true, color: c });
    T(s, t, x + 0.2, 4.65, 3.0, 0.5, { fontSize: 22, bold: true, color: C.white });
  });
  T(s, `例⑤ 深梁 P_u = ${f0(N.PU5)} tf、例④ 介面 V_u = ${f0(N.VU4)} tf、基準斷面 35×70；圖上數字全部由同一份 params.py 覆算`, 0.8, 5.9, 11.8, 0.4, { fontSize: 15, color: "9FB3C8" });
}
// ───── 2 地圖 ─────
figSlide("TOPIC MAP", "拼圖四的位置：先問「公式認對了沒」", "fig01_map", [
  cell("桁架類比的兩個前提", ["① 平截面假設成立（B 區）", "② 沒有預先存在的滑動面"], PU),
  cell("前提 ① 破了", ["a/d ≤ 2、集中載重靠近支承、牛腿 → 力走直線 → STM"], BL),
  cell("前提 ② 破了", ["施工縫、新舊混凝土、預鑄接縫 → 沿介面滑動 → 剪力摩擦"], OR)], C.ink, 4.3);
// ───── 3 示範案例 ─────
figSlide("示範案例", "兩個例題＋一個基準斷面：全篇數字都從這裡來", "fig02_cases", [
  cell("例⑤ 深梁", [`a/d = ${N.AD5.toFixed(2)}：拉桿 ${f1(N.T5)} tf、壓桿 ${f1(N.F5)} tf`], BL),
  cell("例④ 剪力摩擦", [`粗糙 ${f2(N.AVF_R)} vs 未粗糙 ${f2(N.AVF_S)} cm²（多 ${f1(N.MORE4)}%）`], OR),
  cell("扭力門檻", [`φT_{th} = ${N.PTTH.toFixed(3)} t-m；誤用 A_{oh} 會低估 ${f1(N.DROP_T)}%`], [C.muted, C.panel, C.line])], C.ink, 4.4);

// ═════ 邊界主題 ① ═════
section("邊界主題 ①", "深梁與壓拉桿模式 STM", "a/d 越小，力越想「走直線」——箍筋不再是主要傳力路徑", C.blu);
figSlide("邊界① | 物理", "B 區與 D 區：平截面假設在哪裡失效", "fig03_bd", [
  cell("D 區（Disturbed）", ["集中載重、支承、斷面突變附近約一個構材深度 h 的範圍（題目常寫 d）"], BL),
  cell("B 區（Bernoulli）", ["遠離不連續處，應變沿深度呈直線 → 可用梁理論與 V_c + V_s"], PU),
  cell("深梁 = 整根都是 D 區", ["l_n ≤ 4h，或集中載重距支承面 ≤ 2h：兩個 D 區連在一起，沒有 B 區可用"], RD)], C.blu, 4.2);
figSlide("邊界① | a/d", "同樣的梁，改變 a/d 就換了力流", "fig04_ad3", [
  cell("a/d 小（≲ 1）", ["斜壓桿直接把載重送進支承：拱作用（arch action）主導"], BL),
  cell("a/d ≈ 2 ~ 2.5", ["拱作用與桁架作用並存；是兩套方法的交界"], OR),
  cell("a/d 大（> 2.5）", ["一根斜壓桿到不了支承，要靠箍筋一段一段「接力」吊上去"], PU)], C.blu, 4.3);
figSlide("邊界① | 強度", "剪力強度隨 a/d 變化：兩個方向的誤用都危險", "fig05_curve", [
  cell("為什麼 a/d 越小越強", ["壓桿越陡、力臂越短 → 同樣 P 對應的斜壓力越小；破壞轉為壓桿壓碎或節點破壞"], BL),
  cell("考場判斷", ["a/d ≤ 2（或規範的深梁定義）→ 直接切換到 STM，不要先算 V_c"], RD)], C.blu, 4.5);
{
  const s = figSlide("邊界① | 三元件", "STM 只要驗三種東西：壓桿、拉桿、節點", "fig06_stm", [], C.blu, 3.75);
  eqPanel(s, 0.6, 5.3, 4.9, 1.7, "壓桿 Strut", ["m_ns"], BL);
  eqPanel(s, 5.65, 5.3, 2.4, 1.7, "拉桿 Tie", ["m_nt"], RD);
  eqPanel(s, 8.2, 5.3, 4.5, 1.7, "節點 Node", ["m_nn"], OR, "φ 一律 0.75");
}
figSlide("邊界① | 壓桿", "壓桿係數 β_s：形狀與周圍鋼筋決定打幾折", "fig07_struts", [
  cell("瓶形為什麼打折", ["壓力從窄端擴散到寬中段 → 產生橫向拉力 → 沿壓桿方向劈裂"], OR),
  cell("β_s = 0.75 的條件", ["穿過壓桿的分布鋼筋要夠：Σ A_{si} sinα_i /(b s_i) ≥ 0.003"], GN),
  cell("考場預設", ["深梁腹板有配水平、垂直分布筋 → 多數題目取 0.75"], BL)], C.blu, 4.3);
figSlide("邊界① | 節點", "節點係數 β_n：錨入的拉桿越多，節點越弱", "fig08_nodes", [
  cell("CCC", ["載重點下方：三面受壓，圍束最好"], GN),
  cell("CCT", ["支承上方：拉桿錨入節點，拉應變干擾混凝土"], OR),
  cell("CTT", ["兩個方向都有拉桿（如框架角隅）"], RD),
  cell("驗算面", ["每個節點面都要驗：承壓面、壓桿端面、拉桿錨定面"], BL)], C.blu, 4.3);
figSlide("邊界① | 拉桿", "拉桿：強度只是一半，另一半是錨定", "fig09_anchor", [], C.blu, 5.5);
{
  const s = newSlide(); header(s, "邊界① | 例⑤ 建模", `例⑤：a/d = ${N.AD5.toFixed(2)} 的深梁，先畫出桁架`, C.blu);
  img(s, "fig10_ex5", 0.6, 1.35, 7.7, 5.6);
  eqPanel(s, 8.45, 1.4, 4.25, 1.7, "① 上節點高度（水平壓桿剛好滿應力）", ["m_wtop"], BL);
  eqPanel(s, 8.45, 3.25, 4.25, 1.7, "② 力臂與壓桿角度", ["m_z", "m_th"], BL);
  eqPanel(s, 8.45, 5.1, 4.25, 1.85, "③ 節點平衡", ["m_f"], BL, "w_{top} 與 z 互相牽動 → 迭代到收斂");
}
{
  const s = newSlide(); header(s, "邊界① | 例⑤ 驗算", "例⑤：三種元件逐一驗算，最緊的是拉桿與上端壓桿", C.blu);
  img(s, "fig11_ex5chk", 0.6, 1.3, 12.1, 2.75);
  eqPanel(s, 0.6, 4.15, 6.0, 1.05, `壓桿下端（w_s = ${f1(N.WS_B)}；β_s 0.75、β_n 0.80 取小 → 178.5）`, ["m_sb"], BL);
  eqPanel(s, 6.75, 4.15, 5.95, 1.05, `壓桿上端（w_s = ${f1(N.WS_T)}；β_s 0.75 控制）`, ["m_st"], BL);
  eqPanel(s, 0.6, 5.3, 6.0, 1.05, "拉桿", ["m_ats"], RD);
  eqPanel(s, 6.75, 5.3, 5.95, 1.05, "深梁總上限", ["m_dlim"], [C.muted, C.panel, C.line]);
  panel(s, 0.6, 6.45, 12.1, 0.55, C.redbg, C.redln);
  T(s, paras([{ t: `陷阱：腹板若沒配分布鋼筋只能取 β_s = 0.60 → 上端壓桿 φF_{ns} = ${f1(N.CAP_ST60)} < ${f1(N.F5)} tf，不通過；拉桿還要回頭檢核錨定。`, o: { bold: true, fontSize: 13.5, color: C.red } }]), 0.85, 6.57, 11.6, 0.4);
}
{
  const s = figSlide("邊界① | 上限", "深梁總上限 2.65√f'_c b_w d 與桁架類比的 5V_c 是同一個數", "fig12_limit", [], C.blu, 3.9);
  eqPanel(s, 0.6, 5.4, 6.0, 1.6, "係數對帳", ["m_5vc"], PU);
  panel(s, 6.75, 5.4, 5.95, 1.6, C.bluebg || C.blubg, C.bluln);
  T(s, paras([{ t: "共通物理", o: { bold: true, fontSize: 15, color: C.blu } },
    { t: "不論力走桁架還是走拱，最後都是混凝土斜壓力帶被壓碎——所以天花板一樣，只是深梁的「地板」高很多。", o: { fontSize: 14 } }]), 6.95, 5.52, 5.6, 1.4, { paraSpaceAfter: 4 });
}

// ═════ 邊界主題 ② ═════
section("邊界主題 ②", "剪力摩擦", "鋼筋不是「擋住」滑動，而是「夾住」介面", C.org);
{
  const s = figSlide("邊界② | 機制", "機制的三個動作：滑動 → 張開 → 夾緊", "fig13_sfmech", [], C.org, 4.0);
  eqPanel(s, 0.6, 5.5, 5.0, 1.5, "基本式", ["m_sf"], OR);
  panel(s, 5.75, 5.5, 6.95, 1.5, C.orgbg, C.orgln);
  T(s, paras([{ t: "P_c：垂直介面的「永久」壓力才可計入", o: { bold: true, fontSize: 15, color: C.org } },
    { t: "活載重、地震等可能消失的壓力不能算；若介面有淨拉力，要另外配鋼筋承擔，不可與 A_{vf} 共用。", o: { fontSize: 14 } }]), 5.95, 5.62, 6.6, 1.3, { paraSpaceAfter: 4 });
}
{
  const s = figSlide("邊界② | μ", "μ 不是「摩擦係數」，是規範給的等效值", "fig14_mu", [], C.org, 3.9);
  cells(s, [
    cell("λ", ["常重混凝土 1.0、全輕質 0.75；μ 一律乘 λ"], OR),
    cell("粗糙化的定義", ["硬固面刻意打毛，凹凸幅度約 6 mm"], OR),
    cell("f_y 限制", ["A_{vf} 的 f_y 不得超過 4200 kgf/cm²"], OR)], 5.45, 1.5);
}
{
  const s = figSlide("邊界② | 例④", "例④：粗糙化與否，鋼筋量差 66.7%", "fig15_ex4", [], C.org, 3.6);
  eqPanel(s, 0.6, 5.1, 3.9, 1.9, "反算鋼筋", ["m_avf"], OR);
  eqPanel(s, 4.65, 5.1, 4.2, 1.9, "兩種介面", ["m_avf1", "m_avf2"], OR);
  eqPanel(s, 9.0, 5.1, 3.7, 1.9, "上限（粗糙面）", ["m_sflim", "m_sflim1"], OR);
}
figSlide("邊界② | 陷阱", "A_{vf} 是「垂直穿過介面」的鋼筋，不是梁的箍筋 A_v", "fig16_avf", [
  cell("先畫出介面", ["介面方向決定哪些鋼筋算數：只有穿過介面、且兩側都錨定足夠的才算"], GN),
  cell("斜向穿過時", ["鋼筋與介面夾角 α 時改用 V_n = A_{vf} f_y (μ sinα + cosα)，且只限受拉方向"], OR),
  cell("未粗糙面的上限", [`只剩 min(0.2f'_c, 56)A_c；本例 f'_c = 280 時兩者剛好都是 56`], RD)], C.org, 4.2);

// ═════ 附帶：扭力門檻 ═════
section("附帶主題", "扭力何時可以忽略？", "門檻用外緣 A_{cp}、p_{cp}；真正設計才換成箍筋中心線 A_{oh}、A_o", "9AA3AE");
{
  const s = figSlide("扭力 | 門檻", "門檻判定用 A_{cp}，配筋設計才用 A_{oh}", "fig17_torsion", [], C.ink, 3.85);
  eqPanel(s, 0.6, 5.35, 3.6, 1.65, "門檻公式", ["m_tth"], [C.muted, C.panel, C.line]);
  eqPanel(s, 4.35, 5.35, 4.3, 1.65, "基準斷面代數字", ["m_tth1"], [C.muted, C.panel, C.line]);
  eqPanel(s, 8.8, 5.35, 3.9, 1.65, "物理意義：¼ 開裂扭矩", ["m_tcr"], [C.muted, C.panel, C.line]);
}
// ───── 流程圖 ─────
{
  const s = newSlide(); header(s, "解題流程圖", "考場上照著走：先認公式，再代數字", C.ink);
  img(s, "fig18_flow", 0.6, 1.35, 12.1, 5.65);
}
// ───── 陷阱 ─────
{
  const s = newSlide(); header(s, "考場陷阱", "最常扣分的六個地方", C.red);
  const L = [
    ["1｜深梁照樣算 V_c + V_s", "a/d ≤ 2 還用桁架類比：強度低估 2 ~ 4 倍，配出一堆無效箍筋；反過來用 STM 算細長梁則不安全。", BL],
    ["2｜β_s 隨便取 0.75", "0.75 綁著分布鋼筋 Σ A_{si} sinα_i/(b s_i) ≥ 0.003；沒配就是 0.60。例⑤ 取 0.60 上端壓桿就不過。", RD],
    ["3｜拉桿只算面積", "錨定長度從拉桿重心離開延伸節點區處起算；長度不夠 → 彎鉤、錨定板或加長支承板。", RD],
    ["4｜拿箍筋 A_v 當 A_{vf}", "A_{vf} 必須垂直穿過介面、兩側錨定；鉛直介面時梁箍筋完全沒有夾緊作用。", OR],
    ["5｜μ 與上限記錯", "粗糙 1.0、未粗糙 0.6、單體 1.4、鋼板 0.7（× λ）；上限不夠加鋼筋無效，只能加 A_c。", OR],
    ["6｜扭力門檻用 A_{oh}", `門檻用外緣 A_{cp}、p_{cp}；誤用 A_{oh}、p_h 會把門檻從 ${N.PTTH.toFixed(3)} 算成 ${N.PTTH_WRONG.toFixed(3)} t-m。`, PU]];
  L.forEach(([h, b, P], i) => {
    const x = 0.6 + (i % 3) * 4.08, y = 1.5 + Math.floor(i / 3) * 2.75;
    panel(s, x, y, 3.94, 2.55, P[1], P[2]);
    T(s, paras([{ t: h, o: { bold: true, fontSize: 16, color: P[0] } }, { t: b, o: { fontSize: 14 } }]), x + 0.22, y + 0.2, 3.5, 2.2, { paraSpaceAfter: 8 });
  });
}
// ───── 速查 ─────
{
  const s = newSlide(); header(s, "公式速查", "拼圖四：必背數值一頁看完", C.ink);
  const H = (t) => ({ text: t, options: { bold: true, color: C.white, fill: { color: "2A3B55" } } });
  const R = (a, b, c, col) => [{ text: runs(a, { bold: true, color: col }) }, { text: runs(b) }, { text: runs(c, { color: C.muted }) }];
  const rows = [[H("項目"), H("公式／數值"), H("備註")],
    R("STM 強度", "φF = φ f_{ce} A；f_{ce} = 0.85β f'_c；φ = 0.75", "壓桿、節點共用同一形式", C.blu),
    R("壓桿 β_s", "1.0 稜柱／0.75 瓶形有筋／0.60λ 瓶形無筋／0.40 拉力構材", "0.75 需分布筋 ≥ 0.003", C.blu),
    R("節點 β_n", "1.0 CCC／0.80 CCT／0.60 CTT", "看錨入幾根拉桿", C.blu),
    R("拉桿／幾何", "φF_{nt} = φA_{ts} f_y；θ ≥ 25°；V_n ≤ 2.65√f'_c b_w d", "錨定從延伸節點區外起算", C.blu),
    R("剪力摩擦", "V_n = μ(A_{vf} f_y + P_c)；A_{vf} = V_u/(φμf_y)", "P_c 只計永久壓力", C.org),
    R("μ（× λ）", "1.4 單體／1.0 粗糙／0.6 未粗糙／0.7 鋼板", "粗糙 vs 未粗糙差 66.7%", C.org),
    R("摩擦上限", "min(0.2f'_c, 34+0.08f'_c, 112)A_c；未粗糙 min(0.2f'_c, 56)A_c", "f'_c = 280 → 56 A_c", C.org),
    R("扭力門檻", "T_u ≤ φ0.265√f'_c A_{cp}²/p_{cp}（= φT_{cr}/4）", "外緣 A_{cp}，不是 A_{oh}", C.muted)];
  s.addTable(rows, { x: 0.6, y: 1.45, w: 12.1, colW: [2.0, 6.9, 3.2], fontFace: FT, fontSize: 14, color: C.ink, rowH: 0.6, valign: "middle",
    border: { type: "solid", color: "D5DAE1", pt: 1 }, fill: { color: "FFFFFF" }, margin: 0.08 });
}
// ───── 單元總結 ─────
{
  const s = newSlide(); header(s, "單元總結", "RC 剪力四塊拼圖：一個底層邏輯貫穿到底", C.ink);
  const R = [["拼圖一", "底層邏輯", "剪應力 → 45° 斜向主拉 → 混凝土被拉裂", C.teal, [C.teal, C.grnbg, C.grnln]],
             ["拼圖二", "三大機制", "桁架類比（B 區）／壓拉桿（D 區）／剪力摩擦（既有介面）", C.pur, PU],
             ["拼圖三", "四道關卡", "V_u 位置 → V_c 選臉 → V_s 區間與斷面 → 間距四取小", C.org, OR],
             ["拼圖四", "兩個邊界", `STM：例⑤ 拉桿 ${f1(N.U_T)}%、上端壓桿 ${f1(N.U_ST)}%｜剪力摩擦：例④ ${f2(N.AVF_R)} vs ${f2(N.AVF_S)} cm²`, C.blu, BL]];
  R.forEach(([g, q, rule, col, P], i) => {
    const y = 1.4 + i * 1.27;
    panel(s, 0.6, y, 12.1, 1.14, P[1], P[2]);
    T(s, g, 0.85, y + 0.18, 1.5, 0.4, { fontSize: 18, bold: true, color: P[0] });
    T(s, q, 0.85, y + 0.62, 1.8, 0.4, { fontSize: 14, color: C.muted });
    T(s, rule, 2.8, y + 0.35, 9.7, 0.5, { fontSize: 16, bold: true });
  });
  T(s, "每一題都先問：力怎麼走？平截面還成立嗎？有沒有既有介面？——認對機制，公式才會對。", 0.6, 6.65, 12.1, 0.4, { fontSize: 16, bold: true, align: "center" });
}
pres.writeFile({ fileName: "RC-U2-1_兩個邊界主題.pptx" }).then(() => console.log("done", pg));
