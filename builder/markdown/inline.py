"""Conversion des elements en ligne du markdown vers HTML.

Aucune dependance externe. La strategie tient en trois temps :
1. les fragments litteraux (code, liens automatiques) sont mis de cote ;
2. le reste du texte est echappe puis transforme par expressions regulieres ;
3. les fragments litteraux sont reinjectes, echappes eux aussi.
"""

import re
import unicodedata

SENTINEL = "\x00{}\x00"

CODE_SPAN = re.compile(r"(?<!`)(`+)(?!`)(.+?)(?<!`)\1(?!`)", re.DOTALL)
AUTOLINK = re.compile(r"<((?:https?|mailto):[^>\s]+)>")
FOOTNOTE_REF = re.compile(r"\[\^([^\]\s]+)\]")
LINK = re.compile(r"\[([^\]]*)\]\(\s*(<[^>]*>|[^)\s]*)(?:\s+\"([^\"]*)\")?\s*\)")
IMAGE = re.compile(r"!\[([^\]]*)\]\(\s*([^)\s]+)(?:\s+\"([^\"]*)\")?\s*\)")
STRONG = re.compile(r"\*\*(?=\S)(.+?)(?<=\S)\*\*", re.DOTALL)
STRONG_ALT = re.compile(r"(?<![\w])__(?=\S)(.+?)(?<=\S)__(?![\w])", re.DOTALL)
EMPHASIS = re.compile(r"(?<![\*\w])\*(?=\S)([^\*]+?)(?<=\S)\*(?!\*)")
EMPHASIS_ALT = re.compile(r"(?<![\w_])_(?=\S)([^_]+?)(?<=\S)_(?![\w_])")
STRIKE = re.compile(r"~~(?=\S)(.+?)(?<=\S)~~", re.DOTALL)
ESCAPED_CHAR = re.compile(r"\\([\\`*_{}\[\]()#+\-.!|~>])")
BADGE = re.compile(r"\{\{\s*(confiance|gravite)\s*:\s*([\w-]+)\s*\}\}")

# Statuts reserves : la pastille est toujours doublee d'un libelle.
BADGE_LABELS = {
    ("confiance", "elevee"): "Confiance élevée",
    ("confiance", "moyenne"): "Confiance moyenne",
    ("confiance", "faible"): "Confiance faible",
    ("gravite", "bloquant"): "Constat bloquant",
    ("gravite", "majeur"): "Constat majeur",
    ("gravite", "mineur"): "Constat mineur",
}


def escape_html(text):
    """Echappe les caracteres qui changeraient la structure du document."""
    return (
        text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    )


def escape_attribute(text):
    return escape_html(text).replace('"', "&quot;")


def slugify(text, fallback="section"):
    """Identifiant d'ancre : sans accent, sans ponctuation, en minuscules."""
    stripped = unicodedata.normalize("NFD", text)
    stripped = "".join(c for c in stripped if unicodedata.category(c) != "Mn")
    stripped = re.sub(r"[^a-zA-Z0-9]+", "-", stripped).strip("-").lower()
    return stripped or fallback


class _LiteralStore:
    """Range les fragments a ne pas transformer, sous un jeton unique."""

    def __init__(self):
        self.fragments = []

    def put(self, html):
        self.fragments.append(html)
        return SENTINEL.format(len(self.fragments) - 1)

    def restore(self, text):
        for index, html in enumerate(self.fragments):
            text = text.replace(SENTINEL.format(index), html)
        return text


def _clean_url(url):
    if url.startswith("<") and url.endswith(">"):
        url = url[1:-1]
    return escape_attribute(url)


def _render_link(match):
    label, url, title = match.group(1), match.group(2), match.group(3)
    attrs = ' title="%s"' % escape_attribute(title) if title else ""
    return '<a href="%s"%s>%s</a>' % (_clean_url(url), attrs, label)


def render_inline(text, footnote_ids=None):
    """Transforme une portion de texte markdown en fragment HTML."""
    store = _LiteralStore()

    def stash_code(match):
        return store.put("<code>%s</code>" % escape_html(match.group(2).strip()))

    def stash_autolink(match):
        target = match.group(1)
        return store.put(
            '<a href="%s">%s</a>' % (escape_attribute(target), escape_html(target))
        )

    def stash_image(match):
        alt, url, title = match.group(1), match.group(2), match.group(3)
        attrs = ' title="%s"' % escape_attribute(title) if title else ""
        return store.put(
            '<img src="%s" alt="%s"%s loading="lazy">'
            % (_clean_url(url), escape_attribute(alt), attrs)
        )

    def stash_footnote(match):
        key = slugify(match.group(1), "note")
        if footnote_ids is None:
            return store.put(escape_html(match.group(0)))
        first_reference = key not in footnote_ids
        if first_reference:
            footnote_ids.append(key)
        number = footnote_ids.index(key) + 1
        anchor = ' id="renvoi-%s"' % key if first_reference else ""
        return store.put(
            '<sup><a class="footnote-ref" href="#note-%s"%s'
            ' aria-label="Note de bas de page %d">[%d]</a></sup>'
            % (key, anchor, number, number)
        )

    def stash_badge(match):
        family, level = match.group(1), match.group(2)
        label = BADGE_LABELS.get((family, level))
        if label is None:
            return store.put(escape_html(match.group(0)))
        return store.put(
            '<span class="badge badge--%s-%s">%s</span>'
            % (family, level, escape_html(label))
        )

    text = CODE_SPAN.sub(stash_code, text)
    text = BADGE.sub(stash_badge, text)
    text = IMAGE.sub(stash_image, text)
    text = AUTOLINK.sub(stash_autolink, text)
    text = FOOTNOTE_REF.sub(stash_footnote, text)
    text = escape_html(text)
    text = LINK.sub(_render_link, text)
    text = STRONG.sub(r"<strong>\1</strong>", text)
    text = STRONG_ALT.sub(r"<strong>\1</strong>", text)
    text = STRIKE.sub(r"<del>\1</del>", text)
    text = EMPHASIS.sub(r"<em>\1</em>", text)
    text = EMPHASIS_ALT.sub(r"<em>\1</em>", text)
    text = ESCAPED_CHAR.sub(r"\1", text)
    return store.restore(text).strip()
