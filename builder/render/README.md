# render

## Purpose
Transforme le manifeste et les fiches converties en pages HTML complètes.

## Usage
| Fichier | Rôle |
|--------|------|
| `template.py` | Gabarit commun : en-tête, navigation, bandeau d'avertissement, fil d'Ariane, pied de page |
| `pages.py` | Page de fiche (sommaire, pagination) et page de rubrique |
| `home.py` | Accueil, page de recherche et index de recherche |

Chaque fonction rend un couple `(chemin relatif, contenu)` ; c'est
`builder/site.py` qui écrit sur disque.

Deux contraintes structurantes :
- tous les liens de rubrique pointent sur `<rubrique>/index.html` — en `file://`
  un dossier nu affiche la liste des fichiers au lieu de la page ;
- l'index de recherche est un `.js` qui pose `window.SEARCH_INDEX`, et non un
  `.json` : `fetch()` est bloqué en `file://`.
