/* ---------------- dessins animés des exercices ---------------- */
// Le squelette (art.py) donne pour chaque point soit un trajet en ligne droite, soit un segment
// qui tourne autour de son articulation : les bras et les jambes gardent leur longueur.
const f1 = x => Math.round(x * 10) / 10;
function rigFrame(R, t) {
  const P = [], N = R.n;
  for (let i = 0; i < N.length; i++) {
    const d = N[i];
    if (d[0] === 0) P.push([d[1] + (d[3] - d[1]) * t, d[2] + (d[4] - d[2]) * t]);
    else { const p = P[d[1]], l = d[2] + (d[3] - d[2]) * t, a = d[4] + d[5] * t; P.push([p[0] + l * Math.cos(a), p[1] + l * Math.sin(a)]); }
  }
  if (R.h) { const o = R.h * Math.sin(Math.PI * t); R.m.forEach(i => { P[i] = [P[i][0], P[i][1] - o]; }); }
  return P;
}
const ptsStr = (P, ids) => ids.map(i => f1(P[i][0]) + ',' + f1(P[i][1])).join(' ');
function rigMarkup(R, P) {
  return R.it.map(it => {
    switch (it[0]) {
      case 'p': return `<polyline points="${ptsStr(P, it[4])}" class="${it[1]}" stroke-width="${it[2]}"${it[3] ? ` stroke-dasharray="${it[3]}"` : ''}/>`;
      case 'n': { const s = ptsStr(P, it[1]); return `<polyline points="${s}" class="s-halo" stroke-width="17"/><polyline points="${s}" class="s-k" stroke-width="12"/>`; }
      case 'c': { const p = P[it[3]]; return `<circle cx="${f1(p[0])}" cy="${f1(p[1])}" r="${it[2]}" class="${it[1]}"/>`; }
      case 'r': { const p = P[it[4]]; return `<circle cx="${f1(p[0])}" cy="${f1(p[1])}" r="${it[3]}" class="${it[1]}" stroke-width="${it[2]}"/>`; }
      case 'b': { const p = P[it[4]]; return `<rect x="${f1(p[0])}" y="${f1(p[1])}" width="${it[1]}" height="${it[2]}" rx="${it[3]}" class="f-eq s-g" stroke-width="2"/>`; }
    }
    return '';
  }).join('');
}
function rigApply(svg, R, P) {
  const els = svg.children; let k = 0;
  R.it.forEach(it => {
    switch (it[0]) {
      case 'p': els[k++].setAttribute('points', ptsStr(P, it[4])); break;
      case 'n': { const s = ptsStr(P, it[1]); els[k++].setAttribute('points', s); els[k++].setAttribute('points', s); break; }
      case 'c': case 'r': { const p = P[it[it.length - 1]]; els[k].setAttribute('cx', f1(p[0])); els[k++].setAttribute('cy', f1(p[1])); break; }
      case 'b': { const p = P[it[4]]; els[k].setAttribute('x', f1(p[0])); els[k++].setAttribute('y', f1(p[1])); break; }
    }
  });
}
function figHtml(slug) {
  const e = EXD[slug];
  if (e.dia) return `<div class="fig">${e.dia}</div>`;
  if (e.rig) return `<div class="fig"><svg data-rig="${slug}" viewBox="${e.rig.vb.join(' ')}" aria-hidden="true">${rigMarkup(e.rig, rigFrame(e.rig, 0))}</svg></div>`;
  return `<div class="fig2"><figure>${e.a}<figcaption>${esc(e.ca)}</figcaption></figure><figure>${e.b}<figcaption>${esc(e.cb)}</figcaption></figure></div>`;
}
let figRaf = 0;
function playFig() {
  cancelAnimationFrame(figRaf);
  const svg = document.querySelector('svg[data-rig]'); if (!svg) return;
  const R = EXD[svg.dataset.rig].rig;
  try { if (matchMedia('(prefers-reduced-motion: reduce)').matches) return; } catch (e) {}
  const HOLD = 550, MOVE = 1300, PER = 2 * (HOLD + MOVE), T0 = performance.now();
  const step = now => {
    if (!svg.isConnected) return;
    const x = (now - T0) % PER;
    const t = x < HOLD ? 0 : x < HOLD + MOVE ? (x - HOLD) / MOVE : x < 2 * HOLD + MOVE ? 1 : 1 - (x - 2 * HOLD - MOVE) / MOVE;
    rigApply(svg, R, rigFrame(R, (1 - Math.cos(Math.PI * t)) / 2));
    figRaf = requestAnimationFrame(step);
  };
  figRaf = requestAnimationFrame(step);
}
