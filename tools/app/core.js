"use strict";
const DATA = /*DATA*/null;
const KEY = 'n10-v3', KEY2 = 'muscu-app-v2', KEY1 = 'muscu-app-v1';
const view = document.getElementById('view');
const WO = document.getElementById('wo');
const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const p2 = n => String(n).padStart(2, '0');
const ymd = d => d.getFullYear() + '-' + p2(d.getMonth() + 1) + '-' + p2(d.getDate());
const D = s => new Date(s + 'T12:00:00');
const TODAY = () => ymd(new Date());
const addDays = (s, n) => { const d = D(s); d.setDate(d.getDate() + n); return ymd(d); };
const JOURS = ['Dimanche', 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi'];
const MOIS = ['janv.', 'févr.', 'mars', 'avr.', 'mai', 'juin', 'juil.', 'août', 'sept.', 'oct.', 'nov.', 'déc.'];
const KEYS = ['dimanche', 'lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi'];
const ORDER = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche'];
const fmtDate = s => { const d = D(s); return d.getDate() + ' ' + MOIS[d.getMonth()]; };
const fmtShort = s => { const d = D(s); return p2(d.getDate()) + '/' + p2(d.getMonth() + 1); };
const num = v => { if (v == null || v === '') return null; const n = parseFloat(String(v).replace(',', '.')); return isFinite(n) ? n : null; };
const fr1 = n => (Math.round(n * 10) / 10).toLocaleString('fr-FR');
const fr0 = n => Math.round(n).toLocaleString('fr-FR');
const frn = n => (Math.round(n * 100) / 100).toLocaleString('fr-FR');
const cap = s => s.charAt(0).toUpperCase() + s.slice(1);
function mondayOf(d) { const x = new Date(d); x.setHours(12, 0, 0, 0); x.setDate(x.getDate() - ((x.getDay() + 6) % 7)); return x; }
const weekKey = (d = new Date()) => ymd(mondayOf(d));
function defaultStart() { const d = new Date(); const i = (d.getDay() + 6) % 7; const m = mondayOf(d); if (i >= 4) m.setDate(m.getDate() + 7); return ymd(m); }
function isoWeek(d) { const t = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate())); const day = t.getUTCDay() || 7; t.setUTCDate(t.getUTCDate() + 4 - day); const y0 = new Date(Date.UTC(t.getUTCFullYear(), 0, 1)); return Math.ceil(((t - y0) / 864e5 + 1) / 7); }
const fishWeek = () => isoWeek(new Date()) % 2 === 0 ? 'A' : 'B';

/* ---------------- state ---------------- */
const BLANK = () => ({ v: 3, start: null, name: '', variant: {}, weights: {}, hist: {}, cur: null, log: [], match: {}, matches: [], tests: [], xp: [], prs: [], badges: {},
  wbonus: {}, daily: {}, food: {}, body: [], shop: {}, coach: { code: '', msgs: [] }, set: { beep: true, wake: true, theme: 'auto' }, ready: {}, recup: {}, migrated: null, welcomed: false });
let S = BLANK();
const DAYS = DATA.days, EXD = DATA.ex;
const dayByKey = k => DAYS.find(d => d.key === k);
const todayKey = () => KEYS[new Date().getDay()];
function slotOptions(sl) { return [sl.ex].concat(sl.alts || []); }
function slotSlug(sl) { const o = slotOptions(sl); return o[Math.min(S.variant[sl.id] || 0, o.length - 1)]; }
function allSlots() { const out = []; DAYS.forEach(d => (d.slots || []).concat(d.pre || [], (d.tech && d.tech.slots) || []).forEach(s => out.push(s))); return out; }
const slotById = id => allSlots().find(s => s.id === id);

function migrateV2(o) {
  const b = BLANK();
  b.start = o.start || null; b.weights = o.weights || {}; b.hist = o.hist || {};
  b.food = o.food || {}; b.body = Array.isArray(o.body) ? o.body : [];
  b.coach = Object.assign(b.coach, o.coach || {}); b.set = Object.assign(b.set, o.set || {});
  const v2v = o.variant || {};
  allSlots().forEach(sl => {
    const i = v2v[sl.ex]; if (!i) return;
    const chosen = [sl.ex].concat(DATA.v2alts[sl.ex] || [])[i];
    const j = slotOptions(sl).indexOf(chosen);
    if (j > 0) b.variant[sl.id] = j;
  });
  b.log = (o.log || []).map(l => ({ d: l.d, day: 'v2', kind: 'gym', name: DATA.v2days[l.day] || 'Séance', col: 'hautA', done: l.done, total: l.total, min: l.min || null, xp: 100 }));
  b.xp = b.log.map(l => ({ d: l.d, n: 100, why: 'Séance' }));
  b.migrated = 'v2';
  S = b;
}
function loadState() {
  let raw = null;
  try { raw = localStorage.getItem(KEY); } catch (e) {}
  if (raw) {
    try { const o = JSON.parse(raw); const b = BLANK(); S = Object.assign(b, o); S.set = Object.assign(BLANK().set, o.set || {}); S.coach = Object.assign({ code: '', msgs: [] }, o.coach || {}); } catch (e) {}
  } else {
    let v2 = null, v1 = null;
    try { v2 = localStorage.getItem(KEY2); v1 = localStorage.getItem(KEY1); } catch (e) {}
    if (v2) { try { migrateV2(JSON.parse(v2)); } catch (e) {} }
    else if (v1) { try { const o = JSON.parse(v1); for (const k in (o.weights || {})) if (o.weights[k]) S.weights[k] = o.weights[k]; S.migrated = 'v1'; } catch (e) {} }
  }
  if (!S.start) S.start = defaultStart();
  const lim = addDays(TODAY(), -21);
  ['food', 'ready', 'recup', 'daily'].forEach(k => { for (const d in S[k]) if (d < lim) delete S[k][d]; });
}
const save = () => { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) {} };

/* ---------------- cycle & prescriptions ---------------- */
function progWeek(s = TODAY()) { const n = Math.floor((D(s) - D(S.start)) / 864e5); return n < 0 ? 0 : Math.floor(n / 7) + 1; }
function weekInfo(real = progWeek()) {
  const w = Math.min(12, Math.max(1, real));
  return { real, w, block: w <= 4 ? 0 : w <= 8 ? 1 : 2, learn: DATA.learn.includes(w), deload: DATA.deload.includes(w), test: DATA.testWeeks.includes(w), before: real === 0, after: real > 12 };
}
const isMatchWeek = (wk = weekKey()) => !!S.match[wk];
function dayView(day, wk = weekKey()) {
  if (day.kind !== 'sunday') return Object.assign({}, day);
  const m = isMatchWeek(wk), sub = m ? day.match : day.tech;
  return Object.assign({}, day, sub, { key: day.key, kind: m ? 'match' : 'tech' });
}
const EFFRX = /^(\d+)\/10/;
function lowerEff(eff, n) {
  const s = String(eff), m = s.match(EFFRX);
  if (m) return Math.max(5, +m[1] - n) + '/10' + s.slice(m[0].length);
  const p = s.match(/^(\d+) %/);
  if (p) return Math.min(+p[1], n >= 2 ? 80 : 90) + ' %';
  return s;
}
function capEff(eff, c) { const s = String(eff), m = s.match(EFFRX); return m && +m[1] > c ? c + '/10' + s.slice(m[0].length) : s; }
function presc(sl, dayKey, info, ready, mw) {
  const base = sl.p[info.block]; if (!base) return null;
  if (sl.from && info.w < sl.from) return null;
  if (dayKey === 'vendredi' && info.test && sl.test) return null;
  let [sets, reps, rest, eff] = base; const why = [];
  const k = sl.kind;
  if (info.learn && ['force', 'power', 'core', 'plyo', 'prev'].includes(k) && sets > 2) { sets = 2; why.push('Semaines 1–2 : 2 séries pour apprendre'); }
  if (info.deload) { sets = Math.max(1, sets - 1); eff = capEff(eff, 7); why.push('Semaine allégée'); }
  if (mw && dayKey === 'vendredi' && ['plyo', 'sprint', 'cod', 'ball'].includes(k)) { const s2 = Math.max(1, Math.round(sets * 0.7)); if (s2 < sets) { sets = s2; why.push('Match dimanche : volume réduit'); } }
  if (mw && dayKey === 'samedi') { if (sets > 2) sets = 2; eff = capEff(eff, 7); why.push('Veille de match : court et sans échec'); }
  if (ready != null && ready <= 2) { sets = Math.max(1, Math.ceil(sets / 2)); eff = lowerEff(eff, 2); why.push('Forme basse : séance allégée'); }
  else if (ready != null && ready <= 4 && ['force', 'power', 'plyo', 'sprint', 'cod'].includes(k)) { if (sets > 1) sets -= 1; eff = lowerEff(eff, 1); why.push('Forme moyenne : une série de moins'); }
  return { sets, reps, rest, eff, why };
}
function planFor(day, info = weekInfo(), ready = null, wk = weekKey()) {
  const v = dayView(day, wk), mw = isMatchWeek(wk);
  const slots = v.kind === 'foot' ? (day.pre || []) : (v.slots || []);
  return slots.map(sl => { const pr = presc(sl, day.key, info, ready, mw); return pr ? { sl, slug: slotSlug(sl), pr } : null; }).filter(Boolean);
}
function repsFor(sl, slug, pr) { const e = EXD[slug]; return slug !== sl.ex && e.reps ? e.reps : pr.reps; }
function topOf(reps) { const s = String(reps); if (/min|\bm\b/.test(s)) return null; const m = s.match(/(\d+)(?:\s*[–-]\s*(\d+))?/); return m ? +(m[2] || m[1]) : null; }
function modeOf(sl, slug, reps) {
  if (['plyo', 'sprint', 'cod', 'ball'].includes(sl.kind) || EXD[slug].eq === 'velo') return 'drill';
  if (/\d\s*s\b/.test(reps) && !/×/.test(reps)) return 'hold';
  if (/\d\s*m\b/.test(reps)) return EXD[slug].step ? 'carry' : 'drill';
  return EXD[slug].step ? 'load' : 'reps';
}
const KIND = DATA.kinds;
const EQL = { machine: 'Machine', halteres: 'Haltères', pdc: 'Poids du corps', medball: 'Médecine-ball', box: 'Box', terrain: 'Terrain', ballon: 'Ballon', velo: 'Vélo' };
const restTxt = s => !s ? '—' : s >= 60 ? (s % 60 ? Math.floor(s / 60) + ' min ' + (s % 60) : s / 60 + ' min') : s + ' s';
const restShort = s => !s ? '—' : s >= 60 ? (s % 60 ? Math.floor(s / 60) + ':' + p2(s % 60) : s / 60 + ' min') : s + ' s';

/* ---------------- history, records ---------------- */
const exName = slug => (EXD[slug] && EXD[slug].name) || DATA.oldnames[slug] || slug;
const exStep = slug => EXD[slug] ? EXD[slug].step : 1;
const exNeg = slug => !!(EXD[slug] && EXD[slug].neg) || DATA.oldneg.includes(slug);
function lastHist(slug, exceptToday = true) { const h = (S.hist[slug] || []).filter(x => !exceptToday || x.d !== TODAY()); return h[h.length - 1] || null; }
function bestOf(slug, beforeDate) {
  const h = (S.hist[slug] || []).filter(x => !beforeDate || x.d < beforeDate);
  if (exStep(slug)) {
    let b = null; const neg = exNeg(slug);
    h.forEach(x => { const v = num(x.w); if (v == null) return; if (b == null || (neg ? v < b : v > b)) b = v; });
    return b;
  }
  let b = null; h.forEach(x => { if (x.r != null && (b == null || x.r > b)) b = x.r; }); return b;
}
function recordHist(slug, patch) {
  const h = S.hist[slug] || (S.hist[slug] = []);
  let e = h.find(x => x.d === TODAY());
  if (!e) { e = { d: TODAY() }; h.push(e); }
  Object.assign(e, patch);
  if (h.length > 80) h.splice(0, h.length - 80);
}
function targetFor(slug) {
  const st = exStep(slug); if (!st) return null;
  const last = lastHist(slug); if (!last) return null;
  const w = num(last.w); if (w == null) return null;
  const up = (last.top === true && last.fb !== 'dur') || last.fb === 'facile';
  const neg = exNeg(slug);
  const t = up ? (neg ? Math.max(0, w - st) : w + st) : w;
  return { w: t, up, last };
}

/* ---------------- XP, levels, badges ---------------- */
const LEVELS = DATA.levels;
let pending = [];
function xpTotal() { return S.xp.reduce((a, x) => a + (x.n || 0), 0); }
function levelOf(xp = xpTotal()) {
  let i = 0; while (i + 1 < LEVELS.length && xp >= LEVELS[i + 1].xp) i++;
  const cur = LEVELS[i], nx = LEVELS[i + 1];
  return { i, n: i + 1, t: cur.t, em: cur.em, xp, from: cur.xp, to: nx ? nx.xp : null, pct: nx ? (xp - cur.xp) / (nx.xp - cur.xp) : 1, next: nx ? nx.t : null };
}
function addXP(n, why, d = TODAY()) {
  if (!n) return;
  const before = levelOf().i;
  S.xp.push({ d, n, why });
  const after = levelOf();
  if (after.i > before) pending.push({ kind: 'level', lv: after });
}
function daysWithActivity(from, to) { const set = new Set(); S.log.forEach(l => { if (l.d >= from && l.d < to) set.add(l.d); }); return set; }
const weekActs = (wk = weekKey()) => daysWithActivity(wk, addDays(wk, 7)).size;
function streak() {
  let n = 0; const m = mondayOf(new Date());
  if (weekActs(ymd(m)) >= 5) n++;
  m.setDate(m.getDate() - 7);
  for (let k = 0; k < 104; k++) { if (weekActs(ymd(m)) >= 5) { n++; m.setDate(m.getDate() - 7); } else break; }
  return n;
}
function checkWeekly() {
  const wk = weekKey();
  if (!S.wbonus[wk] && weekActs(wk) >= DATA.weekGoal) { S.wbonus[wk] = 1; addXP(150, 'Objectif de la semaine atteint'); pending.push({ kind: 'week' }); }
}
function testVals(k) { return S.tests.filter(t => num(t[k]) != null).sort((a, b) => a.d.localeCompare(b.d)).map(t => num(t[k])); }
function testDelta(k) { const v = testVals(k); return v.length >= 2 ? v[v.length - 1] - v[0] : null; }
const sumM = k => S.matches.reduce((a, m) => a + (m[k] || 0), 0);
function blockDone(n) {
  const b = DATA.blocks[n - 1], end = addDays(S.start, b.weeks[b.weeks.length - 1] * 7);
  return TODAY() >= end && S.log.some(l => l.d >= addDays(S.start, (b.weeks[0] - 1) * 7) && l.d < end);
}
function anyFullWeek() { const wks = {}; S.log.forEach(l => { const k = weekKey(D(l.d)); (wks[k] = wks[k] || new Set()).add(l.d); }); return Object.values(wks).some(s => s.size >= 7); }
const BTEST = {
  first: () => S.log.length >= 1, week7: anyFullWeek, streak3: () => streak() >= 3, streak6: () => streak() >= 6,
  s10: () => S.log.length >= 10, s25: () => S.log.length >= 25, s50: () => S.log.length >= 50,
  pr1: () => S.prs.length >= 1, pr10: () => S.prs.length >= 10,
  pullup: () => (S.hist['assisted-pullup'] || []).some(x => num(x.w) === 0),
  rocket: () => { const d = testDelta('t20'); return d != null && d <= -0.1; },
  spring: () => { const d = testDelta('broad'); return d != null && d >= 10; },
  weak: () => (S.hist['weak-foot-wall'] || []).length >= 5,
  juggle: () => testVals('jongle').some(v => v >= 50),
  match1: () => S.matches.length >= 1, goals5: () => sumM('goals') >= 5, assists5: () => sumM('assists') >= 5,
  recup: () => S.log.filter(l => l.kind === 'recup').length >= 4,
  b1: () => blockDone(1), b2: () => blockDone(2), b3: () => blockDone(3),
};
function checkBadges() {
  DATA.badges.forEach(b => {
    if (S.badges[b.id] || !BTEST[b.id]) return;
    let ok = false; try { ok = BTEST[b.id](); } catch (e) {}
    if (ok) { S.badges[b.id] = TODAY(); pending.push({ kind: 'badge', b }); }
  });
}
function afterEvent() { checkWeekly(); checkBadges(); save(); flushCele(); }

/* ---------------- nutrition helpers ---------------- */
const F = k => DATA.foods[k];
function kp(f, q) { const x = F(f); const m = x.per === 'g' ? q / 100 : q; return [x.kcal * m, x.p * m]; }
function mealTotals(items) { let k = 0, p = 0; for (const f in items) { const [a, b] = kp(f, items[f]); k += a; p += b; } return [k, p]; }
function mealsFor(dayName, opts = {}) {
  const md = DATA.meals.find(x => x.day === dayName);
  const wk = opts.wk || weekKey();
  const useAlt = md.alt && (opts.alt != null ? opts.alt : isMatchWeek(wk));
  const base = useAlt ? md.alt : md;
  const week = opts.fish || fishWeek();
  const meals = base.meals.map(m => m.fish ? Object.assign({ name: m.name, fish: true }, m[week]) : m);
  return { md, base, alt: !!useAlt, week, meals, target: base.target, tag: base.tag };
}
function foodDay(d = TODAY()) { if (!S.food[d]) S.food[d] = { eaten: {}, water: 0 }; return S.food[d]; }
function todayNutrition() {
  const { meals } = mealsFor(JOURS[new Date().getDay()]);
  const fd = S.food[TODAY()] || { eaten: {}, water: 0 };
  let P = 0, eP = 0, K = 0, eK = 0;
  meals.forEach((m, i) => { const [k, p] = mealTotals(m.items); P += p; K += k; if (fd.eaten[i]) { eP += p; eK += k; } });
  return { P, eP, K, eK, water: fd.water || 0 };
}
function nutritionXP() {
  const t = todayNutrition(), d = S.daily[TODAY()] || (S.daily[TODAY()] = {});
  if (!d.prot && t.P && t.eP >= t.P * 0.9) { d.prot = 1; addXP(20, 'Protéines du jour'); toast('Protéines du jour atteintes', 20); }
  if (!d.water && t.water >= 10) { d.water = 1; addXP(10, 'Hydratation'); toast('2,5 L d’eau bus', 10); }
}
