"""Produit un dossier autonome, pret a pousser sur GitHub Pages.

Usage : py site/publier.py [--sortie <chemin>]

Reconstruit le site, puis copie dans `dist/` uniquement ce qui doit etre servi :
le HTML, les assets, l'index de recherche. Le generateur Python et les sources
markdown restent en dehors.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

SITE = Path(__file__).parent
RACINE = SITE.parent

# Ce qui est servi au navigateur. Tout le reste est du code ou de la source.
A_PUBLIER = ("assets", "chapitres", "chiffrage", "ce-qui-marcherait", "comprendre",
             "obstacles", "sources")
FICHIERS = ("index.html", "recherche.html", "search-index.js", ".nojekyll")

EXCLUS = shutil.ignore_patterns("__pycache__", "*.pyc", "*.py")


def construire() -> None:
    """Relance le generateur pour que la sortie reflete les sources."""
    resultat = subprocess.run(
        [sys.executable, str(SITE / "build.py")],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    print(resultat.stdout.strip())
    if resultat.returncode != 0:
        print(resultat.stderr.strip(), file=sys.stderr)
        raise SystemExit("Le build a echoue : rien n'a ete publie.")


def copier(sortie: Path) -> tuple[int, int]:
    if sortie.exists():
        shutil.rmtree(sortie)
    sortie.mkdir(parents=True)

    dossiers = 0
    for nom in A_PUBLIER:
        source = SITE / nom
        if source.is_dir():
            shutil.copytree(source, sortie / nom, ignore=EXCLUS)
            dossiers += 1

    fichiers = 0
    for nom in FICHIERS:
        source = SITE / nom
        if source.is_file():
            shutil.copy2(source, sortie / nom)
            fichiers += 1

    (sortie / ".nojekyll").touch()
    return dossiers, fichiers


def verifier(sortie: Path) -> list[str]:
    """Controles qui cassent un deploiement GitHub Pages."""
    alertes = []
    pages = list(sortie.rglob("*.html"))
    if not pages:
        alertes.append("aucune page HTML produite")

    for page in pages:
        texte = page.read_text(encoding="utf-8", errors="replace")
        if 'href="/' in texte or 'src="/' in texte:
            alertes.append(f"{page.relative_to(sortie)} : chemin absolu (casse en sous-dossier)")
        if "http://" in texte:
            alertes.append(f"{page.relative_to(sortie)} : ressource en http, bloquee en https")

    if list(sortie.rglob("*.py")):
        alertes.append("du code Python subsiste dans la sortie")
    if not (sortie / "index.html").exists():
        alertes.append("index.html manquant a la racine")
    return alertes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sortie", default=str(RACINE / "dist"),
                        help="dossier de sortie (defaut : programme_lfi/dist)")
    args = parser.parse_args()
    sortie = Path(args.sortie)

    construire()
    dossiers, fichiers = copier(sortie)
    pages = len(list(sortie.rglob("*.html")))
    poids = sum(f.stat().st_size for f in sortie.rglob("*") if f.is_file()) / 1e6

    print(f"\nPublie dans {sortie}")
    print(f"  {pages} pages, {dossiers} rubriques, {fichiers} fichiers racine, {poids:.1f} Mo")

    alertes = verifier(sortie)
    if alertes:
        print("\nA corriger avant de pousser :")
        for alerte in alertes:
            print(f"  - {alerte}")
        return 1

    print("  Controles GitHub Pages : OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
