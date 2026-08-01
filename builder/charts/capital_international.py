"""La France est deja quatrieme de l'OCDE, et premiere sur les successions.

Ce fait borne le raisonnement : on ne peut pas batir un programme de recettes
sur l'idee que le capital francais serait sous-taxe en niveau. Il ne l'est
pas. Ce qui est vrai, c'est qu'il est mal taxe — taux facials tres eleves,
assiette percee, progressivite qui s'inverse au sommet.

Chiffres : `transverses/12_assiettes_capital.md` § 4.3. Source primaire :
Conseil des prelevements obligatoires, decembre 2025, d'apres les
Statistiques des recettes publiques de l'OCDE, donnees 2022.
"""

from .bars import barres
from .base import figure, legende, nombre, table
from .figures import heros

SOURCE = (
    "Source : Conseil des prélèvements obligatoires, <em>Corriger les "
    "principales distorsions de l'imposition du patrimoine</em>, décembre "
    "2025, d'après l'OCDE et <em>Taxation Trends</em>, données 2022. Repris "
    "par la transverse 12, § 4.3."
)

# (libelle, valeur, serie) — serie 2 = la France, serie 1 = les autres.
DETENTION = [
    ("Royaume-Uni", 4.0, 1), ("Corée du Sud", 3.8, 1), ("France", 3.7, 2),
    ("Belgique", 3.3, 1), ("Espagne", 2.6, 1), ("Italie", 2.5, 1),
    ("Suisse", 2.2, 1), ("Moyenne de l'OCDE", 1.8, 1), ("Allemagne", 1.1, 1),
]

SUCCESSIONS = [
    ("France", 0.70, 2), ("Corée du Sud", 0.68, 1), ("Belgique", 0.65, 1),
]

# (poste, France, moyenne)
POSTES = [
    ("Impôts récurrents sur la propriété immobilière", 4.3, 2.8),
    ("Droits de mutation à titre onéreux", 2.1, 1.4),
    ("Droits de succession et de donation", 1.6, 0.4),
]


def _pays(source, note):
    return [
        {"libelle": libelle, "bas": valeur, "serie": serie,
         "note": note if serie == 2 else ""}
        for libelle, valeur, serie in source
    ]


def _confrontation():
    lignes = []
    for poste, france, moyenne in POSTES:
        lignes.append({"libelle": poste, "bas": france, "serie": 2,
                       "note": "France"})
        lignes.append({"libelle": "→ moyenne de l'OCDE", "bas": moyenne,
                       "serie": 1, "note": "Moyenne des 38 pays"})
    return lignes


def _corps():
    return (
        heros(
            "4ᵉ sur 38",
            "le rang de la France dans l'OCDE pour l'imposition du patrimoine",
            "3,7 % du PIB contre 1,8 % en moyenne et 1,1 % en Allemagne — et "
            "le premier rang, sans partage, sur les droits de succession",
        )
        + legende([("mark--2", "France"),
                   ("mark--1", "Autres pays et moyennes")])
        + '<p class="chart__facet-title">1. Imposition de la détention et de '
        "la transmission du patrimoine (% du PIB, 2022)</p>"
        + barres(
            _pays(DETENTION,
                  "Quatrième rang de l'OCDE, derrière Israël, le "
                  "Royaume-Uni et la Corée. Plus du double de la moyenne, "
                  "plus du triple de l'Allemagne."),
            unite="% du produit intérieur brut",
        )
        + '<p class="chart__facet-title">2. Droits de succession et de '
        "donation : les trois seuls pays au-dessus de 0,5 % du PIB</p>"
        + barres(
            _pays(SUCCESSIONS,
                  "Les droits de succession et de donation les plus élevés "
                  "de l'OCDE. Aucun autre pays ne dépasse 0,5 point de PIB."),
            unite="% du produit intérieur brut",
        )
        + '<p class="chart__facet-title">3. Poste par poste, la France est '
        "au-dessus partout — <em>autre unité, autre axe</em></p>"
        + barres(
            _confrontation(),
            unite="% de l'ensemble des prélèvements obligatoires",
        )
    )


def _donnees():
    lignes = [[libelle, "%s %%" % nombre(valeur, 1),
               "Détention et transmission, % du PIB"]
              for libelle, valeur, _ in DETENTION]
    lignes += [[libelle, "%s %%" % nombre(valeur, 2),
                "Droits de succession et de donation, % du PIB"]
               for libelle, valeur, _ in SUCCESSIONS]
    for poste, france, moyenne in POSTES:
        lignes.append([poste,
                       "France %s %% · OCDE %s %%"
                       % (nombre(france, 1), nombre(moyenne, 1)),
                       "% de l'ensemble des prélèvements obligatoires"])
    lignes += [
        ["Impôts sur les revenus du capital des ménages", "France 1,7 %",
         "% du PIB — le plus élevé de l'Union européenne, contre 0,9 % de "
         "moyenne"],
        ["Fiscalité française du patrimoine des ménages", "3,9 % du PIB",
         "Mesure du CPO, périmètre complet : 113,2 Md€, 9,1 % des "
         "prélèvements obligatoires"],
        ["Taux de prélèvements obligatoires, toutes assiettes", "43,8 % du PIB",
         "Premier des 38 pays de l'OCDE, contre 33,9 % de moyenne"],
    ]
    return table(
        ["Pays ou poste", "Valeur", "Périmètre"],
        lignes,
        "Comparaison internationale de la fiscalité du patrimoine, 2022.",
    )


def fiscalite_capital_comparee():
    return figure(
        "fiscalite-capital-comparee",
        "La France taxe déjà le patrimoine plus que trente-quatre pays de l'OCDE",
        "<strong>Comment lire.</strong> Chaque panneau a son propre périmètre "
        "et sa propre unité : le premier rapporte l'impôt à la production "
        "nationale, le troisième à l'ensemble des impôts et cotisations. Ils "
        "ne se comparent pas entre eux — mais chacun dit la même chose. La "
        "moyenne de l'OCDE figure comme une ligne parmi les pays : c'est un "
        "repère, pas un pays.",
        _corps(),
        _donnees(),
        SOURCE,
        note="<strong>Ce constat interdit et n'interdit pas.</strong> Il "
        "interdit de bâtir un programme de recettes sur l'idée que le capital "
        "français serait sous-taxé <em>en niveau</em> — le prétendre revient "
        "à annoncer des recettes qui n'arriveront pas. Il n'interdit pas de "
        "dire qu'il est <em>mal</em> taxé : taux affichés très élevés, "
        "assiette percée, progressivité qui s'inverse au sommet. L'organisme "
        "qui produit ces comparaisons recommande lui-même « une logique de "
        "taux bas, d'assiette large ». En part de l'ensemble des prélèvements "
        "obligatoires, la France n'est en revanche que huitième, à 8,1 % : "
        "son dénominateur est le plus élevé de l'OCDE.",
    )
