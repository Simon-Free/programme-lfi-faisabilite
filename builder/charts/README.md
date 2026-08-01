# charts

## Purpose
Les dix-sept infographies du site, en SVG écrit à la main. Aucune dépendance,
aucun CDN : le site doit s'ouvrir par double-clic en `file://`.

Le dessin vit ici et non dans les fiches markdown pour deux raisons : le
convertisseur échappe le HTML brut (une figure ne peut donc pas être écrite
dans une fiche), et deux cents lignes de SVG noieraient le texte qu'elles
illustrent. Une fiche appelle une figure par son identifiant :

```
::: graphique chiffrage-consolide
:::
```

Une figure déclinable prend ses arguments à la suite de l'identifiant, séparés
par des espaces. `rendre_figure()` les passe à la fabrique ; les figures sans
argument s'appellent exactement comme avant.

```
::: graphique detail-mesures 5
:::
```

## Règles de tracé
- **Aucune couleur écrite ici.** Les marques portent une classe `mark--N`
  (série catégorielle) ou `mark--<statut>` (statut réservé) ; les valeurs
  vivent dans `assets/charts.css`, qui lit les jetons de `assets/style.css`.
- **Palette validée** par `scripts/validate_palette.js` de la compétence
  `dataviz`, dans les deux thèmes, sur les sous-ensembles réellement employés.
  Au-delà de quatre séries adjacentes la palette échoue : on facette ou on
  coupe, on ne cycle jamais les teintes.
- **Les couleurs de statut ne séparent pas des identités.** Elles échouent au
  contrôle daltonien dès que deux aplats se touchent : les barres de statut
  sont détachées et portent toujours un libellé en clair.
- **Jamais de double axe.** Deux unités qui ne s'additionnent pas donnent deux
  panneaux séparés, chacun avec son échelle et son titre.
- **La gouttière des libellés se mesure sur le plus long d'entre eux** : un
  libellé n'est jamais tronqué, c'est la gouttière qui cède.
- **Une valeur négative se dessine à gauche d'un zéro, jamais du bord du
  cadre.** Sans valeur négative, le plancher de l'échelle reste à zéro et le
  tracé est inchangé. Sinon l'échelle descend d'un cran arrondi — le plus
  petit qui couvre la valeur *et* laisse une bande visible —, un repère marque
  le zéro, et la part sous zéro porte un jeton de statut réservé, doublé du
  signe sur l'étiquette et d'une mention en clair : jamais la couleur seule.
- Chaque figure est autonome : titre qui énonce le résultat, phrase de lecture,
  tableau de substitution, note de source.

## Fichiers
| Fichier | Rôle |
|---|---|
| `__init__.py` | Le registre : identifiant → fabrique de figure |
| `base.py` | Enveloppe commune, formatage des nombres, tableau, légende |
| `bars.py` | Barres horizontales à fourchette, axe gradué, tracé des valeurs négatives |
| `bars_echelle.py` | Le cadrage des barres : plafond, plancher sous zéro, graduations, gouttière |
| `stacks.py` | Barres empilées : la part dans un tout, en valeur ou en % |
| `figures.py` | Formes qui ne sont pas des graphiques : héros, jauge, étapes |
| `budget.py` | Chiffrage consolidé, coût par chapitre, doubles comptes |
| `natures.py` | Les trois natures de coût, acquisitions détaillées |
| `decaissement.py` | Le profil sur dix ans — le seul axe additif |
| `recettes.py` | Taux de couverture — 18,4 % — et origine des 84,6 Md€/an de ressources opposables |
| `sources.py` | D'où viennent les recettes, et quand elles arrivent |
| `capital_stock.py` | Le patrimoine national et sa composition |
| `capital_distribution.py` | La distribution, et l'inversion au sommet |
| `capital_rendement.py` | Ce que le capital rapporte, et ce qui est déjà pris |
| `capital_international.py` | La position française dans l'OCDE |
| `capital_gisements.py` | Le rendement supplémentaire défendable |
| `murs.py` | Niveaux de confiance, mur de la main-d'œuvre |
| `institutions.py` | Calendrier législatif, risque constitutionnel |
| `variantes.py` | Variantes rentables à objectifs inchangés |
| `chiffrages_cellules.py` | Lit une cellule de tableau d'analyse : montant, unité, nature |
| `chiffrages_analyses.py` | Le coût net par mesure, extrait du § 4 des 18 analyses |
| `mesures_lecture.py` | Croise l'inventaire de l'audit et les coûts du § 4 : retenues, non confirmées, muettes |
| `mesures.py` | Le nuage global des mesures au coût vérifié, échelle log |
| `detail_mesures.py` | Le détail par chapitre : `detail-mesures <numéro>` |
| `detail_mesures_trace.py` | Un panneau de sucettes classées, échelle log adaptative |
| `detail_mesures_couverture.py` | La bande chiffré / sans montant, hachurée |
| `detail_mesures_note.py` | Convention d'échelle et écart au total publié |
| `detail_mesures_totaux.py` | Les totaux de chapitre cités depuis `chiffrage.md` |

## L'absence de donnée n'est pas une couleur
Les mesures que le dossier laisse sans montant occupent leur part de la bande
de couverture, **hachurées** et non teintées : une teinte se lirait comme une
valeur. La hachure sert aussi de canal accessible à l'impression et en
`forced-colors`. Les mesures sans coût propre ne sont jamais omises d'une
figure : les taire laisserait croire à un inventaire complet. Elles se
comptent en deux paquets distincts, et la note sous la figure les nomme
séparément — celles que le dossier chiffre dans un bloc ou une enveloppe qu'il
ne ventile pas, et celles qui ne portent aucun montant nulle part.

## Palette employée, et son contrôle
Contrôlée par `scripts/validate_palette.js` de la compétence `dataviz`, dans
les deux thèmes, sur les sous-ensembles réellement adjacents : `{1,2}`,
`{1,3}`, `{1,2,3}`, `{1,2,7}`, `{1,2,3,4}` et `{1,2,3,7}`. Tous passent les
six contrôles. Deux avertissements de contraste subsistent en thème clair —
`--cat-3` à 2,82:1 et `--cat-4` à 2,17:1 — et ils sont couverts comme la
compétence l'exige : étiquettes de valeur visibles hors des aplats, et
tableau de substitution sous chaque figure. **Une valeur n'est jamais écrite
à l'intérieur d'un segment coloré** : à 11 px elle tomberait sous le seuil
dans l'un des deux thèmes au moins.
