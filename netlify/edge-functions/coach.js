// Coach IA : relaie les questions de l'app vers l'API Claude (Anthropic) avec la clé gardée dans Netlify.
// Variables d'environnement Netlify : ANTHROPIC_API_KEY (obligatoire), COACH_CODE (obligatoire), COACH_MODEL (facultatif).
const json = (o, status = 200) => new Response(JSON.stringify(o), { status, headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' } });

export default async (request) => {
  if (request.method !== 'POST') return json({ error: 'method' }, 405);
  const env = (k) => (globalThis.Netlify && Netlify.env.get(k)) || '';
  const key = env('ANTHROPIC_API_KEY'), code = env('COACH_CODE');
  if (!key || !code) return json({ error: 'not_configured' }, 503);
  let body;
  try { body = await request.json(); } catch { return json({ error: 'bad_request' }, 400); }
  if (!body || typeof body.code !== 'string' || body.code.trim() !== code.trim()) return json({ error: 'bad_code' }, 401);

  // Nettoie l'historique : rôles valides, alternance user/assistant, taille bornée.
  const msgs = [];
  for (const m of (Array.isArray(body.messages) ? body.messages : []).slice(-16)) {
    if (!m || (m.role !== 'user' && m.role !== 'assistant') || typeof m.content !== 'string' || !m.content.trim()) continue;
    const content = m.content.slice(0, 4000);
    if (msgs.length && msgs[msgs.length - 1].role === m.role) msgs[msgs.length - 1].content += '\n\n' + content;
    else msgs.push({ role: m.role, content });
  }
  while (msgs.length && msgs[0].role !== 'user') msgs.shift();
  if (!msgs.length || msgs[msgs.length - 1].role !== 'user') return json({ error: 'bad_request' }, 400);
  const system = typeof body.system === 'string' ? body.system.slice(0, 24000) : '';

  let upstream;
  try {
    upstream = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: { 'x-api-key': key, 'anthropic-version': '2023-06-01', 'content-type': 'application/json' },
      body: JSON.stringify({ model: env('COACH_MODEL') || 'claude-haiku-5-5', max_tokens: 1000, system, messages: msgs, stream: true }),
    });
  } catch (e) {
    return json({ error: 'upstream', detail: 'API injoignable' }, 502);
  }
  if (!upstream.ok || !upstream.body) {
    let detail = '';
    try { const j = await upstream.json(); detail = (j && j.error && j.error.message) || ''; } catch { /* ignore */ }
    return json({ error: upstream.status === 401 ? 'bad_key' : upstream.status === 429 ? 'rate_limited' : 'upstream', status: upstream.status, detail: detail.slice(0, 300) }, 502);
  }
  return new Response(upstream.body, { headers: { 'content-type': 'text/event-stream; charset=utf-8', 'cache-control': 'no-store' } });
};

export const config = { path: '/api/coach' };
