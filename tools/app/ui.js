/* ---------------- icônes ---------------- */
const I = {
  check: '<svg viewBox="0 0 24 24"><path d="M6 12.5l4 4 8-9"/></svg>',
  chev: '<svg class="chev" viewBox="0 0 24 24"><path d="M9 6l6 6-6 6"/></svg>',
  play: '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9.5"/><path class="fill" d="M10 8.6v6.8l5.6-3.4z"/></svg>',
  ok: '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9.5"/><path d="M8 12.4l2.8 2.8 5.4-5.6"/></svg>',
  no: '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9.5"/><path d="M9 9l6 6M15 9l-6 6"/></svg>',
  swap: '<svg viewBox="0 0 24 24"><path d="M5 9h13l-3.5-3.5M19 15H6l3.5 3.5"/></svg>',
  warm: '<svg viewBox="0 0 24 24"><path d="M12 3.5c.6 2.8 4.5 4.6 4.5 9a4.5 4.5 0 0 1-9 0c0-1.9.9-3.3 2-4.2.1 1.4.8 2.3 1.8 2.7-.2-2.6-.3-5 .7-7.5z"/></svg>',
  ball: '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7.5l3.6 2.6-1.4 4.2H9.8l-1.4-4.2z"/><path d="M12 3v4.5M15.6 10.1l4.6-1.5M14.2 14.3l2.8 4M9.8 14.3 7 18.3M8.4 10.1 3.8 8.6"/></svg>',
  send: '<svg viewBox="0 0 24 24"><path d="M12 19V5M5.5 11.5 12 5l6.5 6.5"/></svg>',
  cart: '<svg viewBox="0 0 24 24"><path d="M3 4.5h2.2l2.1 10.2h10.2l2-7.2H6.6"/><circle cx="9.3" cy="19" r="1.4"/><circle cx="16.4" cy="19" r="1.4"/></svg>',
};
const LETTRES = ['L', 'M', 'M', 'J', 'V', 'S', 'D'];
const nomJour = k => JOURS[KEYS.indexOf(k)];
let selDay = todayKey(), openId = null, shopOpen = false;

function prescText(sl, slug, pr) {
  const reps = repsFor(sl, slug, pr);
  const s = pr.sets > 1 ? `${pr.sets}&nbsp;×&nbsp;${esc(reps)}` : esc(reps);
  return s + (pr.rest ? ` · repos ${restTxt(pr.rest)}` : '');
}
function weekStrip() {
  return `<nav class="week" aria-label="Jours de la semaine">${ORDER.map((k, i) => {
    const d = dateOf(k), sel = k === selDay;
    return `<button type="button" class="wd${sel ? ' sel' : ''}${d === TODAY() ? ' today' : ''}${dayDone(k) ? ' done' : ''}" data-day="${k}" aria-pressed="${sel}" aria-label="${nomJour(k)} ${fmtDate(d)}${dayDone(k) ? ', fait' : ''}"><small>${LETTRES[i]}</small><b>${D(d).getDate()}</b><i>${I.check}</i></button>`;
  }).join('')}</nav>`;
}
function overline(k) { const d = dateOf(k); return d === TODAY() ? 'Aujourd’hui' : `${nomJour(k)} ${fmtDate(d)}`; }

/* ---------------- une ligne de la liste ---------------- */
function rowHtml(k, r) {
  const d = dateOf(k), open = openId === r.id;
  const lead = r.check === false ? `<span class="lead">${r.icon || ''}</span>`
    : `<button type="button" class="ck" data-ck="${r.id}" aria-pressed="${checked(d, r.id)}" aria-label="${esc(r.name)} : fait">${I.check}</button>`;
  const body = `<span class="nm">${esc(r.name)}</span>${r.sub ? `<span class="sb">${r.sub}</span>` : ''}`;
  return `<li class="row${r.check !== false && checked(d, r.id) ? ' on' : ''}${open ? ' open' : ''}">${lead}`
    + (r.detail ? `<button type="button" class="rt" data-open="${r.id}" aria-expanded="${open}">${body}${I.chev}</button>` : `<div class="rt">${body}</div>`)
    + (open && r.detail ? `<div class="det">${r.detail()}</div>` : '') + '</li>';
}
function ytUrl(sl, e) {
  const q = e.name.replace(/\s*\(.*\)/, '') + (['plyo', 'sprint', 'cod', 'ball'].includes(sl.kind) ? ' exercice football' : ' musculation');
  return 'https://www.youtube.com/results?search_query=' + encodeURIComponent(q);
}
function exDetail(k, sl, slug, pr) {
  const e = EXD[slug], d = dateOf(k), opts = slotOptions(sl);
  let h = figHtml(slug);
  if (e.steps && e.steps.length) h += `<ol class="steps">${e.steps.map(s => `<li>${esc(s)}</li>`).join('')}</ol>`;
  if (e.tip) h += `<p class="tip ok">${I.ok}<span>${esc(e.tip)}</span></p>`;
  if (e.err) h += `<p class="tip no">${I.no}<span>${esc(e.err)}</span></p>`;
  if (modeOf(sl, slug, repsFor(sl, slug, pr)) === 'load') {
    const cur = histOn(slug, d), last = lastBefore(slug, d);
    const hint = last != null ? `La dernière fois : ${frn(last)}&nbsp;kg` : e.start ? `Pour commencer : ${esc(e.start)}` : '';
    h += `<div class="wt"><label for="w-${sl.id}">${e.neg ? 'Contrepoids' : 'Poids'}</label><input id="w-${sl.id}" type="text" inputmode="decimal" autocomplete="off" enterkeyhint="done" data-w="${slug}" value="${cur != null ? frn(cur) : ''}" placeholder="–"><span>kg</span>${hint ? `<small>${hint}</small>` : ''}</div>`;
  }
  h += '<div class="links">';
  if (e.eq !== 'velo') h += `<a class="lnk" href="${ytUrl(sl, e)}" target="_blank" rel="noopener">${I.play}<span>Voir en vidéo</span></a>`;
  opts.forEach((o, i) => { if (o !== slug) h += `<button type="button" class="lnk" data-alt="${sl.id}" data-i="${i}">${I.swap}<span>${o === sl.ex ? 'Revenir à' : 'Pris ? Fais plutôt'} : ${esc(EXD[o].name)}</span></button>`; });
  return h + '</div>';
}
function listHtml(k, rows) { return `<ul class="list">${rows.map(r => rowHtml(k, r)).join('')}</ul>`; }
function warmRow(key, extra) {
  return { id: 'w-' + key, check: false, icon: I.warm, name: 'Échauffement', sub: '8 à 10&nbsp;min',
    detail: () => `<ul class="plain">${DATA.warmup[key].concat(extra || []).map(x => `<li>${esc(x)}</li>`).join('')}</ul>` };
}
function slotRows(k, slots, info) {
  return slots.map(sl => ({ sl, slug: slotSlug(sl), pr: presc(sl, info) })).filter(p => p.pr).map(p => ({
    id: p.sl.id, name: EXD[p.slug].name, sub: prescText(p.sl, p.slug, p.pr), detail: () => exDetail(k, p.sl, p.slug, p.pr) }));
}

/* ---------------- SÉANCE ---------------- */
function renderSeance() {
  const k = selDay, day = dayByKey(k), info = weekInfo(), d = dateOf(k);
  let title = day.name, sub = [day.theme, day.dur].filter(Boolean).join(' · '), notes = [], body = '';
  if (day.kind === 'gym' || day.kind === 'speed') {
    if (info.learn && day.kind === 'gym') notes.push('Semaines 1 et 2 : 2 séries seulement, le temps d’apprendre les gestes.');
    if (info.deload) notes.push('Semaine plus légère : une série de moins partout.');
    if (day.note) notes.push(day.note);
    if (day.place) notes.push('Matériel : ' + day.place.charAt(0).toLowerCase() + day.place.slice(1) + '.');
    body = listHtml(k, [warmRow(day.warm)].concat(slotRows(k, day.slots, info)));
    if (day.kind === 'gym') body += '<p class="foot">Toutes tes répétitions passent facilement ? Ajoute un peu de poids la fois suivante. Garde toujours 1 ou 2 répétitions en réserve.</p>';
  } else if (day.kind === 'foot') {
    body = listHtml(k, [{ id: 'f1', name: 'Entraînement avec l’équipe', sub: esc(day.text) }]);
  } else if (day.kind === 'recup') {
    body = listHtml(k, day.items.map(it => it.ex
      ? { id: it.id, name: it.txt, sub: esc(EXD[it.ex].tip || ''), detail: () => exDetail(k, { id: it.id, ex: it.ex, alts: [], kind: 'recup' }, it.ex, { sets: 1, reps: '20 min', rest: 0 }) }
      : { id: it.id, name: it.txt, sub: 'Tiens chaque position sans forcer', detail: () => `<ul class="plain">${it.list.map(x => `<li>${esc(x)}</li>`).join('')}</ul>` }));
  } else if (day.kind === 'sunday') {
    const m = day.match, t = day.tech;
    title = 'Match ou technique'; sub = '';
    body = `<h2 class="sec">Si tu as match</h2>` + listHtml(k, [{ id: 'm1', name: 'Match', sub: 'Avant, échauffement, après',
      detail: () => `<h4>Avant</h4><ul class="plain">${m.before.map(x => `<li>${esc(x)}</li>`).join('')}</ul><h4>Échauffement</h4><ul class="plain">${DATA.warmup.match.map(x => `<li>${esc(x)}</li>`).join('')}</ul><h4>Après</h4><ul class="plain">${m.after.map(x => `<li>${esc(x)}</li>`).join('')}</ul>` }])
      + `<h2 class="sec">Sinon : technique <small>${esc(t.dur)}</small></h2>`
      + (t.place ? `<p class="note">Matériel : ${esc(t.place.charAt(0).toLowerCase() + t.place.slice(1))}.</p>` : '')
      + listHtml(k, [warmRow(t.warm)].concat(slotRows(k, t.slots, info)));
  }
  const done = dayDone(k);
  view.innerHTML = `${weekStrip()}
    <header class="head"><p class="over">${overline(k)}</p><h1>${esc(title)}</h1>${sub ? `<p class="sub">${sub}</p>` : ''}</header>
    ${done ? `<p class="fin">${I.check}<span>${day.kind === 'foot' ? 'Entraînement fait.' : day.kind === 'recup' ? 'Récup faite.' : k === 'dimanche' && checked(d, 'm1') ? 'Match joué.' : 'Séance terminée.'} Bien joué&nbsp;!</span></p>` : ''}
    ${notes.map(n => `<p class="note">${esc(n)}</p>`).join('')}
    ${body}`;
  playFig();
}

/* ---------------- REPAS ---------------- */
function qtyLabel(f, q) {
  const x = F(f);
  const n = s => esc(s.replace(' (poids cru)', ''));
  if (x.per === 'g') return `<b>${q}&nbsp;g</b> ${n(x.n)}`;
  if (x.unit) return `<b>${q} ${esc(x.unit)}${q > 1 && !/\./.test(x.unit) ? 's' : ''}</b> ${n(x.n)}`;
  return `<b>${q}</b> ${n(q > 1 && x.pl ? x.pl : x.n)}`;
}
function renderRepas() {
  const dn = nomJour(selDay), r = mealsFor(dn);
  view.innerHTML = `${weekStrip()}
    <header class="head"><p class="over">${overline(selDay)}</p><h1>Repas</h1><p class="sub">Environ ${fr0(r.md.target)}&nbsp;kcal</p></header>
    ${r.meals.map(m => `<section class="meal"><h2>${esc(m.name)}</h2>${m.title ? `<p class="dish">${esc(m.title)}</p>` : ''}<ul>${Object.keys(m.items).map(f => `<li>${qtyLabel(f, m.items[f])}</li>`).join('')}</ul></section>`).join('')}
    ${dn === 'Samedi' || dn === 'Dimanche' ? '<p class="note">Match le lendemain : ajoute 40&nbsp;g de pâtes au dîner. Jour de match : repas 3&nbsp;h avant.</p>' : ''}
    <p class="note">Poulet, pâtes et riz pesés crus. Une seule whey par jour.</p>
    <ul class="list mt">${`<li class="row${shopOpen ? ' open' : ''}"><span class="lead">${I.cart}</span><button type="button" class="rt" data-shopopen="1" aria-expanded="${shopOpen}"><span class="nm">Liste de courses</span><span class="sb">Pour toute la semaine</span>${I.chev}</button>${shopOpen ? `<div class="det">${coursesHtml()}</div>` : ''}</li>`}</ul>`;
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
    const rows = list.filter(f => tot[f]).map(f => { const on = !!S.shop.checked[f]; return `<li class="shop${on ? ' on' : ''}"><button type="button" class="ck sm" data-shop="${f}" aria-pressed="${on}" aria-label="${esc(F(f).n)}">${I.check}</button><span class="nm">${esc((tot[f] > 1 && F(f).pl ? F(f).pl : F(f).n).replace(/ \(.*\)$/, ''))}</span><span class="q">${buyText(f, tot[f])}</span></li>`; }).join('');
    return rows ? `<h4>${g}</h4><ul class="shopl">${rows}</ul>` : '';
  }).join('') + (Object.keys(S.shop.checked).length ? '<button type="button" class="lnk" data-shopreset="1"><span>Tout décocher</span></button>' : '');
}
