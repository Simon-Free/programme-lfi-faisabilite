"""Les variantes rentables a objectifs inchanges.

Deux unites incompatibles cohabitent dans ce dossier : une economie ANNUELLE
et un capital evite VERSE UNE FOIS. Elles ne partagent jamais un axe. Le
raffinement du chapitre 1, lui, COUTE 119 M€ : toutes les variantes ne sont
pas des economies, et celle-la figure aussi.
"""

from .bars import barres
from .base import figure, nombre, table
from .figures import heros

SOURCE = (
    "Source : journal de la phase 2, récapitulatif des quatre blocs de "
    "variantes (chapitres 1 à 18)."
)

ANNUELLES = [
    ("Voie légale européenne", 17, 20.2, 28.7,
     "Plutôt que le bras de fer. Compte de contrôle du règlement 2024/1263 ; "
     "le chapitre devient bénéficiaire. Mise en œuvre : 48 à 97 M€/an."),
    ("Maîtrise des coûts du climat", "12+13", 20, 34,
     "Trajectoire d'émissions inchangée, un seul article de loi de finances."),
    ("Décote levée pour les seuls inaptes", 8, 13, 13,
     "Retraite, avec étalement. L'effet dit « multiplicatif » de la décote "
     "est un facteur de ±15 %, non de 3."),
    ("Paramètre T_delta relevé", 15, 10, 14,
     "Coût nul, un alinéa du même article. Sans lui, 62 % de la recette de "
     "substitution du 100 % Sécu est absorbée par le barème des allègements."),
    ("CSG assise sur le revenu du foyer", 6, 10.5, 10.5,
     "Recette, pas économie. Le dispositif existe déjà sur les pensions. "
     "Plus 25 à 55 Md€ de trésorerie cumulée."),
    ("Ratio d'encadrement 6/10 opposable", 10, 4.4, 6.9,
     "En maison de retraite. L'objectif de 210 000 professionnels est "
     "dépassé : 264 000 ETP."),
    ("Compteur de formation plafonné", 8, 5, 5,
     "À 1 000 €/an : seule manière de borner une fourchette allant de 4 à 29."),
]

CAPITAL = [
    ("Échéance des concessions autoroutières", 2, 47, 55,
     "Attendre 2031-2036. « Aucun véhicule — une décision de ne pas "
     "légiférer. » Central 51 Md€. Le rachat anticipé détruit 1,5 à "
     "16,2 Md€ de valeur, la fiscalité perdue écrasant l'écart de taux."),
]


def _lignes(source, serie):
    return [
        {"libelle": libelle, "bas": bas, "haut": haut, "serie": serie,
         "note": "chapitre %s — %s" % (chapitre, texte)}
        for libelle, chapitre, bas, haut, texte in source
    ]


def variantes_rentables():
    corps = (
        heros(
            "135 à 142 Md€/an",
            "d'économies sans renoncer à un seul objectif du programme",
            "plus 165 à 283 Md€ de capital évité",
        )
        + '<p class="chart__facet-title">Économies annuelles récurrentes '
        "(Md€/an)</p>"
        + barres(_lignes(ANNUELLES, 3), unite="Md€/an")
        + '<p class="chart__facet-title">Capital évité, versé une seule fois '
        "(Md€) — <em>autre unité, autre axe</em></p>"
        + barres(_lignes(CAPITAL, 7), unite="Md€")
    )
    donnees = table(
        ["Variante", "Ch.", "Gain", "Unité", "Pourquoi elle ne coûte pas "
         "d'objectif"],
        [
            [libelle, str(chapitre),
             nombre(bas) if bas == haut else "%s à %s" % (nombre(bas),
                                                          nombre(haut)),
             unite, texte]
            for source, unite in ((ANNUELLES, "Md€/an"), (CAPITAL, "Md€"))
            for libelle, chapitre, bas, haut, texte in source
        ],
        "Variantes chiffrées à objectifs strictement inchangés.",
    )
    return figure(
        "variantes-rentables",
        "Cent trente-cinq milliards par an s'économisent sans renoncer à un objectif",
        "<strong>Comment lire.</strong> Deux panneaux séparés parce que les "
        "deux unités ne s'additionnent pas : une économie annuelle revient "
        "chaque année, un capital évité ne se verse qu'une fois. Les mettre "
        "sur un même axe gonflerait le total d'un facteur trompeur.",
        corps,
        donnees,
        SOURCE,
        note="Une variante a été RETIRÉE de ce graphique : « Engie à 50,01 % "
        "au lieu de 100 % », 40,7 à 50,7 Md€, deuxième économie du dossier. "
        "Elle est juridiquement impossible — l'État détenant 33,08 % des "
        "droits de vote, l'article 234-5 du règlement général de l'AMF "
        "l'oblige à déposer une offre publique sur la totalité du capital. "
        "Le capital évité passe donc de 206-334 à 165-283 Md€, par "
        "soustraction directe des deux bornes. "
        "Toutes les variantes ne sont pas des économies : le raffinement "
        "du chapitre 1 <em>coûte</em> 119 M€, et il achète onze mesures "
        "sauvées d'une censure annoncée quasi certaine. Le dossier ne publie "
        "aucun classement transverse : ces sept variantes sont les plus "
        "rentables de leurs blocs respectifs, et non un palmarès général.",
    )
