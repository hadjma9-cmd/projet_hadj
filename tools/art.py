# -*- coding: utf-8 -*-
"""Dessins des exercices pour l'app.

Chaque exercice a deux poses (départ, arrivée). On en fait un petit squelette : chaque segment
(bras, avant-bras, cuisse…) tourne autour de son articulation pendant l'animation, au lieu de glisser
en ligne droite. L'app (ui.js) n'a plus qu'à calculer les positions image par image.
Quelques exercices gardent deux images fixes (ex. planche : bonne position / à éviter).
"""
import io, math, re, contextlib, difflib
with contextlib.redirect_stdout(io.StringIO()):
    import figs, ex2, ex3
    from exercises import EX as DRAW

OFF = 368                      # écart horizontal entre les deux panneaux d'origine
VB = [24, 50, 344, 214]        # cadre du panneau « départ »
STATIC = {'plank', 'broad-jump', 'starts-10', 'decel'}   # deux images fixes : plus clair pour une position ou une course
HOP = {}                       # petit bond pendant l'animation (slug: hauteur)


def groups(sc):
    out, cur = [], None
    for it in sc.items:
        k = it[0]
        if k == 'g+': cur = []; continue
        if k == 'g-': out.append(cur); cur = None; continue
        if cur is not None: cur.append(it)
    return out


def is_panel(it):
    return it[0] == 'b' and it[5] == 't' and it[6] == 't' and it[3] > 300


def sig(it):
    k = it[0]
    if k == 'pl': return ('pl', len(it[1]), it[2], it[3], it[4])
    if k == 'near': return ('near', len(it[1]))
    if k == 'c': return ('c', it[3], it[4])
    if k == 'ring': return ('ring', it[3], it[4], it[5], it[6])
    if k == 'b': return ('b', it[3], it[4], it[5], it[6], it[7])
    return (k,)


def pts_of(it, dx=0):
    k = it[0]
    if k in ('pl', 'near'): return [(x - dx, y) for x, y in it[1]]
    return [(it[1] - dx, it[2])]          # c, ring, b : un seul point (centre ou coin)


def wrap(a):
    while a > math.pi: a -= 2 * math.pi
    while a < -math.pi: a += 2 * math.pi
    return a


def rig(draw, hop=0):
    """Squelette animable, ou None si les deux poses ne se correspondent pas."""
    G = groups(DRAW[draw]())
    if len(G) < 2: return None
    A = [it for it in G[0] if it[0] not in ('t', 'arr') and not is_panel(it)]
    B = [it for it in G[1] if it[0] not in ('t', 'arr') and not is_panel(it)]
    sm = difflib.SequenceMatcher(None, [sig(x) for x in A], [sig(x) for x in B], autojunk=False)
    pairs = [(A[m.a + k], B[m.b + k]) for m in sm.get_matching_blocks() for k in range(m.size)]
    if not pairs: return None

    nodes, index = [], {}            # nœud = (ax, ay, bx, by)
    def node(pa, pb):
        key = (pa[0], pa[1], pb[0], pb[1])
        if key not in index: index[key] = len(nodes); nodes.append(key)
        return index[key]

    # 1) le corps : torse, membres proches et membres opposés
    adj = {}
    body = set()
    for a, b in pairs:
        if a[0] == 'near' or (a[0] == 'pl' and a[2] in ('k', 'f')):
            ids = [node(pa, pb) for pa, pb in zip(pts_of(a), pts_of(b, OFF))]
            for i in ids: body.add(i); adj.setdefault(i, set())
            for u, v in zip(ids, ids[1:]):
                if u != v: adj[u].add(v); adj[v].add(u)
    if not body: return None

    disp = lambda i: math.hypot(nodes[i][2] - nodes[i][0], nodes[i][3] - nodes[i][1])
    parent = {}
    seen = set()
    order = []
    for start in sorted(body, key=lambda i: (round(disp(i), 1), -len(adj[i]), i)):
        if start in seen: continue
        seen.add(start); parent[start] = None; queue = [start]
        while queue:
            u = queue.pop(0); order.append(u)
            for v in sorted(adj[u]):
                if v not in seen: seen.add(v); parent[v] = u; queue.append(v)

    # 2) le reste : charges, ballon, tête, pièces de machine
    extra = {}                        # nœud -> parent (attaché) ou None (glisse en ligne droite)
    items = []
    for a, b in pairs:
        ids = []
        for pa, pb in zip(pts_of(a), pts_of(b, OFF)):
            key = (pa[0], pa[1], pb[0], pb[1])
            if key in index and index[key] in body: ids.append(index[key]); continue
            i = node(pa, pb)
            if i not in extra and i not in body:
                if pa == pb: extra[i] = None
                else:
                    best, bd = None, 1e9
                    for j in body:
                        ax, ay, bx, by = nodes[j]
                        dA = math.hypot(pa[0] - ax, pa[1] - ay); dB = math.hypot(pb[0] - bx, pb[1] - by)
                        if dA <= 70 and abs(dA - dB) <= 2.5 and dA < bd: best, bd = j, dA
                    extra[i] = best
            ids.append(i)
        items.append((a, ids))

    # ordre de calcul : corps (parents avant enfants), puis le reste
    seq = order + [i for i in extra if extra[i] is None] + [i for i in extra if extra[i] is not None]
    pos = {old: new for new, old in enumerate(seq)}
    out_nodes = []
    for i in seq:
        ax, ay, bx, by = nodes[i]
        p = parent.get(i) if i in body else extra[i]
        if p is None:
            out_nodes.append([0, ax, ay, bx, by])
        else:
            px, py, qx, qy = nodes[p]
            la, lb = math.hypot(ax - px, ay - py), math.hypot(bx - qx, by - qy)
            ga = math.atan2(ay - py, ax - px) if la > .5 else (math.atan2(by - qy, bx - qx) if lb > .5 else 0)
            gb = math.atan2(by - qy, bx - qx) if lb > .5 else ga
            out_nodes.append([1, pos[p], round(la, 1), round(lb, 1), round(ga, 4), round(wrap(gb - ga), 4)])

    out_items = []
    for a, ids in items:
        ids = [pos[i] for i in ids]
        k = a[0]
        if k == 'pl': out_items.append(['p', 's-' + a[2], a[3], a[4] or 0, ids])
        elif k == 'near': out_items.append(['n', ids])
        elif k == 'c': out_items.append(['c', 'f-' + a[4], a[3], ids[0]])
        elif k == 'ring':
            fc = 'f-none' if a[6] == 'none' else ('f-halo' if a[4] == 'a' else 'f-eq')
            out_items.append(['r', fc + ' s-' + a[4], a[5], a[3], ids[0]])
        elif k == 'b': out_items.append(['b', a[3], a[4], a[7], ids[0]])
    moving = [pos[i] for i in seq if disp(i) > .5]
    R = dict(vb=VB, n=out_nodes, it=out_items)
    if hop: R['h'] = hop; R['m'] = moving
    R['vb'] = frame_box(R)
    return R


def frame(R, t):
    P = []
    for d in R['n']:
        if d[0] == 0: P.append((d[1] + (d[3] - d[1]) * t, d[2] + (d[4] - d[2]) * t))
        else:
            px, py = P[d[1]]; l = d[2] + (d[3] - d[2]) * t; a = d[4] + d[5] * t
            P.append((px + l * math.cos(a), py + l * math.sin(a)))
    if R.get('h'):
        o = R['h'] * math.sin(math.pi * t)
        for i in R['m']: P[i] = (P[i][0], P[i][1] - o)
    return P


def frame_box(R):
    """Cadre qui contient tout le mouvement (la tête ne doit jamais être coupée)."""
    x0, y0, x1 = VB[0], VB[1], VB[0] + VB[2]
    for k in range(21):
        P = frame(R, k / 20)
        for it in R['it']:
            if it[0] == 'p': ids, m = it[4], it[2] / 2
            elif it[0] == 'n': ids, m = it[1], 8.5
            elif it[0] == 'c': ids, m = [it[3]], it[2]
            elif it[0] == 'r': ids, m = [it[4]], it[3] + it[2] / 2
            else: ids, m = [it[4]], 0
            for i in ids:
                x, y = P[i]
                x0, y0, x1 = min(x0, x - m - 4), min(y0, y - m - 4), max(x1, x + m + 4)
    y1 = VB[1] + VB[3]
    return [math.floor(x0), math.floor(y0), math.ceil(x1 - math.floor(x0)), math.ceil(y1 - math.floor(y0))]


def frames(draw):
    """Deux images fixes (départ, arrivée) avec flèches et repères."""
    sc = DRAW[draw]()
    out, caps = groups(sc), []
    for it in sc.items:
        if it[0] == 't' and it[1] in ('pose-1', 'pose-2'): caps.append(re.sub(r'^\d · ', '', it[4]))
    svgs = []
    for i, items in enumerate(out[:2]):
        ox = 24 if i == 0 else 392
        mid = f'm-{draw}-{i}'
        o = [f"<svg viewBox='{ox} 30 344 234' aria-hidden='true'><defs><marker id='{mid}' viewBox='0 0 10 10' refX='7' refY='5' markerWidth='5' markerHeight='5' orient='auto-start-reverse'><path d='M0 0L10 5L0 10z' class='f-a'/></marker></defs>"]
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
                if is_panel(it): continue
                o.append(f"<rect x='{it[1]}' y='{it[2]}' width='{it[3]}' height='{it[4]}' rx='{it[7]}' class='f-eq s-g' stroke-width='2'/>")
            elif k == 'arr':
                o.append(f"<path d='{it[1]}' class='s-a' stroke-width='4' marker-end='url(#{mid})'/>")
        o.append('</svg>')
        svgs.append(''.join(o))
    return svgs, caps


def art(slug, draw):
    """Ce que l'app affiche pour un exercice : {'rig': …} ou {'a','b','ca','cb'}."""
    if slug not in STATIC:
        R = rig(draw, HOP.get(slug, 0))
        if R: return dict(rig=R)
    s, caps = frames(draw)
    return dict(a=s[0], b=s[1], ca=caps[0], cb=caps[1])
