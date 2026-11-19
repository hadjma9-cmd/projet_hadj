/* ---------------- workout overlay ---------------- */
let woTick = null, woIn = {}, exOpenHow = false;
const curDay = () => dayByKey(S.cur.day);
const curView = () => dayView(curDay());
const curInfo = () => weekInfo(S.cur.w || progWeek());
function curPlan() { return planFor(curDay(), curInfo(), S.cur.ready ? S.cur.ready.score : null); }
function curCounts() {
  const plan = curPlan();
  const total = plan.reduce((a, p) => a + p.pr.sets, 0);
  const done = plan.reduce((a, p) => a + Math.min(p.pr.sets, (S.cur.sets[p.sl.id] || []).length), 0);
  return { plan, total, done };
}
function hasProgress(c = S.cur) { return !!c && (Object.values(c.sets || {}).some(a => a.length) || Object.values(c.checks || {}).some(Boolean)); }

function startDay(dk) {
  const day = dayByKey(dk || todayKey()), v = dayView(day);
  if (S.cur && S.cur.date === TODAY() && S.cur.day === day.key) { openWO(); return; }
  if (S.cur && hasProgress()) finishSession(null, true);
  let step = { recup: 'recup', match: 'match', foot: 'foot' }[v.kind] || 'ready';
  const rt = S.ready[TODAY()];
  if (step === 'ready' && rt) step = 'warm';
  S.cur = { day: day.key, kind: v.kind, date: TODAY(), w: progWeek(), step, i: 0, ready: step === 'warm' && rt ? { score: rt.score } : null, sets: {}, fb: {}, warm: {}, checks: {}, t0: 0, prs: [], tested: false, m: { min: null, rpe: null, goals: 0, assists: 0 } };
  woIn = {}; save(); openWO();
}
function openWO() { WO.classList.add('on'); document.body.classList.add('wo-on'); renderWO(); WO.scrollTop = 0; clearInterval(woTick); woTick = setInterval(updClock, 1000); wake(); }
function closeWO() { WO.classList.remove('on'); document.body.classList.remove('wo-on'); clearInterval(woTick); stopTimer(); render(); }
function updClock() { const el = WO.querySelector('.clock'); if (!el || !S.cur) return; const s = S.cur.t0 ? Math.floor((Date.now() - S.cur.t0) / 1000) : 0; el.textContent = Math.floor(s / 60) + ':' + p2(s % 60); }
function woTop(sub) {
  const v = curView();
  return `<div class="wo-top"><button type="button" class="ico-btn" data-wo="close" aria-label="Quitter (ta séance est gardée)">${I.close}</button><div class="ttl"><b>${esc(v.name)}</b><small>${esc(sub || '')}</small></div><span class="clock">0:00</span></div>`;
}
function renderWO() {
  if (!S.cur) { closeWO(); return; }
  const v = curView();
  WO.className = 'on c-' + v.col;
  const st = S.cur.step;
  const html = st === 'ready' ? woReady() : st === 'warm' ? woWarm() : st === 'tests' ? woTests() : st === 'ex' ? woEx() : st === 'sum' ? woSum()
    : st === 'recup' ? woRecup() : st === 'foot' ? woFoot() : st === 'match' ? woMatch() : '';
  WO.innerHTML = `<div class="wo-in">${html}</div>`;
  updClock();
}
const footBar = (inner) => `<div class="wo-foot"><div>${inner}</div></div>`;

/* readiness */
function woReady() {
  const r = S.cur.rd || (S.cur.rd = {});
  const all = DATA.ready.every(q => r[q.k] != null);
  const score = all ? DATA.ready.reduce((a, q) => a + r[q.k], 0) : null;
  const L = score == null ? null : score >= 5 ? ['#22C55E', 'Feu vert', 'Séance normale. Donne tout sur chaque série.'] : score >= 3 ? ['#F59E0B', 'Feu orange', 'Une série de moins sur la force, les sauts et les sprints, effort baissé d’un cran. Tu progresses quand même.'] : ['#F43F5E', 'Feu rouge', 'Séance très allégée : moitié moins de séries, sprints à 80 %. Si tu es vraiment à plat, fais plutôt la récup du jeudi.'];
  const cols = ['#F43F5E', '#F59E0B', '#22C55E'];
  return `${woTop('Check forme · 10 secondes')}
    <div class="step-k">Avant de commencer</div><h1 class="wo-h">Comment tu te sens ?</h1><p class="wo-sub">L’app adapte la séance à ta forme du jour.</p>
    ${DATA.ready.map(q => `<div class="big-q sm">${esc(q.q)}</div><div class="opts3">${q.a.map((a, i) => `<button type="button" class="opt" data-rd="${q.k}" data-v="${i}" aria-pressed="${r[q.k] === i}"><i style="background:${cols[i]}"></i>${esc(a[0])}<small>${esc(a[1])}</small></button>`).join('')}</div>`).join('')}
    ${L ? `<div class="light"><span class="dotl" style="background:${L[0]};color:${L[0]}"></span><div><b>${L[1]}</b><p>${L[2]}</p></div></div>` : ''}
    ${footBar(`<button type="button" class="btn txt" data-wo="skipready">Passer</button><button type="button" class="btn" data-wo="readyok" ${all ? '' : 'disabled'}>C’est parti</button>`)}`;
}
/* warm-up */
function woWarm() {
  const v = curView(), list = DATA.warmup[v.warm] || [], w = S.cur.warm;
  const n = list.filter((_, i) => w[i]).length;
  return `${woTop('Échauffement')}
    <div class="step-k">Étape 1</div><h1 class="wo-h">Échauffement</h1><p class="wo-sub">${list.length} étapes, environ 8 à 12 minutes. Coche au fur et à mesure.</p>
    <div class="checks mt16">${list.map((x, i) => `<button type="button" class="ck" data-warm="${i}" aria-pressed="${!!w[i]}"><span class="bx">${tick}</span><span class="ct">${esc(x)}</span></button>`).join('')}</div>
    ${v.place ? `<p class="box-note"><b>Matériel :</b> ${esc(v.place)}</p>` : ''}
    ${footBar(`<button type="button" class="btn" data-wo="warmok">${n >= list.length ? 'Échauffement fait ✓' : n ? 'Continuer' : 'Passer l’échauffement'}</button>`)}`;
}
/* tests */
function woTests() {
  return `${woTop('Semaine de tests')}
    <div class="step-k">Tests · semaine ${curInfo().w}</div><h1 class="wo-h">Mesure tes progrès</h1><p class="wo-sub">${esc(DATA.testNote)}</p>
    <div class="tests mt16" id="wotests">${testInputs({})}</div>
    ${footBar(`<button type="button" class="btn txt" data-wo="skiptests">Passer</button><button type="button" class="btn" data-wo="testsok">Enregistrer les tests</button>`)}`;
}
/* exercise */
function woEx() {
  const c = S.cur, { plan, total, done } = curCounts(), N = plan.length;
  if (!N) { c.step = 'sum'; return woSum(); }
  c.i = Math.max(0, Math.min(N - 1, c.i));
  const p = plan[c.i], sl = p.sl, slug = p.slug, e = EXD[slug];
  const reps = repsFor(sl, slug, p.pr), mode = modeOf(sl, slug, reps);
  const arr = c.sets[sl.id] || [], n = p.pr.sets, complete = arr.length >= n;
  const opts = slotOptions(sl);
  const vsw = opts.length > 1 ? `<div class="vsw" role="group" aria-label="Variante"><small>Variante</small>${opts.map((o, i) => `<button type="button" data-var="${sl.id}" data-i="${i}" aria-pressed="${o === slug}">${esc(EXD[o].short || EXD[o].name)}</button>`).join('')}</div>` : '';
  const t = targetFor(slug), last = lastHist(slug);
  let lastLine = '';
  if (mode === 'load' || mode === 'carry') {
    const unit = exNeg(slug) ? ' kg de contrepoids' : ' kg';
    if (t) lastLine = `Dernière fois : <b>${frn(num(t.last.w))}${unit}</b>${t.last.r ? ' · ' + t.last.r + ' reps max' : ''}. ${t.up ? `<span class="up">Objectif : ${frn(t.w)}${unit}</span>` : t.last.fb === 'dur' ? 'C’était dur : garde la même charge.' : 'Garde la charge, vise une répétition de plus.'}`;
    else lastLine = `Première fois : commence avec <b>${esc(e.start || 'une charge légère')}</b> et ajuste.`;
  } else if (mode === 'reps' && last && last.r) lastLine = `Dernière fois : <b>${last.r} répétitions</b> sur ta meilleure série.${last.top ? ' <span class="up">Vise plus !</span>' : ''}`;
  else if (mode === 'hold' && last && last.r) lastLine = `Dernière fois : <b>${last.r} s</b>.`;
  // inputs
  const k = sl.id + ':' + slug;
  if (!woIn[k]) {
    const prevSet = arr[arr.length - 1];
    const nums = String(e.start || '').match(/\d+(?:[.,]\d+)?/g) || [];
    const fromStart = e.step && nums.length && !/seule|Poids du corps/.test(e.start) ? num(exNeg(slug) ? nums[nums.length - 1] : nums[0]) : null;
    const w0 = prevSet && prevSet.w != null ? prevSet.w : t ? t.w : num(S.weights[slug]) != null ? num(S.weights[slug]) : fromStart;
    const r0 = prevSet && prevSet.r != null ? prevSet.r : topOf(reps);
    woIn[k] = { w: w0 != null ? w0 : null, r: r0 != null ? r0 : null };
  }
  const inp = woIn[k];
  const unitW = exNeg(slug) ? 'kg contrepoids' : e.pair ? 'kg par main' : 'kg';
  const stW = `<div class="stp"><label for="w-in">Charge</label><div class="ctl"><button type="button" data-stp="w" data-d="-1" aria-label="Moins lourd">−</button><input id="w-in" inputmode="decimal" autocomplete="off" placeholder="—" value="${inp.w != null ? frn(inp.w) : ''}"><button type="button" data-stp="w" data-d="1" aria-label="Plus lourd">+</button></div><small>${unitW}</small></div>`;
  const stR = (lab, unit) => `<div class="stp${mode === 'reps' || mode === 'hold' ? ' one' : ''}"><label for="r-in">${lab}</label><div class="ctl"><button type="button" data-stp="r" data-d="-1" aria-label="Moins">−</button><input id="r-in" inputmode="numeric" autocomplete="off" placeholder="—" value="${inp.r != null ? inp.r : ''}"><button type="button" data-stp="r" data-d="1" aria-label="Plus">+</button></div><small>${unit}</small></div>`;
  let steppers = '';
  if (!complete) {
    if (mode === 'load') steppers = `<div class="steppers">${stW}${stR('Répétitions', 'faites')}</div>`;
    else if (mode === 'carry') steppers = `<div class="steppers">${stW.replace('class="stp"', 'class="stp one"')}</div>`;
    else if (mode === 'reps') steppers = `<div class="steppers">${stR('Répétitions', 'faites')}</div>`;
    else if (mode === 'hold') steppers = `<div class="steppers">${stR('Secondes', /côté|jambe/.test(reps) ? 'par côté' : 'tenues')}</div>`;
  }
  const DL = { plyo: ['séries', 'répét.', 'Série', 'la série'], sprint: ['sprints', 'distance', 'Sprint', 'le sprint'], cod: ['essais', 'par essai', 'Essai', 'l’essai'], ball: ['séries', 'par série', 'Série', 'la série'] };
  const lab = mode === 'drill' ? (DL[sl.kind] || DL.ball) : ['séries', mode === 'hold' ? 'temps' : mode === 'carry' ? 'distance' : 'reps', 'Série', 'la série'];
  const unitLab = lab[2];
  const dots = Array.from({ length: n }, (_, j) => `<i class="${j < arr.length ? 'on' : ''}${j === arr.length && !complete ? ' cur' : ''}"></i>`).join('');
  const fbv = c.fb[sl.id];
  const isLast = c.i === N - 1;
  let main;
  if (!complete) {
    if (mode === 'hold') main = `<button type="button" class="btn" data-wo="hold">${I.play}Lancer ${inp.r || topOf(reps) || 30} s${/côté|jambe/.test(reps) ? ' × 2' : ''}</button>`;
    else main = `<button type="button" class="btn" data-wo="set">${I.check.replace('<svg', '<svg style="fill:none;stroke:#fff;stroke-width:3;stroke-linecap:round;stroke-linejoin:round"')}Valider ${lab[3]}</button>`;
  } else main = `<button type="button" class="btn ${isLast ? 'ok' : ''}" data-wo="${isLast ? 'tosum' : 'next'}">${isLast ? 'Terminer la séance' : 'Exercice suivant'}</button>`;
  const fb = complete && mode !== 'drill' ? `<div class="big-q" style="margin-top:18px">C’était comment ?</div><div class="fb">${[['facile', '😎', 'Trop facile'], ['ok', '👌', 'Parfait'], ['dur', '🥵', 'Trop dur']].map(([v2, em, lab]) => `<button type="button" data-fb="${v2}" aria-pressed="${fbv === v2}"><span>${em}</span>${lab}</button>`).join('')}</div><p class="small muted mt8">${fbv === 'facile' ? 'Noté : la charge montera la prochaine fois.' : fbv === 'dur' ? 'Noté : on garde la même charge la prochaine fois.' : fbv === 'ok' ? 'Noté : on vise une répétition de plus la prochaine fois.' : 'Ta réponse règle la charge de la prochaine séance.'}</p>` : '';
  const nextP = plan[c.i + 1];
  return `${woTop(`Exercice ${c.i + 1} sur ${N}`)}
    <div class="wo-prog"><i style="width:${total ? done / total * 100 : 0}%"></i></div>
    <div class="exnav"><span class="k">${esc(KIND[sl.kind])} · ${esc(EQL[e.eq] || '')}</span><span class="k">${done}/${total} séries</span></div>
    ${artHtml(e)}
    <h1 class="wo-h" style="font-size:28px;margin-top:14px">${esc(e.name)}</h1>
    ${vsw}
    <div class="presc"><div><b>${n}</b><small>${lab[0]}</small></div><div><b style="font-size:${String(reps).length > 7 ? 15 : 21}px">${esc(reps)}</b><small>${lab[1]}</small></div><div><b>${restShort(p.pr.rest)}</b><small>repos</small></div><div><b style="font-size:${String(p.pr.eff).length > 6 ? 15 : 21}px">${esc(p.pr.eff)}</b><small>effort</small></div></div>
    ${p.pr.why.length ? `<p class="adapt">⚠ ${esc(p.pr.why.join(' · '))}</p>` : ''}
    ${lastLine ? `<p class="lastline">${lastLine}</p>` : ''}
    <div class="dots">${dots}</div>
    ${complete ? `<div class="setlab" style="color:var(--ok)">${n > 1 ? 'Tout est validé' : 'Validé'} ✓</div>` : `<div class="setlab">${unitLab} ${arr.length + 1} sur ${n}</div>`}
    ${steppers}
    ${fb}
    <details class="fold"${exOpenHow ? ' open' : ''} id="howfold"><summary>Comment faire${I.chev}</summary><div>${exDetail(e, slug).replace(artHtml(e), '')}</div></details>
    ${nextP && !complete ? `<p class="small muted mt12">Ensuite : ${esc(EXD[nextP.slug].name)}</p>` : ''}
    ${!isLast || !complete ? `<button type="button" class="danger mt12" data-wo="tosum">Terminer la séance maintenant</button>` : ''}
    ${footBar(`<button type="button" class="nb" data-wo="prev" aria-label="Exercice précédent" ${c.i === 0 ? 'disabled style="opacity:.35"' : ''}>${I.left}</button>${main}<button type="button" class="nb" data-wo="next" aria-label="Exercice suivant" ${isLast ? 'disabled style="opacity:.35"' : ''}>${I.right}</button>`)}`;
}
function readInputs() {
  const w = WO.querySelector('#w-in'), r = WO.querySelector('#r-in');
  return { w: w ? num(w.value) : null, r: r ? (num(r.value) != null ? Math.round(num(r.value)) : null) : null };
}
function stepInput(which, d) {
  const c = S.cur, p = curPlan()[c.i], slug = p.slug, k = p.sl.id + ':' + slug;
  const cur = readInputs(); woIn[k] = { w: cur.w, r: cur.r };
  if (which === 'w') {
    const st = exStep(slug) || 1; let v = woIn[k].w;
    if (v == null) v = num(S.weights[slug]) || 0;
    v = Math.max(0, Math.round((v + d * st) * 100) / 100); woIn[k].w = v;
  } else {
    const reps = repsFor(p.sl, slug, p.pr), hold = modeOf(p.sl, slug, reps) === 'hold';
    let v = woIn[k].r == null ? (topOf(reps) || 0) : woIn[k].r; v = Math.max(0, v + d * (hold ? 5 : 1)); woIn[k].r = v;
  }
  const el = WO.querySelector(which === 'w' ? '#w-in' : '#r-in');
  if (el) el.value = which === 'w' ? frn(woIn[k].w) : woIn[k].r;
  haptic(8);
}
function validateSet(forced) {
  const c = S.cur, plan = curPlan(), p = plan[c.i]; if (!p) return;
  const sl = p.sl, slug = p.slug, reps = repsFor(sl, slug, p.pr), mode = modeOf(sl, slug, reps);
  const arr = c.sets[sl.id] || (c.sets[sl.id] = []);
  if (arr.length >= p.pr.sets) return;
  const v = forced || readInputs(); const rec = {};
  if (mode === 'load' || mode === 'carry') {
    if (v.w == null) { toast('Indique la charge utilisée (ou 0).'); WO.querySelector('#w-in') && WO.querySelector('#w-in').focus(); return; }
    rec.w = v.w; S.weights[slug] = String(v.w);
  }
  if (mode === 'load' || mode === 'reps' || mode === 'hold') rec.r = v.r;
  arr.push(rec); if (!c.t0) c.t0 = Date.now();
  woIn[sl.id + ':' + slug] = { w: rec.w != null ? rec.w : null, r: rec.r != null ? rec.r : null };
  unlockAudio(); wake(); haptic(25);
  const done = arr.length >= p.pr.sets;
  if (done) finishExercise(p, reps, mode);
  save(); const y = WO.scrollTop; renderWO(); WO.scrollTop = done ? 0 : y;
  if (!done && p.pr.rest) startTimer(p.pr.rest, 'rest', `${mode === 'drill' ? ({ sprint: 'Sprint', cod: 'Essai' }[sl.kind] || 'Série') : 'Série'} ${arr.length + 1} sur ${p.pr.sets}`);
  else if (done && c.i < plan.length - 1) { const nx = plan[c.i + 1]; startTimer(Math.min(90, Math.max(30, p.pr.rest || 60)), 'rest', 'Ensuite : ' + EXD[nx.slug].name); }
}
function finishExercise(p, reps, mode) {
  const c = S.cur, sl = p.sl, slug = p.slug, arr = c.sets[sl.id] || [];
  if (mode === 'drill') { recordHist(slug, { r: arr.length, drill: 1 }); return; }
  const top = topOf(reps), neg = exNeg(slug), step = exStep(slug);
  const loads = arr.map(s => num(s.w)).filter(x => x != null);
  const wBest = loads.length ? (neg ? Math.min(...loads) : Math.max(...loads)) : null;
  const rMax = Math.max(0, ...arr.map(s => s.r || 0));
  const reached = top != null && arr.every(s => (s.r || 0) >= top) && (mode !== 'carry');
  const prev = bestOf(slug, TODAY());
  const patch = { top: reached, r: rMax || null };
  if (step) patch.w = wBest != null ? String(wBest) : '';
  recordHist(slug, patch);
  let isPr = false, txt = '';
  if (step && wBest != null && prev != null && (neg ? wBest < prev : wBest > prev)) { isPr = true; txt = neg ? `${frn(wBest)} kg de contrepoids (avant : ${frn(prev)} kg). Tu t’approches de la vraie traction.` : `${frn(wBest)} kg (avant : ${frn(prev)} kg).`; }
  if (!step && rMax && prev != null && rMax > prev) { isPr = true; txt = mode === 'hold' ? `${rMax} secondes (avant : ${prev} s).` : `${rMax} répétitions (avant : ${prev}).`; }
  if (isPr && !c.prs.includes(slug)) { c.prs.push(slug); S.prs.push({ d: TODAY(), slug, v: step ? wBest : rMax }); addXP(25, 'Record : ' + exName(slug)); toast('Record : ' + exName(slug), 25); }
}
function setFeedback(v) {
  const c = S.cur, p = curPlan()[c.i]; if (!p) return;
  c.fb[p.sl.id] = v; recordHist(p.slug, { fb: v }); save(); const y = WO.scrollTop; renderWO(); WO.scrollTop = y;
}
function startHold() {
  const c = S.cur, p = curPlan()[c.i], reps = repsFor(p.sl, p.slug, p.pr);
  const sec = readInputs().r || topOf(reps) || 30, two = /côté|jambe/.test(reps);
  unlockAudio(); wake(); if (!c.t0) c.t0 = Date.now();
  const seq = two ? [[sec, 'Tiens bon', 'Côté 1'], [5, 'Change de côté', 'Prépare-toi'], [sec, 'Tiens bon', 'Côté 2']] : [[sec, 'Tiens bon', 'Garde la position']];
  runSeq(seq, () => validateSet({ w: null, r: sec }));
}

/* summary */
function woSum() {
  const c = S.cur, v = curView(), { plan, total, done } = curCounts();
  const min = c.t0 ? Math.max(1, Math.round((Date.now() - c.t0) / 60000)) : 0;
  let vol = 0; plan.forEach(p => (c.sets[p.sl.id] || []).forEach(s => { if (s.w != null && s.r && !EXD[p.slug].neg) vol += s.w * s.r * (EXD[p.slug].pair ? 2 : 1); }));
  const base = done === 0 ? 0 : done >= total ? 120 : done >= total / 2 ? 100 : 60;
  const prs = c.prs.length;
  const rpe = c.rpe;
  return `${woTop('Résumé')}
    <div class="sum-hero"><div class="trophy">${I.trophy}</div><h2>${done >= total ? 'Séance terminée' : done ? 'Bien joué' : 'Séance vide'}</h2><p>${done >= total ? 'Tout est validé. C’est comme ça qu’on devient le meilleur joueur du terrain.' : done ? `${done} séries sur ${total} : ça compte quand même.` : 'Aucune série validée pour l’instant.'}</p></div>
    <div class="stats"><div><b>${min}</b><small>minute${min > 1 ? 's' : ''}</small></div><div><b>${done}/${total}</b><small>séries</small></div><div><b>${vol ? fr0(vol) : prs}</b><small>${vol ? 'kg soulevés' : 'records'}</small></div></div>
    <div class="xpl"><div><span>${esc(v.name)}${done >= total ? ' complète' : ''}</span><b>+${base} XP</b></div>${prs ? `<div><span>${prs} record${prs > 1 ? 's' : ''} personnel${prs > 1 ? 's' : ''}</span><b>+${prs * 25} XP</b></div>` : ''}${c.tested ? '<div><span>Tests</span><b>+50 XP</b></div>' : ''}</div>
    <div class="big-q">Difficulté ressentie ?</div><div class="rpe">${Array.from({ length: 10 }, (_, i) => `<button type="button" data-rpe="${i + 1}" aria-pressed="${rpe === i + 1}">${i + 1}</button>`).join('')}</div><div class="rpe-l"><span>Facile</span><span>Maximal</span></div>
    <p class="small muted mt12">Le coach s’en sert pour adapter la suite.</p>
    <button type="button" class="danger mt16" data-wo="cancel">Annuler cette séance sans l’enregistrer</button>
    ${footBar(`<button type="button" class="nb" data-wo="back" aria-label="Revenir aux exercices">${I.left}</button><button type="button" class="btn ok" data-wo="finish" ${done ? '' : 'disabled'}>Enregistrer ma séance</button>`)}`;
}
function finishSession(rpe, silent) {
  const c = S.cur; if (!c) return;
  const day = dayByKey(c.day), v = dayView(day, weekKey(D(c.date)));
  let done = 0, total = 0, xp = 0, extra = {};
  if (['gym', 'speed', 'tech'].includes(c.kind)) {
    const plan = planFor(day, weekInfo(c.w || progWeek(c.date)), c.ready ? c.ready.score : null, weekKey(D(c.date)));
    total = plan.reduce((a, p) => a + p.pr.sets, 0); done = plan.reduce((a, p) => a + Math.min(p.pr.sets, (c.sets[p.sl.id] || []).length), 0);
    xp = done === 0 ? 0 : done >= total ? 120 : done >= total / 2 ? 100 : 60;
  } else if (c.kind === 'recup') { const n = Object.values(c.checks).filter(Boolean).length; done = n; total = day.items.length; xp = n >= 3 ? 50 : n ? 20 : 0; }
  if (!done) { S.cur = null; save(); return; }
  const min = c.t0 ? Math.max(1, Math.round((Date.now() - c.t0) / 60000)) : null;
  const prev = S.log.find(l => l.d === c.date && l.day === c.day && l.kind === c.kind);
  S.log = S.log.filter(l => l !== prev);
  const entry = Object.assign({ d: c.date, day: c.day, kind: c.kind, name: v.name, col: v.col, done, total, min: silent ? null : min, rpe: rpe || null, xp, prs: c.prs.length }, extra);
  S.log.push(entry); S.log.sort((a, b) => a.d.localeCompare(b.d));
  if (S.log.length > 500) S.log.splice(0, S.log.length - 500);
  addXP(Math.max(0, xp - (prev ? prev.xp || 0 : 0)), v.name, c.date);
  S.cur = null; save();
  if (!silent) { toast(v.name + ' enregistrée', xp); }
}

/* récup */
function woRecup() {
  const c = S.cur, day = curDay(), info = curInfo(), n = Object.values(c.checks).filter(Boolean).length;
  return `${woTop('Récupération active')}
    <div class="step-k">Jeudi</div><h1 class="wo-h">Récupère, prévient</h1><p class="wo-sub">Coche ce que tu fais. Récup validée à partir de 3 éléments.</p>
    <div class="checks mt16">${day.items.map(it => {
      const e = it.ex ? EXD[it.ex] : null, op = c.open === it.id;
      return `<div><button type="button" class="ck" data-chk="${it.id}" aria-pressed="${!!c.checks[it.id]}"><span class="bx">${tick}</span><span class="ct"><b>${esc(itemText(it, info))}</b>${it.list ? `<ul>${it.list.map(x => `<li>${esc(x)}</li>`).join('')}</ul>` : ''}</span></button>
        ${e ? `<button type="button" class="link small" data-howr="${it.id}" style="padding:6px 14px">${op ? 'Masquer' : 'Voir comment faire'}</button>${op ? `<div class="card mt8">${exDetail(e, it.ex)}</div>` : ''}` : ''}</div>`;
    }).join('')}</div>
    ${footBar(`<button type="button" class="btn ok" data-wo="recupok" ${n >= 1 ? '' : 'disabled'}>${n >= 3 ? 'Valider ma récup · +50 XP' : n ? 'Valider (' + n + '/3 pour le bonus)' : 'Coche au moins un élément'}</button>`)}`;
}
/* foot collectif */
function woFoot() {
  const c = S.cur, day = curDay(), pre = planFor(day, curInfo());
  const chips = (key, vals, lab) => `<div class="gchips">${vals.map(x => `<button type="button" data-mset="${key}" data-v="${x}" aria-pressed="${c.m[key] === x}">${lab(x)}</button>`).join('')}</div>`;
  return `${woTop('Entraînement collectif')}
    <div class="step-k">Mercredi</div><h1 class="wo-h">Ton entraînement</h1><p class="wo-sub">Deux réponses et c’est enregistré.</p>
    <div class="big-q">Durée</div>${chips('min', [60, 75, 90, 105, 120], x => x + ' min')}
    <div class="big-q">Difficulté ressentie</div><div class="rpe">${Array.from({ length: 10 }, (_, i) => `<button type="button" data-mset="rpe" data-v="${i + 1}" aria-pressed="${c.m.rpe === i + 1}">${i + 1}</button>`).join('')}</div><div class="rpe-l"><span>Facile</span><span>Maximal</span></div>
    <div class="big-q">Bonus pied faible <small class="muted" style="font:600 14px var(--f-c)">(avant l’entraînement)</small></div>
    <div class="checks">${pre.map(p => `<button type="button" class="ck" data-chk="${p.sl.id}" aria-pressed="${!!c.checks[p.sl.id]}"><span class="bx">${tick}</span><span class="ct"><b>${esc(EXD[p.slug].name)}</b> · ${p.pr.sets}&nbsp;×&nbsp;${esc(p.pr.reps)}</span></button>`).join('')}</div>
    <details class="fold"><summary>Voir les exercices${I.chev}</summary><div>${pre.map(p => `<h3 style="margin:10px 0 8px">${esc(EXD[p.slug].name)}</h3>${exDetail(EXD[p.slug], p.slug)}`).join('<hr style="border:0;border-top:1px solid var(--line);margin:16px 0">')}</div></details>
    ${footBar(`<button type="button" class="btn ok" data-wo="footok" ${c.m.min && c.m.rpe ? '' : 'disabled'}>Valider l’entraînement · +${80 + (Object.values(c.checks).some(Boolean) ? 10 : 0)} XP</button>`)}`;
}
/* match */
function woMatch() {
  const c = S.cur, day = curDay(), m = c.m;
  const chips = (key, vals, lab) => `<div class="gchips">${vals.map(x => `<button type="button" data-mset="${key}" data-v="${x}" aria-pressed="${m[key] === x}">${lab(x)}</button>`).join('')}</div>`;
  const stp = (key, lab) => `<div class="stepper-row"><b>${lab}</b><div class="mini-stp"><button type="button" data-mstp="${key}" data-d="-1" aria-label="Moins">−</button><output>${m[key] || 0}</output><button type="button" data-mstp="${key}" data-d="1" aria-label="Plus">+</button></div></div>`;
  const xp = 100 + 30 * (m.goals || 0) + 20 * (m.assists || 0);
  return `${woTop('Jour de match')}
    <div class="step-k">Dimanche</div><h1 class="wo-h">Jour de match</h1><p class="wo-sub">Avant : coche ta préparation. Après : note ton match.</p>
    <div class="big-q">Avant le match</div>
    <div class="checks">${day.match.before.map((x, i) => `<button type="button" class="ck" data-chk="b${i}" aria-pressed="${!!c.checks['b' + i]}"><span class="bx">${tick}</span><span class="ct">${esc(x)}</span></button>`).join('')}</div>
    <details class="fold"><summary>Échauffement 20 min${I.chev}</summary><div><ol class="small" style="margin:0;padding-left:18px">${DATA.warmup.match.map(w => `<li>${esc(w)}</li>`).join('')}</ol></div></details>
    <div class="big-q">Après le match</div>
    <p class="small muted" style="margin:-4px 0 10px">Temps de jeu</p>${chips('min', [20, 30, 40, 50, 60, 70], x => x + (x === 70 ? '+' : '') + ' min')}
    <p class="small muted" style="margin:14px 0 10px">Difficulté ressentie</p><div class="rpe">${Array.from({ length: 10 }, (_, i) => `<button type="button" data-mset="rpe" data-v="${i + 1}" aria-pressed="${m.rpe === i + 1}">${i + 1}</button>`).join('')}</div>
    <div class="checks mt16">${stp('goals', 'Buts')}${stp('assists', 'Passes décisives')}</div>
    <div class="big-q">Récupération</div>
    <div class="checks">${day.match.after.map((x, i) => `<button type="button" class="ck" data-chk="a${i}" aria-pressed="${!!c.checks['a' + i]}"><span class="bx">${tick}</span><span class="ct">${esc(x)}</span></button>`).join('')}</div>
    ${footBar(`<button type="button" class="btn ok" data-wo="matchok" ${m.min && m.rpe ? '' : 'disabled'}>Enregistrer mon match · +${xp} XP</button>`)}`;
}
function saveFoot() {
  const c = S.cur, day = curDay(), pre = Object.values(c.checks).some(Boolean);
  if (pre) planFor(day, curInfo()).forEach(p => { if (c.checks[p.sl.id]) recordHist(p.slug, { r: p.pr.sets, drill: 1 }); });
  const xp = 80 + (pre ? 10 : 0), prev = S.log.find(l => l.d === TODAY() && l.kind === 'foot');
  S.log = S.log.filter(l => l !== prev);
  S.log.push({ d: TODAY(), day: 'mercredi', kind: 'foot', name: 'Entraînement collectif', col: 'foot', min: c.m.min, rpe: c.m.rpe, xp, done: 1, total: 1 });
  addXP(Math.max(0, xp - (prev ? prev.xp : 0)), 'Entraînement collectif');
  S.cur = null; save(); closeWO(); toast('Entraînement enregistré', xp); afterEvent();
}
function saveMatch() {
  const c = S.cur, m = c.m;
  const xp = 100 + 30 * (m.goals || 0) + 20 * (m.assists || 0);
  S.matches = S.matches.filter(x => x.d !== TODAY()); S.matches.push({ d: TODAY(), min: m.min, rpe: m.rpe, goals: m.goals || 0, assists: m.assists || 0 });
  const prev = S.log.find(l => l.d === TODAY() && l.kind === 'match');
  S.log = S.log.filter(l => l !== prev);
  S.log.push({ d: TODAY(), day: 'dimanche', kind: 'match', name: 'Match', col: 'match', min: m.min, rpe: m.rpe, goals: m.goals || 0, assists: m.assists || 0, xp, done: 1, total: 1 });
  addXP(Math.max(0, xp - (prev ? prev.xp : 0)), 'Match');
  S.cur = null; save(); closeWO(); toast('Match enregistré', xp); afterEvent();
}
function settleStale() {
  if (!S.cur || S.cur.date === TODAY()) return;
  if (hasProgress() && ['gym', 'speed', 'tech', 'recup'].includes(S.cur.kind)) finishSession(null, true);
  S.cur = null; save();
}

/* ---------------- timer, sound, wake ---------------- */
let T = { end: 0, len: 0, int: null, hide: null, mode: 'rest', seq: null, cb: null };
let AC = null, WL = null;
const tEl = document.getElementById('timer');
function unlockAudio() { try { if (!AC) AC = new (window.AudioContext || window.webkitAudioContext)(); if (AC.state === 'suspended') AC.resume(); } catch (e) {} }
function beep(n = 3) { if (!S.set.beep || !AC) return; try { const t = AC.currentTime; Array.from({ length: n }, (_, i) => i * 0.22).forEach((dt, i) => { const o = AC.createOscillator(), g = AC.createGain(); o.frequency.value = i === n - 1 ? 1046 : 784; o.connect(g); g.connect(AC.destination); g.gain.setValueAtTime(.0001, t + dt); g.gain.exponentialRampToValueAtTime(.35, t + dt + .02); g.gain.exponentialRampToValueAtTime(.0001, t + dt + .18); o.start(t + dt); o.stop(t + dt + .2); }); } catch (e) {} }
const haptic = ms => { try { navigator.vibrate && navigator.vibrate(ms); } catch (e) {} };
async function wake() { if (!S.set.wake || WL || !('wakeLock' in navigator)) return; try { WL = await navigator.wakeLock.request('screen'); WL.addEventListener('release', () => { WL = null; }); } catch (e) {} }
function startTimer(sec, mode, next, cb) {
  clearTimeout(T.hide); clearInterval(T.int);
  T.len = sec; T.end = Date.now() + sec * 1000; T.mode = mode; T.cb = cb || null;
  tEl.className = ''; document.body.classList.add('timer-on');
  document.getElementById('tlbl').textContent = mode === 'hold' ? 'Chrono' : 'Repos';
  document.getElementById('tnext').textContent = next || '';
  document.getElementById('tplus').textContent = mode === 'hold' ? 'Terminer' : '+15 s';
  document.getElementById('tskip').textContent = mode === 'hold' ? 'Annuler' : 'Passer';
  tickT(); T.int = setInterval(tickT, 200);
}
function tickT() {
  const ms = Math.max(0, T.end - Date.now()), s = Math.ceil(ms / 1000);
  document.getElementById('tval').textContent = Math.floor(s / 60) + ':' + p2(s % 60);
  document.getElementById('tring').style.strokeDashoffset = (251.3 * (1 - ms / (T.len * 1000))).toFixed(1);
  if (T.mode === 'hold' && s <= 3 && s > 0 && T.lastBeep !== s) { T.lastBeep = s; beep(1); }
  if (ms <= 0) {
    clearInterval(T.int);
    if (T.mode === 'hold') { beep(2); haptic([120, 60, 120]); const cb = T.cb; T.cb = null; document.body.classList.remove('timer-on'); if (T.seq && T.seq.length) { nextSeq(); return; } if (cb) cb(); return; }
    tEl.classList.add('go'); document.getElementById('tlbl').textContent = 'C’est reparti'; document.getElementById('tnext').textContent = document.getElementById('tnext').textContent || 'Série suivante';
    beep(3); haptic([200, 100, 200]);
    T.hide = setTimeout(stopTimer, 5000);
  }
}
function stopTimer() { clearInterval(T.int); clearTimeout(T.hide); T.seq = null; document.body.classList.remove('timer-on'); }
function runSeq(seq, done) { T.seq = seq.slice(); T.seqDone = done; nextSeq(); }
function nextSeq() {
  const [sec, lab, sub] = T.seq.shift();
  const last = !T.seq.length;
  startTimer(sec, 'hold', sub, last ? T.seqDone : null);
  document.getElementById('tlbl').textContent = lab;
}
document.getElementById('tplus').addEventListener('click', () => {
  if (T.mode === 'hold') { T.end = Date.now(); tickT(); return; }
  if (tEl.classList.contains('go')) { startTimer(15, 'rest', 'Encore un peu'); return; }
  T.end += 15000; T.len += 15; tickT();
});
document.getElementById('tskip').addEventListener('click', () => { if (T.mode === 'hold') { T.cb = null; T.seq = null; } stopTimer(); });
