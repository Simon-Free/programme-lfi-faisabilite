"""Les trois figures du chiffrage : le consolide, les chapitres, les doubles comptes.

Chiffres verifies dans SYNTHESE_GENERALE.md (l. 165-175, 437-460, 476-482) et
JOURNAL_PHASE2.md. La colonne « centrale » du dossier est le milieu de la
fourchette « et rien d'autre » : elle ne porte aucune probabilite, et n'est
donc jamais dessinee comme si elle etait l'estimation.
"""

from .bars import barres
from .base import figure, legende, nombre, table
from .figures import heros, jauge

SOURCE = (
    "Source : synthèse générale, § chiffrage consolidé ; journal de la phase 2. "
    "Fourchettes en euros 2026."
)

CONSOLIDE = [
    # Ligne 12+13 ramenee a 35,0-75,6 (transverses/04 § 2.5 bis) : -6,1 sur la
    # borne basse, -11,25 sur le central, -16,4 sur la borne haute.
    ("Dépenses — littérale, base consolidée", 389, 460, 509, 1),
    ("Dépenses — littérale, chaîne auditée", 389, 448, 509, 1),
    ("Dépenses — variantes appliquées", 334, 384, 434, 1),
    # Ressources : 86,85 jusqu'au 2026-08-01 ; la refonte de la ligne M-6.7
    # (socialisation bancaire) sur le prix d'acquisition reel retire 2,22.
    ("Ressources nouvelles opposables", 29.34, 84.63, 139.93, 3),
    ("dont recettes fiscales nouvelles", -2.26, 33.93, 70.13, 3),
]


def chiffrage_consolide():
    lignes = [
        {
            "libelle": libelle,
            "bas": bas,
            "haut": haut,
            "serie": serie,
            "note": "milieu de fourchette : %s Md€/an" % nombre(central),
        }
        for libelle, bas, central, haut, serie in CONSOLIDE
    ]
    corps = (
        heros(
            "18,4 %",
            "des dépenses nouvelles sont couvertes par une ressource nouvelle",
            "fourchette 6,4 à 30,4 % ; 13,5 % si les économies vont en "
            "réduction de la dépense. Il manque 376 Md€/an",
        )
        + legende([("mark--1", "Dépenses nouvelles"),
                   ("mark--3", "Ressources nouvelles")])
        + barres(lignes, unite="Md€/an")
        + jauge(
            18.4,
            "Moins d’un euro sur cinq",
            "est financé par une ressource nouvelle identifiée. Les quatre "
            "autres ne le sont pas.",
        )
    )
    donnees = table(
        ["Poste", "Bas", "Milieu", "Haut"],
        [
            [libelle, nombre(bas), nombre(central), nombre(haut)]
            for libelle, bas, central, haut, _ in CONSOLIDE
        ]
        + [["<strong>Solde à combler (littérale, base consolidée)</strong>",
            "−431", "<strong>−376</strong>", "−320"],
           ["Solde annuel à combler (variantes appliquées, base 448)", "−251",
            "−340", "−420"]],
        "Dépenses et ressources nouvelles du programme, en Md€/an.",
    )
    return figure(
        "chiffrage-consolide",
        "Les ressources couvrent moins d’un cinquième des dépenses",
        "<strong>Comment lire.</strong> La barre pleine va jusqu'à la borne "
        "basse de la fourchette, la barre claire jusqu'à la borne haute. "
        "Une ligne dont la fourchette enjambe zéro n'a pas cette double "
        "barre : elle est coupée au zéro, la part située à gauche indiquant "
        "que la mesure peut coûter au lieu de rapporter. "
        "Même en retenant la borne haute des ressources et la borne basse des "
        "dépenses, l'écart ne se referme pas.",
        corps,
        donnees,
        SOURCE,
        note="La ligne « ressources nouvelles opposables » réunit les recettes "
        "fiscales du compte complet (33,9), les économies proposées par le "
        "programme et non encore comptées (3,6), les effets de retour "
        "budgétaires (40,0), les dividendes des entités publiques (2,35), la "
        "TVA sur la consommation induite (4,5) et les recettes de sanction "
        "(0,25) — soit 84,6 Md€/an. En face, la dépense récurrente consolidée "
        "vaut 460 Md€/an : l'enveloppe climat des chapitres 12 et 13 y entre "
        "pour 35,0 à 75,6 Md€/an, c'est-à-dire la reconstruction ligne à ligne "
        "des mesures, sans les quatre postes que l'objectif du programme "
        "appellerait mais qu'aucune de ses mesures ne finance. "
        "<strong>Il manque 376 Md€/an, soit 12,6 points de PIB.</strong>",
    )


CHAPITRES = [
    (8, "Travail et retraites", 97.2, 178.5),
    (5, "Éducation, service citoyen", 52, 102),
    (10, "Égalité, grand âge, handicap", 52, 94),
    (7, "Solidarité, logement", 50, 93),
    (9, "Industrie, salaires publics", 37, 56),
    # Enveloppe climat consolidée : reconstruction ligne à ligne de
    # consolidation/p1_postes_01-05.md § 1.8, nette du double compte des
    # cantines (−0,3 / −0,8) et hors clause de complétude, celle-ci mesurant
    # l'objectif du programme et non ses mesures.
    # Arbitrage rendu par transverses/28 § 2 ; voir transverses/04 § 2.5 bis.
    ("12+13", "Écologie et grands chantiers", 35.0, 75.6),
    (15, "Santé (net du gage)", 11, 27),
    (16, "Diplomatie et défense", 9.6, 19.7),
    (11, "Culture et sport", 8.4, 19.3),
    (18, "Mer, espace, numérique", 4, 11.8),
    (3, "Entreprise et communes", 2.44, 7.15),
    (14, "Biens communs (part État)", 2.5, 7.0),
    (17, "Europe (désobéissance ciblée)", 3, 6),
    (2, "Propriété, nationalisations (flux)", 1.40, 4.45),
    (4, "Libertés et justice", 1.45, 3.21),
    (1, "Institutions", 0.29, 0.93),
]

PETITS = CHAPITRES[9:]


def _lignes_chapitres(source):
    return [
        {
            "libelle": "%s. %s" % (numero, titre),
            "bas": bas,
            "haut": haut,
            "serie": 1,
            "note": "chapitre %s" % numero,
        }
        for numero, titre, bas, haut in source
    ]


def cout_par_chapitre():
    corps = (
        barres(_lignes_chapitres(CHAPITRES), unite="Md€/an")
        + '<p class="chart__facet-title">Les sept plus petits chapitres, '
        "à l'échelle agrandie</p>"
        + barres(_lignes_chapitres(PETITS), unite="Md€/an")
    )
    donnees = table(
        ["Chapitre", "Bas (Md€/an)", "Haut (Md€/an)"],
        [
            ["%s. %s" % (numero, titre), nombre(bas), nombre(haut)]
            for numero, titre, bas, haut in CHAPITRES
        ]
        + [["6. Fiscalité", "recettes : +20", "recettes : +80"]],
        "Coût annuel récurrent par chapitre, borne basse et borne haute.",
    )
    return figure(
        "cout-par-chapitre",
        "Quatre chapitres portent les deux tiers du coût",
        "<strong>Comment lire.</strong> Un seul axe, partagé par les seize "
        "lignes : le chapitre 8 pèse à lui seul près de deux cents fois le "
        "chapitre 1. Le second panneau reprend les sept derniers avec un axe "
        "propre, dix fois plus fin — c'est un agrandissement, pas un second "
        "axe sur le même dessin.",
        corps,
        donnees,
        SOURCE,
        note="Le chapitre 8 ne porte plus ici sa charge d'annulation de la "
        "contribution sur les revenus financiers à 24 Md€ : la consolidation "
        "la ramène à 8,1, la mesure n'étant pas condamnée par la "
        "jurisprudence européenne. La ligne n'est pas isolable sur cet axe. "
        "Les chapitres 12 et 13 sont fusionnés en une ligne : le dossier "
        "ne publie pas de ventilation séparée après arbitrage du double compte "
        "climat. Le chapitre 6 est un chapitre de recettes, pas de dépenses, et "
        "ne figure donc pas sur l'axe des coûts. Sept lignes donnent la "
        "<em>contribution au consolidé</em> et non le total de la fiche du "
        "chapitre, l'écart étant le double compte neutralisé : chapitre 5 "
        "(fiche 63-110), 8 (95-170), 10 (76-118), 14 (7,4-21,6 tous "
        "financeurs), 15 (20,9-40,8 en littéral), 17 (20-28 pour le bras de "
        "fer généralisé). Le chapitre 2 ne porte ici que son flux annuel : "
        "ses 23 à 390 Md€ de capital sont d'une autre unité.",
    )


DOUBLES = [
    ("L'enveloppe climat", "12 et 13", 96.7, 172.4, 35, 76, "62 à 97"),
    ("Le salaire des fonctionnaires", "5, 8 et 9",
     43.3, 57, 22, 26, "20 à 28"),
    ("Le service citoyen", "5 et 10", 38.4, 47.7, 14.4, 23.7, "24"),
    ("La hausse du SMIC", "8 et 9", 25, 29, 8, 12, "19"),
    ("La garantie d'autonomie", "5, 7 et 10", 61, 69, 47.5, 58.5, "3 à 8"),
]


def doubles_comptes():
    lignes = []
    for libelle, chapitres, naif_b, naif_h, vrai_b, vrai_h, retire in DOUBLES:
        lignes.append({
            "libelle": libelle,
            "bas": naif_b, "haut": naif_h, "serie": 2,
            "note": "addition naïve des chapitres %s" % chapitres,
        })
        lignes.append({
            "libelle": "→ consolidé correct",
            "bas": vrai_b, "haut": vrai_h, "serie": 1,
            "note": "poste retiré : %s Md€/an" % retire,
        })
    corps = (
        legende([("mark--2", "Addition naïve des chapitres"),
                 ("mark--1", "Consolidé correct après neutralisation")])
        + barres(lignes, unite="Md€/an")
    )
    donnees = table(
        ["Double compte", "Chapitres", "Addition naïve", "Consolidé correct",
         "Poste retiré"],
        [
            [libelle, chapitres,
             "%s à %s" % (nombre(nb), nombre(nh)),
             "%s à %s" % (nombre(vb), nombre(vh)), retire]
            for libelle, chapitres, nb, nh, vb, vh, retire in DOUBLES
        ],
        "Doubles comptes en flux annuel, avant et après neutralisation "
        "(Md€/an).",
    )
    return figure(
        "doubles-comptes",
        "Additionner les chapitres facture deux fois la même dépense",
        "<strong>Comment lire.</strong> Chaque paire oppose ce que donne "
        "l'addition brute des chapitres à ce que vaut réellement la mesure. "
        "L'écart entre les deux barres est de l'argent compté deux fois. "
        "Dernière paire : la garantie d'autonomie, où le double compte "
        "soupçonné a été <em>réfuté</em> — les deux barres se ressemblent, et "
        "c'est le résultat.",
        corps,
        donnees,
        SOURCE,
        note="Un sixième recouvrement, le rachat des autoroutes, ne figure pas "
        "ici : il porte sur du capital versé une fois (70 à 90 Md€), et non sur "
        "une dépense annuelle. Mélanger les deux unités sur un même axe serait "
        "une erreur de lecture. Le poste retiré n'est pas toujours l'exacte "
        "différence entre les deux barres : plusieurs arbitrages ont révisé la "
        "mesure en même temps qu'ils la dédoublonnaient.",
    )
