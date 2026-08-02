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
    """Le compte honnete, en distinguant la lecture de la simple resolution.

    « Verifiee » veut dire que quelqu'un a ouvert le document et constate qu'il
    porte bien ce qu'on lui attribue. « Resout » veut seulement dire que
    l'adresse repond et sert un document : c'est une machine qui l'a constate,
    sans rien lire. Les deux comptes ne se melangent pas.
    """
    avec_lien = [entree for entree in entrees if url_utilisable(entree.get("url"))]
    non_lues = [entree for entree in avec_lien if not entree.get("url_verifiee")]
    compte = {
        "total": len(entrees),
        "verifiees": len(avec_lien) - len(non_lues),
        "resolus": sum(
            1 for entree in non_lues
            if entree.get("lien_resout") in (True, "redirige")
        ),
        "refuses": sum(
            1 for entree in non_lues if entree.get("lien_resout") == "refuse"
        ),
        "morts": sum(1 for entree in non_lues if entree.get("lien_resout") is False),
        "sans_lien": len(entrees) - len(avec_lien),
    }
    compte["jamais"] = len(non_lues) - (
        compte["resolus"] + compte["refuses"] + compte["morts"]
    )
    return compte


def phrase_de_decompte(entrees):
    """Le compte, dit au lecteur en toutes lettres."""
    compte = decompte(entrees)
    total, verifiees = compte["total"], compte["verifiees"]
    resolus, sans_lien = compte["resolus"], compte["sans_lien"]
    phrase = "%d source%s. %d port%s un lien vérifié en l’ouvrant" % (
        total,
        "s" if total > 1 else "",
        verifiees,
        "ent" if verifiees > 1 else "e",
    )
    if resolus:
        phrase += ", %d un lien qui répond sans que le document ait été relu" % resolus
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
