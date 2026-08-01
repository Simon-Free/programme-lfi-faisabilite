"""La page bibliographie du site, rendue par la directive `::: bibliographie`.

Toutes les sources du dossier, groupees par organisme, chaque organisme
presente une fois, et le decompte honnete de ce qui est verifie et de ce qui ne
l'est pas.
"""

from ..markdown import escape_attribute, escape_html, slugify
from .entree import (
    ancre_de,
    classe_de,
    rendre_acces,
    rendre_reperage,
    rendre_titre,
    url_utilisable,
)
from .regroupement import rassembler

VIDE = (
    '<div class="callout callout--methode"><p class="callout__title">'
    "Bibliographie en cours de constitution</p><p>Les références du dossier sont "
    "vérifiées une par une, en ouvrant chaque document. Cette page se remplit "
    "d’elle-même à chaque construction du site.</p></div>"
)


def _compte_global(entrees, organismes, partielles):
    total = len(entrees)
    verifiees = sum(
        1
        for entree in entrees
        if url_utilisable(entree.get("url")) and entree.get("url_verifiee")
    )
    sans_lien = sum(1 for entree in entrees if not url_utilisable(entree.get("url")))
    faibles = sum(1 for entree in entrees if entree.get("solidite") == "faible")
    lignes = [
        "<strong>%d</strong> références au total, réparties entre "
        "<strong>%d</strong> organismes." % (total, len(organismes)),
        "<strong>%d</strong> portent un lien qui a été ouvert et vérifié." % verifiees,
        "<strong>%d</strong> n’ont pas été retrouvées en ligne : elles sont citées "
        "par leur référence exacte, sans lien mort." % sans_lien,
        "<strong>%d</strong> sont signalées de solidité faible." % faibles,
    ]
    if partielles:
        lignes.append(
            "La collecte de %d fiche(s) était en cours d’écriture à la "
            "construction de cette page : %s."
            % (len(partielles), escape_html(", ".join(partielles)))
        )
    return '<ul class="biblio-compte">%s</ul>' % "".join(
        "<li>%s</li>" % ligne for ligne in lignes
    )


def _sommaire(organismes):
    items = "".join(
        '<li><a href="#%s">%s</a> <span>%d</span></li>'
        % (
            slugify(organisme.nom, "organisme"),
            escape_html(organisme.nom),
            len(organisme.documents),
        )
        for organisme in organismes
    )
    return (
        '<nav class="biblio-sommaire" aria-label="Les organismes cités">'
        "<ol>%s</ol></nav>" % items
    )


def _usages(document):
    liens = []
    for libelle, adresse in document.usages:
        if adresse:
            liens.append(
                '<a href="%s">%s</a>'
                % (escape_attribute(adresse), escape_html(libelle))
            )
        else:
            liens.append(escape_html(libelle))
    if not liens:
        return ""
    return '<p class="source__usages">Sert dans : %s</p>' % ", ".join(liens)


def _document(document, prefixe):
    entree = document.entree
    tire = escape_html((entree.get("ce_qu_on_en_tire") or "").strip())
    morceaux = [
        rendre_titre(entree),
        '<p class="source__tire">%s</p>' % tire if tire else "",
        rendre_reperage(entree),
        _usages(document),
        rendre_acces(entree),
    ]
    return '<li class="%s" id="%s">%s</li>' % (
        classe_de(entree),
        ancre_de(entree, prefixe),
        "".join(morceaux),
    )


def _organisme(organisme):
    ancre = slugify(organisme.nom, "organisme")
    explication = escape_html(organisme.explication)
    documents = "".join(
        _document(document, ancre) for document in organisme.documents_tries
    )
    return (
        '<section class="biblio-organisme">'
        '<h3 id="%s">%s</h3>%s<ol class="sources-liste">%s</ol></section>'
        % (
            ancre,
            escape_html(organisme.nom),
            '<p class="biblio-organisme__explique">%s</p>' % explication
            if explication
            else "",
            documents,
        )
    )


def rendre_bibliographie():
    """`::: bibliographie` — toutes les sources du dossier, par organisme."""
    organismes, entrees, partielles = rassembler()
    if not organismes:
        return VIDE
    return '<div class="biblio">%s%s%s</div>' % (
        _compte_global(entrees, organismes, partielles),
        _sommaire(organismes),
        "".join(_organisme(organisme) for organisme in organismes),
    )
