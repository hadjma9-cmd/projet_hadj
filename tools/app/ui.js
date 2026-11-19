/* ---------------- icônes et éléments communs ---------------- */
const I = {
  gear: '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="3.2"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z"/></svg>',
  play: '<svg viewBox="0 0 24 24"><path d="M8 5.5v13a1 1 0 0 0 1.5.86l10.4-6.5a1 1 0 0 0 0-1.72L9.5 4.64A1 1 0 0 0 8 5.5z"/></svg>',
  check: '<svg viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>',
  close: '<svg viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18"/></svg>',
  chev: '<svg class="chev" viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg>',
  left: '<svg viewBox="0 0 24 24"><path d="M15 5l-7 7 7 7"/></svg>',
  right: '<svg viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg>',
  send: '<svg viewBox="0 0 24 24"><path d="M3.4 20.4 21 12 3.4 3.6 3.4 10l12.6 2-12.6 2z"/></svg>',
};
const tick = '<svg viewBox="0 0 14 14"><path d="M2.5 7.5l3 3 6-7"/></svg>';
const muscleText = arr => (arr || []).map(k => DATA.muscles[k]).join(', ');
function artHtml(e) {
  if (e.dia) return `<figure class="diafig">${e.dia}</figure>`;
  return `<div class="art"><figure class="pose">${e.a}<figcaption>${esc(e.ca)}</figcaption></figure><figure class="pose">${e.b}<figcaption>${esc(e.cb)}</figcaption></figure></div>`;
}
const thumbHtml = e => `<div class="thumb">${e.dia ? e.dia : e.b}</div>`;
function prescText(p) {
  const reps = repsFor(p.sl, p.slug, p.pr);
  const s = p.pr.sets > 1 ? `${p.pr.sets}&nbsp;×&nbsp;${esc(reps)}` : esc(reps);
  return s + (p.pr.rest ? ` · repos ${restTxt(p.pr.rest)}` : '');
}
function guideHtml(e) {
  return `<div class="guide"><div class="gb"><b>Exécution</b><p>${esc(e.how)}</p></div>
    <div class="gb ok"><b>Conseil</b><p>${esc(e.tip || '')}</p></div>
    <div class="gb no"><b>À éviter</b><p>${esc(e.err)}</p></div>
    ${e.prim && e.prim.length ? `<p class="mus-l">Muscles : ${esc(muscleText(e.prim))}</p>` : ''}</div>`;
}
function exCard(p) {
  const e = EXD[p.slug];
  return `<button type="button" class="exc" data-exd="${p.sl.id}">${thumbHtml(e)}<div class="grow"><h3>${esc(e.name)}</h3><p>${prescText(p)}</p></div>${I.chev}</button>`;
}
let toastT = null;
function toast(t) {
  const el = document.getElementById('toast');
  el.innerHTML = `<span>${esc(t)}</span>`;
  el.classList.add('show'); clearTimeout(toastT); toastT = setTimeout(() => el.classList.remove('show'), 2400);
}

/* ---------------- une journée (accueil et programme) ---------------- */
let progDay = null, sunMode = {};
function sunOf(k, wk) { return k !== 'dimanche' ? null : (sunMode[wk] || (isMatchWeek(wk) ? 'match' : 'tech')); }
function dayBody(dk, isToday) {
  const day = dayByKey(dk), mode = sunOf(dk, weekKey()), v = dayView(day, mode), info = weekInfo();
  let h = '';
  if (dk === 'dimanche') h += `<div class="seg mt12" role="group" aria-label="Dimanche"><button type="button" data-sun="match" aria-pressed="${mode === 'match'}">J’ai match</button><button type="button" data-sun="tech" aria-pressed="${mode === 'tech'}">Pas de match</button></div>`;
  const done = isToday && doneOn(TODAY());
  const btn = (lab, act) => done ? `<div class="donebar">${I.check}<span>C’est fait pour aujourd’hui. Bravo !</span></div>`
    : `<button type="button" class="btn white" data-act="${act}" data-day="${dk}">${act === 'start' ? I.play : ''}${esc(lab)}</button>`;
  h += `<section class="hero c-${v.col} mt12"><div class="kick">${isToday ? 'Aujourd’hui · ' : ''}${JOURS[KEYS.indexOf(dk)]}${v.dur ? ' · ' + esc(v.dur) : ''}</div><h2>${esc(v.name)}</h2><div class="theme">${esc(v.theme || '')}</div>`;
  if (v.kind === 'gym' || v.kind === 'speed' || v.kind === 'tech') {
    h += `<div style="height:16px"></div>${btn('Commencer', 'start')}</section>`;
    if (day.note) h += `<p class="note">${esc(day.note)}</p>`;
    if (v.place) h += `<p class="note">Matériel : ${esc(v.place)}</p>`;
    h += `<div class="exl">${planFor(day, mode, info).map(exCard).join('')}</div>`;
  } else if (v.kind === 'foot') {
    h += `<p class="theme mt12">${esc(day.text)}</p><div style="height:16px"></div>${btn('C’est fait', 'done')}</section>`;
  } else if (v.kind === 'recup') {
    h += `<div style="height:16px"></div>${btn('C’est fait', 'done')}</section>`;
    h += `<div class="exl">${day.items.map(it => it.ex ? `<button type="button" class="exc" data-exr="${it.ex}">${thumbHtml(EXD[it.ex])}<div class="grow"><h3>${esc(it.txt)}</h3><p>${esc(EXD[it.ex].tip || '')}</p></div>${I.chev}</button>`
      : `<div class="exc static"><div class="grow"><h3>${esc(it.txt)}</h3><ul>${(it.list || []).map(x => `<li>${esc(x)}</li>`).join('')}</ul></div></div>`).join('')}</div>`;
  } else if (v.kind === 'match') {
    h += `<div style="height:16px"></div>${btn('Match joué', 'done')}</section>`;
    h += `<div class="exl"><div class="exc static"><div class="grow"><h3>Avant le match</h3><ul>${day.match.before.map(x => `<li>${esc(x)}</li>`).join('')}</ul></div></div>
      <div class="exc static"><div class="grow"><h3>Échauffement</h3><ul>${DATA.warmup.match.map(x => `<li>${esc(x)}</li>`).join('')}</ul></div></div>
      <div class="exc static"><div class="grow"><h3>Après le match</h3><ul>${day.match.after.map(x => `<li>${esc(x)}</li>`).join('')}</ul></div></div></div>`;
  }
  return h;
}

/* ---------------- AUJOURD’HUI ---------------- */
function renderAccueil() {
  const dk = todayKey(), info = weekInfo(), now = new Date();
  const wk = ORDER.map((k, i) => {
    const d = addDays(weekKey(), i), v = dayView(dayByKey(k), sunOf(k, weekKey())), done = doneOn(d);
    return `<button type="button" class="wd c-${v.col}${done ? ' on' : ''}${d === TODAY() ? ' today' : ''}" data-go="programme" data-day="${k}"><small>${JOURS[(i + 1) % 7].slice(0, 3).toUpperCase()}</small><i>${done ? I.check : D(d).getDate()}</i><span>${esc(v.tag)}</span></button>`;
  }).join('');
  view.innerHTML = `
    <div class="hello"><div class="avatar">10</div><div class="grow"><h1>${S.name ? 'Salut ' + esc(S.name) : 'Salut'}</h1><p>${JOURS[now.getDay()]} ${fmtDate(TODAY())}${info.before ? '' : ' · semaine ' + info.w + ' sur 12'}</p></div><button type="button" class="ico-btn" data-sheet="settings" aria-label="Réglages">${I.gear}</button></div>
    ${dayBody(dk, true)}
    <div class="sec-t"><h2>Ma semaine</h2></div>
    <div class="week">${wk}</div>`;
}

/* ---------------- PROGRAMME ---------------- */
function renderProgramme() {
  const dk = progDay || todayKey();
  const chips = ORDER.map(k => { const v = dayView(dayByKey(k), sunOf(k, weekKey())); return `<button type="button" class="chip c-${v.col}" data-day="${k}" aria-pressed="${k === dk}"><b>${JOURS[KEYS.indexOf(k)].slice(0, 3)}</b><span>${esc(v.tag)}</span></button>`; }).join('');
  view.innerHTML = `<div class="page-h"><h1>Programme</h1></div>
    <div class="chips dchips">${chips}</div>
    ${dayBody(dk, dk === todayKey())}
    <section class="card mt16"><h3 class="ct-h">Pour progresser</h3>
      <ul class="rules-l"><li>Tu réussis toutes les séries facilement ? Prends un peu plus lourd la fois suivante.</li>
      <li>Garde toujours 1 ou 2 répétitions en réserve : jamais jusqu’à l’échec.</li>
      <li>Une douleur dans une articulation : arrête l’exercice.</li></ul></section>`;
}

/* ---------------- REPAS ---------------- */
let mealDay = JOURS[new Date().getDay()], mealTab = 'menus';
const MEAL_DAYS = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'];
function qtyLabel(f, q) {
  const x = F(f);
  if (x.per === 'g') return `<b>${q} g</b> ${esc(x.n)}`;
  if (x.unit) return `<b>${q} ${esc(x.unit)}${q > 1 && !/\./.test(x.unit) ? 's' : ''}</b> ${esc(x.n)}`;
  return `<b>${q}</b> ${esc(q > 1 && x.pl ? x.pl : x.n)}`;
}
function renderRepas() {
  const chips = MEAL_DAYS.map(dn => `<button type="button" class="chip" data-mday="${dn}" aria-pressed="${dn === mealDay}"><b>${dn.slice(0, 3)}</b></button>`).join('');
  let content;
  if (mealTab === 'menus') {
    const r = mealsFor(mealDay);
    content = `<div class="chips mt12">${chips}</div>
      ${r.meals.map(m => `<article class="meal"><h3>${esc(m.name)}</h3>${m.title ? `<p class="dish">${esc(m.title)}</p>` : ''}<ul class="foods">${Object.keys(m.items).map(f => `<li>${qtyLabel(f, m.items[f])}</li>`).join('')}</ul></article>`).join('')}
      ${mealDay === 'Samedi' || mealDay === 'Dimanche' ? '<p class="note">Match le lendemain : ajoute 40 g de pâtes au dîner. Jour de match : repas 3 h avant.</p>' : ''}
      <p class="note">Poulet, pâtes et riz pesés crus. Une seule whey par jour.</p>`;
  } else content = coursesHtml();
  view.innerHTML = `<div class="page-h"><h1>Repas</h1></div>
    <div class="seg" role="group" aria-label="Menus ou courses"><button type="button" data-mtab="menus" aria-pressed="${mealTab === 'menus'}">Menus</button><button type="button" data-mtab="courses" aria-pressed="${mealTab === 'courses'}">Courses</button></div>
    ${content}`;
}
const GROUPS = [['Viande, poisson, œufs', ['poulet', 'oeuf', 'meuniere', 'thon', 'sardines']], ['Laitier, whey', ['skyr', 'whey']], ['Féculents', ['pates', 'riz', 'wedges', 'avoine', 'pain']], ['Fruits et légumes', ['banane', 'fruit', 'tomate', 'salade', 'legumes']], ['Épicerie', ['sauce', 'amandes', 'huile', 'miel']]];
function buyText(f, q) {
  const r = x => Math.ceil(x / 50) * 50;
  switch (f) {
    case 'poulet': case 'skyr': return (Math.ceil(q / 100) / 10).toLocaleString('fr-FR') + ' kg';
    case 'whey': return q + ' doses';
    case 'meuniere': return q + ' filet' + (q > 1 ? 's' : '');
    case 'thon': case 'sardines': return '1 boîte';
    case 'salade': return q + ' bols';
    case 'huile': return q + ' c. à soupe';
    case 'miel': return q + ' c. à café';
    case 'pain': return q + ' tranches';
    case 'oeuf': case 'banane': case 'fruit': case 'tomate': return String(q);
    default: return r(q) + ' g';
  }
}
function coursesHtml() {
  const wk = weekKey();
  if (!S.shop || S.shop.week !== wk) S.shop = { week: wk, checked: {} };
  const tot = {};
  MEAL_DAYS.forEach(dn => mealsFor(dn).meals.forEach(m => { for (const f in m.items) tot[f] = (tot[f] || 0) + m.items[f]; }));
  return GROUPS.map(([g, list]) => {
    const rows = list.filter(f => tot[f]).map(f => { const on = !!S.shop.checked[f]; return `<button type="button" class="shop" data-shop="${f}" aria-pressed="${on}"><span class="bx">${tick}</span><span class="nm">${esc((tot[f] > 1 && F(f).pl ? F(f).pl : F(f).n).replace(/ \(.*\)$/, ''))}</span><span class="q">${esc(buyText(f, tot[f]))}</span></button>`; }).join('');
    return rows ? `<section class="card grp mt12"><h3>${g}</h3>${rows}</section>` : '';
  }).join('') + `<button type="button" class="danger" data-shopreset="1">Tout décocher</button>`;
}

/* ---------------- fiches (exercice, réglages) ---------------- */
function openSheet(kind, arg) {
  const p = document.getElementById('sheetp');
  if (kind === 'ex' || kind === 'exr') {
    let e, slug, line = '', vsw = '';
    if (kind === 'ex') {
      const sl = slotById(arg); slug = slotSlug(sl); e = EXD[slug];
      const pr = presc(sl, weekInfo()); line = pr ? `<p class="presc-l">${prescText({ sl, slug, pr })}</p>` : '';
      const opts = slotOptions(sl);
      if (opts.length > 1) vsw = `<div class="vsw"><small>Si c’est pris</small>${opts.map((o, i) => `<button type="button" data-svar="${sl.id}" data-i="${i}" aria-pressed="${o === slug}">${esc(EXD[o].short || EXD[o].name)}</button>`).join('')}</div>`;
    } else { slug = arg; e = EXD[slug]; }
    p.innerHTML = `<div class="grab"></div><h2>${esc(e.name)}</h2>${line}${vsw}<div class="mt12">${artHtml(e)}</div>${guideHtml(e)}`;
  } else if (kind === 'settings') {
    p.innerHTML = `<div class="grab"></div><h2>Réglages</h2>
      <div class="field"><label for="sname">Prénom</label><input type="text" id="sname" autocomplete="given-name" value="${esc(S.name)}" placeholder="facultatif"></div>
      <div class="field"><label>Thème</label><div class="seg" style="width:210px" role="group" aria-label="Thème"><button type="button" data-theme="auto" aria-pressed="${S.set.theme === 'auto'}">Auto</button><button type="button" data-theme="dark" aria-pressed="${S.set.theme === 'dark'}">Sombre</button><button type="button" data-theme="light" aria-pressed="${S.set.theme === 'light'}">Clair</button></div></div>
      <div class="field"><label for="sstart">Début du programme<small>Un lundi</small></label><input type="date" id="sstart" value="${esc(S.start)}"></div>
      <div class="field"><label for="sbeep">Bip à la fin du repos</label><span class="tog"><input type="checkbox" id="sbeep" ${S.set.beep ? 'checked' : ''}><span></span></span></div>
      <div class="field"><label for="swake">Écran allumé pendant la séance</label><span class="tog"><input type="checkbox" id="swake" ${S.set.wake ? 'checked' : ''}><span></span></span></div>
      <div class="field"><label for="scode">Code du coach<small>Version Netlify seulement</small></label><input type="password" id="scode" autocomplete="off" value="${esc(S.coach.code)}" placeholder="ton code"></div>
      <div class="row mt16"><button type="button" class="btn sm" id="backup">Copier une sauvegarde</button><button type="button" class="btn sm ghost" id="restoreopen">Restaurer</button></div>
      <div id="restore" hidden><textarea class="backup" id="restoretxt" placeholder="Colle ta sauvegarde ici"></textarea><button type="button" class="btn sm mt8" id="restoredo">Restaurer</button></div>`;
  }
  p.insertAdjacentHTML('afterbegin', `<button type="button" class="ico-btn sheet-x" data-close="1" aria-label="Fermer">${I.close}</button>`);
  document.getElementById('sheet').classList.add('on'); document.body.classList.add('wo-on');
  p.scrollTop = 0;
}
function closeSheet() { document.getElementById('sheet').classList.remove('on'); if (!WO.classList.contains('on')) document.body.classList.remove('wo-on'); }
