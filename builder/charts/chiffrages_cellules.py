"""Lire une cellule de tableau d'analyse : un montant, une unite, une nature.

Les dix-huit § 4 « Chiffrage consolide » n'ont pas ete ecrits pour une machine.
Leurs en-tetes varient — « Cout net », « Cout net bas », « Rendement net (bas –
haut) », « Montant (Md€) » —, leur unite se declare tantot dans l'en-tete,
tantot dans le chapeau, tantot dans la cellule, et leurs fourchettes s'ecrivent
« 2 a 3 » ici, « 0,012 – 0,020 » la.

Ce module ne fait que lire ces formes. Il refuse plutot que de deviner : une
cellule dont l'unite ne se lit nulle part, ou dont la valeur est negative,
qualifiee dans le temps ou marquee « recette », ne rend aucun montant.
"""

from __future__ import annotations

import re

SEPARATEUR = re.compile(r"^[\s|:-]+$")
REFERENCE = re.compile(r"M-(\d+)\.(\d+)")
NOMBRE = re.compile(r"(-|–|−)?\s*(\d[\d   ]*(?:[.,]\d+)?)")

# Cellules qui ne portent pas un cout de mesure. Les qualificatifs de duree
# (« +13 a 15 Md€ la 1re annee, puis negatif ») decrivent une trajectoire, pas
# un cout de croisiere : les placer sur une echelle de couts serait faux.
NON_COUT = re.compile(
    r"recette|non retenu|non chiffr|sans objet"
    r"|1re année|1ère année|première année|puis |s'annule|théoriq|ensuite",
    re.I,
)
PONCTUEL = re.compile(r"non récurrent|en capital|une fois|cumulé", re.I)
RECURRENT = re.compile(r"€\s*/\s*an|par an|annuel|récurrent|croisière", re.I)


def propre(cellule):
    return cellule.replace("**", "").replace("*", "").replace("`", "").strip()


def cellules(ligne):
    return [propre(part) for part in ligne.split("|")[1:-1]]


def tableaux(section):
    """(entetes, lignes de corps, titre de sous-section) pour chaque tableau."""
    lignes = section.split("\n")
    titre = ""
    for indice, ligne in enumerate(lignes):
        if ligne.startswith("### "):
            titre = ligne
        suivante = lignes[indice + 1] if indice + 1 < len(lignes) else ""
        if not (ligne.startswith("|") and SEPARATEUR.match(suivante or "x")):
            continue
        corps = []
        for candidate in lignes[indice + 2:]:
            if not candidate.startswith("|"):
                break
            corps.append(candidate)
        yield cellules(ligne), corps, titre


def colonnes_de_cout(entetes):
    """Indices de la colonne nette, ou a defaut des colonnes de montant.

    Le net, jamais le brut : c'est le cout que le dossier retient, effets de
    retour deduits, et c'est celui que la fiche du chapitre additionne.
    """
    nets = [i for i, entete in enumerate(entetes) if "net" in entete.lower()]
    if nets:
        return nets
    return [
        i for i, entete in enumerate(entetes)
        if re.search(r"coût|montant|€\s*/\s*an", entete, re.I)
        and "brut" not in entete.lower()
    ]


def unite(contexte):
    """Md€ vaut 1, M€ vaut 0,001 ; None quand le texte ne tranche pas."""
    if "Md€" in contexte:
        return 1.0
    if "M€" in contexte:
        return 0.001
    return None


def unite_sans_ambiguite(section):
    """L'unite du § 4 entier, et seulement s'il n'en emploie qu'une.

    Dernier recours pour les tableaux dont ni l'en-tete ni le chapeau ne
    portent l'unite. Un § 4 qui melange Md€ et M€ ne tranche rien : mieux vaut
    renoncer a ses mesures que de les publier a un facteur mille pres.
    """
    if "Md€" in section and "M€" in section.replace("Md€", ""):
        return None
    return unite(section)


def _est_negatif(cellule, trouve):
    """Un tiret entre deux nombres separe une fourchette ; ailleurs il soustrait.

    « 0,012 – 0,020 » est une fourchette de deux montants positifs, quand
    « −12,1 à −14,7 » est un effet de retour. Les distinguer au caractere qui
    precede le tiret evite de lire la borne haute d'une fourchette comme une
    recette, ce qui ferait disparaitre la mesure.
    """
    if not trouve.group(1):
        return False
    avant = cellule[:trouve.start()].rstrip()
    return not (avant and avant[-1].isdigit())


def cout_de_cellule(cellule, unite_par_defaut):
    """Cout central de la cellule en Md€, ou None si ce n'est pas un cout."""
    if not cellule or cellule in {"—", "-", "–", "0"} or NON_COUT.search(cellule):
        return None
    trouves = list(NOMBRE.finditer(cellule))
    if not trouves:
        return None
    echelle = unite(cellule) or unite_par_defaut
    if echelle is None:
        return None
    bornes = []
    for trouve in trouves[:2]:
        valeur = float(re.sub(r"[\s ]", "", trouve.group(2)).replace(",", "."))
        bornes.append(-valeur if _est_negatif(cellule, trouve) else valeur)
    if any(borne <= 0 for borne in bornes):
        return None
    return sum(bornes) / len(bornes) * echelle


def nature_du_tableau(entetes_de_cout, titre, chapeau):
    """Recurrent ou ponctuel, en interrogeant du plus precis au plus large.

    L'ordre compte : le chapeau du § 4 du ch. 18 annonce « millions d'euros par
    an, sauf mention *investissement* (montant non recurrent) ». Lu en bloc, il
    fait passer tout le chapitre pour du ponctuel ; lu apres l'en-tete et le
    titre de sous-section, il ne sert que de defaut, et il dit « par an ».
    """
    for contexte in (entetes_de_cout, titre):
        if PONCTUEL.search(contexte):
            return "ponctuel"
        if RECURRENT.search(contexte):
            return "récurrent"
    if PONCTUEL.search(chapeau) and not RECURRENT.search(chapeau):
        return "ponctuel"
    return "récurrent"


def reference_unique(libelle):
    """La mesure nommee, ou None si la ligne en nomme zero ou plusieurs.

    Une ligne qui nomme deux mesures est une enveloppe : « M-8.10 a M-8.14 »
    porte un cout de groupe, dont la part de chaque mesure ne se deduit pas.
    """
    references = {"M-%s.%s" % trouve for trouve in REFERENCE.findall(libelle)}
    return references.pop() if len(references) == 1 else None
