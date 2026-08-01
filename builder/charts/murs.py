"""Niveaux de confiance et mur de la main-d'oeuvre.

Les niveaux de confiance et de risque portent les couleurs de STATUT reservees.
Ces couleurs ne separent pas des identites : elles ne passent pas le controle de
separation daltonienne quand deux aplats se touchent. Les barres de statut sont
donc toujours detachees et toujours nommees par un libelle en clair.
"""

from .bars import barres
from .base import figure, legende, nombre, table
from .figures import heros, ratio

SRC_CONF = "Source : feuille de route de consolidation, § classement des postes."
SRC_MO = "Source : transverse 01, besoins en main-d'œuvre consolidés."

NIVEAUX = [
    ("P1 — critique", 15, 380, "blocking",
     "Déplace le consolidé de plus de 5 Md€/an, ou renverse un verdict."),
    ("P2 — significatif", 34, 75, "major",
     "Déplace le consolidé de 1 à 5 Md€/an."),
    ("P3 — cosmétique", 61, 12, "minor",
     "Moins de 1 Md€/an, ou correction de forme."),
]


def niveaux_confiance():
    nombre_lignes = [
        {"libelle": libelle, "bas": compte, "serie": statut, "note": texte}
        for libelle, compte, _, statut, texte in NIVEAUX
    ]
    ampleur_lignes = [
        {"libelle": libelle, "bas": montant, "serie": statut, "note": texte}
        for libelle, _, montant, statut, texte in NIVEAUX
    ]
    corps = (
        heros(
            "91 %",
            "du chiffre publiable repose sur des chiffrages fragiles",
            "soit environ 420 Md€/an sur les 460 publiés",
        )
        + '<p class="chart__facet-title">Combien de postes, par niveau</p>'
        + barres(nombre_lignes, unite="postes")
        + '<p class="chart__facet-title">Ce que ces postes déplacent, '
        "par niveau</p>"
        + barres(ampleur_lignes, unite="Md€/an")
    )
    donnees = table(
        ["Niveau", "Définition", "Nombre de postes", "Amplitude (Md€/an)"],
        [
            [libelle, texte, nombre(compte), "≈ %s" % nombre(montant)]
            for libelle, compte, montant, _, texte in NIVEAUX
        ],
        "Postes fragiles par niveau de criticité : effectif et amplitude.",
    )
    return figure(
        "niveaux-confiance",
        "Quinze postes sur cent dix décident de l'essentiel du chiffrage",
        "<strong>Comment lire.</strong> Deux panneaux, deux grandeurs "
        "différentes, donc deux axes séparés — jamais superposés. Les P1 sont "
        "les moins nombreux (15 sur 110) mais concentrent l'essentiel de "
        "l'amplitude : ce sont eux qu'il faut lever en premier.",
        corps,
        donnees,
        SRC_CONF,
        note="Les trois niveaux se lisent au libellé, jamais à la couleur "
        "seule : la teinte redit le libellé, elle ne le remplace pas.",
    )


COLLISIONS = [
    ("Soignants", 560, 810, 5, 10,
     "Solde net de 5 000 à 10 000 infirmiers par an ; solde négatif chez les "
     "aides-soignants."),
    ("Bâtiment", 295, 420, 120, 240,
     "120 000 à 240 000 créations nettes de filière, mais sur onze ans."),
    ("Enseignants", 151, 155, 21.5, 21.5,
     "21 484 admis à tous les concours, dont 12 000 de simple remplacement."),
]


def mur_main_doeuvre():
    lignes = []
    for titre, dem_b, dem_h, off_b, off_h, texte in COLLISIONS:
        lignes.append({"libelle": titre, "bas": dem_b, "haut": dem_h,
                       "serie": 2, "note": "demandé par le programme"})
        lignes.append({"libelle": "→ réellement disponible", "bas": off_b,
                       "haut": off_h, "serie": 3, "note": texte})
    corps = (
        ratio((420000, "emplois demandés par an, pendant cinq ans"),
              (90000, "créations nettes par an dans le pays"))
        + '<p class="chart__facet-title">Les trois collisions internes : le '
        "programme se dispute sa propre main-d'œuvre</p>"
        + legende([("mark--2", "Demandé par le programme"),
                   ("mark--3", "Réellement disponible")])
        + barres(lignes, unite="milliers d'emplois")
    )
    donnees = table(
        ["Métier", "Demandé (milliers)", "Disponible (milliers)", "Verrou"],
        [
            [titre, "%s à %s" % (nombre(db), nombre(dh)),
             "%s à %s" % (nombre(ob), nombre(oh)), texte]
            for titre, db, dh, ob, oh, texte in COLLISIONS
        ],
        "Emplois demandés par le programme contre viviers réellement "
        "mobilisables.",
    )
    return figure(
        "mur-main-doeuvre",
        "Le programme demande quatre à cinq fois la main-d'œuvre que le pays crée",
        "<strong>Comment lire.</strong> Le besoin total est de 1,86 à 2,35 "
        "millions d'emplois sur cinq ans, soit 370 000 à 470 000 par an. "
        "L'économie française en crée 90 000 nets par an. Les trois paires du "
        "bas montrent que les chapitres se disputent les mêmes personnes : "
        "ce qui est promis en cinq ans en demande douze à quinze.",
        corps,
        donnees,
        SRC_MO,
        note="Neuf collisions ont été identifiées et chiffrées ; les trois "
        "plus graves sont représentées ici.",
    )
