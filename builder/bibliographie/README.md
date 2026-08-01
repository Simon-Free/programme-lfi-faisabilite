# bibliographie

## Purpose
L'appareil de sources du site. Lit les récoltes de `sources/*.json` **à la
construction** — jamais dans le navigateur, le site restant consultable en
`file://` — et les rend sous deux formes : la bibliographie d'une fiche, en
pied de page, et la bibliographie générale du dossier, groupée par organisme.

Un fichier absent, partiel ou illisible ne casse jamais la construction : il
produit un encadré qui dit où en est la récolte.

## Usage
Depuis une fiche markdown, deux directives :

```
::: sources 7
:::

::: bibliographie
:::
```

`::: sources` accepte le numéro du chapitre (`7`, `07`, `ch07`) ou le nom du
markdown de la fiche (`obstacle_europe`). En Python :

```python
from builder.bibliographie import rendre_liste, rendre_bibliographie
```

Trois états sont toujours écrits en toutes lettres, jamais portés par la
couleur seule : lien vérifié, lien non vérifié, référence non retrouvée en
ligne — auxquels s'ajoute la mention de solidité faible. Une `url` qui ne
commence pas par `http://` ou `https://` ne produit aucun lien.

## Modules
| Module | Description |
|--------|-------------|
| `lecture.py` | Chargement tolérant des JSON et titres des fiches du manifeste |
| `entree.py` | Rendu d'une source : ce qu'on en tire, organisme, titre, repérage, accès |
| `liste.py` | Bibliographie d'une fiche et son décompte (`::: sources`) |
| `regroupement.py` | Dédoublonnage des documents et regroupement par organisme |
| `page.py` | Page bibliographie du site (`::: bibliographie`) |
