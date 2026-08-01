"""Le seul axe ou les trois natures de cout s'additionnent legitimement.

Une fois converties en « euros reellement payes pendant l'annee N », les
trois natures deviennent additives — et c'est la seule vue qui les reunit
sans faute. Le resultat est contre-intuitif : le pic tombe en annee 5, la
seule des cinq premieres ou il n'y a plus une seule acquisition.

Chiffres : `transverses/20_ponctuel_vs_recurrent.md` § 5.2, reconstitue sur
les series publiees de `transverses/04` § 6.1, § 6.2 et § 7.4.
"""

from .bars import barres
from .base import figure, legende, table
from .figures import heros

SOURCE = (
    "Source : transverse 20, § 5.2 ; profil de montée en charge de la "
    "transverse 04, § 6.1 et § 6.2 ; charge d'intérêt, § 7.4."
)

# (annee, decaissement brut, note) — la seule vue additive.
PROFIL = [
    ("An 1", 156, "138 récurrent + 18 ponctuel. Le récurrent n'est qu'à 30 % "
     "de son régime."),
    ("An 2", 327, "230 + 22 + 75 d'acquisitions. La marche la plus raide du "
     "mandat : +171 Md€ d'un exercice à l'autre, soit un doublement."),
    ("An 3", 369, "313 + 26 + 30 d'acquisitions."),
    ("An 4", 444, "391 + 28 + 25 d'acquisitions."),
    ("An 5", 490, "460 + 30. PIC : plus aucune acquisition, et pourtant "
     "l'année la plus lourde — le récurrent seul pèse plus que tout le "
     "reste réuni."),
    ("An 6-10", 483, "460 + 23 d'investissement résiduel."),
    ("An 11+", 460, "L'investissement est achevé. Il ne reste que le "
     "récurrent, qui ne s'arrête jamais."),
]


def profil_decaissement():
    lignes = [
        {"libelle": annee, "bas": montant, "serie": 2 if annee == "An 5" else 1,
         "note": note}
        for annee, montant, note in PROFIL
    ]
    corps = (
        heros(
            "490 Md€",
            "c'est le pic annuel de décaissement, et il tombe en année 5",
            "530 Md€ de besoin de financement cette année-là, recettes "
            "déduites et charge d'intérêt comprise",
        )
        + legende([("mark--2", "Année de pic"),
                   ("mark--1", "Autres exercices")])
        + barres(lignes, unite="Md€ décaissés dans l'année")
    )
    donnees = table(
        ["Exercice", "Récurrent", "Ponctuel", "Acquisitions",
         "Décaissement brut", "Besoin de financement"],
        [["An 1", "138", "18", "0", "156", "151"],
         ["An 2", "230", "22", "75", "327", "318"],
         ["An 3", "313", "26", "30", "369", "368"],
         ["An 4", "391", "28", "25", "444", "459"],
         ["An 5", "460", "30", "0", "490", "530"],
         ["An 6-10", "460", "≈ 23", "0", "≈ 483", "≈ 462"],
         ["An 11+", "460", "0", "0", "460", "≈ 416"]],
        "Décaissement annuel par nature, en Md€. Le besoin de financement "
        "ajoute la charge d'intérêt et déduit les recettes nouvelles. "
        "Scénario central d'acquisitions, hors pôle bancaire.",
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
        "dossier ne détermine pas. Les années 6 à 10 supposent que le solde "
        "de l'enveloppe d'investissement se décaisse à plat : hypothèse "
        "raisonnable, non sourcée, et déclarée comme telle.",
    )
