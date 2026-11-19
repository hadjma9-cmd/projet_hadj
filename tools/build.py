# -*- coding: utf-8 -*-
"""Build « Numéro 10 » : assemble l'app (public/index.html) à partir du programme, des repas et des dessins."""
import sys, io, json, re, contextlib, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
with contextlib.redirect_stdout(io.StringIO()):
    import art
from catalog import EX as EX2, DAYS as DAYS2, ABS as ABS2
import program as PG
from drills import DIAGRAMS
from foods import FOODS
import plan as P


ex = {}
USED = PG.used()
for slug, e in PG.EX.items():
    if slug not in USED: continue
    d = dict(e)
    draw = d.pop('drawing', slug)
    if slug in DIAGRAMS:
        d['dia'] = DIAGRAMS[slug]()
    else:
        d.update(art.art(slug, draw))
    # « Comment faire » en étapes courtes (sans répéter le conseil)
    how = (d.pop('how', '') or '').replace('Bloc 3 :', 'Semaines 9 à 12 :')
    tip = (d.get('tip') or '').strip()
    d['steps'] = [x for x in re.split(r'(?<=[.!?])\s+', how.strip()) if x and x.strip() != tip]
    for k in ('qual', 'sec', 'inc', 'pair', 'timed'):
        d.pop(k, None)
    ex[slug] = d

days = []
for day in PG.DAYS:
    dd = dict(day)
    def fix(slots):
        out = []
        for sl in slots:
            s2 = dict(sl)
            if s2.get('note') and 'semaine 3' in s2['note']: s2['from'] = 3
            out.append(s2)
        return out
    for k in ('slots', 'pre'):
        if k in dd: dd[k] = fix(dd[k])
    if 'tech' in dd:
        dd['tech'] = dict(dd['tech']); dd['tech']['slots'] = fix(dd['tech']['slots'])
    days.append(dd)
for d in days:
    for sl in d.get('slots', []) + (d.get('tech') or {}).get('slots', []):
        for s in [sl['ex']] + sl['alts']: assert s in ex, s
    for it in d.get('items', []):
        assert not it['ex'] or it['ex'] in ex, it['ex']

meals = []
for day, md in P.PLAN.items():
    def conv(ms):
        out = []
        for name, items, title in ms:
            if items == 'FISH':
                out.append(dict(name=name, fish=True, A=dict(title=P.FISH_TITLES['A'], items=P.FISH_A), B=dict(title=P.FISH_TITLES['B'], items=P.FISH_B)))
            else:
                out.append(dict(name=name, title=title, items=items))
        return out
    m = dict(day=day, tag=md['tag'], target=md['target'], meals=conv(md['meals']))
    if 'alt' in md: m['alt'] = dict(tag=md['alt']['tag'], target=md['alt']['target'], meals=conv(md['alt']['meals']))
    meals.append(m)

_LEVELS = [(0, 'Recrue', '🌱'), (300, 'Espoir', '⚡'), (750, 'Remplaçant', '🔄'), (1350, 'Titulaire', '👕'), (2100, 'Box-to-box', '🔁'), (3000, 'Relayeur', '🎯'),
          (4100, 'Meneur de jeu', '🧠'), (5400, 'Numéro 10', '🔟'), (6900, 'Capitaine', '🎖️'), (8600, 'Patron du milieu', '👑'), (10500, 'Maestro', '🎼'), (12600, 'Légende', '🏆')]
_BADGES = [('first', '🚀', 'Coup d’envoi', 'Ta première activité'), ('week7', '💯', 'Semaine parfaite', '7 activités en une semaine'),
          ('streak3', '🔥', 'Régulier', '3 semaines de suite à 5 activités'), ('streak6', '🌋', 'Increvable', '6 semaines de suite à 5 activités'),
          ('s10', '🔟', '10 séances', '10 activités enregistrées'), ('s25', '🥈', '25 séances', '25 activités'), ('s50', '🥇', '50 séances', '50 activités'),
          ('pr1', '💥', 'Premier record', 'Bats un record personnel'), ('pr10', '🧨', 'Collectionneur', '10 records personnels'),
          ('pullup', '🦍', 'Vraie traction', 'Traction à 0 kg de contrepoids'), ('rocket', '⚡', 'Fusée', '−0,1 s sur le sprint 20 m'),
          ('spring', '🦘', 'Ressort', '+10 cm au saut en longueur'), ('weak', '🦶', 'Pied faible', '5 séances de pied faible'),
          ('juggle', '🤹', 'Jongleur', '50 jongles d’affilée'), ('match1', '⚽', 'Premier match', 'Enregistre un match'),
          ('goals5', '🎯', 'Buteur', '5 buts'), ('assists5', '🤝', 'Passeur', '5 passes décisives'), ('recup', '🧊', 'Pro de la récup', '4 récups validées'),
          ('b1', '🧱', 'Fondations', 'Bloc 1 terminé'), ('b2', '🏋️', 'Force', 'Bloc 2 terminé'), ('b3', '🏆', 'Cycle bouclé', 'Les 12 semaines terminées')]

v2alts = {}
for d in DAYS2:
    for sl in d['slots']: v2alts[sl['main']] = sl['alts']
for sl in ABS2: v2alts[sl['main']] = sl['alts']
oldnames = {k: v['name'] for k, v in EX2.items() if k not in ex}
oldneg = [k for k, v in EX2.items() if k not in ex and 'Contrepoids' in v.get('start', '')]

DATA = dict(version=4, muscles=PG.MUSCLES, ex=ex, days=days, warmup=PG.WARMUP, learn=PG.LEARN, deload=PG.DELOAD, foods=FOODS, meals=meals,
            v2days={d['key']: d['name'] for d in DAYS2}, v2alts=v2alts, oldnames=oldnames, oldneg=oldneg,
            artifact='https://claude.ai/artifact/FFj7RQyJijK2JHKivdXzSZ')

NB = '\u00a0'
def nbsp(o, key=None):
    if isinstance(o, str):
        if key in ('a', 'b', 'dia') or o.startswith('<'): return o
        o = re.sub(r'(\d)\s(%|min\b|m\b|s\b|kg\b|cm\b|h\b|g\b|L\b|×|ml\b)', lambda m: m.group(1) + NB + m.group(2), o)
        o = re.sub(r'×\s(\d)', lambda m: '×' + NB + m.group(1), o)
        return o.replace(' :', NB + ':').replace(' ?', NB + '?').replace(' !', NB + '!')
    if isinstance(o, list): return [nbsp(x) for x in o]
    if isinstance(o, dict): return {k: (v if k in ('regions', 'rig') else nbsp(v, k)) for k, v in o.items()}
    return o
DATA = nbsp(DATA)

A = os.path.join(HERE, 'app')
shell = open(os.path.join(A, 'shell.html')).read()
css = open(os.path.join(A, 'style.css')).read()
js = '\n'.join(open(os.path.join(A, f)).read() for f in ('core.js', 'fig.js', 'ui.js', 'coach.js', 'main.js'))
js = js.replace('/*DATA*/null', json.dumps(DATA, ensure_ascii=False, separators=(',', ':')))
html = shell.replace('/*CSS*/', css).replace('/*JS*/', js)
out = os.path.join(HERE, '..', 'public', 'index.html')
open(out, 'w').write(html)
print('ok', len(html), 'octets ·', len(ex), 'exercices ·', sum(1 for e in ex.values() if 'rig' in e), 'animés ·', sum(1 for e in ex.values() if 'a' in e), 'fixes ·', sum(1 for e in ex.values() if 'dia' in e), 'schémas terrain')
