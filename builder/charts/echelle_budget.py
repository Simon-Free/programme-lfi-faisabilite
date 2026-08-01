"""Le programme rapporte aux finances publiques existantes.

Un montant sans repere ne dit rien : « 460 milliards » ne se lit qu'en
sachant que la depense publique francaise vaut 1 714 milliards. Cette
figure donne l'echelle, puis l'effet sur le deficit.

Tous les libelles derivent des constantes ci-dessous. Le consolide a deja
bouge trois fois : un texte fige finirait par contredire la barre qu'il
legende.

Chiffres : PIB et depense publique de `transverses/09` (corrections 5 et 7),
depense nouvelle de `transverses/20` (total consolide), ressources de
`transverses/25` § 4, deficit courant de `transverses/11` § 6.
"""

from .bars import barres
from .base import figure, legende, nombre, table
from .figures import heros

PIB = 2993.0
DEPENSE_PUBLIQUE = 1714.1
# Deficit courant : valeur retenue par `vulgarise/chiffrage.md`, section
# « Les ordres de grandeur ». 152,5 / 2 993 = 5,1 % — les deux concordent.
DEFICIT_MONTANT = 152.5
DEFICIT_PART = DEFICIT_MONTANT / PIB * 100
# Chaine de calcul, verifiee sur `transverses/20` ligne TOTAL :
#   448,2  somme des chapitres, apres les corrections des transverses 22 et 28
#  +12,2   consolidation des postes 6-10 (consolidation/p1_postes_06-10)
#   460,4  total courant, « 460 arrondi »
# Le 472 qui circule ailleurs comptait la consolidation deux fois : il prenait
# 460,4 pour la base auditee et lui rajoutait les memes 12,2.
PROGRAMME = 460.4           # depense nouvelle recurrente, consolidee
RESSOURCES = 86.9
EDUCATION = 197.1
CHARGE_DETTE = 54.4

SOLDE = PROGRAMME - RESSOURCES
POINTS_PIB = SOLDE / PIB * 100
PART_DEPENSE = PROGRAMME / DEPENSE_PUBLIQUE * 100
DEFICIT_APRES = DEFICIT_PART + POINTS_PIB
COUVERTURE = RESSOURCES / PROGRAMME * 100

SOURCE = (
    "Sources : Insee, comptes nationaux 2025 (PIB, dépense publique) ; "
    "Cour des comptes et Sénat pour la charge de la dette ; DEPP pour la "
    "dépense d'éducation. Montants du programme : transverses 20 et 25."
)


def _echelle():
    return [
        {"libelle": "Dépense publique française, toutes administrations",
         "bas": DEPENSE_PUBLIQUE, "serie": 1,
         "note": "État, sécurité sociale et collectivités réunis, en 2025."},
        {"libelle": "Dépense nouvelle demandée par le programme",
         "bas": PROGRAMME, "serie": 2,
         "note": "Récurrent, en régime de croisière. Soit %s %% de la "
                 "dépense publique actuelle en plus." % nombre(PART_DEPENSE, 1)},
        {"libelle": "Dépense intérieure d'éducation", "bas": EDUCATION,
         "serie": 3,
         "note": "Tout l'enseignement, de la maternelle au supérieur, tous "
                 "financeurs. Le programme demande %s fois cette somme."
                 % nombre(PROGRAMME / EDUCATION, 1)},
        {"libelle": "Déficit public actuel", "bas": DEFICIT_MONTANT,
         "serie": 4,
         "note": "%s %% du PIB. C'est déjà au-delà du seuil européen de 3 %%."
                 % nombre(DEFICIT_PART, 1)},
        {"libelle": "Ressources nouvelles du programme", "bas": RESSOURCES,
         "serie": 6,
         "note": "Recettes et économies réunies. Elles couvrent %s %% de la "
                 "dépense demandée." % nombre(COUVERTURE, 1)},
        {"libelle": "Charge de la dette, 2025", "bas": CHARGE_DETTE,
         "serie": 7,
         "note": "Les seuls intérêts. Programmée à 91,8 Md€ en 2029, sans le "
                 "programme."},
    ]


def _deficit():
    return [
        {"libelle": "Déficit public aujourd'hui", "bas": DEFICIT_PART,
         "serie": 1,
         "note": "%s Md€. La France est sous procédure de déficit excessif "
                 "depuis 2024." % nombre(DEFICIT_MONTANT, 1)},
        {"libelle": "Seuil européen", "bas": 3.0, "serie": 6,
         "note": "3 % du PIB : la limite fixée par les traités, dépassée "
                 "depuis plusieurs exercices."},
        {"libelle": "Déficit après exécution du programme",
         "bas": DEFICIT_APRES, "serie": 8,
         "note": "Les %s %% actuels, plus les %s points que représente le "
                 "solde de %s Md€ à combler."
                 % (nombre(DEFICIT_PART, 1), nombre(POINTS_PIB, 1),
                    nombre(SOLDE, 1))},
    ]


def echelle_budget():
    corps = (
        heros(
            "+%s %%" % nombre(PART_DEPENSE, 1),
            "de dépense publique en plus",
            "%s Md€/an ajoutés à une dépense publique de %s Md€"
            % (nombre(PROGRAMME, 1), nombre(DEPENSE_PUBLIQUE, 1)),
        )
        + legende([
            ("mark--1", "Dépense publique existante"),
            ("mark--2", "Demandé par le programme"),
            ("mark--8", "Situation après exécution"),
        ])
        + barres(_echelle(), unite="Md€/an")
        + '<p class="chart__note">Et sur le déficit, en points de PIB :</p>'
        + barres(_deficit(), unite="% du PIB")
    )
    donnees = table(
        ["Grandeur", "Montant"],
        [
            ["Produit intérieur brut", "%s Md€" % nombre(PIB)],
            ["Dépense publique, toutes administrations",
             "%s Md€" % nombre(DEPENSE_PUBLIQUE, 1)],
            ["Dépense nouvelle du programme",
             "%s Md€/an" % nombre(PROGRAMME, 1)],
            ["Part de la dépense publique actuelle",
             "%s %%" % nombre(PART_DEPENSE, 1)],
            ["Ressources nouvelles", "%s Md€/an" % nombre(RESSOURCES, 1)],
            ["Solde à combler", "%s Md€/an, soit %s points de PIB"
             % (nombre(SOLDE, 1), nombre(POINTS_PIB, 1))],
            ["Déficit public actuel", "%s %% du PIB, soit %s Md€"
             % (nombre(DEFICIT_PART, 1), nombre(DEFICIT_MONTANT, 1))],
            ["Déficit après exécution",
             "%s %% du PIB" % nombre(DEFICIT_APRES, 1)],
            ["Charge de la dette 2025", "%s Md€" % nombre(CHARGE_DETTE, 1)],
        ],
        "Le programme rapporté aux finances publiques françaises.",
    )
    return figure(
        "echelle-budget",
        "Le programme ajoute un quart à la dépense publique, et triple le déficit",
        "Les %s milliards par an demandés s'ajoutent à une dépense publique de "
        "%s milliards : c'est un quart de plus. Les ressources nouvelles en "
        "couvrent moins d'un cinquième, de sorte que le déficit public "
        "passerait de %s %% à %s %% du produit intérieur brut."
        % (nombre(PROGRAMME, 1), nombre(DEPENSE_PUBLIQUE, 1),
           nombre(DEFICIT_PART, 1), nombre(DEFICIT_APRES, 1)),
        corps,
        donnees,
        SOURCE,
        note="Les montants récurrents et les investissements ne s'additionnent "
             "pas : cette figure ne porte que le récurrent.",
    )
