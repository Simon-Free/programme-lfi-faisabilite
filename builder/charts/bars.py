"""Barres horizontales a fourchette, tracees a la main en SVG.

Une fourchette n'est pas une barre : la valeur centrale du dossier est le
milieu de l'intervalle « et rien d'autre ». On dessine donc un socle plein
jusqu'a la borne la plus proche du zero, puis une continuation claire jusqu'a
la borne lointaine, separes par un intervalle de 2px a la couleur de la
surface.

Une valeur negative se dessine a gauche du zero — pas du bord du cadre. Le
cadrage vit dans `bars_echelle`; ici, une part sous zero porte une couleur de
statut reservee et un repere marque le zero : un signe qui s'inverse n'est
pas une petite valeur, c'est un renversement de sens. Une serie entierement
positive garde exactement le trace d'avant.
"""

from ..markdown.inline import escape_html
from .bars_echelle import LARGEUR, MARGE_DROITE, abscisse, bornes, largeur_gouttiere
from .base import infobulle, nombre

HAUTEUR_BARRE = 18
PAS = 31
BANDE_AXE = 46  # graduations + ligne d'unite : la bande doit tenir dans le cadre
ECART = 2.0  # gouttiere de surface entre deux aplats qui se touchent
MINI_VISIBLE = 2.5  # px : une moitie de fourchette ne tombe jamais a rien
CLASSE_NEGATIVE = "mark--negatif"  # statut reserve, jamais une couleur de serie

MENTION_NEGATIF = (
    '<ul class="chart__legend"><li><span class="chart__puce mark--negatif" '
    'aria-hidden="true"></span>Part située sous le zéro : la valeur s’inverse '
    "de sens. Le signe est aussi porté par l’étiquette chiffrée.</li></ul>"
)


def _axe(domaine, valeurs, hauteur_plot, unite, gouttiere):
    parts = []
    for valeur in valeurs:
        x = abscisse(valeur, domaine, gouttiere)
        parts.append(
            '<line class="chart__grid" x1="%.1f" y1="0" x2="%.1f" y2="%d"/>'
            % (x, x, hauteur_plot)
        )
        parts.append(
            '<text class="chart__tick" x="%.1f" y="%d">%s</text>'
            % (x, hauteur_plot + 18, nombre(valeur))
        )
    if domaine[0] < 0:
        # Repere de zero : sans lui, on ne sait plus d'ou partent les barres.
        zero = abscisse(0, domaine, gouttiere)
        parts.append(
            '<line class="chart__zero" x1="%.1f" y1="-4" x2="%.1f" y2="%d"/>'
            % (zero, zero, hauteur_plot + 4)
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
    if bas == haut:
        return nombre(bas)
    # Un tiret de fourchette colle a un signe moins devient illisible :
    # une fourchette signee s'ecrit donc en toutes lettres.
    liaison = " à " if bas < 0 else "–"
    return "%s%s%s" % (nombre(bas), liaison, nombre(haut))


def _rect(classe, origine, extremite, y, mini=0.0):
    """Aplat oriente : l'origine ne bouge pas, la largeur pousse vers l'extremite."""
    largeur = max(abs(extremite - origine), mini)
    x = origine if extremite >= origine else origine - largeur
    return (
        '<rect class="mark %s" x="%.1f" y="%.1f" width="%.1f" '
        'height="%d" rx="3"/>' % (classe, x, y, largeur, HAUTEUR_BARRE)
    )


def _etendue(classe, depart, arrivee, y):
    """Continuation vers la borne lointaine, detachee de 2px de ce qui precede."""
    if abs(arrivee - depart) <= ECART + 0.5:
        return ""
    sens = 1.0 if arrivee >= depart else -1.0
    return _rect(classe + " chart__range", depart + ECART * sens, arrivee, y)


def _demi(classe, zero, extremite, y):
    """Moitie d'une fourchette qui traverse le zero.

    Pleine et non en continuation : le clair dit « au-dela, c'est incertain »
    par contraste avec le socle qui le precede. Une fourchette a cheval sur le
    zero n'a pas de socle — tout en clair, elle deviendrait la ligne la plus
    pale du panneau alors qu'elle en porte le resultat.

    Detachee du repere de 2px, et jamais reduite a neant : une part sous zero
    de 2,26 sur un axe qui monte a 600 vaut un pixel et disparaitrait — or
    c'est justement elle que la figure doit montrer. Elle garde donc une
    largeur plancher, que la bande sous zero est dimensionnee pour accueillir.
    """
    sens = 1.0 if extremite >= zero else -1.0
    longueur = max(abs(extremite - zero) - ECART, MINI_VISIBLE)
    depart = zero + ECART * sens
    return _rect(classe, depart, depart + sens * longueur, y)


def _marques(bas, haut, y, domaine, gouttiere, serie):
    """Les aplats d'une ligne, selon le signe de ses deux bornes.

    Bornes de meme signe : socle plein du zero jusqu'a la borne proche, puis
    continuation jusqu'a la lointaine. Fourchette qui traverse le zero : rien
    n'est acquis, pas meme le signe — les deux moities sont en continuation,
    coupees au zero, chacune portant la couleur de son signe.
    """
    positive = "mark--%s" % serie
    zero = abscisse(0, domaine, gouttiere)
    x_bas = abscisse(bas, domaine, gouttiere)
    x_haut = abscisse(haut, domaine, gouttiere)
    if bas >= 0:
        return _rect(positive, zero, x_bas, y, 1.5) + _etendue(
            positive, x_bas, x_haut, y
        )
    if haut <= 0:
        return _rect(CLASSE_NEGATIVE, zero, x_haut, y, 1.5) + _etendue(
            CLASSE_NEGATIVE, x_haut, x_bas, y
        )
    return _demi(CLASSE_NEGATIVE, zero, x_bas, y) + _demi(
        positive, zero, x_haut, y
    )


def _texte_valeur(bas, haut, y, domaine, gouttiere):
    """La valeur imprimee, posee apres la borne haute — donc jamais sur un aplat.

    C'est vrai quel que soit le signe : la borne haute est toujours l'extremite
    droite de la barre, et elle est toujours a droite du bord du plot. Aucun
    cas ne renvoie donc l'etiquette dans la gouttiere des libelles.
    """
    return '<text class="chart__value" x="%.1f" y="%.1f">%s</text>' % (
        abscisse(haut, domaine, gouttiere) + 8,
        y + HAUTEUR_BARRE * 0.5 + 5,
        _valeur_lisible(bas, haut),
    )


def _barre(ligne, y, domaine, unite, gouttiere):
    serie = ligne.get("serie", 1)
    bas, haut = ligne["bas"], ligne.get("haut", ligne["bas"])
    bulle = infobulle(
        ligne["libelle"],
        "%s %s" % (_valeur_lisible(bas, haut), unite.strip()),
        ligne.get("note", ""),
    )
    return '<g class="chart__mark-group"%s>%s%s</g>' % (
        bulle,
        _marques(bas, haut, y, domaine, gouttiere, serie),
        _texte_valeur(bas, haut, y, domaine, gouttiere),
    )


def barres(lignes, unite="Md€/an", maximum=None, numerote=False):
    """Rend un jeu de barres horizontales a fourchette dans un SVG autonome."""
    gouttiere = largeur_gouttiere(lignes)
    plancher, plafond, valeurs = bornes(
        lignes, maximum, LARGEUR - gouttiere - MARGE_DROITE
    )
    domaine = (plancher, plafond)
    hauteur_plot = len(lignes) * PAS
    hauteur = hauteur_plot + BANDE_AXE + 8
    corps = [_axe(domaine, valeurs, hauteur_plot, unite, gouttiere)]
    for index, ligne in enumerate(lignes):
        y = index * PAS + (PAS - HAUTEUR_BARRE) / 2.0
        corps.append(_etiquette(ligne["libelle"], y, gouttiere))
        corps.append(_barre(ligne, y, domaine, unite, gouttiere))
    svg = (
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
    # La couleur de statut ne voyage jamais seule : elle est nommee sous la
    # figure ou elle apparait, et nulle part ailleurs.
    return svg + (MENTION_NEGATIF if plancher < 0 else "")
