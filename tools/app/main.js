/* ---------------- render / tabs ---------------- */
const TABS = ['accueil', 'programme', 'repas', 'progres', 'coach'];
let tab = TABS.includes(location.hash.slice(1)) ? location.hash.slice(1) : 'accueil';
function render() {
  document.querySelectorAll('.nav [data-tab]').forEach(b => b.setAttribute('aria-current', b.dataset.tab === tab ? 'page' : 'false'));
  ({ accueil: renderAccueil, programme: renderProgramme, repas: renderRepas, progres: renderProgres, coach: renderCoach }[tab] || renderAccueil)();
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

/* ---------------- events : pages ---------------- */
document.querySelector('.nav').addEventListener('click', e => { const b = e.target.closest('[data-tab]'); if (b) go(b.dataset.tab); });
view.addEventListener('click', e => {
  const t = e.target.closest('button, a[data-go]'); if (!t) return;
  const d = t.dataset;
  if (d.act) { if (d.act === 'resume') openWO(); else startDay(d.day || todayKey()); return; }
  if (d.go) { if (d.day) { progDay = d.day; sunView = null; openEx.clear(); } go(d.go); return; }
  if (d.sheet) { openSheet(d.sheet); return; }
  if (d.welcome) { S.welcomed = true; save(); rerender(); return; }
  if (d.match != null) { const wk = weekKey(); if (d.match === '1') S.match[wk] = true; else delete S.match[wk]; save(); rerender(); toast(d.match === '1' ? 'Semaine de match : vendredi, samedi et repas adaptés' : 'Dimanche : séance technique'); return; }
  if (d.water) { const fd = foodDay(); fd.water = Math.max(0, Math.min(20, fd.water + +d.water)); if (+d.water > 0) haptic(10); nutritionXP(); afterEvent(); rerender(); return; }
  if (d.day && !d.act) { progDay = d.day; sunView = null; openEx.clear(); rerender(); return; }
  if (d.sun) { sunView = d.sun; rerender(); return; }
  if (d.ex) { openEx.has(d.ex) ? openEx.delete(d.ex) : openEx.add(d.ex); rerender(); return; }
  if (d.mtab) { mealTab = d.mtab; rerender(); return; }
  if (d.mday) { mealDay = d.mday; fishView = null; altView = null; rerender(); return; }
  if (d.fish) { fishView = d.fish; rerender(); return; }
  if (d.alt != null) { altView = d.alt === '1'; rerender(); return; }
  if (d.eat != null) { const fd = foodDay(); fd.eaten[d.eat] = !fd.eaten[d.eat]; nutritionXP(); afterEvent(); rerender(); return; }
  if (d.shop) { S.shop.checked[d.shop] = !S.shop.checked[d.shop]; save(); rerender(); return; }
  if (d.shopreset) { S.shop.checked = {}; save(); rerender(); return; }
  if (d.q) { askCoach(d.q); return; }
  if (t.id === 'newchat') { if (coachAbort) coachAbort.abort(); S.coach.msgs = []; save(); render(); return; }
});
view.addEventListener('submit', e => {
  e.preventDefault();
  if (e.target.id === 'composer') { const ta = document.getElementById('ask'); const v = ta.value; ta.value = ''; askCoach(v); }
  if (e.target.id === 'bodyform') {
    const kg = num(document.getElementById('kg').value), waist = num(document.getElementById('waist').value);
    if (kg == null || kg < 30 || kg > 250) { toast('Entre ton poids en kg, par exemple 81,6.'); return; }
    S.body = S.body.filter(b => b.d !== TODAY()); S.body.push(Object.assign({ d: TODAY(), kg }, waist ? { waist } : {}));
    S.body.sort((a, b) => a.d.localeCompare(b.d));
    const dd = S.daily[TODAY()] || (S.daily[TODAY()] = {}); if (!dd.weigh) { dd.weigh = 1; addXP(10, 'Pesée'); toast('Poids enregistré', 10); } else toast('Poids mis à jour');
    afterEvent(); rerender();
  }
});
view.addEventListener('input', e => { if (e.target.id === 'ask') { e.target.style.height = 'auto'; e.target.style.height = Math.min(140, e.target.scrollHeight) + 'px'; } });
view.addEventListener('keydown', e => { if (e.target.id === 'ask' && e.key === 'Enter' && !e.shiftKey && window.matchMedia('(pointer: fine)').matches) { e.preventDefault(); document.getElementById('composer').requestSubmit(); } });

/* ---------------- events : workout ---------------- */
WO.addEventListener('click', e => {
  const t = e.target.closest('button'); if (!t || !S.cur) return;
  const d = t.dataset, c = S.cur;
  if (d.rd) { (c.rd = c.rd || {})[d.rd] = +d.v; save(); const y = WO.scrollTop; renderWO(); WO.scrollTop = y; return; }
  if (d.warm != null) { c.warm[d.warm] = !c.warm[d.warm]; save(); const y = WO.scrollTop; renderWO(); WO.scrollTop = y; return; }
  if (d.var) { S.variant[d.var] = +d.i; save(); const y = WO.scrollTop; renderWO(); WO.scrollTop = y; return; }
  if (d.stp) { stepInput(d.stp, +d.d); return; }
  if (d.fb) { setFeedback(d.fb); return; }
  if (d.rpe) { c.rpe = +d.rpe; save(); const y = WO.scrollTop; renderWO(); WO.scrollTop = y; return; }
  if (d.chk) { c.checks[d.chk] = !c.checks[d.chk]; if (!c.t0) c.t0 = Date.now(); save(); const y = WO.scrollTop; renderWO(); WO.scrollTop = y; return; }
  if (d.howr) { c.open = c.open === d.howr ? null : d.howr; const y = WO.scrollTop; renderWO(); WO.scrollTop = y; return; }
  if (d.mset) { c.m[d.mset] = +d.v; save(); const y = WO.scrollTop; renderWO(); WO.scrollTop = y; return; }
  if (d.mstp) { c.m[d.mstp] = Math.max(0, Math.min(20, (c.m[d.mstp] || 0) + +d.d)); save(); const y = WO.scrollTop; renderWO(); WO.scrollTop = y; return; }
  const a = d.wo; if (!a) return;
  if (a === 'close') { closeWO(); return; }
  if (a === 'skipready') { c.ready = null; c.step = 'warm'; save(); renderWO(); WO.scrollTop = 0; return; }
  if (a === 'readyok') { const sc = DATA.ready.reduce((s, q) => s + (c.rd[q.k] || 0), 0); c.ready = { score: sc }; S.ready[TODAY()] = { score: sc, ans: c.rd }; c.step = 'warm'; save(); renderWO(); WO.scrollTop = 0; return; }
  if (a === 'warmok') { c.step = curInfo().test && c.day === 'vendredi' && !c.tested && !curInfo().before ? 'tests' : 'ex'; if (!c.t0) c.t0 = Date.now(); save(); renderWO(); WO.scrollTop = 0; return; }
  if (a === 'skiptests') { c.step = 'ex'; save(); renderWO(); WO.scrollTop = 0; return; }
  if (a === 'testsok') { if (saveTests(readTests(document.getElementById('wotests')))) { c.tested = true; c.step = 'ex'; save(); renderWO(); WO.scrollTop = 0; } return; }
  if (a === 'set') { validateSet(); return; }
  if (a === 'hold') { startHold(); return; }
  if (a === 'prev') { if (c.i > 0) { c.i--; save(); renderWO(); WO.scrollTop = 0; } return; }
  if (a === 'next') { c.i++; save(); stopTimerIfRest(); renderWO(); WO.scrollTop = 0; return; }
  if (a === 'tosum') { c.step = 'sum'; stopTimer(); save(); renderWO(); WO.scrollTop = 0; return; }
  if (a === 'back') { c.step = 'ex'; save(); renderWO(); WO.scrollTop = 0; return; }
  if (a === 'cancel') { if (t.dataset.armed) { S.cur = null; save(); closeWO(); toast('Séance annulée'); } else { t.dataset.armed = '1'; t.textContent = 'Touche encore pour annuler'; } return; }
  if (a === 'finish') { finishSession(c.rpe || null); closeWO(); afterEvent(); return; }
  if (a === 'recupok') { const n = Object.values(c.checks).filter(Boolean).length; c.kind = 'recup'; finishSession(null); closeWO(); if (n >= 3) toast('Récup validée', 50); afterEvent(); return; }
  if (a === 'footok') { saveFoot(); return; }
  if (a === 'matchok') { saveMatch(); return; }
});
WO.addEventListener('toggle', e => { if (e.target.id === 'howfold') exOpenHow = e.target.open; }, true);
WO.addEventListener('change', e => {
  if (!S.cur || S.cur.step !== 'ex') return;
  if (e.target.id === 'w-in' || e.target.id === 'r-in') { const p = curPlan()[S.cur.i]; if (p) { const r = readInputs(); woIn[p.sl.id + ':' + p.slug] = { w: r.w, r: r.r }; } }
});
function stopTimerIfRest() { if (T.mode === 'rest') stopTimer(); }

/* ---------------- events : sheet, celebration ---------------- */
document.getElementById('sheet').addEventListener('click', e => {
  if (e.target.closest('[data-close]')) { closeSheet(); render(); return; }
  const t = e.target.closest('button'); if (!t) return;
  if (t.dataset.theme) { S.set.theme = t.dataset.theme; save(); applyTheme(); openSheet('settings'); return; }
  if (t.id === 'backup') { const txt = JSON.stringify(S); (navigator.clipboard ? navigator.clipboard.writeText(txt) : Promise.reject()).then(() => toast('Sauvegarde copiée : colle-la dans tes notes.'), () => { const ta = document.getElementById('restoretxt'); document.getElementById('restore').hidden = false; ta.value = txt; ta.select(); toast('Copie la sauvegarde affichée.'); }); return; }
  if (t.id === 'restoreopen') { const r = document.getElementById('restore'); r.hidden = !r.hidden; return; }
  if (t.id === 'restoredo') {
    try { const o = JSON.parse(document.getElementById('restoretxt').value); if (!o || typeof o !== 'object') throw 0;
      if (o.v === 3) { const b = BLANK(); S = Object.assign(b, o); } else if (o.v === 2 || o.weights) migrateV2(o); else throw 0;
      if (!S.start) S.start = defaultStart(); save(); toast('Sauvegarde restaurée.'); closeSheet(); applyTheme(); render(); } catch (err) { toast('Cette sauvegarde n’est pas valide.'); }
    return;
  }
  if (t.id === 'newcycle') { if (t.dataset.armed) { S.start = defaultStart(); if (S.start <= TODAY()) { const m = mondayOf(new Date()); m.setDate(m.getDate() + 7); S.start = ymd(m); } save(); closeSheet(); toast('Nouveau cycle : il commence le ' + fmtDate(S.start)); render(); } else { t.dataset.armed = '1'; t.textContent = 'Touche encore : le cycle repart lundi prochain'; } return; }
  if (t.id === 'wipe') { if (t.dataset.armed) { try { localStorage.removeItem(KEY); localStorage.removeItem(KEY2); localStorage.removeItem(KEY1); } catch (e2) {} location.reload(); } else { t.dataset.armed = '1'; t.textContent = 'Touche encore pour tout effacer'; setTimeout(() => { if (t.isConnected) { delete t.dataset.armed; t.textContent = 'Tout effacer'; } }, 4000); } return; }
  if (t.id === 'testsave') { if (saveTests(readTests(document.getElementById('sheetp')))) { closeSheet(); afterEvent(); render(); } return; }
});
document.getElementById('sheet').addEventListener('change', e => {
  const el = e.target;
  if (el.id === 'sname') { S.name = el.value.trim().slice(0, 24); save(); }
  if (el.id === 'sstart' && el.value) { S.start = ymd(mondayOf(D(el.value))); el.value = S.start; save(); toast('Début du cycle : lundi ' + fmtDate(S.start)); }
  if (el.id === 'sbeep') { S.set.beep = el.checked; save(); }
  if (el.id === 'swake') { S.set.wake = el.checked; save(); }
  if (el.id === 'scode') { S.coach.code = el.value.trim(); save(); toast('Code enregistré.'); }
});
document.getElementById('cele').addEventListener('click', e => { if (e.target.closest('[data-cele]')) { document.getElementById('cele').classList.remove('on'); setTimeout(flushCele, 250); } });
document.addEventListener('visibilitychange', () => {
  if (document.hidden) return;
  if (document.body.classList.contains('timer-on') && !tEl.classList.contains('go')) tickT();
  if (S.cur && WO.classList.contains('on')) wake();
  if (S.cur && S.cur.date !== TODAY()) { settleStale(); closeWO(); }
});

/* ---------------- init ---------------- */
loadState(); applyTheme(); settleStale(); save();
render();
if (location.hash === '#coach') go('coach');
if (S.cur && S.cur.date === TODAY() && hasProgress()) toast('Ta séance en cours est gardée : touche « Reprendre ».');
try { if ('serviceWorker' in navigator && location.protocol === 'https:' && !/claude/.test(location.hostname)) navigator.serviceWorker.register('sw.js').catch(() => {}); } catch (e) {}
