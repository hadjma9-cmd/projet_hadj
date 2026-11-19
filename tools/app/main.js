/* ---------------- onglets ---------------- */
const TABS = ['accueil', 'programme', 'repas', 'coach'];
let tab = TABS.includes(location.hash.slice(1)) ? location.hash.slice(1) : 'accueil';
function render() {
  document.querySelectorAll('.nav [data-tab]').forEach(b => b.setAttribute('aria-current', b.dataset.tab === tab ? 'page' : 'false'));
  view.className = '';
  ({ accueil: renderAccueil, programme: renderProgramme, repas: renderRepas, coach: renderCoach }[tab] || renderAccueil)();
}
function go(t) { tab = t; try { history.replaceState(null, '', '#' + t); } catch (e) {} render(); window.scrollTo(0, 0); }
function rerender() { const y = window.scrollY; render(); window.scrollTo(0, y); }
window.addEventListener('hashchange', () => { const h = location.hash.slice(1); if (TABS.includes(h) && h !== tab) { tab = h; render(); } });
function applyTheme() {
  let t = S.set.theme || 'auto';
  if (t === 'auto') t = window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', t);
  const m = document.querySelector('meta[name=theme-color]'); if (m) m.setAttribute('content', t === 'light' ? '#F2F3F6' : '#0A0D13');
}
try { window.matchMedia('(prefers-color-scheme: light)').addEventListener('change', () => { if (S.set.theme === 'auto') applyTheme(); }); } catch (e) {}

/* ---------------- pages ---------------- */
document.querySelector('.nav').addEventListener('click', e => { const b = e.target.closest('[data-tab]'); if (b) go(b.dataset.tab); });
view.addEventListener('click', e => {
  const t = e.target.closest('button'); if (!t) return;
  const d = t.dataset;
  if (d.act === 'start') { startDay(d.day); return; }
  if (d.act === 'done') { const v = dayView(dayByKey(d.day), sunOf(d.day, weekKey())); logDay(v.kind, v.name, v.col); toast('Bien joué !'); rerender(); return; }
  if (d.go) { if (d.day) progDay = d.day; go(d.go); return; }
  if (d.sheet) { openSheet(d.sheet); return; }
  if (d.exd) { openSheet('ex', d.exd); return; }
  if (d.exr) { openSheet('exr', d.exr); return; }
  if (d.sun) { sunMode[weekKey()] = d.sun; if (d.sun === 'match') S.match[weekKey()] = true; else delete S.match[weekKey()]; save(); rerender(); return; }
  if (d.day) { progDay = d.day; rerender(); return; }
  if (d.mtab) { mealTab = d.mtab; rerender(); return; }
  if (d.mday) { mealDay = d.mday; rerender(); return; }
  if (d.shop) { S.shop.checked[d.shop] = !S.shop.checked[d.shop]; save(); rerender(); return; }
  if (d.shopreset) { S.shop.checked = {}; save(); rerender(); return; }
  if (d.q) { askCoach(d.q); return; }
  if (t.id === 'newchat') { if (coachAbort) coachAbort.abort(); S.coach.msgs = []; save(); render(); return; }
});
view.addEventListener('submit', e => { e.preventDefault(); if (e.target.id === 'composer') { const ta = document.getElementById('ask'); const v = ta.value; ta.value = ''; askCoach(v); } });
view.addEventListener('input', e => { if (e.target.id === 'ask') { e.target.style.height = 'auto'; e.target.style.height = Math.min(140, e.target.scrollHeight) + 'px'; } });
view.addEventListener('keydown', e => { if (e.target.id === 'ask' && e.key === 'Enter' && !e.shiftKey && window.matchMedia('(pointer: fine)').matches) { e.preventDefault(); document.getElementById('composer').requestSubmit(); } });

/* ---------------- séance ---------------- */
WO.addEventListener('click', e => {
  const t = e.target.closest('button'); if (!t || !S.cur) return;
  const d = t.dataset, c = S.cur;
  if (d.var) { S.variant[d.var] = +d.i; save(); const y = WO.scrollTop; renderWO(); WO.scrollTop = y; return; }
  if (d.stp) { stepW(+d.stp); haptic(8); return; }
  const a = d.wo; if (!a) return;
  if (a === 'close') { closeWO(); return; }
  if (a === 'go') { c.step = 'ex'; if (!c.t0) c.t0 = Date.now(); save(); renderWO(); WO.scrollTop = 0; return; }
  if (a === 'set') { validateSet(); return; }
  if (a === 'hold') { const sec = +d.sec; unlockAudio(); wake(); if (!c.t0) c.t0 = Date.now(); startTimer(sec, 'hold', 'Garde la position', () => validateSet(sec)); return; }
  if (a === 'prev') { if (c.i > 0) { c.i--; save(); renderWO(); WO.scrollTop = 0; } return; }
  if (a === 'next') { c.i++; if (T.mode === 'rest') stopTimer(); save(); renderWO(); WO.scrollTop = 0; return; }
  if (a === 'end') { c.step = 'end'; stopTimer(); save(); renderWO(); WO.scrollTop = 0; return; }
  if (a === 'finish') { finishSession(); closeWO(); return; }
});
WO.addEventListener('change', e => { if (e.target.id === 'w-in' && S.cur) { const p = curPlan()[S.cur.i]; if (p) woW[p.sl.id + ':' + p.slug] = readW(); } });

/* ---------------- fiches ---------------- */
document.getElementById('sheet').addEventListener('click', e => {
  if (e.target.closest('[data-close]')) { closeSheet(); rerender(); return; }
  const t = e.target.closest('button'); if (!t) return;
  if (t.dataset.svar) { S.variant[t.dataset.svar] = +t.dataset.i; save(); openSheet('ex', t.dataset.svar); return; }
  if (t.dataset.theme) { S.set.theme = t.dataset.theme; save(); applyTheme(); openSheet('settings'); return; }
  if (t.id === 'backup') { const txt = JSON.stringify(S); (navigator.clipboard ? navigator.clipboard.writeText(txt) : Promise.reject()).then(() => toast('Sauvegarde copiée : colle-la dans tes notes.'), () => { document.getElementById('restore').hidden = false; const ta = document.getElementById('restoretxt'); ta.value = txt; ta.select(); }); return; }
  if (t.id === 'restoreopen') { const r = document.getElementById('restore'); r.hidden = !r.hidden; return; }
  if (t.id === 'restoredo') {
    try { const o = JSON.parse(document.getElementById('restoretxt').value); if (!o || typeof o !== 'object') throw 0;
      if (o.v === 3) S = Object.assign(BLANK(), o); else if (o.v === 2 || o.weights) migrateV2(o); else throw 0;
      if (!S.start) S.start = defaultStart(); save(); toast('Sauvegarde restaurée.'); closeSheet(); applyTheme(); render(); } catch (err) { toast('Cette sauvegarde n’est pas valide.'); }
  }
});
document.getElementById('sheet').addEventListener('change', e => {
  const el = e.target;
  if (el.id === 'sname') { S.name = el.value.trim().slice(0, 24); save(); }
  if (el.id === 'sstart' && el.value) { S.start = ymd(mondayOf(D(el.value))); el.value = S.start; save(); toast('Début : lundi ' + fmtDate(S.start)); }
  if (el.id === 'sbeep') { S.set.beep = el.checked; save(); }
  if (el.id === 'swake') { S.set.wake = el.checked; save(); }
  if (el.id === 'scode') { S.coach.code = el.value.trim(); save(); toast('Code enregistré.'); }
});
document.addEventListener('visibilitychange', () => {
  if (document.hidden) return;
  if (document.body.classList.contains('timer-on') && !tEl.classList.contains('go')) tickT();
  if (S.cur && WO.classList.contains('on')) wake();
  if (S.cur && S.cur.date !== TODAY()) { settleStale(); closeWO(); }
});

/* ---------------- démarrage ---------------- */
loadState(); applyTheme(); settleStale(); save();
render();
try { if ('serviceWorker' in navigator && location.protocol === 'https:' && !/claude/.test(location.hostname)) navigator.serviceWorker.register('sw.js').catch(() => {}); } catch (e) {}
