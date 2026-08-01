"""Analyseur de blocs markdown : titres, paragraphes, citations, code, notes.

Les tableaux, les listes et les blocs composants `:::` sont delegues au
sous-paquet `elements`. L'assemblage final vit dans `document.py`.
"""

import re

from .elements import (
    is_container_close,
    is_container_open,
    parse_list,
    parse_table,
    render_container,
    starts_list,
    starts_table,
)
from .inline import escape_html, render_inline, slugify

HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
FENCE = re.compile(r"^(?:```|~~~)\s*([\w+-]*)\s*$")
RULE = re.compile(r"^\s*(?:-{3,}|\*{3,}|_{3,})\s*$")
QUOTE = re.compile(r"^\s*>\s?(.*)$")
FOOTNOTE_DEF = re.compile(r"^\[\^([^\]\s]+)\]:\s*(.*)$")
TAGS = re.compile(r"<[^>]+>")


class Parser:
    """Parcourt les lignes une seule fois et produit une liste de blocs HTML."""

    def __init__(self, lines, footnote_ids):
        self.lines = lines
        self.index = 0
        self.footnote_ids = footnote_ids
        self.sections = []
        self.titre = None
        self.footnotes = {}

    # -- utilitaires ----------------------------------------------------
    def done(self):
        return self.index >= len(self.lines)

    def inline(self, text):
        return render_inline(text, self.footnote_ids)

    def sub_parse(self, lines):
        inner = Parser(lines, self.footnote_ids)
        rendered = "\n".join(inner.parse())
        self.footnotes.update(inner.footnotes)
        return rendered

    # -- boucle principale ----------------------------------------------
    def parse(self):
        handlers = (
            self.take_container,
            self.take_fence,
            self.take_heading,
            self.take_rule,
            self.take_table,
            self.take_footnote,
            self.take_quote,
            self.take_list,
        )
        parts = []
        while not self.done():
            if not self.lines[self.index].strip():
                self.index += 1
                continue
            line = self.lines[self.index]
            block = None
            for handler in handlers:
                block = handler(line)
                if block is not None:
                    break
            parts.append(self.take_paragraph() if block is None else block)
        return [part for part in parts if part]

    # -- blocs ----------------------------------------------------------
    def take_container(self, line):
        opening = is_container_open(line)
        if not opening:
            return None
        self.index += 1
        body, depth = [], 1
        while not self.done():
            current = self.lines[self.index]
            self.index += 1
            if is_container_close(current):
                depth -= 1
                if depth == 0:
                    break
            elif is_container_open(current):
                depth += 1
            body.append(current)
        return render_container(
            opening.group(1),
            opening.group(2),
            body,
            self.sub_parse,
            self.footnote_ids,
        )

    def take_fence(self, line):
        opening = FENCE.match(line)
        if not opening:
            return None
        language = opening.group(1)
        self.index += 1
        body = []
        while not self.done() and not FENCE.match(self.lines[self.index]):
            body.append(self.lines[self.index])
            self.index += 1
        self.index += 1
        attr = ' class="language-%s"' % language if language else ""
        return "<pre><code%s>%s</code></pre>" % (attr, escape_html("\n".join(body)))

    def take_heading(self, line):
        found = HEADING.match(line)
        if not found:
            return None
        self.index += 1
        level, text = len(found.group(1)), found.group(2)
        rendered = self.inline(text)
        if level == 1:
            if self.titre is None:
                self.titre = TAGS.sub("", rendered)
                return ""
            level = 2
        anchor = slugify(text, "section-%d" % self.index)
        if level == 2:
            self.sections.append((anchor, TAGS.sub("", rendered)))
        return '<h%d id="%s">%s</h%d>' % (level, anchor, rendered, level)

    def take_rule(self, line):
        if not RULE.match(line):
            return None
        self.index += 1
        return "<hr>"

    def take_footnote(self, line):
        found = FOOTNOTE_DEF.match(line)
        if not found:
            return None
        self.index += 1
        body = [found.group(2)]
        while not self.done() and self.lines[self.index].startswith("    "):
            body.append(self.lines[self.index].strip())
            self.index += 1
        self.footnotes[slugify(found.group(1), "note")] = " ".join(body).strip()
        return ""

    def take_quote(self, line):
        if not QUOTE.match(line):
            return None
        body = []
        while not self.done() and QUOTE.match(self.lines[self.index]):
            body.append(QUOTE.match(self.lines[self.index]).group(1))
            self.index += 1
        return "<blockquote>%s</blockquote>" % self.sub_parse(body)

    def take_table(self, line):
        if not starts_table(self.lines, self.index):
            return None
        html, self.index = parse_table(self.lines, self.index, self.inline)
        return html

    def take_list(self, line):
        if not starts_list(line):
            return None
        html, self.index = parse_list(self.lines, self.index, self.inline)
        return html

    # -- paragraphe : bloc de repli --------------------------------------
    def _starts_new_block(self, line):
        if HEADING.match(line) or starts_list(line) or QUOTE.match(line):
            return True
        if RULE.match(line) or FENCE.match(line) or FOOTNOTE_DEF.match(line):
            return True
        if is_container_open(line) or is_container_close(line):
            return True
        return starts_table(self.lines, self.index)

    def take_paragraph(self):
        body = []
        while not self.done() and self.lines[self.index].strip():
            if body and self._starts_new_block(self.lines[self.index]):
                break
            body.append(self.lines[self.index].strip())
            self.index += 1
        if not body:
            self.index += 1
            return ""
        return "<p>%s</p>" % self.inline(" ".join(body))
