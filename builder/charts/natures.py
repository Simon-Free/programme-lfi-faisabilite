"""Les trois natures de cout, et le seul axe ou elles s'additionnent.

Regle de la transverse 20 : un flux annuel recurrent, un investissement
ponctuel etale et une acquisition d'actif ne partagent JAMAIS un axe — sauf
un, et un seul : le decaissement d'une annee donnee. Une fois converties en
« euros payes pendant l'annee N », les trois natures deviennent additives,
et c'est la seule vue qui les reunit legitimement.

Chiffres : transverses/20_ponctuel_vs_recurrent.md § 3 et § 5, construits sur
transverses/04 § 5.4 (blocs) et § 6.1-6.2 (montee en charge).
"""

from .bars import barres
from .base import figure, legende, table
from .figures import heros

SOURCE = (
    "Source : transverse 20, coût ponctuel et coût récurrent ; profil de "
    "montée en charge de la transverse 04, § 6.1 et § 6.2."
)

# (libelle, bas, haut, note) — trois natures, trois axes distincts.
RECURRENT = [
    ("Dépense récurrente, en régime", 472, 472,
     "Revient chaque année, indéfiniment. Lecture littérale consolidée."),
]

PONCTUEL = [
    ("Investissement non récurrent", 175, 305,
     "Étalé sur dix ans, puis s'arrête. Soit 18 à 31 Md€/an pendant la "
     "période. La transverse 20 le corrige à 190-379 en réintégrant le "
     "chapitre 11 et la valeur révisée du chapitre 5."),
]

ACQUISITIONS = [
    ("Acquisitions d'actifs — décaissement", 352, 395,
     "Versé une fois. L'État reçoit un bien en échange : neutre au déficit "
     "à hauteur de la valeur de marché, mais intégralement à financer."),
    ("dont part frappant le déficit", 47, 161,
     "Indemnités de résiliation et primes de contrôle : rien n'est acheté "
     "en échange. Soit 1,6 à 5,4 points de PIB sur un seul exercice."),
]

# (annee, decaissement brut, note) — la seule vue additive.
PROFIL = [
    ("An 1", 160, "142 récurrent + 18 ponctuel. Le récurrent n'est qu'à 30 % "
     "de son régime."),
    ("An 2", 333, "236 + 22 + 75 d'acquisitions. La marche la plus raide du "
     "mandat : le décaissement double en un exercice."),
    ("An 3", 377, "321 + 26 + 30 d'acquisitions."),
    ("An 4", 454, "401 + 28 + 25 d'acquisitions."),
    ("An 5", 502, "472 + 30. PIC : plus aucune acquisition, et pourtant "
     "l'année la plus lourde — le récurrent seul pèse plus que tout le reste."),
    ("An 6-10", 495, "472 + 23 d'investissement résiduel."),
    ("An 11+", 472, "L'investissement est achevé. Il ne reste que le "
     "récurrent, qui ne s'arrête jamais."),
]


def _lignes(source, serie):
    return [
        {"libelle": libelle, "bas": bas, "haut": haut, "serie": serie,
         "note": note}
        for libelle, bas, haut, note in source
    ]


def _panneau(titre, lignes, unite):
    return ('<p class="chart__facet-title">%s</p>' % titre) + barres(
        lignes, unite=unite
    )


def natures_du_cout():
    corps = (
        heros(
            "472 Md€/an",
            "de dépense récurrente — le seul montant qui revient chaque année",
            "plus 175 à 305 Md€ d'investissement étalé et 352 à 395 Md€ "
            "d'acquisitions d'actifs : trois natures, trois axes, aucune "
            "addition",
        )
        + _panneau(
            "1. Coût récurrent (Md€/an) — revient chaque année",
            _lignes(RECURRENT, 1),
            "Md€/an",
        )
        + _panneau(
            "2. Coût ponctuel (Md€, une fois) — <em>autre unité, autre axe</em>",
            _lignes(PONCTUEL, 3),
            "Md€",
        )
        + _panneau(
            "3. Acquisitions d'actifs (Md€, une fois) — "
            "<em>troisième nature, troisième axe</em>",
            _lignes(ACQUISITIONS, 7),
            "Md€",
        )
    )
    donnees = table(
        ["Nature", "Bas", "Haut", "Unité", "Ce qu'elle fait au déficit"],
        [
            ["Coût récurrent", "472", "472", "Md€/an",
             "Dégrade le déficit chaque année, indéfiniment"],
            ["Coût ponctuel", "175", "305", "Md€ (10 ans)",
             "Dégrade le déficit pendant la période, puis s'arrête"],
            ["Acquisitions d'actifs", "352", "395", "Md€ (une fois)",
             "Neutre au déficit au prix de marché ; augmente la dette brute"],
            ["dont part frappant le déficit", "47", "161", "Md€ (une fois)",
             "Transfert en capital : aucune contrepartie d'actif"],
        ],
        "Les trois natures de coût du programme, avec leur unité propre.",
    )
    return figure(
        "natures-du-cout",
        "Trois natures de coût, trois axes : elles ne s'additionnent jamais",
        "<strong>Comment lire.</strong> Trois panneaux séparés, et c'est "
        "l'essentiel du dessin : un euro dépensé <em>chaque année</em>, un "
        "euro dépensé <em>une fois</em> et un euro <em>échangé contre un "
        "actif</em> ne sont pas la même grandeur. Les mettre sur un même axe "
        "donnerait « environ mille milliards » — un nombre qui ne veut rien "
        "dire.",
        corps,
        donnees,
        SOURCE,
        note="La part des acquisitions qui frappe réellement le déficit — 47 "
        "à 161 Md€ — est un <em>sous-ensemble</em> de la barre du dessus, et "
        "non une quatrième catégorie : ce sont les indemnités de résiliation "
        "et les primes de contrôle, contre lesquelles l'État ne reçoit aucun "
        "actif. Le poste le plus lourd du bloc, le pôle bancaire à 235-262 "
        "Md€, est celui qui coûte le moins au déficit : zéro, s'il est acheté "
        "au cours. La transverse 18 annoncée sur les acquisitions n'existe "
        "pas encore ; si elle est produite, elle prime sur ces valeurs.",
    )


def profil_decaissement():
    lignes = [
        {"libelle": annee, "bas": montant, "serie": 2 if annee == "An 5" else 1,
         "note": note}
        for annee, montant, note in PROFIL
    ]
    corps = (
        heros(
            "502 Md€",
            "c'est le pic annuel de décaissement, et il tombe en année 5",
            "542 Md€ de besoin de financement cette année-là, recettes "
            "déduites et charge d'intérêt comprise",
        )
        + legende([("mark--2", "Année de pic"),
                   ("mark--1", "Autres exercices")])
        + barres(lignes, unite="Md€ décaissés dans l'année")
    )
    donnees = table(
        ["Exercice", "Récurrent", "Ponctuel", "Acquisitions",
         "Décaissement brut"],
        [["An 1", "142", "18", "0", "160"],
         ["An 2", "236", "22", "75", "333"],
         ["An 3", "321", "26", "30", "377"],
         ["An 4", "401", "28", "25", "454"],
         ["An 5", "472", "30", "0", "502"],
         ["An 6-10", "472", "≈ 23", "0", "≈ 495"],
         ["An 11+", "472", "0", "0", "472"]],
        "Décaissement annuel par nature, en Md€. Scénario central "
        "d'acquisitions, hors pôle bancaire.",
    )
    return figure(
        "profil-decaissement",
        "Le pic de décaissement tombe en année 5, quand il n'y a plus une seule acquisition",
        "<strong>Comment lire.</strong> C'est le <em>seul</em> axe où les "
        "trois natures s'additionnent légitimement — parce qu'elles ont toutes "
        "été converties dans la même unité : les euros réellement payés "
        "pendant l'année. On attendrait le pic en année 2 ou 3, quand les "
        "nationalisations se décaissent. Il n'en est rien : en année 5 il n'y "
        "a plus d'acquisition du tout, et c'est pourtant l'année la plus "
        "lourde, parce que le récurrent seul pèse plus que tout le reste "
        "réuni.",
        corps,
        donnees,
        SOURCE,
        note="Reconstitution de la transverse 20, § 5.2, sur le profil de "
        "montée en charge publié par la transverse 04 (dépense à 30 / 50 / 68 "
        "/ 85 / 100 % du régime). Contrôle : le cumul sur cinq ans du besoin "
        "de financement donne 1 865 Md€, contre 1 850 publiés — 0,8 % "
        "d'écart, sans calage. <strong>Ce profil retient le scénario central "
        "d'acquisitions.</strong> En lecture littérale, le pôle bancaire "
        "ajoute 235 à 262 Md€ sur un exercice que le programme ne date pas : "
        "le pic monterait alors entre 570 et 765 Md€, à une date que le "
        "dossier ne détermine pas.",
    )
