/* ---------------- coach IA ---------------- */
const QUICK = ['Je suis fatigué aujourd’hui, j’adapte comment ?', 'Un exercice pour mon pied faible', 'Comment gagner en vitesse sur 10 m ?', 'Que manger avant mon match ?',
  'J’ai des courbatures aux ischios', 'La machine est prise, je fais quoi ?', 'Analyse mes dernières séances'];
let coachBusy = false, coachMode = null, sampler = null, coachAbort = null;
async function detectCoach() {
  if (coachMode) return coachMode;
  try {
    if (window.claude && typeof window.claude.use === 'function') {
      sampler = await window.claude.use('sample');
      if (sampler) return (coachMode = 'sample');
    }
  } catch (e) {}
  return (coachMode = location.protocol.startsWith('http') && !/claude\.ai$|claudeusercontent/.test(location.hostname) ? 'api' : 'none');
}
function coachSystem() {
  const info = weekInfo(), dk = todayKey(), day = dayByKey(dk), v = dayView(day), L = [];
  L.push('Tu es le coach intégré à l’app « Numéro 10 », la préparation physique d’un milieu offensif de foot à 7. Tu réponds en français, tu tutoies, tu es motivant, direct et concret.');
  L.push('Profil : homme, 26 ans, 1,76 m, environ 82 kg, débutant en musculation, milieu offensif. Objectif : dominer au milieu, puissant dans les duels, explosif, rapide, endurant, agile et très technique, sans prendre de poids inutile. Il fait des pompes au sol, pas encore de tractions, les dips moyennement. Il n’aime pas la poulie : n’en propose jamais. Il n’a pas compris les fentes arrière (remplacées par des montées sur banc). Halal, pas de viande rouge, il a du mal avec les légumineuses, une seule dose de whey par jour.');
  L.push(`Aujourd’hui : ${JOURS[new Date().getDay()]} ${TODAY()}. ${info.before ? 'Le cycle commence le ' + S.start : info.after ? 'Cycle de 12 semaines terminé' : `Semaine ${info.w}/12, bloc ${DATA.blocks[info.block].name}${info.learn ? ' (apprentissage : 2 séries)' : ''}${info.deload ? ' (semaine allégée)' : ''}${info.test ? ' (tests le vendredi)' : ''}`}. Match ce dimanche : ${isMatchWeek() ? 'oui' : 'non'}.`);
  L.push('Semaine type : lundi haut du corps A (force et duels), mardi bas du corps (force, puissance, Nordic), mercredi entraînement collectif, jeudi récupération (vélo, mobilité, Copenhague, équilibre), vendredi vitesse et appuis (pogo, sauts, départs 10 m, sprints 20 m, freinages, changements de direction, conduite rapide), samedi haut du corps B (puissance et gainage), dimanche match ou technique (slalom, contrôle orienté, pied faible, jonglages, intervalles 15/15). Semaine de match : vendredi −30 % de volume, samedi 2 séries max à 7/10.');
  L.push('Séance du jour (' + v.name + ') : ' + (['gym', 'speed', 'tech'].includes(v.kind) ? planFor(day).map(p => `${EXD[p.slug].name} ${p.pr.sets}×${repsFor(p.sl, p.slug, p.pr)} (${p.pr.eff})`).join(' ; ') : v.kind === 'foot' ? 'entraînement avec l’équipe' : v.kind === 'recup' ? 'récupération active' : 'match') + '.');
  const r = S.ready[TODAY()]; if (r) L.push(`Check forme du jour : ${r.score}/6 (${r.score >= 5 ? 'vert' : r.score >= 3 ? 'orange' : 'rouge'}).`);
  const logs = S.log.slice(-6).map(l => `${l.d} ${l.name}${l.done != null && l.total > 1 ? ` ${l.done}/${l.total} séries` : ''}${l.rpe ? `, ressenti ${l.rpe}/10` : ''}${l.min ? `, ${l.min} min` : ''}`);
  if (logs.length) L.push('Dernières activités : ' + logs.join(' ; ') + '.');
  const loads = Object.keys(S.hist).map(k => { const h = S.hist[k]; const l = h[h.length - 1]; if (!l) return ''; return `${exName(k)} : ${l.w ? l.w + ' kg' : l.r ? l.r + (/s$/.test(String(l.r)) ? '' : ' reps') : 'fait'} le ${l.d}${l.fb ? ' (' + ({ facile: 'trop facile', ok: 'parfait', dur: 'trop dur' }[l.fb]) + ')' : ''}`; }).filter(Boolean);
  if (loads.length) L.push('Dernières charges : ' + loads.slice(-18).join(' ; ') + '.');
  if (S.tests.length) L.push('Tests : ' + S.tests.slice(-3).map(t => `${t.d} ` + DATA.testDef.filter(x => t[x.k] != null).map(x => `${x.name} ${t[x.k]}${x.unit}`).join(', ')).join(' | ') + '.');
  if (S.matches.length) L.push(`Matchs : ${S.matches.length} joués, ${sumM('goals')} buts, ${sumM('assists')} passes décisives.`);
  const w = weeklyAvg(); if (w.length) L.push('Poids moyen : ' + w.slice(-4).map(x => `${fr1(x.avg)} kg (semaine du ${x.k})`).join(', ') + '.');
  L.push('Alimentation : environ 2 050 à 2 550 kcal selon la journée (plus les jours de foot et de match), environ 160 g de protéines par jour, poisson 2 fois par semaine dont un gras (ANSES), thon limité à 100 g une semaine sur deux.');
  L.push(`Niveau ${levelOf().n} (${levelOf().t}), ${fr0(xpTotal())} XP, série de ${streak()} semaine(s).`);
  L.push('Règles : réponses courtes (moins de 150 mots sauf si on te demande une séance complète), pratiques, avec séries × répétitions et 2 ou 3 consignes. Exercices faisables avec machines guidées sans poulie, haltères, barre guidée, médecine-ball, box, poids du corps, ou sur un terrain avec plots et ballon. Adapte à la fatigue : forme basse = moins de séries, pas d’échec, sprints sous-maximaux ; rappelle que la séance du mercredi et le match passent avant la muscu. Douleur : arrêter l’exercice, ne pas forcer, consulter un médecin ou un kiné si la douleur est vive, articulaire ou dure plusieurs jours ; jamais de diagnostic. Pas de régime extrême ; complément en dehors de la whey seulement si on te le demande (créatine monohydrate possible, en précisant la petite prise d’eau). Hors sujet sport, nutrition, sommeil : une phrase, puis reviens au sujet. Mise en forme : phrases simples, listes avec « - », gras avec ** sur les mots clés, pas de titres.');
  return L.join('\n');
}
function md(t) {
  const lines = esc(t).replace(/\*\*(.+?)\*\*/g, '<b>$1</b>').split(/\n/);
  let html = '', list = null;
  const close = () => { if (list) { html += `</${list}>`; list = null; } };
  lines.forEach(l => {
    const ul = l.match(/^\s*[-•*]\s+(.*)/), ol = l.match(/^\s*\d+[.)]\s+(.*)/);
    if (ul || ol) { const t2 = ul ? 'ul' : 'ol'; if (list !== t2) { close(); html += `<${t2}>`; list = t2; } html += `<li>${(ul || ol)[1]}</li>`; }
    else if (!l.trim()) close();
    else { close(); html += `<p>${l.replace(/^#+\s*/, '')}</p>`; }
  });
  close(); return html;
}
function coachSetupHtml() {
  return `<div class="banner"><b>Coach à activer sur ce site.</b> Ici, le coach passe par ta clé Claude enregistrée dans Netlify ; entre ensuite ton code dans <b>Réglages</b> (roue crantée de l’accueil).<br><br>Gratuit avec ton abonnement : <a href="${DATA.artifact}#coach">ouvrir le coach dans Claude</a>.</div>`;
}
function renderCoach() {
  const msgs = S.coach.msgs, empty = !msgs.length;
  view.className = '';
  view.innerHTML = `<div class="page-h"><h1>Coach</h1><span class="sub">Il connaît ton programme</span></div>
    <div id="coachnote"></div>
    <div class="quick">${QUICK.map(q => `<button type="button" data-q="${esc(q)}">${esc(q)}</button>`).join('')}</div>
    <div class="chat" id="chat">${empty ? `<div class="msg bot"><p>Salut ! Je connais ton programme, tes charges, tes tests et ta forme du jour. Demande-moi d’adapter une séance, un exercice pour ton pied faible ou ta vitesse, ou quoi manger avant un match.</p></div>` : msgs.map(m => m.role === 'user' ? `<div class="msg user">${esc(m.content)}</div>` : `<div class="msg bot">${md(m.content)}</div>`).join('')}</div>
    ${empty ? '' : '<button type="button" class="danger mt12" id="newchat">Nouvelle conversation</button>'}
    <div class="coach-pad"></div>
    <div class="composer"><form id="composer"><textarea id="ask" rows="1" placeholder="Écris ta question…" aria-label="Ta question"></textarea><button type="submit" aria-label="Envoyer">${I.send}</button></form></div>`;
  detectCoach().then(mode => {
    const note = document.getElementById('coachnote'); if (!note) return;
    if (mode === 'api' && !S.coach.code) note.innerHTML = coachSetupHtml();
    if (mode === 'none') note.innerHTML = '<div class="banner">Le coach a besoin d’une connexion à Internet.</div>';
  });
  if (!empty) setTimeout(() => window.scrollTo(0, document.body.scrollHeight), 0);
}
async function askCoach(text) {
  if (coachBusy || !text.trim()) return;
  const mode = await detectCoach();
  coachBusy = true;
  S.coach.msgs.push({ role: 'user', content: text.trim().slice(0, 2000) });
  if (S.coach.msgs.length > 40) S.coach.msgs.splice(0, S.coach.msgs.length - 40);
  save(); renderCoach();
  const chat = document.getElementById('chat');
  const bubble = document.createElement('div'); bubble.className = 'msg bot'; bubble.innerHTML = '<span class="typing"><i></i><i></i><i></i></span>';
  chat.appendChild(bubble); window.scrollTo(0, document.body.scrollHeight);
  const history = S.coach.msgs.slice(-16).filter((m, i) => i > 0 || m.role === 'user');
  let answer = '';
  const onText = t => { answer = t; bubble.innerHTML = md(t); };
  try {
    if (mode === 'sample') {
      const sys = coachSystem();
      const input = history.map((m, i) => i === 0 ? { role: 'user', content: sys + '\n\n---\nQuestion : ' + m.content } : m);
      const res = await sampler(input, { onText: ({ text }) => onText(text), cache: false, modelTier: 'default' });
      answer = (res && res.text) || answer;
    } else if (mode === 'api') {
      if (!S.coach.code) throw { code: 'no_code' };
      coachAbort = new AbortController();
      const res = await fetch('/api/coach', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ code: S.coach.code, system: coachSystem(), messages: history }), signal: coachAbort.signal });
      if (!res.ok) { let j = {}; try { j = await res.json(); } catch (e) {} throw { code: j.error || 'http_' + res.status, detail: j.detail }; }
      const reader = res.body.getReader(), dec = new TextDecoder(); let buf = '';
      for (;;) {
        const { done, value } = await reader.read(); if (done) break;
        buf += dec.decode(value, { stream: true });
        let i;
        while ((i = buf.indexOf('\n\n')) >= 0) {
          const chunk = buf.slice(0, i); buf = buf.slice(i + 2);
          chunk.split('\n').forEach(line => {
            if (!line.startsWith('data:')) return;
            let ev; try { ev = JSON.parse(line.slice(5).trim()); } catch (e) { return; }
            if (ev.type === 'content_block_delta' && ev.delta && ev.delta.type === 'text_delta') onText(answer + ev.delta.text);
            else if (ev.type === 'error') throw { code: 'upstream', detail: ev.error && ev.error.message };
          });
        }
      }
    } else throw { code: 'offline' };
    if (!answer.trim()) throw { code: 'empty' };
    S.coach.msgs.push({ role: 'assistant', content: answer });
  } catch (e) {
    const c = (e && e.code) || 'error';
    const msg = c === 'no_code' || c === 'bad_code' ? 'Code du coach manquant ou incorrect : vérifie-le dans les réglages (roue crantée de l’accueil).'
      : c === 'not_configured' ? 'Le coach n’est pas encore activé sur ce site : il faut ajouter la clé dans Netlify (voir le message en haut).'
      : c === 'bad_key' ? 'La clé Claude enregistrée dans Netlify n’est pas valide : vérifie la variable ANTHROPIC_API_KEY.'
      : c === 'rate_limited' ? 'Trop de questions d’un coup : réessaie dans une minute.'
      : c === 'not_granted' ? 'Tu as refusé l’accès à Claude pour cette page : le coach ne peut pas répondre ici.'
      : c === 'offline' ? 'Pas de connexion : le coach a besoin d’Internet.'
      : 'Le coach n’a pas pu répondre' + (e && e.detail ? ' (' + String(e.detail).slice(0, 120) + ')' : '') + '. Réessaie dans un instant.';
    bubble.className = 'msg bot err'; bubble.textContent = msg;
    if (answer.trim()) S.coach.msgs.push({ role: 'assistant', content: answer }); else S.coach.msgs.pop();
    if (c === 'not_configured' || c === 'no_code') { const n = document.getElementById('coachnote'); if (n) n.innerHTML = coachSetupHtml(); }
  } finally {
    coachBusy = false; coachAbort = null; save();
    if (tab === 'coach' && document.getElementById('chat') && !bubble.classList.contains('err')) renderCoach();
  }
}
