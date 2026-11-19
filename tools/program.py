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

KEEP = ['db-bench', 'chest-press', 'smith-bench', 'assisted-pullup', 'smith-inverted-row', 'db-pullover',
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

# ---------------------------------------------------------------- séances
def S(id, ex, alts, kind, b1, b2, b3, test=False, note=None):
    """b1/b2/b3 : (séries, répétitions, repos en s, effort) pour les semaines 1–4, 5–8, 9–12 (None = pas dans ce bloc)."""
    return dict(id=id, ex=ex, alts=alts, kind=kind, p=[b1, b2, b3], test=test, note=note)

WARMUP = {
    'haut': ['5 min de vélo ou de rameur, rythme facile', '10 rotations d’épaules vers l’avant, puis vers l’arrière',
             '10 pompes (mains sur un banc si besoin)', '1 série légère du premier exercice de force (la moitié de la charge)'],
    'bas': ['5 min de vélo, rythme facile', '10 squats au poids du corps', '10 balancements de jambe d’avant en arrière, puis de côté, par jambe',
            '10 petits sauts sur place, souples', '1 série légère du squat (la moitié de la charge)'],
    'vitesse': ['3 min de footing léger', 'Montées de genoux, puis talons-fesses : 2 × 15 m chacun', 'Pas chassés : 2 × 15 m de chaque côté',
                'Skippings : 2 × 15 m', '3 accélérations progressives de 30 m (60 %, 75 %, 90 %)'],
    'technique': ['5 min de conduite libre et de jonglages', 'Balancements de jambes et ouvertures de hanche : 10 par jambe',
                  '2 accélérations de 20 m avec ballon, à 70 %'],
    'match': ['5 min de footing léger avec ouvertures et fermetures de hanche', 'Mobilité : balancements de jambes, talons-fesses, montées de genoux',
              '5 min de passes et contrôles avec ballon', '3 accélérations progressives de 20 m (60 %, 80 %, 90 %)',
              '3 changements de direction à 80 %', '2 sprints de 10 m à fond, puis on garde la chaleur jusqu’au coup d’envoi'],
}

DAYS = [
    dict(key='lundi', dow=1, kind='gym', name='Haut du corps A', tag='Haut A', theme='Force & duels', col='hautA', dur='50 min', warm='haut',
         goal='Gagner tes duels : pousser, tirer, tenir l’adversaire à distance, avec un tronc solide.',
         slots=[
            S('l1', 'mb-chest-throw', ['explosive-pushup'], 'power', (3, '5', 60, 'Explosif'), (3, '5', 60, 'Explosif'), (4, '4', 75, 'Explosif')),
            S('l2', 'db-bench', ['chest-press', 'smith-bench'], 'force', (3, '8–10', 120, '7/10'), (4, '6–8', 150, '8/10'), (3, '4–6', 180, '8/10')),
            S('l3', 'assisted-pullup', ['smith-inverted-row', 'db-pullover'], 'force', (3, '6–8', 120, '7/10'), (4, '5–6', 150, '8/10'), (3, '4–6', 150, '8/10')),
            S('l4', 'hk-press', ['machine-shoulder-press', 'standing-db-press'], 'force', (3, '8–10 par bras', 75, '7/10'), (3, '6–8 par bras', 90, '8/10'), (3, '6 par bras', 90, '8/10')),
            S('l5', 'db-row', ['machine-row', 'incline-db-row'], 'force', (3, '8–10 par bras', 75, '7/10'), (4, '6–8 par bras', 90, '8/10'), (3, '6–8 par bras', 90, '8/10, tirage rapide')),
            S('l6', 'dead-bug', ['reverse-crunch', 'flutter-kicks'], 'core', (2, '8 par côté', 45, 'Contrôle'), (3, '10 par côté', 45, 'Contrôle'), (3, '10 par côté, lent', 45, 'Contrôle')),
            S('l7', 'suitcase-carry', ['side-plank'], 'core', (2, '20 m par côté', 60, '7/10'), (3, '20 m par côté', 60, '8/10'), (3, '25 m par côté', 60, '8/10')),
         ]),
    dict(key='mardi', dow=2, kind='gym', name='Bas du corps', tag='Bas', theme='Force & puissance', col='bas', dur='55 min', warm='bas',
         goal='Des jambes fortes et explosives, des ischios et des mollets blindés contre les blessures.',
         note='Entraînement collectif demain : arrête chaque série avec 2 à 3 répétitions en réserve, jamais à l’échec.',
         slots=[
            S('m1', 'box-jump', ['cmj'], 'plyo', (3, '3', 90, 'Explosif'), (4, '3', 90, 'Explosif'), (4, '3', 90, 'Explosif')),
            S('m2', 'goblet-squat', ['smith-squat', 'leg-press'], 'force', (3, '8–10', 120, '7/10'), (4, '6–8', 150, '8/10'), (3, '4–6', 180, '8/10, montée rapide')),
            S('m3', 'rdl', ['smith-rdl', 'db-hip-thrust'], 'force', (3, '8–10', 120, '7/10'), (4, '6–8', 120, '8/10'), (3, '5–6', 150, '8/10')),
            S('m4', 'step-up', ['lateral-step-up', 'single-leg-press'], 'force', (3, '8 par jambe', 75, '7/10'), (3, '6–8 par jambe', 90, '8/10'), (3, '5 par jambe', 90, 'Montée explosive')),
            S('m5', 'nordic', ['leg-curl-ecc', 'single-leg-rdl'], 'prev', (2, '3–4', 120, 'Descente lente'), (3, '4–5', 120, 'Descente lente'), (2, '5', 120, 'Descente lente')),
            S('m6', 'calf-raise-sl', ['machine-calf', 'seated-calf'], 'force', (3, '12 par jambe', 60, '7/10'), (3, '8–10 par jambe', 60, '8/10, avec haltère'), (3, '10 par jambe', 60, 'Montée explosive')),
         ]),
    dict(key='mercredi', dow=3, kind='foot', name='Entraînement collectif', tag='Foot', theme='Avec l’équipe', col='foot', dur='Selon ton club',
         goal='Ta séance la plus importante de la semaine. Arrive frais, joue à fond.',
         pre=[
            S('w1', 'weak-foot-wall', [], 'ball', (2, '20 passes', 30, 'Qualité'), (2, '25 passes', 30, 'Qualité'), (2, '25 passes, 1 touche', 30, 'Qualité')),
            S('w2', 'wall-control', [], 'ball', (2, '5 par côté', 30, 'Qualité'), (2, '8 par côté', 30, 'Qualité'), (2, '10 par côté', 30, 'Qualité')),
         ]),
    dict(key='jeudi', dow=4, kind='recup', name='Récupération', tag='Récup', theme='Récupérer & prévenir', col='recup', dur='35 min',
         goal='Relancer la circulation, garder des hanches mobiles et blinder adducteurs et chevilles.',
         items=[
            dict(id='r1', ex='easy-bike', txt='Vélo facile 20 à 25 min (effort 3/10)'),
            dict(id='r2', ex=None, txt='Mobilité 10 min', list=['Hanches en 90/90 : 2 × 30 s par côté', 'Fléchisseurs de hanche (genou au sol) : 2 × 30 s par côté',
                                                                 'Mollets contre un mur : 2 × 30 s par jambe', 'Ischios, talon sur un banc : 2 × 30 s par jambe',
                                                                 'Rotations du haut du dos à quatre pattes : 10 par côté']),
            dict(id='r3', ex='copenhagen', txt='Copenhague', p=['2 × 15–20 s par côté, genou sur le banc', '3 × 20 s par côté, genou sur le banc', '3 × 20–25 s par côté, cheville sur le banc']),
            dict(id='r4', ex='single-leg-balance', txt='Équilibre sur une jambe : 2 × 30 s par jambe'),
            dict(id='r5', ex='calf-iso', txt='Mollets tenus : 2 × 30 s par jambe'),
            dict(id='r6', ex='juggling', txt='Jonglages 10 min, sans forcer (bonus)'),
            dict(id='r7', ex=None, txt='Ce soir : 8 h de sommeil, écran coupé 30 min avant'),
         ]),
    dict(key='vendredi', dow=5, kind='speed', name='Vitesse & appuis', tag='Vitesse', theme='Explosivité · freinages · changements de direction', col='vitesse',
         dur='50 min', warm='vitesse', place='Terrain ou herbe, 30 m de long, 6 plots, un ballon',
         goal='Gagner les 5 premiers mètres, freiner plus court, changer de direction plus vite que ton adversaire.',
         slots=[
            S('v1', 'pogo', [], 'plyo', (2, '10', 60, 'Réactif'), (2, '15', 60, 'Réactif'), (2, '15', 60, 'Réactif')),
            S('v2', 'broad-jump', [], 'plyo', (3, '3', 90, 'Max'), (3, '3', 90, 'Max'), None, test=True),
            S('v3', 'drop-jump', [], 'plyo', None, None, (3, '4', 90, 'Contact court')),
            S('v4', 'skater', [], 'plyo', (2, '4 par côté', 60, 'Réception tenue 2 s'), (3, '4 par côté', 60, 'Plus loin'), (2, '4 par côté', 60, 'Rebond immédiat')),
            S('v5', 'bounds', [], 'plyo', None, (2, '4 par jambe', 90, 'Max'), (3, '4 par jambe', 90, 'Max')),
            S('v6', 'starts-10', [], 'sprint', (6, '10 m', 60, '90 %'), (6, '10 m', 75, '100 %'), (6, '10 m, départ sur signal', 75, '100 %'), test=True),
            S('v7', 'sprint-20', ['hill-sprint'], 'sprint', (4, '20 m', 120, '90 %'), (5, '20 m', 150, '100 %'), (5, '20 m', 150, '100 %'), test=True),
            S('v8', 'decel', [], 'cod', (4, '10 m + arrêt', 60, '70 %'), (5, '10 m + arrêt', 60, '85 %'), (5, '15 m + arrêt', 75, '100 %')),
            S('v9', 'cut-45', [], 'cod', (6, '5 m + 5 m', 60, '75 %'), None, None),
            S('v10', 'cod-505', [], 'cod', None, (4, '1 aller-retour', 90, '100 %'), None, test=True),
            S('v11', 'reactive-agility', [], 'cod', None, None, (6, '1 réaction', 75, '100 %')),
            S('v12', 'dribble-sprint', [], 'ball', (4, '20 m', 60, '90 %'), (4, '20 m', 60, '100 %'), (4, '20 m + crochet', 60, '100 %')),
         ]),
    dict(key='samedi', dow=6, kind='gym', name='Haut du corps B', tag='Haut B', theme='Puissance & gainage', col='hautB', dur='50 min', warm='haut',
         goal='De la puissance de rotation pour frapper et protéger le ballon, un gainage qui encaisse les contacts.',
         slots=[
            S('s1', 'mb-rotation', ['db-woodchop'], 'power', (3, '5 par côté', 60, 'Explosif'), (3, '5 par côté', 60, 'Explosif'), (4, '4 par côté', 60, 'Explosif')),
            S('s2', 'incline-press', ['smith-incline', 'pushup'], 'force', (3, '8–10', 120, '7/10'), (4, '6–8', 150, '8/10'), (3, '5–6', 150, '8/10')),
            S('s3', 'assisted-pullup', ['smith-inverted-row', 'db-pullover'], 'force', (3, '6–8', 120, '7/10'), (3, '5–6', 150, '8/10'), (3, '4–6', 150, '8/10')),
            S('s4', 'dips', ['assisted-dip-machine', 'close-grip-db-press'], 'force', (3, '6–8', 120, '7/10'), (3, '6–10', 120, '8/10'), (3, '5–8', 120, '8/10')),
            S('s5', 'machine-row', ['incline-db-row', 'smith-inverted-row'], 'force', (3, '10', 90, '7/10'), (3, '8', 90, '8/10'), (3, '6–8', 90, '8/10, tirage rapide')),
            S('s6', 'shoulder-tap-plank', ['plank', 'dead-bug'], 'core', (2, '8 par côté', 45, 'Contrôle'), (3, '10 par côté', 45, 'Contrôle'), (3, '12 par côté', 45, 'Contrôle')),
            S('s7', 'side-plank', ['plank', 'bicycle-crunch'], 'core', (2, '20–30 s par côté', 30, 'Contrôle'), (3, '30 s par côté', 30, 'Contrôle'), (3, '40 s par côté', 30, 'Contrôle')),
            S('s8', 'leg-raise', ['reverse-crunch', 'flutter-kicks'], 'core', (2, '10–12', 45, 'Contrôle'), (3, '12–15', 45, 'Contrôle'), (3, '15', 45, 'Contrôle')),
         ]),
    dict(key='dimanche', dow=0, kind='sunday', name='Match ou technique', tag='Dimanche', theme='Selon ton calendrier', col='match', dur='',
         goal='Jour de match : arrive préparé. Sans match : séance technique avec ballon.',
         match=dict(name='Jour de match', tag='Match', col='match', theme='Prépare-toi, joue, récupère',
                    before=['Repas d’avant-match 3 h avant le coup d’envoi (voir Repas)', 'Collation 1 h avant : une banane, ou du pain avec du miel',
                            '500 ml d’eau dans les 2 h qui précèdent', 'Échauffement de 20 min (liste ci-dessous)'],
                    after=['Dans l’heure : ta dose de whey et un fruit, puis un vrai repas', 'Bois au moins 1 L d’eau dans les 2 h',
                           '5 min de marche et de mobilité légère', 'Couché tôt : le sommeil est ta meilleure récup']),
         tech=dict(name='Technique & conduite de balle', tag='Technique', col='tech', theme='Conduite · contrôle orienté · pied faible', dur='50 min', warm='technique',
                   place='Un ballon, 8 plots, un mur, un but si possible',
                   slots=[
                      S('d1', 'dribble-slalom', [], 'ball', (4, '1 passage par pied', 45, 'Propre'), (5, '1 passage par pied', 45, 'Rapide'), (5, '1 passage par pied', 45, 'Vitesse match')),
                      S('d2', 'wall-control', [], 'ball', (3, '10 par côté', 45, 'Qualité'), (3, '10 par côté, extérieur', 45, 'Qualité'), (3, '10 par côté, en 2 touches', 45, 'Vitesse')),
                      S('d3', 'weak-foot-wall', [], 'ball', (3, '20 passes', 30, 'Qualité'), (3, '25 passes', 30, 'Qualité'), (3, '25 passes en 1 touche', 30, 'Qualité')),
                      S('d4', 'juggling', [], 'ball', (1, '5 min', 0, 'Record'), (1, '5 min', 0, 'Record'), (1, '5 min', 0, 'Record')),
                      S('d5', 'dribble-shot', [], 'ball', (6, '1 action', 30, 'Précision'), (8, '1 action', 30, 'Précision'), (8, '1 action, pied faible une fois sur deux', 30, 'Vitesse')),
                      S('d6', 'dribble-intervals', [], 'ball', (1, '8 × 15 s / 15 s', 120, 'Régulier'), (2, '8 × 15 s / 15 s', 120, 'Régulier'), (2, '10 × 15 s / 15 s', 120, 'Régulier'),
                        note='À partir de la semaine 3'),
                   ])),
]

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
