"""Un panneau de mesures classees, sur une echelle logarithmique.

Le chapitre le plus fourni aligne soixante-dix mesures, le plus maigre en
aligne quatre, et les montants vont de trois cent mille euros a quarante
milliards. Une echelle lineaire ecraserait la moitie des lignes contre l'axe :
on lit donc en decades, et la convention est ecrite sous la figure.

Les bornes de l'echelle se mesurent sur les donnees du panneau, pas sur le
programme entier : un chapitre a 620 M€ de maximum ne perd pas les deux tiers
de sa largeur a dessiner des decades vides.
"""

from math import ceil, floor, log10

from .base import escape_html, infobulle, nombre

LARGEUR = 720
GOUTTIERE = 302
MARGE_DROITE = 76
PAS = 19
RAYON = 4.0
PLANCHER = 0.0001  # 0,1 M€ : rien dans le dossier ne descend plus bas
CARACTERES_LIBELLE = 50


def montant_lisible(montant):
    """« 33,8 Md€ » ou « 0,3 M€ » : l'unite suit l'ordre de grandeur."""
    if montant >= 1:
        return "%s Md€" % nombre(montant, 1)
    millions = montant * 1000
    return "%s M€" % nombre(millions, 1 if millions < 10 else 0)


def _decades(valeurs):
    bas = floor(log10(max(min(valeurs), PLANCHER)))
    haut = ceil(log10(max(valeurs)))
    if haut <= bas:
        haut = bas + 1
    return bas, haut


def _abscisse(valeur, bornes):
    bas, haut = bornes
    part = (log10(max(valeur, 10.0 ** bas)) - bas) / float(haut - bas)
    return GOUTTIERE + part * (LARGEUR - GOUTTIERE - MARGE_DROITE)


def _axe(bornes, hauteur_plot, unite):
    bas, haut = bornes
    parts = []
    for exposant in range(bas, haut + 1):
        valeur = 10.0 ** exposant
        x = _abscisse(valeur, bornes)
        parts.append(
            '<line class="chart__grid" x1="%.1f" y1="0" x2="%.1f" y2="%d"/>'
            '<text class="chart__tick" x="%.1f" y="%d">%s</text>'
            % (x, x, hauteur_plot, x, hauteur_plot + 15,
               escape_html(montant_lisible(valeur)))
        )
    milieu = (GOUTTIERE + LARGEUR - MARGE_DROITE) / 2.0
    parts.append(
        '<text class="chart__axis-unit" x="%.1f" y="%d">%s</text>'
        % (milieu, hauteur_plot + 31, escape_html(unite))
    )
    return "".join(parts)


def _libelle(entree):
    texte = "%s · %s" % (entree["reference"], entree["intitule"])
    if len(texte) > CARACTERES_LIBELLE:
        texte = texte[: CARACTERES_LIBELLE - 1].rstrip(" ,;’'") + "…"
    return texte


def _sucette(entree, y, bornes, serie, unite):
    """Tige fine + pastille : la position porte le montant, pas la longueur."""
    x = _abscisse(entree["montant"], bornes)
    bulle = infobulle(
        entree["intitule"],
        "%s — coût %s" % (montant_lisible(entree["montant"]), entree["nature"]),
        "Mesure %s · %s" % (entree["reference"], unite),
    )
    milieu = y + PAS / 2.0
    return (
        '<g class="chart__mark-group"%s>'
        '<text class="chart__row-label chart__row-label--dense" x="%d" '
        'y="%.1f" text-anchor="end">%s</text>'
        '<line class="chart__stem" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>'
        '<circle class="mark mark--%d" cx="%.1f" cy="%.1f" r="%.1f"/>'
        '<text class="chart__value chart__value--dense" x="%.1f" y="%.1f">'
        "%s</text></g>"
        % (
            bulle, GOUTTIERE - 10, milieu + 4, escape_html(_libelle(entree)),
            GOUTTIERE, milieu, x, milieu,
            serie, x, milieu, RAYON,
            x + 9, milieu + 4, escape_html(montant_lisible(entree["montant"])),
        )
    )


def _reste(entrees, y, bornes, unite):
    """Les mesures au-dela du rang affiche : une plage, jamais une somme."""
    montants = [entree["montant"] for entree in entrees]
    x_bas, x_haut = _abscisse(min(montants), bornes), _abscisse(max(montants), bornes)
    milieu = y + PAS / 2.0
    etendue = escape_html(
        "%s – %s" % (montant_lisible(min(montants)), montant_lisible(max(montants)))
    )
    bulle = infobulle(
        "%d autres mesures chiffrées, non détaillées ici" % len(entrees),
        "Elles s'échelonnent de %s à %s"
        % (montant_lisible(min(montants)), montant_lisible(max(montants))),
        "Inventaire complet sous « Voir les données du graphique » · " + unite,
    )
    return (
        '<g class="chart__mark-group"%s>'
        '<text class="chart__row-label chart__row-label--dense" x="%d" '
        'y="%.1f" text-anchor="end">et %d autres mesures</text>'
        '<rect class="chart__spread" x="%.1f" y="%.1f" width="%.1f" '
        'height="6" rx="3"/>'
        '<text class="chart__value chart__value--dense chart__value--muted" '
        'x="%.1f" y="%.1f">%s</text></g>'
        % (
            bulle, GOUTTIERE - 10, milieu + 4, len(entrees),
            x_bas, milieu - 3, max(x_haut - x_bas, 3.0),
            x_haut + 9, milieu + 4, etendue,
        )
    )


def panneau(entrees, serie, unite, rang_maximum=20):
    """Rend un panneau SVG : les `rang_maximum` plus lourdes, puis le reste."""
    classees = sorted(entrees, key=lambda entree: -entree["montant"])
    detaillees, reste = classees[:rang_maximum], classees[rang_maximum:]
    bornes = _decades([entree["montant"] for entree in classees])
    lignes = len(detaillees) + (1 if reste else 0)
    hauteur_plot = lignes * PAS
    corps = [_axe(bornes, hauteur_plot, unite)]
    for rang, entree in enumerate(detaillees):
        corps.append(_sucette(entree, rang * PAS, bornes, serie, unite))
    if reste:
        corps.append(_reste(reste, len(detaillees) * PAS, bornes, unite))
    return (
        '<svg class="chart__svg" viewBox="0 0 %d %d" role="img" '
        'preserveAspectRatio="xMinYMin meet" aria-label="%s">'
        '<g transform="translate(0,6)">%s</g></svg>'
        % (
            LARGEUR, hauteur_plot + 48,
            escape_html(
                "%d mesures classées par montant décroissant, échelle "
                "logarithmique, unité %s" % (len(classees), unite)
            ),
            "".join(corps),
        )
    )
