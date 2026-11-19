# -*- coding: utf-8 -*-
"""Top-view field diagrams (themable SVG strings) for sprint, change-of-direction and ball drills."""
import math

W = 344


def _m(i, cls):
    return (f"<marker id='{i}' viewBox='0 0 10 10' refX='7' refY='5' markerWidth='5' markerHeight='5' orient='auto-start-reverse'>"
            f"<path d='M0 0L10 5L0 10z' class='{cls}'/></marker>")


class Dia:
    def __init__(self, slug, h, label):
        self.slug, self.h, self.label, self.o = slug, h, label, []

    def cone(self, x, y): self.o.append(f"<path class='dg-cone' d='M{x-6} {y+5}L{x} {y-7}L{x+6} {y+5}Z'/>")
    def ball(self, x, y, r=5): self.o.append(f"<circle class='dg-ball' cx='{x}' cy='{y}' r='{r}'/>")
    def player(self, x, y, ang=0, partner=False):
        c = 'dg-pl2' if partner else 'dg-pl'
        r = math.radians(ang); nx, ny = x + math.cos(r) * 12, y + math.sin(r) * 12
        self.o.append(f"<line class='{c}n' x1='{x}' y1='{y}' x2='{nx:.1f}' y2='{ny:.1f}'/><circle class='{c}' cx='{x}' cy='{y}' r='8'/>")
    def path(self, d, kind='run', alt=False):
        mk = {'run': 'a', 'drib': 'd', 'shot': 'a', 'pass': 'p', 'walk': 'g'}[kind]
        self.o.append(f"<path class='dg-{kind}{' dg-alt' if alt else ''}' d='{d}' marker-end='url(#dm-{self.slug}-{mk})'/>")
    def wavy(self, pts, amp=3.5, wl=13, alt=False):
        """dribble: wavy line along a polyline"""
        out = []
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            L = math.hypot(x1 - x0, y1 - y0); n = max(2, int(L / 3))
            ux, uy = (x1 - x0) / L, (y1 - y0) / L
            for k in range(n + 1):
                t = k / n; s = t * L
                off = amp * math.sin(2 * math.pi * s / wl) * min(1, s / 10, (L - s) / 10)
                out.append((x0 + ux * s - uy * off, y0 + uy * s + ux * off))
        d = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in out)
        self.path(d, 'drib', alt)
    def text(self, x, y, s, anchor='middle', cls='dg-t'):
        self.o.append(f"<text class='{cls}' x='{x}' y='{y}' text-anchor='{anchor}'>{s}</text>")
    def raw(self, s): self.o.append(s)
    def svg(self):
        s = self.slug
        defs = '<defs>' + _m(f'dm-{s}-a', 'dg-ma') + _m(f'dm-{s}-d', 'dg-md') + _m(f'dm-{s}-p', 'dg-mp') + _m(f'dm-{s}-g', 'dg-mg') + '</defs>'
        return (f"<svg class='dia' viewBox='0 0 {W} {self.h}' role='img' aria-label='{self.label}'>{defs}"
                f"<rect class='dg-bg' x='0' y='0' width='{W}' height='{self.h}' rx='12'/>" + ''.join(self.o) + '</svg>')


def sprint20():
    d = Dia('sprint-20', 150, 'Sprint 20 m vu de dessus')
    for x, lab in ((30, 'Départ'), (172, '10 m'), (314, '20 m')):
        d.cone(x, 52); d.cone(x, 98); d.text(x, 34, lab)
    d.player(30, 75, 0)
    d.path('M44 75 L300 75')
    d.path('M300 124 L44 124', 'walk')
    d.text(172, 144, 'retour en marchant, puis repos')
    return d.svg()


def cut45():
    d = Dia('cut-45', 176, 'Crochets à 45 degrés vus de dessus')
    d.player(30, 100, 0)
    d.cone(132, 100); d.cone(196, 38); d.cone(196, 162)
    d.path('M44 100 L124 100')
    d.path('M134 94 L188 46')
    d.path('M134 106 L188 154', 'run', True)
    d.text(84, 122, '5 m'); d.text(178, 84, '5 m', 'start')
    d.raw("<path class='dg-ang' d='M160 100 A28 28 0 0 0 152 82'/>")
    d.text(166, 104, '45°', 'start')
    d.text(250, 104, 'alterne droite', 'start'); d.text(250, 120, 'et gauche', 'start')
    return d.svg()


def cod505():
    d = Dia('cod-505', 156, 'Demi-tour 5-0-5 vu de dessus')
    d.raw("<rect class='dg-zone' x='200' y='44' width='92' height='64' rx='6'/>")
    d.cone(26, 94); d.cone(200, 50); d.cone(200, 102); d.cone(292, 50); d.cone(292, 102)
    d.raw("<line class='dg-line' x1='292' y1='50' x2='292' y2='102'/>")
    d.player(26, 66, 0)
    d.path('M40 66 L282 66 Q302 76 282 88 L206 88')
    for x, lab in ((26, 'Départ'), (200, '10 m'), (292, '15 m')): d.text(x, 30, lab)
    d.text(246, 130, 'chrono : de la porte des 10 m'); d.text(246, 146, 'à la porte, après le demi-tour')
    return d.svg()


def reactive():
    d = Dia('reactive-agility', 176, 'Agilité sur signal vue de dessus')
    d.player(172, 24, 90, partner=True)
    d.raw("<path class='dg-sig' d='M154 24 L136 24 M190 24 L208 24'/>")
    d.text(232, 28, 'signal', 'start')
    d.cone(70, 86); d.cone(274, 86); d.cone(172, 108)
    d.player(172, 156, -90)
    d.path('M172 142 L172 116')
    d.path('M166 106 L82 88')
    d.path('M178 106 L262 88', 'run', True)
    d.text(184, 136, '3 à 4 m', 'start')
    return d.svg()


def dribble_sprint():
    d = Dia('dribble-sprint', 132, 'Conduite de balle rapide vue de dessus')
    d.raw("<rect class='dg-zone' x='282' y='42' width='46' height='46' rx='6'/>")
    d.cone(30, 46); d.cone(30, 84); d.cone(282, 42); d.cone(328, 42); d.cone(282, 88); d.cone(328, 88)
    d.player(22, 65, 0); d.ball(38, 65)
    d.wavy([(46, 65), (290, 65)])
    d.text(160, 40, '20 m, touches longues'); d.text(334, 112, 'arrêt du ballon', 'end')
    return d.svg()


def slalom():
    d = Dia('dribble-slalom', 132, 'Slalom ballon vu de dessus')
    xs = [74 + 34 * k for k in range(7)]
    for x in xs: d.cone(x, 66)
    d.player(26, 66, 0); d.ball(42, 66)
    pts = [(50 + k * 2, 66 + 20 * math.cos(math.pi * (50 + k * 2 - 74) / 34 + math.pi) * min(1, (k * 2) / 24)) for k in range(int((xs[-1] + 30 - 50) / 2))]
    d.path('M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts), 'drib')
    d.text(172, 118, '1 m entre les plots · intérieur, extérieur, semelle')
    return d.svg()


def wall_control():
    d = Dia('wall-control', 186, 'Contrôle orienté au mur vu de dessus')
    d.raw("<rect class='dg-wall' x='318' y='16' width='12' height='154' rx='3'/>")
    d.cone(112, 40); d.cone(112, 146)
    d.player(196, 94, 0); d.ball(212, 94)
    d.path('M218 90 L312 90', 'pass')
    d.path('M312 100 L220 100', 'pass')
    d.path('M190 84 Q160 60 122 48', 'drib')
    d.path('M126 44 L312 60', 'pass', True)
    d.text(262, 128, '5 m'); d.raw("<path class='dg-meas' d='M196 116 L318 116'/>")
    d.text(112, 70, 'contrôle', 'middle'); d.text(112, 84, 'orienté', 'middle')
    d.text(196, 172, 'passe, contrôle vers un plot, repasse')
    return d.svg()


def weak_foot():
    d = Dia('weak-foot-wall', 146, 'Passes du pied faible contre un mur vues de dessus')
    d.raw("<rect class='dg-wall' x='318' y='16' width='12' height='100' rx='3'/>")
    d.player(112, 66, 0); d.ball(128, 66)
    d.path('M136 60 L312 60', 'pass'); d.path('M312 74 L138 74', 'pass')
    d.raw("<path class='dg-meas' d='M112 96 L318 96'/>"); d.text(215, 112, '4 à 6 m')
    d.text(172, 136, 'pied faible uniquement')
    return d.svg()


def dribble_shot():
    d = Dia('dribble-shot', 176, 'Dribble et frappe vus de dessus')
    d.raw("<path class='dg-goal' d='M330 46 L304 46 L304 126 L330 126'/>")
    d.cone(170, 96)
    d.player(30, 132, -20); d.ball(46, 128)
    d.wavy([(54, 126), (150, 104)])
    d.path('M152 100 Q170 72 196 80', 'drib')
    d.path('M204 80 L298 70', 'shot')
    d.text(170, 124, 'crochet'); d.text(250, 60, 'frappe')
    return d.svg()


def intervals():
    d = Dia('dribble-intervals', 176, 'Intervalles ballon 15/15 vus de dessus')
    d.raw("<rect class='dg-zone2' x='74' y='18' width='196' height='140' rx='4'/>")
    for x, y in ((74, 18), (270, 18), (74, 158), (270, 158)): d.cone(x, y + 4 if y == 18 else y)
    d.player(110, 130, -40); d.ball(124, 120)
    d.path('M130 114 C170 70 140 44 196 48 C250 52 236 100 206 104 C170 108 196 140 238 130', 'drib')
    d.text(172, 14, '15 m'); d.text(40, 92, '15 s', 'middle'); d.text(40, 108, 'à fond', 'middle')
    d.text(304, 92, '15 s', 'middle'); d.text(304, 108, 'lent', 'middle')
    return d.svg()


DIAGRAMS = {
    'sprint-20': sprint20, 'cut-45': cut45, 'cod-505': cod505, 'reactive-agility': reactive,
    'dribble-sprint': dribble_sprint, 'dribble-slalom': slalom, 'wall-control': wall_control,
    'weak-foot-wall': weak_foot, 'dribble-shot': dribble_shot, 'dribble-intervals': intervals,
}

# light theme preview colours (the app styles these classes itself)
PREVIEW_CSS = """
.dg-bg{fill:#e3f1e3}.dg-cone{fill:#ff7a1a}.dg-ball{fill:#fff;stroke:#111;stroke-width:2}
.dg-pl{fill:#111}.dg-pln{stroke:#111;stroke-width:4;stroke-linecap:round}.dg-pl2{fill:#8a8f98}.dg-pl2n{stroke:#8a8f98;stroke-width:4;stroke-linecap:round}
.dg-run,.dg-drib,.dg-shot{fill:none;stroke:#2563eb;stroke-width:3;stroke-linecap:round;stroke-linejoin:round}
.dg-drib{stroke:#e0306b;stroke-width:2.5}.dg-shot{stroke-width:3.5}
.dg-pass{fill:none;stroke:#111;stroke-width:2;stroke-dasharray:5 5}.dg-walk{fill:none;stroke:#8a8f98;stroke-width:2;stroke-dasharray:4 6}
.dg-alt{opacity:.35}.dg-md{fill:#e0306b}.dg-ma{fill:#2563eb}.dg-mp{fill:#111}.dg-mg{fill:#8a8f98}
.dg-t{font:600 12px Helvetica,Arial,sans-serif;fill:#3b4250}.dg-zone{fill:#2563eb;opacity:.12}.dg-zone2{fill:none;stroke:#3b4250;stroke-width:2;stroke-dasharray:6 6}
.dg-wall{fill:#9aa1ab}.dg-goal{fill:none;stroke:#111;stroke-width:4;stroke-linejoin:round}.dg-line{stroke:#111;stroke-width:2}
.dg-meas{stroke:#3b4250;stroke-width:1.5;stroke-dasharray:3 4}.dg-sig{stroke:#ff7a1a;stroke-width:3;stroke-linecap:round}.dg-ang{fill:none;stroke:#3b4250;stroke-width:1.5}
"""

if __name__ == '__main__':
    import subprocess, os, sys
    out = '/home/claude/draw/out3'; os.makedirs(out, exist_ok=True)
    pngs = []
    for k, f in DIAGRAMS.items():
        s = f().replace("<svg class='dia'", "<svg xmlns='http://www.w3.org/2000/svg' width='688' class='dia'", 1)
        s = s.replace('<defs>', f'<style>{PREVIEW_CSS}</style><defs>', 1)
        p = f'{out}/{k}'
        open(p + '.svg', 'w').write(s)
        subprocess.run(['rsvg-convert', '-w', '520', '-o', p + '.png', p + '.svg'], check=True)
        pngs.append(p + '.png')
    subprocess.run(['montage'] + pngs + ['-tile', '2x', '-geometry', '+6+6', '-background', '#ffffff', '/home/claude/draw/sheet_dia.png'], check=True)
    print('ok', len(pngs))
