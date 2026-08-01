# assets

## Purpose
La charte graphique et le comportement client. Zéro dépendance externe :
polices système, aucun CDN, aucune requête réseau.

## Usage
Les trois feuilles sont chargées dans cet ordre par le gabarit.

| Fichier | Rôle |
|--------|------|
| `style.css` | **Jetons** (couleurs, typographie, espacement), réinitialisation, titres, texte |
| `components.css` | Barre de navigation, fil d'Ariane, sommaire, cartes, pagination, pied de page |
| `content.css` | Chiffres clés, encadrés, tableaux, badges, notes, recherche |
| `app.js` | Bascule de thème (mémorisée) et filtrage de la recherche |

## Règles de couleur
Tous les hex vivent dans les deux blocs de jetons de `style.css` — un thème
clair et un thème sombre. **Ne jamais écrire un hex ailleurs.**

- `--cat-1` à `--cat-8` : palette de données, assignée dans l'ordre, jamais cyclée.
- `--confidence-*` et `--severity-*` : **réservées**. Jamais utilisées comme
  couleur de série, et toujours accompagnées d'un libellé — jamais la couleur seule.

Le thème suit `prefers-color-scheme`, et l'attribut `data-theme` posé par le
bouton l'emporte dans les deux sens.
