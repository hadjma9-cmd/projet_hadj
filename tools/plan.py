# -*- coding: utf-8 -*-
"""Repas v3 : calories ajustées au type de journée, ~160 g de protéines chaque jour, une seule whey par jour.
Poisson 2 fois par semaine (ANSES) : lundi soir (semaine A meunière / semaine B thon 100 g) et jeudi soir (sardines, poisson gras)."""
from foods import FOODS, kp

FISH_A = dict(meuniere=1, wedges=170, oeuf=2, salade=1, tomate=1, huile=1)
FISH_B = dict(thon=100, riz=95, oeuf=2, tomate=1, salade=1, huile=1)
FISH_TITLES = dict(A='Poisson meunière, œufs durs et wedges', B='Salade de riz au thon')

# (nom du repas, aliments, titre du plat)
PLAN = {
 'Lundi': dict(tag='Haut A', target=2200, meals=[
   ('Petit-déjeuner', dict(oeuf=3, pain=2, banane=1), 'Œufs brouillés et tartines'),
   ('Déjeuner', dict(poulet=170, pates=90, sauce=120, salade=1, huile=1), 'Pâtes au poulet, sauce tomate'),
   ('Après la séance', dict(whey=1, fruit=1, amandes=15), ''),
   ('Dîner', 'FISH', ''),
   ('Soir', dict(skyr=150), ''),
 ]),
 'Mardi': dict(tag='Bas', target=2350, meals=[
   ('Petit-déjeuner', dict(skyr=200, avoine=70, banane=1, miel=1), 'Bol skyr, avoine, banane'),
   ('Déjeuner', dict(poulet=170, riz=120, legumes=150, huile=1), 'Poulet, riz et légumes'),
   ('Après la séance', dict(whey=1, pain=2, miel=1), ''),
   ('Dîner', dict(poulet=120, pates=115, sauce=120, salade=1, huile=1), 'Pâtes au poulet, sauce tomate'),
   ('Soir', dict(skyr=150), ''),
 ]),
 'Mercredi': dict(tag='Foot', target=2500, meals=[
   ('Petit-déjeuner', dict(oeuf=3, pain=2, fruit=1), 'Œufs et tartines'),
   ('Déjeuner', dict(poulet=160, pates=140, sauce=150, salade=1, huile=1), 'Pâtes au poulet, sauce tomate'),
   ('1 h 30 avant le foot', dict(skyr=150, banane=1, pain=1, miel=1), ''),
   ('Après le foot', dict(whey=1, fruit=1), ''),
   ('Dîner', dict(poulet=150, wedges=290, salade=1, tomate=1, huile=1), 'Poulet et wedges'),
 ]),
 'Jeudi': dict(tag='Récup', target=2050, meals=[
   ('Petit-déjeuner', dict(skyr=200, avoine=50, fruit=1, amandes=10), 'Bol skyr, avoine, fruit'),
   ('Déjeuner', dict(poulet=170, riz=80, legumes=200, huile=1), 'Poulet, riz et légumes'),
   ('Collation', dict(whey=1, fruit=1, amandes=15), ''),
   ('Dîner', dict(sardines=100, pates=95, sauce=120, salade=1), 'Pâtes aux sardines, sauce tomate'),
   ('Soir', dict(skyr=150), ''),
 ]),
 'Vendredi': dict(tag='Vitesse', target=2300, meals=[
   ('Petit-déjeuner', dict(skyr=200, avoine=70, banane=1, miel=1), 'Bol skyr, avoine, banane'),
   ('Déjeuner', dict(poulet=170, riz=115, legumes=150, huile=1), 'Poulet, riz et légumes'),
   ('Après la séance', dict(whey=1, banane=1, amandes=10), ''),
   ('Dîner', dict(poulet=100, oeuf=2, sauce=150, pain=3, huile=1, salade=1), 'Chakchouka au poulet'),
   ('Soir', dict(skyr=150), ''),
 ]),
 'Samedi': dict(tag='Haut B', target=2250, meals=[
   ('Petit-déjeuner', dict(oeuf=3, pain=2, banane=1), 'Œufs et tartines'),
   ('Déjeuner', dict(poulet=170, wedges=260, salade=1, tomate=1, huile=1), 'Poulet et wedges'),
   ('Après la séance', dict(whey=1, fruit=1, amandes=15), ''),
   ('Dîner', dict(poulet=130, pates=115, sauce=120, salade=1, huile=1), 'Pâtes au poulet, sauce tomate'),
   ('Soir', dict(skyr=150), ''),
 ], alt=dict(tag='Veille de match', target=2400, meals=[
   ('Petit-déjeuner', dict(oeuf=3, pain=2, banane=1), 'Œufs et tartines'),
   ('Déjeuner', dict(poulet=170, wedges=260, salade=1, tomate=1, huile=1), 'Poulet et wedges'),
   ('Après la séance', dict(whey=1, fruit=1, amandes=15), ''),
   ('Dîner', dict(poulet=130, pates=150, sauce=150, salade=1, huile=1), 'Pâtes au poulet : grosse assiette, veille de match'),
   ('Soir', dict(skyr=150, miel=1), ''),
 ])),
 'Dimanche': dict(tag='Technique', target=2300, meals=[
   ('Petit-déjeuner', dict(oeuf=3, pain=2, tomate=1, banane=1), 'Œufs, tartines et tomate'),
   ('Déjeuner', dict(poulet=170, wedges=260, salade=1, huile=1), 'Poulet et wedges'),
   ('Après la séance', dict(whey=1, fruit=1, amandes=20), ''),
   ('Dîner', dict(poulet=140, riz=115, legumes=200, huile=1), 'Poulet, riz et légumes'),
   ('Soir', dict(skyr=150, miel=1), ''),
 ], alt=dict(tag='Match', target=2550, meals=[
   ('Petit-déjeuner', dict(oeuf=3, pain=2, banane=1, miel=1), 'Œufs, tartines et miel'),
   ('Repas d’avant-match (3 h avant)', dict(poulet=130, pates=135, sauce=120, huile=1), 'Pâtes au poulet, peu de légumes'),
   ('1 h avant le match', dict(banane=1, pain=1, miel=1), ''),
   ('Après le match', dict(whey=1, fruit=1, pain=1), ''),
   ('Dîner', dict(poulet=150, riz=110, legumes=150, huile=1), 'Poulet, riz et légumes'),
   ('Soir', dict(skyr=150), ''),
 ])),
}

def resolve(items, week):
    return (FISH_A if week == 'A' else FISH_B) if items == 'FISH' else items

def day_totals(meals, week):
    k = p = 0
    for name, items, title in meals:
        for f, q in resolve(items, week).items():
            a, b = kp(f, q); k += a; p += b
    return k, p

if __name__ == '__main__':
    for week in 'AB':
        print('== Semaine', week)
        for day, d in PLAN.items():
            for lab, dd in [('', d)] + ([('  +' + d['alt']['tag'], d['alt'])] if 'alt' in d else []):
                k, p = day_totals(dd['meals'], week)
                wh = sum(1 for _, it, _ in dd['meals'] if it != 'FISH' and 'whey' in it)
                print(f'  {day:9s}{lab:18s} {k:5.0f} kcal (cible {dd["target"]}) {p:5.1f} g prot  whey={wh}')
