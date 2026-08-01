"""Rendu d'une source, dans l'ordre de lecture utile au lecteur.

D'abord ce qu'on en tire — la seule ligne qui interesse quelqu'un qui lit la
fiche —, ensuite l'organisme et ce qu'il est, le titre exact, l'endroit ou
regarder dans le document, et enfin l'acces.

Les trois etats — lien verifie, reference sans lien, solidite faible — sont
toujours ecrits en toutes lettres : la couleur seule ne porte jamais
l'information.
"""

from urllib.parse import urlsplit

from ..markdown import escape_attribute, escape_html, slugify

SCHEMAS_AUTORISES = ("https://", "http://")

ETIQUETTES = {
    "verifie": ("source__etat--verifie", "Lien vérifié"),
    "non-verifie": ("source__etat--non-verifie", "Lien non vérifié"),
    "sans-lien": ("source__etat--sans-lien", "Référence non retrouvée en ligne"),
    "faible": ("source__etat--faible", "Solidité faible"),
}


def url_utilisable(valeur):
    """Une URL n'est retenue que si elle est http(s) et d'un seul tenant."""
    if not isinstance(valeur, str):
        return ""
    url = valeur.strip()
    if not url or any(blanc in url for blanc in (" ", "\t", "\n", "\r")):
        return ""
    if not url.lower().startswith(SCHEMAS_AUTORISES):
        return ""
    return url


def _etat(cle):
    classe, libelle = ETIQUETTES[cle]
    return '<span class="source__etat %s">%s</span>' % (classe, libelle)


def _domaine(url):
    hote = urlsplit(url).hostname or ""
    return hote[4:] if hote.startswith("www.") else hote


def rendre_acces(entree):
    """Le lien s'il est utilisable, et l'etat de la reference en toutes lettres."""
    url = url_utilisable(entree.get("url"))
    marques = []
    if url:
        verifie = "verifie" if entree.get("url_verifiee") else "non-verifie"
        marques.append(_etat(verifie))
        marques.append(
            '<a class="source__lien" href="%s" target="_blank" rel="noopener">'
            "Ouvrir le document%s</a>"
            % (
                escape_attribute(url),
                " sur %s" % escape_html(_domaine(url)) if _domaine(url) else "",
            )
        )
    else:
        marques.append(_etat("sans-lien"))
    if entree.get("solidite") == "faible":
        marques.append(_etat("faible"))
    return '<p class="source__acces">%s</p>' % "".join(marques)


def ancre_de(entree, prefixe):
    """Ancre stable d'une entree, prefixee pour rester unique sur une page."""
    brut = "%s-%s" % (prefixe, entree.get("id") or entree.get("titre") or "")
    return slugify(brut, "source")


def classe_de(entree):
    """La solidite faible se lit aussi sur la mise en forme du bloc."""
    if entree.get("solidite") == "faible":
        return "source source--faible"
    return "source"


def rendre_titre(entree):
    titre = escape_html((entree.get("titre") or "").strip())
    reference = escape_html((entree.get("reference") or "").strip())
    annee = str(entree.get("annee") or "")
    # La reference porte souvent deja la date : ne pas l'ecrire deux fois.
    if annee and annee in reference:
        annee = ""
    details = [part for part in (reference, annee) if part]
    if not titre and not details:
        return ""
    corps = "<em>%s</em>" % titre if titre else "<em>Document sans titre</em>"
    if details:
        corps += " — %s" % ", ".join(details)
    return '<p class="source__titre">%s</p>' % corps


def rendre_reperage(entree):
    localisation = escape_html((entree.get("localisation") or "").strip())
    if not localisation:
        return ""
    return '<p class="source__reperage">Où regarder : %s</p>' % localisation


def rendre_entree(entree, prefixe_ancre, avec_explication):
    """Une entree de bibliographie, en liste.

    `avec_explication` porte la presentation de l'organisme : elle n'est ecrite
    qu'a sa premiere apparition dans la liste, pour ne pas repeter deux cents
    caracteres identiques quatre fois de suite.
    """
    organisme = escape_html((entree.get("organisme") or "Organisme non précisé").strip())
    tire = escape_html((entree.get("ce_qu_on_en_tire") or "").strip())
    explique = escape_html((entree.get("organisme_explique") or "").strip())
    morceaux = [
        '<p class="source__tire">%s</p>' % tire if tire else "",
        '<p class="source__provenance">%s</p>' % organisme,
        '<p class="source__explique">%s</p>' % explique
        if explique and avec_explication
        else "",
        rendre_titre(entree),
        rendre_reperage(entree),
        rendre_acces(entree),
    ]
    return '<li class="%s" id="%s">%s</li>' % (
        classe_de(entree),
        ancre_de(entree, prefixe_ancre),
        "".join(morceaux),
    )
