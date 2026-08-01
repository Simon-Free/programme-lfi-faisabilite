"""Le cout retenu de chaque mesure, lu au § 4 « Chiffrage consolide » des analyses.

Pourquoi ne pas lire les colonnes de montants de l'audit de couverture : elles
portent les deux premiers montants rencontres dans le corps de la rubrique
« c. Chiffrage », recopies sur chaque mesure d'une sous-section groupee. Elles
ramassent donc une assiette, une masse salariale, une variante ecartee ou le
produit interieur brut aussi volontiers qu'un cout (transverse 33, § 2).

Le § 4 de chaque analyse est, lui, un tableau **par mesure** : cout brut, effets
de retour, cout net. C'est la colonne nette qui est lue ici, et elle seule.

Trois refus deliberes, parce qu'un montant faux coute plus cher qu'un blanc :
une ligne qui nomme plusieurs mesures (enveloppe non ventilable) ; une ligne
dont l'unite ne se lit ni dans la cellule, ni dans l'en-tete, ni dans le
chapeau ; une ligne negative ou marquee « recette » (une ressource n'est pas
un cout).

La lecture des cellules elles-memes vit dans `chiffrages_cellules`.
"""

from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

from .chiffrages_cellules import (
    cellules,
    colonnes_de_cout,
    cout_de_cellule,
    nature_du_tableau,
    reference_unique,
    tableaux,
    unite,
    unite_sans_ambiguite,
)

ANALYSES = Path(__file__).parents[3] / "analyses"
TITRE_SECTION = "## 4. Chiffrage consolidé"

# Lignes de synthese : elles totalisent des mesures, elles n'en sont pas une.
# « variante » n'est refuse qu'en tete de libelle : une ligne qui COMMENCE par
# la est un scenario ecarte (« variante perimetre B pour M-11.1 »), alors que
# « M-10.29 Garantie d'autonomie (variante B) » nomme l'option retenue.
AGREGAT = re.compile(r"total|agrégat|^dont\b|^lecture\b|^variante\b", re.I)


def _section(numero):
    """Le § 4 de l'analyse du chapitre, ou None."""
    fichier = ANALYSES / ("chapitre%02d_analyse.md" % numero)
    if not fichier.exists():
        return None
    texte = fichier.read_text(encoding="utf-8")
    debut = texte.find(TITRE_SECTION)
    if debut < 0:
        return None
    fin = texte.find("\n## ", debut + len(TITRE_SECTION))
    return texte[debut:fin if fin > 0 else len(texte)]


def _unite_du_tableau(entetes, indices, chapeau, repli):
    return (
        unite(" ".join(entetes[i] for i in indices))
        or unite(chapeau)
        or repli
    )


def _libelle(cellules_de_ligne, colonne_libelle):
    """Quand le tableau ouvre sur une colonne « # », c'est tantot elle qui
    porte la reference (ch. 15), tantot le libelle qui suit (ch. 14) : les
    deux sont alors lues ensemble."""
    if colonne_libelle:
        return " ".join(cellules_de_ligne[:2])
    return cellules_de_ligne[0]


def _lignes_chiffrees(section, chapeau):
    releves = [
        (entetes, corps, titre, colonnes_de_cout(entetes))
        for entetes, corps, titre in tableaux(section)
    ]
    # Un § 4 dont un seul tableau declare son unite la declare pour tous : le
    # ch. 18 n'ecrit « M€/an » que sur son tableau de synthese. La prose ne sert
    # qu'en dernier ressort, car elle cite des ordres de grandeur en Md€.
    entetes_de_cout = " ".join(
        entetes[i] for entetes, _, _, indices in releves for i in indices
    )
    repli = unite(entetes_de_cout) or unite_sans_ambiguite(section)

    for entetes, corps, titre, indices in releves:
        if not indices or not entetes:
            continue
        colonne_libelle = 1 if entetes[0].strip() in {"#", ""} else 0
        echelle = _unite_du_tableau(entetes, indices, chapeau, repli)
        nature = nature_du_tableau(
            " ".join(entetes[i] for i in indices), titre, chapeau
        )
        for ligne in corps:
            valeurs = cellules(ligne)
            if len(valeurs) <= max(indices + [colonne_libelle]):
                continue
            libelle = _libelle(valeurs, colonne_libelle)
            if AGREGAT.search(libelle):
                continue
            reference = reference_unique(libelle)
            if reference is None:
                continue
            couts = [cout_de_cellule(valeurs[i], echelle) for i in indices]
            couts = [valeur for valeur in couts if valeur is not None]
            if couts:
                yield reference, sum(couts) / len(couts), nature


def _resolue(par_nature):
    """Un cout par mesure, ou None quand le § 4 en publie plusieurs.

    Deux lignes de natures differentes se completent — un investissement une
    fois, une charge chaque annee — et la recurrente prime, c'est elle que la
    figure compare au total du chapitre. Deux lignes de MEME nature portant des
    valeurs differentes ne se departagent pas : la mesure passe alors en « sans
    cout propre publie » plutot que d'en choisir une au hasard.
    """
    for nature in ("récurrent", "ponctuel"):
        montants = set(par_nature.get(nature, []))
        if len(montants) == 1:
            return {"montant": montants.pop(), "nature": nature}
    return None


def couts_retenus():
    """{« M-8.23 »: {"montant": 10.0, "nature": "récurrent"}} pour les mesures
    dont le § 4 d'une analyse publie un cout net propre et non ambigu."""
    releves = defaultdict(lambda: defaultdict(list))
    for numero in range(1, 19):
        section = _section(numero)
        if section is None:
            continue
        chapeau = section[:section.find("|") if "|" in section else len(section)]
        for reference, montant, nature in _lignes_chiffrees(section, chapeau):
            releves[reference][nature].append(round(montant, 6))

    couts = {}
    for reference, par_nature in releves.items():
        resolue = _resolue(par_nature)
        if resolue is not None:
            couts[reference] = resolue
    return couts
