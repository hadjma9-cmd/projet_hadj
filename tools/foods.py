# Valeurs moyennes (table Ciqual de l'ANSES et étiquettes courantes) : kcal et protéines
# 'g' = pour 100 g ; sinon par unité
FOODS = {
 'poulet':   dict(n='Escalope de poulet halal (poids cru)', per='g', kcal=110, p=23.0),
 'oeuf':     dict(n='Œuf', pl='Œufs', per='u', kcal=72, p=6.4, w=50),
 'skyr':     dict(n='Skyr nature', per='g', kcal=62, p=10.5),
 'whey':     dict(n='Whey (1 dose de 30 g)', per='u', kcal=115, p=23.0),
 'thon':     dict(n='Thon au naturel, égoutté', per='g', kcal=110, p=25.0),
 'meuniere': dict(n='Filet de limande ou merlu façon meunière', per='u', kcal=190, p=13.8, w=110),
 'sardines': dict(n='Sardines à l’huile d’olive, égouttées', per='g', kcal=210, p=24.5, new=True),
 'pates':    dict(n='Pâtes (poids cru)', per='g', kcal=355, p=12.5),
 'riz':      dict(n='Riz (poids cru)', per='g', kcal=350, p=7.0),
 'wedges':   dict(n='Wedges Aldi à l’air fryer', per='g', kcal=140, p=2.2),
 'sauce':    dict(n='Sauce tomate', per='g', kcal=50, p=1.5),
 'salade':   dict(n='Salade', per='u', kcal=8, p=0.6, unit='bol'),
 'tomate':   dict(n='Tomate', pl='Tomates', per='u', kcal=22, p=1.0),
 'huile':    dict(n='Huile d’olive', per='u', kcal=90, p=0, unit='c. à soupe'),
 'avoine':   dict(n='Flocons d’avoine', per='g', kcal=370, p=13.5, new=True),
 'pain':     dict(n='Pain complet', per='u', kcal=85, p=3.3, unit='tranche', new=True),
 'banane':   dict(n='Banane', pl='Bananes', per='u', kcal=105, p=1.3, new=True),
 'fruit':    dict(n='Fruit (pomme, poire, orange…)', pl='Fruits de saison', per='u', kcal=75, p=0.5, new=True),
 'amandes':  dict(n='Amandes', per='g', kcal=630, p=21.0, new=True),
 'miel':     dict(n='Miel', per='u', kcal=22, p=0, unit='c. à café', new=True),
 'legumes':  dict(n='Légumes verts surgelés', per='g', kcal=30, p=2.0, new=True),
}
def kp(f, q):
    F = FOODS[f]
    k = F['kcal'] * q / 100 if F['per'] == 'g' else F['kcal'] * q
    pr = F['p'] * q / 100 if F['per'] == 'g' else F['p'] * q
    return k, pr
