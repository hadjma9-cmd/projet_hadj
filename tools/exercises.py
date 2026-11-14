from figs import *

EX = {}
def ex(slug, title):
    def deco(fn):
        def build():
            sc = Scene(slug, title); fn(sc); return sc
        EX[slug] = build; return build
    return deco

# ---------------- HAUT 1 ----------------
@ex('chest-press', 'Développé pecs à la machine : pousse les poignées devant toi')
def _(sc):
    def draw(sc, i):
        # machine
        sc.rect(30, 22, 14, 186, 'g', 't', 3)
        sc.pl([(37, 26), (150, 26)], 'g', 6)
        sc.pl([(84, 176), (140, 176)], 'g', 9)       # seat
        sc.pl([(112, 182), (112, 206)], 'g', 6)
        sc.pl([(84, 166), (70, 82)], 'g', 9)         # backrest
        sc.pl([(44, 150), (76, 150)], 'g', 5)
        hip = (104, 160)
        hand = (136, 112) if i == 0 else (164, 106)
        sc.pl([(150, 26), (hand[0], hand[1]-12)], 'g', 5)
        J = side(sc, hip, -99, head=-92,
                 legs=[dict(th=0, sh=86, foot=0)],
                 arms=[dict(hand=hand, bend=1)])
        h = J['arms'][0][2]
        sc.pl([(h[0], h[1]-13), (h[0], h[1]+13)], 'a', 7)
        if i == 0: sc.arrow((158, 112), (206, 108))
    panels(sc, draw=draw)

@ex('shoulder-press', 'Développé épaules haltères assis : pousse au-dessus de la tête')
def _(sc):
    def draw(sc, i):
        c, hy = 172, 148; sy = hy-60
        sc.rect(c-26, sy-34, 52, 96, 'g', 't', 8)     # backrest
        sc.rect(c-40, hy+2, 80, 12, 'g', 't', 5)       # seat
        sc.pl([(c, hy+16), (c, 206)], 'g', 6)
        a = dict(el=(50, 20), ha=(52, -12)) if i == 0 else dict(el=(36, -30), ha=(30, -62))
        arms = front(sc, c, sy, a, 'seated', hy)
        for sh, el, ha in arms: dumbbell_h(sc, (ha[0], ha[1]-4))
        if i == 0:
            sc.arrow((c+92, sy-10), (c+92, sy-58)); sc.arrow((c-92, sy-10), (c-92, sy-58))
    panels(sc, draw=draw)

@ex('incline-pushup', 'Pompes mains surélevées : le corps reste droit comme une planche')
def _(sc):
    def draw(sc, i):
        sc.rect(206, 164, 104, 11, 'g', 't', 5)
        sc.pl([(220, 177), (220, 206)], 'g', 6); sc.pl([(296, 177), (296, 206)], 'g', 6)
        an = (92, 192); th = 38 if i == 0 else 21
        kn = add(an, -th, LEN['sh']); hip = add(kn, -th, LEN['th'])
        hand = (224, 158)
        sh = add(hip, -th, LEN['torso'])
        el, ha = ik(sh, hand, LEN['ua'], LEN['fa'], -1)
        sc.pl([hip, sh], 'k', TW)
        sc.circ(add(sh, -th-6, 21), LEN['head'], 'k')
        sc.near([hip, kn, an, (86, 203)])
        sc.near([sh, el, ha])
        if i == 0: sc.arrow((262, 92), (272, 132), (276, 108))
        else: sc.text('cue-pushup', (150, 96), 'Poitrine près du banc', 14, None, 'q', 'middle')
    panels(sc, draw=draw)

@ex('lateral-raise', 'Élévations latérales : monte les bras sur les côtés jusqu’aux épaules')
def _(sc):
    def draw(sc, i):
        c, hy = 172, 112; sy = hy-60
        a = dict(el=(29, 36), ha=(31, 68)) if i == 0 else dict(el=(57, 8), ha=(88, 12))
        arms = front(sc, c, sy, a, 'stand', hy)
        for sh, el, ha in arms: dumbbell_end(sc, (ha[0], ha[1]+ (8 if i == 0 else 2)))
        if i == 0:
            sc.arrow((c+52, sy+70), (c+100, sy+24), (c+96, sy+60)); sc.arrow((c-52, sy+70), (c-100, sy+24), (c-96, sy+60))
        else:
            sc.pl([(c-110, sy+2), (c+110, sy+2)], 'a', 2, '5 5')
    panels(sc, draw=draw)

@ex('triceps-pushdown', 'Extension triceps à la poulie : les coudes restent collés au corps')
def _(sc):
    def draw(sc, i):
        sc.rect(270, 14, 16, 194, 'g', 't', 3)
        sc.pl([(248, 22), (278, 22)], 'g', 5); sc.ring((246, 24), 7, 'g', 3, 't')
        hip = (150, 114)
        sh = add(hip, -82, LEN['torso'])
        el = add(sh, 84, LEN['ua'])
        ha = add(el, -38 if i == 0 else 78, LEN['fa'])
        sc.pl([(246, 30), ha], 'g', 2)
        J = side(sc, hip, -82, head=-76, legs=[dict(ankle=(150, 202), bend=-1, foot=0)], arms=[dict(pts=(el, ha))])
        sc.pl([ha, add(ha, 70 if i == 0 else 95, 13)], 'a', 6)
        if i == 0: sc.arrow((204, 78), (190, 124), (208, 106))
        sc.ring(el, 15, 'a', 2, 'none')
    panels(sc, draw=draw)

@ex('plank', 'Planche : tiens la position, épaules, hanches et chevilles alignées')
def _(sc):
    def draw(sc, i):
        if i == 0:
            an = (66, 192); th = 11
            kn = add(an, -th, LEN['sh']); hip = add(kn, -th, LEN['th']); sh = add(hip, -th, LEN['torso'])
        else:
            an = (66, 193); hip = (154, 194); kn = (110, 194); sh = (212, 166)
        el = (sh[0]+2, 199); ha = (el[0]+32, 199)
        sc.pl([hip, sh], 'k', TW)
        sc.circ(add(sh, -8, 22), LEN['head'], 'k')
        sc.near([hip, kn, an, (60, 203)])
        sc.near([sh, el, ha])
        if i == 0:
            sc.pl([(an[0], an[1]-24), (sh[0]+6, sh[1]-26)], 'ok', 3, '6 6')
        else:
            sc.arrow((154, 150), (154, 176), None, 'bad') if False else None
            sc.pl([(142, 150), (166, 172)], 'bad', 4); sc.pl([(166, 150), (142, 172)], 'bad', 4)
    panels(sc, 'Bonne position', 'À éviter : bassin qui tombe', draw=draw)

# ---------------- HAUT 2 ----------------
@ex('lat-pulldown', 'Tirage vertical : amène la barre vers le haut de la poitrine')
def _(sc):
    def draw(sc, i):
        c, hy = 172, 148; sy = hy-60
        sc.rect(c-36, hy+14, 72, 12, 'g', 't', 5)
        sc.pl([(c, hy+28), (c, 206)], 'g', 6)
        by = sy-62 if i == 0 else sy+2
        sc.pl([(c, 0), (c, by)], 'g', 2)
        if i == 0:
            arms = front(sc, c, sy, dict(hand=(52, -60), bend=-1), 'seated', hy)
            sc.pl([(c-84, by+7), (c-66, by), (c+66, by), (c+84, by+7)], 'a', 6)
        else:
            arms = front(sc, c, sy, dict(hand=(50, 2), bend=1), 'seated', hy)
            sc.pl([(c-84, by+7), (c-66, by), (c+66, by), (c+84, by+7)], 'a', 6)
            for sh, el, ha in arms: sc.circ(ha, 6, 'k')
        sc.rect(c-38, hy+2, 76, 11, 'g', 't', 5)       # thigh pad
        if i == 0:
            sc.arrow((c+112, sy-52), (c+112, sy-4)); sc.arrow((c-112, sy-52), (c-112, sy-4))
    panels(sc, draw=draw)

@ex('seated-row', 'Tirage horizontal assis : tire la poignée vers le nombril, dos droit')
def _(sc):
    def draw(sc, i):
        sc.pl([(58, 176), (176, 176)], 'g', 9)
        sc.pl([(76, 182), (76, 206)], 'g', 6); sc.pl([(160, 182), (160, 206)], 'g', 6)
        sc.pl([(196, 142), (204, 190)], 'g', 7); sc.pl([(202, 190), (202, 206)], 'g', 6)
        sc.rect(286, 60, 16, 148, 'g', 't', 3); sc.ring((280, 122), 7, 'g', 3, 't')
        hip = (98, 160); tor = -86 if i == 0 else -93
        sh = add(hip, tor, LEN['torso'])
        hand = (sh[0]+63, 118) if i == 0 else (sh[0]+22, 122)
        sc.pl([(280, 122), hand], 'g', 2)
        J = side(sc, hip, tor, head=-90, legs=[dict(ankle=(184, 168), bend=-1, foot=-78)],
                 arms=[dict(hand=hand, bend=1)])
        h = J['arms'][0][2]
        sc.pl([(h[0]+2, h[1]-10), (h[0]+2, h[1]+10)], 'a', 7)
        if i == 0: sc.arrow((258, 98), (208, 98))
    panels(sc, draw=draw)

@ex('face-pull', 'Face pull : tire la corde vers le front, coudes hauts et écartés')
def _(sc):
    def draw(sc, i):
        if i == 0:
            sc.rect(286, 14, 16, 194, 'g', 't', 3); sc.ring((280, 52), 7, 'g', 3, 't')
            hip = (140, 114); sh = add(hip, -90, LEN['torso'])
            el, ha = ik(sh, (sh[0]+64, sh[1]+4), LEN['ua'], LEN['fa'], 1)
            sc.pl([(280, 52), ha], 'g', 2)
            side(sc, hip, -90, legs=[dict(ankle=(132, 202), bend=-1, foot=0, far=True), dict(ankle=(152, 202), bend=-1, foot=0)],
                 arms=[dict(pts=(el, ha))])
            sc.pl([ha, add(ha, 0, 14)], 'a', 6)
            sc.arrow((250, 34), (204, 32))
        else:
            c, hy = 172, 112; sy = hy-60
            arms = front(sc, c, sy, dict(el=(58, 0), ha=(50, -32)), 'stand', hy)
            for s_, (sh, el, ha) in zip((-1, 1), arms):
                sc.pl([ha, (ha[0]-s_*16, ha[1]+3)], 'a', 6)
            sc.pl([(c-112, sy+2), (c+112, sy+2)], 'a', 2, '5 5')
            sc.text('cue-facepull', (c+104, 132), 'Mains à hauteur', 14, None, 'q', 'middle')
            sc.text('cue-facepull-2', (c+104, 150), 'des oreilles', 14, None, 'q', 'middle')
    panels(sc, '1 · Départ (de profil)', '2 · Arrivée (de face)', draw=draw)

@ex('biceps-curl', 'Curl biceps haltères : seul l’avant-bras bouge')
def _(sc):
    def draw(sc, i):
        hip = (160, 114); sh = add(hip, -90, LEN['torso'])
        el = add(sh, 88, LEN['ua']); ha = add(el, 82 if i == 0 else -66, LEN['fa'])
        J = side(sc, hip, -90, legs=[dict(ankle=(160, 202), bend=-1, foot=0)], arms=[dict(pts=(el, ha))])
        dumbbell_end(sc, add(ha, 82 if i == 0 else -66, 4))
        if i == 0: sc.arrow((190, 116), (192, 64), (212, 90))
        sc.ring(el, 15, 'a', 2, 'none')
    panels(sc, draw=draw)

@ex('leg-raise', 'Relevé de jambes allongé : monte les jambes, le bas du dos reste au sol')
def _(sc):
    def draw(sc, i):
        sc.rect(36, 198, 272, 9, 'g', 't', 4)
        hip = (150, 187); sh = (88, 187)
        a = -4 if i == 0 else -86
        J = side(sc, hip, 180, legs=[dict(th=a, sh=a, foot=a-88)],
                 arms=[dict(pts=((120, 190), (152, 192)))])
        if i == 0: sc.arrow((246, 160), (186, 96), (238, 108))
    panels(sc, draw=draw)

# ---------------- BAS ----------------
@ex('leg-press', 'Presse à cuisses : pousse la plateforme sans verrouiller les genoux')
def _(sc):
    def draw(sc, i):
        hip = (112, 176); tor = -142
        u = dv(tor); nb = dv(tor+90); nb = (-nb[0], -nb[1]) if nb[1] < 0 else nb   # behind/back side (down)
        b0 = (hip[0]+nb[0]*17+8, hip[1]+nb[1]*17+6); b1 = (b0[0]+u[0]*98, b0[1]+u[1]*98)
        sc.pl([b0, b1], 'g', 9)
        sc.pl([b0, (b0[0]+34, b0[1]+8)], 'g', 9)
        rail = -42
        r0 = (146, 204); sc.pl([r0, add(r0, rail, 190)], 'g', 6)
        ank = add(hip, rail, 54 if i == 0 else 85)
        pc = add(ank, rail, 9)
        p0 = add(pc, rail-90, 34); p1 = add(pc, rail+90, 30)
        sc.pl([p1, add(p1, rail+90, 14)], 'g', 6)
        sc.ring(add(pc, rail, 24), 15, 'a', 6, 't')
        J = side(sc, hip, tor, legs=[dict(ankle=ank, bend=-1, foot=rail-90)],
                 arms=[dict(hand=(hip[0]+4, hip[1]+10), bend=-1)])
        sc.pl([p0, p1], 'a', 7)
        if i == 0:
            s = add(pc, rail-90, 56); sc.arrow(add(s, rail, 4), add(s, rail, 44))
    panels(sc, draw=draw)

@ex('rdl', 'Soulevé de terre roumain : pousse les fesses en arrière, dos plat')
def _(sc):
    def draw(sc, i):
        if i == 0:
            hip = (160, 114); J = side(sc, hip, -90, legs=[dict(ankle=(160, 202), bend=-1, foot=0)], arms=[dict(ua=86, fa=84)])
            ha = J['arms'][0][2]; dumbbell_end(sc, (ha[0]+2, ha[1]+4))
            sc.arrow((196, 118), (196, 162))
            sc.arrow((128, 116), (92, 116))
            sc.text('cue-rdl-hips', (84, 98), 'Fesses en arrière', 14, None, 'q', 'middle')
        else:
            hip = (128, 122); tor = -27
            J = side(sc, hip, tor, head=-14, legs=[dict(ankle=(156, 202), bend=-1, foot=0)], arms=[dict(ua=90, fa=90)])
            ha = J['arms'][0][2]; dumbbell_end(sc, (ha[0], ha[1]+4))
            sh = J['sh']
            sc.pl([(hip[0]-6, hip[1]-24), (sh[0]+2, sh[1]-24)], 'ok', 3, '6 6')
            sc.text('cue-rdl', (200, 46), 'Dos plat, genoux à peine fléchis', 14, None, 'q', 'middle')
    panels(sc, draw=draw)

@ex('reverse-lunge', 'Fentes arrière : un grand pas en arrière, puis remonte')
def _(sc):
    def draw(sc, i):
        if i == 0:
            hip = (190, 114); J = side(sc, hip, -90, legs=[dict(ankle=(190, 202), bend=-1, foot=0)], arms=[dict(ua=90, fa=88)])
            ha = J['arms'][0][2]; dumbbell_end(sc, (ha[0], ha[1]+4))
            sc.arrow((166, 150), (112, 192), (124, 150))
        else:
            hip = (150, 156)
            J = side(sc, hip, -88, legs=[dict(th=108, sh=190, foot=110, far=True), dict(th=2, sh=91, foot=0)], arms=[dict(ua=90, fa=88)])
            ha = J['arms'][0][2]; dumbbell_end(sc, (ha[0], ha[1]+4))
            sc.text('cue-lunge', (244, 120), 'Genou avant', 14, None, 'q', 'middle')
            sc.text('cue-lunge-2', (244, 138), 'au-dessus du pied', 14, None, 'q', 'middle')
    panels(sc, draw=draw)

@ex('leg-curl', 'Leg curl assis : ramène les talons sous le siège')
def _(sc):
    def draw(sc, i):
        sc.rect(84, 150, 30, 58, 'g', 't', 4)
        sc.pl([(84, 146), (150, 146)], 'g', 9)
        sc.pl([(84, 136), (68, 52)], 'g', 9)
        hip = (104, 130); kn = add(hip, 0, LEN['th'])
        sa = 8 if i == 0 else 114
        an = add(kn, sa, LEN['sh'])
        rol = add(add(kn, sa, LEN['sh']-4), sa+90, 16)
        sc.pl([(kn[0], kn[1]+10), rol], 'g', 5)
        J = side(sc, hip, -100, head=-92, legs=[dict(th=0, sh=sa, foot=sa-82)], arms=[dict(hand=(118, 142), bend=1)])
        sc.circ(rol, 10, 'a')
        sc.rect(124, 104, 32, 11, 'g', 't', 5)
        if i == 0: sc.arrow((204, 164), (150, 196), (196, 196))
    panels(sc, draw=draw)

# ---------------- HAUT 3 ----------------
@ex('incline-press', 'Développé incliné haltères : pousse les haltères vers le plafond')
def _(sc):
    def draw(sc, i):
        hip = (166, 160); tor = -146
        u = dv(tor); nb = (-math.sin(math.radians(tor))*-1, math.cos(math.radians(tor))*-1)
        nb = dv(tor-90)   # behind the back (down-left)
        b0 = (hip[0]+nb[0]*17, hip[1]+nb[1]*17); b1 = (b0[0]+u[0]*96, b0[1]+u[1]*96)
        sc.pl([b0, b1], 'g', 9)
        sc.pl([(b0[0]+6, b0[1]+2), (b0[0]+48, b0[1]+2)], 'g', 9)
        mid = (b0[0]+u[0]*56, b0[1]+u[1]*56)
        sc.pl([mid, (mid[0], 206)], 'g', 6); sc.pl([(b0[0]+30, b0[1]+8), (b0[0]+30, 206)], 'g', 6)
        sh = add(hip, tor, LEN['torso'])
        if i == 0: el = add(sh, 58, LEN['ua']); ha = add(el, -92, LEN['fa'])
        else: el = add(sh, -88, LEN['ua']); ha = add(el, -90, LEN['fa'])
        J = side(sc, hip, tor, legs=[dict(th=-6, sh=84, foot=0)], arms=[dict(pts=(el, ha))])
        dumbbell_end(sc, (ha[0], ha[1]-4))
        if i == 0: sc.arrow((ha[0]+26, ha[1]-8), (ha[0]+26, ha[1]-56))
    panels(sc, draw=draw)

@ex('dips', 'Dips : descends jusqu’à avoir les coudes à angle droit, puis pousse')
def _(sc):
    def draw(sc, i):
        sc.pl([(112, 118), (112, 206)], 'g', 6); sc.pl([(222, 118), (222, 206)], 'g', 6)
        sc.pl([(100, 116), (234, 116)], 'g', 8)
        if i == 0:
            sh = (156, 44); tor = -84; th, shn = 86, 160
            arm = dict(hand=(160, 108), bend=1)
        else:
            sh = (182, 82); tor = -68; th, shn = 92, 172
            arm = dict(pts=((150, 76), (158, 108)))
        hip = add(sh, tor+180, LEN['torso'])
        side(sc, hip, tor, head=tor+10, legs=[dict(th=th, sh=shn, foot=shn+20)], arms=[arm])
        if i == 0: sc.arrow((212, 44), (212, 88))
        else: sc.text('cue-dips', (86, 40), 'Buste un peu penché', 14, None, 'q', 'middle')
    panels(sc, draw=draw)

@ex('crunch', 'Crunch : décolle les épaules, les mains glissent vers les genoux')
def _(sc):
    def draw(sc, i):
        sc.rect(36, 198, 272, 9, 'g', 't', 4)
        hip = (176, 187)
        if i == 0:
            spine = [hip, (140, 187), (114, 187)]; hc = (92, 186); arm = dict(hand=(176, 170), bend=-1)
        else:
            spine = [hip, (142, 186), (120, 166)]; hc = (104, 151); arm = dict(hand=(186, 150), bend=-1)
        side(sc, hip, spine=spine, headpos=hc, legs=[dict(th=-52, sh=62, foot=0)], arms=[arm])
        if i == 0: sc.arrow((72, 166), (88, 130), (66, 140))
    panels(sc, draw=draw)

# ---------------- REMPLACEMENTS (sans poulie, sans fentes) ----------------
@ex('assisted-pullup', 'Tractions assistées : tire jusqu’au menton au-dessus des poignées')
def _(sc):
    def draw(sc, i):
        sc.rect(286, 8, 16, 200, 'g', 't', 3)
        sc.pl([(206, 30), (294, 30)], 'g', 6)
        if i == 0:
            hand = (204, 30); sh = (180, 92); padY = 194
        else:
            hand = (210, 30); sh = (180, 42); padY = 144
        hip = add(sh, 92, LEN['torso'])
        kn = (hip[0]+22, hip[1]+40); an = (kn[0]-44, kn[1]+1)
        sc.rect(146, padY+5, 78, 9, 'g', 't', 4)
        sc.pl([(224, padY+9), (294, padY+9)], 'g', 5)
        sc.pl([hip, add(hip, -88, LEN['torso'])], 'k', TW)
        sc.near([hip, kn, an, (an[0]-4, an[1]-1)])
        el, ha = ik(sh, hand, LEN['ua'], LEN['fa'], 1)
        sc.near([sh, el, ha])
        sc.ring(add(sh, -100, 22), LEN['head']+3, 't', 3, 'none')
        sc.circ(add(sh, -100, 22), LEN['head'], 'k')
        sc.pl([(ha[0]-3, ha[1]), (ha[0]+15, ha[1])], 'a', 7)
        if i == 0: sc.arrow((248, 150), (248, 102))
    panels(sc, draw=draw)

@ex('db-row', 'Rowing haltère un bras : tire l’haltère vers la hanche, dos plat')
def _(sc):
    def draw(sc, i):
        sc.rect(46, 168, 160, 9, 'g', 't', 4)
        sc.pl([(64, 179), (64, 206)], 'g', 6); sc.pl([(188, 179), (188, 206)], 'g', 6)
        hip = (104, 122); sh = (166, 110)
        sc.far([hip, (100, 164), (56, 165)])
        sc.far([sh, (172, 138), (176, 164)])
        sc.pl([hip, sh], 'k', TW)
        sc.circ((188, 103), LEN['head'], 'k')
        kn, an = ik(hip, (122, 204), LEN['th'], LEN['sh'], -1)
        sc.near([hip, kn, an, (139, 204)])
        if i == 0: el = (166, 142); ha = (167, 174)
        else: el = (134, 98); ha = (136, 130)
        sc.near([sh, el, ha])
        dumbbell_end(sc, (ha[0], ha[1]+3))
        if i == 0: sc.arrow((214, 150), (214, 108))
        else: sc.pl([(96, 92), (170, 80)], 'ok', 3, '6 6')
    panels(sc, draw=draw)

@ex('rear-fly', 'Oiseau à la machine : écarte les bras vers l’arrière (vu de dessus)')
def _(sc):
    def draw(sc, i):
        c = 172
        sc.rect(c-26, 128, 52, 46, 'g', 't', 8)        # siège
        sc.rect(c-30, 82, 60, 12, 'g', 't', 6)         # coussin poitrine
        sc.pl([(c, 94), (c, 60)], 'g', 6)              # axe machine
        L, R = (c-24, 116), (c+24, 116)
        if i == 0: hl, hr = (c-10, 52), (c+10, 52)
        else: hl, hr = (c-92, 112), (c+92, 112)
        for sh, h in ((L, hl), (R, hr)):
            el = ((sh[0]+h[0])/2, (sh[1]+h[1])/2)
            sc.near([sh, el, h])
            sc.pl([(h[0]-9, h[1]), (h[0]+9, h[1])] if i == 1 else [(h[0], h[1]-9), (h[0], h[1]+9)], 'a', 7)
        sc.pl([L, R], 'k', 22)
        sc.circ((c, 112), 15, 'k')
        if i == 0:
            sc.arrow((c-34, 46), (c-96, 92), (c-80, 44)); sc.arrow((c+34, 46), (c+96, 92), (c+80, 44))
    panels(sc, '1 · Départ (vu de dessus)', '2 · Arrivée (vu de dessus)', draw=draw)

@ex('overhead-ext', 'Extension triceps haltère au-dessus de la tête : seuls les avant-bras bougent')
def _(sc):
    def draw(sc, i):
        sc.pl([(84, 176), (140, 176)], 'g', 9)
        sc.pl([(112, 182), (112, 206)], 'g', 6)
        sc.pl([(84, 166), (78, 92)], 'g', 9)
        hip = (104, 160)
        J = side(sc, hip, -91, head=-90, legs=[dict(th=0, sh=88, foot=0)], arms=[])
        sh = J['sh']
        el = (sh[0]+12, sh[1]-32)
        ha = (el[0]-29, el[1]+14) if i == 0 else (el[0]+3, el[1]-32)
        sc.near([sh, el, ha])
        dumbbell_end(sc, (ha[0], ha[1]+(4 if i == 0 else -4)), 11)
        sc.ring(el, 15, 'a', 2, 'none')
        if i == 0: sc.arrow((152, 92), (152, 44), (166, 66))
    panels(sc, draw=draw)

@ex('step-up', 'Montées sur banc : pousse sur le pied posé sur le banc pour monter')
def _(sc):
    save = dict(LEN); 
    for k in LEN: LEN[k] = LEN[k]*0.8
    try:
        def draw(sc, i):
            sc.rect(176, 168, 120, 40, 'g', 't', 4)
            if i == 0:
                hip = (150, 136)
                J = side(sc, hip, -89, legs=[dict(ankle=(150, 204), bend=-1, foot=0, far=True), dict(ankle=(194, 166), bend=-1, foot=0)],
                         arms=[dict(ua=91, fa=90)])
                ha = J['arms'][0][2]; dumbbell_end(sc, (ha[0], ha[1]+3), 8)
                sc.arrow((236, 150), (236, 100))
            else:
                hip = (204, 96)
                J = side(sc, hip, -89, legs=[dict(ankle=(198, 158), bend=-1, foot=8, far=True), dict(ankle=(206, 166), bend=-1, foot=0)],
                         arms=[dict(ua=91, fa=90)])
                ha = J['arms'][0][2]; dumbbell_end(sc, (ha[0], ha[1]+3), 8)
        panels(sc, draw=draw)
    finally:
        LEN.update(save)
