/* ---------------- onglets ---------------- */
const TABS = ['seance', 'repas', 'coach'];
const OLD_TABS = { accueil: 'seance', programme: 'seance' };
let tab = (h => TABS.includes(h) ? h : OLD_TABS[h] || 'seance')(location.hash.slice(1));
function render() {
  document.querySelectorAll('.nav [data-tab]').forEach(b => b.setAttribute('aria-current', b.dataset.tab === tab ? 'page' : 'false'));
  ({ seance: renderSeance, repas: renderRepas, coach: renderCoach }[tab] || renderSeance)();
}
function go(t) { tab = t; openId = null; try { history.replaceState(null, '', '#' + t); } catch (e) {} render(); window.scrollTo(0, 0); }
function rerender() { const y = window.scrollY; render(); window.scrollTo(0, y); }
window.addEventListener('hashchange', () => { const h = location.hash.slice(1); if (TABS.includes(h) && h !== tab) { tab = h; render(); } });
function applyTheme() {
  const dark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  const m = document.querySelector('meta[name=theme-color]'); if (m) m.setAttribute('content', dark ? '#000000' : '#F2F2F7');
}
try { window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', applyTheme); } catch (e) {}

/* ---------------- actions ---------------- */
document.querySelector('.nav').addEventListener('click', e => { const b = e.target.closest('[data-tab]'); if (b) go(b.dataset.tab); });
view.addEventListener('click', e => {
  const t = e.target.closest('button'); if (!t) return;
  const d = t.dataset;
  if (d.day) { if (d.day !== selDay) { selDay = d.day; openId = null; shopOpen = false; render(); } return; }
  if (d.ck) {
    const fin = toggleCheck(selDay, d.ck);
    if (fin && navigator.vibrate) { try { navigator.vibrate(30); } catch (err) {} }
    rerender(); return;
  }
  if (d.open) { openId = openId === d.open ? null : d.open; rerender(); return; }
  if (d.alt) { S.variant[d.alt] = +d.i; save(); rerender(); return; }
  if (d.shopopen) { shopOpen = !shopOpen; rerender(); return; }
  if (d.shop) { S.shop.checked[d.shop] = !S.shop.checked[d.shop]; save(); rerender(); return; }
  if (d.shopreset) { S.shop.checked = {}; save(); rerender(); return; }
  if (d.q) { askCoach(d.q); return; }
  if (t.id === 'newchat') { if (coachAbort) coachAbort.abort(); S.coach.msgs = []; save(); render(); return; }
});
view.addEventListener('change', e => {
  const el = e.target;
  if (el.dataset.w) { const w = num(el.value); setW(el.dataset.w, dateOf(selDay), w != null && w >= 0 ? w : null); }
});
view.addEventListener('submit', e => {
  e.preventDefault();
  if (e.target.id === 'composer') { const ta = document.getElementById('ask'); const v = ta.value; ta.value = ''; ta.style.height = ''; askCoach(v); }
  if (e.target.id === 'codeform') { const v = document.getElementById('ccode').value.trim(); if (v) { S.coach.code = v; save(); render(); } }
});
view.addEventListener('input', e => { if (e.target.id === 'ask') { e.target.style.height = 'auto'; e.target.style.height = Math.min(140, e.target.scrollHeight) + 'px'; } });
view.addEventListener('keydown', e => {
  if (e.target.id === 'ask' && e.key === 'Enter' && !e.shiftKey && window.matchMedia('(pointer: fine)').matches) { e.preventDefault(); document.getElementById('composer').requestSubmit(); }
  if (e.target.dataset && e.target.dataset.w && e.key === 'Enter') e.target.blur();
});
let lastToday = TODAY();
document.addEventListener('visibilitychange', () => {
  if (document.hidden) return;
  if (TODAY() !== lastToday) { lastToday = TODAY(); selDay = todayKey(); openId = null; }
  if (tab !== 'coach') rerender();
});

/* ---------------- démarrage ---------------- */
loadState(); applyTheme(); save();
render();
try { if ('serviceWorker' in navigator && location.protocol === 'https:' && !/claude/.test(location.hostname)) navigator.serviceWorker.register('sw.js').catch(() => {}); } catch (e) {}
