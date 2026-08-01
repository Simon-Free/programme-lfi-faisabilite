"""D'ou viennent les recettes nouvelles, et quand elles arrivent.

Le brut ne fait pas le net : trois blocs se retranchent du rendement des
mesures — les mesures de cout du chapitre, ses doubles comptes internes, et
la part deja gagee ailleurs. Ces trois blocs sont dessines a part, sur le
meme axe, parce qu'ils sont de meme nature : des euros de rendement annuel.

Chiffres : `transverses/04_bouclage_macrobudgetaire.md` § 5.5 (compte de
recettes, bornes basse et haute) et § 6.1 (montee en charge).
"""

from .bars import barres
from .base import figure, nombre, table
from .figures import heros

SOURCE = (
    "Source : compte de recettes de la transverse 04, § 5.5, et son profil de "
    "montée en charge, § 6.1 ; profil concurrent de l'analyse du chapitre 6, "
    "§ 5.5 ; confrontation des deux et reconstitution dans l'audit du compte "
    "de recettes, transverse 25, § 5."
)

# (libelle, bas, haut, note) — rendement de regime, avant retranchements.
POSTES = [
    ("CSG progressive à 14 tranches", 10.0, 25.0,
     "Le poste le plus lourd — et le seul dont aucun barème n'est publié : "
     "à lui seul 103 Md€/an d'amplitude. Intégralement pré-empté par le "
     "100 % Sécu."),
    ("Impôt sur le revenu à 14 tranches", 5.0, 12.0, "Barème non publié."),
    ("Successions, héritage plafonné", 5.0, 11.0, ""),
    ("Impôt sur les sociétés progressif", 5.0, 9.0,
     "Retenu contre la mesure concurrente du chapitre 8."),
    ("Niches fiscales", 2.0, 12.0, ""),
    ("Fin du quotient conjugal", 2.0, 7.0, ""),
    ("Superprofits permanents", 2.0, 6.0, ""),
    ("Fraude et évasion fiscales", 2.0, 4.5,
     "Élasticité effectif/rendement de 0,35 : doubler les agents ne double "
     "pas le recouvrement."),
    ("Taxe sur les transactions financières", 3.0, 4.5,
     "Révisé à la hausse : le précédent suédois était mal transposé."),
    ("Impôt sur la fortune renforcé", 1.4, 3.1,
     "Recalculé au coefficient d'érosion corrigé, de 0,46 à 0,26 : la ligne "
     "valait 2,5 à 5,5."),
    ("Taxe foncière progressive", 0.0, 4.0, ""),
    ("Impôt universel", 1.1, 4.5, ""),
    ("Capital au barème", 1.5, 3.5, ""),
    ("Taxe Zucman, après imputation sur l'ISF", 0.5, 3.0,
     "Impôt plancher imputable sur l'ISF : non additif."),
    ("Socialisation bancaire", -1.42, 1.19,
     "Nette de la charge de portage, 5,79 à 8,40 Md€/an, omise par le "
     "chapitre. Le pôle BNP Paribas + Société générale vaut 180,9 Md€ au "
     "cours et 235 à 262 avec la prime de contrôle que l'offre publique "
     "obligatoire impose : la charge excède alors le dividende, et la "
     "ligne devient négative."),
    ("Arbitrage de dividendes (CumEx)", 0.8, 1.8, ""),
    ("Exit tax et cinq mesures mineures", 1.05, 2.6, ""),
]

# (libelle, bas, haut, note) — ce qui se retranche, en valeur absolue.
RETRANCHEMENTS = [
    ("Doubles comptes internes au chapitre", 8.0, 20.0,
     "Sept recouvrements ; le plus lourd — impôt sur le revenu, CSG et "
     "capital au barème sur la même assiette — vaut 8 à 15 Md€/an et "
     "n'était neutralisé à aucun niveau."),
    ("Part pré-emptée par le 100 % Sécu", 10.0, 25.0,
     "La même assiette CSG ne finance pas deux fois. Corrigée ensuite à "
     "50 % de pré-emption dans le total retenu."),
    ("Mesures de coût du chapitre", 12.4, 12.45,
     "Dont la TVA de première nécessité, −6 à −10 Md€/an : la seule mesure "
     "de coût majeure du bloc, absente de l'addition publiée."),
    ("Provision sur les cinq barèmes inédits", 5.0, 7.0,
     "Impôt sur le revenu, CSG, impôt sur les sociétés, impôt sur la "
     "fortune, successions : aucun n'est écrit."),
]

# (annee, part du regime, note) — le dossier porte DEUX profils
# incompatibles et ne le signale nulle part. Les deux sont donc traces.
MONTEE = [
    ("An 1 — profil du chapitre 6", 36,
     "Calibré sur une hypothèse médiane de 70 Md€ en régime, que le compte "
     "consolidé a divisée par deux à trois sans recalculer les parts."),
    ("An 1 — profil de la transverse 04", 20,
     "Aucune recette majeure n'est encaissable : l'ISF rend 0 %, la taxe "
     "Zucman 0 %, la CSG 0 à 20 %. Seuls l'impôt sur le revenu et le "
     "quotient conjugal répondent vite."),
    ("An 1 — reconstitution sur le compte consolidé", 31,
     "Chaque ligne du compte affectée de son propre délai d'encaissement, "
     "pondérée par les montants consolidés."),
    ("An 2 — profil du chapitre 6", 64, ""),
    ("An 2 — profil de la transverse 04", 52, ""),
    ("An 2 — reconstitution sur le compte consolidé", 58, ""),
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


def sources_recettes():
    corps = (
        heros(
            "36 à 50 Md€",
            "de dépense tombent dès la première année, par décret, contre 2 à "
            "10 Md€ de recette",
            "et la seule mesure fiscale qui produise 100 % de son effet dès "
            "le premier jour est une mesure de coût : la baisse de TVA de "
            "première nécessité, −6 à −10 Md€/an",
        )
        + _panneau(
            "1. Ce que rapportent les mesures, avant retranchement (Md€/an)",
            _lignes(POSTES, 3),
            "Md€/an de rendement de régime",
        )
        + _panneau(
            "2. Ce qui se retranche de ce brut (Md€/an, en valeur absolue)",
            _lignes(RETRANCHEMENTS, 2),
            "Md€/an retranchés",
        )
        + _panneau(
            "3. Quand la recette arrive — et le dossier porte deux profils "
            "qui ne se parlent pas <em>(autre unité, autre axe)</em>",
            [{"libelle": annee, "bas": part, "serie": 7, "note": note}
             for annee, part, note in MONTEE],
            "% du rendement de régime encaissé",
        )
    )
    donnees = table(
        ["Poste", "Bas (Md€/an)", "Haut (Md€/an)"],
        [[libelle, nombre(bas), nombre(haut)]
         for libelle, bas, haut, _ in POSTES]
        + [["Sous-total des postes positifs", "40,93", "114,69"]]
        + [["moins " + libelle, "−" + nombre(bas), "−" + nombre(haut)]
           for libelle, bas, haut, _ in RETRANCHEMENTS]
        + [["Rendement disponible pour le solde, tel que publié", "10,9",
            "68,6"],
           ["<strong>Le même, refait ligne à ligne</strong>",
            "<strong>−2,6</strong>", "66,3"],
           ["Total retenu après révision de la pré-emption", "18,9", "77,6"],
           ["<strong>Compte de recettes corrigé, rebranché sur le bloc "
            "consolidé</strong>", "<strong>−2,3</strong>",
            "<strong>70,1</strong>"],
           ["Valeur centrale corrigée", "33,9", "33,9"]],
        "Compte de recettes nouvelles, poste par poste, en Md€/an de régime.",
    )
    return figure(
        "sources-recettes",
        "Un tiers du rendement brut disparaît avant d'atteindre le solde, et la seule recette immédiate est négative",
        "<strong>Comment lire.</strong> Le premier panneau donne ce que chaque "
        "mesure rapporte en régime ; le deuxième, ce qui s'en retranche — "
        "mesures de coût oubliées de l'addition publiée, recouvrements entre "
        "impôts frappant la même assiette, part déjà promise à une autre "
        "dépense. Le troisième change d'unité : il ne compte plus des euros "
        "mais la part du régime encaissée chaque année — et il montre que le "
        "dossier porte <em>deux</em> profils de montée en charge, écartés de "
        "seize points en première année, sans qu'aucun des deux fichiers "
        "mentionne l'autre.",
        corps,
        donnees,
        SOURCE,
        note="<strong>Le calendrier ne décide de rien, et c'est le résultat "
        "du troisième panneau.</strong> Que les recettes montent en 36/64 ou "
        "en 20/52, l'écart cumulé sur cinq ans est de l'ordre de 15 à 20 Md€ "
        "— face à un besoin de financement cumulé de 1 865 Md€ sur la même "
        "période. Le débat sur la montée en charge porte sur 1 % du problème : "
        "« le problème n'est pas que l'argent arrive tard, c'est qu'il "
        "n'arrive pas ». Aucun des deux profils n'est adossé à une source "
        "externe ; le premier est calibré sur un régime de 70 Md€ qui "
        "n'existe plus. <strong>Deux corrections sur ce compte, et l'une est "
        "défavorable au programme.</strong> La borne basse publiée, 10,9 "
        "Md€/an, n'est pas reconstituable : c'est le rendement brut retraité "
        "recopié sans lui appliquer les trois lignes qui suivent. Refaite, "
        "elle vaut −2,6 — <strong>dans le scénario bas, le compte de recettes "
        "du programme est nul</strong>, et le signe n'est pas garanti. En "
        "sens inverse, le rebranchement du bloc consolidé des cinq barèmes "
        "sur le compte complet porte la valeur centrale à 33,9 Md€/an. "
        "Les totaux successivement publiés sur ce site — 18,9 / 44,3 / 77,6 "
        "puis 21,2 — ne sont pas la somme arithmétique du panneau 1 moins le "
        "panneau 2, et surtout <strong>ils ne mesuraient que les cinq barèmes "
        "fiscaux</strong>. La décomposition par poste n'a jamais été "
        "republiée après ces arbitrages : elle est donnée ici telle que le "
        "compte de recettes l'établit, et les totaux corrigés figurent dans "
        "le tableau de données. Le chiffrage complet des ressources "
        "opposables — 84,6 Md€/an — vit dans la figure du taux de couverture.",
    )
