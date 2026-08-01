# builder

## Purpose
Le générateur du site : lecture du manifeste, conversion markdown, rendu des
pages, écriture idempotente. Bibliothèque standard uniquement.

## Usage
```python
from builder import build_site, load_manifest

manifest = load_manifest("site/manifest.json")
ecrits, inchanges, publiees = build_site(manifest, "site")
```
`load_manifest` trie les fiches par rubrique et par ordre, et refuse un
manifeste qui référence une rubrique inconnue. `build_site` n'écrit un fichier
que si son contenu a changé — d'où l'idempotence.

## Subfolders
| Folder | Description |
|--------|-------------|
| `bibliographie/` | Sources lues dans `sources/*.json` : liste en pied de fiche et page bibliographie |
| `charts/` | Les huit infographies, en SVG écrit à la main, et leur registre |
| `markdown/` | Convertisseur markdown maison (aucune dépendance) |
| `render/` | Gabarit HTML et construction des pages |
