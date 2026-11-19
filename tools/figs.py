import math

LEN = dict(torso=62, ua=34, fa=32, th=46, sh=44, foot=17, head=14, neck=7)
LW = 12      # limb width
TW = 22      # torso width (side view)
HEX = dict(k='#0d0d0d', q='#73726c', g='#c3c3b4', f='#a3a39b', r='#deded8', t='#ececea', a='#2b78d6',
           ok='#2e9e5b', bad='#d64545', none='none')
TOK = dict(k='k', q='q', g='g', f='f', r='r', t='t', a='a', ok='ok', bad='bad')

def dv(a):
    r = math.radians(a); return (math.cos(r), math.sin(r))
def add(p, a, l):
    v = dv(a); return (p[0]+v[0]*l, p[1]+v[1]*l)
def dist(a, b): return math.hypot(b[0]-a[0], b[1]-a[1])
def angle(a, b): return math.degrees(math.atan2(b[1]-a[1], b[0]-a[0]))
def ik(A, T, l1, l2, bend):
    dd = dist(A, T)
    dd = max(min(dd, l1+l2-0.01), abs(l1-l2)+0.01)
    base = math.atan2(T[1]-A[1], T[0]-A[0])
    ca = (l1*l1 + dd*dd - l2*l2)/(2*l1*dd)
    a = math.acos(max(-1, min(1, ca)))
    j = (A[0]+l1*math.cos(base+bend*a), A[1]+l1*math.sin(base+bend*a))
    ea = math.atan2(T[1]-j[1], T[0]-j[0])
    e = (j[0]+l2*math.cos(ea), j[1]+l2*math.sin(ea))
    return j, e

class Scene:
    def __init__(self, slug, title, H=300):
        self.slug, self.title, self.H = slug, title, H
        self.items = []; self.ox = 0; self.oy = 0
    def at(self, ox, oy): self.ox, self.oy = ox, oy
    def _p(self, p): return (round(p[0]+self.ox), round(p[1]+self.oy))
    def pl(self, pts, c='g', w=LW, dash=None):
        self.items.append(('pl', [self._p(p) for p in pts], c, w, dash))
    def near(self, pts):
        self.items.append(('near', [self._p(p) for p in pts]))
    def far(self, pts): self.pl(pts, 'f', LW)   # membres du côté opposé (gris)
    def circ(self, c, r, fill='k'):
        x, y = self._p(c); self.items.append(('c', x, y, r, fill))
    def ring(self, c, r, stroke='g', sw=2, fill='none'):
        x, y = self._p(c); self.items.append(('ring', x, y, r, stroke, sw, fill))
    def rect(self, x, y, w, h, stroke='g', fill='none', rx=5):
        X, Y = self._p((x, y)); self.items.append(('b', X, Y, round(w), round(h), stroke, fill, rx))
    def arrow(self, p0, p1, ctrl=None, c='a'):
        p0 = self._p(p0); p1 = self._p(p1)
        if ctrl is None: d = f'M{p0[0]} {p0[1]}L{p1[0]} {p1[1]}'
        else:
            ct = self._p(ctrl); d = f'M{p0[0]} {p0[1]}Q{ct[0]} {ct[1]} {p1[0]} {p1[1]}'
        self.items.append(('arr', d, c))
    def text(self, tid, p, s, size=15, weight=None, fill='k', anchor=None):
        x, y = self._p(p); self.items.append(('t', tid, x, y, s, size, weight, fill, anchor))
    def group(self, name): self.items.append(('g+', name))
    def end(self): self.items.append(('g-',))

    # ---------- emitters ----------
    def to_svg(self):
        o = [f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 760 {self.H}' width='760' height='{self.H}' font-family='Helvetica, Arial, sans-serif'>",
             "<rect width='760' height='%d' fill='#ffffff'/>" % self.H,
             f"<defs><marker id='ar' viewBox='0 0 10 10' refX='7' refY='5' markerWidth='5' markerHeight='5' orient='auto-start-reverse'><path d='M0 0L10 5L0 10z' fill='{HEX['a']}'/></marker>"
             f"<marker id='ar-ok' viewBox='0 0 10 10' refX='7' refY='5' markerWidth='5' markerHeight='5' orient='auto-start-reverse'><path d='M0 0L10 5L0 10z' fill='{HEX['ok']}'/></marker></defs>"]
        o.append(f"<text x='24' y='30' font-size='18' font-weight='600' fill='{HEX['k']}'>{self.title}</text>")
        for it in self.items:
            k = it[0]
            if k == 'pl':
                pts = ' '.join(f'{x},{y}' for x, y in it[1]); dash = f" stroke-dasharray='{it[4]}'" if it[4] else ''
                o.append(f"<polyline points='{pts}' fill='none' stroke='{HEX[it[2]]}' stroke-width='{it[3]}' stroke-linecap='round' stroke-linejoin='round'{dash}/>")
            elif k == 'near':
                pts = ' '.join(f'{x},{y}' for x, y in it[1])
                o.append(f"<polyline points='{pts}' fill='none' stroke='{HEX['g']}' stroke-width='{LW+4}' stroke-linecap='round' stroke-linejoin='round'/>")
                o.append(f"<polyline points='{pts}' fill='none' stroke='{HEX['k']}' stroke-width='{LW}' stroke-linecap='round' stroke-linejoin='round'/>")
            elif k == 'c':
                o.append(f"<circle cx='{it[1]}' cy='{it[2]}' r='{it[3]}' fill='{HEX[it[4]]}'/>")
            elif k == 'ring':
                o.append(f"<circle cx='{it[1]}' cy='{it[2]}' r='{it[3]}' fill='{HEX[it[6]]}' stroke='{HEX[it[4]]}' stroke-width='{it[5]}'/>")
            elif k == 'b':
                o.append(f"<rect x='{it[1]}' y='{it[2]}' width='{it[3]}' height='{it[4]}' rx='{it[7]}' fill='{HEX[it[6]]}' stroke='{HEX[it[5]]}' stroke-width='2'/>")
            elif k == 'arr':
                mk = 'ar-ok' if it[2] == 'ok' else 'ar'
                o.append(f"<path d='{it[1]}' fill='none' stroke='{HEX[it[2]]}' stroke-width='3.5' stroke-linecap='round' marker-end='url(#{mk})'/>")
            elif k == 't':
                _, tid, x, y, s, size, weight, fill, anchor = it
                extra = (f" font-weight='{weight}'" if weight else '') + (f" text-anchor='{anchor}'" if anchor else '')
                o.append(f"<text x='{x}' y='{y}' font-size='{size}' fill='{HEX[fill]}'{extra}>{s}</text>")
            elif k == 'g+': o.append('<g>')
            elif k == 'g-': o.append('</g>')
        o.append('</svg>')
        return '\n'.join(o)

    def to_jsx(self):
        used = set()
        body = []
        for it in self.items:
            k = it[0]
            if k == 'pl':
                pts = ' '.join(f'{x},{y}' for x, y in it[1])
                if it[4]:
                    body.append(f"<polyline points='{pts}' fill='none' stroke={{{it[2]}}} strokeWidth='{it[3]}' strokeLinecap='round' strokeDasharray='{it[4]}'/>")
                else:
                    body.append(f"{{P('{pts}',{it[2]},{it[3]})}}")
                used.add(it[2])
            elif k == 'near':
                pts = ' '.join(f'{x},{y}' for x, y in it[1]); body.append(f"{{N('{pts}')}}")
            elif k == 'c':
                body.append(f"{{C({it[1]},{it[2]},{it[3]},{it[4]})}}"); used.add(it[4])
            elif k == 'ring':
                f = "'none'" if it[6] == 'none' else it[6]
                body.append(f"<circle cx='{it[1]}' cy='{it[2]}' r='{it[3]}' fill={{{f}}} stroke={{{it[4]}}} strokeWidth='{it[5]}'/>"); used.add(it[4])
                if it[6] != 'none': used.add(it[6])
            elif k == 'b':
                f = "'none'" if it[6] == 'none' else it[6]
                body.append(f"{{B({it[1]},{it[2]},{it[3]},{it[4]},{it[5]},{f},{it[7]})}}"); used.add(it[5])
                if it[6] != 'none': used.add(it[6])
            elif k == 'arr':
                if it[2] == 'ok':
                    body.append(f"<path d='{it[1]}' fill='none' stroke={{ok}} strokeWidth='3.5' strokeLinecap='round' markerEnd='url(#{self.slug}-arrow-ok)'/>"); used.add('ok'); used.add('arrok')
                else:
                    body.append(f"{{A('{it[1]}')}}"); used.add('arr')
            elif k == 't':
                _, tid, x, y, s, size, weight, fill, anchor = it
                extra = (f" fontWeight='{weight}'" if weight else '') + (f" textAnchor='{anchor}'" if anchor else '')
                body.append(f"<text data-claude-text-id='{tid}' x='{x}' y='{y}' fontSize='{size}'{extra} fill={{{fill}}}>{s}</text>"); used.add(fill)
            elif k == 'g+': body.append(f"<g data-claude-anchor='{it[1]}'>")
            elif k == 'g-': body.append('</g>')
        tok = dict(k='var(--cds-text-primary)', q='var(--cds-text-secondary)', g='var(--cds-chart-axis)', f='var(--cds-chart-axis)', r='var(--cds-chart-grid)',
                   t='var(--cds-chart-reference-tint)', a='var(--cds-chart-categorical-1)', ok='var(--cds-chart-status-good)', bad='var(--cds-chart-status-critical)')
        need = ['k', 't', 'a', 'g'] + [c for c in ['q', 'r', 'f', 'ok', 'bad'] if c in used]
        consts = ', '.join(f"{c} = '{tok[c]}'" for c in need)
        hl = ["const P = (p, c, w) => <polyline points={p} fill='none' stroke={c} strokeWidth={w} strokeLinecap='round' strokeLinejoin='round'/>;",
              f"const N = p => <g>{{P(p, g, {LW+4})}}{{P(p, k, {LW})}}</g>;",
              "const C = (x, y, rad, c) => <circle cx={x} cy={y} r={rad} fill={c}/>;",
              "const B = (x, y, w, h, c, f, rx) => <rect x={x} y={y} width={w} height={h} rx={rx} fill={f} stroke={c} strokeWidth='2'/>;",
              f"const A = d => <path d={{d}} fill='none' stroke={{a}} strokeWidth='3.5' strokeLinecap='round' markerEnd='url(#{self.slug}-arrow)'/>;"]
        mk = f"<marker id='{self.slug}-arrow' viewBox='0 0 10 10' refX='7' refY='5' markerWidth='5' markerHeight='5' orient='auto-start-reverse'><path d='M0 0L10 5L0 10z' fill={{a}}/></marker>"
        if 'arrok' in used:
            mk += f"<marker id='{self.slug}-arrow-ok' viewBox='0 0 10 10' refX='7' refY='5' markerWidth='5' markerHeight='5' orient='auto-start-reverse'><path d='M0 0L10 5L0 10z' fill={{ok}}/></marker>"
        aria = self.title.replace("'", "’")
        code = (f"export default () => {{ const {consts}; " + ' '.join(hl) +
                f" return <svg viewBox='0 0 760 {self.H}' role='img' aria-label='{aria}' fontSize='15'><defs>{mk}</defs>"
                f"<text data-claude-text-id='title' x='24' y='30' fontSize='18' fontWeight='600' fill={{k}}>{aria}</text>"
                + ''.join(body) + "</svg>; };")
        return code

# ---------- figures ----------
G = 208   # local ground y

def side(sc, hip, torso=-90, head=None, arms=(), legs=(), spine=None, headpos=None):
    """side view figure. arms/legs: dicts. returns joints"""
    if spine:
        pts = spine; sh = spine[-1]; t_ang = angle(spine[-2], spine[-1])
    else:
        sh = add(hip, torso, LEN['torso']); pts = [hip, sh]; t_ang = torso
    h_ang = t_ang if head is None else head
    hc = headpos or add(sh, h_ang, LEN['head']+LEN['neck'])
    J = dict(hip=hip, sh=sh, head=hc, arms=[], legs=[])
    def arm(a):
        if 'pts' in a: el, ha = a['pts']
        elif 'hand' in a: el, ha = ik(sh, a['hand'], LEN['ua'], LEN['fa'], a.get('bend', 1))
        else:
            el = add(sh, a['ua'], LEN['ua']); ha = add(el, a['fa'], LEN['fa'])
        return [sh, el, ha]
    def leg(l):
        if 'ankle' in l: kn, an = ik(hip, l['ankle'], LEN['th'], LEN['sh'], l.get('bend', -1))
        else:
            kn = add(hip, l['th'], LEN['th']); an = add(kn, l['sh'], LEN['sh'])
        ft = add(an, l.get('foot', 0), LEN['foot'])
        return [hip, kn, an, ft]
    A = [(arm(a), a.get('far', False)) for a in arms]
    Lg = [(leg(l), l.get('far', False)) for l in legs]
    for p, far in Lg:
        if far: sc.far(p)
    for p, far in A:
        if far: sc.far(p)
    sc.pl(pts, 'k', TW)
    sc.circ(hc, LEN['head'], 'k')
    for p, far in Lg:
        if not far: sc.near(p)
        J['legs'].append(p)
    for p, far in A:
        if not far: sc.near(p)
        J['arms'].append(p)
    return J

def front(sc, c, sy, arms, legs='stand', hy=None):
    """front view. arms: (left_pts, right_pts) each [elbow, hand] absolute, or dict(hand=(dx,dy), bend) mirrored"""
    hy = hy if hy is not None else sy+60
    shL, shR = (c-24, sy+2), (c+24, sy+2)
    # legs
    if legs == 'stand':
        for s in (-1, 1):
            sc.near([(c+s*11, hy), (c+s*13, hy+46), (c+s*14, hy+88), (c+s*24, hy+90)])
    elif legs == 'seated':
        for s in (-1, 1):
            sc.near([(c+s*12, hy), (c+s*21, hy+12), (c+s*22, hy+52), (c+s*32, hy+54)])
    # torso
    sc.items.append(('pl', [sc._p(p) for p in [(c-19, sy+4), (c+19, sy+4), (c+12, hy), (c-12, hy), (c-19, sy+4), (c+19, sy+4)]], 'k', 12, None))
    sc.pl([(c, sy+6), (c, hy-2)], 'k', 26)
    sc.circ((c, sy-22), LEN['head'], 'k')
    out = []
    for s, sh in ((-1, shL), (1, shR)):
        a = arms
        if 'hand' in a:
            T = (c+s*a['hand'][0], sy+a['hand'][1])
            el, ha = ik(sh, T, LEN['ua'], LEN['fa'], s*a.get('bend', 1))
        else:
            el = (c+s*a['el'][0], sy+a['el'][1]); ha = (c+s*a['ha'][0], sy+a['ha'][1])
        sc.near([sh, el, ha]); out.append((sh, el, ha))
    return out

def panels(sc, l1='1 · Départ', l2='2 · Arrivée', draw=None):
    for i, (ox, lab) in enumerate(((24, l1), (392, l2))):
        sc.at(0, 0)
        sc.group(f'pose-{i+1}')
        sc.rect(ox, 46, 344, 238, stroke='t', fill='t', rx=10)
        sc.at(ox, 46)
        sc.pl([(12, G), (332, G)], 'r', 2)
        draw(sc, i)
        sc.text(f'pose-{i+1}', (14, 230), lab, 15, 600, 'k')
        sc.end()
    sc.at(0, 0)

def dumbbell_h(sc, p, half=13):
    """dumbbell seen from the side (horizontal bar)"""
    x, y = p
    sc.pl([(x-half, y), (x+half, y)], 'a', 5)
    sc.pl([(x-half-2, y-8), (x-half-2, y+8)], 'a', 7)
    sc.pl([(x+half+2, y-8), (x+half+2, y+8)], 'a', 7)

def dumbbell_end(sc, p, r=10):
    sc.circ(p, r, 'a')
