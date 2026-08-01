"""Construction des pages de fiche et des pages de rubrique."""

from ..markdown import escape_html, render_markdown
from .template import render_page

ABSENT = (
    '<div class="callout callout--methode">'
    '<p class="callout__title">Fiche à venir</p>'
    "<p>Le texte de cette fiche n'est pas encore rédigé. Le fichier attendu est "
    "<code>%s</code> dans le dossier <code>vulgarise/</code>. La page se remplira "
    "d'elle-même à la prochaine exécution du générateur.</p></div>"
)

LOREM_WARNING = (
    '<div class="callout callout--attention">'
    '<p class="callout__title">Contenu de démonstration</p>'
    "<p>Cette fiche contient du texte factice servant à valider la chaîne de "
    "publication. <span class=\"lorem-flag\">Elle ne doit pas être lue comme un "
    "résultat d'expertise.</span></p></div>"
)


def fiche_url(fiche):
    return "%s/%s.html" % (fiche["rubrique"], fiche["slug"])


def _toc(sections):
    if len(sections) < 2:
        return ""
    items = "".join(
        '<li><a href="#%s">%s</a></li>' % (anchor, label)
        for anchor, label in sections
    )
    return (
        '<nav class="toc" aria-labelledby="titre-sommaire">'
        '<p class="toc__title" id="titre-sommaire">Sur cette page</p>'
        "<ol>%s</ol></nav>" % items
    )


def _pager(previous, following):
    if not previous and not following:
        return ""
    cells = []
    if previous:
        cells.append(
            '<a class="pager__prev" href="../%s" rel="prev">'
            "<small>Fiche précédente</small>%s</a>"
            % (fiche_url(previous), escape_html(previous["titre"]))
        )
    else:
        cells.append("<span></span>")
    if following:
        cells.append(
            '<a class="pager__next" href="../%s" rel="next">'
            "<small>Fiche suivante</small>%s</a>"
            % (fiche_url(following), escape_html(following["titre"]))
        )
    return '<nav class="pager" aria-label="Navigation entre fiches">%s</nav>' % "".join(
        cells
    )


def _read_source(source_dir, fiche):
    path = source_dir / fiche["source"]
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def render_fiche(site, rubriques, rubrique, fiche, source_dir, neighbours):
    """Page d'une fiche. Retourne (chemin relatif, html)."""
    raw = _read_source(source_dir, fiche)
    if raw is None:
        body_html, sections = ABSENT % escape_html(fiche["source"]), []
    else:
        document = render_markdown(raw)
        body_html, sections = document.html, document.sections
        if "LOREM" in raw:
            body_html = LOREM_WARNING + body_html

    previous, following = neighbours
    head = (
        '<div class="page-head">'
        '<p class="page-head__kicker">%s</p><h1>%s</h1>'
        '<p class="page-head__lede">%s</p></div>'
        % (
            escape_html(rubrique["titre"]),
            escape_html(fiche["titre"]),
            escape_html(fiche["resume"]),
        )
    )
    article = '<article class="prose">%s%s%s</article>' % (
        head,
        body_html,
        _pager(previous, following),
    )
    body = '<div class="layout layout--with-toc">%s%s</div>' % (
        article,
        _toc(sections),
    )
    html = render_page(
        site,
        rubriques,
        title="%s — %s" % (fiche["titre"], site["titre"]),
        description=fiche["resume"],
        base="../",
        active=rubrique["slug"],
        trail=[
            ("Accueil", "../index.html"),
            (rubrique["titre"], "../%s/index.html" % rubrique["slug"]),
            (fiche["titre"], None),
        ],
        body=body,
    )
    return fiche_url(fiche), html


def _card(fiche, published):
    state = "" if published else '<p class="empty-note">Fiche à venir.</p>'
    return (
        '<li><a class="card" href="%s.html">'
        '<h3>%s</h3><p>%s</p>%s</a></li>'
        % (
            fiche["slug"],
            escape_html(fiche["titre"]),
            escape_html(fiche["resume"]),
            state,
        )
    )


def render_rubrique(site, rubriques, rubrique, fiches, source_dir):
    """Page d'index d'une rubrique. Retourne (chemin relatif, html)."""
    cards = "".join(
        _card(fiche, (source_dir / fiche["source"]).exists()) for fiche in fiches
    )
    grid_class = "card-grid card-grid--3" if len(fiches) > 4 else "card-grid"
    head = (
        '<div class="page-head"><p class="page-head__kicker">Rubrique</p>'
        '<h1>%s</h1><p class="page-head__lede">%s</p></div>'
        % (escape_html(rubrique["titre"]), escape_html(rubrique["resume"]))
    )
    body = (
        '<div class="layout"><div class="prose">%s</div>'
        '<ul class="%s">%s</ul></div>' % (head, grid_class, cards)
    )
    html = render_page(
        site,
        rubriques,
        title="%s — %s" % (rubrique["titre"], site["titre"]),
        description=rubrique["resume"],
        base="../",
        active=rubrique["slug"],
        trail=[("Accueil", "../index.html"), (rubrique["titre"], None)],
        body=body,
    )
    return "%s/index.html" % rubrique["slug"], html
