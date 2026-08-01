"""Page d'accueil, page de recherche et index de recherche."""

import json

from ..markdown import escape_html, render_markdown
from .pages import fiche_url
from .template import render_page


def _rubrique_card(rubrique, published, total):
    return (
        '<li><a class="card card--slot-%d" href="%s/index.html">'
        '<p class="card__meta">%d fiche%s sur %d</p>'
        "<h3>%s</h3><p>%s</p></a></li>"
        % (
            rubrique.get("slot", 1),
            rubrique["slug"],
            published,
            "s" if published > 1 else "",
            total,
            escape_html(rubrique["titre"]),
            escape_html(rubrique["resume"]),
        )
    )


def render_index(site, rubriques, fiches_par_rubrique, source_dir, intro_html):
    cards = []
    published_total = 0
    fiche_total = 0
    for rubrique in rubriques:
        fiches = fiches_par_rubrique.get(rubrique["slug"], [])
        published = sum(
            1 for fiche in fiches if (source_dir / fiche["source"]).exists()
        )
        published_total += published
        fiche_total += len(fiches)
        cards.append(_rubrique_card(rubrique, published, len(fiches)))

    head = (
        '<div class="page-head"><p class="page-head__kicker">'
        "Expertise de faisabilité</p><h1>%s</h1>"
        '<p class="page-head__lede">%s</p></div>'
        % (escape_html(site["titre"]), escape_html(site["accroche"]))
    )
    etat = (
        '<p class="empty-note">%d fiches publiées sur %d prévues — version du %s.</p>'
        % (published_total, fiche_total, escape_html(site["date"]))
    )
    body = (
        '<div class="layout"><div class="prose">%s%s%s</div>'
        '<ul class="card-grid card-grid--3">%s</ul></div>'
        % (head, intro_html, etat, "".join(cards))
    )
    html = render_page(
        site,
        rubriques,
        title=site["titre"],
        description=site["accroche"],
        base="",
        active="",
        trail=[],
        body=body,
    )
    return "index.html", html


def render_search(site, rubriques):
    body = (
        '<div class="layout"><div class="prose">'
        '<div class="page-head"><p class="page-head__kicker">Recherche</p>'
        "<h1>Chercher une fiche</h1>"
        '<p class="page-head__lede">Le filtre porte sur les titres, les résumés '
        "et les mots-clés. Il fonctionne hors ligne, sans requête réseau.</p></div>"
        '<div class="search">'
        '<label class="visually-hidden" for="recherche">Rechercher une fiche</label>'
        '<input class="search__field" id="recherche" type="search" '
        'data-search-field data-base="" autocomplete="off" '
        'placeholder="Par exemple : retraite, Europe, main-d\'œuvre">'
        '<p class="search__status" data-search-status role="status" '
        'aria-live="polite"></p>'
        '<ul class="search__results" data-search-results></ul>'
        "</div></div></div>"
    )
    html = render_page(
        site,
        rubriques,
        title="Recherche — %s" % site["titre"],
        description="Filtrer les fiches par titre, resume ou mot-cle.",
        base="",
        active="recherche",
        trail=[("Accueil", "index.html"), ("Recherche", None)],
        body=body,
        scripts='<script src="search-index.js"></script>',
    )
    return "recherche.html", html


def render_search_index(rubriques, fiches, source_dir):
    labels = {rubrique["slug"]: rubrique["titre"] for rubrique in rubriques}
    entries = []
    for fiche in fiches:
        published = (source_dir / fiche["source"]).exists()
        entries.append(
            {
                "titre": fiche["titre"],
                "resume": fiche["resume"]
                if published
                else fiche["resume"] + " (fiche à venir)",
                "rubrique": labels.get(fiche["rubrique"], fiche["rubrique"]),
                "url": fiche_url(fiche),
                "mots": fiche.get("mots", ""),
                "publie": published,
            }
        )
    payload = json.dumps(entries, ensure_ascii=False, indent=1, sort_keys=True)
    return "search-index.js", "window.SEARCH_INDEX = %s;\n" % payload


def render_intro(source_dir, filename):
    """Le texte d'accueil est optionnel : le site se construit sans lui."""
    if not filename:
        return ""
    path = source_dir / filename
    if not path.exists():
        return ""
    return render_markdown(path.read_text(encoding="utf-8")).html
