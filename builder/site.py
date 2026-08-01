"""Orchestration : lecture du manifeste, rendu de toutes les pages, ecriture."""

import json
from pathlib import Path

from .render import (
    render_fiche,
    render_index,
    render_intro,
    render_rubrique,
    render_search,
    render_search_index,
)


class Manifest:
    """Le manifeste, deja trie et indexe par rubrique."""

    def __init__(self, data, root):
        self.site = data["site"]
        self.rubriques = data["rubriques"]
        self.source_dir = (root / self.site["source_dir"]).resolve()
        known = {rubrique["slug"] for rubrique in self.rubriques}
        inconnues = sorted(
            fiche["rubrique"]
            for fiche in data["fiches"]
            if fiche["rubrique"] not in known
        )
        if inconnues:
            raise ValueError("Rubriques inconnues dans le manifeste : %s" % inconnues)
        self.fiches_par_rubrique = {
            rubrique["slug"]: sorted(
                (f for f in data["fiches"] if f["rubrique"] == rubrique["slug"]),
                key=lambda f: f["ordre"],
            )
            for rubrique in self.rubriques
        }
        self.ordre_lecture = [
            fiche
            for rubrique in self.rubriques
            for fiche in self.fiches_par_rubrique[rubrique["slug"]]
        ]


def load_manifest(path):
    path = Path(path).resolve()
    data = json.loads(path.read_text(encoding="utf-8"))
    return Manifest(data, path.parent)


def _neighbours(ordre, position):
    previous = ordre[position - 1] if position > 0 else None
    following = ordre[position + 1] if position + 1 < len(ordre) else None
    return previous, following


def _render_all(manifest):
    """Produit la liste complete des couples (chemin relatif, contenu)."""
    site, rubriques = manifest.site, manifest.rubriques
    source_dir = manifest.source_dir
    intro = render_intro(source_dir, site.get("accueil"))
    outputs = [
        render_index(
            site, rubriques, manifest.fiches_par_rubrique, source_dir, intro
        ),
        render_search(site, rubriques),
        render_search_index(rubriques, manifest.ordre_lecture, source_dir),
    ]
    for rubrique in rubriques:
        fiches = manifest.fiches_par_rubrique[rubrique["slug"]]
        outputs.append(
            render_rubrique(site, rubriques, rubrique, fiches, source_dir)
        )
        for fiche in fiches:
            position = manifest.ordre_lecture.index(fiche)
            outputs.append(
                render_fiche(
                    site,
                    rubriques,
                    rubrique,
                    fiche,
                    source_dir,
                    _neighbours(manifest.ordre_lecture, position),
                )
            )
    return outputs


def _write_if_changed(path, content):
    """Ecriture idempotente : le fichier n'est touche que s'il change."""
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    return True


def build_site(manifest, output_dir):
    """Ecrit le site. Retourne (fichiers ecrits, fichiers inchanges, fiches publiees)."""
    output_dir = Path(output_dir).resolve()
    written, unchanged = [], []
    for relative, content in _render_all(manifest):
        if _write_if_changed(output_dir / relative, content):
            written.append(relative)
        else:
            unchanged.append(relative)
    publiees = [
        fiche
        for fiche in manifest.ordre_lecture
        if (manifest.source_dir / fiche["source"]).exists()
    ]
    return written, unchanged, publiees
