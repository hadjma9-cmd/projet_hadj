"use strict";
const DATA = /*DATA*/null;
const KEY = 'n10-v3', KEY2 = 'muscu-app-v2', KEY1 = 'muscu-app-v1';
const view = document.getElementById('view');
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
const num = v => { if (v == null || v === '') return null; const n = parseFloat(String(v).replace(',', '.')); return isFinite(n) ? n : null; };
const fr0 = n => Math.round(n).toLocaleString('fr-FR');
const frn = n => (Math.round(n * 100) / 100).toLocaleString('fr-FR');
function mondayOf(d) { const x = new Date(d); x.setHours(12, 0, 0, 0); x.setDate(x.getDate() - ((x.getDay() + 6) % 7)); return x; }
const weekKey = (d = new Date()) => ymd(mondayOf(d));
function defaultStart() { const d = new Date(); const i = (d.getDay() + 6) % 7; const m = mondayOf(d); if (i >= 4) m.setDate(m.getDate() + 7); return ymd(m); }
function isoWeek(d) { const t = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate())); const day = t.getUTCDay() || 7; t.setUTCDate(t.getUTCDate() + 4 - day); const y0 = new Date(Date.UTC(t.getUTCFullYear(), 0, 1)); return Math.ceil(((t - y0) / 864e5 + 1) / 7); }
const fishWeek = () => isoWeek(new Date()) % 2 === 0 ? 'A' : 'B';

/* ---------------- state (les anciennes données restent dans le stockage) ---------------- */
const BLANK = () => ({ v: 3, start: null, name: '', variant: {}, weights: {}, hist: {}, cur: null, log: [], checks: {}, match: {}, food: {}, body: [], shop: {},
  coach: { code: '', msgs: [] }, set: { beep: true, wake: true, theme: 'auto' }, migrated: null });
let S = BLANK();
const DAYS = DATA.days, EXD = DATA.ex;
const dayByKey = k => DAYS.find(d => d.key === k);
const todayKey = () => KEYS[new Date().getDay()];
function slotOptions(sl) { return [sl.ex].concat(sl.alts || []); }
function slotSlug(sl) { const o = slotOptions(sl); return o[Math.min(S.variant[sl.id] || 0, o.length - 1)]; }
function allSlots() { const out = []; DAYS.forEach(d => (d.slots || []).concat((d.tech && d.tech.slots) || []).forEach(s => out.push(s))); return out; }
const slotById = id => allSlots().find(s => s.id === id);

function mapV2Variants(v2v) {
  const out = {}; v2v = v2v || {};
  allSlots().forEach(sl => {
    const i = v2v[sl.ex]; if (!i) return;
    const j = slotOptions(sl).indexOf([sl.ex].concat(DATA.v2alts[sl.ex] || [])[i]);
    if (j > 0) out[sl.id] = j;
  });
  return out;
}
function migrateV2(o) {
  const b = BLANK();
  b.start = o.start || null; b.weights = o.weights || {}; b.hist = o.hist || {};
  b.food = o.food || {}; b.body = Array.isArray(o.body) ? o.body : [];
  b.coach = Object.assign(b.coach, o.coach || {}); b.set = Object.assign(b.set, o.set || {});
  b.variant = mapV2Variants(o.variant); b.layout = 'simple';
  b.log = (o.log || []).map(l => ({ d: l.d, day: 'v2', kind: 'gym', name: DATA.v2days[l.day] || 'Séance', col: 'hautA', done: l.done, total: l.total, min: l.min || null }));
  b.migrated = 'v2';
  S = b;
}
function loadState() {
  let raw = null;
  try { raw = localStorage.getItem(KEY); } catch (e) {}
  if (raw) {
    try { const o = JSON.parse(raw); S = Object.assign(BLANK(), o); S.set = Object.assign(BLANK().set, o.set || {}); S.coach = Object.assign({ code: '', msgs: [] }, o.coach || {}); } catch (e) {}
  } else {
    let v2 = null, v1 = null;
    try { v2 = localStorage.getItem(KEY2); v1 = localStorage.getItem(KEY1); } catch (e) {}
    if (v2) { try { migrateV2(JSON.parse(v2)); } catch (e) {} }
    else if (v1) { try { const o = JSON.parse(v1); for (const k in (o.weights || {})) if (o.weights[k]) S.weights[k] = o.weights[k]; S.migrated = 'v1'; } catch (e) {} }
  }
  if (!S.start) S.start = defaultStart();
  if (S.layout !== 'simple') {
    let v2 = null; try { v2 = JSON.parse(localStorage.getItem(KEY2) || 'null'); } catch (e) {}
    S.variant = mapV2Variants(v2 && v2.variant); S.layout = 'simple';
  }
  const lim = addDays(TODAY(), -21);
  for (const d in (S.food || {})) if (d < lim) delete S.food[d];
  if (!S.checks || typeof S.checks !== 'object') S.checks = {};
  const lim2 = addDays(TODAY(), -120);
  for (const d in S.checks) if (d < lim2) delete S.checks[d];
  S.cur = null;
  // les séances déjà validées dans l'ancienne version apparaissent cochées
  S.log.forEach(l => {
    if (S.checks[l.d] || l.d < weekKey() || l.d > addDays(weekKey(), 6)) return;
    const k = KEYS[D(l.d).getDay()];
    S.checks[l.d] = k === 'dimanche' ? (l.kind === 'match' ? ['m1'] : dayIds('dimanche')) : dayIds(k);
  });
}
const save = () => { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) {} };

/* ---------------- programme ---------------- */
function progWeek(s = TODAY()) { const n = Math.floor((D(s) - D(S.start)) / 864e5); return n < 0 ? 0 : Math.floor(n / 7) + 1; }
function weekInfo(real = progWeek()) {
  const w = Math.min(12, Math.max(1, real));
  return { real, w, block: w <= 4 ? 0 : w <= 8 ? 1 : 2, learn: DATA.learn.includes(w), deload: DATA.deload.includes(w), before: real === 0, after: real > 12 };
}
const isMatchWeek = (wk = weekKey()) => !!S.match[wk];
function dayView(day, mode) {
  if (day.kind !== 'sunday') return Object.assign({}, day);
  const m = mode ? mode === 'match' : isMatchWeek();
  return Object.assign({}, day, m ? day.match : day.tech, { key: day.key, kind: m ? 'match' : 'tech' });
}
function presc(sl, info) {
  const base = sl.p[info.block]; if (!base) return null;
  let [sets, reps, rest] = base;
  if (info.learn && ['force', 'core', 'plyo'].includes(sl.kind) && sets > 2) sets = 2;
  if (info.deload) sets = Math.max(1, sets - 1);
  return { sets, reps, rest };
}
function planFor(day, mode, info = weekInfo()) {
  const v = dayView(day, mode);
  return (v.slots || []).map(sl => ({ sl, slug: slotSlug(sl), pr: presc(sl, info) })).filter(p => p.pr);
}
function repsFor(sl, slug, pr) { const e = EXD[slug]; return slug !== sl.ex && e.reps && !/\d\s*s\b/.test(pr.reps) ? e.reps : pr.reps; }
function topOf(reps) { const s = String(reps); if (/min|\bm\b/.test(s)) return null; const m = s.match(/(\d+)(?:\s*[–-]\s*(\d+))?/); return m ? +(m[2] || m[1]) : null; }
function modeOf(sl, slug, reps) {
  if (['plyo', 'sprint', 'cod', 'ball'].includes(sl.kind) || EXD[slug].eq === 'velo') return 'drill';
  if (/\d\s*s\b/.test(reps) && !/×/.test(reps)) return 'hold';
  return EXD[slug].step ? 'load' : 'reps';
}
const restTxt = s => !s ? '' : s >= 60 ? (s % 60 ? Math.floor(s / 60) + ' min ' + (s % 60) : s / 60 + ' min') : s + ' s';
const exName = slug => (EXD[slug] && EXD[slug].name) || DATA.oldnames[slug] || slug;
const exStep = slug => EXD[slug] ? EXD[slug].step : 1;
const exNeg = slug => !!(EXD[slug] && EXD[slug].neg);
function lastLoad(slug) { const h = (S.hist[slug] || []).filter(x => x.d !== TODAY() && num(x.w) != null); return h.length ? num(h[h.length - 1].w) : num(S.weights[slug]); }
function recordHist(slug, patch) {
  const h = S.hist[slug] || (S.hist[slug] = []);
  let e = h.find(x => x.d === TODAY());
  if (!e) { e = { d: TODAY() }; h.push(e); }
  Object.assign(e, patch);
  if (h.length > 80) h.splice(0, h.length - 80);
}
/* ---------------- cases à cocher (une par exercice) ---------------- */
const dateOf = k => addDays(weekKey(), ORDER.indexOf(k));
const checked = (d, id) => !!(S.checks[d] && S.checks[d].includes(id));
function dayIds(k) {
  const day = dayByKey(k);
  if (day.kind === 'foot') return ['f1'];
  if (day.kind === 'recup') return day.items.map(it => it.id);
  if (day.kind === 'sunday') return (S.match[weekKey()] ? ['m1'] : []).concat(dayByKey('mardi').slots.map(s => s.id));
  if (day.kind === 'rest') return [];
  return day.slots.map(s => s.id);
}
function dayDone(k) {
  const d = dateOf(k);
  const ids = dayIds(k);
  return ids.length > 0 && ids.every(id => checked(d, id));
}
function toggleCheck(k, id) {
  const d = dateOf(k), was = dayDone(k);
  const a = S.checks[d] || (S.checks[d] = []);
  const i = a.indexOf(id);
  if (i >= 0) a.splice(i, 1); else a.push(id);
  if (!a.length) delete S.checks[d];
  const now = dayDone(k);
  if (now !== was) {   // l'historique garde les jours faits
    S.log = S.log.filter(l => l.d !== d);
    if (now) {
      const day = dayByKey(k), match = k === 'dimanche' && checked(d, 'm1');
      const v = k === 'dimanche' ? (match ? day.match : day.tech) : day;
      S.log.push({ d, day: k, kind: k === 'dimanche' ? (match ? 'match' : 'tech') : day.kind, name: v.name, col: v.col || day.col });
      S.log.sort((x, y) => x.d.localeCompare(y.d));
      if (S.log.length > 500) S.log.splice(0, S.log.length - 500);
    }
  }
  save();
  return now && !was;
}
/* ---------------- poids notés ---------------- */
const histOn = (slug, d) => { const e = (S.hist[slug] || []).find(x => x.d === d); return e ? num(e.w) : null; };
function lastBefore(slug, d) {
  const h = (S.hist[slug] || []).filter(x => x.d < d && num(x.w) != null);
  return h.length ? num(h[h.length - 1].w) : num(S.weights[slug]);
}
function setW(slug, d, w) {
  const h = S.hist[slug] || (S.hist[slug] = []);
  let e = h.find(x => x.d === d);
  if (w == null) { if (e) { delete e.w; if (Object.keys(e).length === 1) h.splice(h.indexOf(e), 1); } }
  else { if (!e) { e = { d }; h.push(e); h.sort((a, b) => a.d.localeCompare(b.d)); } e.w = w; }
  if (h.length > 80) h.splice(0, h.length - 80);
  if (!h.length) delete S.hist[slug];
  save();
}

/* ---------------- repas ---------------- */
const F = k => DATA.foods[k];
function kp(f, q) { const x = F(f); const m = x.per === 'g' ? q / 100 : q; return [x.kcal * m, x.p * m]; }
function mealsFor(dayName) {
  const md = DATA.meals.find(x => x.day === dayName), week = fishWeek();
  return { md, week, meals: md.meals.map(m => m.fish ? Object.assign({ name: m.name, fish: true }, m[week]) : m) };
}
