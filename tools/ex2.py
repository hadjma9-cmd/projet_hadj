"""Second batch of exercise drawings: floor push-ups, two-dumbbell triceps, and every alternative."""
import math
from figs import *
from exercises import EX, ex


def flat_bench(sc, x0=80, x1=214, top=166):
    sc.rect(x0, top, x1 - x0, 9, 'g', 't', 4)
    sc.pl([(x0 + 16, top + 11), (x0 + 16, 206)], 'g', 6)
    sc.pl([(x1 - 16, top + 11), (x1 - 16, 206)], 'g', 6)


def rail(sc, x):
    sc.pl([(x, 10), (x, 206)], 'g', 3)
    sc.pl([(x - 10, 10), (x + 10, 10)], 'g', 4)


def bar_end(sc, p):
    sc.circ(p, 10, 'a')


def db_perp(sc, p, ang, half=13):
    """dumbbell seen side-on, its handle perpendicular to the forearm (angle ang)"""
    u = dv(ang + 90)
    a = (p[0] - u[0] * half, p[1] - u[1] * half); b = (p[0] + u[0] * half, p[1] + u[1] * half)
    sc.pl([a, b], 'a', 5)
    n = dv(ang)
    for q in (a, b):
        sc.pl([(q[0] - n[0] * 8, q[1] - n[1] * 8), (q[0] + n[0] * 8, q[1] + n[1] * 8)], 'a', 7)


def db_vertical(sc, p, half=13):
    db_perp(sc, p, 0, half)


def scale_from(sc, start, k, px, py):
    """scale every item drawn since `start` around local point (px, py)"""
    PX, PY = px + sc.ox, py + sc.oy
    S = lambda p: (round(PX + (p[0] - PX) * k), round(PY + (p[1] - PY) * k))
    for i in range(start, len(sc.items)):
        it = sc.items[i]; t = it[0]
        if t == 'pl':
            sc.items[i] = ('pl', [S(p) for p in it[1]], it[2], it[3], it[4])
        elif t == 'near':
            sc.items[i] = ('near', [S(p) for p in it[1]])
        elif t == 'c':
            x, y = S((it[1], it[2])); sc.items[i] = ('c', x, y, round(it[3] * k, 1), it[4])
        elif t == 'ring':
            x, y = S((it[1], it[2])); sc.items[i] = ('ring', x, y, round(it[3] * k, 1), it[4], it[5], it[6])
        elif t == 'b':
            x, y = S((it[1], it[2])); sc.items[i] = ('b', x, y, round(it[3] * k), round(it[4] * k), it[5], it[6], it[7])


# ---------- lying on a flat bench (head on the left) ----------
LIE_HIP = (196, 155)
LIE_SH = add(LIE_HIP, 180, LEN['torso'])


def lie(sc, arms):
    return side(sc, LIE_HIP, 180, legs=[dict(ankle=(244, 206), bend=1, foot=0)], arms=arms)


def press_pose(i):
    sh = LIE_SH
    if i == 0:
        el = add(sh, 75, LEN['ua']); ha = add(el, -90, LEN['fa'])
    else:
        el = add(sh, -80, LEN['ua']); ha = add(el, -86, LEN['fa'])
    return el, ha


@ex('db-bench', 'Développé couché haltères : pousse vers le plafond')
def _(sc):
    def draw(sc, i):
        flat_bench(sc)
        el, ha = press_pose(i)
        lie(sc, [dict(pts=(el, ha))])
        dumbbell_end(sc, (ha[0], ha[1] - 5))
        if i == 0: sc.arrow((ha[0] + 34, ha[1] - 4), (ha[0] + 34, ha[1] - 52))
    panels(sc, draw=draw)


@ex('smith-bench', 'Développé couché à la barre guidée')
def _(sc):
    def draw(sc, i):
        el, ha = press_pose(i)
        rail(sc, round(ha[0]))
        flat_bench(sc)
        lie(sc, [dict(pts=(el, ha))])
        bar_end(sc, (ha[0], ha[1] - 5))
        if i == 0: sc.arrow((ha[0] + 34, ha[1] - 4), (ha[0] + 34, ha[1] - 52))
    panels(sc, draw=draw)


def incline_bench(sc, hip, tor):
    u = dv(tor); nb = dv(tor - 90)
    b0 = (hip[0] + nb[0] * 17, hip[1] + nb[1] * 17); b1 = (b0[0] + u[0] * 96, b0[1] + u[1] * 96)
    sc.pl([b0, b1], 'g', 9)
    sc.pl([(b0[0] + 6, b0[1] + 2), (b0[0] + 48, b0[1] + 2)], 'g', 9)
    mid = (b0[0] + u[0] * 56, b0[1] + u[1] * 56)
    sc.pl([mid, (mid[0], 206)], 'g', 6); sc.pl([(b0[0] + 30, b0[1] + 8), (b0[0] + 30, 206)], 'g', 6)


@ex('smith-incline', 'Développé incliné à la barre guidée')
def _(sc):
    def draw(sc, i):
        hip = (166, 160); tor = -146
        sh = add(hip, tor, LEN['torso'])
        if i == 0: el = add(sh, 70, LEN['ua']); ha = add(el, -90, LEN['fa'])
        else: el = add(sh, -80, LEN['ua']); ha = add(el, -84, LEN['fa'])
        rail(sc, 125)
        incline_bench(sc, hip, tor)
        side(sc, hip, tor, legs=[dict(th=-6, sh=84, foot=0)], arms=[dict(pts=(el, ha))])
        bar_end(sc, (125, ha[1] - 5))
        if i == 0: sc.arrow((160, ha[1] - 4), (160, ha[1] - 52))
    panels(sc, draw=draw)


# ---------- seated side view machines ----------
def seat(sc, back=True):
    sc.pl([(84, 176), (140, 176)], 'g', 9)
    sc.pl([(112, 182), (112, 206)], 'g', 6)
    if back: sc.pl([(84, 166), (72, 86)], 'g', 9)


@ex('machine-shoulder-press', 'Développé épaules à la machine : pousse vers le haut')
def _(sc):
    def draw(sc, i):
        sc.rect(30, 22, 14, 186, 'g', 't', 3)
        seat(sc)
        hip = (104, 160); sh = add(hip, -95, LEN['torso'])
        if i == 0: el = (sh[0] + 9, sh[1] + 32); ha = (el[0] + 5, el[1] - 32)
        else: el = add(sh, -84, LEN['ua']); ha = add(el, -86, LEN['fa'])
        sc.pl([(37, 34), ha], 'g', 5)
        side(sc, hip, -95, head=-92, legs=[dict(th=0, sh=86, foot=0)], arms=[dict(pts=(el, ha))])
        sc.pl([(ha[0] - 9, ha[1]), (ha[0] + 9, ha[1])], 'a', 7)
        if i == 0: sc.arrow((160, 112), (160, 62))
    panels(sc, draw=draw)


@ex('machine-triceps-dip', 'Dips assis à la machine : pousse les poignées vers le bas')
def _(sc):
    def draw(sc, i):
        seat(sc)
        hip = (104, 160); sh = add(hip, -94, LEN['torso'])
        if i == 0: el = add(sh, 122, LEN['ua']); ha = add(el, 18, LEN['fa'])
        else: el = add(sh, 96, LEN['ua']); ha = add(el, 90, LEN['fa'])
        sc.pl([(196, 104), ha], 'g', 5)
        sc.rect(190, 60, 14, 148, 'g', 't', 3)
        side(sc, hip, -94, head=-92, legs=[dict(th=0, sh=86, foot=0)], arms=[dict(pts=(el, ha))])
        sc.pl([(ha[0] - 8, ha[1]), (ha[0] + 8, ha[1])], 'a', 7)
        if i == 0: sc.arrow((150, 112), (150, 160))
    panels(sc, draw=draw)


@ex('machine-row', 'Rowing à la machine : poitrine contre le coussin, tire les coudes')
def _(sc):
    def draw(sc, i):
        sc.pl([(84, 176), (140, 176)], 'g', 9); sc.pl([(112, 182), (112, 206)], 'g', 6)
        sc.rect(130, 92, 11, 60, 'g', 't', 5); sc.pl([(136, 152), (136, 206)], 'g', 6)
        sc.rect(250, 30, 14, 178, 'g', 't', 3)
        hip = (104, 160); sh = add(hip, -82, LEN['torso'])
        if i == 0: el = add(sh, 12, LEN['ua']); ha = add(el, 10, LEN['fa'])
        else: el = add(sh, 150, LEN['ua']); ha = add(el, -4, LEN['fa'])
        sc.pl([(256, 44), ha], 'g', 5)
        side(sc, hip, -82, head=-82, legs=[dict(th=0, sh=86, foot=0)], arms=[dict(pts=(el, ha))])
        sc.pl([(ha[0], ha[1] - 9), (ha[0], ha[1] + 9)], 'a', 7)
        if i == 0: sc.arrow((214, 82), (168, 82))
    panels(sc, draw=draw)


@ex('machine-preacher-curl', 'Curl biceps à la machine : les bras restent sur le pupitre')
def _(sc):
    def draw(sc, i):
        sc.pl([(84, 176), (140, 176)], 'g', 9); sc.pl([(112, 182), (112, 206)], 'g', 6)
        hip = (104, 160); sh = add(hip, -84, LEN['torso'])
        el = add(sh, 42, LEN['ua'])
        p0 = add(sh, 42 + 90, 15); sc.pl([add(p0, 42, 2), add(p0, 42, 50)], 'g', 10)
        sc.pl([add(p0, 42, 44), (add(p0, 42, 44)[0], 206)], 'g', 6)
        ha = add(el, 48, LEN['fa']) if i == 0 else add(el, -84, LEN['fa'])
        sc.pl([el, ha], 'g', 4)
        side(sc, hip, -84, head=-86, legs=[dict(th=0, sh=86, foot=0)], arms=[dict(pts=(el, ha))])
        sc.pl([(ha[0] - 8, ha[1]), (ha[0] + 8, ha[1])], 'a', 7)
        if i == 0: sc.arrow((196, 146), (184, 94), (214, 112))
    panels(sc, draw=draw)


@ex('leg-extension', 'Leg extension : tends les jambes, redescends lentement')
def _(sc):
    def draw(sc, i):
        sc.rect(84, 150, 30, 58, 'g', 't', 4)
        sc.pl([(84, 146), (150, 146)], 'g', 9)
        sc.pl([(84, 136), (68, 52)], 'g', 9)
        hip = (104, 130); kn = add(hip, 0, LEN['th'])
        sa = 92 if i == 0 else -4
        rol = add(add(kn, sa, LEN['sh'] - 6), sa - 90, 14)
        sc.pl([(kn[0], kn[1] + 4), rol], 'g', 5)
        side(sc, hip, -100, head=-92, legs=[dict(th=0, sh=sa, foot=sa - 82)], arms=[dict(hand=(118, 142), bend=1)])
        sc.circ(rol, 10, 'a')
        if i == 0: sc.arrow((196, 196), (214, 130), (222, 180))
    panels(sc, draw=draw)


# ---------- top views ----------
def top_arms(sc, c, hands, handle='circle'):
    L, R = (c - 24, 116), (c + 24, 116)
    for sh, h in ((L, hands[0]), (R, hands[1])):
        el = ((sh[0] + h[0]) / 2, (sh[1] + h[1]) / 2 + 3)
        sc.near([sh, el, h])
        if handle == 'circle': sc.circ(h, 7, 'a')
        else: sc.pl([(h[0], h[1] - 9), (h[0], h[1] + 9)], 'a', 7)
    sc.pl([L, R], 'k', 22)
    sc.circ((c, 112), 15, 'k')


@ex('pec-deck', 'Butterfly à la machine : ramène les bras devant toi (vu de dessus)')
def _(sc):
    def draw(sc, i):
        c = 172
        sc.rect(c - 26, 138, 52, 50, 'g', 't', 8)
        sc.rect(c - 30, 126, 60, 12, 'g', 't', 6)
        hands = ((c - 92, 114), (c + 92, 114)) if i == 0 else ((c - 9, 58), (c + 9, 58))
        top_arms(sc, c, hands, 'bar')
        if i == 0:
            sc.arrow((c - 100, 94), (c - 40, 48), (c - 98, 50)); sc.arrow((c + 100, 94), (c + 40, 48), (c + 98, 50))
    panels(sc, '1 · Départ (vu de dessus)', '2 · Arrivée (vu de dessus)', draw=draw)


@ex('db-fly', 'Écarté couché haltères : ouvre puis referme les bras (vu de dessus)')
def _(sc):
    def draw(sc, i):
        c = 172
        sc.rect(c - 24, 62, 48, 130, 'g', 't', 8)
        sc.pl([(c - 9, 150), (c - 18, 182), (c - 30, 204)], 'k', 12)
        sc.pl([(c + 9, 150), (c + 18, 182), (c + 30, 204)], 'k', 12)
        sc.pl([(c, 100), (c, 150)], 'k', 34)
        L, R = (c - 24, 96), (c + 24, 96)
        hands = ((c - 94, 100), (c + 94, 100)) if i == 0 else ((c - 8, 108), (c + 8, 108))
        for sh, h in ((L, hands[0]), (R, hands[1])):
            el = ((sh[0] + h[0]) / 2, (sh[1] + h[1]) / 2 + (6 if i == 0 else -4))
            sc.near([sh, el, h])
            sc.pl([(h[0], h[1] - 10), (h[0], h[1] + 10)], 'a', 7)
        sc.pl([L, R], 'k', 20)
        sc.circ((c, 74), 14, 'k')
        if i == 0:
            sc.arrow((c - 100, 84), (c - 30, 82), (c - 70, 50)); sc.arrow((c + 100, 84), (c + 30, 82), (c + 70, 50))
    panels(sc, '1 · Départ (vu de dessus)', '2 · Arrivée (vu de dessus)', draw=draw)


# ---------- front views ----------
def pad(sc, sh, el):
    a = angle(sh, el); m = add(sh, a, LEN['ua'] * 0.62)
    n = dv(a + 90)
    sc.pl([(m[0] - n[0] * 10, m[1] - n[1] * 10), (m[0] + n[0] * 10, m[1] + n[1] * 10)], 'a', 9)


@ex('machine-lateral-raise', 'Élévations latérales à la machine : monte les coudes sur les côtés')
def _(sc):
    def draw(sc, i):
        c, hy = 172, 148; sy = hy - 60
        sc.rect(c - 26, sy - 34, 52, 96, 'g', 't', 8)
        sc.rect(c - 40, hy + 2, 80, 12, 'g', 't', 5)
        sc.pl([(c, hy + 16), (c, 206)], 'g', 6)
        a = dict(el=(29, 34), ha=(31, 64)) if i == 0 else dict(el=(57, 6), ha=(87, 9))
        arms = front(sc, c, sy, a, 'seated', hy)
        for sh, el, ha in arms: pad(sc, sh, el)
        if i == 0:
            sc.arrow((c + 56, sy + 56), (c + 100, sy + 6), (c + 98, sy + 46)); sc.arrow((c - 56, sy + 56), (c - 100, sy + 6), (c - 98, sy + 46))
        else:
            sc.pl([(c - 112, sy + 2), (c + 112, sy + 2)], 'a', 2, '5 5')
    panels(sc, draw=draw)


@ex('seated-lateral-raise', 'Élévations latérales assis : monte jusqu’à la hauteur des épaules')
def _(sc):
    def draw(sc, i):
        c, hy = 172, 148; sy = hy - 60
        sc.rect(c - 48, hy + 4, 96, 11, 'g', 't', 5)
        sc.pl([(c - 36, hy + 17), (c - 36, 206)], 'g', 6); sc.pl([(c + 36, hy + 17), (c + 36, 206)], 'g', 6)
        a = dict(el=(29, 36), ha=(31, 66)) if i == 0 else dict(el=(57, 8), ha=(88, 12))
        arms = front(sc, c, sy, a, 'seated', hy)
        for sh, el, ha in arms: dumbbell_end(sc, (ha[0], ha[1] + (8 if i == 0 else 2)))
        if i == 0:
            sc.arrow((c + 54, sy + 66), (c + 100, sy + 20), (c + 98, sy + 58)); sc.arrow((c - 54, sy + 66), (c - 100, sy + 20), (c - 98, sy + 58))
        else:
            sc.pl([(c - 112, sy + 2), (c + 112, sy + 2)], 'a', 2, '5 5')
    panels(sc, draw=draw)


@ex('standing-db-press', 'Développé épaules haltères debout : pousse au-dessus de la tête')
def _(sc):
    def draw(sc, i):
        c, hy = 172, 112; sy = hy - 60
        n0 = len(sc.items)
        a = dict(el=(50, 20), ha=(52, -12)) if i == 0 else dict(el=(36, -30), ha=(30, -62))
        arms = front(sc, c, sy, a, 'stand', hy)
        for sh, el, ha in arms: dumbbell_h(sc, (ha[0], ha[1] - 4))
        scale_from(sc, n0, 0.8, c, 206)
        if i == 0:
            sc.arrow((c + 96, 104), (c + 96, 60)); sc.arrow((c - 96, 104), (c - 96, 60))
    panels(sc, draw=draw)


@ex('db-overhead-ext2', 'Extension triceps haltères : un haltère par main, seuls les avant-bras bougent')
def _(sc):
    def draw(sc, i):
        c, hy = 172, 148; sy = hy - 60
        sc.rect(c - 26, sy - 30, 52, 92, 'g', 't', 8)
        sc.rect(c - 40, hy + 2, 80, 12, 'g', 't', 5)
        sc.pl([(c, hy + 16), (c, 206)], 'g', 6)
        a = dict(el=(18, -34), ha=(19, -16)) if i == 0 else dict(el=(15, -34), ha=(13, -66))
        arms = front(sc, c, sy, a, 'seated', hy)
        for sh, el, ha in arms:
            dumbbell_end(sc, (ha[0] + (2 if ha[0] > c else -2) * (i == 0), ha[1] + (0 if i == 0 else -4)), 9)
            if i == 0: sc.ring(el, 14, 'a', 2, 'none')
        sc.ring((c, sy - 22), 16, 't', 4, 'none')
        sc.circ((c, sy - 22), LEN['head'], 'k')
        if i == 0:
            sc.arrow((c + 62, sy - 2), (c + 62, sy - 52)); sc.arrow((c - 62, sy - 2), (c - 62, sy - 52))
    panels(sc, draw=draw)


@ex('bent-reverse-fly', 'Oiseau haltères buste penché : monte les bras sur les côtés (vu de face)')
def _(sc):
    def draw(sc, i):
        c = 172
        sc.rect(c - 56, 170, 112, 10, 'g', 't', 4)
        sc.pl([(c - 44, 182), (c - 44, 206)], 'g', 6); sc.pl([(c + 44, 182), (c + 44, 206)], 'g', 6)
        for s in (-1, 1):
            sc.near([(c + s * 14, 160), (c + s * 24, 176), (c + s * 26, 204), (c + s * 36, 205)])
        L, R = (c - 26, 128), (c + 26, 128)
        sc.pl([(c, 132), (c, 156)], 'k', 30)
        sc.pl([L, R], 'k', 22)
        for s, sh in ((-1, L), (1, R)):
            if i == 0: el, ha = (sh[0] + s * 6, sh[1] + 32), (sh[0] + s * 8, sh[1] + 62)
            else: el, ha = (sh[0] + s * 32, sh[1] + 4), (sh[0] + s * 64, sh[1] + 6)
            sc.near([sh, el, ha]); dumbbell_end(sc, (ha[0], ha[1] + 4), 9)
        sc.ring((c, 148), 16, 't', 4, 'none'); sc.circ((c, 148), LEN['head'], 'k')
        if i == 0:
            sc.arrow((c + 46, 196), (c + 96, 132), (c + 94, 188)); sc.arrow((c - 46, 196), (c - 96, 132), (c - 94, 188))
        else:
            sc.pl([(c - 112, 128), (c + 112, 128)], 'a', 2, '5 5')
    panels(sc, draw=draw)


@ex('sumo-squat', 'Squat sumo haltère : pieds écartés, genoux vers l’extérieur')
def _(sc):
    def draw(sc, i):
        c = 172
        hy = 120 if i == 0 else 152
        sy = hy - 60
        front(sc, c, sy, dict(el=(17, 32), ha=(5, 62)), legs=None, hy=hy)
        for s in (-1, 1):
            kn = (c + s * 30, 164) if i == 0 else (c + s * 46, 170)
            sc.near([(c + s * 11, hy), kn, (c + s * 44, 204), (c + s * 58, 206)])
        sc.pl([(c - 12, hy - 2), (c + 12, hy - 2)], 'k', 14)
        db_vertical(sc, (c, sy + 76))
        if i == 0: sc.arrow((c + 92, 90), (c + 92, 138)); sc.arrow((c - 92, 90), (c - 92, 138))
    panels(sc, draw=draw)


# ---------- floor / bodyweight ----------
@ex('pushup', 'Pompes : corps droit comme une planche, poitrine vers le sol')
def _(sc):
    def draw(sc, i):
        a = (70, 201)
        th = -23.6 if i == 0 else -9.5
        kn = add(a, th, LEN['sh']); hip = add(kn, th, LEN['th']); sh = add(hip, th, LEN['torso'])
        hand = (212, 204)
        if i == 0: el = ((sh[0] + hand[0]) / 2, (sh[1] + hand[1]) / 2)
        else: el, _h = ik(sh, hand, LEN['ua'], LEN['fa'], 1)
        sc.pl([hip, sh], 'k', TW)
        sc.circ(add(sh, th - 8, 21), LEN['head'], 'k')
        sc.near([hip, kn, a, (62, 207)])
        sc.near([sh, el, hand])
        if i == 0: sc.arrow((262, 118), (270, 168), (282, 136))
        else: sc.pl([(64, 182), (232, 168)], 'ok', 3, '6 6')
    panels(sc, draw=draw)


@ex('smith-inverted-row', 'Tractions australiennes à la barre guidée : tire la poitrine vers la barre')
def _(sc):
    def draw(sc, i):
        H = (330, 206); bar = (213, 126)
        phi = 9 if i == 0 else 26
        sh = (H[0] - 152 * math.cos(math.radians(phi)), H[1] - 152 * math.sin(math.radians(phi)))
        d = angle(sh, H)
        hip = add(sh, d, LEN['torso']); kn = add(hip, d, LEN['th'])
        rail(sc, bar[0])
        sc.pl([hip, sh], 'k', TW)
        sc.circ(add(sh, d + 180, 21), LEN['head'], 'k')
        sc.near([hip, kn, H, (H[0] + 6, H[1] - 15)])
        el, ha = ik(sh, bar, LEN['ua'], LEN['fa'], -1)
        sc.near([sh, el, ha])
        bar_end(sc, bar)
        if i == 0: sc.arrow((150, 150), (150, 104))
        else: sc.pl([(150, 112), (318, 180)], 'ok', 3, '6 6')
    panels(sc, draw=draw)


@ex('db-pullover', 'Pull-over haltère : de derrière la tête jusqu’au-dessus de la poitrine')
def _(sc):
    def draw(sc, i):
        flat_bench(sc)
        sh = LIE_SH
        if i == 0: el = add(sh, 172, LEN['ua']); ha = add(el, 178, LEN['fa'])
        else: el = add(sh, -92, LEN['ua']); ha = add(el, -90, LEN['fa'])
        lie(sc, [dict(pts=(el, ha))])
        sc.circ((ha[0] + (-4 if i == 0 else 0), ha[1] + (0 if i == 0 else -5)), 11, 'a')
        if i == 0: sc.arrow((56, 120), (104, 76), (58, 78))
    panels(sc, draw=draw)


@ex('db-skullcrusher', 'Extension triceps allongé : seuls les avant-bras bougent')
def _(sc):
    def draw(sc, i):
        flat_bench(sc)
        sh = LIE_SH
        el = add(sh, -100, LEN['ua'])
        ha = add(el, 150, LEN['fa']) if i == 0 else add(el, -90, LEN['fa'])
        lie(sc, [dict(pts=(el, ha))])
        dumbbell_end(sc, (ha[0] + (-3 if i == 0 else 0), ha[1] - (2 if i == 0 else 5)), 9)
        sc.ring(el, 14, 'a', 2, 'none')
        if i == 0: sc.arrow((82, 116), (118, 78), (84, 80))
    panels(sc, draw=draw)


@ex('incline-db-row', 'Rowing haltères sur banc incliné : poitrine collée au banc')
def _(sc):
    def draw(sc, i):
        tor = -32
        hip = (124, 154); sh = add(hip, tor, LEN['torso'])
        b0 = add(hip, tor + 90, 17); b0 = add(b0, tor + 180, 22); b1 = add(b0, tor, 122)
        sc.pl([b0, b1], 'g', 9)
        sc.pl([add(b0, tor, 40), (add(b0, tor, 40)[0], 206)], 'g', 6)
        sc.pl([add(b0, tor, 96), (add(b0, tor, 96)[0], 206)], 'g', 6)
        if i == 0: el = add(sh, 92, LEN['ua']); ha = add(el, 90, LEN['fa'])
        else: el = add(sh, -150, LEN['ua']); ha = add(el, 96, LEN['fa'])
        side(sc, hip, tor, head=tor + 6, legs=[dict(ankle=(64, 205), bend=1, foot=180)], arms=[dict(pts=(el, ha))])
        dumbbell_end(sc, (ha[0], ha[1] + 4))
        if i == 0: sc.arrow((222, 196), (222, 148))
    panels(sc, draw=draw)


# ---------- standing ----------
@ex('hammer-curl', 'Curl marteau : paumes face au corps, seul l’avant-bras bouge')
def _(sc):
    def draw(sc, i):
        hip = (160, 114); sh = add(hip, -90, LEN['torso'])
        el = add(sh, 88, LEN['ua']); fa = 82 if i == 0 else -66
        ha = add(el, fa, LEN['fa'])
        side(sc, hip, -90, legs=[dict(ankle=(160, 202), bend=-1, foot=0)], arms=[dict(pts=(el, ha))])
        db_perp(sc, add(ha, fa, 4), fa)
        if i == 0: sc.arrow((200, 116), (202, 64), (222, 90))
        sc.ring(el, 15, 'a', 2, 'none')
    panels(sc, draw=draw)


@ex('goblet-squat', 'Squat gobelet : haltère contre la poitrine, buste droit')
def _(sc):
    def draw(sc, i):
        an = (180, 204)
        if i == 0: hip = (176, 116); tor = -90
        else: hip = (138, 166); tor = -62
        sh = add(hip, tor, LEN['torso'])
        db = add(add(sh, tor + 90, 22), tor + 180, 18)
        el, ha = ik(sh, (db[0] - 2, db[1] - 8), LEN['ua'], LEN['fa'], 1)
        side(sc, hip, tor, head=tor + 6, legs=[dict(ankle=an, bend=-1, foot=0)], arms=[dict(pts=(el, ha))])
        db_perp(sc, db, tor - 90)
        if i == 0: sc.arrow((236, 82), (236, 132))
    panels(sc, draw=draw)


@ex('smith-squat', 'Squat à la barre guidée : fesses en arrière, cuisses parallèles au sol')
def _(sc):
    def draw(sc, i):
        an = (197, 205)
        if i == 0: hip = (182, 118); tor = -90
        else: hip = (159, 170); tor = -70
        sh = add(hip, tor, LEN['torso'])
        bar = (177, sh[1] + 2)
        rail(sc, 177)
        el, ha = ik(sh, (bar[0] + 2, bar[1]), LEN['ua'], LEN['fa'], 1)
        side(sc, hip, tor, head=tor + 6, legs=[dict(ankle=an, bend=-1, foot=0)], arms=[dict(pts=(el, ha))])
        bar_end(sc, bar)
        if i == 0: sc.arrow((236, 70), (236, 120))
    panels(sc, draw=draw)


@ex('smith-rdl', 'Soulevé de terre roumain à la barre guidée : dos plat, fesses en arrière')
def _(sc):
    def draw(sc, i):
        an = (166, 204)
        if i == 0: hip = (168, 114); sh = (168, 52); bar = (172, 120)
        else: sh = (178, 112); hip = add(sh, 160, LEN['torso']); bar = (172, 178)
        rail(sc, 172)
        tor = angle(hip, sh)
        side(sc, hip, tor, head=tor + 6, legs=[dict(ankle=an, bend=-1, foot=0)], arms=[dict(hand=bar, bend=1)])
        bar_end(sc, bar)
        if i == 0: sc.arrow((214, 124), (214, 172))
        else: sc.pl([(116, 112), (182, 88)], 'ok', 3, '6 6')
    panels(sc, draw=draw)


@ex('single-leg-rdl', 'Soulevé de terre sur une jambe : buste et jambe arrière à l’horizontale')
def _(sc):
    def draw(sc, i):
        an = (178, 204)
        if i == 0:
            hip = (176, 114); tor = -90
            side(sc, hip, tor, legs=[dict(ankle=(152, 192), bend=-1, foot=60, far=True), dict(ankle=an, bend=-1, foot=0)],
                 arms=[dict(ua=90, fa=88)])
            ha = add(add(add(hip, tor, LEN['torso']), 90, LEN['ua']), 88, LEN['fa'])
        else:
            hip = (170, 120); tor = -8
            side(sc, hip, tor, head=tor, legs=[dict(th=173, sh=172, foot=95, far=True), dict(ankle=an, bend=-1, foot=0)],
                 arms=[dict(ua=90, fa=90)])
            sh = add(hip, tor, LEN['torso']); ha = add(add(sh, 90, LEN['ua']), 90, LEN['fa'])
            sc.pl([(80, 104), (250, 92)], 'ok', 3, '6 6')
        dumbbell_end(sc, (ha[0], ha[1] + 4))
        if i == 0: sc.arrow((214, 70), (250, 104), (246, 72))
    panels(sc, draw=draw)


# ---------- legs, floor ----------
@ex('db-hip-thrust', 'Hip thrust haltère : monte le bassin, serre les fessiers')
def _(sc):
    def draw(sc, i):
        sc.rect(36, 170, 82, 10, 'g', 't', 4)
        sc.pl([(50, 182), (50, 206)], 'g', 6); sc.pl([(104, 182), (104, 206)], 'g', 6)
        sh = (114, 160); an = (226, 204)
        hip = (166, 196) if i == 0 else (176, 162)
        kb = -1 if i == 0 else 1
        tor = angle(hip, sh)
        db = add(hip, -90, 17)
        el, ha = ik(sh, (db[0] - 6, db[1] - 4), LEN['ua'], LEN['fa'], -1)
        side(sc, hip, tor, head=tor - 10, legs=[dict(ankle=an, bend=kb, foot=0)], arms=[dict(pts=(el, ha))])
        sc.circ(db, 11, 'a')
        if i == 0: sc.arrow((150, 156), (150, 108))
        else: sc.pl([(112, 140), (214, 140)], 'ok', 3, '6 6')
    panels(sc, draw=draw)


@ex('lying-leg-curl', 'Leg curl allongé : ramène les talons vers les fesses')
def _(sc):
    def draw(sc, i):
        sc.rect(54, 150, 196, 10, 'g', 't', 4)
        sc.pl([(74, 162), (74, 206)], 'g', 6); sc.pl([(230, 162), (230, 206)], 'g', 6)
        hip = (156, 139); tor = 180
        sh = add(hip, tor, LEN['torso'])
        kn = add(hip, 0, LEN['th'])
        sa = 0 if i == 0 else -104
        rol = add(add(kn, sa, LEN['sh'] - 6), sa - 90, 12)
        sc.pl([(kn[0] + 2, kn[1] + 10), rol], 'g', 5)
        side(sc, hip, tor, head=180, legs=[dict(th=0, sh=sa, foot=sa + 90)], arms=[dict(pts=((sh[0] - 6, sh[1] + 22), (sh[0] - 30, sh[1] + 26)))])
        sc.circ(rol, 10, 'a')
        if i == 0: sc.arrow((268, 116), (222, 72), (266, 74))
    panels(sc, draw=draw)


@ex('assisted-dip-machine', 'Dips assistés à la machine : genoux sur la plateforme')
def _(sc):
    def draw(sc, i):
        sc.rect(286, 8, 16, 200, 'g', 't', 3)
        sc.pl([(112, 118), (112, 206)], 'g', 6); sc.pl([(222, 118), (222, 206)], 'g', 6)
        sc.pl([(100, 116), (234, 116)], 'g', 8)
        if i == 0: sh = (156, 46); tor = -84; arm = dict(hand=(160, 108), bend=1)
        else: sh = (182, 82); tor = -68; arm = dict(pts=((150, 76), (158, 108)))
        hip = add(sh, tor + 180, LEN['torso'])
        kn = add(hip, 92, 44); an = add(kn, 180, 42)
        py = kn[1] + 9
        sc.rect(an[0] - 6, py, 70, 9, 'g', 't', 4)
        sc.pl([(an[0] + 64, py + 4), (294, py + 4)], 'g', 5)
        sc.pl([hip, add(hip, tor, LEN['torso'])], 'k', TW)
        sc.near([hip, kn, an, (an[0] - 4, an[1] - 1)])
        el, ha = (ik(sh, arm['hand'], LEN['ua'], LEN['fa'], 1) if 'hand' in arm else arm['pts'])
        sc.near([sh, el, ha])
        sc.ring(add(sh, tor - 6, 21), LEN['head'] + 3, 't', 3, 'none')
        sc.circ(add(sh, tor - 6, 21), LEN['head'], 'k')
        if i == 0: sc.arrow((214, 44), (214, 90))
    panels(sc, draw=draw)


# ---------- abs (lying, head on the left) ----------
def mat(sc):
    sc.rect(36, 198, 272, 9, 'g', 't', 4)


@ex('weighted-crunch', 'Crunch lesté : haltère contre la poitrine, décolle les épaules')
def _(sc):
    def draw(sc, i):
        mat(sc)
        hip = (176, 187)
        if i == 0: spine = [hip, (140, 187), (114, 187)]; hc = (92, 186); db = (130, 168)
        else: spine = [hip, (142, 186), (120, 166)]; hc = (104, 151); db = (141, 158)
        el, ha = ik(spine[-1], (db[0] - 4, db[1] - 2), LEN['ua'], LEN['fa'], -1)
        side(sc, hip, spine=spine, headpos=hc, legs=[dict(th=-52, sh=62, foot=0)], arms=[dict(pts=(el, ha))])
        sc.circ(db, 10, 'a')
        if i == 0: sc.arrow((72, 166), (88, 130), (66, 140))
    panels(sc, draw=draw)


@ex('bicycle-crunch', 'Crunch vélo : coude vers le genou opposé, puis l’autre côté')
def _(sc):
    def draw(sc, i):
        mat(sc)
        hip = (176, 188)
        spine = [hip, (142, 186), (120, 166)]; hc = (104, 151)
        sh = spine[-1]
        el = (140, 140) if i == 0 else (130, 150); ha = (106, 144)
        bent = dict(th=-118, sh=-8, foot=-8); straight = dict(th=-16, sh=-16, foot=-80)
        legs = [dict(straight, far=True), bent] if i == 0 else [dict(bent, far=True), straight]
        side(sc, hip, spine=spine, headpos=hc, legs=legs, arms=[dict(pts=(el, ha))])
    panels(sc, '1 · Un côté', '2 · L’autre côté', draw=draw)


@ex('reverse-crunch', 'Relevé de bassin : amène les genoux vers la poitrine')
def _(sc):
    def draw(sc, i):
        mat(sc)
        if i == 0:
            hip = (176, 188); spine = [hip, (140, 188), (114, 188)]; hc = (92, 188)
            lg = dict(th=-90, sh=0, foot=-90)
        else:
            hip = (168, 176); spine = [hip, (140, 186), (112, 189)]; hc = (90, 189)
            lg = dict(th=-128, sh=-28, foot=-110)
        sh = spine[-1]
        side(sc, hip, spine=spine, headpos=hc, legs=[lg], arms=[dict(pts=((sh[0] + 30, sh[1] + 6), (sh[0] + 62, sh[1] + 8)))])
        if i == 0: sc.arrow((236, 128), (196, 96), (234, 92))
    panels(sc, draw=draw)


@ex('flutter-kicks', 'Battements de jambes : petits mouvements, bas du dos au sol')
def _(sc):
    def draw(sc, i):
        mat(sc)
        hip = (176, 187); spine = [hip, (140, 187), (116, 184)]; hc = (95, 180)
        hi_, lo = dict(th=-22, sh=-22, foot=-110), dict(th=-8, sh=-8, foot=-96)
        legs = [dict(lo, far=True), hi_] if i == 0 else [dict(hi_, far=True), lo]
        sh = spine[-1]
        side(sc, hip, spine=spine, headpos=hc, legs=legs, arms=[dict(pts=((sh[0] + 30, sh[1] + 8), (sh[0] + 60, sh[1] + 10)))])
        sc.arrow((282, 142), (282, 116)) if i == 0 else sc.arrow((282, 120), (282, 146))
    panels(sc, '1 · Une jambe en haut', '2 · On alterne', draw=draw)


@ex('dead-bug', 'Dead bug : bras et jambe opposés, bas du dos plaqué')
def _(sc):
    def draw(sc, i):
        mat(sc)
        hip = (176, 188); spine = [hip, (140, 188), (114, 188)]; hc = (92, 188)
        sh = spine[-1]
        table = dict(th=-90, sh=0, foot=-90)
        up_arm = dict(pts=((sh[0], sh[1] - 34), (sh[0], sh[1] - 66)))
        if i == 0:
            legs = [dict(table, far=True), table]; arms = [dict(up_arm, far=True), up_arm]
        else:
            legs = [dict(th=-8, sh=-6, foot=-90, far=True), table]
            arms = [dict(up_arm, far=True), dict(pts=((sh[0] - 32, sh[1] - 16), (sh[0] - 62, sh[1] - 26)))]
        side(sc, hip, spine=spine, headpos=hc, legs=legs, arms=arms)
        if i == 0: sc.arrow((104, 110), (54, 150), (60, 112))
    panels(sc, draw=draw)


@ex('side-plank', 'Planche latérale : épaule, hanche et chevilles alignées')
def _(sc):
    def draw(sc, i):
        a = (64, 201)
        if i == 0:
            th = -12.5
            kn = add(a, th, LEN['sh']); hip = add(kn, th, LEN['th']); sh = add(hip, th, LEN['torso'])
        else:
            kn = (107, 197); hip = (152, 196); sh = (212, 168)
        sc.pl([hip, sh], 'k', TW)
        sc.circ(add(sh, -18, 21), LEN['head'], 'k')
        sc.near([hip, kn, a, (58, 206)])
        el = (sh[0], sh[1] + 34); sc.near([sh, el, (el[0] + 22, 204)])
        sc.near([sh, (sh[0], sh[1] - 34), (sh[0], sh[1] - 66)])
        if i == 0: sc.pl([(a[0], a[1] - 24), (sh[0] + 2, sh[1] - 26)], 'ok', 3, '6 6')
        else: sc.pl([(140, 160), (164, 182)], 'bad', 4); sc.pl([(164, 160), (140, 182)], 'bad', 4)
    panels(sc, 'Bonne position', 'À éviter : bassin qui tombe', draw=draw)


ALIAS = {'machine-row-wide': 'machine-row', 'close-grip-db-press': 'db-bench'}
