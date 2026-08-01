"""Lecture des chiffrages mesure par mesure, depuis l'audit de couverture.

L'audit (`transverses/17_audit_couverture.md`) porte un tableau de 830 lignes
dont deux colonnes donnent le cout ponctuel et le cout recurrent tels que la
rubrique « c. Chiffrage » de chaque analyse les publie.

Piege documente : une cellule melange parfois une grandeur de contexte et le
cout propre de la mesure — « 160 Md€/an ; 3 a 6 Md€/an », ou 160 est la
depense existante du secteur. Le cout suit le contexte, d'ou la regle du
dernier groupe. Un plafond de vraisemblance ecarte ce qui subsiste.
"""

from __future__ import annotations

import re
from pathlib import Path

AUDIT = Path(__file__).parents[3] / "transverses" / "17_audit_couverture.md"

LIGNE = re.compile(r"^\|\s*\d+\s*\|")
NOMBRE = r"(\d[\d   ]*(?:[.,]\d+)?)"
CHAPITRE = re.compile(r"^M-(\d+)\.")

# Aucune mesure isolee ne pese plus que le total d'un chapitre : au-dela,
# la cellule porte un agregat ou un objectif, pas un cout.
PLAFOND = 60.0


def _valeur(cellule, flux):
    """Cout propre de la mesure, en Md€. `flux` exige le suffixe « /an »."""
    texte = cellule.replace(" ", " ").replace(" ", " ")
    dernier = texte.split(";")[-1]
    suffixe = r"\s*/\s*an" if flux else ""
    valeurs = []
    for trouve in re.finditer(NOMBRE + r"\s*(Md€|M€)" + suffixe, dernier):
        brut = float(trouve.group(1).replace(" ", "").replace(",", "."))
        valeurs.append(brut if trouve.group(2) == "Md€" else brut / 1000)
    return max(valeurs) if valeurs else None


def _chapitre(reference):
    trouve = CHAPITRE.match(reference)
    return int(trouve.group(1)) if trouve else None


def mesures_chiffrees():
    """Renvoie (retenues, ecartees, muettes).

    Une mesure retenue porte : chapitre, reference, intitule, montant en
    Md€/an, et la nature du cout.
    """
    if not AUDIT.exists():
        return [], [], 0

    retenues, ecartees, muettes = [], [], 0
    for ligne in AUDIT.read_text(encoding="utf-8").split("\n"):
        if not LIGNE.match(ligne):
            continue
        cellules = [part.strip() for part in ligne.split("|")[1:-1]]
        if len(cellules) < 7:
            continue
        intitule, reference, ponctuel, recurrent = (
            cellules[1], cellules[2], cellules[4], cellules[5]
        )
        chapitre = _chapitre(reference)
        if chapitre is None:
            continue

        montant = _valeur(recurrent, flux=True)
        nature = "récurrent"
        if montant is None:
            montant = _valeur(ponctuel, flux=False)
            nature = "ponctuel"
        if montant is None:
            muettes += 1
            continue

        entree = {
            "chapitre": chapitre,
            "reference": reference,
            "intitule": intitule.rstrip("…").strip(),
            "montant": montant,
            "nature": nature,
        }
        (ecartees if montant > PLAFOND else retenues).append(entree)

    retenues.sort(key=lambda e: (e["chapitre"], -e["montant"]))
    return retenues, ecartees, muettes
