"""De quoi la richesse francaise est faite : quatre cinquiemes de pierre.

Chiffres : `transverses/12_assiettes_capital.md` § 1.1 et § 1.2. Source
primaire : Insee et Banque de France, comptes nationaux base 2020, encours
fin 2024.
"""

from .bars import barres
from .base import figure, legende, nombre, table
from .figures import heros, jauge
from .stacks import empilements

SOURCE = (
    "Source : Insee et Banque de France, « Le patrimoine économique national "
    "en 2024 », <em>Bulletin de la Banque de France</em> n° 261/1, novembre "
    "2025. Repris par la transverse 12, § 1."
)

NATIONAL = 19559
BRUT_MENAGES = 17063

SECTEURS = [
    ("Ménages", 14953, 1,
     "76,5 % du patrimoine net national. Leur patrimoine financier net, "
     "+4 986 Md€, absorbe la totalité du passif net des autres secteurs."),
    ("Sociétés non financières et financières", 3916, 2,
     "3 860 + 56 Md€. Leurs fonds propres en valeur de marché valent 15 278 "
     "Md€, détenus pour l'essentiel par des ménages : il n'existe pas "
     "d'assiette « entreprises » distincte de l'assiette « ménages »."),
    ("Administrations publiques", 690, 7,
     "3,5 % du total, en recul de 6,7 % sur un an. Céder ce patrimoine ne "
     "produirait qu'un encaissement unique, pas une recette pérenne."),
]

MENAGES = [
    ("Logements — les murs", 4807, "28,2 % des actifs bruts des ménages."),
    ("Terrains bâtis — le sol", 4043, "23,7 %."),
    ("Actions et parts de fonds", 2155,
     "Dont 1 745 Md€ de participations directes hors OPC : l'assiette que "
     "l'administration ne sait pas valoriser à coût raisonnable."),
    ("Numéraire et dépôts", 2108, ""),
    ("Assurance-vie", 1856, ""),
    ("Autres actifs non financiers", 1116,
     "Terres agricoles, autres bâtiments, machines, stocks."),
    ("Autres comptes à recevoir", 571, ""),
    ("Droits à pension", 234, ""),
    ("Titres, crédits, garanties", 172, ""),
]


def _part(valeur, total):
    return "%s %%" % nombre(100.0 * valeur / total, 1)


def _corps():
    return (
        heros(
            "19 559 Md€",
            "de patrimoine national — soit 6,7 années de production du pays",
            "dont 14 953 aux ménages, et 79 % en constructions et terrains",
        )
        + jauge(
            79.3,
            "79 % de pierre et de sol",
            "15 504 Md€ sur 19 559. Un impôt sur le patrimoine en France est, "
            "à 79 %, un impôt sur l'immobilier — quelle que soit l'intention "
            "de son auteur.",
        )
        + legende([("mark--1", "Ménages"),
                   ("mark--2", "Sociétés"),
                   ("mark--7", "Administrations publiques")])
        + '<p class="chart__facet-title">1. Qui détient les 19 559 Md€ '
        "(encours fin 2024)</p>"
        + empilements(
            [("Patrimoine net, par secteur institutionnel", SECTEURS)],
            unite="Md€",
        )
        + '<p class="chart__facet-title">2. Les 17 063 Md€ d\'actifs bruts '
        "des ménages, poste par poste</p>"
        + barres(
            [{"libelle": libelle, "bas": valeur, "serie": 1, "note": note}
             for libelle, valeur, note in MENAGES],
            unite="Md€ d'encours",
        )
    )


def _donnees():
    lignes = [[libelle, nombre(valeur), _part(valeur, NATIONAL)]
              for libelle, valeur, _, _ in SECTEURS]
    lignes.append(["Ensemble de l'économie nationale", "19 559", "100 %"])
    lignes.append(["dont constructions et terrains sous-jacents", "15 504",
                   "79,0 %"])
    lignes += [[libelle, nombre(valeur), _part(valeur, BRUT_MENAGES)]
               for libelle, valeur, _ in MENAGES]
    lignes.append(["Actifs bruts des ménages", "17 063", "100 %"])
    lignes.append(["moins passifs financiers des ménages", "−2 112", "—"])
    lignes.append(["Patrimoine net des ménages", "14 953", "—"])
    return table(
        ["Poste", "Montant (Md€)", "Part de son ensemble"],
        lignes,
        "Patrimoine économique national et actifs bruts des ménages, encours "
        "fin 2024, en Md€.",
    )


def patrimoine_composition():
    return figure(
        "patrimoine-composition",
        "Quatre cinquièmes de la richesse française sont de la pierre et du sol",
        "<strong>Comment lire.</strong> La barre du haut partage le patrimoine "
        "du pays entre ceux qui le détiennent : les ménages en portent plus "
        "des trois quarts. Le panneau du bas ouvre leur part poste par poste, "
        "et le résultat y est le même : les deux premières lignes — les murs "
        "et le sol — pèsent à elles seules plus que tout le patrimoine "
        "financier réuni.",
        _corps(),
        _donnees(),
        SOURCE,
        note="C'est ce fait, et non un choix de barème, qui explique le "
        "rendement de l'impôt sur la fortune immobilière : en ne retenant que "
        "l'immobilier, la réforme de 2018 a gardé les 79 % et supprimé les "
        "21 %. Les deux panneaux ne portent pas sur la même grandeur — le "
        "premier donne le patrimoine <em>net</em> par secteur, le second les "
        "actifs <em>bruts</em> des seuls ménages, dont il faut retrancher "
        "2 112 Md€ de dettes pour retrouver les 14 953 du premier. Ils ne se "
        "soustraient donc pas l'un de l'autre.",
    )
