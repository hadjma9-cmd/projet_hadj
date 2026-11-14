import sys, io, json, re, contextlib, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
with contextlib.redirect_stdout(io.StringIO()):
    import figs, ex2
    from exercises import EX as DRAW
    from musclemap import regions
from catalog import MUSCLES, EX, INC, DAYS, ABS, WARMUP
from foods import FOODS
import plan as P

def poses(slug):
    sc = DRAW[slug]()
    out, caps, cur = [], [], None
    for it in sc.items:
        k = it[0]
        if k == 'g+': cur = []; continue
        if k == 'g-': out.append(cur); cur = None; continue
        if cur is None: continue
        if k == 't':
            if it[1] in ('pose-1', 'pose-2'): caps.append(re.sub(r'^\d · ', '', it[4]))
            continue
        cur.append(it)
    svgs = []
    for i, items in enumerate(out):
        ox = 24 if i == 0 else 392
        mid = f'm-{slug}-{i}'
        o = [f"<svg viewBox='{ox} 50 344 214' aria-hidden='true'><defs><marker id='{mid}' viewBox='0 0 10 10' refX='7' refY='5' markerWidth='5' markerHeight='5' orient='auto-start-reverse'><path d='M0 0L10 5L0 10z' class='f-a'/></marker></defs>"]
        for it in items:
            k = it[0]
            if k == 'pl':
                pts = ' '.join(f'{x},{y}' for x, y in it[1]); dash = f" stroke-dasharray='{it[4]}'" if it[4] else ''
                o.append(f"<polyline points='{pts}' class='s-{it[2]}' stroke-width='{it[3]}'{dash}/>")
            elif k == 'near':
                pts = ' '.join(f'{x},{y}' for x, y in it[1])
                o.append(f"<polyline points='{pts}' class='s-halo' stroke-width='{figs.LW + 5}'/><polyline points='{pts}' class='s-k' stroke-width='{figs.LW}'/>")
            elif k == 'c':
                o.append(f"<circle cx='{it[1]}' cy='{it[2]}' r='{it[3]}' class='f-{it[4]}'/>")
            elif k == 'ring':
                fc = 'f-none' if it[6] == 'none' else ('f-halo' if it[4] == 'a' else 'f-eq')
                o.append(f"<circle cx='{it[1]}' cy='{it[2]}' r='{it[3]}' class='{fc} s-{it[4]}' stroke-width='{it[5]}'/>")
            elif k == 'b':
                if it[5] == 't' and it[6] == 't' and it[3] > 300: continue
                o.append(f"<rect x='{it[1]}' y='{it[2]}' width='{it[3]}' height='{it[4]}' rx='{it[7]}' class='f-eq s-g' stroke-width='2'/>")
            elif k == 'arr':
                o.append(f"<path d='{it[1]}' class='s-a' stroke-width='4' marker-end='url(#{mid})'/>")
        o.append('</svg>')
        svgs.append(''.join(o))
    return svgs, caps

ex = {}
for slug, e in EX.items():
    d = dict(e)
    s, caps = poses(d.pop('drawing', slug))
    d.update(a=s[0], b=s[1], ca=caps[0], cb=caps[1])
    ex[slug] = d
for day in DAYS:
    for sl in day['slots']:
        for s in [sl['main']] + sl['alts']: assert s in ex, s
for sl in ABS:
    for s in [sl['main']] + sl['alts']: assert s in ex, s

TITLES = {('Mardi', 'Dîner', 'A'): 'Poisson meunière, œufs durs et wedges', ('Mardi', 'Dîner', 'B'): 'Salade de riz au thon',
          ('Jeudi', 'Dîner', ''): 'Chakchouka express : œufs cuits dans la sauce tomate', ('Vendredi', 'Dîner', ''): 'Pâtes aux sardines, sauce tomate',
          ('Mardi', 'Petit-déjeuner', ''): 'Bol skyr, avoine, banane', ('Jeudi', 'Petit-déjeuner', ''): 'Bol skyr, avoine, fruit',
          ('Samedi', 'Petit-déjeuner', ''): 'Bol skyr, avoine, banane'}
TAG = {'Lundi': 'Haut 1', 'Mardi': 'Haut 2', 'Mercredi': 'Foot', 'Jeudi': 'Repos', 'Vendredi': 'Bas', 'Samedi': 'Haut 3', 'Dimanche': 'Repos'}
LABEL = {'Avant le foot': '1 h 30 avant le foot'}
meals = []
for day, ms in P.PLAN.items():
    lst = []
    for name, items in ms:
        nm = LABEL.get(name, name)
        if name == 'Collation' and TAG[day] not in ('Repos', 'Foot'): nm = 'Collation · après la séance'
        if items == 'FISH':
            lst.append(dict(name=nm, fish=True, A=dict(title=TITLES[(day, name, 'A')], items=P.FISH_A), B=dict(title=TITLES[(day, name, 'B')], items=P.FISH_B)))
        else:
            lst.append(dict(name=nm, title=TITLES.get((day, name, ''), ''), items=items))
    meals.append(dict(day=day, tag=TAG[day], meals=lst))

DATA = dict(muscles=MUSCLES, regions=regions(), inc=INC, ex=ex, days=DAYS, abs=ABS, warmup=WARMUP, foods=FOODS, meals=meals,
            artifact='https://claude.ai/artifact/FFj7RQyJijK2JHKivdXzSZ')
tpl = open(os.path.join(HERE, 'app.tpl.html')).read()
html = tpl.replace('/*DATA*/null', json.dumps(DATA, ensure_ascii=False, separators=(',', ':')))
out = os.path.join(HERE, '..', 'public', 'index.html')
open(out, 'w').write(html)
print('ok', len(html), 'exercises', len(ex))
