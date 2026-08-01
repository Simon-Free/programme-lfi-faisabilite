"""Barres horizontales a fourchette, tracees a la main en SVG.

Une fourchette n'est pas une barre : la valeur centrale du dossier est le
milieu de l'intervalle « et rien d'autre ». On dessine donc un socle plein
jusqu'a la borne basse, puis une continuation claire jusqu'a la borne haute,
separes par un intervalle de 2px a la couleur de la surface.
"""

from ..markdown.inline import escape_html
from .base import infobulle, nombre

LARGEUR = 720
MARGE_DROITE = 96
HAUTEUR_BARRE = 18
PAS = 31
BANDE_AXE = 46  # graduations + ligne d'unite : la bande doit tenir dans le cadre
LARGEUR_CARACTERE = 6.4  # approximation a 12px : sert a dimensionner la gouttiere

PAS_JOLIS = (1, 2, 2.5, 5, 10, 20, 25, 50, 100, 200, 250, 500, 1000, 2000)


def graduations(maximum, cible=6):
    """Choisit un pas rond ; la derniere graduation couvre toujours le maximum.

    Sans cette garantie la barre la plus longue depasserait le plafond de
    l'echelle et sortirait du cadre.
    """
    brut = maximum / float(cible)
    pas = next((p for p in PAS_JOLIS if p >= brut), PAS_JOLIS[-1])
    valeurs, courant = [0], pas
    while courant < maximum - pas * 0.001:
        valeurs.append(courant)
        courant += pas
    valeurs.append(courant)
    return valeurs


def _gouttiere(lignes):
    """Largeur reservee aux libelles, mesuree sur le plus long d'entre eux.

    Une gouttiere fixe rognait les libelles longs — « Orange » devenait
    « range ». Un libelle n'est jamais tronque : c'est la gouttiere qui cede.
    """
    plus_long = max(len(ligne["libelle"]) for ligne in lignes)
    return int(min(324, max(120, plus_long * LARGEUR_CARACTERE + 18)))


def _echelle(valeur, maximum, gouttiere):
    largeur_plot = LARGEUR - gouttiere - MARGE_DROITE
    return gouttiere + (float(valeur) / maximum) * largeur_plot


def _axe(maximum, hauteur_plot, unite, gouttiere):
    parts = []
    for valeur in graduations(maximum):
        x = _echelle(valeur, maximum, gouttiere)
        parts.append(
            '<line class="chart__grid" x1="%.1f" y1="0" x2="%.1f" y2="%d"/>'
            % (x, x, hauteur_plot)
        )
        parts.append(
            '<text class="chart__tick" x="%.1f" y="%d">%s</text>'
            % (x, hauteur_plot + 18, nombre(valeur))
        )
    # L'unite vit sous les graduations : posee au bout de l'axe, elle se
    # collait a la derniere valeur (« 600Md€/an »).
    milieu = (gouttiere + LARGEUR - MARGE_DROITE) / 2.0
    parts.append(
        '<text class="chart__axis-unit" x="%.1f" y="%d">%s</text>'
        % (milieu, hauteur_plot + 34, escape_html(unite))
    )
    return "".join(parts)


def _etiquette(libelle, y, gouttiere):
    """Libelle de ligne, aligne a droite contre le plot. Jamais la couleur data."""
    return (
        '<text class="chart__row-label" x="%d" y="%.1f" text-anchor="end">%s</text>'
        % (gouttiere - 10, y + HAUTEUR_BARRE * 0.5 + 5, escape_html(libelle))
    )


def _valeur_lisible(bas, haut):
    return nombre(bas) if bas == haut else "%s–%s" % (nombre(bas), nombre(haut))


def _barre(ligne, y, maximum, unite, gouttiere):
    """Socle plein (borne basse) + continuation claire (jusqu'a la haute)."""
    serie = ligne.get("serie", 1)
    bas, haut = ligne["bas"], ligne.get("haut", ligne["bas"])
    x0 = _echelle(0, maximum, gouttiere)
    x_bas = _echelle(bas, maximum, gouttiere)
    x_haut = _echelle(haut, maximum, gouttiere)
    bulle = infobulle(
        ligne["libelle"],
        "%s %s" % (_valeur_lisible(bas, haut), unite.strip()),
        ligne.get("note", ""),
    )
    socle = (
        '<rect class="mark mark--%s" x="%.1f" y="%.1f" width="%.1f" '
        'height="%d" rx="3"/>' % (serie, x0, y, max(x_bas - x0, 1.5), HAUTEUR_BARRE)
    )
    etendue = ""
    if x_haut - x_bas > 2.5:
        etendue = (
            '<rect class="mark mark--%s chart__range" x="%.1f" y="%.1f" '
            'width="%.1f" height="%d" rx="3"/>'
            % (serie, x_bas + 2, y, x_haut - x_bas - 2, HAUTEUR_BARRE)
        )
    texte = (
        '<text class="chart__value" x="%.1f" y="%.1f">%s</text>'
        % (x_haut + 8, y + HAUTEUR_BARRE * 0.5 + 5, _valeur_lisible(bas, haut))
    )
    return '<g class="chart__mark-group"%s>%s%s%s</g>' % (
        bulle,
        socle,
        etendue,
        texte,
    )


def barres(lignes, unite="Md€/an", maximum=None, numerote=False):
    """Rend un jeu de barres horizontales a fourchette dans un SVG autonome."""
    plafond = maximum or max(
        ligne.get("haut", ligne["bas"]) for ligne in lignes
    )
    plafond = graduations(plafond)[-1]
    gouttiere = _gouttiere(lignes)
    hauteur_plot = len(lignes) * PAS
    hauteur = hauteur_plot + BANDE_AXE + 8
    corps = [_axe(plafond, hauteur_plot, unite, gouttiere)]
    for index, ligne in enumerate(lignes):
        y = index * PAS + (PAS - HAUTEUR_BARRE) / 2.0
        corps.append(_etiquette(ligne["libelle"], y, gouttiere))
        corps.append(_barre(ligne, y, plafond, unite, gouttiere))
    return (
        '<svg class="chart__svg" viewBox="0 0 %d %d" role="img" '
        'preserveAspectRatio="xMinYMin meet" aria-label="%s">'
        '<g transform="translate(0,8)">%s</g></svg>'
        % (
            LARGEUR,
            hauteur,
            escape_html("Barres horizontales, unité %s" % unite),
            "".join(corps),
        )
    )
