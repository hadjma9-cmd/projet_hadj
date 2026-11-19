/* ---------------- icônes ---------------- */
const I = {
  check: '<svg viewBox="0 0 24 24"><path d="M6 12.5l4 4 8-9"/></svg>',
  chev: '<svg class="chev" viewBox="0 0 24 24"><path d="M9 6l6 6-6 6"/></svg>',
  close: '<svg viewBox="0 0 24 24"><path d="M6.5 6.5l11 11M17.5 6.5l-11 11"/></svg>',
  play: '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9.5"/><path class="fill" d="M10 8.6v6.8l5.6-3.4z"/></svg>',
  ok: '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9.5"/><path d="M8 12.4l2.8 2.8 5.4-5.6"/></svg>',
  no: '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9.5"/><path d="M9 9l6 6M15 9l-6 6"/></svg>',
  swap: '<svg viewBox="0 0 24 24"><path d="M5 9h13l-3.5-3.5M19 15H6l3.5 3.5"/></svg>',
  whistle: '<svg viewBox="0 0 24 24"><path d="M9 8.5h11.5v4.2h-6.6"/><circle cx="9" cy="14" r="5.5"/><circle cx="9" cy="14" r="1.5"/></svg>',
  flame: '<svg viewBox="0 0 24 24"><path d="M12 3.5c.6 2.8 4.5 4.6 4.5 9a4.5 4.5 0 0 1-9 0c0-1.9.9-3.3 2-4.2.1 1.4.8 2.3 1.8 2.7-.2-2.6-.3-5 .7-7.5z"/></svg>',
  cart: '<svg viewBox="0 0 24 24"><path d="M3 4.5h2.2l2.1 10.2h10.2l2-7.2H6.6"/><circle cx="9.3" cy="19" r="1.4"/><circle cx="16.4" cy="19" r="1.4"/></svg>',
  send: '<svg viewBox="0 0 24 24"><path d="M12 19V5M5.5 11.5 12 5l6.5 6.5"/></svg>',
};
const nomJour = k => JOURS[KEYS.indexOf(k)];
let selDay = todayKey(), warmOpen = false, shopOpen = false;

/* ---------------- textes d'une prescription ---------------- */
function prescLine(sl, slug, pr) {
  const reps = repsFor(sl, slug, pr);
  return (pr.sets > 1 ? `${pr.sets}&nbsp;×&nbsp;${esc(reps)}` : esc(reps)) + (pr.rest ? `, repos ${restTxt(pr.rest)}` : '');
}
function scoreItems(sl, slug, pr) {   // les trois chiffres de la fiche : séries, répétitions, repos
  const reps = String(repsFor(sl, slug, pr)), out = [];
  if (pr.sets > 1) out.push([String(pr.sets), 'séries']);
  const m = reps.match(/^(\d+(?:\s*[–-]\s*\d+)?)\s*(.*)$/);
  if (!m) out.push([esc(reps), '']);
  else {
    const n = m[1], rest = m[2].replace(/^,\s*/, '');
    if (rest === '') out.push([n, 'répétitions']);
    else if (/^(s|min)$/.test(rest)) out.push([n + '&nbsp;' + rest, rest === 's' ? 'tenue' : 'durée']);
    else if (rest === 'm') out.push([n + '&nbsp;m', 'distance']);
    else if (/^m\b/.test(rest)) out.push([n + '&nbsp;m', rest.replace(/^m\s*\+?\s*/, 'puis ')]);
    else out.push([n, /^(par |passes|passage)/.test(rest) ? rest : 'répétitions, ' + rest]);
  }
  if (pr.rest) out.push([pr.rest < 60 ? pr.rest + '&nbsp;s' : pr.rest % 60 ? Math.floor(pr.rest / 60) + ':' + p2(pr.rest % 60) : pr.rest / 60 + '&nbsp;min', 'repos']);
  return out;
}

/* ---------------- bandeau « terrain » ---------------- */
function dayStrip() {
  return `<nav class="days" aria-label="Jours de la semaine">${ORDER.map(k => {
    const sel = k === selDay, today = k === todayKey(), done = dayDone(k);
    return `<button type="button" class="dy${sel ? ' sel' : ''}" data-day="${k}" aria-pressed="${sel}" aria-label="${nomJour(k)}${today ? ', aujourd’hui' : ''}${done ? ', fait' : ''}"><span>${nomJour(k).slice(0, 3)}</span><i class="${done ? 'd' : today ? 't' : ''}">${done ? I.check : ''}</i></button>`;
  }).join('')}</nav>`;
}
const LINES = '<svg class="lines" viewBox="0 0 390 300" preserveAspectRatio="xMaxYMid slice" aria-hidden="true"><path d="M318 -10V310"/><circle cx="318" cy="168" r="74"/><circle cx="318" cy="168" r="4.5" class="spot"/></svg>';
const PLATE = '<svg class="lines" viewBox="0 0 390 300" preserveAspectRatio="xMaxYMid slice" aria-hidden="true"><circle cx="318" cy="168" r="74"/><circle cx="318" cy="168" r="61"/><circle cx="318" cy="168" r="17"/><circle cx="318" cy="168" r="6" class="spot"/><text x="318" y="131" class="plate-t">20</text><text x="318" y="222" class="plate-t sm">kg</text></svg>';
const TERRAIN = ['mercredi', 'jeudi', 'dimanche'];
const themeOf = k => k === 'dimanche' ? (S.match[weekKey()] ? 'terrain' : 'salle') : TERRAIN.includes(k) ? 'terrain' : 'salle';
const band = (inner, days = true, th = 'terrain') => `<header class="band ${th}">${th === 'salle' ? PLATE : LINES}${days ? dayStrip() : ''}<div class="band-in">${inner}</div></header>`;

/* ---------------- les fiches du jour (ce qu'on fait défiler) ---------------- */
function deckFor(k, which) {
  const day = dayByKey(k), info = weekInfo();
  const fromSlots = slots => slots.map(sl => ({ sl, slug: slotSlug(sl), pr: presc(sl, info) })).filter(p => p.pr)
    .map(p => ({ id: p.sl.id, type: 'ex', sl: p.sl, slug: p.slug, pr: p.pr }));
  if (day.kind === 'gym' || day.kind === 'speed') return fromSlots(day.slots);
  if (day.kind === 'recup') return day.items.map(it => it.ex
    ? { id: it.id, type: 'ex', sl: { id: it.id, ex: it.ex, alts: [], kind: 'recup' }, slug: it.ex, pr: { sets: 1, reps: '20 min', rest: 0 }, name: 'Vélo facile' }
    : { id: it.id, type: 'list', name: 'Étirements', sub: '10 min, sans forcer', list: it.list });
  if (day.kind === 'sunday') return which === 'match' ? [{ id: 'm1', type: 'match' }] : fromSlots(dayByKey('mardi').slots);   // dimanche : haut du corps, avec ou sans match
  return [];
}
const cardName = c => c.type === 'ex' ? (c.name || EXD[c.slug].name) : c.type === 'match' ? 'Match' : c.name;

/* ---------------- SÉANCE ---------------- */
function lineupHtml(k, deck, which, warmKey, title) {
  const d = dateOf(k);
  let h = '<section class="lineup">' + (title ? `<h2 class="lh">${esc(title)}</h2>` : '');
  if (warmKey) {
    h += `<button type="button" class="row warm" data-warm="1" aria-expanded="${warmOpen}"><span class="num ic">${I.flame}</span><span class="tx"><b>Échauffement</b><small>8 à 10 min</small></span>${I.chev}</button>`;
    if (warmOpen) h += `<ul class="warm-l">${DATA.warmup[warmKey].map(x => `<li>${esc(x)}</li>`).join('')}</ul>`;
  }
  h += '<ol class="xs">' + deck.map((c, i) => {
    const on = checked(d, c.id);
    const sub = c.type === 'ex' ? (c.sl.kind === 'recup' ? '20 min, sans forcer' : prescLine(c.sl, c.slug, c.pr)) : c.type === 'list' ? esc(c.sub) : 'Avant, échauffement, après';
    const voir = c.type === 'ex' ? 'Voir l’exécution' : c.type === 'list' ? 'Voir les étirements' : 'Voir le déroulé';
    return `<li class="x${on ? ' on' : ''}"><span class="num${c.type === 'match' ? ' ic' : ''}">${on ? I.check : c.type === 'match' ? I.whistle : i + 1}</span>`
      + `<button type="button" class="tx" data-deck="${which}" data-i="${i}"><b>${esc(cardName(c))}</b><small>${sub}</small></button>`
      + `<button type="button" class="tick" data-ck="${c.id}" aria-pressed="${on}" aria-label="${esc(cardName(c))} : fait">${I.check}<small>Fait</small></button>`
      + `<button type="button" class="voir" data-deck="${which}" data-i="${i}">${I.play}<span>${voir}</span></button></li>`;
  }).join('') + '</ol>';
  return h + '</section>';
}
function renderSeance() {
  const k = selDay, day = dayByKey(k), info = weekInfo(), d = dateOf(k), today = k === todayKey();
  let what = day.name, meta = '', cta = '', body = '';
  const foot = [], done = dayDone(k);
  if (day.kind === 'gym' || day.kind === 'speed' || day.kind === 'recup') {
    const deck = deckFor(k, 'main'), n = deck.filter(c => checked(d, c.id)).length;
    meta = day.kind === 'recup' ? `${day.theme}, ${day.dur}` : `${deck.length} exercices, ${day.dur}`;
    cta = done ? `<p class="fini">${I.check}<span>${day.kind === 'recup' ? 'Récup faite' : 'Séance terminée'}. Bien joué&nbsp;!</span></p>`
      : `<button type="button" class="cta" data-start="main">${n ? 'Continuer' : 'Commencer'}</button>`;
    body = lineupHtml(k, deck, 'main', day.warm);
    if (day.note) foot.push(day.note);
    if (day.place) foot.push('Matériel : ' + day.place.charAt(0).toLowerCase() + day.place.slice(1) + '.');
    if (info.learn && day.kind === 'gym') foot.push('Semaines 1 et 2 : 2 séries seulement, le temps d’apprendre les gestes.');
    if (info.deload && day.kind !== 'recup') foot.push('Semaine plus légère : une série de moins partout.');
    if (day.kind === 'gym') foot.push('Toutes tes répétitions passent facilement ? Ajoute un peu de poids la fois suivante. Garde toujours 1 ou 2 répétitions en réserve.');
  } else if (day.kind === 'rest') {
    meta = day.theme;
    body = `<section class="lineup text"><p>${esc(day.text)}</p></section>`;
  } else if (day.kind === 'foot') {
    meta = 'Avec ton équipe';
    cta = checked(d, 'f1') ? `<button type="button" class="fini as-btn" data-ck="f1">${I.check}<span>Entraînement fait. Bien joué&nbsp;!</span></button>`
      : `<button type="button" class="cta" data-ck="f1">C’est fait</button>`;
    body = `<section class="lineup text"><p>${esc(day.text)}</p></section>`;
  } else if (day.kind === 'sunday') {
    const m = S.match[weekKey()];
    what = m === true ? 'Match et haut du corps' : 'Haut du corps';
    meta = m ? 'Le haut du corps après le match, plus léger' : 'Salle, 45 min';
    if (done) cta = `<p class="fini">${I.check}<span>${'Séance terminée'}. Bien joué&nbsp;!</span></p>`;
    body = (m ? lineupHtml(k, deckFor(k, 'match'), 'match', null, 'Le match') : '') + lineupHtml(k, deckFor(k, 'tech'), 'tech', 'haut', m ? 'Après le match : haut du corps' : null);
    body += `<button type="button" class="lnk center" data-match="${m ? '0' : '1'}"><span>${m ? 'Finalement je ne joue pas' : 'Je joue un match dimanche'}</span></button>`;
  }
  const wk = weekKey(), ans = S.match[wk];
  const ask = ['vendredi', 'samedi', 'dimanche'].includes(k) && ['vendredi', 'samedi', 'dimanche'].includes(todayKey()) && ans === undefined
    ? `<div class="ask"><p>Tu joues un match dimanche ?</p><div><button type="button" data-match="1">Oui</button><button type="button" data-match="0">Non</button></div></div>` : '';
  view.innerHTML = band(`${today ? '<p class="when">Aujourd’hui</p>' : ''}<h1 class="xd">${nomJour(k)}</h1><p class="what">${esc(what)}</p>${meta ? `<p class="meta">${esc(meta)}</p>` : ''}${cta}${ask}`, true, themeOf(k))
    + `<div class="page">${body}${foot.map(f => `<p class="foot">${esc(f)}</p>`).join('')}</div>`;
}

/* ---------------- la fiche plein écran (on fait défiler les exercices) ---------------- */
let SH = null;   // { k, which, deck, i }
const sheetEl = () => document.getElementById('sheet');
function ytUrl(sl, e) {
  const q = e.name.replace(/\s*\(.*\)/, '') + (['plyo', 'sprint', 'cod', 'ball'].includes(sl.kind) ? ' exercice football' : ' musculation');
  return 'https://www.youtube.com/results?search_query=' + encodeURIComponent(q);
}
function cardHtml(c, d) {
  if (c.type === 'list') return `<article class="card"><h2 class="xd">${esc(c.name)}</h2><p class="lead">${esc(c.sub)}</p><ol class="steps">${c.list.map(x => `<li>${esc(x)}</li>`).join('')}</ol></article>`;
  if (c.type === 'match') {
    const m = dayByKey('dimanche').match;
    const li = a => `<ul class="plain">${a.map(x => `<li>${esc(x)}</li>`).join('')}</ul>`;
    return `<article class="card"><h2 class="xd">Jour de match</h2><h3>Avant</h3>${li(m.before)}<h3>Échauffement</h3>${li(DATA.warmup.match)}<h3>Après</h3>${li(m.after)}</article>`;
  }
  const e = EXD[c.slug], sl = c.sl, opts = slotOptions(sl);
  let h = `<article class="card">${figHtml(c.slug)}<h2 class="xd">${esc(cardName(c))}</h2>`;
  h += `<div class="score">${scoreItems(sl, c.slug, c.pr).map(([v, l]) => `<div><b class="xd">${v}</b><small>${esc(l)}</small></div>`).join('')}</div>`;
  if (e.steps && e.steps.length) h += `<ol class="steps">${e.steps.map(s => `<li>${esc(s)}</li>`).join('')}</ol>`;
  if (e.tip) h += `<p class="tip ok">${I.ok}<span>${esc(e.tip)}</span></p>`;
  if (e.err) h += `<p class="tip no">${I.no}<span>${esc(e.err)}</span></p>`;
  if (modeOf(sl, c.slug, repsFor(sl, c.slug, c.pr)) === 'load') {
    const cur = histOn(c.slug, d), last = lastBefore(c.slug, d);
    const hint = last != null ? `La dernière fois : ${frn(last)}&nbsp;kg` : e.start ? `Pour commencer : ${esc(e.neg ? e.start.replace(/^Contrepoids\s*/i, '') : e.start)}` : '';
    h += `<div class="wt"><label for="w-${sl.id}">${e.neg ? 'Contrepoids' : 'Poids'}</label><input id="w-${sl.id}" type="text" inputmode="decimal" autocomplete="off" enterkeyhint="done" data-w="${c.slug}" value="${cur != null ? frn(cur) : ''}" placeholder="–"><span>kg</span>${hint ? `<small>${hint}</small>` : ''}</div>`;
  }
  h += '<div class="links">';
  opts.forEach((o, j) => { if (o !== c.slug) h += `<button type="button" class="lnk" data-alt="${sl.id}" data-j="${j}">${I.swap}<span>${o === sl.ex ? 'Revenir à' : 'Pas dispo ? Fais plutôt'} : ${esc(EXD[o].name)}</span></button>`; });
  return h + '</div></article>';
}
function renderSheet() {
  const el = sheetEl(), d = dateOf(SH.k);
  SH.deck = deckFor(SH.k, SH.which);
  const hint = !S.seenSwipe && SH.deck.length > 1;
  if (hint) { S.seenSwipe = true; save(); }
  el.innerHTML = `<div class="sh-top"><button type="button" class="shx" data-close="1" aria-label="Fermer">${I.close}</button><div class="segs">${SH.deck.map((c, j) => `<button type="button" data-seg="${j}" aria-label="${esc(cardName(c))}"></button>`).join('')}</div></div>
    ${hint ? '<p class="swipe-hint">Glisse sur le côté pour passer d’un exercice à l’autre.</p>' : ''}
    <div class="track" id="track">${SH.deck.map(c => cardHtml(c, d)).join('')}</div>
    <div class="sh-bot"><button type="button" class="go" data-done="1"></button></div>`;
  const tr = document.getElementById('track');
  tr.addEventListener('scroll', onTrack, { passive: true });
  tr.scrollLeft = SH.i * tr.clientWidth;
  syncSheet();
}
function syncSheet() {   // segments, bouton du bas, dessin animé
  const d = dateOf(SH.k), c = SH.deck[SH.i];
  sheetEl().querySelectorAll('[data-seg]').forEach((b, j) => { b.className = (checked(d, SH.deck[j].id) ? 'd' : '') + (j === SH.i ? ' c' : ''); });
  const go = sheetEl().querySelector('.go'), on = checked(d, c.id);
  go.className = 'go' + (on ? ' is-done' : '');
  go.innerHTML = on ? `${I.check}<span>Fait</span>` : `<span>${c.type === 'match' ? 'Match joué' : 'C’est fait'}</span>`;
  go.setAttribute('aria-label', on ? cardName(c) + ' : fait. Toucher pour annuler' : cardName(c) + ' : c’est fait');
  const card = sheetEl().querySelectorAll('.card')[SH.i];
  playFig(card && card.querySelector('svg[data-rig]'));
}
let trackRaf = 0;
function onTrack() {
  cancelAnimationFrame(trackRaf);
  trackRaf = requestAnimationFrame(() => {
    const tr = document.getElementById('track'); if (!tr || !SH) return;
    const i = Math.max(0, Math.min(SH.deck.length - 1, Math.round(tr.scrollLeft / tr.clientWidth)));
    if (i !== SH.i) { SH.i = i; syncSheet(); }
  });
}
const smooth = () => { try { return !matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) { return true; } };
function goCard(i) { const tr = document.getElementById('track'); if (tr) tr.scrollTo({ left: i * tr.clientWidth, behavior: smooth() ? 'smooth' : 'auto' }); }
function openSheet(which, i) {
  SH = { k: selDay, which, i };
  sheetEl().dataset.th = themeOf(selDay);
  document.body.classList.add('sheet-on');
  sheetEl().setAttribute('aria-hidden', 'false');
  sheetEl().classList.add('on');
  renderSheet();
}
function closeSheet() {
  cancelAnimationFrame(figRaf);
  sheetEl().classList.remove('on');
  sheetEl().setAttribute('aria-hidden', 'true');
  document.body.classList.remove('sheet-on');
  SH = null;
  rerender();
  setTimeout(() => { if (!SH) sheetEl().innerHTML = ''; }, 350);
}

/* ---------------- REPAS ---------------- */
function qtyLabel(f, q) {
  const x = F(f), n = s => esc(s.replace(' (poids cru)', ''));
  if (x.per === 'g') return `<b>${q}&nbsp;g</b> ${n(x.n)}`;
  if (x.unit) return `<b>${q} ${esc(x.unit)}${q > 1 && !/\./.test(x.unit) ? 's' : ''}</b> ${n(x.n)}`;
  return `<b>${q}</b> ${n(q > 1 && x.pl ? x.pl : x.n)}`;
}
function renderRepas() {
  const dn = nomJour(selDay), r = mealsFor(dn);
  view.innerHTML = band(`${selDay === todayKey() ? '<p class="when">Aujourd’hui</p>' : ''}<h1 class="xd">${dn}</h1><p class="what">Repas</p><p class="meta">Environ ${fr0(r.md.target)}&nbsp;kcal</p>`, true, themeOf(selDay))
    + `<div class="page"><section class="lineup meals">${r.meals.map(m => `<div class="meal"><h2>${esc(m.name)}</h2>${m.title ? `<p class="dish">${esc(m.title)}</p>` : ''}<ul>${Object.keys(m.items).map(f => `<li>${qtyLabel(f, m.items[f])}</li>`).join('')}</ul></div>`).join('')}</section>
    ${dn === 'Samedi' || dn === 'Dimanche' ? '<p class="foot">Match le lendemain : ajoute 40&nbsp;g de pâtes au dîner. Jour de match : repas 3&nbsp;h avant.</p>' : ''}
    <p class="foot">Poulet, pâtes et riz pesés crus. Une seule whey par jour.</p>
    <section class="lineup"><button type="button" class="row" data-shopopen="1" aria-expanded="${shopOpen}"><span class="num ic">${I.cart}</span><span class="tx"><b>Liste de courses</b><small>Pour toute la semaine</small></span>${I.chev}</button>${shopOpen ? `<div class="shop-in">${coursesHtml()}</div>` : ''}</section></div>`;
}
const GROUPS = [['Viande, poisson, œufs', ['poulet', 'oeuf', 'meuniere', 'thon', 'sardines']], ['Laitier, whey', ['skyr', 'whey']], ['Féculents', ['pates', 'riz', 'wedges', 'avoine', 'pain']], ['Fruits et légumes', ['banane', 'fruit', 'tomate', 'salade', 'legumes']], ['Épicerie', ['sauce', 'amandes', 'huile', 'miel']]];
function buyText(f, q) {
  const r = x => Math.ceil(x / 50) * 50;
  switch (f) {
    case 'poulet': case 'skyr': return (Math.ceil(q / 100) / 10).toLocaleString('fr-FR') + '&nbsp;kg';
    case 'whey': return q + ' doses';
    case 'meuniere': return q + ' filet' + (q > 1 ? 's' : '');
    case 'thon': case 'sardines': return '1 boîte';
    case 'salade': return q + ' bols';
    case 'huile': return q + ' c. à soupe';
    case 'miel': return q + ' c. à café';
    case 'pain': return q + ' tranches';
    case 'oeuf': case 'banane': case 'fruit': case 'tomate': return String(q);
    default: return r(q) + '&nbsp;g';
  }
}
function coursesHtml() {
  const wk = weekKey();
  if (!S.shop || S.shop.week !== wk) S.shop = { week: wk, checked: {} };
  const tot = {};
  ORDER.forEach(k => mealsFor(nomJour(k)).meals.forEach(m => { for (const f in m.items) tot[f] = (tot[f] || 0) + m.items[f]; }));
  return GROUPS.map(([g, list]) => {
    const rows = list.filter(f => tot[f]).map(f => { const on = !!S.shop.checked[f]; return `<li class="shop${on ? ' on' : ''}"><button type="button" class="tick sm" data-shop="${f}" aria-pressed="${on}" aria-label="${esc(F(f).n)}">${I.check}</button><span class="nm">${esc((tot[f] > 1 && F(f).pl ? F(f).pl : F(f).n).replace(/ \(.*\)$/, ''))}</span><span class="q">${buyText(f, tot[f])}</span></li>`; }).join('');
    return rows ? `<h3>${g}</h3><ul class="shopl">${rows}</ul>` : '';
  }).join('') + (Object.keys(S.shop.checked).length ? '<button type="button" class="lnk" data-shopreset="1"><span>Tout décocher</span></button>' : '');
}
