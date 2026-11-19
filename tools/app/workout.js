/* ---------------- séance ---------------- */
let woTick = null, woW = {};
const curDay = () => dayByKey(S.cur.day);
const curView = () => dayView(curDay(), S.cur.mode);
const curPlan = () => planFor(curDay(), S.cur.mode, weekInfo(S.cur.w || progWeek()));
function startDay(dk) {
  const day = dayByKey(dk || todayKey()), mode = sunOf(day.key, weekKey());
  if (S.cur && S.cur.date === TODAY() && S.cur.day === day.key) { openWO(); return; }
  S.cur = { day: day.key, mode, date: TODAY(), w: progWeek(), step: 'warm', i: 0, sets: {}, t0: 0 };
  woW = {}; save(); openWO();
}
function openWO() { WO.classList.add('on'); document.body.classList.add('wo-on'); renderWO(); WO.scrollTop = 0; clearInterval(woTick); woTick = setInterval(updClock, 1000); wake(); }
function closeWO() { WO.classList.remove('on'); document.body.classList.remove('wo-on'); clearInterval(woTick); stopTimer(); render(); }
function updClock() { const el = WO.querySelector('.clock'); if (!el || !S.cur) return; const s = S.cur.t0 ? Math.floor((Date.now() - S.cur.t0) / 1000) : 0; el.textContent = Math.floor(s / 60) + ':' + p2(s % 60); }
const footBar = inner => `<div class="wo-foot"><div>${inner}</div></div>`;
function woTop(sub) { return `<div class="wo-top"><button type="button" class="ico-btn" data-wo="close" aria-label="Quitter (ta séance est gardée)">${I.close}</button><div class="ttl"><b>${esc(curView().name)}</b><small>${esc(sub || '')}</small></div><span class="clock">0:00</span></div>`; }
function renderWO() {
  if (!S.cur) { closeWO(); return; }
  WO.className = 'on c-' + curView().col;
  const st = S.cur.step;
  WO.innerHTML = `<div class="wo-in">${st === 'warm' ? woWarm() : st === 'end' ? woEnd() : woEx()}</div>`;
  updClock();
}
function woWarm() {
  const v = curView();
  return `${woTop('Échauffement')}<h1 class="wo-h">Échauffement</h1><p class="wo-sub">5 minutes pour éviter les blessures.</p>
    <ol class="warm">${(DATA.warmup[v.warm] || []).map(w => `<li>${esc(w)}</li>`).join('')}</ol>
    ${footBar(`<button type="button" class="btn" data-wo="go">C’est parti</button>`)}`;
}
function woEx() {
  const c = S.cur, plan = curPlan(), N = plan.length;
  if (!N) { c.step = 'end'; return woEnd(); }
  c.i = Math.max(0, Math.min(N - 1, c.i));
  const p = plan[c.i], sl = p.sl, slug = p.slug, e = EXD[slug];
  const reps = repsFor(sl, slug, p.pr), mode = modeOf(sl, slug, reps);
  const arr = c.sets[sl.id] || [], n = p.pr.sets, complete = arr.length >= n, isLast = c.i === N - 1;
  const total = plan.reduce((a, q) => a + q.pr.sets, 0), done = plan.reduce((a, q) => a + Math.min(q.pr.sets, (c.sets[q.sl.id] || []).length), 0);
  const opts = slotOptions(sl);
  const vsw = opts.length > 1 ? `<div class="vsw"><small>Si c’est pris</small>${opts.map((o, i) => `<button type="button" data-var="${sl.id}" data-i="${i}" aria-pressed="${o === slug}">${esc(EXD[o].short || EXD[o].name)}</button>`).join('')}</div>` : '';
  const k = sl.id + ':' + slug;
  if (woW[k] === undefined) {
    let w0 = arr.length && arr[arr.length - 1].w != null ? arr[arr.length - 1].w : lastLoad(slug);
    if (w0 == null && e.step && e.start && !/Poids du corps|seule/.test(e.start)) { const ns = String(e.start).match(/\d+(?:[.,]\d+)?/g) || []; if (ns.length) w0 = num(exNeg(slug) ? ns[ns.length - 1] : ns[0]); }
    woW[k] = w0;
  }
  const load = mode === 'load' && !complete ? `<div class="load"><span>Charge</span><button type="button" data-stp="-1" aria-label="Moins lourd">−</button><input id="w-in" inputmode="decimal" autocomplete="off" placeholder="—" value="${woW[k] != null ? frn(woW[k]) : ''}"><button type="button" data-stp="1" aria-label="Plus lourd">+</button><span>kg${exNeg(slug) ? ' (contrepoids)' : ''}</span></div>` : '';
  const sec = mode === 'hold' ? (topOf(reps) || 30) : 0;
  const unit = mode === 'drill' ? 'Répétition' : 'Série';
  let main;
  if (complete) main = `<button type="button" class="btn ${isLast ? 'ok' : ''}" data-wo="${isLast ? 'end' : 'next'}">${isLast ? 'Terminer la séance' : 'Exercice suivant'}</button>`;
  else if (mode === 'hold') main = `<button type="button" class="btn" data-wo="hold" data-sec="${sec}">${I.play}Lancer ${sec} s</button>`;
  else main = `<button type="button" class="btn" data-wo="set">${unit} faite ✓</button>`;
  return `${woTop(`Exercice ${c.i + 1} sur ${N}`)}
    <div class="wo-prog"><i style="width:${total ? done / total * 100 : 0}%"></i></div>
    ${artHtml(e)}
    <h1 class="wo-h" style="margin-top:14px">${esc(e.name)}</h1>
    <p class="presc-l">${prescText(p)}</p>
    ${vsw}
    <div class="dots">${Array.from({ length: n }, (_, j) => `<i class="${j < arr.length ? 'on' : ''}${j === arr.length && !complete ? ' cur' : ''}"></i>`).join('')}</div>
    <div class="setlab"${complete ? ' style="color:var(--ok)"' : ''}>${complete ? 'Terminé ✓' : `${unit} ${arr.length + 1} sur ${n}`}</div>
    ${load}
    ${guideHtml(e)}
    ${footBar(`<button type="button" class="nb" data-wo="prev" aria-label="Exercice précédent" ${c.i === 0 ? 'disabled style="opacity:.35"' : ''}>${I.left}</button>${main}<button type="button" class="nb" data-wo="next" aria-label="Exercice suivant" ${isLast ? 'disabled style="opacity:.35"' : ''}>${I.right}</button>`)}`;
}
function woEnd() {
  const c = S.cur, min = c.t0 ? Math.max(1, Math.round((Date.now() - c.t0) / 60000)) : 0;
  return `${woTop('Fin')}<div class="sum-hero"><div class="trophy">💪</div><h2>Séance terminée</h2><p>${min ? min + ' minute' + (min > 1 ? 's' : '') + '. ' : ''}Bien joué, à la prochaine.</p></div>
    ${footBar(`<button type="button" class="btn ok" data-wo="finish">Fermer</button>`)}`;
}
function readW() { const el = WO.querySelector('#w-in'); return el ? num(el.value) : null; }
function stepW(d) {
  const p = curPlan()[S.cur.i], k = p.sl.id + ':' + p.slug, st = exStep(p.slug) || 1;
  let v = readW(); if (v == null) v = woW[k] != null ? woW[k] : 0;
  woW[k] = Math.max(0, Math.round((v + d * st) * 100) / 100);
  const el = WO.querySelector('#w-in'); if (el) el.value = frn(woW[k]);
}
function validateSet(secs) {
  const c = S.cur, plan = curPlan(), p = plan[c.i]; if (!p) return;
  const sl = p.sl, slug = p.slug, reps = repsFor(sl, slug, p.pr), mode = modeOf(sl, slug, reps);
  const arr = c.sets[sl.id] || (c.sets[sl.id] = []);
  if (arr.length >= p.pr.sets) return;
  const rec = {};
  if (mode === 'load') { const w = readW(); if (w != null) { rec.w = w; S.weights[slug] = String(w); woW[sl.id + ':' + slug] = w; } }
  if (secs) rec.r = secs;
  arr.push(rec); if (!c.t0) c.t0 = Date.now();
  unlockAudio(); wake(); haptic(25);
  const done = arr.length >= p.pr.sets;
  if (done) {
    const loads = arr.map(s => s.w).filter(x => x != null);
    recordHist(slug, loads.length ? { w: String(exNeg(slug) ? Math.min(...loads) : Math.max(...loads)) } : { r: arr.length });
  }
  save(); const y = WO.scrollTop; renderWO(); WO.scrollTop = done ? 0 : y;
  if (!done && p.pr.rest) startTimer(p.pr.rest, 'rest', `${mode === 'drill' ? 'Répétition' : 'Série'} ${arr.length + 1} sur ${p.pr.sets}`);
  else if (done && c.i < plan.length - 1) startTimer(Math.min(90, Math.max(30, p.pr.rest || 60)), 'rest', 'Ensuite : ' + EXD[plan[c.i + 1].slug].name);
}
function finishSession() {
  const c = S.cur; if (!c) return;
  const v = dayView(dayByKey(c.day), c.mode);
  const done = Object.values(c.sets).reduce((a, x) => a + x.length, 0);
  if (done) logDay(v.kind, v.name, v.col, { min: c.t0 ? Math.max(1, Math.round((Date.now() - c.t0) / 60000)) : null, done });
  S.cur = null; save();
}
function settleStale() { if (S.cur && S.cur.date !== TODAY()) { S.cur = null; save(); } }

/* ---------------- chrono, son, écran ---------------- */
let T = { end: 0, len: 0, int: null, hide: null, mode: 'rest', cb: null, seq: null };
let AC = null, WL = null;
const tEl = document.getElementById('timer');
function unlockAudio() { try { if (!AC) AC = new (window.AudioContext || window.webkitAudioContext)(); if (AC.state === 'suspended') AC.resume(); } catch (e) {} }
function beep(n = 3) { if (!S.set.beep || !AC) return; try { const t = AC.currentTime; for (let i = 0; i < n; i++) { const dt = i * 0.22, o = AC.createOscillator(), g = AC.createGain(); o.frequency.value = i === n - 1 ? 1046 : 784; o.connect(g); g.connect(AC.destination); g.gain.setValueAtTime(.0001, t + dt); g.gain.exponentialRampToValueAtTime(.35, t + dt + .02); g.gain.exponentialRampToValueAtTime(.0001, t + dt + .18); o.start(t + dt); o.stop(t + dt + .2); } } catch (e) {} }
const haptic = ms => { try { navigator.vibrate && navigator.vibrate(ms); } catch (e) {} };
async function wake() { if (!S.set.wake || WL || !('wakeLock' in navigator)) return; try { WL = await navigator.wakeLock.request('screen'); WL.addEventListener('release', () => { WL = null; }); } catch (e) {} }
function startTimer(sec, mode, next, cb) {
  clearTimeout(T.hide); clearInterval(T.int);
  T.len = sec; T.end = Date.now() + sec * 1000; T.mode = mode; T.cb = cb || null;
  tEl.className = ''; document.body.classList.add('timer-on');
  document.getElementById('tlbl').textContent = mode === 'hold' ? 'Tiens bon' : 'Repos';
  document.getElementById('tnext').textContent = next || '';
  document.getElementById('tplus').textContent = mode === 'hold' ? 'Terminer' : '+15 s';
  document.getElementById('tskip').textContent = mode === 'hold' ? 'Annuler' : 'Passer';
  tickT(); T.int = setInterval(tickT, 200);
}
function tickT() {
  const ms = Math.max(0, T.end - Date.now()), s = Math.ceil(ms / 1000);
  document.getElementById('tval').textContent = Math.floor(s / 60) + ':' + p2(s % 60);
  document.getElementById('tring').style.strokeDashoffset = (251.3 * (1 - ms / (T.len * 1000))).toFixed(1);
  if (ms > 0) return;
  clearInterval(T.int);
  if (T.mode === 'hold') { beep(2); haptic([120, 60, 120]); const cb = T.cb; T.cb = null; document.body.classList.remove('timer-on'); if (cb) cb(); return; }
  tEl.classList.add('go'); document.getElementById('tlbl').textContent = 'C’est reparti';
  beep(3); haptic([200, 100, 200]);
  T.hide = setTimeout(stopTimer, 5000);
}
function stopTimer() { clearInterval(T.int); clearTimeout(T.hide); document.body.classList.remove('timer-on'); }
document.getElementById('tplus').addEventListener('click', () => {
  if (T.mode === 'hold') { T.end = Date.now(); tickT(); return; }
  if (tEl.classList.contains('go')) { startTimer(15, 'rest', 'Encore un peu'); return; }
  T.end += 15000; T.len += 15; tickT();
});
document.getElementById('tskip').addEventListener('click', () => { if (T.mode === 'hold') T.cb = null; stopTimer(); });
