# markdown

## Purpose
Convertisseur markdown écrit pour ce site, sans aucune dépendance.
Couvre titres, gras, italique, barré, listes imbriquées, tableaux avec
alignement, liens, images, code, citations, notes de bas de page, plus des
composants propres au projet (badges de statut, encadrés, chiffres clés).

## Usage
```python
from builder.markdown import render_markdown

doc = render_markdown(texte)
doc.html      # le corps HTML
doc.titre     # le premier titre de niveau 1, retiré du corps
doc.sections  # [(ancre, libellé)] des titres de niveau 2, pour le sommaire
```

| Fichier | Rôle |
|--------|------|
| `inline.py` | Éléments en ligne, échappement HTML, ancres, badges `{{...}}` |
| `blocks.py` | Analyseur ligne à ligne : titres, paragraphes, citations, code |
| `document.py` | Assemblage final : corps, sommaire, notes de bas de page |

Le HTML brut présent dans une fiche est échappé, jamais interprété : les
composants de la charte passent par les raccourcis documentés dans
`elements/README.md`.

## Subfolders
| Folder | Description |
|--------|-------------|
| `elements/` | Tableaux, listes et blocs composants `:::` |
