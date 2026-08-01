"""Lecture des recoltes de sources, tolerante aux fichiers absents ou partiels.

Les fichiers de `sources/` sont ecrits par des agents recolteurs pendant que le
site se construit. Un fichier peut donc etre absent, tronque en plein milieu
d'une accolade, ou verrouille par le processus qui l'ecrit. Aucun de ces cas ne
doit interrompre la construction : le module renvoie alors une recolte vide en
etat degrade, que le rendu affiche honnetement.
"""

import json
import re
from pathlib import Path

RACINE = Path(__file__).resolve().parents[3]
DOSSIER_SOURCES = RACINE / "sources"
MANIFESTE = RACINE / "site" / "manifest.json"


class Recolte:
    """Les sources d'une fiche, avec l'etat de la recolte au moment du build."""

    def __init__(self, clef, entrees, etat):
        self.clef = clef
        self.entrees = entrees
        self.etat = etat  # « ok », « absente » ou « partielle »

    def __len__(self):
        return len(self.entrees)


CLEF_VALIDE = re.compile(r"^[a-z0-9_-]+$")


def clef_normalisee(appel):
    """« 7 », « 07 » et « ch07 » designent le meme fichier de recolte.

    Une clef inattendue est rejetee plutot que transformee en chemin : elle ne
    doit jamais pouvoir designer un fichier hors du dossier de recolte.
    """
    clef = (appel or "").strip().lower()
    if clef.isdigit():
        return "ch%02d" % int(clef)
    return clef if CLEF_VALIDE.match(clef) else ""


def _lire_entrees(chemin):
    """Retourne (entrees, etat). Un fichier en cours d'ecriture rend ([], partielle)."""
    try:
        texte = chemin.read_text(encoding="utf-8")
        donnees = json.loads(texte)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        # Le recolteur ecrit dans ce fichier a l'instant meme : on l'annonce
        # au lecteur plutot que de casser la construction du site.
        return [], "partielle"
    if not isinstance(donnees, dict):
        return [], "partielle"
    entrees = donnees.get("sources")
    if not isinstance(entrees, list):
        return [], "partielle"
    valides = [entree for entree in entrees if isinstance(entree, dict)]
    return valides, "ok"


def charger(appel):
    """Recolte d'une seule fiche, designee par son numero ou son nom de fichier."""
    clef = clef_normalisee(appel)
    if not clef:
        return Recolte(clef, [], "absente")
    chemin = DOSSIER_SOURCES / ("%s.json" % clef)
    if not chemin.is_file():
        return Recolte(clef, [], "absente")
    entrees, etat = _lire_entrees(chemin)
    return Recolte(clef, entrees, etat)


def charger_tout():
    """Toutes les recoltes presentes sur le disque, dans l'ordre des fichiers."""
    if not DOSSIER_SOURCES.is_dir():
        return []
    recoltes = []
    for chemin in sorted(DOSSIER_SOURCES.glob("*.json")):
        entrees, etat = _lire_entrees(chemin)
        recoltes.append(Recolte(chemin.stem, entrees, etat))
    return recoltes


def fiches_du_manifeste():
    """Clef de recolte -> (titre lisible, url relative depuis une page de rubrique).

    La clef d'une recolte est exactement le nom du markdown qui la porte :
    `ch07.json` accompagne `ch07.md`, `obstacle_europe.json` accompagne
    `obstacle_europe.md`. Le manifeste fournit donc le titre et l'adresse.
    """
    if not MANIFESTE.is_file():
        return {}
    donnees = json.loads(MANIFESTE.read_text(encoding="utf-8"))
    return {
        Path(fiche["source"]).stem: (
            fiche["titre"],
            "../%s/%s.html" % (fiche["rubrique"], fiche["slug"]),
        )
        for fiche in donnees.get("fiches", [])
    }
