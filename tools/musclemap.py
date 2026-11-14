"""Muscle map: front and back silhouettes built from muscle regions."""
import json
FR, BK = 30, 94   # centres of the front and back figures

def e(dx, y, rx, ry, rot=0):
    return ('e', dx, y, rx, ry, rot)
def p(*pts):  # path from relative points; 'C' handled by tuples of 3
    return ('p',) + pts
def r(x0, y0, x1, y1, rr):
    return ('r', x0, y0, x1, y1, rr)

# (keys lighting it, shape, paired?)
FRONT = [
  ([], e(0, 8, 5.6, 6.4), False), ([], r(-2.6, 13, 2.6, 17.5, 1), False),
  (['trapezes'], p(('M', -2.6, 15.6), ('L', -10.4, 19.8), ('L', -3, 19.4)), True),
  (['pecs'], p(('M', -0.7, 19.8), ('C', -5, 18.6, -10.6, 19.2, -11.3, 23.6), ('C', -11.5, 28.8, -5.8, 30.8, -0.7, 29.3)), True),
  (['epaules_av', 'epaules_cote'], e(-12.8, 23.4, 4.4, 5.1, 18), True),
  (['biceps'], e(-15.3, 31.8, 2.9, 5.8, 12), True),
  (['avantbras'], e(-17.7, 43.6, 2.6, 6.4, 14), True),
  ([], e(-19.7, 52.7, 2.1, 2.8, 14), True),
  (['abdos'], r(-4.6, 30.8, 4.6, 52, 3), False),
  (['obliques'], p(('M', -5.5, 31.4), ('L', -10.3, 30.6), ('C', -10.9, 37, -10.3, 44, -8.7, 50.6), ('L', -5.5, 52)), True),
  ([], p(('M', -8.7, 52.6), ('L', 8.7, 52.6), ('L', 6.2, 59.2), ('L', -6.2, 59.2)), False),
  (['flechisseurs'], e(-5.4, 56.2, 2.3, 2.7, 0), True),
  (['quadris'], e(-6.7, 70.6, 4.5, 12.4, 4), True),
  (['adducteurs'], e(-2.3, 64.6, 1.5, 5.6, -6), True),
  ([], e(-6.4, 85.4, 2.6, 2.6), True),
  ([], e(-6.6, 96.2, 2.6, 8.2, 0), True),
  ([], e(-7.4, 107.2, 3.4, 1.8), True),
]
BACK = [
  ([], e(0, 8, 5.6, 6.4), False), ([], r(-2.6, 13, 2.6, 17.5, 1), False),
  (['trapezes'], p(('M', 0, 13.8), ('L', -10.8, 20), ('L', -4.8, 24.8), ('L', 0, 34.2), ('L', 4.8, 24.8), ('L', 10.8, 20)), False),
  (['haut_dos'], p(('M', -4.2, 25.4), ('L', 0, 23.6), ('L', 4.2, 25.4), ('L', 3.2, 31), ('L', 0, 33.4), ('L', -3.2, 31)), False),
  (['epaules_arr', 'epaules_cote'], e(-12.8, 23.4, 4.4, 5.1, -18), True),
  (['dorsaux'], p(('M', -10.4, 26.4), ('C', -12, 33.4, -10.4, 41.4, -5.6, 47.2), ('L', -2.2, 47.8), ('L', -2.6, 35.4), ('C', -4.6, 31.8, -7.4, 28.4, -10.4, 26.4)), True),
  (['triceps'], e(-15.4, 31.8, 3.0, 6.0, 12), True),
  (['avantbras'], e(-17.7, 43.6, 2.6, 6.4, 14), True),
  ([], e(-19.7, 52.7, 2.1, 2.8, 14), True),
  (['lombaires'], r(-4.4, 43.2, 4.4, 53, 2.4), False),
  (['fessiers'], e(-5, 58.6, 5.2, 5.5, 0), True),
  (['ischios'], e(-6.3, 73.4, 4.3, 10.4, 3), True),
  ([], e(-6.4, 85.4, 2.6, 2.6), True),
  (['mollets'], e(-6.6, 93.6, 3.4, 8.4, 0), True),
  ([], e(-7.4, 107.2, 3.4, 1.8), True),
]

def emit(shape, cx, m):
    t = shape[0]
    f = lambda v: round(v, 2)
    if t == 'e':
        _, dx, y, rx, ry, rot = shape
        x = cx + m * dx
        tr = f" transform='rotate({f(-rot * m)} {f(x)} {f(y)})'" if rot else ''
        return f"<ellipse cx='{f(x)}' cy='{f(y)}' rx='{rx}' ry='{ry}'{tr}/>"
    if t == 'r':
        _, x0, y0, x1, y1, rr = shape
        return f"<rect x='{f(cx + x0)}' y='{y0}' width='{f(x1 - x0)}' height='{f(y1 - y0)}' rx='{rr}'/>"
    d = []
    for seg in shape[1:]:
        if seg[0] in 'ML': d.append(f"{seg[0]}{f(cx + m * seg[1])} {seg[2]}")
        else: d.append(f"C{f(cx + m * seg[1])} {seg[2]} {f(cx + m * seg[3])} {seg[4]} {f(cx + m * seg[5])} {seg[6]}")
    return f"<path d='{' '.join(d)}Z'/>"

def regions():
    out = []
    for cx, parts in ((FR, FRONT), (BK, BACK)):
        for keys, shape, paired in parts:
            for m in ((1, -1) if paired else (1,)):
                out.append([keys, emit(shape, cx, m)])
    return out

def svg(prim, sec, acc='#2563EB', base='#D7DAE0', bg='#ffffff'):
    o = [f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 124 114' width='372' height='342'><rect width='124' height='114' fill='{bg}'/>"]
    for keys, el in regions():
        if any(k in prim for k in keys): fill = f"fill='{acc}'"
        elif any(k in sec for k in keys): fill = f"fill='{acc}' fill-opacity='.38'"
        else: fill = f"fill='{base}'"
        o.append(el.replace('<ellipse', f'<ellipse {fill}').replace('<rect', f'<rect {fill}').replace('<path', f'<path {fill}'))
    # six-pack lines
    o.append(f"<path d='M{FR} 31 V51.6 M{FR-4.6} 37.6 H{FR+4.6} M{FR-4.6} 44.4 H{FR+4.6}' stroke='{bg}' stroke-width='.8'/>")
    o.append('</svg>')
    return ''.join(o)

if __name__ == '__main__':
    import subprocess
    open('out2/mm1.svg', 'w').write(svg(['pecs'], ['triceps', 'epaules_av']))
    open('out2/mm2.svg', 'w').write(svg(['dorsaux', 'haut_dos'], ['biceps', 'epaules_arr'], acc='#0D9488'))
    open('out2/mm3.svg', 'w').write(svg(['quadris', 'fessiers'], ['ischios', 'adducteurs'], acc='#EA580C'))
    for n in ('mm1', 'mm2', 'mm3'):
        subprocess.run(['rsvg-convert', '-o', f'out2/{n}.png', f'out2/{n}.svg'], check=True)
    subprocess.run(['montage', 'out2/mm1.png', 'out2/mm2.png', 'out2/mm3.png', '-tile', '3x', '-geometry', '+4+4', 'out2/mm.png'], check=True)
    json.dump(regions(), open('out2/regions.json', 'w'))
    print('ok')
