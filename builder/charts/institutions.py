"""Calendrier legislatif et risque constitutionnel : les deux murs de droit.

Les niveaux de risque portent les couleurs de STATUT reservees. Ces couleurs
ne separent pas des identites : elles ne passent pas le controle de separation
daltonienne quand deux aplats se touchent. Les barres de statut sont donc
toujours detachees et toujours nommees par un libelle en clair.
"""

from .bars import barres
from .base import figure, legende, nombre, table
from .figures import etapes, heros, plaques

SRC_LOI = ("Source : transverse 35, capacité parlementaire mesurée sur les "
           "statistiques de séance de l'Assemblée nationale et du Sénat.")
SRC_CONST = "Source : transverse 02, risques constitutionnels et conventionnels."

# Véhicules législatifs supposés par le programme, après regroupement. Chiffre
# reconstruit par le dossier, non établi par une source externe.
VEHICULES_NECESSAIRES = 96

# Capacité mesurée sur cinq sessions ordinaires, hors conventions
# internationales : valeur centrale et intervalle observé (sessions de 43 à
# 67 lois, mesurées de 2007-2008 à 2025-2026).
CAPACITE_TOUTES_LOIS = 260
CAPACITE_BASSE = 215
CAPACITE_HAUTE = 335

# Capacité du seul canal gouvernemental sur cinq sessions, selon la majorité.
CAPACITE_GOUV_ABSOLUE = 170
CAPACITE_GOUV_RELATIVE = 70

# Projets de loi hors conventions aboutis par session, selon la majorité.
PROJETS_ABSOLUE = 34
PROJETS_RELATIVE = 14


def calendrier_legislatif():
    lignes = [
        {"libelle": "Lois adoptées en cinq sessions, hors conventions",
         "bas": CAPACITE_TOUTES_LOIS, "serie": 1,
         "note": f"mesuré : {CAPACITE_BASSE} à {CAPACITE_HAUTE} selon la "
         "session"},
        {"libelle": "Véhicules supposés par le programme",
         "bas": VEHICULES_NECESSAIRES, "serie": 2,
         "note": "après regroupement de 89 textes en 56 — chiffre estimé"},
        {"libelle": "dont canal gouvernemental, majorité absolue",
         "bas": CAPACITE_GOUV_ABSOLUE, "serie": 1,
         "note": f"{PROJETS_ABSOLUE} projets de loi aboutis par session"},
        {"libelle": "dont canal gouvernemental, majorité relative",
         "bas": CAPACITE_GOUV_RELATIVE, "serie": 1,
         "note": f"{PROJETS_RELATIVE} projets de loi aboutis par session"},
    ]
    recul = round(
        100 * (PROJETS_ABSOLUE - PROJETS_RELATIVE) / PROJETS_ABSOLUE)
    corps = (
        heros(f"−{recul} %", "de projets de loi aboutis sans majorité absolue",
              f"de {PROJETS_ABSOLUE} à {PROJETS_RELATIVE} par session")
        + legende([("mark--2", "Supposés par le programme"),
                   ("mark--1", "Mesurés")])
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
        ["Session", "Lois hors conventions", "dont propositions de loi",
         "Majorité"],
        [["2018-2019", "50", "25", "Absolue"],
         ["2019-2020", "42", "18", "Absolue"],
         ["2020-2021", "54", "19", "Absolue"],
         ["2021-2022", "61", "41", "Absolue"],
         ["2022-2023", "44", "29", "Relative"],
         ["2023-2024", "51", "30", "Relative"],
         ["2024-2025", "56", "45", "Relative"],
         ["2025-2026", "43", "—", "Relative"]],
        "Textes définitivement adoptés par session, hors conventions "
        "internationales. Sources : recueils statistiques de l'Assemblée "
        "nationale et rapports annuels de la direction de la Séance du Sénat, "
        "qui donnent des valeurs identiques sur les sessions récentes.",
    )
    return figure(
        "calendrier-legislatif",
        "Le Parlement vote assez de lois ; c'est le canal du gouvernement "
        "qui se ferme",
        "<strong>Comment lire.</strong> Quatre barres sur un axe unique. La "
        f"première, {CAPACITE_TOUTES_LOIS} lois, est ce que le Parlement "
        "adopte réellement en cinq sessions hors conventions internationales. "
        f"La deuxième, {VEHICULES_NECESSAIRES}, est ce que le programme "
        "suppose. Les deux dernières isolent le seul canal gouvernemental, "
        f"qui se contracte de {recul} % en l'absence de majorité absolue.",
        corps,
        donnees,
        SRC_LOI,
        note="Les conventions internationales, écartées ici, représentent 19 "
        "à 34 % du volume législatif brut. Le chiffre de 96 est reconstruit "
        "par le dossier et non établi par une source externe : son détail par "
        "type somme à 97, voire à 102 selon le traitement des lois organiques "
        "d'application. S'y ajoutent 2 000 à 3 000 décrets et 27 fronts "
        "européens, hors de ce décompte.",
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
