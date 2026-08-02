"""La page bibliographie du site, rendue par la directive `::: bibliographie`.

Toutes les sources du dossier, groupees par organisme, chaque organisme
presente une fois, et le decompte honnete de ce qui est verifie et de ce qui ne
l'est pas.
"""

from ..markdown import escape_attribute, escape_html, slugify
from .entree import ancre_de, classe_de, rendre_acces, rendre_reperage, rendre_titre
from .liste import decompte
from .regroupement import rassembler

VIDE = (
    '<div class="callout callout--methode"><p class="callout__title">'
    "Bibliographie en cours de constitution</p><p>Les références du dossier sont "
    "vérifiées une par une, en ouvrant chaque document. Cette page se remplit "
    "d’elle-même à chaque construction du site.</p></div>"
)


ENTETE = (
    "<strong>%d</strong> références au total, réparties entre "
    "<strong>%d</strong> organismes."
)

GABARITS = [
    ("verifiees", "<strong>%d</strong> portent un lien qui a été ouvert et "
     "vérifié : le document s’y trouve, et il porte bien ce qu’on lui attribue."),
    ("resolus", "<strong>%d</strong> portent un lien qui répond et sert un "
     "document, sans que ce document ait été relu. C’est une machine qui a "
     "ouvert l’adresse ; elle n’a pas regardé ce qu’elle recevait."),
    ("refuses", "<strong>%d</strong> pointent vers un site qui refuse tout "
     "client automatisé : la page s’ouvre dans un navigateur, elle n’a pas pu "
     "être contrôlée autrement."),
    ("morts", "<strong>%d</strong> pointent vers une adresse qui ne sert plus "
     "rien, sans qu’une adresse de remplacement ait été trouvée."),
    ("jamais", "<strong>%d</strong> portent un lien qui n’a encore été ouvert "
     "par personne."),
    ("sans_lien", "<strong>%d</strong> n’ont pas été retrouvées en ligne : elles "
     "sont citées par leur référence exacte, sans lien mort."),
]


def _compte_global(entrees, organismes, partielles):
    """Le decompte par etat. Une ligne dont le compte est nul n'est pas ecrite."""
    compte = decompte(entrees)
    faibles = sum(1 for entree in entrees if entree.get("solidite") == "faible")
    lignes = [ENTETE % (compte["total"], len(organismes))]
    lignes += [gabarit % compte[cle] for cle, gabarit in GABARITS if compte[cle]]
    lignes.append(
        "<strong>%d</strong> sont signalées de solidité faible." % faibles
    )
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
