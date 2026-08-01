"""Structures repetitives du markdown : tableaux et listes.

Fonctions pures : elles recoivent les lignes, la position courante et une
fonction de rendu en ligne, et rendent le couple (html, position suivante).
"""

import re

LIST_ITEM = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$")
TABLE_SEPARATOR = re.compile(r"^\s*\|?[\s:|-]+\|[\s:|-]*$")
HEADING_START = re.compile(r"^#{1,6}\s+")
ALIGNMENTS = {(True, True): "col-center", (False, True): "col-right"}

TABLE_SHELL = (
    '<div class="table-wrap" tabindex="0" role="region"'
    ' aria-label="Tableau, défilement horizontal possible">'
    "<table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>"
)


def _split_row(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [cell.strip() for cell in line.split("|")]


def _alignment_classes(separator_cells):
    return [
        ALIGNMENTS.get((cell.startswith(":"), cell.endswith(":")), "")
        for cell in (raw.strip() for raw in separator_cells)
    ]


def _cell(tag, content, css_class, render):
    attr = ' class="%s"' % css_class if css_class else ""
    return "<%s%s>%s</%s>" % (tag, attr, render(content), tag)


def starts_table(lines, index):
    header = lines[index]
    following = lines[index + 1] if index + 1 < len(lines) else None
    return "|" in header and bool(following) and bool(TABLE_SEPARATOR.match(following))


def parse_table(lines, index, render):
    columns = _split_row(lines[index])
    classes = _alignment_classes(_split_row(lines[index + 1]))
    classes += [""] * (len(columns) - len(classes))
    index += 2
    head = "".join(
        _cell("th", text, classes[position], render)
        for position, text in enumerate(columns)
    )
    rows = []
    while index < len(lines) and lines[index].strip() and "|" in lines[index]:
        cells = _split_row(lines[index])
        cells += [""] * (len(columns) - len(cells))
        rows.append(
            "<tr>%s</tr>"
            % "".join(
                _cell("td", text, classes[position], render)
                for position, text in enumerate(cells[: len(columns)])
            )
        )
        index += 1
    return TABLE_SHELL % (head, "".join(rows)), index


def starts_list(line):
    return bool(LIST_ITEM.match(line))


def _is_continuation(lines, index, indent):
    line = lines[index]
    if not line.strip() or LIST_ITEM.match(line) or HEADING_START.match(line):
        return False
    return len(line) - len(line.lstrip()) > indent


def parse_list(lines, index, render, indent=None):
    """Une liste, ses items et ses eventuelles sous-listes."""
    if indent is None:
        indent = len(LIST_ITEM.match(lines[index]).group(1))
    ordered = None
    items = []
    while index < len(lines):
        found = LIST_ITEM.match(lines[index])
        if not found or len(found.group(1)) < indent:
            break
        if len(found.group(1)) > indent:
            nested, index = parse_list(lines, index, render, len(found.group(1)))
            if items:
                items[-1] += nested
            else:
                items.append(nested)
            continue
        if ordered is None:
            ordered = found.group(2) not in ("-", "*", "+")
        index += 1
        body = [found.group(3)]
        while index < len(lines) and _is_continuation(lines, index, indent):
            body.append(lines[index].strip())
            index += 1
        items.append(render(" ".join(body)))
    tag = "ol" if ordered else "ul"
    html = "<%s>%s</%s>" % (
        tag,
        "".join("<li>%s</li>" % item for item in items),
        tag,
    )
    return html, index
