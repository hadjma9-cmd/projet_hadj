# Mon programme muscu

App web (iPhone) : séances avec alternatives et dessins, muscles travaillés, suivi des charges et du poids, repas, courses et coach IA.

- `public/` : le site publié par Netlify (`index.html`, icônes, mode hors ligne `sw.js`).
- `netlify/edge-functions/coach.js` : relaie les questions du coach vers l'API Claude.
- `tools/` : programmes Python qui génèrent `public/index.html` (dessins, exercices, repas). Après une modification : `python3 tools/build.py`.

## Activer le coach sur Netlify

Dans Netlify → Project configuration → Environment variables, ajouter :

| Variable | Valeur |
| --- | --- |
| `ANTHROPIC_API_KEY` | ta clé API Claude (console Claude) |
| `COACH_CODE` | un code de ton choix, à saisir dans l'app (Suivi → Réglages) |
| `COACH_MODEL` | facultatif, `claude-haiku-5-5` par défaut |

Puis Deploys → Trigger deploy.
