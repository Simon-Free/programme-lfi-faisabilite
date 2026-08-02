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

## Les deux constats, et les états qu'ils produisent

Une récolte porte **deux champs distincts**, qu'il ne faut jamais confondre.

| Champ | Ce qu'il établit | Qui l'établit |
|--------|------------------|---------------|
| `url_verifiee` | le lien a été ouvert **et** le document s'y trouve, portant bien ce qu'on lui attribue | une lecture |
| `lien_resout` | l'adresse répond et sert *un* document, sans que personne ait regardé lequel | une interrogation automatique |

`lien_resout` prend quatre valeurs :

| Valeur | Ce qu'elle dit | Étiquette rendue |
|---|---|---|
| `true` | l'adresse sert un document | Lien ouvert, document non relu |
| `"redirige"` | elle sert un document, à une autre adresse que celle annoncée | Lien ouvert, adresse déplacée |
| `"refuse"` | le site oppose un mur à tout client automatisé ; la page s'ouvre dans un navigateur | Lien refusé aux clients automatisés |
| `false` | elle ne sert rien, et aucun remplacement n'a été trouvé | Lien mort |

**Absent**, il signifie que l'adresse n'a jamais été interrogée. Passer de
`lien_resout` à `url_verifiee` suppose qu'un lecteur ait ouvert le document :
aucune interrogation automatique ne fait franchir cette marche, et `url_verifiee`
l'emporte toujours sur `lien_resout` au rendu — une référence lue reste
« vérifiée » même quand la machine n'a pas su ouvrir son adresse.

Un champ facultatif `lien_note` porte une phrase quand l'accès est
inhabituel — un site qui oppose un défi aux clients automatisés, un éditeur
dont l'accès est fermé. Elle est écrite à côté de la pastille.

Les états sont toujours écrits en toutes lettres, jamais portés par la couleur
seule, et chaque pastille est doublée d'un signe typographique. S'y ajoutent
« Lien non vérifié » quand `lien_resout` est absent, « Référence non retrouvée
en ligne » quand il n'y a pas d'adresse, et la mention de solidité faible.
**Une seule pastille d'état par référence** : la liste en compte plus de cinq
cents, deux marques par ligne la rendraient illisible. Une `url` qui ne commence
pas par `http://` ou `https://` ne produit aucun lien.

## Modules
| Module | Description |
|--------|-------------|
| `lecture.py` | Chargement tolérant des JSON et titres des fiches du manifeste |
| `entree.py` | Rendu d'une source : ce qu'on en tire, organisme, titre, repérage, accès |
| `liste.py` | Bibliographie d'une fiche et son décompte (`::: sources`) |
| `regroupement.py` | Dédoublonnage des documents et regroupement par organisme |
| `page.py` | Page bibliographie du site (`::: bibliographie`) |
