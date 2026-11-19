# -*- coding: utf-8 -*-
"""Programme « Numéro 10 » : préparation physique d'un milieu offensif de foot à 7, cycle de 12 semaines.
Source unique pour l'app, le document et le coach."""
from catalog import MUSCLES, EX as EX2, DAYS as DAYS2, ABS as ABS2

# ---------------------------------------------------------------- cycle
BLOCKS = [
    dict(n=1, name='Fondations', weeks=[1, 2, 3, 4],
         goal='Apprendre les gestes, poser la base de force, habituer tendons et chevilles aux sauts et aux sprints.'),
    dict(n=2, name='Force', weeks=[5, 6, 7, 8],
         goal='Charges plus lourdes (6 à 8 répétitions), sprints à 100 %, freinages et demi-tours.'),
    dict(n=3, name='Puissance & vitesse', weeks=[9, 10, 11, 12],
         goal='Transformer la force en vitesse : charges lourdes mais rapides, sauts réactifs, agilité sur signal.'),
]
LEARN = [1, 2]          # 2 séries max : on apprend les gestes
DELOAD = [8, 12]        # semaine allégée : une série de moins, effort 7/10
TESTS = [1, 4, 8, 12]   # tests du vendredi

EFFORT = {
    '7/10': '3 répétitions en réserve',
    '8/10': '2 répétitions en réserve',
}

# ---------------------------------------------------------------- exercices
# eq : machine | halteres | pdc | medball | box | terrain | ballon | velo
# kind : force | power | core | plyo | sprint | cod | ball | prev | cardio
# qual : qualités travaillées (pour les exercices de terrain)
# step : pas de charge dans l'app ; neg=True : contrepoids (moins = plus dur)
SHORT = {
    'shoulder-press': 'Haltères', 'leg-curl': 'Assis', 'lying-leg-curl': 'Allongé', 'crunch': 'Crunch',
    'db-bench': 'Haltères', 'chest-press': 'Machine', 'smith-bench': 'Barre guidée',
    'assisted-pullup': 'Machine assistée', 'smith-inverted-row': 'Australiennes', 'db-pullover': 'Pull-over',
    'machine-shoulder-press': 'Machine', 'standing-db-press': 'Debout 2 bras',
    'db-row': 'Haltère 1 bras', 'machine-row': 'Machine', 'incline-db-row': 'Banc incliné',
    'dead-bug': 'Dead bug', 'plank': 'Planche', 'reverse-crunch': 'Relevé de bassin', 'flutter-kicks': 'Battements',
    'side-plank': 'Planche latérale', 'bicycle-crunch': 'Crunch vélo', 'leg-raise': 'Relevé de jambes',
    'goblet-squat': 'Gobelet', 'smith-squat': 'Barre guidée', 'leg-press': 'Presse',
    'rdl': 'Haltères', 'smith-rdl': 'Barre guidée', 'db-hip-thrust': 'Hip thrust',
    'step-up': 'De face', 'leg-curl': 'Leg curl', 'single-leg-rdl': 'Sur 1 jambe',
    'incline-press': 'Haltères', 'smith-incline': 'Barre guidée', 'pushup': 'Pompes',
    'dips': 'Barres', 'assisted-dip-machine': 'Machine assistée', 'close-grip-db-press': 'Haltères serrés',
}

KEEP = ['shoulder-press', 'leg-curl', 'lying-leg-curl', 'crunch', 'db-bench', 'chest-press', 'smith-bench', 'assisted-pullup', 'smith-inverted-row', 'db-pullover',
        'machine-shoulder-press', 'standing-db-press', 'db-row', 'machine-row', 'incline-db-row',
        'dead-bug', 'plank', 'reverse-crunch', 'flutter-kicks', 'side-plank', 'bicycle-crunch', 'leg-raise',
        'goblet-squat', 'smith-squat', 'leg-press', 'rdl', 'smith-rdl', 'db-hip-thrust', 'step-up',
        'single-leg-rdl', 'incline-press', 'smith-incline', 'pushup', 'dips', 'assisted-dip-machine', 'close-grip-db-press']

EX = {}
for k in KEEP:
    e = dict(EX2[k]); e['short'] = SHORT[k]; EX[k] = e

# retouches pour le nouveau contexte
EX['goblet-squat']['how'] = ('Tiens un haltère vertical contre la poitrine, pieds un peu plus larges que les épaules. Descends en gardant le buste droit, '
                             'coudes entre les genoux, cuisses au moins parallèles au sol, puis remonte vite en poussant dans tout le pied. '
                             'Quand l’haltère le plus lourd devient trop facile, passe sur « Barre guidée ».')
EX['goblet-squat']['start'] = '14–18 kg'
EX['rdl']['start'] = '12–14 kg par main'
EX['step-up']['how'] = ('Face à un banc stable (hauteur sous le genou), un haltère dans chaque main. Pose tout le pied sur le banc et pousse sur ce talon '
                        'pour monter, sans t’aider de la jambe au sol. Redescends lentement. Bloc 3 : la montée devient explosive.')
EX['assisted-pullup']['how'] = ('Genoux sur la plateforme. Lundi : mains un peu plus larges que les épaules. Samedi : prise serrée, paumes face à toi. '
                                'Tire jusqu’au menton au-dessus des poignées, redescends bras tendus. Plus de contrepoids = plus facile.')
EX['assisted-pullup']['inc'] = 'Haut de la fourchette à toutes les séries ? Enlève 5 kg de contrepoids. À 0 kg, tu fais de vraies tractions.'
EX['dips']['inc'] = 'Haut de la fourchette à toutes les séries ? Ralentis la descente (3 s), puis passe à 3 × 10.'
EX['plank']['inc'] = 'Tu tiens 45 s à chaque série ? Passe aux touches d’épaule.'
EX['plank']['reps'] = '30–45 s'
EX['side-plank']['reps'] = '20–30 s par côté'
EX['dead-bug']['reps'] = '8 par côté'

NEW = {
 # ---------------- haut du corps : puissance, duels
 'mb-chest-throw': dict(name='Lancer de médecine-ball poitrine', short='Médecine-ball', eq='medball', prim=['pecs', 'triceps'], sec=['epaules_av', 'abdos', 'quadris'],
    start='Ballon de 3 à 5 kg', reps='5',
    how='Debout face à un mur, à 2 ou 3 m, ballon contre la poitrine, genoux souples. Pousse le ballon le plus fort possible contre le mur en tendant les bras '
        'et en avançant d’un petit pas, rattrape-le au rebond, replace-toi. Chaque lancer est à fond.',
    err='Lancer avec les bras seuls : pousse avec les jambes et le tronc, comme pour repousser un adversaire.',
    inc='Les lancers restent rapides jusqu’au dernier ? Prends un ballon 1 kg plus lourd.'),
 'explosive-pushup': dict(name='Pompes explosives', short='Pompes explosives', eq='pdc', prim=['pecs', 'triceps'], sec=['epaules_av', 'abdos'],
    start='Poids du corps', reps='5',
    how='Position de pompe, corps gainé. Descends en contrôle, puis pousse le plus vite possible pour que les mains décollent du sol. '
        'Réceptionne-toi bras souples et enchaîne. Trop dur : mains posées sur un banc.',
    err='Laisser tomber le bassin à la réception.'),
 'hk-press': dict(name='Développé épaule un bras, à genou', short='À genou, 1 bras', eq='halteres', prim=['epaules_av', 'epaules_cote'], sec=['triceps', 'obliques', 'abdos'],
    start='8–10 kg', reps='8–10 par bras',
    how='Un genou au sol sur un tapis, l’autre pied devant. Haltère à l’épaule du côté du genou posé. Serre le fessier de ce côté, '
        'pousse au-dessus de la tête sans pencher le buste, redescends lentement. Toutes les répétitions d’un bras, puis l’autre.',
    err='Pencher le buste sur le côté pour pousser : c’est ton gainage qui doit tenir.'),
 'suitcase-carry': dict(name='Marche valise (un haltère)', short='Marche valise', eq='halteres', prim=['obliques'], sec=['abdos', 'avantbras', 'trapezes', 'fessiers'],
    start='16–20 kg', reps='20 m par côté',
    how='Un haltère lourd dans une seule main, bras le long du corps. Marche 20 m en restant parfaitement droit, épaules à la même hauteur, '
        'puis change de main. Pas lents et contrôlés.',
    err='Te pencher vers l’haltère : grandis-toi et serre les abdos.',
    inc='Tu restes droit sans effort ? Prends 2 kg de plus.'),
 'mb-rotation': dict(name='Lancer rotatif de médecine-ball', short='Médecine-ball', eq='medball', prim=['obliques', 'abdos'], sec=['fessiers', 'epaules_av'],
    start='Ballon de 3 à 4 kg', reps='5 par côté',
    how='De profil à un mur, à 1 ou 2 m, ballon tenu à hauteur de la hanche la plus éloignée du mur. Tourne les hanches puis les épaules et lance fort '
        'contre le mur, comme une frappe. Rattrape et enchaîne. Toutes les répétitions d’un côté, puis l’autre.',
    err='Lancer avec les bras : le mouvement part des pieds et des hanches.',
    inc='Les lancers restent rapides ? Ballon 1 kg plus lourd.'),
 'db-woodchop': dict(name='Bûcheron haltère', short='Haltère', eq='halteres', prim=['obliques'], sec=['abdos', 'epaules_av', 'fessiers'],
    start='6–8 kg', reps='8 par côté',
    how='Debout, haltère tenu à deux mains près d’une hanche, genoux fléchis. Monte-le en diagonale au-dessus de l’épaule opposée en pivotant '
        'sur le pied arrière : vite à la montée, lentement au retour.',
    err='Arrondir le dos en bas du mouvement.'),
 'shoulder-tap-plank': dict(name='Planche haute, touches d’épaule', short='Touches d’épaule', eq='pdc', prim=['abdos', 'obliques'], sec=['epaules_av', 'pecs'],
    start='Poids du corps', reps='8–12 par côté',
    how='En position de pompe, bras tendus, pieds un peu écartés. Touche l’épaule opposée avec une main, repose-la, puis l’autre, '
        'sans que le bassin tourne. Plus les pieds sont proches, plus c’est dur.',
    err='Laisser le bassin balancer : ralentis.'),
 # ---------------- bas du corps
 'box-jump': dict(name='Saut sur box', short='Box', eq='box', prim=['quadris', 'fessiers'], sec=['mollets', 'ischios'],
    start='Box de 40 à 50 cm', reps='3',
    how='Face à une box stable. Lance les bras en arrière en descendant en quart de squat, puis saute sur la box. Atterris en douceur, '
        'pieds à plat, genoux dans l’axe des pieds. Redescends en marchant : on ne saute jamais en arrière.',
    err='Prendre une box trop haute et atterrir accroupi : c’est la vitesse du saut qui compte, pas la hauteur.'),
 'cmj': dict(name='Saut vertical', short='Sans box', eq='pdc', prim=['quadris', 'fessiers'], sec=['mollets'],
    start='Poids du corps', reps='3',
    how='Debout, descends vite en quart de squat en lançant les bras en arrière, puis saute le plus haut possible en lançant les bras vers le ciel. '
        'Atterris souple, genoux dans l’axe. Une seconde de pause entre deux sauts.',
    err='Genoux qui rentrent à la réception.'),
 'lateral-step-up': dict(name='Montée latérale sur banc', short='Latérale', eq='halteres', prim=['quadris', 'fessiers'], sec=['adducteurs'],
    start='6–8 kg par main', reps='8 par jambe',
    how='De profil à un banc stable, pied le plus proche posé dessus. Pousse sur ce pied pour monter sur le côté, sans t’aider de l’autre jambe, '
        'puis redescends lentement. Idéal pour les appuis latéraux.',
    err='Genou qui rentre vers l’intérieur.'),
 'single-leg-press': dict(name='Presse à cuisses une jambe', short='Presse 1 jambe', eq='machine', prim=['quadris', 'fessiers'], sec=['ischios'],
    start='30–40 kg', reps='8 par jambe', drawing='leg-press',
    how='Comme la presse classique, mais un seul pied au milieu de la plateforme. Descends jusqu’à l’angle droit, pousse sans verrouiller le genou. '
        'Une jambe, puis l’autre.',
    err='Laisser le genou partir vers l’intérieur.'),
 'nordic': dict(name='Nordic (ischios)', short='Nordic', eq='pdc', prim=['ischios'], sec=['fessiers', 'mollets'],
    start='Poids du corps', reps='3–5',
    how='À genoux sur un tapis, talons bloqués sous une barre basse (barre guidée réglée au plus bas, coussin d’un appareil ou partenaire). '
        'Corps droit des genoux aux épaules, laisse-toi descendre vers l’avant le plus lentement possible en freinant avec l’arrière des cuisses. '
        'Rattrape-toi avec les mains, pousse pour revenir.',
    err='Plier les hanches (fesses en arrière) : le corps reste droit comme une planche.',
    inc='Tu freines jusqu’en bas ? Descends encore plus lentement (5 s), puis ajoute une répétition.'),
 'leg-curl-ecc': dict(name='Leg curl assis, retour lent', short='Leg curl lent', eq='machine', prim=['ischios'], sec=['mollets'],
    start='20–30 kg', reps='6–8', drawing='leg-curl',
    how='Comme un leg curl classique : ramène les talons sous le siège en 1 seconde, puis laisse remonter en 4 secondes. '
        'C’est le freinage qui protège tes ischios.',
    err='Lâcher la charge au retour.'),
 'calf-raise-sl': dict(name='Mollets sur une jambe', short='Sur une marche', eq='pdc', prim=['mollets'], sec=[],
    start='Poids du corps, puis un haltère', reps='12 par jambe',
    how='L’avant du pied sur une marche ou un step, une main sur un support. Descends le talon le plus bas possible, puis monte sur la pointe '
        'le plus haut possible, 1 seconde de pause. Une jambe, puis l’autre. Ajoute un haltère dans la main du côté qui travaille quand c’est facile.',
    err='Faire de petits mouvements rapides : amplitude complète.'),
 'machine-calf': dict(name='Mollets debout à la machine', short='Machine debout', eq='machine', prim=['mollets'], sec=[],
    start='40–60 kg', reps='12',
    how='Épaules sous les coussins, avant des pieds sur la marche. Descends les talons, monte sur la pointe, 1 seconde de pause en haut.',
    err='Plier les genoux pour aider.'),
 'seated-calf': dict(name='Mollets assis à la machine', short='Machine assis', eq='machine', prim=['mollets'], sec=[],
    start='20–30 kg', reps='12–15',
    how='Assis, genoux sous le coussin, avant des pieds sur la marche. Descends les talons, monte le plus haut possible, 1 seconde de pause.',
    err='Rebondir en bas du mouvement.'),
 # ---------------- prévention, récupération
 'copenhagen': dict(name='Copenhague (adducteurs)', short='Copenhague', eq='pdc', prim=['adducteurs'], sec=['obliques', 'abdos'],
    start='Poids du corps', reps='15–25 s par côté', timed=True,
    how='Sur le côté, coude sous l’épaule, le genou de la jambe du dessus posé sur un banc. Monte le bassin pour aligner épaules, hanches et genoux ; '
        'la jambe du dessous reste sous le banc. Tiens, puis change de côté. Bloc 3 : pose la cheville sur le banc, c’est plus dur.',
    err='Laisser tomber le bassin.'),
 'single-leg-balance': dict(name='Équilibre sur une jambe', short='Équilibre', eq='pdc', prim=['mollets'], sec=['fessiers', 'abdos'],
    start='Poids du corps', reps='30 s par jambe', timed=True,
    how='Debout sur une jambe, genou légèrement fléchi, l’autre pied décollé. Tiens 30 s sans poser le pied. Plus dur : yeux fermés, '
        'ou sur un coussin.',
    err='Verrouiller le genou tendu.'),
 'calf-iso': dict(name='Mollets tenus (isométrie)', short='Mollets tenus', eq='pdc', prim=['mollets'], sec=[],
    start='Poids du corps', reps='30 s par jambe', timed=True, drawing='calf-raise-sl',
    how='Sur une jambe, monte sur la pointe à mi-hauteur et tiens 30 s, genou légèrement fléchi. Protège tendon d’Achille et chevilles.',
    err='Monter et descendre : ici, on tient la position.'),
 'easy-bike': dict(name='Vélo facile', short='Vélo', eq='velo', prim=[], sec=[], qual=['Récupération', 'Endurance de base'],
    start='Résistance légère', reps='20–25 min', timed=True,
    how='Vélo d’appartement ou de salle, résistance légère, effort 3/10 : tu peux parler en phrases complètes. '
        'Marche rapide ou natation : ça marche aussi.',
    err='Accélérer : aujourd’hui on récupère, on ne s’entraîne pas.'),
 'juggling': dict(name='Jonglages', short='Jonglages', eq='ballon', prim=[], sec=[], qual=['Toucher de balle', 'Pied faible'],
    start='Un ballon', reps='5–10 min', timed=True,
    how='Jongle en alternant pied droit et pied gauche, puis cuisses et tête. Compte ta meilleure série sans que le ballon touche le sol : c’est ton record.',
    err='Jongler seulement du bon pied.'),
 # ---------------- vitesse, sauts, appuis (vendredi)
 'pogo': dict(name='Pogo (rebonds de chevilles)', short='Pogo', eq='pdc', prim=['mollets'], sec=['quadris'], qual=['Réactivité'],
    start='Poids du corps', reps='10',
    how='Petits rebonds rapides sur l’avant des pieds, jambes presque tendues, comme à la corde à sauter. Le temps au sol doit être le plus court possible.',
    err='Plier les genoux à chaque rebond : ce sont les chevilles qui font ressort.'),
 'broad-jump': dict(name='Saut en longueur sans élan', short='Longueur', eq='pdc', prim=['fessiers', 'quadris'], sec=['ischios', 'mollets'], qual=['Puissance'],
    start='Poids du corps', reps='3',
    how='Pieds à largeur de hanches. Lance les bras en arrière en descendant, puis saute le plus loin possible en lançant les bras vers l’avant. '
        'Atterris sur les deux pieds, genoux souples, et tiens 2 secondes.',
    err='Atterrir jambes tendues ou genoux qui rentrent.'),
 'skater': dict(name='Bonds latéraux (patineur)', short='Patineur', eq='pdc', prim=['fessiers', 'adducteurs'], sec=['quadris', 'mollets'], qual=['Appuis latéraux'],
    start='Poids du corps', reps='4 par côté',
    how='Sur une jambe, pousse fort sur le côté pour atterrir sur l’autre jambe, le plus loin possible. Stabilise 2 secondes, genou au-dessus du pied, '
        'puis repars de l’autre côté.',
    err='Genou qui rentre à la réception.'),
 'bounds': dict(name='Foulées bondissantes', short='Bondissements', eq='terrain', prim=['fessiers', 'ischios'], sec=['mollets', 'quadris'], qual=['Puissance', 'Foulée'],
    start='Sur 20 m environ', reps='4 par jambe',
    how='Course en bonds longs : pousse fort sur chaque jambe, genou avant haut, bras actifs. Cherche la distance et le temps en l’air, pas la vitesse.',
    err='Atterrir sur le talon, jambe tendue.'),
 'drop-jump': dict(name='Drop jump', short='Drop jump', eq='box', prim=['mollets', 'quadris'], sec=['fessiers'], qual=['Réactivité'],
    start='Box de 30 cm', reps='4',
    how='Sur une box basse, fais un pas en avant pour tomber (ne saute pas). Dès que tes pieds touchent le sol, rebondis le plus haut possible, '
        'avec un contact au sol très court.',
    err='Rester longtemps au sol ou s’écraser en squat.'),
 'starts-10': dict(name='Départs sur 10 m', short='Départs', eq='terrain', prim=['fessiers', 'quadris'], sec=['mollets', 'ischios'], qual=['Accélération'],
    start='2 plots à 10 m', reps='10 m',
    how='Départ debout, un pied devant. Penche-toi et pousse fort dans le sol, bras puissants, pendant 10 m. Varie : départ debout, de dos '
        '(demi-tour puis sprint), après un pas chassé. Retour en marchant.',
    err='Te redresser tout de suite : reste penché les 5 premiers mètres.'),
 'sprint-20': dict(name='Sprint 20 m', short='Plat', eq='terrain', prim=['ischios', 'fessiers'], sec=['mollets', 'quadris'], qual=['Vitesse', 'Accélération'],
    start='Plots à 0, 10 et 20 m', reps='20 m',
    how='Départ arrêté, accélère jusqu’au plot des 20 m. Bloc 1 : à 90 %, rapide mais relâché. Ensuite : à fond. Retour en marchant ; '
        'chaque sprint doit être aussi rapide que le premier.',
    err='Raccourcir le repos : la vitesse se travaille frais.'),
 'hill-sprint': dict(name='Sprint en côte', short='En côte', eq='terrain', prim=['fessiers', 'ischios'], sec=['mollets', 'quadris'], qual=['Accélération', 'Puissance'],
    start='Côte douce', reps='15 m',
    how='Une côte douce. Sprinte 15 m en montée, buste penché, genoux hauts, bras puissants. Redescends en marchant.',
    err='Côte trop raide : tu dois pouvoir courir, pas grimper.'),
 'decel': dict(name='Freinage', short='Freinage', eq='terrain', prim=['quadris', 'fessiers'], sec=['ischios'], qual=['Freinage'],
    start='2 plots à 10 m', reps='10 m + arrêt',
    how='Sprinte 10 m puis arrête-toi en 3 pas maximum : petits pas, hanches basses, buste légèrement en arrière, pieds sous toi. Tiens 2 secondes.',
    err='Freiner sur une seule grande foulée, jambe tendue.'),
 'cut-45': dict(name='Crochets à 45°', short='Crochet 45°', eq='terrain', prim=['quadris', 'adducteurs'], sec=['fessiers'], qual=['Changement de direction'],
    start='3 plots', reps='5 m + 5 m',
    how='Sprinte 5 m jusqu’au plot, crochète à 45° en poussant sur le pied extérieur, réaccélère 5 m. Abaisse-toi juste avant le plot. '
        'Alterne droite et gauche.',
    err='Arriver droit et haut sur le plot.'),
 'cod-505': dict(name='Demi-tour 5-0-5', short='5-0-5', eq='terrain', prim=['quadris', 'fessiers'], sec=['adducteurs', 'ischios'], qual=['Changement de direction', 'Freinage'],
    start='Plots à 0, 10 et 15 m', reps='1 aller-retour',
    how='Sprinte du départ jusqu’à la ligne des 15 m, fais demi-tour en posant un pied dessus, puis resprinte jusqu’au plot des 10 m. '
        'Pour le test, on chronomètre de la porte des 10 m au retour à cette porte. Alterne le pied de demi-tour.',
    err='Tourner en arc de cercle au lieu de freiner et repartir.'),
 'reactive-agility': dict(name='Agilité sur signal', short='Sur signal', eq='terrain', prim=['quadris', 'adducteurs'], sec=['fessiers'], qual=['Agilité', 'Réaction'],
    start='3 plots + un partenaire', reps='1 réaction',
    how='Un partenaire face à toi montre à droite ou à gauche au dernier moment (ou crie une couleur de plot). Tu sprintes 3 à 4 m, tu réagis '
        'et tu crochètes vers le bon plot. Seul : une appli de signal aléatoire fait l’affaire.',
    err='Partir avant le signal : on travaille la réaction.'),
 'dribble-sprint': dict(name='Conduite de balle rapide', short='Conduite rapide', eq='ballon', prim=[], sec=[], qual=['Vitesse avec ballon', 'Conduite'],
    start='Ballon + 2 plots', reps='20 m',
    how='Conduis le ballon à pleine vitesse sur 20 m avec des touches longues, puis contrôle-le dans la zone du dernier plot. '
        'Alterne pied fort et pied faible. Bloc 3 : un crochet au plot, puis réaccélère.',
    err='Fixer le ballon : lève la tête entre les touches.'),
 # ---------------- technique (dimanche) et routine du mercredi
 'dribble-slalom': dict(name='Slalom ballon', short='Slalom', eq='ballon', prim=[], sec=[], qual=['Conduite', 'Pied faible'],
    start='6 à 8 plots à 1 m', reps='1 passage',
    how='6 à 8 plots en ligne espacés d’un mètre. Slalome avec le ballon : intérieur-extérieur du même pied, puis de l’autre pied, puis semelle. '
        'Propreté d’abord, vitesse ensuite.',
    err='Toucher les plots : ralentis jusqu’à ce que ce soit propre.'),
 'wall-control': dict(name='Contrôle orienté au mur', short='Contrôle orienté', eq='ballon', prim=[], sec=[], qual=['Contrôle orienté', 'Premier contrôle'],
    start='Un mur + 2 plots', reps='10 par côté',
    how='À 5 m d’un mur, un plot à 45° de chaque côté. Passe au mur, contrôle orienté vers un plot avec l’intérieur (puis l’extérieur) du pied, '
        'et repasse au mur depuis ce plot. Une touche pour orienter, une pour passer.',
    err='Contrôler le ballon sous toi : oriente-le dans ta course.'),
 'weak-foot-wall': dict(name='Pied faible au mur', short='Pied faible', eq='ballon', prim=[], sec=[], qual=['Pied faible', 'Passe'],
    start='Un mur', reps='20 passes',
    how='À 4 à 6 m d’un mur, passes uniquement du pied faible : intérieur du pied, puis contrôle et passe, puis en une touche. '
        'Recule d’un mètre quand c’est propre.',
    err='Repasser sur le bon pied dès que ça devient dur.'),
 'dribble-shot': dict(name='Dribble et frappe', short='Dribble + frappe', eq='ballon', prim=[], sec=[], qual=['Finition', 'Dribble'],
    start='Ballon, 1 plot, un but ou une cible', reps='1 action',
    how='Conduis vers un plot, crochète (intérieur ou extérieur), puis frappe au but ou dans une cible. Alterne les côtés et le pied de frappe.',
    err='Frapper sans regarder la cible.'),
 'dribble-intervals': dict(name='Intervalles ballon 15/15', short='Intervalles', eq='ballon', prim=[], sec=[], qual=['Endurance', 'Répétition des efforts'],
    start='Carré de 15 m', reps='8 × 15 s',
    how='Dans un carré de 15 m, conduis le ballon 15 s à fond (crochets, accélérations), puis 15 s de conduite lente. 8 fois = 1 série. '
        '2 minutes de repos entre les séries.',
    err='Partir trop vite et finir en marchant : garde le même rythme du début à la fin.'),
}
for k, v in NEW.items():
    v.setdefault('sec', []); v.setdefault('prim', [])
    EX[k] = v

KINDS = {'force': 'Force', 'power': 'Puissance', 'core': 'Gainage', 'plyo': 'Sauts', 'sprint': 'Vitesse', 'cod': 'Appuis',
         'ball': 'Ballon', 'prev': 'Prévention', 'cardio': 'Récup'}

# pas de charge par matériel (kg)
STEP = {'halteres': 2, 'machine': 2.5, 'medball': 1}
for k, e in EX.items():
    e['step'] = STEP.get(e['eq'], 0)
    if 'Contrepoids' in e.get('start', ''):
        e['neg'] = True; e['step'] = 5
    if k in ('smith-bench', 'smith-incline', 'smith-squat', 'smith-rdl'):
        e['step'] = 2.5
    if k == 'suitcase-carry':
        e['step'] = 2
    if e['eq'] in ('pdc', 'box', 'terrain', 'ballon', 'velo'):
        e['step'] = 0
    if k == 'smith-inverted-row':
        e['step'] = 0
    if k == 'calf-raise-sl':
        e['step'] = 2
    if k in ('db-bench', 'incline-press', 'rdl', 'step-up', 'lateral-step-up', 'standing-db-press', 'incline-db-row', 'close-grip-db-press'):
        e['pair'] = True

# ---------------------------------------------------------------- séances (version simple)
def S(id, ex, alts, kind, b1, b2, b3, note=None):
    """b1/b2/b3 : (séries, répétitions, repos en s, effort) pour les semaines 1–4, 5–8, 9–12."""
    return dict(id=id, ex=ex, alts=alts, kind=kind, p=[b1, b2, b3], test=False, note=note)

WARMUP = {
    'haut': ['5 min de vélo ou de rameur', 'Rotations des épaules : 10 vers l’avant, 10 vers l’arrière', '1 série légère du premier exercice'],
    'bas': ['5 min de vélo', '10 squats sans charge', '10 balancements de jambe de chaque côté'],
    'vitesse': ['5 min de footing léger', 'Montées de genoux et talons-fesses : 2 × 15 m', '3 accélérations sur 30 m, de plus en plus vite'],
    'technique': ['5 min de conduite de balle tranquille', '10 balancements de jambe de chaque côté'],
    'match': ['5 min de footing léger', 'Montées de genoux, talons-fesses, pas chassés', '5 min de passes et de contrôles', '3 accélérations de 20 m, de plus en plus vite'],
}

DAYS = [
    dict(key='lundi', dow=1, kind='gym', name='Haut du corps A', tag='Haut A', theme='Pecs, dos, épaules', col='hautA', dur='45 min', warm='haut',
         slots=[
            S('a1', 'db-bench', ['chest-press'], 'force', (3, '10', 120, '7/10'), (4, '8', 150, '8/10'), (4, '6', 150, '8/10')),
            S('a2', 'assisted-pullup', ['smith-inverted-row'], 'force', (3, '8', 120, '7/10'), (4, '6–8', 150, '8/10'), (4, '5–6', 150, '8/10')),
            S('a3', 'shoulder-press', ['machine-shoulder-press'], 'force', (3, '10', 90, '7/10'), (3, '8', 120, '8/10'), (3, '6–8', 120, '8/10')),
            S('a4', 'db-row', ['machine-row'], 'force', (3, '10 par bras', 90, '7/10'), (3, '8 par bras', 90, '8/10'), (4, '8 par bras', 90, '8/10')),
            S('a5', 'pushup', [], 'force', (2, '10', 60, '7/10'), (3, '12', 60, '8/10'), (3, '10, en poussant vite', 60, '8/10')),
            S('a6', 'plank', [], 'core', (3, '30 s', 45, 'Contrôle'), (3, '40 s', 45, 'Contrôle'), (3, '45 s', 45, 'Contrôle')),
         ]),
    dict(key='mardi', dow=2, kind='gym', name='Bas du corps', tag='Bas', theme='Jambes, fessiers, ischios', col='bas', dur='50 min', warm='bas',
         note='Foot demain : arrête chaque série avec 2 répétitions en réserve.',
         slots=[
            S('b1', 'cmj', [], 'plyo', (3, '5', 90, 'À fond'), (4, '5', 90, 'À fond'), (4, '5', 90, 'À fond')),
            S('b2', 'goblet-squat', ['leg-press'], 'force', (3, '10', 120, '7/10'), (4, '8', 150, '8/10'), (4, '6', 150, '8/10')),
            S('b3', 'rdl', ['smith-rdl'], 'force', (3, '10', 120, '7/10'), (4, '8', 120, '8/10'), (4, '6–8', 150, '8/10')),
            S('b4', 'step-up', [], 'force', (3, '8 par jambe', 90, '7/10'), (3, '8 par jambe', 90, '8/10'), (3, '6 par jambe', 90, '8/10')),
            S('b5', 'leg-curl', ['lying-leg-curl'], 'force', (3, '10', 90, '7/10'), (3, '10', 90, '8/10'), (3, '8', 90, '8/10')),
            S('b6', 'machine-calf', ['calf-raise-sl'], 'force', (3, '15', 60, '7/10'), (3, '12', 60, '8/10'), (3, '12', 60, '8/10')),
         ]),
    dict(key='mercredi', dow=3, kind='foot', name='Entraînement collectif', tag='Foot', theme='Avec ton équipe', col='foot', dur='',
         text='Ton entraînement avec l’équipe. Rien d’autre à faire aujourd’hui : arrive frais et joue à fond.'),
    dict(key='jeudi', dow=4, kind='recup', name='Récupération', tag='Récup', theme='Vélo et étirements', col='recup', dur='30 min',
         items=[
            dict(id='r1', ex='easy-bike', txt='Vélo facile : 20 min'),
            dict(id='r2', ex=None, txt='Étirements : 10 min', list=['Mollets contre un mur : 30 s par jambe', 'Arrière des cuisses, talon sur un banc : 30 s par jambe',
                                                                     'Devant des cuisses, debout, talon vers les fesses : 30 s par jambe', 'Hanches, un genou au sol : 30 s par côté']),
         ]),
    dict(key='vendredi', dow=5, kind='speed', name='Vitesse', tag='Vitesse', theme='Sprints et changements de direction', col='vitesse', dur='40 min', warm='vitesse',
         place='Un terrain, 6 plots, un ballon',
         note='Match dimanche ? Fais 2 répétitions de moins sur chaque exercice.',
         slots=[
            S('v1', 'broad-jump', [], 'plyo', (3, '3', 90, 'À fond'), (3, '3', 90, 'À fond'), (3, '3', 90, 'À fond')),
            S('v2', 'starts-10', [], 'sprint', (6, '10 m', 60, 'Vite'), (6, '10 m', 60, 'À fond'), (8, '10 m', 60, 'À fond')),
            S('v3', 'sprint-20', [], 'sprint', (4, '20 m', 120, 'Vite'), (5, '20 m', 120, 'À fond'), (5, '20 m', 120, 'À fond')),
            S('v4', 'decel', [], 'cod', (4, '10 m + arrêt', 60, 'Vite'), (5, '10 m + arrêt', 60, 'À fond'), (5, '10 m + arrêt', 60, 'À fond')),
            S('v5', 'cut-45', [], 'cod', (6, '5 m + 5 m', 60, 'Vite'), (6, '5 m + 5 m', 60, 'À fond'), (8, '5 m + 5 m', 60, 'À fond')),
            S('v6', 'dribble-sprint', [], 'ball', (4, '20 m', 60, 'Vite'), (4, '20 m', 60, 'À fond'), (4, '20 m', 60, 'À fond')),
         ]),
    dict(key='samedi', dow=6, kind='gym', name='Haut du corps B', tag='Haut B', theme='Pecs, dos, bras, abdos', col='hautB', dur='45 min', warm='haut',
         note='Match demain ? 2 séries par exercice, sans forcer.',
         slots=[
            S('c1', 'incline-press', ['smith-incline'], 'force', (3, '10', 120, '7/10'), (4, '8', 150, '8/10'), (4, '6', 150, '8/10')),
            S('c2', 'assisted-pullup', ['smith-inverted-row'], 'force', (3, '8', 120, '7/10'), (3, '6–8', 120, '8/10'), (4, '5–6', 150, '8/10')),
            S('c3', 'dips', ['assisted-dip-machine'], 'force', (3, '8', 90, '7/10'), (3, '10', 90, '8/10'), (3, '10', 90, '8/10')),
            S('c4', 'machine-row', ['db-row'], 'force', (3, '10', 90, '7/10'), (3, '10', 90, '8/10'), (4, '8', 90, '8/10')),
            S('c5', 'leg-raise', [], 'core', (3, '12', 45, 'Contrôle'), (3, '15', 45, 'Contrôle'), (3, '15', 45, 'Contrôle')),
            S('c6', 'crunch', [], 'core', (3, '15', 45, 'Contrôle'), (3, '20', 45, 'Contrôle'), (3, '20', 45, 'Contrôle')),
         ]),
    dict(key='dimanche', dow=0, kind='sunday', name='Match ou technique', tag='Dimanche', theme='', col='match', dur='',
         match=dict(name='Jour de match', tag='Match', col='match', theme='Prépare-toi bien',
                    before=['Repas 3 h avant le match (pâtes et poulet)', 'Une banane 1 h avant', 'Échauffement de 15 à 20 min'],
                    after=['Mange un vrai repas dans l’heure (avec ta whey)', '5 min d’étirements', 'Couche-toi tôt']),
         tech=dict(name='Technique', tag='Technique', col='tech', theme='Ballon : conduite, contrôle, pied faible', dur='40 min', warm='technique',
                   place='Un ballon, 6 plots, un mur',
                   slots=[
                      S('t1', 'dribble-slalom', [], 'ball', (4, '1 passage par pied', 45, 'Propre'), (5, '1 passage par pied', 45, 'Vite'), (5, '1 passage par pied', 45, 'Vite')),
                      S('t2', 'weak-foot-wall', [], 'ball', (3, '20 passes', 30, 'Propre'), (3, '25 passes', 30, 'Propre'), (3, '25 passes', 30, 'Propre')),
                      S('t3', 'wall-control', [], 'ball', (3, '10 par côté', 30, 'Propre'), (3, '10 par côté', 30, 'Propre'), (3, '10 par côté', 30, 'Vite')),
                      S('t4', 'juggling', [], 'ball', (1, '5 min', 0, 'Record'), (1, '5 min', 0, 'Record'), (1, '5 min', 0, 'Record')),
                   ])),
]

# textes simples : exécution, conseil, à éviter
TEXT = {
 'db-bench': ('Allongé sur un banc plat, un haltère dans chaque main au-dessus de la poitrine. Descends les haltères sur les côtés de la poitrine, puis pousse vers le haut.',
              'Pieds bien à plat, omoplates serrées contre le banc.', 'Écarter les coudes à l’horizontale : garde-les un peu rentrés.'),
 'chest-press': (None, 'Règle le siège pour avoir les poignées à hauteur de poitrine.', None),
 'assisted-pullup': ('Genoux sur la plateforme, mains un peu plus larges que les épaules. Tire jusqu’à passer le menton au-dessus des poignées, puis redescends bras tendus.',
                     'Plus il y a de contrepoids, plus c’est facile. Enlève 5 kg quand tu fais toutes tes répétitions.', 'Te balancer ou donner des coups de reins pour monter.'),
 'smith-inverted-row': (None, 'Corps droit des talons aux épaules. Plus la barre est basse, plus c’est dur.', None),
 'shoulder-press': (None, 'Garde le dos collé au dossier et le ventre serré.', None),
 'machine-shoulder-press': (None, 'Poignées à hauteur des épaules au départ.', None),
 'db-row': (None, 'Tire le coude vers la hanche, pas vers le plafond.', None),
 'machine-row': (None, 'Serre les omoplates en fin de mouvement, 1 seconde.', None),
 'pushup': (None, 'Corps droit comme une planche, mains sous les épaules.', None),
 'plank': (None, 'Serre les fesses et le ventre, et respire normalement.', None),
 'cmj': ('Pieds écartés à largeur de hanches. Plie vite les genoux en lançant les bras en arrière, puis saute le plus haut possible en lançant les bras vers le haut.',
         'Atterris en douceur, genoux souples, puis prends 2 secondes avant le saut suivant.', 'Genoux qui rentrent vers l’intérieur à l’atterrissage.'),
 'goblet-squat': ('Tiens un haltère contre la poitrine, pieds un peu plus larges que les épaules. Descends comme pour t’asseoir, cuisses parallèles au sol, puis remonte.',
                  'Talons collés au sol, genoux dans l’axe des pieds.', 'Arrondir le dos ou décoller les talons.'),
 'leg-press': (None, 'Ne verrouille jamais les genoux en haut.', None),
 'rdl': (None, 'Pense à pousser les fesses en arrière, pas à descendre le dos.', None),
 'smith-rdl': (None, 'Pense à pousser les fesses en arrière.', None),
 'step-up': ('Face à un banc stable, un haltère dans chaque main. Pose tout le pied sur le banc et monte en poussant sur ce pied, puis redescends doucement.',
             'Pousse sur le talon du pied posé sur le banc, pas sur l’autre jambe.', 'Te pencher en avant ou t’aider de la jambe au sol.'),
 'leg-curl': (None, 'Redescends lentement, en 3 secondes : ça protège tes ischios.', None),
 'lying-leg-curl': (None, 'Redescends lentement, en 3 secondes.', None),
 'machine-calf': (None, 'Monte le plus haut possible et tiens 1 seconde en haut.', None),
 'calf-raise-sl': (None, 'Une main sur un support pour l’équilibre.', None),
 'easy-bike': ('Vélo d’appartement ou de salle, résistance légère, 20 minutes.', 'Tu dois pouvoir parler sans être essoufflé.', 'Accélérer : aujourd’hui, on récupère.'),
 'broad-jump': (None, 'Atterris sur les deux pieds et tiens 2 secondes sans bouger.', None),
 'starts-10': ('Départ debout, un pied devant. Penche-toi en avant et pousse fort dans le sol pendant 10 m. Reviens en marchant.',
               'Reste penché les 5 premiers mètres, et pousse fort avec les bras.', 'Te redresser tout de suite.'),
 'sprint-20': ('Plots à 0 et à 20 m. Pars arrêté et sprinte jusqu’au plot des 20 m. Reviens en marchant.',
               'Prends le repos en entier : chaque sprint doit être aussi rapide que le premier.', 'Raccourcir le repos.'),
 'decel': (None, 'Petits pas, hanches basses, comme pour t’asseoir.', None),
 'cut-45': (None, 'Baisse-toi juste avant le plot et pousse sur le pied extérieur.', None),
 'dribble-sprint': (None, 'Touches longues quand c’est libre, lève la tête entre les touches.', None),
 'incline-press': (None, 'Banc incliné à 30° environ, pas plus.', None),
 'smith-incline': (None, 'Banc incliné à 30° environ.', None),
 'dips': (None, 'Descends jusqu’à avoir les coudes à angle droit, pas plus bas.', None),
 'assisted-dip-machine': (None, 'Plus de contrepoids = plus facile.', None),
 'leg-raise': (None, 'Plaque le bas du dos au sol pendant tout le mouvement.', None),
 'crunch': (None, 'Décolle seulement les épaules, regard vers le plafond.', None),
 'dribble-slalom': ('6 plots en ligne, espacés d’un mètre. Slalome entre les plots avec le ballon, une fois du pied droit, une fois du pied gauche.',
                    'Petites touches, le ballon reste près du pied.', 'Aller trop vite et toucher les plots.'),
 'weak-foot-wall': ('À 4 ou 5 m d’un mur, fais des passes uniquement avec ton pied faible : contrôle, puis passe.',
                    'Recule d’un mètre quand ça devient facile.', 'Repasser sur ton bon pied.'),
 'wall-control': ('Passe au mur. Quand le ballon revient, contrôle-le vers la droite ou vers la gauche pour l’emmener dans ta course, puis repasse.',
                  'Le premier contrôle doit déjà t’emmener vers l’avant.', 'Contrôler le ballon sous tes pieds.'),
 'juggling': ('Jongle avec les pieds, en alternant droit et gauche.', 'Compte ta meilleure série : c’est ton record à battre.', 'Jongler uniquement du bon pied.'),
}
for k, (how, tip, err) in TEXT.items():
    if k not in EX: continue
    if how: EX[k]['how'] = how
    if err: EX[k]['err'] = err
    EX[k]['tip'] = tip
EX['starts-10']['name'] = 'Sprint 10 m'
EX['decel']['name'] = 'Freinage'
EX['cut-45']['name'] = 'Changements de direction'
EX['dribble-sprint']['name'] = 'Conduite de balle rapide'
EX['plank']['reps'] = '30 s'

READY = [
    dict(k='sleep', q='Ta nuit ?', a=[['Mauvaise', 'moins de 6 h'], ['Moyenne', '6 à 7 h'], ['Bonne', '7 h ou plus']]),
    dict(k='legs', q='Tes jambes ?', a=[['Lourdes', 'courbatures'], ['Fatiguées', 'un peu'], ['Fraîches', 'prêtes']]),
    dict(k='energy', q='Ton énergie ?', a=[['À plat', 'pas envie'], ['Normale', 'ça va'], ['À bloc', 'motivé']]),
]

TESTDEF = [
    dict(k='t10', name='Sprint 10 m', unit='s', low=True, how='Départ arrêté, un pied devant. 2 essais, 3 min de repos, garde le meilleur.'),
    dict(k='t20', name='Sprint 20 m', unit='s', low=True, how='Même départ. 2 essais, 3 min de repos, garde le meilleur.'),
    dict(k='broad', name='Saut en longueur sans élan', unit='cm', low=False, how='3 essais, mesure de la ligne de départ au talon le plus proche.'),
    dict(k='cod', name='Demi-tour 5-0-5', unit='s', low=True, how='2 essais par côté, garde le meilleur.'),
    dict(k='jongle', name='Jongles (meilleure série)', unit='', low=False, how='Ton record de la semaine, pieds et cuisses.'),
]
TEST_NOTE = ('Chrono : un ami au départ et à l’arrivée, ou une vidéo au ralenti. Prends toujours la même méthode et le même terrain, '
             'sinon les temps ne sont pas comparables.')

def used():
    u = set()
    for d in DAYS:
        for sl in d.get('slots', []) + (d.get('tech') or {}).get('slots', []):
            u.update([sl['ex']] + sl['alts'])
        for it in d.get('items', []):
            if it['ex']: u.add(it['ex'])
    return u

REMOVED = [
    ('Élévations latérales (×2)', 'Exercice esthétique, sans transfert sur le terrain. Les épaules travaillent déjà avec les développés et le développé à genou.'),
    ('Extension triceps', 'Les triceps travaillent déjà avec les développés, les dips et les lancers de médecine-ball.'),
    ('Oiseau à la machine', 'Remplacé par deux rowings lourds par semaine, plus utiles pour tenir un adversaire.'),
    ('Curl biceps (×2)', 'Les tractions et les rowings suffisent largement pour les biceps d’un footballeur.'),
    ('Crunch', 'Remplacé par du gainage qui résiste aux rotations et aux poussées : dead bug, marche valise, touches d’épaule.'),
]

if __name__ == '__main__':
    used = set()
    for d in DAYS:
        for sl in d.get('slots', []) + d.get('pre', []) + (d.get('tech') or {}).get('slots', []):
            used.update([sl['ex']] + sl['alts'])
        for it in d.get('items', []):
            if it['ex']: used.add(it['ex'])
    missing = used - set(EX)
    print('exercices utilisés', len(used), 'manquants', missing)
    print('inutilisés', set(EX) - used)
