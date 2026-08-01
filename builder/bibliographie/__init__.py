"""Appareil de sources du site : bibliographie de fiche et bibliographie generale.

Deux directives markdown y donnent acces :

    ::: sources 7
    :::

rend la bibliographie du chapitre 7 en pied de fiche, et

    ::: bibliographie
    :::

rend la page qui rassemble tout le dossier par organisme.

Les fichiers de `sources/` sont lus a la construction, jamais par le navigateur :
le site reste consultable en `file://`, sans requete ni dependance externe.
"""

from .liste import rendre_liste
from .page import rendre_bibliographie

__all__ = ["rendre_liste", "rendre_bibliographie"]
