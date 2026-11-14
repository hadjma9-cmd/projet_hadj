from foods import FOODS, kp
# Poisson : 2 fois par semaine (ANSES) dont 1 poisson gras. L'autre poisson alterne :
# semaine A = poisson meunière, semaine B = thon (100 g). Le repas 'FISH' est remplacé selon la semaine.
FISH_A = dict(meuniere=1, wedges=150, salade=1, tomate=1, huile=1, oeuf=2)
FISH_B = dict(thon=100, riz=85, oeuf=2, tomate=1, salade=1, huile=1)
PLAN = {
 'Lundi': [
   ('Petit-déjeuner', dict(oeuf=3, pain=2, banane=1)),
   ('Déjeuner', dict(poulet=170, pates=85, sauce=120, salade=1, huile=1)),
   ('Collation', dict(whey=1, fruit=1, amandes=20)),
   ('Dîner', dict(poulet=150, riz=70, legumes=200, huile=1)),
   ('Soir', dict(skyr=150)),
 ],
 'Mardi': [
   ('Petit-déjeuner', dict(skyr=200, avoine=50, banane=1, miel=1)),
   ('Déjeuner', dict(poulet=170, riz=85, legumes=150, huile=1)),
   ('Collation', dict(whey=1, fruit=1, amandes=15)),
   ('Dîner', 'FISH'),
   ('Soir', dict(skyr=150)),
 ],
 'Mercredi': [
   ('Petit-déjeuner', dict(oeuf=3, pain=2, fruit=1)),
   ('Déjeuner', dict(poulet=160, pates=110, sauce=150, salade=1, huile=1)),
   ('Avant le foot', dict(skyr=150, banane=1, miel=1)),
   ('Après le foot', dict(whey=1)),
   ('Dîner', dict(poulet=150, wedges=200, salade=1, tomate=1, huile=1)),
 ],
 'Jeudi': [
   ('Petit-déjeuner', dict(skyr=200, avoine=50, fruit=1, amandes=10)),
   ('Déjeuner', dict(poulet=170, pates=90, sauce=120, salade=1, huile=1)),
   ('Collation', dict(whey=1, fruit=1, amandes=15)),
   ('Dîner', dict(oeuf=4, sauce=150, pain=2, salade=1, huile=1)),
   ('Soir', dict(skyr=150)),
 ],
 'Vendredi': [
   ('Petit-déjeuner', dict(oeuf=3, pain=2, banane=1)),
   ('Déjeuner', dict(poulet=170, riz=90, legumes=150, huile=1)),
   ('Collation', dict(whey=1, fruit=1, amandes=15)),
   ('Dîner', dict(sardines=100, pates=85, sauce=120, salade=1)),
   ('Soir', dict(skyr=150)),
 ],
 'Samedi': [
   ('Petit-déjeuner', dict(skyr=200, avoine=50, banane=1, miel=1)),
   ('Déjeuner', dict(poulet=170, wedges=190, salade=1, tomate=1, huile=1)),
   ('Collation', dict(whey=1, pain=2, oeuf=1)),
   ('Dîner', dict(poulet=140, pates=90, sauce=120, salade=1, huile=1)),
   ('Soir', dict(skyr=150)),
 ],
 'Dimanche': [
   ('Petit-déjeuner', dict(oeuf=3, pain=2, tomate=1, fruit=1)),
   ('Déjeuner', dict(poulet=170, wedges=200, salade=1, huile=1)),
   ('Collation', dict(whey=1, fruit=1, amandes=20)),
   ('Dîner', dict(poulet=140, riz=90, legumes=200, huile=1)),
   ('Soir', dict(skyr=150, miel=1)),
 ],
}
def resolve(items, week):
    return (FISH_A if week == 'A' else FISH_B) if items == 'FISH' else items
if __name__ == '__main__':
    for week in 'AB':
        print('== Semaine', week)
        tk = tp = 0
        for day, meals in PLAN.items():
            k = p = 0
            for name, items in meals:
                for f, q in resolve(items, week).items():
                    a, b = kp(f, q); k += a; p += b
            tk += k; tp += p
            print(f'  {day:9s} {k:5.0f} kcal {p:5.1f} g')
        print(f'  moyenne {tk/7:5.0f} kcal {tp/7:5.1f} g')
