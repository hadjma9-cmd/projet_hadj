# Numéro 10 · prépa foot

App web (iPhone) sur le thème du terrain. En haut, les jours de la semaine. Pour chaque jour, la séance se présente comme une feuille de match : les exercices numérotés, à cocher. « Commencer » ouvre une fiche par exercice : le dessin animé à la craie sur le terrain, séries, répétitions et repos, comment le faire, un conseil, ce qu'il faut éviter. On glisse pour passer à l'exercice suivant, et « C'est fait » coche puis avance. Il y a aussi les repas, la liste de courses et un coach IA.

- `public/` : le site publié par Netlify (`index.html`, police Archivo dans `fonts/`, icônes, mode hors ligne `sw.js`).
- `netlify/edge-functions/coach.js` : relaie les questions du coach vers l'API Claude.
- `tools/` : génère `public/index.html`. Après une modification : `python3 tools/build.py`.
  - `program.py` : exercices (exécution, conseil, à éviter), semaine type, progression sur 12 semaines.
  - `plan.py` + `foods.py` : repas par type de journée, calories et protéines.
  - `exercises.py`, `ex2.py`, `ex3.py`, `figs.py` : les deux poses de chaque exercice (départ, arrivée).
  - `art.py` : transforme les deux poses en squelette animé (les membres tournent autour des articulations).
  - `drills.py` : schémas terrain vus de dessus.
  - `app/` : l'interface (`style.css`, `shell.html`, `core.js`, `fig.js`, `ui.js`, `coach.js`, `main.js`).

Les données restent sur le téléphone (clé `n10-v3`) : cases cochées, poids notés, remplacements d'exercices. Les données des anciennes versions sont reprises automatiquement.

## Activer le coach sur Netlify

Dans Netlify → Project configuration → Environment variables, ajouter :

| Variable | Valeur |
| --- | --- |
| `ANTHROPIC_API_KEY` | ta clé API Claude (console Claude) |
| `COACH_CODE` | un code de ton choix, à saisir dans l'app (onglet Coach) |
| `COACH_MODEL` | facultatif, `claude-haiku-5-5` par défaut |

Puis Deploys → Trigger deploy.

Police : Archivo (SIL Open Font License), servie depuis `public/fonts/`.
