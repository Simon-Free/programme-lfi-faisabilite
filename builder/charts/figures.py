"""Formes qui ne sont pas des graphiques : chiffre-heros, jauge, sequence.

Quand l'histoire est un seul nombre, le nombre EST le graphique : une barre
unique ou un camembert a deux parts seraient des dessins pour rien.
"""

from ..markdown.inline import escape_html
from .base import infobulle, nombre


def heros(valeur, libelle, precision=""):
    """Le chiffre que la figure veut faire retenir. Un seul par figure."""
    return (
        '<div class="chart__hero"><p class="chart__hero-value">%s</p>'
        '<p class="chart__hero-label">%s</p>%s</div>'
        % (
            escape_html(valeur),
            escape_html(libelle),
            precision
            and '<p class="chart__hero-note">%s</p>' % escape_html(precision),
        )
    )


def jauge(part, libelle, detail):
    """Jauge de couverture : la portion remplie contre la portion manquante.

    La piste non remplie est un gris de surface, jamais une seconde couleur
    de serie : il n'y a qu'une grandeur, sa part atteinte.
    """
    largeur = max(min(float(part), 100.0), 0.6)
    return (
        '<div class="chart__meter"%s>'
        '<div class="chart__meter-track">'
        '<div class="chart__meter-fill" style="width:%.2f%%"></div></div>'
        '<p class="chart__meter-label"><strong>%s</strong> %s</p></div>'
        % (
            infobulle(libelle, detail),
            largeur,
            escape_html(libelle),
            escape_html(detail),
        )
    )


def etapes(items):
    """Chemin critique : une sequence ordonnee, numerotee, pas un graphique.

    items : (titre, duree, precision).
    """
    cellules = []
    for index, (titre, duree, precision) in enumerate(items, start=1):
        cellules.append(
            '<li class="chart__step"><p class="chart__step-rank">%d</p>'
            '<p class="chart__step-title">%s</p>'
            '<p class="chart__step-time">%s</p>'
            '<p class="chart__step-note">%s</p></li>'
            % (index, escape_html(titre), escape_html(duree),
               escape_html(precision))
        )
    return '<ol class="chart__steps">%s</ol>' % "".join(cellules)


def _plaque(entree):
    valeur, libelle, detail, statut = entree
    return (
        '<li class="chart__tile chart__tile--%s"%s>'
        '<span class="chart__tile-value">%s</span>'
        '<span class="chart__tile-label">%s</span>'
        '<span class="chart__tile-note">%s</span></li>'
        % (
            statut,
            infobulle(libelle, detail),
            escape_html(valeur),
            escape_html(libelle),
            escape_html(detail),
        )
    )


def plaques(entrees):
    """Rangee de tuiles de statut : valeur, libelle, note, couleur reservee."""
    return '<ul class="chart__tiles">%s</ul>' % "".join(
        _plaque(entree) for entree in entrees
    )


def ratio(gauche, droite, unite=""):
    """Confrontation de deux grandeurs de meme unite, cote a cote."""
    (val_g, lib_g), (val_d, lib_d) = gauche, droite
    facteur = val_g / float(val_d) if val_d else 0
    return (
        '<div class="chart__ratio">'
        '<div class="chart__ratio-side"><p class="chart__ratio-value">%s</p>'
        '<p class="chart__ratio-label">%s</p></div>'
        '<p class="chart__ratio-sign">contre</p>'
        '<div class="chart__ratio-side chart__ratio-side--faible">'
        '<p class="chart__ratio-value">%s</p>'
        '<p class="chart__ratio-label">%s</p></div>'
        '<p class="chart__ratio-factor">facteur %s</p></div>'
        % (
            escape_html(nombre(val_g) + unite),
            escape_html(lib_g),
            escape_html(nombre(val_d) + unite),
            escape_html(lib_d),
            nombre(facteur, 1),
        )
    )
