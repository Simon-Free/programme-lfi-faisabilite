"""Assemblage du document final : corps HTML, titre, sommaire, notes."""

from .blocks import Parser
from .inline import render_inline


class Document:
    """Resultat d'une conversion : le corps HTML et sa table des matieres."""

    def __init__(self, html, titre, sections):
        self.html = html
        self.titre = titre
        self.sections = sections


def _render_footnotes(definitions, order):
    """Les notes sont numerotees dans l'ordre de leur premier appel."""
    used = [key for key in order if key in definitions]
    if not used:
        return ""
    items = "".join(
        '<li id="note-%s">%s <a href="#renvoi-%s" aria-label="Retour au texte">'
        "&#8617;</a></li>" % (key, render_inline(definitions[key], None), key)
        for key in used
    )
    return (
        '<section class="footnotes" aria-labelledby="titre-notes">'
        '<h2 id="titre-notes">Notes</h2><ol>%s</ol></section>' % items
    )


def render_markdown(text):
    """Point d'entree du convertisseur : un texte markdown, un Document."""
    footnote_ids = []
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    parser = Parser(lines, footnote_ids)
    body = "\n".join(parser.parse())
    body += _render_footnotes(parser.footnotes, list(dict.fromkeys(footnote_ids)))
    return Document(body, parser.titre, parser.sections)
