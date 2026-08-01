# elements

## Purpose
Les blocs markdown qui ont une structure propre, sortis de l'analyseur
principal pour le garder lisible.

## Usage
| Fichier | Rôle |
|--------|------|
| `tableaux.py` | Tableaux (avec alignement) et listes imbriquées. Fonctions pures : `(lignes, position, rendu) -> (html, position suivante)` |
| `containers.py` | Blocs `:::` : encadrés et grilles de chiffres clés |

### Raccourcis offerts aux rédacteurs

Encadrés — types `attention`, `bloquant`, `methode` ; le titre est facultatif :

```
::: attention Point de vigilance
Texte markdown normal.
:::
```

Grille de chiffres clés — `valeur | libellé | note` :

```
::: chiffres
- 460 Md€/an | Dépenses annoncées | Lecture littérale
:::
```

Badges de statut, utilisables en ligne y compris dans une cellule de tableau :
`{{confiance:elevee}}` `{{confiance:moyenne}}` `{{confiance:faible}}`
`{{gravite:bloquant}}` `{{gravite:majeur}}` `{{gravite:mineur}}`.
Chaque badge affiche toujours son libellé : la couleur ne porte jamais
l'information seule.
