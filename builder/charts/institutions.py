"""Calendrier legislatif et risque constitutionnel : les deux murs de droit.

Les niveaux de risque portent les couleurs de STATUT reservees. Ces couleurs
ne separent pas des identites : elles ne passent pas le controle de separation
daltonienne quand deux aplats se touchent. Les barres de statut sont donc
toujours detachees et toujours nommees par un libelle en clair.
"""

from .bars import barres
from .base import figure, legende, nombre, table
from .figures import etapes, heros, plaques

SRC_LOI = "Source : transverse 03, véhicules législatifs et calendrier."
SRC_CONST = "Source : transverse 02, risques constitutionnels et conventionnels."


def calendrier_legislatif():
    lignes = [
        {"libelle": "Véhicules nécessaires", "bas": 96, "serie": 2,
         "note": "après regroupement optimal de 89 textes en 56"},
        {"libelle": "Capacité réelle sur cinq sessions", "bas": 51,
         "serie": 1,
         "note": "≈ 7 semaines de séance utile par session"},
    ]
    corps = (
        heros("45 textes", "manquent à l'appel sur cinq ans",
              "soit 47 % du programme législatif")
        + legende([("mark--2", "Nécessaires"), ("mark--1", "Possibles")])
        + barres(lignes, unite="textes")
        + '<p class="chart__facet-title">Le chemin critique, en cinq '
        "étapes</p>"
        + etapes([
            ("Encaissement fiscal", "an 1",
             "36 % du régime seulement : 85 Md€ de besoin transitoire cumulé."),
            ("Registres et systèmes d'information", "12 à 36 mois",
             "Baux, aides, carrières, valorisation : aucun ne relève de la loi."),
            ("Formation et recrutement", "30 à 96 mois",
             "C'est le vrai plafond du calendrier."),
            ("Processus constituant", "à partir de l'an 4",
             "Aucun effet avant la fin du mandat."),
            ("Fenêtres européennes", "calendrier exogène",
             "Budget pluriannuel 2028-2034, octroi de mer, politique agricole."),
        ])
    )
    donnees = table(
        ["Type de véhicule", "Nombre"],
        [["Lois ordinaires (après fusion de 89 textes)", "56"],
         ["Lois de programmation", "11"],
         ["Lois organiques", "11"],
         ["Véhicules budgétaires", "12"],
         ["Lois d'autorisation", "4"],
         ["Référendums", "2"],
         ["Processus constituant", "1"],
         ["Total retenu par le dossier", "96"],
         ["Capacité réelle sur cinq sessions", "51"],
         ["Écart", "45, soit 47 %"]],
        "Véhicules législatifs nécessaires, par type, et capacité réelle.",
    )
    return figure(
        "calendrier-legislatif",
        "Le Parlement peut voter la moitié des lois que le programme exige",
        "<strong>Comment lire.</strong> Deux barres sur un axe unique : 96 "
        "textes sont nécessaires, 51 sont votables en cinq sessions. Le "
        "chemin critique du bas montre que la loi n'est même pas le premier "
        "verrou — la formation des agents l'est.",
        corps,
        donnees,
        SRC_LOI,
        note="Le détail par type somme à 97 et non à 96 : le dossier ne "
        "réconcilie pas ce dernier point. Le chiffre de 51 est le plus fragile "
        "du dossier — il est marqué « à vérifier » à sa source. S'y ajoutent "
        "2 000 à 3 000 décrets et 27 fronts européens, hors de ce décompte.",
    )


RISQUES = [
    ("Rouge — censure quasi certaine", 11, "blocking",
     "La rédaction heurte frontalement un précédent exprès."),
    ("Orange — sauvable par réécriture", 28, "major",
     "Risque supérieur à 50 %, mais une variante à objectif constant existe."),
    ("Jaune — réel mais maîtrisable", 31, "medium",
     "Risque de 15 à 50 %, selon durée, seuil, périmètre ou compensation."),
    ("Bleu — verrou de rang", 14, "minor",
     "Exige une loi organique ou une révision : impossible, non censurable."),
    ("Noir — irrémédiable après révision", 13, "irremediable",
     "Bute sur un engagement international que le constituant national ne lève pas."),
]


def risque_constitutionnel():
    lignes = [
        {"libelle": libelle, "bas": compte, "serie": statut, "note": texte}
        for libelle, compte, statut, texte in RISQUES
    ]
    corps = (
        plaques([
            ("87", "mesures exposées", "sur ≈ 620 énoncés inventoriés",
             "neutre"),
            ("11", "en censure quasi certaine", "en l'état des rédactions",
             "blocking"),
            ("13", "irrémédiables", "même après révision constitutionnelle",
             "irremediable"),
        ])
        + barres(lignes, unite="mesures")
    )
    donnees = table(
        ["Niveau", "Définition", "Mesures"],
        [[libelle, texte, nombre(compte)]
         for libelle, compte, statut, texte in RISQUES],
        "Mesures exposées à un risque constitutionnel, par niveau. Les "
        "niveaux se recoupent : leur somme dépasse le total.",
    )
    return figure(
        "risque-constitutionnel",
        "Onze mesures seraient censurées en l'état, treize le resteraient après révision",
        "<strong>Comment lire.</strong> Cinq barres détachées, une par niveau "
        "de risque, chacune nommée en clair. <strong>Ce n'est pas un "
        "camembert&nbsp;:</strong> les niveaux se recoupent, et leur somme "
        "(97) dépasse le total de 87 mesures exposées.",
        corps,
        donnees,
        SRC_CONST,
        note="Le dossier déclare un recoupement de 4 mesures au niveau noir, "
        "ce qui ramène la somme à 93 — sans expliquer les 6 restantes. Les "
        "niveaux sont donc présentés comme des catégories qui se chevauchent, "
        "et jamais comme un partage du total. Le volet conventionnel est "
        "marqué « à vérifier » à sa source.",
    )
