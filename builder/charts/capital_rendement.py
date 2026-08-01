"""Pourquoi un stock enorme ne donne qu'une marge etroite.

C'est la figure decisive du bloc capital. Elle tient en trois temps : sur
les 398,5 Md€ de « revenus du capital », 215 sont des loyers imputes que
personne n'encaisse ; il reste 183 Md€ de revenu monetaire ; et l'Etat en
preleve deja 113,2, soit 62 centimes par euro.

Chiffres : `transverses/12_assiettes_capital.md` § 3.1, § 4.1, § 7.1, § 7.2
et § 7.3. Sources primaires : Insee References, SDES Compte du logement
2024, Conseil des prelevements obligatoires, decembre 2025.
"""

from .bars import barres
from .base import figure, legende, table
from .figures import heros, jauge
from .stacks import empilements

SOURCE = (
    "Source : Insee Références, <em>Revenu des ménages en comptabilité "
    "nationale</em>, éd. 2024 ; SDES, <em>Compte du logement 2024</em> ; "
    "Conseil des prélèvements obligatoires, décembre 2025. Repris par la "
    "transverse 12, § 3, § 4 et § 7."
)

REVENUS = [
    ("Les « 398,5 Md€ de revenus du capital » des ménages", [
        ("Revenu monétaire réellement encaissé", 183, 1,
         "Loyers réels, dividendes, intérêts, plus-values réalisées. C'est "
         "le seul flux sur lequel un impôt peut être payé en espèces."),
        ("Loyers imputés aux propriétaires occupants", 215, 2,
         "Le loyer fictif qu'un propriétaire occupant est réputé se verser à "
         "lui-même. Aucun relevé bancaire ne le porte. La France l'a imposé "
         "jusqu'au milieu des années 1960, puis y a renoncé."),
    ]),
]

TAUX = [
    ("Revenu monétaire, rapporté au patrimoine brut", 1.07,
     "183 Md€ sur 17 063. C'est ce que le patrimoine distribue en argent."),
    ("Revenu au sens de la comptabilité nationale", 2.34,
     "398,5 sur 17 063, loyers fictifs compris."),
    ("Croissance de la valeur du patrimoine, 1995-2024", 4.90,
     "Faite d'épargne nouvelle, de plus-values latentes et du service de "
     "logement : aucune des trois ne se prélève en espèces sans forcer une "
     "vente d'actif."),
]

PLAFONDS = [
    ("Prélevé aujourd'hui", 113.2, 1,
     "Taxe foncière 26,1 · successions et donations 20,8 · CSG sur le "
     "capital 17,9 · impôt sur le revenu, part capital 15,2 · droits de "
     "vente 14,7 · prélèvement de solidarité 14,6 · CRDS 1,2 · impôt sur la "
     "fortune immobilière 2,7."),
    ("Plafond de 75 % des revenus — la norme française", 137.0, 2,
     "Article 979 du code général des impôts : impôt sur la fortune, impôt "
     "sur le revenu et prélèvements sociaux réunis ne peuvent excéder 75 % "
     "des revenus de l'année précédente. Marge : +24 Md€/an."),
    ("Totalité du revenu monétaire", 183.0, 1,
     "Inutilisable : un taux de 100 % sur le revenu du capital est la "
     "définition de la confiscation, et des taux bien inférieurs ont été "
     "censurés — 72 % en 2012."),
]


def _panneau(titre, lignes, unite):
    return ('<p class="chart__facet-title">%s</p>' % titre) + barres(
        lignes, unite=unite
    )


def _corps():
    return (
        heros(
            "1,07 %",
            "c'est tout ce que le patrimoine des ménages distribue en argent "
            "réel, chaque année",
            "183 Md€ sur 17 063 Md€ de patrimoine brut — et l'État en prélève "
            "déjà 62 %",
        )
        + legende([("mark--1", "Revenu monétaire, encaissable"),
                   ("mark--2", "Loyers imputés, que personne n'encaisse")])
        + '<p class="chart__facet-title">1. Plus de la moitié des « revenus '
        "du capital » n'existe pas en trésorerie (Md€/an)</p>"
        # Le total n'est pas ecrit : 183 est un arrondi, et « 398 » au bout
        # de la barre contredirait le 398,5 du titre pour un demi-milliard.
        + empilements(REVENUS, unite="Md€/an", total_visible=False)
        + jauge(
            61.9,
            "62 centimes par euro",
            "sont déjà prélevés sur le revenu monétaire du patrimoine : "
            "113,2 Md€ sur 183. Ce n'est pas un taux marginal — c'est "
            "l'agrégat de tous les impôts sur le stock, les transactions, "
            "les transmissions et les revenus.",
        )
        + _panneau(
            "2. Trois taux de rendement, tous exacts, tous différents "
            "— <em>autre unité, autre axe</em>",
            [{"libelle": libelle, "bas": valeur, "serie": 1, "note": note}
             for libelle, valeur, note in TAUX],
            "% du patrimoine brut, par an",
        )
        + '<p class="chart__facet-title">3. Ce qu\'un critère de '
        "soutenabilité autorise (Md€/an de prélèvement)</p>"
        + legende([("mark--2", "Le seul critère défendable"),
                   ("mark--1", "Niveau actuel et plafond théorique")])
        + barres(
            [{"libelle": libelle, "bas": valeur, "serie": serie, "note": note}
             for libelle, valeur, serie, note in PLAFONDS],
            unite="Md€/an prélevés sur le patrimoine",
        )
    )


def _donnees():
    return table(
        ["Grandeur", "Valeur", "Calcul ou précision"],
        [["Revenus du patrimoine, concept large", "398,5 Md€/an",
          "Insee Références, 2023, loyers imputés inclus"],
         ["moins loyers imputés aux propriétaires occupants", "−215 Md€/an",
          "SDES, Compte du logement 2024"],
         ["= Revenus monétaires du patrimoine", "≈ 183 Md€/an", "Estimation"],
         ["Patrimoine brut des ménages", "17 063 Md€", "Encours fin 2024"],
         ["Rendement monétaire", "1,07 %/an", "183 / 17 063"],
         ["Rendement en comptabilité nationale", "2,34 %/an", "398,5 / 17 063"],
         ["Croissance nominale du patrimoine", "4,90 %/an",
          "× 4,0 en 29 ans, 1995-2024"],
         ["Prélèvements sur le patrimoine des ménages", "113,2 Md€/an",
          "CPO, 2024 ; 3,9 % du PIB"],
         ["Prélèvements / revenu monétaire", "61,9 %", "113,2 / 183"],
         ["Prélèvements / revenu au sens large", "28,4 %", "113,2 / 398,5"],
         ["Prélèvements / patrimoine brut", "0,66 %/an", "113,2 / 17 063"],
         ["Plafond au critère des 75 %", "137 Md€/an", "0,75 × 183"],
         ["Marge macroéconomique qui en découle", "+24 Md€/an", "137 − 113,2"]],
        "Ce que le patrimoine des ménages produit, et ce que l'État en "
        "prélève déjà.",
    )


def rendement_capital():
    return figure(
        "rendement-capital",
        "Un stock de 17 000 milliards ne distribue que 183 milliards, et l'État en prend déjà 62 %",
        "<strong>Comment lire.</strong> On lit partout que « les revenus du "
        "capital pèsent 398 milliards ». Le chiffre est exact, mais plus de "
        "la moitié n'est encaissée par personne : c'est le loyer fictif que "
        "les propriétaires occupants sont réputés se verser à eux-mêmes. Une "
        "fois retiré, il reste 183 milliards — dont l'État prélève déjà "
        "soixante-deux centimes par euro. <strong>C'est de cette étroite "
        "bande, et non des 19 559 milliards de patrimoine, que sort toute "
        "recette nouvelle.</strong>",
        _corps(),
        _donnees(),
        SOURCE,
        note="Les 62 % ne sont pas un taux marginal : aucun contribuable ne "
        "les subit. Le taux de droit commun sur un dividende reste de 30 %, "
        "porté à environ 37 % au sommet. Le dénominateur est un choix, et il "
        "double presque le résultat : en comptant les loyers fictifs, le "
        "ratio tombe à 28,4 %. Exclure ces loyers correspond à la question "
        "posée — un revenu que personne n'encaisse ne finance aucun impôt. "
        "<strong>L'écart entre 1,07 % et 4,90 % est la clé du sujet</strong> : "
        "le patrimoine grossit de près de 5 % par an en valeur et n'en "
        "distribue qu'un peu plus de 1 % en monnaie. C'est pourquoi tout "
        "impôt pérenne sur le stock doit être plafonné sur le revenu, en "
        "droit français — une contrainte économique avant d'être "
        "constitutionnelle.",
    )
