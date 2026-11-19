"""Third batch of drawings: power, plyometrics, sprint mechanics, prevention and ball work (v3 « Numéro 10 »)."""
import math
from figs import *
from exercises import EX, ex
from ex2 import db_perp, seat, mat, rail, bar_end, scale_from


# ---------------------------------------------------------------- helpers
def rot(p, c, deg):
    r = math.radians(deg); x, y = p[0] - c[0], p[1] - c[1]
    return (c[0] + x * math.cos(r) - y * math.sin(r), c[1] + x * math.sin(r) + y * math.cos(r))


def wall(sc, x, top=12):
    sc.rect(x, top, 14, 206 - top, 'g', 't', 2)


def medball(sc, p, r=12):
    sc.circ(p, r, 'a')


def football(sc, p, r=9):
    sc.ring(p, r, 'k', 3, 't')
    sc.circ(p, 3, 'k')


def plyobox(sc, x0, x1, top):
    sc.rect(x0, top, x1 - x0, 206 - top, 'g', 't', 4)


def cone(sc, x, y=206):
    sc.pl([(x - 8, y), (x, y - 15), (x + 8, y), (x - 8, y)], 'a', 4)


def ffig(sc, c, sy, hy, arms, legs, tilt=0, sw=24):
    """Front view, free limbs. arms: [L, R] each dict(hand=..., bend=..) or dict(el=.., ha=..) (absolute, local coords).
    legs: [L, R] each (knee, ankle, toe) absolute, or None. tilt: upper body lean (degrees, + = top to the right)."""
    ctr = (c, hy)
    R = lambda p: rot(p, ctr, tilt)
    for s, lg in zip((-1, 1), legs):
        if lg: sc.near([(c + s * 11, hy)] + list(lg))
    sc.pl([R(p) for p in [(c - 19, sy + 4), (c + 19, sy + 4), (c + 12, hy), (c - 12, hy), (c - 19, sy + 4), (c + 19, sy + 4)]], 'k', 12)
    sc.pl([R((c, sy + 6)), R((c, hy - 2))], 'k', 26)
    sc.circ(R((c, sy - 22)), LEN['head'], 'k')
    out = []
    for s, a in zip((-1, 1), arms):
        sh = R((c + s * sw, sy + 2))
        if 'hand' in a: el, ha = ik(sh, a['hand'], LEN['ua'], LEN['fa'], a.get('bend', s))
        else: el, ha = a['el'], a['ha']
        sc.near([sh, el, ha]); out.append((sh, el, ha))
    return out


def stand_legs(c, hy, dx=0):
    return [((c - 13 + dx, hy + 46), (c - 14 + dx, hy + 88), (c - 24 + dx, hy + 90)),
            ((c + 13 + dx, hy + 46), (c + 14 + dx, hy + 88), (c + 24 + dx, hy + 90))]


def body(sc, pts, head_ang=None, head=None):
    """generic side figure from explicit joints: pts dict(hip, sh, legs=[(kn, an, ft, far)], arms=[(el, ha, far)])"""
    hip, sh = pts['hip'], pts['sh']
    for kn, an, ft, far in pts.get('legs', []):
        if far: sc.far([hip, kn, an, ft])
    for el, ha, far in pts.get('arms', []):
        if far: sc.far([sh, el, ha])
    sc.pl([hip, sh], 'k', TW)
    hc = head or add(sh, angle(hip, sh) if head_ang is None else head_ang, LEN['head'] + LEN['neck'])
    sc.circ(hc, LEN['head'], 'k')
    for kn, an, ft, far in pts.get('legs', []):
        if not far: sc.near([hip, kn, an, ft])
    for el, ha, far in pts.get('arms', []):
        if not far: sc.near([sh, el, ha])
    return hc


def leg_from(hip, th, sh_, foot):
    kn = add(hip, th, LEN['th']); an = add(kn, sh_, LEN['sh']); ft = add(an, foot, LEN['foot'])
    return kn, an, ft


def arm_from(sh, ua, fa):
    el = add(sh, ua, LEN['ua']); return el, add(el, fa, LEN['fa'])


# ================================================================ HAUT DU CORPS
@ex('mb-chest-throw', 'Lancer de médecine-ball : pousse le ballon contre le mur, à fond')
def _(sc):
    def draw(sc, i):
        wall(sc, 306)
        if i == 0:
            hip = (150, 122); tor = -80
            sh = add(hip, tor, LEN['torso']); ball = (sh[0] + 34, sh[1] + 18)
            arms = [dict(hand=(ball[0] - 10, ball[1] + 4), bend=1)]
            legs = [dict(ankle=(132, 204), bend=-1, foot=0, far=True), dict(ankle=(168, 204), bend=-1, foot=0)]
        else:
            hip = (178, 120); tor = -76
            sh = add(hip, tor, LEN['torso']); el, ha = arm_from(sh, -4, -4); ball = (ha[0] + 13, ha[1])
            arms = [dict(pts=(el, ha))]
            legs = [dict(ankle=(148, 204), bend=-1, foot=-30, far=True), dict(ankle=(212, 204), bend=-1, foot=0)]
        side(sc, hip, tor, head=tor + 6, legs=legs, arms=arms)
        medball(sc, ball)
        if i == 0: sc.arrow((ball[0] + 20, ball[1]), (ball[0] + 76, ball[1]))
        else: sc.arrow((ball[0] + 16, ball[1]), (298, ball[1]))
    panels(sc, 'Ballon contre la poitrine', 'Pousse et avance d’un pas', draw=draw)


@ex('explosive-pushup', 'Pompes explosives : pousse si fort que les mains décollent')
def _(sc):
    def draw(sc, i):
        a = (70, 201)
        th = -4.1 if i == 0 else -27
        kn = add(a, th, LEN['sh']); hip = add(kn, th, LEN['th']); sh = add(hip, th, LEN['torso'])
        if i == 0:
            hand = (212, 204); el, _h = ik(sh, hand, LEN['ua'], LEN['fa'], 1)
        else:
            hand = (sh[0] + 8, sh[1] + 60); el = ((sh[0] + hand[0]) / 2 + 2, (sh[1] + hand[1]) / 2)
        sc.pl([hip, sh], 'k', TW)
        sc.circ(add(sh, th - 8, 21), LEN['head'], 'k')
        sc.near([hip, kn, a, (62, 207)])
        sc.near([sh, el, hand])
        if i == 0: sc.arrow((256, 178), (256, 116))
        else: sc.pl([(hand[0] - 14, 206), (hand[0] + 14, 206)], 'a', 3, '4 5')
    panels(sc, 'En bas, corps gainé', 'Les mains décollent', draw=draw)


@ex('hk-press', 'Développé un bras à genou : pousse sans pencher le buste')
def _(sc):
    def draw(sc, i):
        sc.rect(96, 200, 110, 7, 'g', 't', 3)
        hip = (160, 154); sh = add(hip, -90, LEN['torso'])
        knee_b = (160, 200); an_b = (116, 201); ft_b = (104, 206)
        kn_f = add(hip, 0, LEN['th']); an_f = (kn_f[0] + 2, kn_f[1] + LEN['sh']); ft_f = add(an_f, 0, LEN['foot'])
        if i == 0: el = (sh[0] + 9, sh[1] + 32); ha = (el[0] + 5, el[1] - 32)
        else: el = add(sh, -84, LEN['ua']); ha = add(el, -88, LEN['fa'])
        body(sc, dict(hip=hip, sh=sh, legs=[(kn_f, an_f, ft_f, True), (knee_b, an_b, ft_b, False)], arms=[(el, ha, False)]), head_ang=-90)
        db_perp(sc, (ha[0], ha[1] - 5), angle(el, ha))
        if i == 0: sc.arrow((214, 70), (214, 24))
        else: sc.pl([(hip[0] - 30, 30), (hip[0] - 30, 196)], 'ok', 3, '6 6')
    panels(sc, 'Haltère à l’épaule', 'Bras tendu, buste droit', draw=draw)


@ex('suitcase-carry', 'Marche valise : un haltère lourd d’un côté, reste droit')
def _(sc):
    def draw(sc, i):
        c, sy, hy = 172, 52, 112
        tilt = 0 if i == 0 else 9
        arms = [dict(el=rot((c - 38, sy + 30), (c, hy), tilt), ha=rot((c - 44, sy + 58), (c, hy), tilt)),
                dict(el=rot((c + 27, sy + 36), (c, hy), tilt), ha=rot((c + 29, sy + 68), (c, hy), tilt))]
        ffig(sc, c, sy, hy, arms, stand_legs(c, hy), tilt)
        ha = arms[1]['ha']; sc.circ((ha[0], ha[1] + 8), 11, 'a'); sc.pl([(ha[0] - 3, ha[1] + 8), (ha[0] + 3, ha[1] + 8)], 'a', 5)
        if i == 0: sc.pl([(c - 70, sy + 2), (c + 70, sy + 2)], 'ok', 3, '6 6')
        else:
            sc.pl([rot((c - 70, sy + 2), (c, hy), tilt), rot((c + 70, sy + 2), (c, hy), tilt)], 'bad', 3, '6 6')
            sc.pl([(c + 84, 40), (c + 104, 60)], 'bad', 4); sc.pl([(c + 104, 40), (c + 84, 60)], 'bad', 4)
    panels(sc, 'Épaules à la même hauteur', 'À éviter : pencher vers l’haltère', draw=draw)


@ex('mb-rotation', 'Lancer rotatif : la rotation part des hanches, comme une frappe')
def _(sc):
    def draw(sc, i):
        wall(sc, 34)
        c, sy, hy = 196, 54, 114
        if i == 0:
            hands = (c + 36, hy - 6); ball = (c + 44, hy - 12)
            ffig(sc, c, sy, hy, [dict(hand=hands, bend=-1), dict(hand=hands, bend=1)], stand_legs(c, hy), sw=18)
            sc.arrow((c + 40, hy - 34), (c - 60, sy - 4), (c - 4, sy - 40))
        else:
            hands = (c - 54, sy + 18); ball = (c - 70, sy + 14)
            legs = [((c - 14, hy + 46), (c - 15, hy + 88), (c - 25, hy + 90)), ((c + 8, hy + 46), (c + 16, hy + 84), (c + 24, hy + 90))]
            ffig(sc, c, sy, hy, [dict(hand=hands, bend=-1), dict(hand=hands, bend=1)], legs, sw=14)
            sc.arrow((ball[0] - 16, ball[1]), (54, ball[1]))
        medball(sc, ball)
    panels(sc, 'Ballon à la hanche', 'Tourne et lance contre le mur', draw=draw)


@ex('db-woodchop', 'Bûcheron haltère : de la hanche vers l’épaule opposée')
def _(sc):
    def draw(sc, i):
        c, sy, hy = 172, 58, 118
        legs = [((c - 18, hy + 40), (c - 16, hy + 84), (c - 26, hy + 86)), ((c + 18, hy + 40), (c + 16, hy + 84), (c + 26, hy + 86))]
        if i == 0:
            hands = (c - 34, hy - 4); ffig(sc, c, sy, hy, [dict(hand=hands, bend=-1), dict(hand=hands, bend=1)], legs, sw=16)
            sc.circ((hands[0] - 6, hands[1] + 6), 10, 'a')
            sc.arrow((c - 50, hy - 24), (c + 60, sy - 30), (c - 30, sy - 40))
        else:
            hands = (c + 40, sy - 30); ffig(sc, c, sy, hy, [dict(hand=hands, bend=-1), dict(hand=hands, bend=1)], legs, sw=14)
            sc.circ((hands[0] + 6, hands[1] - 6), 10, 'a')
    panels(sc, 'Haltère près de la hanche', 'En haut, côté opposé', draw=draw)


@ex('shoulder-tap-plank', 'Touches d’épaule : le bassin ne bouge pas')
def _(sc):
    def draw(sc, i):
        a = (70, 201); th = -23.6
        kn = add(a, th, LEN['sh']); hip = add(kn, th, LEN['th']); sh = add(hip, th, LEN['torso'])
        hand = (212, 204); el = ((sh[0] + hand[0]) / 2, (sh[1] + hand[1]) / 2)
        if i == 1: sc.far([sh, el, hand])
        sc.pl([hip, sh], 'k', TW)
        sc.circ(add(sh, th - 8, 21), LEN['head'], 'k')
        sc.near([hip, kn, a, (62, 207)])
        if i == 0: sc.near([sh, el, hand])
        else: sc.near([sh, (sh[0] + 8, sh[1] + 32), (sh[0] - 6, sh[1] + 6)])
        sc.pl([(a[0], a[1] - 26), (sh[0] + 6, sh[1] - 26)], 'ok', 3, '6 6')
        if i == 0: sc.arrow((246, 186), (232, 112), (262, 140))
    panels(sc, 'Planche haute, pieds écartés', 'Une main touche l’épaule', draw=draw)


# ================================================================ BAS DU CORPS, SAUTS
@ex('box-jump', 'Saut sur box : saute, atterris en douceur, redescends en marchant')
def _(sc):
    def draw(sc, i):
        plyobox(sc, 214, 314, 150)
        if i == 0:
            hip = (136, 140); tor = -48
            side(sc, hip, tor, head=tor - 16, legs=[dict(ankle=(146, 204), bend=-1, foot=0)], arms=[dict(ua=120, fa=130)])
            sc.arrow((176, 70), (256, 92), (214, 30))
        else:
            hip = (262, 90); tor = -66
            side(sc, hip, tor, head=tor - 10, legs=[dict(ankle=(268, 146), bend=-1, foot=0)], arms=[dict(ua=-10, fa=-20)])
    panels(sc, 'Quart de squat, bras en arrière', 'Réception souple sur la box', draw=draw)


@ex('cmj', 'Saut vertical : descends vite, saute haut, atterris souple')
def _(sc):
    def draw(sc, i):
        if i == 0:
            hip = (172, 140); tor = -50
            side(sc, hip, tor, head=tor - 16, legs=[dict(ankle=(182, 204), bend=-1, foot=0)], arms=[dict(ua=118, fa=128)])
            sc.arrow((236, 150), (236, 74))
        else:
            n0 = len(sc.items)
            hip = (172, 100); tor = -90
            side(sc, hip, tor, legs=[dict(th=92, sh=94, foot=60)], arms=[dict(ua=-96, fa=-94)])
            scale_from(sc, n0, 0.8, 172, 206)
            sc.pl([(150, 205), (194, 205)], 'a', 3, '4 5')
    panels(sc, 'Descente rapide', 'Bras vers le ciel', draw=draw)


@ex('lateral-step-up', 'Montée latérale : pousse sur la jambe posée sur le banc')
def _(sc):
    def draw(sc, i):
        sc.rect(196, 164, 112, 42, 'g', 't', 4)
        if i == 0:
            c, sy, hy = 160, 60, 120
            legs = [((c - 13, hy + 44), (c - 14, hy + 84), (c - 24, hy + 86)), ((c + 34, hy + 22), (c + 46, hy + 42), (c + 56, hy + 42))]
            arms = [dict(el=(c - 30, sy + 32), ha=(c - 32, sy + 62)), dict(el=(c + 30, sy + 32), ha=(c + 32, sy + 62))]
            ffig(sc, c, sy, hy, arms, legs)
            sc.arrow((c + 80, 136), (c + 80, 84))
        else:
            c, sy, hy = 222, 24, 84
            legs = [((c - 16, hy + 40), (c - 34, hy + 64), (c - 44, hy + 62)), ((c + 13, hy + 40), (c + 14, hy + 76), (c + 24, hy + 78))]
            arms = [dict(el=(c - 30, sy + 32), ha=(c - 32, sy + 62)), dict(el=(c + 30, sy + 32), ha=(c + 32, sy + 62))]
            ffig(sc, c, sy, hy, arms, legs)
        for a in arms: sc.circ((a['ha'][0], a['ha'][1] + 8), 9, 'a')
    panels(sc, 'Un pied sur le banc, de côté', 'Debout sur le banc', draw=draw)


@ex('nordic', 'Nordic : descends le plus lentement possible, corps droit')
def _(sc):
    def draw(sc, i):
        sc.rect(60, 200, 150, 7, 'g', 't', 3)
        sc.pl([(98, 186), (98, 206)], 'g', 5)
        knee = (150, 199); an = (108, 199); ft = (100, 194)
        ang = -90 if i == 0 else -32
        hip = add(knee, ang, LEN['th']); sh = add(hip, ang, LEN['torso'])
        if i == 0:
            el, ha = (sh[0] + 14, sh[1] + 28), (sh[0] + 26, sh[1] + 8)
        else:
            el, ha = ik(sh, (sh[0] + 30, 186), LEN['ua'], LEN['fa'], 1)
        body(sc, dict(hip=hip, sh=sh, legs=[(knee, an, ft, False)], arms=[(el, ha, False)]), head_ang=ang)
        bar_end(sc, (98, 184))
        if i == 0: sc.arrow((196, 52), (262, 150), (256, 70))
        else: sc.pl([add(knee, ang, -6), add(knee, ang, 132)], 'ok', 3, '6 6')
    panels(sc, 'Talons bloqués, corps droit', 'Freine la descente', draw=draw)


def _calf(sc, i, machine=False):
    sc.rect(150, 184, 70, 22, 'g', 't', 3)
    up = 0 if i == 0 else 22
    hip = (176, 104 - up)
    an = (182, 190 - up); ft = (198, 183)
    sh = add(hip, -90, LEN['torso'])
    legs = [dict(ankle=an, bend=-1, foot=angle(an, ft))]
    if machine:
        sc.rect(84, 20, 16, 188, 'g', 't', 3)
        sc.pl([(92, sh[1] - 6), (sh[0] + 22, sh[1] - 6)], 'g', 8)
        arms = [dict(hand=(sh[0] + 20, sh[1] + 2), bend=1)]
    else:
        legs.append(dict(th=100, sh=150, foot=150, far=True))
        sc.pl([(244, 60), (244, 206)], 'g', 5)
        arms = [dict(hand=(240, 98 - up // 2), bend=1)]
    side(sc, hip, -90, legs=legs, arms=arms)
    if i == 0: sc.arrow((228, 176), (228, 132))


@ex('calf-raise-sl', 'Mollets sur une jambe : talon tout en bas, puis tout en haut')
def _(sc):
    panels(sc, 'Talon sous la marche', 'Sur la pointe, 1 seconde', draw=lambda sc, i: _calf(sc, i))


@ex('machine-calf', 'Mollets debout à la machine : monte sur la pointe des pieds')
def _(sc):
    panels(sc, 'Talons en bas', 'Sur la pointe, 1 seconde', draw=lambda sc, i: _calf(sc, i, True))


@ex('seated-calf', 'Mollets assis : genoux sous le coussin, monte les talons')
def _(sc):
    def draw(sc, i):
        seat(sc, back=False)
        sc.rect(168, 196, 52, 10, 'g', 't', 3)
        hip = (112, 160)
        th = 0 if i == 0 else -15
        kn = add(hip, th, LEN['th'])
        sc.rect(kn[0] - 30, kn[1] - 19, 44, 9, 'g', 't', 4)
        side(sc, hip, -90, legs=[dict(th=th, sh=84 if i == 0 else 88, foot=-27 if i == 0 else 15)],
             arms=[dict(hand=(kn[0] - 8, kn[1] - 22), bend=1)])
        if i == 0: sc.arrow((240, 186), (240, 140))
    panels(sc, 'Talons en bas', 'Talons en haut', draw=draw)


# ================================================================ PRÉVENTION, RÉCUP
@ex('copenhagen', 'Copenhague : genou du dessus sur le banc, bassin aligné')
def _(sc):
    def draw(sc, i):
        sc.rect(26, 146, 84, 10, 'g', 't', 4); sc.pl([(40, 158), (40, 206)], 'g', 6); sc.pl([(96, 158), (96, 206)], 'g', 6)
        knee = (100, 142); an = (58, 140); ft = (46, 136)
        sh = (222, 170)
        hip = (160, 156) if i == 1 else (160, 190)
        sc.far([hip, (128, 188), (96, 204), (84, 206)])
        sc.pl([hip, sh], 'k', TW)
        sc.circ(add(sh, -14, 21), LEN['head'], 'k')
        sc.near([hip, knee, an, ft])
        el = (sh[0], sh[1] + 34); sc.near([sh, el, (el[0] + 24, 204)])
        sc.near([sh, (sh[0] - 24, sh[1] - 18), (sh[0] - 50, sh[1] - 16)])
        if i == 1: sc.pl([(knee[0] - 6, knee[1] - 24), (sh[0] + 4, sh[1] - 26)], 'ok', 3, '6 6')
        else: sc.arrow((168, 184), (168, 140))
    panels(sc, 'Départ : bassin au sol', 'Bassin monté, tout aligné', draw=draw)


@ex('single-leg-balance', 'Équilibre sur une jambe : genou souple, 30 secondes')
def _(sc):
    def draw(sc, i):
        hip = (172, 114)
        if i == 1: sc.rect(140, 196, 70, 10, 'a', 't', 5)
        an = (174, 204 if i == 0 else 194)
        arms = [dict(ua=150, fa=170)] if i == 0 else [dict(pts=((hip[0] + 22, hip[1] - 40), (hip[0] - 4, hip[1] - 46)))]
        side(sc, hip, -90, legs=[dict(th=60, sh=170, foot=0, far=True), dict(ankle=an, bend=-1, foot=0)], arms=arms)
    panels(sc, 'Sur une jambe', 'Plus dur : sur un coussin', draw=draw)


@ex('easy-bike', 'Vélo facile : tu peux parler pendant l’effort')
def _(sc):
    def draw(sc, i):
        crank = (182, 168)
        sc.ring((236, 172), 26, 'g', 5, 't')
        sc.pl([(110, 206), (262, 206)], 'g', 8); sc.pl([(136, 206), (160, 112)], 'g', 7); sc.pl([(160, 112), (238, 96), (236, 172)], 'g', 7)
        sc.pl([(140, 108), (176, 108)], 'g', 9)
        sc.pl([(238, 96), (248, 74), (262, 74)], 'g', 7)
        hip = (156, 100); tor = -38
        ang = 70 if i == 0 else 250
        ped = add(crank, ang, 20); ped2 = add(crank, ang + 180, 20)
        sc.pl([ped2, crank, ped], 'g', 5)
        side(sc, hip, tor, head=tor + 10, legs=[dict(ankle=(ped2[0] - 4, ped2[1] - 6), bend=-1, foot=0, far=True), dict(ankle=(ped[0] - 4, ped[1] - 6), bend=-1, foot=0)],
             arms=[dict(hand=(258, 72), bend=1)])
        if i == 0: sc.arrow(add(crank, -40, 36), add(crank, 60, 36), add(crank, 10, 56))
    panels(sc, 'Résistance légère', '20 à 25 min, effort 3/10', draw=draw)


@ex('juggling', 'Jonglages : pied droit, pied gauche, cuisses, tête')
def _(sc):
    def draw(sc, i):
        hip = (150, 114)
        if i == 0:
            side(sc, hip, -88, legs=[dict(ankle=(150, 204), bend=-1, foot=0, far=True), dict(th=40, sh=110, foot=-10)], arms=[dict(ua=110, fa=60)])
            football(sc, (196, 160))
            sc.arrow((214, 156), (214, 84))
        else:
            side(sc, hip, -88, legs=[dict(ankle=(150, 204), bend=-1, foot=0, far=True), dict(ankle=(162, 204), bend=-1, foot=0)], arms=[dict(ua=110, fa=60)])
            football(sc, (200, 70))
            sc.arrow((214, 82), (206, 150), (230, 120))
    panels(sc, 'Touche douce, cheville bloquée', 'Le ballon monte à hauteur de poitrine', draw=draw)


# ================================================================ VITESSE, APPUIS
@ex('pogo', 'Pogo : petits rebonds rapides, jambes presque tendues')
def _(sc):
    def draw(sc, i):
        lift = 0 if i == 0 else 18
        hip = (172, 104 - lift)
        an = (174, 192 - lift)
        side(sc, hip, -90, legs=[dict(ankle=(an[0] - 8, an[1]), bend=-1, foot=62, far=True), dict(ankle=an, bend=-1, foot=62)],
             arms=[dict(ua=100, fa=40)])
        if i == 0: sc.arrow((222, 186), (222, 140))
        else: sc.pl([(150, 205), (198, 205)], 'a', 3, '4 5')
    panels(sc, 'Sur l’avant du pied', 'Contact au sol très court', draw=draw)


@ex('broad-jump', 'Saut en longueur sans élan : bras en arrière, puis saute loin')
def _(sc):
    def draw(sc, i):
        if i == 0:
            hip = (90, 140); tor = -46
            side(sc, hip, tor, head=tor - 16, legs=[dict(ankle=(100, 204), bend=-1, foot=0)], arms=[dict(ua=120, fa=130)])
            sc.arrow((140, 96), (300, 170), (232, 30))
            sc.pl([(76, 207), (76, 186)], 'a', 3)
        else:
            hip = (256, 146); tor = -54
            side(sc, hip, tor, head=tor - 10, legs=[dict(ankle=(268, 204), bend=-1, foot=0)], arms=[dict(ua=-30, fa=-20)])
            sc.pl([(36, 207), (36, 186)], 'a', 3); sc.pl([(36, 196), (258, 196)], 'a', 2, '5 6')
    panels(sc, 'Bras en arrière, quart de squat', 'Réception tenue 2 secondes', draw=draw)


@ex('skater', 'Patineur : bondis sur le côté et stabilise sur une jambe')
def _(sc):
    def draw(sc, i):
        if i == 0:
            c, sy, hy = 236, 70, 128
            legs = [((c - 30, hy + 30), (c - 52, hy + 50), (c - 60, hy + 44)), ((c + 16, hy + 40), (c + 10, hy + 76), (c + 20, hy + 78))]
            ffig(sc, c, sy, hy, [dict(el=(c - 36, sy + 18), ha=(c - 54, sy + 34)), dict(el=(c + 30, sy + 30), ha=(c + 44, sy + 54))], legs, tilt=-8)
            sc.arrow((c - 60, sy + 60), (70, 150), (130, 40))
        else:
            c, sy, hy = 100, 70, 128
            legs = [((c - 16, hy + 40), (c - 10, hy + 76), (c - 20, hy + 78)), ((c + 30, hy + 30), (c + 52, hy + 50), (c + 60, hy + 44))]
            ffig(sc, c, sy, hy, [dict(el=(c - 30, sy + 30), ha=(c - 44, sy + 54)), dict(el=(c + 36, sy + 18), ha=(c + 54, sy + 34))], legs, tilt=8)
            sc.pl([(c - 10, 52), (c - 10, 206)], 'ok', 3, '6 6')
    panels(sc, 'Pousse fort sur le côté', 'Genou au-dessus du pied', draw=draw)


@ex('bounds', 'Foulées bondissantes : grands bonds, genou haut')
def _(sc):
    def draw(sc, i):
        if i == 0:
            hip = (150, 120); tor = -76
            kn_r, an_r, ft_r = leg_from(hip, 110, 132, 70)
            kn_f, an_f, ft_f = leg_from(hip, -10, 80, 0)
            sh = add(hip, tor, LEN['torso'])
            body(sc, dict(hip=hip, sh=sh, legs=[(kn_f, an_f, ft_f, True), (kn_r, an_r, ft_r, False)],
                          arms=[arm_from(sh, -20, -70) + (False,), arm_from(sh, 130, 60) + (True,)]), head_ang=tor + 8)
            sc.arrow((210, 100), (300, 150), (270, 70))
        else:
            hip = (200, 96); tor = -78
            kn_r, an_r, ft_r = leg_from(hip, 130, 170, 80)
            kn_f, an_f, ft_f = leg_from(hip, -14, 70, 0)
            sh = add(hip, tor, LEN['torso'])
            body(sc, dict(hip=hip, sh=sh, legs=[(kn_r, an_r, ft_r, True), (kn_f, an_f, ft_f, False)],
                          arms=[arm_from(sh, 140, 70) + (False,), arm_from(sh, -20, -70) + (True,)]), head_ang=tor + 8)
            sc.pl([(60, 200), (110, 150), (150, 140)], 'a', 2, '5 6')
    panels(sc, 'Poussée complète', 'En l’air, genou haut', draw=draw)


@ex('drop-jump', 'Drop jump : tombe de la box, rebondis aussitôt')
def _(sc):
    def draw(sc, i):
        plyobox(sc, 40, 120, 174)
        if i == 0:
            n0 = len(sc.items)
            hip = (92, 82)
            side(sc, hip, -88, legs=[dict(ankle=(90, 170), bend=-1, foot=0, far=True), dict(th=60, sh=100, foot=0)], arms=[dict(ua=100, fa=80)])
            scale_from(sc, n0, 0.85, 92, 172)
            sc.arrow((150, 126), (178, 196), (150, 172))
            sc.arrow((196, 196), (224, 110), (204, 130))
        else:
            n0 = len(sc.items)
            hip = (216, 100)
            side(sc, hip, -90, legs=[dict(th=92, sh=94, foot=60)], arms=[dict(ua=-96, fa=-94)])
            scale_from(sc, n0, 0.8, 216, 206)
            sc.pl([(196, 205), (240, 205)], 'a', 3, '4 5')
    panels(sc, 'Un pas dans le vide', 'Contact court, rebond haut', draw=draw)


def _runner(sc, hip, tor, front_th, front_sh, back_th, back_sh, arm_f=(-40, -100), arm_b=(140, 70), far_front=True, foot_b=60):
    kn_f, an_f, ft_f = leg_from(hip, front_th, front_sh, 0)
    kn_b, an_b, ft_b = leg_from(hip, back_th, back_sh, foot_b)
    sh = add(hip, tor, LEN['torso'])
    legs = [(kn_f, an_f, ft_f, far_front), (kn_b, an_b, ft_b, not far_front)]
    arms = [arm_from(sh, *arm_f) + (not far_front,), arm_from(sh, *arm_b) + (far_front,)]
    body(sc, dict(hip=hip, sh=sh, legs=legs, arms=arms), head_ang=tor + 6)
    return sh


@ex('starts-10', 'Départ : penché vers l’avant, pousse fort dans le sol')
def _(sc):
    def draw(sc, i):
        cone(sc, 40)
        if i == 0:
            hip = (128, 136); tor = -42
            kn_f, an_f, ft_f = leg_from(hip, 40, 98, 0)
            sh = add(hip, tor, LEN['torso'])
            body(sc, dict(hip=hip, sh=sh, legs=[(kn_f, an_f, ft_f, False), leg_from(hip, 108, 122, 30) + (True,)],
                          arms=[arm_from(sh, 110, 60) + (False,), arm_from(sh, 40, -40) + (True,)]), head_ang=tor + 4)
            sc.arrow((210, 120), (290, 120))
        else:
            _runner(sc, (180, 124), -48, -6, 70, 126, 136, arm_f=(10, -70), arm_b=(150, 90))
            sc.pl([(110, 206), (240, 104)], 'ok', 3, '6 6')
    panels(sc, 'Un pied devant, buste penché', 'Corps penché, genou qui monte', draw=draw)


@ex('hill-sprint', 'Sprint en côte : buste penché, genoux hauts')
def _(sc):
    def draw(sc, i):
        sc.pl([(14, 214), (334, 150)], 'g', 6)
        if i == 0: _runner(sc, (150, 118), -60, -20, 60, 118, 130, arm_f=(0, -80), arm_b=(140, 80))
        else: _runner(sc, (210, 104), -60, -24, 60, 120, 132, arm_f=(0, -80), arm_b=(140, 80), far_front=False)
        if i == 0: sc.arrow((236, 120), (306, 96))
    panels(sc, 'Pousse dans la pente', 'Bras puissants', draw=draw)


@ex('decel', 'Freinage : petits pas, hanches basses, arrêt en 3 appuis')
def _(sc):
    def draw(sc, i):
        if i == 0:
            _runner(sc, (130, 108), -78, -30, 70, 130, 150, arm_f=(-20, -90), arm_b=(140, 70))
            sc.arrow((190, 100), (270, 100))
        else:
            hip = (190, 144); tor = -98
            sh = add(hip, tor, LEN['torso'])
            body(sc, dict(hip=hip, sh=sh, legs=[(add(hip, 30, LEN['th']), (226, 204), (242, 206), False),
                                                 (add(hip, 100, LEN['th']), (160, 204), (176, 206), True)],
                          arms=[arm_from(sh, 40, -10) + (False,), arm_from(sh, 60, 10) + (True,)]), head_ang=-84)
            for x in (96, 128, 160):
                sc.pl([(x, 207), (x + 12, 207)], 'a', 4)
    panels(sc, 'Sprint', 'Freinage : hanches basses, pieds devant', draw=draw)
