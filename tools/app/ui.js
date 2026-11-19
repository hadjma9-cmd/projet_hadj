/* ---------------- icons & shared bits ---------------- */
const I = {
  gear: '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="3.2"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z"/></svg>',
  play: '<svg viewBox="0 0 24 24"><path d="M8 5.5v13a1 1 0 0 0 1.5.86l10.4-6.5a1 1 0 0 0 0-1.72L9.5 4.64A1 1 0 0 0 8 5.5z"/></svg>',
  check: '<svg viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>',
  close: '<svg viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18"/></svg>',
  chev: '<svg class="chev" viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg>',
  left: '<svg viewBox="0 0 24 24"><path d="M15 5l-7 7 7 7"/></svg>',
  right: '<svg viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg>',
  bulb: '<svg viewBox="0 0 24 24"><path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-3.6 10.8c.6.5 1 1.2 1.1 2V16h5v-.2c.1-.8.5-1.5 1.1-2A6 6 0 0 0 12 3z"/></svg>',
  trophy: '<svg viewBox="0 0 24 24"><path d="M7 3h10v3h3v2a5 5 0 0 1-4.6 5 5 5 0 0 1-3.4 2.9V19h3v2H9v-2h3v-3.1A5 5 0 0 1 8.6 13 5 5 0 0 1 4 8V6h3V3zm-1 5a3 3 0 0 0 1.3 2.5A6.9 6.9 0 0 1 7 8V8H6zm11 0v.1c0 .9-.1 1.7-.3 2.4A3 3 0 0 0 18 8h-1z"/></svg>',
  send: '<svg viewBox="0 0 24 24"><path d="M3.4 20.4 21 12 3.4 3.6 3.4 10l12.6 2-12.6 2z"/></svg>',
  flame: '🔥',
};
const tick = '<svg viewBox="0 0 14 14"><path d="M2.5 7.5l3 3 6-7"/></svg>';
function mmap(prim, sec) {
  let s = "<svg class='mm' viewBox='0 0 124 114' aria-hidden='true'>";
  DATA.regions.forEach(([keys, el]) => {
    const c = keys.some(k => prim.includes(k)) ? 'mp' : keys.some(k => sec.includes(k)) ? 'ms' : 'mb';
    s += el.replace(/^<(\w+)/, `<$1 class='${c}'`);
  });
  return s + "<path class='sx' d='M30 31V51.6M25.4 37.6H34.6M25.4 44.4H34.6'/></svg>";
}
const muscleText = arr => arr.map(k => DATA.muscles[k]).join(', ');
function artHtml(e) {
  if (e.dia) return `<figure class="diafig">${e.dia}</figure>`;
  return `<div class="art"><figure class="pose">${e.a}<figcaption>${esc(e.ca)}</figcaption></figure><figure class="pose">${e.b}<figcaption>${esc(e.cb)}</figcaption></figure></div>`;
}
function thumbHtml(e) { return `<div class="thumb">${e.dia ? e.dia : e.b}</div>`; }
function exDetail(e, slug) {
  const mus = e.prim && e.prim.length ? `<div class="mus">${mmap(e.prim, e.sec || [])}<p><b>Travaille :</b> ${esc(muscleText(e.prim))}${e.sec && e.sec.length ? `<br>Aussi : ${esc(muscleText(e.sec))}` : ''}</p></div>` : '';
  const qual = e.qual ? `<div class="quals">${e.qual.map(q => `<span>${esc(q)}</span>`).join('')}</div>` : '';
  return `${artHtml(e)}<p class="how">${esc(e.how)}</p><p class="err"><b>À éviter :</b> ${esc(e.err)}</p>${mus}${qual}${e.start ? `<p class="alts">Départ conseillé : <b>${esc(e.start)}</b></p>` : ''}`;
}
let toastT = null;
function toast(t, xp) {
  const el = document.getElementById('toast');
  el.innerHTML = `<span>${esc(t)}</span>${xp ? `<span class="xp">+${xp} XP</span>` : ''}`;
  el.classList.add('show'); clearTimeout(toastT); toastT = setTimeout(() => el.classList.remove('show'), 2600);
}
function confetti() {
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const cols = ['#FF5A1F', '#F0386B', '#FFC53D', '#22C55E', '#3B6CFF', '#8B5CF6'];
  for (let i = 0; i < 70; i++) {
    const c = document.createElement('i'); c.className = 'cf';
    c.style.left = Math.random() * 100 + 'vw'; c.style.background = cols[i % cols.length];
    c.style.setProperty('--dx', (Math.random() * 160 - 80) + 'px'); c.style.setProperty('--rot', (Math.random() * 720 - 360) + 'deg');
    c.style.animationDuration = (1.6 + Math.random() * 1.4) + 's'; c.style.animationDelay = (Math.random() * .3) + 's';
    document.body.appendChild(c); setTimeout(() => c.remove(), 3600);
  }
}
function flushCele() {
  const el = document.getElementById('cele');
  if (el.classList.contains('on') || !pending.length) return;
  const p = pending.shift();
  let em = '🏆', k = '', h = '', t = '';
  if (p.kind === 'level') { em = p.lv.em; k = 'Niveau ' + p.lv.n; h = p.lv.t; t = p.lv.next ? `Prochain titre : ${p.lv.next}, à ${fr0(p.lv.to)} XP.` : 'Tu as atteint le plus haut niveau.'; }
  else if (p.kind === 'badge') { em = p.b.em; k = 'Badge débloqué'; h = p.b.name; t = p.b.desc; }
  else if (p.kind === 'week') { em = '🎯'; k = 'Objectif de la semaine'; h = 'Semaine validée'; t = `${DATA.weekGoal} activités cette semaine : +150 XP. La régularité, c’est ce qui fait progresser.`; }
  else if (p.kind === 'pr') { em = '💥'; k = 'Record personnel'; h = p.name; t = p.txt; }
  el.innerHTML = `<div><div class="em">${em}</div><div class="k">${esc(k)}</div><h2>${esc(h)}</h2><p>${esc(t)}</p><button type="button" class="btn" data-cele="1">Continuer</button></div>`;
  el.classList.add('on'); confetti();
  try { navigator.vibrate && navigator.vibrate([30, 40, 60]); } catch (e) {}
}

/* ---------------- coach tips (rules) ---------------- */
function tips() {
  const out = [], dk = todayKey(), info = weekInfo(), mw = isMatchWeek(), pw = info.real;
  if (info.before) out.push(['Ton cycle commence le ' + fmtDate(S.start), 'Prépare ton matériel : un médecine-ball à la salle, 6 plots et un ballon pour le terrain.']);
  if (info.after) out.push(['Cycle de 12 semaines terminé', 'Fais tes tests, puis lance un nouveau cycle dans les réglages : on repart sur des charges plus lourdes.']);
  if (dk === 'jeudi' && info.test && !info.before) out.push(['Tests demain', 'Couche-toi tôt et mange normalement : demain on mesure tes progrès sur 10 m, 20 m, en saut et au 5-0-5.']);
  if (dk === 'vendredi' && info.test && !info.before) out.push(['Jour de tests', 'Échauffe-toi bien, 2 essais par test, 3 minutes de repos entre deux sprints. Même terrain et même chrono à chaque fois.']);
  if (dk === 'mardi') out.push(['Foot demain', 'Garde 2 à 3 répétitions en réserve sur chaque série : tu dois arriver frais à l’entraînement.']);
  if (dk === 'mercredi') out.push(['Entraînement ce soir', 'Collation 1 h 30 avant (skyr, banane, pain et miel) et ta dose de whey juste après.']);
  if (dk === 'vendredi' && mw) out.push(['Match dimanche', 'La séance est raccourcie automatiquement : moins de répétitions, même intensité.']);
  if (dk === 'samedi' && mw) out.push(['Veille de match', 'Séance courte sans aller à l’échec, et grosse assiette de pâtes ce soir.']);
  if (dk === 'dimanche' && mw) out.push(['Jour de match', 'Repas 3 h avant le coup d’envoi, 500 ml d’eau dans les 2 h, et 20 minutes d’échauffement.']);
  if (dk === 'lundi' && S.matches.some(m => m.d === addDays(TODAY(), -1))) out.push(['Lendemain de match', 'Haut du corps aujourd’hui : les jambes récupèrent. Ajoute 10 minutes de vélo très facile à la fin.']);
  if (info.deload && !info.before) out.push(['Semaine allégée', 'Une série de moins et effort 7/10 : c’est pendant cette semaine que ton corps assimile le travail.']);
  if (info.learn && !info.before) out.push(['Semaine ' + info.w + ' : apprentissage', '2 séries par exercice, charges légères. Le but : des gestes propres avant de charger.']);
  const r = S.ready[addDays(TODAY(), -1)];
  if (r && r.score <= 2) out.push(['Forme basse hier', 'Dors 8 h cette nuit. Si tu es encore à plat demain, fais la séance allégée proposée par l’app.']);
  const day = dayByKey(dk);
  if (['gym'].includes(day.kind)) {
    const up = planFor(day).map(p => ({ p, t: targetFor(p.slug) })).find(x => x.t && x.t.up);
    if (up) out.push(['Objectif du jour', `${exName(up.p.slug)} : la dernière fois tu as tout validé. Aujourd’hui, passe à ${frn(up.t.w)} kg${exNeg(up.p.slug) ? ' de contrepoids' : ''}.`]);
  }
  const left = DATA.weekGoal - weekActs();
  if (left > 0 && left <= 2) out.push(['Plus que ' + left + (left > 1 ? ' activités' : ' activité'), `Valide ta semaine pour gagner 150 XP${streak() ? ' et garder ta série de ' + streak() + ' semaine' + (streak() > 1 ? 's' : '') : ''}.`]);
  const lastW = S.body[S.body.length - 1];
  if (!lastW || lastW.d < addDays(TODAY(), -7)) out.push(['Pèse-toi cette semaine', 'Le matin à jeun, 2 ou 3 fois par semaine : l’app ajuste tes repas si ton poids bouge trop.']);
  if (!out.length) out.push(['Régularité avant tout', 'Une séance faite à 80 % vaut mieux qu’une séance parfaite jamais faite.']);
  return out;
}

/* ---------------- ACCUEIL ---------------- */
function todayStatus(dk = todayKey()) {
  const l = S.log.filter(x => x.d === TODAY());
  return { done: l.length > 0, entry: l[l.length - 1] };
}
function heroAction(day, v) {
  const cur = S.cur && S.cur.date === TODAY() ? S.cur : null;
  if (cur) return { t: 'Reprendre ma séance', a: 'resume' };
  if (v.kind === 'foot') return { t: 'J’ai fait l’entraînement', a: 'foot' };
  if (v.kind === 'recup') return { t: 'Commencer ma récup', a: 'start' };
  if (v.kind === 'match') return { t: 'Préparer mon match', a: 'start' };
  return { t: 'Commencer ma séance', a: 'start' };
}
function renderAccueil() {
  const dk = todayKey(), day = dayByKey(dk), v = dayView(day), info = weekInfo(), lv = levelOf();
  const st = todayStatus(), act = heroAction(day, v);
  const now = new Date();
  const plan = ['gym', 'speed', 'tech'].includes(v.kind) ? planFor(day) : [];
  const tags = [];
  if (info.before) tags.push('Début le ' + fmtDate(S.start)); else tags.push(`Semaine ${info.w}/12 · ${DATA.blocks[info.block].name}`);
  if (v.dur) tags.push(v.dur);
  if (plan.length) tags.push(plan.length + ' exercices');
  if (info.test && dk === 'vendredi' && !info.before) tags.push('Tests');
  if (info.deload && !info.before) tags.push('Allégée');
  let cta = '';
  if (st.done && !(S.cur && S.cur.date === TODAY())) {
    cta = `<div class="done">${'<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>'}<div><b>${esc(st.entry.name)} : c’est fait</b><br><span style="opacity:.85">+${st.entry.xp || 0} XP · ${esc(dayDoneText(st.entry))}</span></div></div>
      <div class="nxt">Demain : <b>${esc(nextView().name)}</b></div>
      <button type="button" class="alt" data-act="${act.a}">Refaire ou compléter</button>`;
  } else {
    cta = `<button type="button" class="btn white" data-act="${act.a}">${I.play}${esc(act.t)}</button>`;
    if (v.kind === 'gym' || v.kind === 'speed' || v.kind === 'tech') cta += `<button type="button" class="alt" data-go="programme" data-day="${dk}">Voir le détail</button>`;
  }
  const t = tips().slice(0, 2);
  const wkDays = ORDER.map((k, i) => {
    const dd = addDays(weekKey(), i), dv = dayView(dayByKey(k)), done = S.log.some(l => l.d === dd);
    const cls = ['wd', 'c-' + dv.col, done ? 'on' : '', dd === TODAY() ? 'today' : '', !done && dd < TODAY() ? 'miss' : ''].join(' ');
    return `<button type="button" class="${cls}" data-go="programme" data-day="${k}"><small>${JOURS[(i + 1) % 7].slice(0, 3).toUpperCase()}</small><i>${done ? I.check : D(dd).getDate()}</i><span>${esc(dv.tag)}</span></button>`;
  }).join('');
  const acts = weekActs(), C = 2 * Math.PI * 32, pct = Math.min(1, acts / DATA.weekGoal), stk = streak();
  const n = todayNutrition();
  const cyc = Array.from({ length: 12 }, (_, i) => {
    const w = i + 1, b = w <= 4 ? 1 : w <= 8 ? 2 : 3;
    const cls = ['b' + b, w < info.real ? 'past' : '', w === info.real ? 'now' : '', DATA.deload.includes(w) ? 'dl' : '', DATA.testWeeks.includes(w) ? 'ts' : ''].join(' ');
    return `<i class="${cls}">${w}</i>`;
  }).join('');
  const nextTest = DATA.testWeeks.find(w => w >= Math.max(1, info.real));
  const ntDate = nextTest ? addDays(S.start, (nextTest - 1) * 7 + 4) : null;
  const hello = S.name ? 'Salut ' + S.name : 'Salut le 10';
  view.className = '';
  view.innerHTML = `
    <div class="hello"><div class="avatar">10</div><div class="grow"><h1>${esc(hello)}</h1><p>${JOURS[now.getDay()]} ${fmtDate(TODAY())}</p></div><button type="button" class="ico-btn" data-sheet="settings" aria-label="Réglages">${I.gear}</button></div>
    <button type="button" class="lvl" data-go="progres" style="width:100%;text-align:left"><span style="font-size:22px">${lv.em}</span><div class="grow"><b>Niv. ${lv.n} · ${esc(lv.t)}</b><div class="bar gold mt8"><i style="width:${Math.round(lv.pct * 100)}%"></i></div></div><small>${lv.to ? fr0(lv.xp) + ' / ' + fr0(lv.to) + ' XP' : fr0(lv.xp) + ' XP'}</small></button>
    <section class="hero c-${v.col}" data-big="${esc(String(v.tag).slice(0, 2).toUpperCase())}">
      <div class="kick">Aujourd’hui · ${JOURS[now.getDay()]}</div>
      <h2>${esc(v.name)}</h2>
      <div class="theme">${esc(v.theme || '')}</div>
      <div class="tags">${tags.map(x => `<span class="tag">${esc(x)}</span>`).join('')}</div>
      ${cta}
    </section>
    ${S.migrated && !S.welcomed ? `<section class="card mt12"><div class="tip"><div class="ti">${I.bulb}</div><div><b>Ton nouveau programme est prêt</b><p>Tes charges, ton poids, tes repas et tes séances passées sont conservés${S.log.length ? ` (${S.log.length} séance${S.log.length > 1 ? 's' : ''}, ${fr0(xpTotal())} XP déjà gagnés)` : ''}. Le programme est maintenant pensé pour le foot : 3 séances de salle, 1 séance de vitesse, la récup et la technique.</p><button type="button" class="btn sm ghost mt12" data-welcome="1">Compris</button></div></div></section>` : ''}
    <section class="card mt12">${t.map(([h, p]) => `<div class="tip"><div class="ti">${I.bulb}</div><div><b>${esc(h)}</b><p>${esc(p)}</p></div></div>`).join('<div style="height:12px"></div>')}</section>
    <div class="sec-t"><h2>Ma semaine</h2><small>${acts}/${DATA.weekGoal} activités</small></div>
    <section class="card">
      <div class="goal"><div class="ring"><svg viewBox="0 0 76 76"><circle class="bg" cx="38" cy="38" r="32"/><circle class="fg" cx="38" cy="38" r="32" stroke-dasharray="${C}" stroke-dashoffset="${C * (1 - pct)}"/></svg><div><span>${acts}<small>sur ${DATA.weekGoal}</small></span></div></div>
        <div class="grow"><h3>${acts >= DATA.weekGoal ? 'Semaine validée' : 'Objectif : ' + DATA.weekGoal + ' activités'}</h3><p>${acts >= DATA.weekGoal ? 'Bonus de 150 XP gagné. Tout ce qui suit, c’est du bonus.' : 'Encore ' + (DATA.weekGoal - acts) + ' pour valider la semaine et gagner 150 XP.'}</p>${stk ? `<p class="flame mt8">🔥 ${stk} semaine${stk > 1 ? 's' : ''} d’affilée</p>` : ''}</div></div>
      <div class="week">${wkDays}</div>
    </section>
    <section class="card mt12"><div class="qa"><div><h3>Match ce dimanche ?</h3><p>${isMatchWeek() ? 'Vendredi, samedi et les repas s’adaptent.' : 'Sinon : séance technique dimanche.'}</p></div>
      <div class="seg sm" role="group" aria-label="Match ce dimanche"><button type="button" data-match="1" aria-pressed="${isMatchWeek()}">Oui</button><button type="button" data-match="0" aria-pressed="${!isMatchWeek()}">Non</button></div></div></section>
    <div class="sec-t"><h2>Nutrition du jour</h2><button type="button" data-go="repas">Voir mes repas</button></div>
    <section class="card"><div class="nut">
      <div><div class="lab"><span>Protéines</span><b>${fr0(n.eP)} / ${fr0(n.P)} g</b></div><div class="bar ok"><i style="width:${n.P ? Math.min(100, n.eP / n.P * 100) : 0}%"></i></div></div>
      <div><div class="lab"><span>Eau</span><b>${fr1(n.water * 0.25)} / 2,5 L</b></div><div class="bar"><i style="width:${Math.min(100, n.water * 10)}%"></i></div></div></div>
      <div class="water"><button type="button" data-water="-1" aria-label="Retirer un verre d’eau">− verre</button><button type="button" data-water="1" aria-label="Ajouter un verre d’eau">+ verre d’eau</button><button type="button" data-go="repas">Cocher un repas</button></div></section>
    <div class="sec-t"><h2>Mon cycle</h2><small>${info.before ? 'Début le ' + fmtDate(S.start) : info.after ? 'Terminé' : 'Semaine ' + info.w + ' sur 12'}</small></div>
    <section class="card"><div class="cycle">${cyc}</div>
      <div class="legend"><span><i style="background:#22A355"></i>Fondations</span><span><i style="background:#FF8A1F"></i>Force</span><span><i style="background:#F0386B"></i>Puissance & vitesse</span></div>
      <p class="small muted mt12">${esc(DATA.blocks[info.block].goal)}${ntDate && !info.after ? ` Prochains tests : vendredi ${fmtDate(ntDate)}` : ''}</p></section>`;
}
function nextView() { const t = addDays(TODAY(), 1); return dayView(dayByKey(KEYS[D(t).getDay()]), weekKey(D(t))); }
function dayDoneText(l) {
  if (l.kind === 'foot') return (l.min ? l.min + ' min' : 'Entraînement') + (l.rpe ? ' · effort ' + l.rpe + '/10' : '');
  if (l.kind === 'match') return (l.goals ? l.goals + ' but' + (l.goals > 1 ? 's' : '') + ' · ' : '') + (l.min ? l.min + ' min jouées' : 'Match joué');
  if (l.kind === 'recup') return 'Récupération faite';
  return `${l.done}/${l.total} séries${l.min ? ' · ' + l.min + ' min' : ''}`;
}

/* ---------------- PROGRAMME ---------------- */
let progDay = null, openEx = new Set(), sunView = null;
function prescLine(pr, sl, slug) {
  const reps = repsFor(sl, slug, pr), mode = modeOf(sl, slug, reps);
  return `<b>${pr.sets}&nbsp;×&nbsp;${esc(reps)}</b>${pr.rest ? ' · repos ' + restTxt(pr.rest) : ''} · ${esc(pr.eff)}`;
}
function exItem(p, i) {
  const e = EXD[p.slug], key = p.sl.id, op = openEx.has(key);
  const alts = slotOptions(p.sl).filter(s => s !== p.slug);
  return `<article class="exi${op ? ' open' : ''}"><button type="button" data-ex="${key}" aria-expanded="${op}">${thumbHtml(e)}<div class="grow"><span class="kind k-${p.sl.kind}">${esc(KIND[p.sl.kind])}</span><h3>${esc(e.name)}</h3><div class="ps">${prescLine(p.pr, p.sl, p.slug)}</div></div>${I.chev}</button>
    ${op ? `<div class="exd">${exDetail(e, p.slug)}${p.pr.why.length ? `<p class="adapt">⚠ ${esc(p.pr.why.join(' · '))}</p>` : ''}${alts.length ? `<p class="alts">Si c’est pris : ${alts.map(a => esc(EXD[a].name)).join(' ou ')} (choix pendant la séance).</p>` : ''}${p.sl.note ? `<p class="alts">${esc(p.sl.note)}</p>` : ''}</div>` : ''}</article>`;
}
function renderProgramme() {
  const dk = progDay || todayKey(), day = dayByKey(dk), info = weekInfo();
  const wk = weekKey();
  const sunMode = dk === 'dimanche' ? (sunView || (isMatchWeek() ? 'match' : 'tech')) : null;
  const v = dk === 'dimanche' ? Object.assign({}, day, sunMode === 'match' ? day.match : day.tech, { key: 'dimanche', kind: sunMode }) : dayView(day);
  const chips = ORDER.map(k => { const dv = dayView(dayByKey(k)); return `<button type="button" class="chip c-${dv.col}" data-day="${k}" aria-pressed="${k === dk}"><b>${JOURS[KEYS.indexOf(k)].slice(0, 3)}${k === todayKey() ? ' ·' : ''}</b><span>${esc(dv.tag)}</span></button>`; }).join('');
  let body = '';
  const startBtn = (lab) => `<button type="button" class="btn white" data-act="start" data-day="${dk}">${I.play}${esc(lab)}</button>`;
  if (v.kind === 'gym' || v.kind === 'speed' || v.kind === 'tech') {
    const mw = isMatchWeek(wk);
    const slots = v.slots.map(sl => ({ sl, slug: slotSlug(sl), pr: presc(sl, dk, info, null, mw) })).filter(p => p.pr);
    const main = slots.filter(p => p.sl.kind !== 'core'), core = slots.filter(p => p.sl.kind === 'core');
    body = `${v.place ? `<p class="box-note"><b>Où :</b> ${esc(v.place)}</p>` : ''}
      <details class="fold mt12"><summary>Échauffement${v.warm ? ' · ' + DATA.warmup[v.warm].length + ' étapes' : ''}${I.chev}</summary><div><ol class="small" style="margin:0;padding-left:18px">${(DATA.warmup[v.warm] || []).map(w => `<li>${esc(w)}</li>`).join('')}</ol></div></details>
      ${info.test && dk === 'vendredi' ? `<p class="box-note"><b>Semaine de tests :</b> après l’échauffement, l’app te guide pour les tests (sprint 10 et 20 m, saut, 5-0-5, jongles). Ils remplacent les sprints et le saut de la séance.</p>` : ''}
      <div class="exl">${main.map(exItem).join('')}</div>
      ${core.length ? `<div class="sec-t"><h2>Gainage</h2><small>${core.length} exercices sans machine</small></div><div class="exl" style="margin-top:0">${core.map(exItem).join('')}</div>` : ''}`;
  } else if (v.kind === 'foot') {
    const pre = planFor(day);
    body = `<p class="box-note"><b>Le plus important de ta semaine.</b> Rien à charger : l’app te demande seulement la durée et ton ressenti après l’entraînement.</p>
      <div class="sec-t"><h2>Bonus avant l’entraînement</h2><small>10 min si tu arrives en avance</small></div><div class="exl" style="margin-top:0">${pre.map(exItem).join('')}</div>`;
  } else if (v.kind === 'recup') {
    body = `<div class="checks mt12">${day.items.map(it => `<div class="ck" style="cursor:default"><div class="ct"><b>${esc(itemText(it, info))}</b>${it.list ? `<ul>${it.list.map(x => `<li>${esc(x)}</li>`).join('')}</ul>` : ''}</div></div>`).join('')}</div>
      <p class="box-note">Récup validée dès que tu coches 3 éléments. Très courbaturé ? Saute la Copenhague et garde vélo + mobilité.</p>`;
  } else if (v.kind === 'match') {
    body = `<div class="sec-t"><h2>Avant le match</h2></div><div class="checks">${day.match.before.map(x => `<div class="ck" style="cursor:default"><div class="ct">${esc(x)}</div></div>`).join('')}</div>
      <div class="sec-t"><h2>Échauffement 20 min</h2></div><section class="card"><ol class="small" style="margin:0;padding-left:18px">${DATA.warmup.match.map(w => `<li>${esc(w)}</li>`).join('')}</ol></section>
      <div class="sec-t"><h2>Après le match</h2></div><div class="checks">${day.match.after.map(x => `<div class="ck" style="cursor:default"><div class="ct">${esc(x)}</div></div>`).join('')}</div>`;
  }
  const sunSw = dk === 'dimanche' ? `<div class="seg mt12" role="group" aria-label="Dimanche"><button type="button" data-sun="match" aria-pressed="${sunMode === 'match'}">Match</button><button type="button" data-sun="tech" aria-pressed="${sunMode === 'tech'}">Technique</button></div>` : '';
  const btnLab = v.kind === 'foot' ? 'J’ai fait l’entraînement' : v.kind === 'recup' ? 'Commencer ma récup' : v.kind === 'match' ? 'Préparer mon match' : 'Commencer cette séance';
  view.className = '';
  view.innerHTML = `<div class="page-h"><h1>Programme</h1><span class="sub">${info.before ? 'Début ' + fmtDate(S.start) : 'Semaine ' + info.w + ' · ' + esc(DATA.blocks[info.block].name)}</span></div>
    <div class="chips dchips">${chips}</div>
    ${sunSw}
    <section class="hero c-${v.col} mt12" data-big="${esc(String(v.tag).slice(0, 2).toUpperCase())}"><div class="kick">${JOURS[KEYS.indexOf(dk)]}${v.dur ? ' · ' + esc(v.dur) : ''}</div><h2>${esc(v.name)}</h2><div class="theme">${esc(day.goal || v.theme || '')}</div>
      ${day.note ? `<div class="tags"><span class="tag">${esc(day.note)}</span></div>` : '<div style="height:14px"></div>'}
      <button type="button" class="btn white" data-act="${v.kind === 'foot' ? 'foot' : 'start'}" data-day="${dk}">${I.play}${esc(btnLab)}</button></section>
    ${body}
    <div class="sec-t"><h2>Le plan sur 12 semaines</h2></div>
    <section class="card"><div class="plan12">${DATA.blocks.map((b, i) => `<div class="blk${i === info.block && !info.before ? ' cur' : ''}"><div class="bn" style="background:${['#22A355', '#FF8A1F', '#F0386B'][i]}">${i + 1}<small>S${b.weeks[0]}–${b.weeks[3]}</small></div><div><h3>${esc(b.name)}</h3><p>${esc(b.goal)}</p></div></div>`).join('')}</div>
      <p class="small muted mt12">Semaines 1–2 : 2 séries pour apprendre. Semaines 8 et 12 : allégées. Tests les vendredis des semaines ${DATA.testWeeks.join(', ')}.</p></section>
    <div class="sec-t"><h2>Les règles</h2></div>
    <section class="rules">
      <div><b>Effort 7/10</b>Tu pourrais encore faire 3 répétitions</div><div><b>Effort 8/10</b>Encore 2 répétitions en réserve, jamais l’échec</div>
      <div><b>Progression</b>Haut de la fourchette partout : charge suivante</div><div><b>Explosif</b>Chaque répétition à fond. Ça ralentit ? Stop</div>
      <div><b>Vitesse</b>Repos complet : la qualité avant la quantité</div><div><b>Douleur</b>Articulation ou vive : on arrête et on en parle au coach</div></section>`;
}
function itemText(it, info) { if (it.p) return it.txt + ' : ' + it.p[info.block]; return it.txt; }

/* ---------------- REPAS ---------------- */
let mealDay = JOURS[new Date().getDay()], mealTab = 'menus', fishView = null, altView = null;
function qtyLabel(f, q) {
  const x = F(f);
  if (x.per === 'g') return `<b>${q} g</b> · ${esc(x.n)}`;
  if (x.unit) return `<b>${q} ${esc(x.unit)}${q > 1 && !/\./.test(x.unit) ? 's' : ''}</b> · ${esc(x.n)}`;
  return `<b>${q}</b> · ${esc(q > 1 && x.pl ? x.pl : x.n)}`;
}
const MEAL_DAYS = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'];
function renderRepas() {
  const isToday = mealDay === JOURS[new Date().getDay()];
  const md0 = DATA.meals.find(x => x.day === mealDay);
  const r = mealsFor(mealDay, { alt: altView, fish: fishView });
  const fd = isToday ? foodDay() : null;
  let K = 0, P = 0;
  const cards = r.meals.map((m, i) => {
    const [k, p] = mealTotals(m.items); K += k; P += p;
    const eaten = fd && fd.eaten[i];
    const rows = Object.keys(m.items).map(f => { const [a, b] = kp(f, m.items[f]); return `<div class="food"><span>${qtyLabel(f, m.items[f])}${F(f).new ? '<span class="new">nouveau</span>' : ''}</span><span class="fp">${b >= 1 ? fr0(b) + ' g prot.' : fr0(a) + ' kcal'}</span></div>`; }).join('');
    const sw = m.fish ? `<div class="seg mt12" role="group" aria-label="Semaine"><button type="button" data-fish="A" aria-pressed="${r.week === 'A'}">Semaine A · poisson</button><button type="button" data-fish="B" aria-pressed="${r.week === 'B'}">Semaine B · thon</button></div>` : '';
    return `<article class="meal${eaten ? ' eaten' : ''}"><div class="meal-h"><div><h3>${esc(m.name)}</h3>${m.title ? `<p class="dish">${esc(m.title)}</p>` : ''}</div><div class="tot"><b>${fr0(p)} g</b>prot. · ${fr0(k)} kcal</div></div>${sw}${rows}${isToday ? `<button type="button" class="eat" data-eat="${i}" aria-pressed="${!!eaten}">${eaten ? 'Mangé ✓' : 'Marquer comme mangé'}</button>` : ''}</article>`;
  }).join('');
  const chips = MEAL_DAYS.map(dn => { const k = dn.toLowerCase(), dv = dayView(dayByKey(k)); return `<button type="button" class="chip c-${dv.col}" data-mday="${dn}" aria-pressed="${dn === mealDay}"><b>${dn.slice(0, 3)}${dn === JOURS[new Date().getDay()] ? ' ·' : ''}</b><span>${esc(dv.tag)}</span></button>`; }).join('');
  const dv = dayView(dayByKey(mealDay.toLowerCase()));
  const altSw = md0.alt ? `<div class="seg mt12" role="group" aria-label="Version"><button type="button" data-alt="0" aria-pressed="${!r.alt}">${esc(md0.tag)}</button><button type="button" data-alt="1" aria-pressed="${r.alt}">${esc(md0.alt.tag)}</button></div>` : '';
  let content;
  if (mealTab === 'menus') {
    const t = isToday ? todayNutrition() : null;
    content = `<div class="chips dchips mt12">${chips}</div>${altSw}
      <section class="hero c-${dv.col} mt12" data-big="${fr0(r.target / 100)}"><div class="kick">${esc(mealDay)} · ${esc(r.tag)}</div><h2>${r.alt ? (mealDay === 'Dimanche' ? 'Jour de match' : 'Veille de match') : esc(dayLabel(mealDay))}</h2>
        <div class="mhero"><div><b>${fr0(K)}</b><small>kcal</small></div><div><b>${fr0(P)} g</b><small>protéines</small></div><div><b>${r.meals.length}</b><small>repas</small></div></div>
        ${t ? `<div class="mt12"><div class="lab" style="display:flex;justify-content:space-between;font:600 13px var(--f-c);text-transform:uppercase;letter-spacing:.6px"><span>Mangé aujourd’hui</span><span>${fr0(t.eP)} / ${fr0(t.P)} g</span></div><div class="bar mt8" style="background:rgba(255,255,255,.2)"><i style="width:${t.P ? Math.min(100, t.eP / t.P * 100) : 0}%;background:#fff"></i></div>
          <div class="water" style="margin-top:12px"><button type="button" data-water="-1" style="background:rgba(255,255,255,.18);border:0;color:#fff">− verre</button><button type="button" data-water="1" style="background:rgba(255,255,255,.18);border:0;color:#fff">+ verre · ${fr1(t.water * 0.25)} L</button></div></div>` : ''}</section>
      <div class="mt12">${cards}</div>
      <section class="box-note"><b>Repères.</b> Environ 160 g de protéines chaque jour (2 g par kg), une seule dose de whey. Les calories suivent ta journée : plus les jours de foot et de match, moins le jeudi. Poulet, pâtes et riz pesés crus ; thon égoutté ; wedges et poisson à l’air fryer, sans huile ajoutée.<br><br><b>Poisson 2 fois par semaine</b> dont un poisson gras, comme le recommande l’ANSES : lundi soir (poisson meunière une semaine, thon 100 g l’autre) et sardines le jeudi.<br><br>Ton poids monte de plus de 0,3 kg par semaine pendant 2 semaines ? Enlève 40 g de pâtes ou de riz par jour. Il baisse de plus de 0,7 kg ? Ajoute-les.</section>`;
  } else content = coursesHtml();
  view.className = '';
  view.innerHTML = `<div class="page-h"><h1>Repas</h1><span class="sub">${mealTab === 'menus' ? 'Semaine ' + fishWeek() : 'Liste de la semaine'}</span></div>
    <div class="seg" role="group" aria-label="Repas ou courses"><button type="button" data-mtab="menus" aria-pressed="${mealTab === 'menus'}">Menus</button><button type="button" data-mtab="courses" aria-pressed="${mealTab === 'courses'}">Courses</button></div>
    ${content}`;
}
function dayLabel(dn) { const k = dn.toLowerCase(), v = dayView(dayByKey(k)); return { gym: 'Jour de salle', speed: 'Jour de vitesse', foot: 'Jour de foot', recup: 'Jour de récup', tech: 'Jour de technique', match: 'Jour de match' }[v.kind] || 'Repas'; }
const GROUPS = [['Protéines', ['poulet', 'oeuf', 'skyr', 'whey', 'meuniere', 'thon', 'sardines']], ['Féculents', ['pates', 'riz', 'wedges', 'avoine', 'pain']], ['Fruits et légumes', ['banane', 'fruit', 'tomate', 'salade', 'legumes']], ['Épicerie', ['sauce', 'amandes', 'huile', 'miel']]];
function buyText(f, q) {
  const r5 = x => Math.ceil(x / 50) * 50;
  switch (f) {
    case 'poulet': return [fr1(Math.ceil(q / 100) / 10) + ' kg', 'poids cru'];
    case 'oeuf': return [String(q), q > 12 ? 'boîtes de 6 ou 12' : ''];
    case 'skyr': return [fr1(q / 1000) + ' kg', Math.ceil(q / 450) + ' pots de 450 g'];
    case 'whey': return [q + ' doses', '30 g par dose'];
    case 'meuniere': return [q + ' filet' + (q > 1 ? 's' : ''), ''];
    case 'thon': return [q + ' g égoutté', '1 boîte de 140 g'];
    case 'sardines': return [q + ' g égouttés', '1 boîte'];
    case 'salade': return [q + ' bols', Math.ceil(q / 5) + ' sachets environ'];
    case 'huile': return [q + ' c. à soupe', ''];
    case 'miel': return [q + ' c. à café', ''];
    case 'pain': return [q + ' tranches', Math.ceil(q / 16) + ' paquet' + (q > 16 ? 's' : '')];
    case 'banane': case 'fruit': case 'tomate': return [String(q), ''];
    default: return [r5(q) + ' g', ''];
  }
}
function coursesHtml() {
  const wk = weekKey(), week = fishWeek(), mw = isMatchWeek();
  if (!S.shop || S.shop.week !== wk) S.shop = { week: wk, checked: {} };
  const tot = {};
  MEAL_DAYS.forEach(dn => mealsFor(dn).meals.forEach(m => { for (const f in m.items) tot[f] = (tot[f] || 0) + m.items[f]; }));
  let left = 0;
  const groups = GROUPS.map(([g, list]) => {
    const rows = list.filter(f => tot[f]).map(f => { const [q, note] = buyText(f, tot[f]); const on = !!S.shop.checked[f]; if (!on) left++; return `<button type="button" class="shop" data-shop="${f}" aria-pressed="${on}"><span class="bx">${tick}</span><span class="nm">${esc((tot[f] > 1 && F(f).pl ? F(f).pl : F(f).n).replace(/ \(.*\)$/, ''))}${F(f).new ? '<span class="new">nouveau</span>' : ''}${note ? `<small>${esc(note)}</small>` : ''}</span><span class="q">${esc(q)}</span></button>`; }).join('');
    return rows ? `<section class="card grp mt12"><h3>${g}</h3>${rows}</section>` : '';
  }).join('');
  return `<section class="hero c-brand mt12" data-big="${left}"><div class="kick">Semaine ${week} · ${mw ? 'avec match' : 'sans match'}</div><h2>${left === 0 ? 'Tout est pris' : left + ' article' + (left > 1 ? 's' : '') + ' à prendre'}</h2>
      <div class="theme">${week === 'A' ? 'Poisson meunière lundi soir' : 'Thon lundi soir'} · sardines jeudi${mw ? ' · pâtes en plus pour samedi et dimanche' : ''}</div><div style="height:6px"></div></section>
    ${groups}<button type="button" class="danger" data-shopreset="1">Tout décocher</button>`;
}

/* ---------------- PROGRÈS ---------------- */
function spark(vals) {
  if (vals.length < 2) return '';
  const W = 70, H = 30, lo = Math.min(...vals), hi = Math.max(...vals), r = hi - lo || 1;
  const d = vals.map((v, i) => (i ? 'L' : 'M') + (2 + (W - 4) * i / (vals.length - 1)).toFixed(1) + ' ' + (H - 3 - (H - 6) * (v - lo) / r).toFixed(1)).join('');
  return `<svg class="spark" viewBox="0 0 ${W} ${H}" aria-hidden="true"><path d="${d}"/></svg>`;
}
function weeklyAvg() {
  const by = {};
  S.body.forEach(b => { const k = weekKey(D(b.d)); (by[k] = by[k] || []).push(b.kg); });
  return Object.keys(by).sort().map(k => ({ k, avg: by[k].reduce((a, b) => a + b, 0) / by[k].length, n: by[k].length }));
}
function weightAdvice(w) {
  if (w.length < 2) return 'Pèse-toi 2 ou 3 matins par semaine, à jeun : l’app calcule ta moyenne et te dit quoi ajuster.';
  const a = w[w.length - 1].avg, b = w[w.length - 2].avg, diff = a - b;
  if (diff < -0.7) return `Tu perds ${fr1(-diff)} kg par semaine : c’est trop rapide pour garder ta vitesse. Ajoute 40 g de pâtes ou de riz par jour (poids cru).`;
  if (w.length >= 3 && a - w[w.length - 3].avg > 0.6) return 'Ton poids monte depuis 2 semaines. Si ton tour de taille monte aussi, enlève 40 g de pâtes ou de riz par jour, sauf les jours de foot et de match.';
  if (w.length >= 4 && Math.abs(a - w[w.length - 4].avg) < 0.2) return 'Poids stable depuis 3 semaines : parfait si tu gagnes en force et que ton tour de taille baisse. Sinon, enlève 30 g de féculents le jeudi et le lundi.';
  if (diff > 0.3) return `+${fr1(diff)} kg cette semaine. Une semaine ne veut rien dire : regarde la tendance sur 2 à 3 semaines.`;
  return `${diff <= 0 ? fr1(diff) : '+' + fr1(diff)} kg par rapport à la semaine dernière : c’est le bon rythme. Continue.`;
}
function lineChart(pts, opt = {}) {
  if (pts.length < 2) return '';
  const W = 320, H = 130, L = 36, R = 10, T = 12, B = 22;
  const vals = pts.map(x => x.v); let lo = Math.min(...vals), hi = Math.max(...vals); const pad = (hi - lo) * 0.15 || (opt.pad || 0.5); lo -= pad; hi += pad;
  const X = i => L + (W - L - R) * (i / (pts.length - 1)), Y = v => T + (H - T - B) * (1 - (v - lo) / (hi - lo || 1));
  const path = pts.map((p, i) => (i ? 'L' : 'M') + X(i).toFixed(1) + ' ' + Y(p.v).toFixed(1)).join('');
  const area = path + `L${X(pts.length - 1).toFixed(1)} ${H - B}L${X(0).toFixed(1)} ${H - B}Z`;
  const fmt = opt.fmt || fr1;
  const grid = [lo, (lo + hi) / 2, hi].map(v => `<line class="gd" x1="${L}" x2="${W - R}" y1="${Y(v)}" y2="${Y(v)}"/><text x="${L - 6}" y="${Y(v) + 4}" text-anchor="end">${fmt(v)}</text>`).join('');
  const labels = pts.map((p, i) => (i === 0 || i === pts.length - 1) ? `<text x="${X(i)}" y="${H - 6}" text-anchor="${i ? 'end' : 'start'}">${fmtShort(p.d)}</text>` : '').join('');
  return `<div class="chart"><svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(opt.label || 'Évolution')}">${grid}<path class="ar" d="${area}"/><path class="ln" d="${path}"/>${pts.map((p, i) => `<circle class="pt" cx="${X(i)}" cy="${Y(p.v)}" r="${i === pts.length - 1 ? 4.5 : 3}"/>`).join('')}${labels}</svg></div>`;
}
function renderProgres() {
  const lv = levelOf(), w = weeklyAvg(), stk = streak();
  const weeks = Array.from({ length: 12 }, (_, i) => { const wk = addDays(weekKey(), -7 * (11 - i)); return { wk, n: weekActs(wk) }; });
  const maxN = 7;
  const bars = weeks.map(x => `<div><i class="${x.n >= DATA.weekGoal ? 'full' : x.n >= 3 ? 'half' : ''}" style="height:${Math.max(4, Math.round(x.n / maxN * 92))}px"></i><span>${fmtShort(x.wk).slice(0, 5)}</span></div>`).join('');
  const recs = Object.keys(S.hist).map(k => {
    const h = (S.hist[k] || []).filter(x => !x.drill); const st = exStep(k); if (!h.length || (EXD[k] && ['terrain', 'ballon', 'box'].includes(EXD[k].eq))) return null;
    const vals = h.map(x => st ? num(x.w) : x.r).filter(v => v != null);
    if (!vals.length) return null;
    const best = bestOf(k), last = vals[vals.length - 1];
    return { k, vals, best, last, d: h[h.length - 1].d, st };
  }).filter(Boolean).sort((a, b) => b.d.localeCompare(a.d));
  const recHtml = recs.length ? recs.slice(0, 14).map(r => `<div class="rec"><div class="nm"><b>${esc(exName(r.k))}</b><small>${r.vals.length} séance${r.vals.length > 1 ? 's' : ''} · record ${r.st ? frn(r.best) + ' kg' : fr0(r.best)}</small></div>${spark(r.vals)}<div class="v">${r.st ? frn(r.last) : fr0(r.last)}<small>${r.st ? (exNeg(r.k) ? 'contrepoids' : 'kg') : 'max'}</small></div></div>`).join('')
    : '<p class="muted small">Tes charges apparaîtront ici dès ta première séance.</p>';
  const T = DATA.testDef;
  const tcards = T.map(t => {
    const v = testVals(t.k); if (!v.length) return `<div class="tcard"><small>${esc(t.name)}</small><b>—</b><span class="dl muted">pas encore testé</span></div>`;
    const last = v[v.length - 1], d = v.length >= 2 ? last - v[0] : null;
    const good = d != null && (t.low ? d < 0 : d > 0);
    return `<div class="tcard"><small>${esc(t.name)}</small><b>${t.unit === 's' ? frn(last) : fr0(last)}${t.unit ? `<span style="font-size:16px"> ${t.unit}</span>` : ''}</b>${d != null && d !== 0 ? `<span class="dl ${good ? 'good' : 'bad'}">${d > 0 ? '+' : ''}${t.unit === 's' ? frn(d) : fr0(d)} ${t.unit} depuis le début</span>` : '<span class="dl muted">1er test</span>'}</div>`;
  }).join('');
  const t20 = S.tests.filter(t => num(t.t20) != null).sort((a, b) => a.d.localeCompare(b.d)).map(t => ({ d: t.d, v: num(t.t20) }));
  const nm = S.matches.length, goals = sumM('goals'), ass = sumM('assists'), mins = sumM('min');
  const lastBody = S.body[S.body.length - 1];
  view.className = '';
  view.innerHTML = `<div class="page-h"><h1>Progrès</h1><button type="button" class="ico-btn" data-sheet="settings" aria-label="Réglages">${I.gear}</button></div>
    <section class="lvcard" data-n="${lv.n}"><div class="kick">Niveau ${lv.n} ${lv.em}</div><h2>${esc(lv.t)}</h2><div class="bar gold"><i style="width:${Math.round(lv.pct * 100)}%"></i></div>
      <p>${fr0(lv.xp)} XP${lv.to ? ` · encore ${fr0(lv.to - lv.xp)} XP pour « ${esc(lv.next)} »` : ' · niveau maximum'}</p></section>
    <div class="statrow mt12"><div><b>${S.log.length}</b><small>activités</small></div><div><b>${stk}</b><small>semaines 🔥</small></div><div><b>${S.prs.length}</b><small>records</small></div></div>
    <div class="sec-t"><h2>Badges</h2><small>${Object.keys(S.badges).length}/${DATA.badges.length}</small></div>
    <div class="badges">${DATA.badges.map(b => `<div class="bdg${S.badges[b.id] ? ' on' : ''}" title="${esc(b.desc)}"><div class="em">${b.em}</div><b>${esc(b.name)}</b><small>${esc(S.badges[b.id] ? fmtShort(S.badges[b.id]) : b.desc)}</small></div>`).join('')}</div>
    <div class="sec-t"><h2>Régularité</h2><small>12 dernières semaines</small></div>
    <section class="card"><p class="small muted">Activités par semaine. En dégradé : objectif de ${DATA.weekGoal} atteint.</p><div class="bars">${bars}<div class="gl" style="bottom:${21 + Math.round(DATA.weekGoal / maxN * 92)}px"></div></div></section>
    <div class="sec-t"><h2>Vitesse & détente</h2><button type="button" data-sheet="tests">+ Ajouter</button></div>
    <div class="tgrid">${tcards}</div>
    ${t20.length >= 2 ? `<section class="card mt12"><b>Sprint 20 m</b><span class="muted small"> · plus bas = plus rapide</span>${lineChart(t20, { fmt: frn, label: 'Sprint 20 m' })}</section>` : ''}
    <div class="sec-t"><h2>Mes charges</h2><small>${recs.length} exercices</small></div>
    <section class="card">${recHtml}</section>
    <div class="sec-t"><h2>Matchs</h2><small>${nm} joué${nm > 1 ? 's' : ''}</small></div>
    <div class="statrow"><div><b>${goals}</b><small>buts</small></div><div><b>${ass}</b><small>passes D</small></div><div><b>${mins}</b><small>minutes</small></div></div>
    ${nm ? `<section class="card mt12">${S.matches.slice(-5).reverse().map(m => `<div class="hist"><span>${fmtDate(m.d)}<small>${m.min || '?'} min · effort ${m.rpe || '?'}/10</small></span><b>${m.goals || 0} but${(m.goals || 0) > 1 ? 's' : ''} · ${m.assists || 0} passe${(m.assists || 0) > 1 ? 's' : ''} D</b></div>`).join('')}</section>` : ''}
    <div class="sec-t"><h2>Poids</h2><small>moyenne par semaine</small></div>
    <section class="card"><form class="form" id="bodyform"><label>Poids (kg)<input id="kg" inputmode="decimal" autocomplete="off" placeholder="${lastBody ? fr1(lastBody.kg) : '82,0'}"></label><label>Tour de taille<input id="waist" inputmode="decimal" autocomplete="off" placeholder="cm"></label><button class="btn sm" type="submit">OK</button></form>
      <p class="small muted mt12">${esc(weightAdvice(w))}</p>${lineChart(w.slice(-10).map(x => ({ d: x.k, v: x.avg })), { label: 'Poids moyen par semaine' })}
      ${S.body.slice(-3).reverse().map(b => `<div class="hist"><span>${fmtDate(b.d)}${b.waist ? `<small>Tour de taille ${fr1(b.waist)} cm</small>` : ''}</span><b>${fr1(b.kg)} kg</b></div>`).join('')}</section>
    <div class="sec-t"><h2>Historique</h2><small>${S.log.length} au total</small></div>
    <section class="card">${S.log.length ? S.log.slice(-10).reverse().map(l => `<div class="hist c-${l.col || 'brand'}"><span><i class="pill-c"></i>${esc(l.name)} · ${fmtDate(l.d)}<small>${esc(dayDoneText(l))}${l.rpe ? ' · ressenti ' + l.rpe + '/10' : ''}</small></span><b style="color:var(--gold)">+${l.xp || 0}</b></div>`).join('') : '<p class="muted small">Tes séances apparaîtront ici.</p>'}</section>`;
}

/* ---------------- sheets ---------------- */
function openSheet(kind) {
  const p = document.getElementById('sheetp');
  if (kind === 'settings') {
    p.innerHTML = `<div class="grab"></div><h2>Réglages</h2>
      <div class="field"><label for="sname">Prénom</label><input type="text" id="sname" autocomplete="given-name" value="${esc(S.name)}" placeholder="facultatif"></div>
      <div class="field"><label>Thème</label><div class="seg" style="width:210px" role="group" aria-label="Thème"><button type="button" data-theme="auto" aria-pressed="${S.set.theme === 'auto'}">Auto</button><button type="button" data-theme="dark" aria-pressed="${S.set.theme === 'dark'}">Sombre</button><button type="button" data-theme="light" aria-pressed="${S.set.theme === 'light'}">Clair</button></div></div>
      <div class="field"><label for="sstart">Début du cycle<small>Un lundi. Semaine actuelle : ${progWeek() || 'pas commencé'}</small></label><input type="date" id="sstart" value="${esc(S.start)}"></div>
      <div class="field"><label for="sbeep">Bip à la fin du repos</label><span class="tog"><input type="checkbox" id="sbeep" ${S.set.beep ? 'checked' : ''}><span></span></span></div>
      <div class="field"><label for="swake">Écran allumé pendant la séance</label><span class="tog"><input type="checkbox" id="swake" ${S.set.wake ? 'checked' : ''}><span></span></span></div>
      <div class="field"><label for="scode">Code du coach<small>Seulement pour la version Netlify</small></label><input type="password" id="scode" autocomplete="off" value="${esc(S.coach.code)}" placeholder="ton code"></div>
      <h2 style="margin-top:18px;font-size:22px">Sauvegarde</h2>
      <p class="small muted">Tes données restent sur ce téléphone. Copie une sauvegarde de temps en temps (dans tes notes) pour la restaurer si besoin.</p>
      <div class="row mt12"><button type="button" class="btn sm" id="backup">Copier</button><button type="button" class="btn sm ghost" id="restoreopen">Restaurer</button></div>
      <div id="restore" hidden><textarea class="backup" id="restoretxt" placeholder="Colle ta sauvegarde ici"></textarea><button type="button" class="btn sm mt8" id="restoredo">Restaurer cette sauvegarde</button></div>
      <button type="button" class="danger mt16" id="newcycle">Recommencer un cycle de 12 semaines</button>
      <button type="button" class="danger" id="wipe">Tout effacer</button>`;
  } else if (kind === 'tests') {
    p.innerHTML = `<div class="grab"></div><h2>Mes tests</h2><p class="small muted">${esc(DATA.testNote)}</p><div class="tests mt12">${testInputs({})}</div><button type="button" class="btn mt16" id="testsave">Enregistrer</button>`;
  }
  p.insertAdjacentHTML('afterbegin', `<button type="button" class="ico-btn sheet-x" data-close="1" aria-label="Fermer">${I.close}</button>`);
  document.getElementById('sheet').classList.add('on'); document.body.classList.add('wo-on');
}
function closeSheet() { document.getElementById('sheet').classList.remove('on'); if (!WO.classList.contains('on')) document.body.classList.remove('wo-on'); }
function testInputs(vals) {
  return DATA.testDef.map(t => `<div class="tst"><label for="t-${t.k}">${esc(t.name)}<input id="t-${t.k}" data-test="${t.k}" inputmode="decimal" autocomplete="off" placeholder="${t.unit || 'nombre'}" value="${esc(vals[t.k] != null ? String(vals[t.k]).replace('.', ',') : '')}"></label><p>${esc(t.how)}</p></div>`).join('');
}
function readTests(root) {
  const o = {}; root.querySelectorAll('[data-test]').forEach(el => { const v = num(el.value); if (v != null) o[el.dataset.test] = v; }); return o;
}
function saveTests(o) {
  if (!Object.keys(o).length) { toast('Entre au moins un résultat.'); return false; }
  const prev = {}; DATA.testDef.forEach(t => { const v = testVals(t.k); if (v.length) prev[t.k] = t.low ? Math.min(...v) : Math.max(...v); });
  S.tests = S.tests.filter(t => t.d !== TODAY()); S.tests.push(Object.assign({ d: TODAY() }, o));
  addXP(50, 'Tests');
  DATA.testDef.forEach(t => { if (o[t.k] != null && prev[t.k] != null && (t.low ? o[t.k] < prev[t.k] : o[t.k] > prev[t.k])) { S.prs.push({ d: TODAY(), slug: 'test-' + t.k, v: o[t.k] }); addXP(25, 'Record : ' + t.name); pending.push({ kind: 'pr', name: t.name, txt: `Nouveau record : ${t.unit === 's' ? frn(o[t.k]) : fr0(o[t.k])} ${t.unit}. Avant : ${t.unit === 's' ? frn(prev[t.k]) : fr0(prev[t.k])} ${t.unit}.` }); } });
  toast('Tests enregistrés', 50);
  return true;
}
