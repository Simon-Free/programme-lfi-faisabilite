"""Le fait central : la composition du patrimoine s'inverse au sommet.

Sept euros sur dix sont immobiliers chez les foyers ordinaires, deux chez
les plus fortunes. C'est ce renversement, et rien d'autre, qui explique
qu'un impot assis sur le seul immobilier manque les grandes fortunes.

Chiffres : `transverses/12_assiettes_capital.md` § 2.2 et § 2.3. Sources
primaires : Insee Focus n° 371 (seuils, patrimoine brut), DGFiP Analyses
n° 08 (partage 79/21), Banque de France (part du dixieme superieur, net).
"""

from .bars import barres
from .base import figure, legende, table
from .figures import heros, jauge
from .stacks import parts_en_pourcent

SOURCE = (
    "Source : DGFiP Analyses n° 08, janvier 2025 ; Insee Focus n° 371, "
    "décembre 2025 ; Banque de France, comptes distributionnels, T2 2023. "
    "Repris par la transverse 12, § 2."
)

COMPOSITION = [
    ("Les foyers à très haut patrimoine — 9,9 M€ en moyenne", [
        ("Immobilier", 21, 1,
         "2,1 M€ sur 9,9. C'est la seule part que l'impôt sur la fortune "
         "immobilière atteint."),
        ("Mobilier", 79, 2,
         "7,8 M€ sur 9,9 : titres, participations, sociétés patrimoniales. "
         "Hors de l'assiette depuis 2018."),
    ]),
    ("Les autres foyers", [
        ("Immobilier", 70, 1, "La résidence principale, pour l'essentiel."),
        ("Mobilier", 30, 2, "Dépôts, assurance-vie, épargne réglementée."),
    ]),
]

# (libelle, milliers d'euros, euros ecrits en clair, note)
SEUILS = [
    ("D1 — plafond des 10 % les moins dotés", 6.2, "6 200 €", ""),
    ("D5 — médiane", 205.1, "205 100 €",
     "La moitié des ménages est en dessous."),
    ("D9 — entrée dans les 10 % supérieurs", 857.7, "857 700 €", ""),
    ("P95 — entrée dans les 5 % supérieurs", 1268.2, "1 268 200 €", ""),
    ("P99 — entrée dans les 1 % supérieurs", 3020.9, "3 020 900 €",
     "Le seuil de 1,3 M€ de l'ancien impôt sur la fortune place donc le "
     "point d'entrée entre P95 et P99 : l'assiette est celle de 1 à 5 % des "
     "ménages."),
]


def _corps():
    return (
        heros(
            "21 % contre 70 %",
            "la part d'immobilier au sommet, et celle de tous les autres",
            "c'est ce renversement qui explique pourquoi l'impôt sur la "
            "fortune immobilière manque les grandes fortunes et atteint les "
            "moyennes",
        )
        + legende([("mark--1", "Immobilier"), ("mark--2", "Mobilier")])
        + '<p class="chart__facet-title">1. La composition s\'inverse au '
        "sommet (% du patrimoine détenu)</p>"
        + parts_en_pourcent(COMPOSITION, unite="%")
        + '<p class="chart__facet-title">2. Les seuils de patrimoine brut '
        "— <em>autre unité, autre axe</em></p>"
        + barres(
            [{"libelle": libelle, "bas": valeur, "serie": 7,
              "note": "%s. %s" % (clair, note)}
             for libelle, valeur, clair, note in SEUILS],
            unite="milliers d'euros de patrimoine brut",
        )
        + jauge(
            54.2,
            "Le dixième supérieur détient 54,2 %",
            "du patrimoine net des ménages — quand la moitié inférieure n'en "
            "détient que 5 %. Aucune recette significative ne peut venir "
            "de là.",
        )
    )


def _donnees():
    lignes = [
        ["Foyers à très haut patrimoine — immobilier", "21 %",
         "2,1 M€ sur 9,9 M€ de patrimoine moyen, données 2016"],
        ["Foyers à très haut patrimoine — mobilier", "79 %", "7,8 M€"],
        ["Autres foyers — immobilier", "70 %", "DGFiP Analyses n° 08"],
        ["Autres foyers — mobilier", "30 %", "idem"],
    ]
    lignes += [[libelle, clair, note or "Insee Focus n° 371, patrimoine brut"]
               for libelle, _, clair, note in SEUILS]
    lignes += [
        ["Part du dixième supérieur, patrimoine net", "54,2 %",
         "7 610 Md€ ; seuil 992 000 €, moyenne 2 418 000 €"],
        ["Part du dixième supérieur, patrimoine brut", "48 %",
         "Enquête Insee, concept brut : les deux mesures ne se confondent pas"],
        ["Part de la moitié inférieure, patrimoine net", "5,0 %", "702 Md€"],
        ["Patrimoine professionnel détenu par le cinquième supérieur", "93 %",
         "L'actif le plus concentré, et le plus largement exonéré"],
    ]
    return table(
        ["Grandeur", "Valeur", "Précision"],
        lignes,
        "Composition et distribution du patrimoine des ménages français.",
    )


def patrimoine_distribution():
    return figure(
        "patrimoine-distribution",
        "Au sommet, le patrimoine n'est plus de la pierre — et l'impôt sur la fortune immobilière ne l'atteint plus",
        "<strong>Comment lire.</strong> Les deux barres du haut sont ramenées "
        "à la même longueur : elles comparent des <em>compositions</em>, non "
        "des montants. Chez les foyers ordinaires, sept euros de patrimoine "
        "sur dix sont immobiliers ; chez les plus fortunés, c'est deux. Un "
        "impôt assis sur le seul immobilier frappe donc la quasi-totalité du "
        "patrimoine des uns, et un cinquième de celui des autres.",
        _corps(),
        _donnees(),
        SOURCE,
        note="Le partage 79/21 est mesuré sur 2016, dernière année de "
        "l'ancien impôt sur la fortune — donc la dernière où l'administration "
        "a connu autre chose que l'immobilier. Les seuils du second panneau "
        "relèvent d'une autre source et d'un autre concept (patrimoine "
        "<em>brut</em>, enquête Insee) que la part du dixième supérieur "
        "(patrimoine <em>net</em>, comptes de la Banque de France) : les deux "
        "ne se soustraient pas. <strong>Le nombre de ménages dont le "
        "patrimoine net dépasse 3, 10 ou 100 M€ n'est publié par aucune "
        "source primaire française</strong> : tout rendement d'un impôt sur "
        "la fortune au-delà de ces seuils repose sur une extrapolation, y "
        "compris dans les chiffrages officiels.",
    )
