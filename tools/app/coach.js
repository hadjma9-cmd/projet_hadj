/* ---------------- coach IA ---------------- */
const QUICK = ['Cette machine n’est pas dans ma salle, je fais quoi ?', 'J’ai mal quelque part, je fais quoi ?', 'Que manger avant mon match ?'];
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
  const info = weekInfo(), day = dayByKey(todayKey()), v = dayView(day), L = [];
  L.push('Tu es le coach intégré à l’app de musculation et de préparation foot de ce joueur. Tu réponds en français, tu tutoies, simplement et brièvement.');
  L.push('Profil : homme, 26 ans, 1,76 m, environ 82 kg, débutant en salle, milieu offensif de foot à 7. Il veut des choses simples. Il n’aime pas la poulie : n’en propose jamais. Halal, pas de viande rouge, pas de légumineuses, une seule whey par jour.');
  L.push('Semaine : lundi haut du corps A, mardi bas du corps, mercredi foot avec l’équipe, jeudi récupération, vendredi vitesse, samedi haut du corps B, dimanche match ou technique.');
  L.push(`Aujourd’hui : ${JOURS[new Date().getDay()]}, ${v.name}${info.before ? '' : `, semaine ${info.w} sur 12`}. ` + ((v.slots || []).length ? 'Exercices : ' + planFor(day).map(p => `${EXD[p.slug].name} ${p.pr.sets} × ${repsFor(p.sl, p.slug, p.pr)}`).join(' ; ') + '.' : ''));
  const loads = Object.keys(S.hist).map(k => { const h = S.hist[k], l = h[h.length - 1]; return l && l.w ? `${exName(k)} ${l.w} kg` : ''; }).filter(Boolean);
  if (loads.length) L.push('Dernières charges : ' + loads.slice(-12).join(' ; ') + '.');
  L.push('Règles : réponses courtes (moins de 120 mots), simples, avec séries × répétitions si tu proposes un exercice. Exercices simples seulement : haltères, machines guidées sans poulie, poids du corps, ou terrain avec plots et ballon. Douleur : arrêter l’exercice, consulter si elle est vive ou dure plusieurs jours, jamais de diagnostic. Mise en forme : phrases simples, listes avec « - », gras avec ** sur les mots clés.');
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
  return `<div class="banner"><p>Pour utiliser le coach sur ce site, entre ton code :</p>
    <form id="codeform" class="codef"><input type="password" id="ccode" autocomplete="off" placeholder="Ton code" aria-label="Code du coach"><button type="submit">OK</button></form>
    <p>Ou gratuitement avec ton abonnement Claude : <a href="${DATA.artifact}#coach" target="_blank" rel="noopener">ouvrir le coach dans Claude</a>.</p></div>`;
}
function renderCoach() {
  const msgs = S.coach.msgs, empty = !msgs.length;
  view.className = '';
  view.innerHTML = `<header class="head"><p class="over">Une question ? Demande.</p><h1>Coach</h1></header>
    <div id="coachnote"></div>
    ${empty ? `<ul class="list quick">${QUICK.map(q => `<li class="row"><button type="button" class="rt" data-q="${esc(q)}"><span class="nm">${esc(q)}</span>${I.chev}</button></li>`).join('')}</ul>` : ''}
    <div class="chat" id="chat">${msgs.map(m => m.role === 'user' ? `<div class="msg user">${esc(m.content)}</div>` : `<div class="msg bot">${md(m.content)}</div>`).join('')}</div>
    ${empty ? '' : '<button type="button" class="lnk center" id="newchat"><span>Nouvelle conversation</span></button>'}
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
    const msg = c === 'no_code' || c === 'bad_code' ? 'Code du coach manquant ou incorrect : entre-le en haut de cette page.'
      : c === 'not_configured' ? 'Le coach n’est pas encore activé sur ce site. Utilise le lien vers Claude en haut de la page.'
      : c === 'bad_key' ? 'La clé Claude enregistrée dans Netlify n’est pas valide : vérifie la variable ANTHROPIC_API_KEY.'
      : c === 'rate_limited' ? 'Trop de questions d’un coup : réessaie dans une minute.'
      : c === 'not_granted' ? 'Tu as refusé l’accès à Claude pour cette page : le coach ne peut pas répondre ici.'
      : c === 'offline' ? 'Pas de connexion : le coach a besoin d’Internet.'
      : 'Le coach n’a pas pu répondre' + (e && e.detail ? ' (' + String(e.detail).slice(0, 120) + ')' : '') + '. Réessaie dans un instant.';
    bubble.className = 'msg bot err'; bubble.textContent = msg;
    if (answer.trim()) S.coach.msgs.push({ role: 'assistant', content: answer }); else S.coach.msgs.pop();
    if (c === 'not_configured' || c === 'no_code' || c === 'bad_code') { const n = document.getElementById('coachnote'); if (n) n.innerHTML = coachSetupHtml(); }
  } finally {
    coachBusy = false; coachAbort = null; save();
    if (tab === 'coach' && document.getElementById('chat') && !bubble.classList.contains('err')) renderCoach();
  }
}
