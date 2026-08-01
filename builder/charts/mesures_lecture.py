"""Les mesures du programme, et le cout de celles qui en ont un de verifie.

Deux sources, et deux roles qu'il ne faut pas melanger.

L'audit de couverture (`transverses/17_audit_couverture.md`) dit **quelles
mesures existent** : 830 lignes, une par mesure, avec son intitule et son
chapitre. C'est l'inventaire, et il fait autorite pour cela.

Le § 4 « Chiffrage consolide » de chaque analyse dit **ce que chaque mesure
coute** : un tableau par mesure, avec cout brut, effets de retour et cout net.
C'est la seule source de couts de cette figure.

Ce que l'audit ne fournit plus, et pourquoi : ses colonnes `Ponctuel` et
`Recurrent` portent les deux premiers montants rencontres dans le corps de la
rubrique « c. Chiffrage », recopies sur chaque mesure d'une sous-section
groupee. Elles ramassent donc une assiette, une masse salariale, une variante
ecartee ou le produit interieur brut aussi volontiers qu'un cout — la
transverse 33 l'etablit sur cinq cas verifies ligne a ligne. Elles servent ici
au seul usage qu'elles supportent : distinguer une mesure que le dossier laisse
sans aucun montant d'une mesure chiffree ailleurs mais pas au § 4.
"""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

from .chiffrages_analyses import couts_retenus

AUDIT = Path(__file__).parents[3] / "transverses" / "17_audit_couverture.md"

LIGNE = re.compile(r"^\|\s*\d+\s*\|")
CHAPITRE = re.compile(r"^M-(\d+)\.")
MONTANT = re.compile(r"\d[\d   ]*(?:[.,]\d+)?\s*(?:Md€|M€|€)")


def _chapitre(reference):
    trouve = CHAPITRE.match(reference)
    return int(trouve.group(1)) if trouve else None


def _inventaire():
    """(chapitre, reference, intitule, l'audit porte-t-il un montant) par mesure."""
    if not AUDIT.exists():
        return []
    mesures = []
    for ligne in AUDIT.read_text(encoding="utf-8").split("\n"):
        if not LIGNE.match(ligne):
            continue
        cellules = [part.strip() for part in ligne.split("|")[1:-1]]
        if len(cellules) < 7:
            continue
        intitule, reference = cellules[1], cellules[2]
        chapitre = _chapitre(reference)
        if chapitre is None:
            continue
        mesures.append({
            "chapitre": chapitre,
            "reference": reference,
            # L'audit ecrit ses intitules en markdown : les etoiles d'emphase
            # n'ont aucun sens dans une infobulle ni dans une gouttiere SVG.
            "intitule": intitule.replace("**", "").rstrip("…").strip(),
            "montant": None,
            "nature": None,
            "audit_chiffre": bool(
                MONTANT.search(cellules[4]) or MONTANT.search(cellules[5])
            ),
        })
    return mesures


def mesures_chiffrees():
    """Renvoie (retenues, non_confirmees, muettes).

    Une **retenue** porte un cout net publie mesure par mesure au § 4 d'une
    analyse : c'est le cout de la mesure, et la figure peut le placer sur une
    echelle. Une **non confirmee** est chiffree quelque part dans le dossier,
    mais son cout propre n'est pas isolable — le § 4 la traite dans une
    enveloppe qui en couvre plusieurs, ou lui donne deux valeurs qui ne se
    departagent pas. Une **muette** ne porte aucun montant nulle part.

    Les deux dernieres sont rendues une par une, et non comptees, pour qu'une
    figure de chapitre puisse nommer ce qu'elle n'affiche pas.
    """
    couts = couts_retenus()
    inventaire = _inventaire()
    # L'audit porte parfois plusieurs mesures sous une meme reference — deux
    # lignes « M-1.8 », quatre lignes « M-8.5 a M-8.9 ». Recopier sur chacune
    # le cout que le § 4 attribue a une seule refabriquerait, a l'identique, le
    # defaut que cette figure corrige : un cout unique duplique sur un groupe.
    lignes_par_reference = Counter(mesure["reference"] for mesure in inventaire)

    retenues, non_confirmees, muettes = [], [], []
    for mesure in inventaire:
        chiffre = mesure.pop("audit_chiffre")
        cout = couts.get(mesure["reference"])
        if lignes_par_reference[mesure["reference"]] > 1:
            cout = None
        if cout is not None:
            mesure["montant"] = cout["montant"]
            mesure["nature"] = cout["nature"]
            retenues.append(mesure)
        elif chiffre:
            non_confirmees.append(mesure)
        else:
            muettes.append(mesure)

    retenues.sort(key=lambda entree: (entree["chapitre"], -entree["montant"]))
    return retenues, non_confirmees, muettes
