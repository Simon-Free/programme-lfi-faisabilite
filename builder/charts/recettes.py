"""Le taux de couverture et sa degradation, puis l'origine des recettes.

Deux figures qui ne partagent aucun axe : la premiere compte des euros de
solde et des pourcentages de couverture — deux panneaux, deux unites ; la
seconde compte des euros de rendement et des parts de montee en charge.

Chiffres verifies dans `vulgarise/chiffrage.md` (§ taux de couverture),
`transverses/25_audit_recettes_et_economies.md` § 7.2, § 7.3 et § 8.1, et
`transverses/04_bouclage_macrobudgetaire.md` § 5.5.

L'historique des valeurs anterieurement publiees est tenu dans
`vulgarise/journal_des_modifications.md`, pas dans la figure.
"""

from .bars import barres
from .base import figure, legende, table
from .figures import heros, jauge

SOURCE = (
    "Source : page « Combien ça coûte », § taux de couverture ; audit du "
    "compte de recettes, transverse 25, § 7.2 (compte de financement), § 7.3 "
    "(taux de couverture) et § 8.1 (décomposition du compte)."
)

# (libelle, montant, note) — les 86,9 Md€/an de ressources opposables.
ECART = [
    ("Cinq barèmes fiscaux du chapitre 6", 21.2,
     "Impôt sur le revenu, contribution sociale généralisée, impôt sur les "
     "sociétés, impôt sur la fortune, successions. Aucun barème n'étant "
     "publié, l'amplitude de ce seul bloc est d'un facteur cinq."),
    ("Douze autres lignes de recette", 14.95,
     "Transactions financières, niches, fraude, quotient conjugal, "
     "superprofits, capital au barème, impôt universel, taxe Zucman, "
     "socialisation bancaire, CumEx, foncier progressif, exit tax — net des "
     "lignes de coût et du retraitement."),
    ("Effets de retour — dépenses évitées", 22.2,
     "Calculées chapitre par chapitre, perdues à la consolidation, qui n'a "
     "retenu que la colonne des coûts. C'est une dépense qui n'a pas lieu, "
     "pas une recette."),
    ("Effets de retour — recettes induites", 17.8,
     "Cotisations et impôts produits par les emplois et les revenus que la "
     "dépense nouvelle crée. Même mécanisme d'omission."),
    ("TVA sur la consommation induite par les transferts", 4.5,
     "Nette de la baisse de TVA de première nécessité que le programme "
     "porte lui-même, qui frappe le même panier."),
    ("Économies proposées par le programme, non comptées", 3.6,
     "Nettes des recouvrements. Une soixantaine de mesures recensées, dont "
     "aucune n'est chiffrée par le programme — et les plus lourdes étaient "
     "déjà comptées sans être nommées."),
    ("Dividendes des entités publiques", 2.35,
     "Produit récurrent des acquisitions, net de ce que la strate des "
     "effets de retour contenait déjà."),
    ("Recettes de sanction", 0.25,
     "Pénalités et amendes nouvelles créées par le programme."),
]


def _panneau(titre, lignes, unite):
    return ('<p class="chart__facet-title">%s</p>' % titre) + barres(
        lignes, unite=unite
    )


def couverture_recettes():
    corps = (
        heros(
            "18,9 %",
            "des dépenses nouvelles sont couvertes par une ressource nouvelle",
            "moins d'un euro sur cinq ; il manque 373 Md€/an",
        )
        + legende([("mark--2", "Prélèvements et recettes nouvelles"),
                   ("mark--1", "Dépenses évitées et économies")])
        + _panneau(
            "D'où viennent les 86,9 Md€/an de ressources opposables",
            [{"libelle": libelle, "bas": montant,
              "serie": 1 if libelle.startswith(
                  ("Effets de retour — dépenses", "Économies")) else 2,
              "note": note}
             for libelle, montant, note in ECART],
            "Md€/an de ressource opposable",
        )
        + jauge(
            18.9,
            "Dix-neuf euros sur cent",
            "voilà ce qu'une ressource nouvelle identifiée finance. Les 81,1 "
            "autres ne le sont pas.",
        )
    )
    donnees = table(
        ["Lecture", "Dépense (Md€/an)", "Ressources (Md€/an)",
         "Solde à combler", "Couverture"],
        [["<strong>Point central</strong>", "460",
          "<strong>86,9</strong>", "<strong>−373</strong>",
          "<strong>18,9 %</strong>"],
         ["Fourchette", "460", "31,4 à 142,3", "−429 à −318",
          "6,8 à 30,9 %"],
         ["Convention alternative — économies au dénominateur", "434,7",
          "61,1", "−373", "14,1 %"]],
        "Solde annuel à combler et taux de couverture des dépenses nouvelles "
        "par les ressources nouvelles opposables.",
    )
    return figure(
        "couverture-recettes",
        "Moins d'un euro sur cinq est couvert — il reste 373 Md€ à trouver chaque année",
        "<strong>Comment lire.</strong> Chaque barre est une composante des "
        "86,9 Md€/an de ressources que l'on peut opposer aux 460 Md€/an de "
        "dépense nouvelle. Elles ne sont pas de même nature : un prélèvement "
        "nouveau crée une recette, une dépense évitée supprime une charge. "
        "La jauge donne la part de la dépense qu'une ressource identifiée "
        "finance.",
        corps,
        donnees,
        SOURCE,
        note="<strong>Le solde, et non le taux, porte le verdict.</strong> "
        "Les dépenses évitées et les économies (25,8 Md€/an) ne sont pas des "
        "prélèvements nouveaux : portées en réduction du dénominateur plutôt "
        "qu'au numérateur, elles donnent un taux de 14,1 % — et le même "
        "solde de 373, qui est invariant. La borne basse du compte de "
        "recettes vaut −0,2 : dans le scénario défavorable, le programme "
        "n'a aucune recette nouvelle nette, et conserve ses 460 Md€/an de "
        "dépense.",
    )
