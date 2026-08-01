"""Blocs composants ouverts par `:::`, utilisables depuis les fiches markdown.

    ::: attention Titre facultatif
    Texte markdown normal.
    :::

    ::: chiffres
    - 460 Md€/an | Depenses annoncees | Lecture litterale, avant correction
    - 12 ans | Duree du chantier | Calendrier reconstitue
    :::

Le rendu passe par les classes de la charte : aucune couleur n'est ecrite ici.
"""

import re

from ..inline import escape_html, render_inline

CONTAINER_FENCE = re.compile(r"^:::+\s*([\w-]*)\s*(.*?)\s*$")
STAT_LINE = re.compile(r"^\s*[-*+]\s+(.*)$")

CALLOUT_TITLES = {
    "attention": "Attention",
    "bloquant": "Point bloquant",
    "methode": "Note de méthode",
}


def is_container_open(line):
    found = CONTAINER_FENCE.match(line)
    return found if found and found.group(1) else None


def is_container_close(line):
    found = CONTAINER_FENCE.match(line)
    return bool(found and not found.group(1) and not found.group(2))


def _callout(kind, title, inner_html):
    label = title or CALLOUT_TITLES[kind]
    return (
        '<div class="callout callout--%s" role="note">'
        '<p class="callout__title">%s</p>%s</div>'
        % (kind, render_inline(label, None), inner_html)
    )


def _stat(position, cells, footnote_ids):
    value = render_inline(cells[0], footnote_ids)
    label = render_inline(cells[1], footnote_ids) if len(cells) > 1 else ""
    note = render_inline(cells[2], footnote_ids) if len(cells) > 2 else ""
    slot = position % 8 + 1
    return (
        '<li><div class="stat stat--%d">'
        '<span class="stat__value">%s</span>'
        '<span class="stat__label">%s</span>%s</div></li>'
        % (
            slot,
            value,
            label,
            '<p class="stat__note">%s</p>' % note if note else "",
        )
    )


def _stats(lines, footnote_ids):
    entries = []
    for line in lines:
        found = STAT_LINE.match(line)
        if not found:
            continue
        cells = [cell.strip() for cell in found.group(1).split("|")]
        entries.append(_stat(len(entries), cells, footnote_ids))
    if not entries:
        return ""
    return '<ul class="stat-grid">%s</ul>' % "".join(entries)


def _figure(title, lines):
    """`::: graphique <identifiant>` — insere une figure du registre.

    L'import est differe : le paquet `charts` lit lui-meme `markdown.inline`,
    et un import en tete de module fermerait le cycle.
    """
    from ...charts import rendre_figure

    identifiant = title.strip() or " ".join(line.strip() for line in lines)
    return rendre_figure(identifiant)


def render_container(kind, title, lines, parse_inner, footnote_ids):
    """Rend un bloc `:::`. Un type inconnu retombe sur un encadre de methode."""
    if kind == "chiffres":
        return _stats(lines, footnote_ids)
    if kind == "graphique":
        return _figure(title, lines)
    if kind not in CALLOUT_TITLES:
        return (
            '<div class="callout callout--methode"><p class="callout__title">'
            "Bloc inconnu : %s</p>%s</div>" % (escape_html(kind), parse_inner(lines))
        )
    return _callout(kind, title, parse_inner(lines))
