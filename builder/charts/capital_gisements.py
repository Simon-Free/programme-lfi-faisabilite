"""Le rendement supplementaire defendable, et d'ou il vient.

Le partage entre les deux panneaux est le resultat, pas une commodite de
mise en page : retirer une derogation rapporte plus, et se heurte a moins
d'obstacles juridiques, que relever un taux. Six gisements sur neuf sont
des derogations, et ils portent 62 % du rendement central.

Chiffres : `transverses/12_assiettes_capital.md` § 9.1, rendements NETS de
regime, apres elasticites documentees en § 8.1.
"""

from .bars import barres
from .base import figure, legende, nombre, table
from .figures import heros

SOURCE = (
    "Source : transverse 12, § 9.1, addition ligne à ligne des rendements "
    "nets de régime ; élasticités de la section 8.1. Contrôle "
    "macroéconomique indépendant en § 7.3."
)

# (libelle, bas, central, haut, confiance, note)
NICHES = [
    ("Élargir l'assiette de l'impôt sur la détention", 1.3, 3.0, 5.0, "faible",
     "Réintégrer les biens exonérés. Le patrimoine professionnel est l'actif "
     "le plus concentré du pays — le cinquième supérieur en détient 93 % — "
     "et c'est celui que le droit exonère le plus largement."),
    ("Aligner l'assurance-vie sur le droit commun des successions", 1.0, 2.0,
     3.5, "moyenne", ""),
    ("Fermer la purge des plus-values au décès et les reports", 1.0, 1.8, 3.0,
     "faible",
     "34 Md€ de plus-values placées en report chaque année, dont 23 pour le "
     "seul dernier centile. Il n'existe aucun chiffrage officiel français du "
     "coût de la purge : elle est absente du tome II des dépenses fiscales."),
    ("Plafonner le pacte Dutreil", 1.0, 1.7, 2.5, "moyenne-haute",
     "Le gisement le mieux documenté. Coût inscrit à 500 M€ pendant treize "
     "ans, réévalué à 5 Md€ en 2025 ; 65 % capté par 110 personnes. Aucun "
     "effet mesuré sur l'investissement ni sur l'emploi."),
    ("Foncier et revenus locatifs", 0.3, 0.5, 1.0, "moyenne",
     "Le résultat le plus décevant du rapport : 79 % de la richesse est "
     "immobilière, et c'est la partie déjà la plus lourdement taxée — "
     "43,5 Md€/an, soit 38 % de toute la fiscalité du patrimoine."),
    ("Petites niches et accès aux données", 0.2, 0.5, 1.0, "moyenne", ""),
]

TAUX = [
    ("Atteindre les revenus logés dans les holdings", 1.0, 2.5, 4.0, "faible",
     "Impôt plancher, chiffré EN MARGINAL après l'élargissement de "
     "l'assiette : chaque euro prélevé par le premier réduit d'autant "
     "l'assiette du second. C'est le double compte que le chapitre fiscal du "
     "programme n'avait pas neutralisé."),
    ("Réformer les successions et donations, hors les deux niches", 1.0, 2.3,
     4.0, "moyenne",
     "Barème et abattements seuls. Le pacte Dutreil et l'assurance-vie sont "
     "des dispositifs de succession : ils sont chiffrés à part et retirés de "
     "cette ligne."),
    ("Rachats d'actions, transactions financières, superprofits", 0.5, 1.0,
     2.0, "moyenne",
     "Mesure de l'écart entre poids politique et rendement : la taxe sur les "
     "rachats d'actions est prévue à 200 M€ en régime, soit 0,18 % de la "
     "fiscalité française du patrimoine."),
]


def _lignes(source, serie):
    return [
        {"libelle": libelle, "bas": bas, "haut": haut, "serie": serie,
         "note": "Central %s Md€/an · confiance %s. %s"
                 % (nombre(central), confiance, note)}
        for libelle, bas, central, haut, confiance, note in source
    ]


def _panneau(titre, lignes):
    return ('<p class="chart__facet-title">%s</p>' % titre) + barres(
        lignes, unite="Md€/an de rendement net de régime", maximum=5.0
    )


def _corps():
    return (
        heros(
            "+15 Md€/an",
            "de rendement supplémentaire défendable, une fois le régime "
            "atteint",
            "fourchette +7 à +26 — soit 6 à 23 % de plus que les 113,2 Md€ "
            "déjà prélevés, et sans commune mesure avec les 428 Md€/an à "
            "combler",
        )
        + legende([("mark--3", "Retirer une dérogation — un gisement "
                    "d'assiette"),
                   ("mark--2", "Relever un taux ou créer un impôt")])
        + _panneau(
            "1. Les niches : +4,8 à +16,0 Md€/an, central +9,5",
            _lignes(NICHES, 3),
        )
        + _panneau(
            "2. Les taux et impôts nouveaux : +2,5 à +10,0 Md€/an, "
            "central +5,8",
            _lignes(TAUX, 2),
        )
    )


def _donnees():
    lignes = []
    for source, nature in ((NICHES, "Niche — assiette"), (TAUX, "Taux")):
        lignes += [[libelle, nature, nombre(bas), nombre(central),
                    nombre(haut), confiance]
                   for libelle, bas, central, haut, confiance, _ in source]
    lignes += [
        ["Sous-total des niches", "Niche — assiette", "4,8", "9,5", "16,0", ""],
        ["Sous-total des taux", "Taux", "2,5", "5,8", "10,0", ""],
        ["Coût administratif — 800 à 1 500 agents", "—", "−0,1", "−0,1",
         "−0,1", "haute"],
        ["TOTAL NET DE RÉGIME", "—", "+7,2", "+15,2", "+25,9", ""],
    ]
    return table(
        ["Gisement", "Nature", "Bas", "Central", "Haut", "Confiance"],
        lignes,
        "Rendement supplémentaire défendable, en Md€/an de régime, net des "
        "réactions de comportement.",
    )


def gisements_capital():
    return figure(
        "gisements-capital",
        "Le supplément défendable vaut quinze milliards par an, et six euros sur dix viennent des niches",
        "<strong>Comment lire.</strong> Les deux panneaux partagent la même "
        "échelle : ils se comparent directement. En haut, ce qu'on gagne à "
        "retirer une dérogation à un impôt qui existe déjà ; en bas, ce qu'on "
        "gagne à relever un taux ou à créer un impôt. Le premier bloc pèse "
        "plus, et il se heurte à moins d'obstacles juridiques — retirer un "
        "avantage n'exige qu'une clause de maintien pour les engagements en "
        "cours, qui étale le rendement sans l'annuler.",
        _corps(),
        _donnees(),
        SOURCE,
        note="<strong>Deux méthodes indépendantes convergent sur un plafond "
        "d'environ 25 Md€/an</strong> : cette addition gisement par gisement, "
        "et un plafond macroéconomique tiré du revenu monétaire du patrimoine "
        "(75 % de 183 Md€, soit +24 Md€/an de marge). Les bornes hautes ne "
        "s'additionnent pas sans réserve : l'impôt plancher est chiffré en "
        "marginal après l'élargissement de l'assiette, et les trois lignes de "
        "transmission portent sur la même matière. <strong>Ce total est "
        "inférieur de 40 % à ce que le dossier lui-même supposait</strong> "
        "(+25 en valeur centrale) et très inférieur aux 90 à 100 Md€ "
        "revendiqués par le programme sur le même périmètre. La première "
        "année rapporte zéro : un impôt déclaratif voté en décembre est "
        "déclaré au printemps et recouvré à l'automne suivants.",
    )
