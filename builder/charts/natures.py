"""Les trois natures de cout, et pourquoi elles ne s'additionnent jamais.

Regle de la transverse 20 : un flux annuel recurrent, un investissement
ponctuel etale et une acquisition d'actif ne partagent JAMAIS un axe. Le
dessin EST la demonstration : le lecteur voit que les barres ne peuvent pas
se toucher. Le seul axe qui les reunit legitimement vit dans
`decaissement.py`.

Chiffres : `transverses/20_ponctuel_vs_recurrent.md` § 1, § 3.1, § 3.2 et
§ 4, construits sur `transverses/04` § 5.4.
"""

from .bars import barres
from .base import figure, table
from .figures import heros

SOURCE = (
    "Source : transverse 20, § 3 (coût ponctuel) et § 4 (acquisitions "
    "d'actifs, d'après la consolidation des postes 6 à 10)."
)

RECURRENT = [
    ("Dépense récurrente, en régime", 460, 460,
     "Revient chaque année, indéfiniment. Lecture littérale consolidée."),
]

PONCTUEL = [
    ("Investissement non récurrent — publié partout", 175, 305,
     "Étalé sur dix ans, puis s'arrête. Soit 18 à 31 Md€/an pendant la "
     "période. Bâti sur la transverse 04, § 5.4 (a)."),
    ("→ total corrigé, quatre omissions réintégrées", 193, 384,
     "La contre-analyse du chapitre 5 prime sur l'analyse (100-226 au lieu "
     "de 102-183) ; les 15 à 30 Md€ d'équipements culturels et sportifs du "
     "chapitre 11, les 1,06 à 1,99 du chapitre 14, les 1,71 à 3,25 du "
     "chapitre 7 et le référendum du chapitre 17 manquaient au consolidé. "
     "La borne haute se déplace de 26 %."),
]

# (libelle, bas, haut, note) — le decaissement, operation par operation.
OPERATIONS = [
    ("Pôle bancaire — BNP Paribas et Société générale", 235.2, 262.3,
     "Le poste le plus lourd, et celui qui coûte le MOINS au déficit : zéro, "
     "s'il est acheté au cours. Il pèse en revanche 7,9 à 8,8 points de "
     "dette. Le programme ne date pas l'opération."),
    ("Engie — 77,36 % du capital", 70.1, 78.2,
     "Zéro au prix de marché ; −16,2 à −24,3 Md€ de déficit si la prime de "
     "contrôle est requalifiée."),
    ("Autoroutes — résiliation anticipée", 47, 55,
     "Le poste le plus léger, et celui qui coûte le PLUS au déficit : la "
     "totalité, parce qu'une indemnité de résiliation n'achète aucun actif. "
     "C'est aussi le seul que le programme peut annuler sans renoncer à son "
     "objectif, en attendant les échéances de 2031-2036."),
    ("EDF", 0, 0,
     "Zéro : l'opération a été réalisée le 8 juin 2023. Le programme la "
     "demande encore ; elle est déjà faite."),
]

BILAN = [
    ("Décaissement total, lecture littérale", 352, 395,
     "À financer intégralement par emprunt, même quand le déficit ne bouge "
     "pas : il n'existe aucune configuration où un achat d'actions financé "
     "par emprunt laisse la dette brute inchangée."),
    ("dont part frappant réellement le déficit", 47, 161,
     "Indemnités de résiliation et primes de contrôle : rien n'est acheté "
     "en échange. Soit 1,6 à 5,4 points de PIB sur un seul exercice."),
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


def _corps():
    return (
        heros(
            "460 Md€/an",
            "de dépense récurrente — le seul montant qui revient chaque année",
            "plus 193 à 384 Md€ d'investissement étalé sur dix ans et 352 à "
            "395 Md€ d'acquisitions d'actifs : trois natures, trois axes, "
            "aucune addition",
        )
        + _panneau(
            "1. Coût récurrent (Md€/an) — revient chaque année",
            _lignes(RECURRENT, 1),
            "Md€/an",
        )
        + _panneau(
            "2. Coût ponctuel (Md€, sur dix ans) — "
            "<em>autre unité, autre axe</em>",
            _lignes(PONCTUEL, 3),
            "Md€ sur dix ans",
        )
        + _panneau(
            "3. Acquisitions d'actifs, opération par opération (Md€ décaissés "
            "une fois) — <em>troisième nature, troisième axe</em>",
            _lignes(OPERATIONS, 7),
            "Md€ décaissés une fois",
        )
        + _panneau(
            "4. Et ce que ces acquisitions font vraiment au déficit",
            _lignes(BILAN, 7),
            "Md€, une fois",
        )
    )


def _donnees():
    lignes = [
        ["Coût récurrent", "460", "460", "Md€/an",
         "Dégrade le déficit chaque année, indéfiniment"],
        ["Coût ponctuel — publié", "175", "305", "Md€ (10 ans)",
         "Dégrade le déficit pendant la période, puis s'arrête"],
        ["Coût ponctuel — corrigé", "193", "384", "Md€ (10 ans)",
         "Chapitres 7, 11, 14 et 17 réintégrés, chapitre 5 à sa valeur de "
         "contre-analyse"],
    ]
    lignes += [[libelle, str(bas), str(haut), "Md€ (une fois)",
                "Décaissement de l'opération"]
               for libelle, bas, haut, _ in OPERATIONS]
    lignes += [
        ["Acquisitions — décaissement total", "352", "395", "Md€ (une fois)",
         "Neutre au déficit au prix de marché ; augmente la dette brute"],
        ["dont part frappant le déficit", "47", "161", "Md€ (une fois)",
         "Transfert en capital : aucune contrepartie d'actif"],
        ["Reclassement de la dette d'EDF", "51,5", "51,5", "Md€ de dette",
         "Aucune des trois natures : un effet de reclassement statistique, "
         "sans le moindre décaissement — 1,72 point de PIB"],
    ]
    return table(
        ["Nature ou opération", "Bas", "Haut", "Unité",
         "Ce qu'elle fait au déficit"],
        lignes,
        "Les trois natures de coût du programme, chacune avec son unité "
        "propre, et le détail des acquisitions d'actifs.",
    )


def natures_du_cout():
    return figure(
        "natures-du-cout",
        "Trois natures de coût, trois axes : elles ne s'additionnent jamais",
        "<strong>Comment lire.</strong> Quatre panneaux séparés, et c'est "
        "l'essentiel du dessin : un euro dépensé <em>chaque année</em>, un "
        "euro dépensé <em>une fois</em> et un euro <em>échangé contre un "
        "actif</em> ne sont pas la même grandeur. Les mettre sur un même axe "
        "donnerait « environ mille milliards » — un nombre qui ne veut rien "
        "dire. Les deux derniers panneaux ouvrent les acquisitions, où la "
        "lecture s'inverse deux fois.",
        _corps(),
        _donnees(),
        SOURCE,
        note="<strong>Les acquisitions se lisent à l'envers de l'intuition.</"
        "strong> Le poste le plus lourd — le pôle bancaire, 235 à 262 Md€ — "
        "est celui qui coûte le moins au déficit : zéro, s'il est acheté au "
        "cours. Le plus léger — les autoroutes, 47 à 55 Md€ — est celui qui "
        "coûte le plus : la totalité. Et le panneau 4 n'est pas une "
        "cinquième catégorie : ses 47 à 161 Md€ sont un <em>sous-ensemble</em> "
        "du décaissement du panneau 3. Le panneau 2 publie côte à côte le "
        "montant repris partout dans le dossier (175-305) et son total "
        "corrigé (193-384) : la correction n'a pas été reportée ailleurs, "
        "parce qu'elle suppose de rouvrir le bouclage macrobudgétaire. "
        "La transverse 18 sur les bénéfices de la propriété publique, annoncée "
        "quand ce panneau a été dessiné et produite depuis, confirme les "
        "352-395 Md€, les 47-161 Md€ de part frappant le déficit et la "
        "valorisation du pôle bancaire à 235,20-262,33.",
    )
