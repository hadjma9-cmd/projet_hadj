/* ---------------- onglets ---------------- */
const TABS = ['seance', 'repas', 'coach'];
const OLD_TABS = { accueil: 'seance', programme: 'seance' };
let tab = (h => TABS.includes(h) ? h : OLD_TABS[h] || 'seance')(location.hash.slice(1));
function render() {
  document.querySelectorAll('.nav [data-tab]').forEach(b => b.setAttribute('aria-current', b.dataset.tab === tab ? 'page' : 'false'));
  ({ seance: renderSeance, repas: renderRepas, coach: renderCoach }[tab] || renderSeance)();
}
function go(t) { tab = t; try { history.replaceState(null, '', '#' + t); } catch (e) {} render(); window.scrollTo(0, 0); }
function rerender() { const y = window.scrollY; render(); window.scrollTo(0, y); }
window.addEventListener('hashchange', () => { const h = location.hash.slice(1); if (TABS.includes(h) && h !== tab) { tab = h; render(); } });
function applyTheme() {
  const dark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  const m = document.querySelector('meta[name=theme-color]'); if (m) m.setAttribute('content', dark ? '#0F4C31' : '#14603D');
}
try { window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', applyTheme); } catch (e) {}
const buzz = () => { if (navigator.vibrate) { try { navigator.vibrate(25); } catch (e) {} } };

/* ---------------- page ---------------- */
document.querySelector('.nav').addEventListener('click', e => { const b = e.target.closest('[data-tab]'); if (b) go(b.dataset.tab); });
view.addEventListener('click', e => {
  const t = e.target.closest('button'); if (!t) return;
  const d = t.dataset;
  if (d.day) { if (d.day !== selDay) { selDay = d.day; warmOpen = false; shopOpen = false; render(); } return; }
  if (d.ck) { if (toggleCheck(selDay, d.ck)) buzz(); rerender(); return; }
  if (d.start) {   // la première fiche pas encore faite
    const deck = deckFor(selDay, d.start), dd = dateOf(selDay);
    const i = deck.findIndex(c => !checked(dd, c.id));
    openSheet(d.start, Math.max(0, i)); return;
  }
  if (d.deck) { openSheet(d.deck, +d.i); return; }
  if (d.warm) { warmOpen = !warmOpen; rerender(); return; }
  if (d.shopopen) { shopOpen = !shopOpen; rerender(); return; }
  if (d.shop) { S.shop.checked[d.shop] = !S.shop.checked[d.shop]; save(); rerender(); return; }
  if (d.shopreset) { S.shop.checked = {}; save(); rerender(); return; }
  if (d.q) { askCoach(d.q); return; }
  if (t.id === 'newchat') { if (coachAbort) coachAbort.abort(); S.coach.msgs = []; save(); render(); return; }
});
view.addEventListener('submit', e => {
  e.preventDefault();
  if (e.target.id === 'composer') { const ta = document.getElementById('ask'); const v = ta.value; ta.value = ''; ta.style.height = ''; askCoach(v); }
  if (e.target.id === 'codeform') { const v = document.getElementById('ccode').value.trim(); if (v) { S.coach.code = v; save(); render(); } }
});
view.addEventListener('input', e => { if (e.target.id === 'ask') { e.target.style.height = 'auto'; e.target.style.height = Math.min(140, e.target.scrollHeight) + 'px'; } });
view.addEventListener('keydown', e => { if (e.target.id === 'ask' && e.key === 'Enter' && !e.shiftKey && window.matchMedia('(pointer: fine)').matches) { e.preventDefault(); document.getElementById('composer').requestSubmit(); } });

/* ---------------- fiche plein écran ---------------- */
const SHEET = document.getElementById('sheet');
SHEET.addEventListener('click', e => {
  const t = e.target.closest('button'); if (!t || !SH) return;
  const d = t.dataset;
  if (d.close) { closeSheet(); return; }
  if (d.seg) { goCard(+d.seg); return; }
  if (d.alt) {   // machine prise : on garde la même fiche, avec l'autre exercice
    S.variant[d.alt] = +d.j; save();
    const tr = document.getElementById('track'), y = tr.children[SH.i].scrollTop;
    renderSheet(); document.getElementById('track').children[SH.i].scrollTop = y; return;
  }
  if (d.done) {
    const c = SH.deck[SH.i], dd = dateOf(SH.k), was = checked(dd, c.id);
    if (toggleCheck(SH.k, c.id)) buzz();
    syncSheet();
    if (was) return;   // on vient d'annuler : on reste sur la fiche
    const n = SH.deck.length, next = [...Array(n).keys()].map(j => (SH.i + 1 + j) % n).find(j => !checked(dd, SH.deck[j].id));
    if (next == null) setTimeout(closeSheet, 450);   // tout est fait
    else setTimeout(() => goCard(next), 250);
  }
});
SHEET.addEventListener('change', e => { const el = e.target; if (el.dataset.w && SH) { const w = num(el.value); setW(el.dataset.w, dateOf(SH.k), w != null && w >= 0 ? w : null); } });
SHEET.addEventListener('keydown', e => { if (e.target.dataset && e.target.dataset.w && e.key === 'Enter') e.target.blur(); });
document.addEventListener('keydown', e => {
  if (!SH) return;
  if (e.key === 'Escape') closeSheet();
  if (e.target.tagName === 'INPUT') return;
  if (e.key === 'ArrowRight' && SH.i < SH.deck.length - 1) goCard(SH.i + 1);
  if (e.key === 'ArrowLeft' && SH.i > 0) goCard(SH.i - 1);
});
window.addEventListener('resize', () => { if (SH) { const tr = document.getElementById('track'); if (tr) tr.scrollLeft = SH.i * tr.clientWidth; } });

let lastToday = TODAY();
document.addEventListener('visibilitychange', () => {
  if (document.hidden || SH) return;
  if (TODAY() !== lastToday) { lastToday = TODAY(); selDay = todayKey(); }
  if (tab !== 'coach') rerender();
});

/* ---------------- démarrage ---------------- */
loadState(); applyTheme(); save();
render();
try { if ('serviceWorker' in navigator && location.protocol === 'https:' && !/claude/.test(location.hostname)) navigator.serviceWorker.register('sw.js').catch(() => {}); } catch (e) {}
