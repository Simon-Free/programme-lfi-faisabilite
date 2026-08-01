"""Gabarit HTML commun a toutes les pages du site."""

from ..markdown import escape_attribute, escape_html

# Applique le theme memorise avant le premier rendu, pour eviter un clignotement.
THEME_BOOTSTRAP = (
    "(function(){try{var t=localStorage.getItem('aec-theme');"
    "if(t==='dark'||t==='light')"
    "document.documentElement.setAttribute('data-theme',t);}catch(e){}})();"
)

DOCUMENT = """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="stylesheet" href="{base}assets/style.css">
<link rel="stylesheet" href="{base}assets/components.css">
<link rel="stylesheet" href="{base}assets/content.css">
<link rel="stylesheet" href="{base}assets/charts.css">
<script>{bootstrap}</script>
</head>
<body>
<a class="skip-link" href="#contenu">Aller au contenu</a>
{header}
<div class="layout">
{breadcrumb}
</div>
<main id="contenu">
{body}
</main>
{footer}
{scripts}
<script src="{base}assets/app.js"></script>
<script src="{base}assets/charts.js"></script>
</body>
</html>
"""


def _nav(rubriques, base, active):
    links = []
    for rubrique in rubriques:
        current = ' aria-current="page"' if rubrique["slug"] == active else ""
        # Le chemin de l'index est explicite : en file:// un dossier nu
        # affiche la liste des fichiers au lieu de la page.
        links.append(
            '<li><a href="%s%s/index.html"%s>%s</a></li>'
            % (base, rubrique["slug"], current, escape_html(rubrique["titre"]))
        )
    search_current = ' aria-current="page"' if active == "recherche" else ""
    links.append(
        '<li><a href="%srecherche.html"%s>Recherche</a></li>'
        % (base, search_current)
    )
    return (
        '<nav class="site-nav" aria-label="Rubriques"><ul>%s</ul></nav>'
        % "".join(links)
    )


def _header(site, rubriques, base, active):
    return (
        '<header class="site-header"><div class="site-header__bar">'
        '<a class="site-header__brand" href="%sindex.html">%s<span>%s</span></a>'
        "%s"
        '<button type="button" class="theme-toggle" data-theme-toggle'
        ' aria-label="Changer de thème">Thème sombre</button>'
        "</div></header>"
        % (
            base,
            escape_html(site["titre"]),
            escape_html(site["sous_titre"]),
            _nav(rubriques, base, active),
        )
    )


def _breadcrumb(trail):
    """trail : liste de couples (libelle, url ou None pour la page courante)."""
    if not trail:
        return ""
    items = []
    for label, url in trail:
        if url:
            items.append('<li><a href="%s">%s</a></li>' % (url, escape_html(label)))
        else:
            items.append(
                '<li><span aria-current="page">%s</span></li>' % escape_html(label)
            )
    return (
        '<nav class="breadcrumb" aria-label="Fil d\'Ariane"><ol>%s</ol></nav>'
        % "".join(items)
    )


def _footer(site, base):
    return (
        '<footer class="site-footer"><div>'
        "<p>%s — expertise de faisabilité, version du %s. "
        'Chiffres et sources : voir <a href="%ssources/index.html">Sources et '
        "méthode</a>.</p>"
        "<p>Site statique, sans suivi ni dépendance externe.</p>"
        "</div></footer>"
        % (escape_html(site["titre"]), escape_html(site["date"]), base)
    )


def render_page(site, rubriques, **page):
    """Assemble une page complete.

    Cles attendues : title, description, body, base, active, trail,
    et optionnellement scripts.
    """
    base = page.get("base", "")
    return DOCUMENT.format(
        title=escape_html(page["title"]),
        description=escape_attribute(page.get("description", "")),
        base=base,
        bootstrap=THEME_BOOTSTRAP,
        header=_header(site, rubriques, base, page.get("active", "")),
        breadcrumb=_breadcrumb(page.get("trail", [])),
        body=page["body"],
        footer=_footer(site, base),
        scripts=page.get("scripts", ""),
    )
