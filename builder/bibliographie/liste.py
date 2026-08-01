"""La bibliographie d'une seule fiche, rendue par la directive `::: sources`.

Une recolte absente ou en cours d'ecriture ne fait pas echouer la construction :
elle produit un encadre qui dit ou en est le travail.
"""

from ..markdown import escape_html
from .entree import rendre_entree, url_utilisable
from .lecture import charger

ATTENTE = (
    '<div class="callout callout--methode"><p class="callout__title">'
    "Sources en cours de collecte</p><p>%s</p></div>"
)

MESSAGES = {
    "absente": "Les références de cette fiche sont en cours de vérification, une "
    "par une, en ouvrant chaque document. Elles paraîtront ici dès que cette "
    "vérification sera terminée.",
    "partielle": "La collecte des références de cette fiche était en cours "
    "d’écriture au moment où cette page a été produite. Elle paraîtra "
    "entièrement à la prochaine construction du site.",
    "vide": "Aucune référence n’a encore été versée au dossier de cette fiche.",
}


def decompte(entrees):
    """Le compte honnete : combien de sources, combien verifiees, combien sans lien."""
    total = len(entrees)
    verifiees = sum(
        1
        for entree in entrees
        if url_utilisable(entree.get("url")) and entree.get("url_verifiee")
    )
    sans_lien = sum(1 for entree in entrees if not url_utilisable(entree.get("url")))
    return total, verifiees, sans_lien


def phrase_de_decompte(entrees):
    """Le compte, dit au lecteur en toutes lettres."""
    total, verifiees, sans_lien = decompte(entrees)
    phrase = "%d source%s. %d port%s un lien vérifié en l’ouvrant" % (
        total,
        "s" if total > 1 else "",
        verifiees,
        "ent" if verifiees > 1 else "e",
    )
    if sans_lien:
        phrase += ", %d n’%s pas été retrouvée%s en ligne" % (
            sans_lien,
            "ont" if sans_lien > 1 else "a",
            "s" if sans_lien > 1 else "",
        )
    return escape_html(phrase + ".")


def _entrees_rendues(recolte):
    """Rend les entrees, l'explication d'un organisme n'etant ecrite qu'une fois."""
    organismes_presentes = set()
    rendues = []
    for entree in recolte.entrees:
        organisme = (entree.get("organisme") or "").strip()
        premiere_fois = organisme not in organismes_presentes
        organismes_presentes.add(organisme)
        rendues.append(rendre_entree(entree, recolte.clef, premiere_fois))
    return "".join(rendues)


def rendre_liste(appel):
    """`::: sources ch07` — la bibliographie de la fiche, ou son etat d'avancement."""
    recolte = charger(appel)
    if recolte.etat != "ok":
        return ATTENTE % MESSAGES[recolte.etat]
    if not recolte.entrees:
        return ATTENTE % MESSAGES["vide"]
    return (
        '<div class="sources-fiche">'
        '<p class="sources-fiche__compte">%s</p>'
        '<ol class="sources-liste">%s</ol></div>'
        % (phrase_de_decompte(recolte.entrees), _entrees_rendues(recolte))
    )
