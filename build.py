#!/usr/bin/env python3
"""Genere le site statique de l'expertise de faisabilite.

Bibliotheque standard uniquement. Relancable a volonte : seules les pages dont
le contenu change sont reecrites.

    python site/build.py
    python site/build.py --manifeste site/manifest.json --sortie site
"""

import argparse
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent
if str(RACINE) not in sys.path:
    sys.path.insert(0, str(RACINE))

from builder import build_site, load_manifest  # noqa: E402


def analyser_arguments(argv):
    parser = argparse.ArgumentParser(
        description="Genere le site statique a partir des fiches de vulgarise/."
    )
    parser.add_argument(
        "--manifeste",
        default=str(RACINE / "manifest.json"),
        help="Chemin du manifeste (defaut : site/manifest.json).",
    )
    parser.add_argument(
        "--sortie",
        default=str(RACINE),
        help="Dossier de sortie (defaut : site/).",
    )
    parser.add_argument(
        "--silencieux",
        action="store_true",
        help="N'affiche que le resume final.",
    )
    return parser.parse_args(argv)


def main(argv=None):
    options = analyser_arguments(argv)
    manifest = load_manifest(options.manifeste)
    ecrits, inchanges, publiees = build_site(manifest, options.sortie)

    if not options.silencieux:
        for chemin in ecrits:
            print("  ecrit      %s" % chemin)
        for chemin in inchanges:
            print("  inchange   %s" % chemin)

    total = len(manifest.ordre_lecture)
    manquantes = [
        fiche["source"]
        for fiche in manifest.ordre_lecture
        if fiche not in publiees
    ]
    print(
        "\n%d pages generees (%d reecrites, %d inchangees)."
        % (len(ecrits) + len(inchanges), len(ecrits), len(inchanges))
    )
    print("%d fiches sur %d ont un markdown source." % (len(publiees), total))
    if manquantes:
        print(
            "En attente dans %s : %s"
            % (manifest.source_dir.name, ", ".join(manquantes))
        )
    print("Ouvrir : %s" % (Path(options.sortie).resolve() / "index.html"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
