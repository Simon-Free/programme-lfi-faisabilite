"""Barres empilees horizontales : la part dans un tout, tracees a la main.

Une barre empilee repond a une question que la barre a fourchette ne sait pas
poser : « de quoi ce total est-il fait ? ». Les segments sont separes par un
intervalle de 2px a la couleur de la surface — jamais par une bordure — et un
segment ne porte son etiquette a l'interieur que si elle y tient avec sa marge ;
sinon la valeur descend dans l'infobulle et dans le tableau.
"""

from ..markdown.inline import escape_html
from .base import infobulle, nombre

LARGEUR = 720
MARGE_DROITE = 92  # place du total, pose au bout de la barre
HAUTEUR_BARRE = 26
PAS = 74  # titre + barre + ligne de valeurs, sans que deux rangs se frolent
ECART = 2  # l'intervalle de surface entre deux segments
LARGEUR_CARACTERE = 6.2  # a 11px : sert a decider si une etiquette tient


def _tient(texte, largeur):
    """Une etiquette n'entre dans un segment que si elle y respire."""
    return largeur >= len(texte) * LARGEUR_CARACTERE + 16


def _segment(part, x, largeur, y, unite, total):
    libelle, valeur, serie, note = part
    pourcent = 100.0 * valeur / total if total else 0
    bulle = infobulle(
        libelle,
        "%s %s — %s %% du total" % (nombre(valeur), unite, nombre(pourcent, 1)),
        note,
    )
    rendu = [
        '<rect class="mark mark--%s" x="%.1f" y="%d" width="%.1f" height="%d" '
        'rx="3"/>' % (serie, x, y, max(largeur, 1.5), HAUTEUR_BARRE)
    ]
    texte = nombre(valeur)
    if _tient(texte, largeur):
        rendu.append(
            '<text class="chart__seg-value" x="%.1f" y="%d">%s</text>'
            % (x + largeur / 2.0, y + HAUTEUR_BARRE + 13, texte)
        )
    return '<g class="chart__mark-group"%s>%s</g>' % (bulle, "".join(rendu))


def _ligne(entree, y, maximum, unite, total_visible):
    """Un empilement : son titre au-dessus, ses segments, son total au bout."""
    titre, parts = entree
    total = sum(valeur for _, valeur, _, _ in parts)
    largeur_plot = LARGEUR - MARGE_DROITE
    rendu = [
        '<text class="chart__stack-label" x="0" y="%d">%s</text>'
        % (y, escape_html(titre))
    ]
    y_barre = y + 10
    curseur = 0.0
    for index, part in enumerate(parts):
        largeur = (float(part[1]) / maximum) * largeur_plot
        if index:
            largeur -= ECART
            curseur += ECART
        rendu.append(_segment(part, curseur, largeur, y_barre, unite, total))
        curseur += largeur
    if total_visible:
        rendu.append(
            '<text class="chart__value" x="%.1f" y="%.1f">%s</text>'
            % (curseur + 10, y_barre + HAUTEUR_BARRE * 0.5 + 4, nombre(total))
        )
    return "".join(rendu)


def empilements(entrees, unite="Md€", maximum=None, total_visible=True):
    """entrees : couples (titre, [(libelle, valeur, serie, note), ...]).

    Toutes les barres partagent une meme echelle : c'est ce qui rend deux
    empilements comparables entre eux, et non seulement lisibles chacun.
    """
    plafond = maximum or max(
        sum(valeur for _, valeur, _, _ in parts) for _, parts in entrees
    )
    hauteur = len(entrees) * PAS + 12
    corps = [
        _ligne(entree, index * PAS + 12, plafond, unite, total_visible)
        for index, entree in enumerate(entrees)
    ]
    return (
        '<svg class="chart__svg" viewBox="0 0 %d %d" role="img" '
        'preserveAspectRatio="xMinYMin meet" aria-label="%s">%s</svg>'
        % (
            LARGEUR,
            hauteur,
            escape_html("Barres empilées, unité %s" % unite),
            "".join(corps),
        )
    )


def parts_en_pourcent(entrees, unite="%"):
    """Empilements ramenes a 100 % : la composition, pas la taille.

    Deux populations de tailles tres differentes ne se comparent que ramenees
    a la meme longueur — sinon la plus petite disparait. Le total n'est pas
    ecrit : il vaut 100 sur chaque rang, et le repeter est du bruit.
    """
    return empilements(entrees, unite=unite, maximum=100, total_visible=False)
