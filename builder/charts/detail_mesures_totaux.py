"""Total publie de chaque chapitre, et l'ecart avec la somme de ses mesures.

Les valeurs viennent du tableau recapitulatif de `vulgarise/chiffrage.md`,
colonne « Central ». Elles ne sont pas recalculees ici : la fiche du chapitre
fait foi, cette figure ne fait que la citer.

La somme des mesures d'un chapitre ne retombe jamais sur ce total, et l'ecart
va dans les deux sens. Il se lit, chapitre par chapitre, comme le prix des
consolidations : doubles comptes retires, variantes exclusives comptees une
seule fois, milieux de fourchette substitues aux bornes.
"""

TITRES = {
    1: "Institutions", 2: "Propriété et nationalisations",
    3: "Entreprise et communes", 4: "Libertés et justice",
    5: "Éducation et service citoyen", 6: "Fiscalité",
    7: "Solidarité, logement, justice sociale", 8: "Travail et retraites",
    9: "Industrie et salaires publics", 10: "Égalité, grand âge, handicap",
    11: "Culture et sport", 12: "Planification écologique",
    13: "Grands chantiers", 14: "Biens communs",
    15: "Santé", 16: "Diplomatie et défense", 17: "Europe",
    18: "Mer, espace, numérique",
}

# chapitre : (central Md€/an, precision sur le perimetre du total publie)
TOTAUX = {
    1: (0.61, ""),
    2: (2.93, "flux annuel seul : le capital, 23 à 390 Md€, est hors total"),
    3: (4.80, ""),
    4: (2.33, ""),
    5: (77.0, "net de la part éducation du point d'indice, transférée au ch. 9"),
    6: (None, "il ne dépense pas, il encaisse"),
    7: (71.5, ""),
    8: (137.85, "après transferts vers les ch. 9 et 15 et annulation d'une recette"),
    9: (46.5, "point d'indice consolidé des chapitres 5, 8 et 9"),
    10: (73.0, "net du service citoyen, déjà compté au ch. 5"),
    11: (13.85, ""),
    12: (55.3, "enveloppe climat consolidée, comptée une seule fois"),
    13: (55.3, "enveloppe climat consolidée, comptée une seule fois"),
    14: (4.75, "part du budget de l'État seule, hors redevances"),
    15: (19.0, "net de la recette de substitution qui gage le 100 % Sécu"),
    16: (14.65, ""),
    17: (4.5, "coût d'une désobéissance ciblée, et non du bras de fer généralisé"),
    18: (7.9, ""),
}

CONJOINTS = (12, 13)


def total_publie(chapitre):
    """(central, precision). `central` vaut None quand le chapitre n'en a pas."""
    return TOTAUX.get(chapitre, (None, ""))


def titre(chapitre):
    return TITRES.get(chapitre, "Chapitre %d" % chapitre)
