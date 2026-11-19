# Numéro 10 · prépa foot

App web (iPhone), version simple : la séance du jour, chaque exercice avec son dessin, son exécution, un conseil et ce qu'il faut éviter, un mode séance avec chrono de repos, les repas, la liste de courses et un coach IA.

- `public/` : le site publié par Netlify (`index.html`, polices dans `fonts/`, icônes, mode hors ligne `sw.js`).
- `netlify/edge-functions/coach.js` : relaie les questions du coach vers l'API Claude.
- `tools/` : génère `public/index.html`. Après une modification : `python3 tools/build.py`.
  - `program.py` : exercices (exécution, conseil, à éviter), semaine type, progression sur 12 semaines.
  - `plan.py` + `foods.py` : repas par type de journée, calories et protéines.
  - `ex2.py`, `ex3.py` (dessins des exercices), `drills.py` (schémas terrain vus de dessus), `musclemap.py`.
  - `app/` : l'interface (`style.css`, `shell.html`, `core.js`, `ui.js`, `workout.js`, `coach.js`, `main.js`).

Les données restent sur le téléphone (clé `n10-v3`). Les données de l'ancienne version (`muscu-app-v2`) sont reprises automatiquement au premier lancement.

## Activer le coach sur Netlify

Dans Netlify → Project configuration → Environment variables, ajouter :

| Variable | Valeur |
| --- | --- |
| `ANTHROPIC_API_KEY` | ta clé API Claude (console Claude) |
| `COACH_CODE` | un code de ton choix, à saisir dans l'app (Accueil → roue crantée → Code du coach) |
| `COACH_MODEL` | facultatif, `claude-haiku-5-5` par défaut |

Puis Deploys → Trigger deploy.

Polices : Big Shoulders Display, Barlow et Barlow Condensed (SIL Open Font License), servies depuis `public/fonts/`.
