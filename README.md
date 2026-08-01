# site

## Purpose
Génère le site statique de l'expertise de faisabilité à partir des fiches
markdown de `../vulgarise/` et des métadonnées de `manifest.json`.
Aucune dépendance : bibliothèque standard Python 3.13, CSS et JavaScript purs.
Le site s'ouvre par double-clic sur `index.html` (protocole `file://`).

## Usage
```
python site/build.py                 # génère tout
python site/build.py --silencieux    # n'affiche que le résumé
python site/build.py --sortie /tmp/x # génère ailleurs
```
Le script est idempotent : une page n'est réécrite que si son contenu change.
Une fiche dont le markdown est absent produit une page « Fiche à venir » ;
il suffit de relancer le build quand le fichier arrive.

`manifest.json` pilote tout : `site` (titres, dossier source), `rubriques`
(slug, titre, résumé, slot de palette) et `fiches` (slug, source, rubrique,
ordre, titre, résumé, mots-clés). Ajouter une fiche = ajouter une ligne.

## Fichiers générés
`index.html`, `recherche.html`, `search-index.js`, et un dossier par rubrique
contenant `index.html` plus une page par fiche. Ne pas les éditer à la main.

## Subfolders
| Folder | Description |
|--------|-------------|
| `assets/` | Charte CSS (thème clair et sombre), composants, JavaScript |
| `builder/` | Le générateur : convertisseur markdown et rendu des pages |
