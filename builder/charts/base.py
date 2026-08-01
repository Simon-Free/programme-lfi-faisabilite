"""Enveloppe commune a toutes les figures : titre, lecture, table, source.

Aucune couleur n'est ecrite ici. Les marques portent une classe
`mark--N` (serie categorielle) ou `mark--<statut>` (statut reserve) ;
les valeurs vivent dans `assets/charts.css`, qui lit les jetons de la charte.
"""

from ..markdown.inline import escape_html

ESPACE_FIN = " "  # espace fine insecable : separateur de milliers francais


def nombre(valeur, decimales=None):
    """Formate un nombre a la francaise : virgule decimale, milliers espaces.

    La precision suit la donnee : arrondir 0,29 a 0,3 contredisait le tableau
    de la fiche imprime juste en dessous du graphique.
    """
    if valeur is None:
        return "—"
    if decimales is None:
        reel = float(valeur)
        decimales = 0 if reel == int(reel) else (1 if reel * 10 == int(reel * 10) else 2)
    texte = ("%%.%df" % decimales) % valeur
    entier, _, reste = texte.partition(".")
    signe, chiffres = ("−", entier[1:]) if entier.startswith("-") else ("", entier)
    groupes = []
    while len(chiffres) > 3:
        groupes.insert(0, chiffres[-3:])
        chiffres = chiffres[:-3]
    groupes.insert(0, chiffres)
    rendu = signe + ESPACE_FIN.join(groupes)
    return rendu + ("," + reste if reste else "")


def fourchette(bas, haut, unite=""):
    """« 41,4 a 92,8 Md€/an », ou la valeur seule si les bornes coincident."""
    if haut is None or bas == haut:
        return nombre(bas) + unite
    return "%s à %s%s" % (nombre(bas), nombre(haut), unite)


def infobulle(*lignes):
    """Attributs d'une marque survolable. La premiere ligne est le titre."""
    contenu = "\n".join(ligne for ligne in lignes if ligne)
    return ' tabindex="0" data-bulle="%s"' % escape_html(contenu).replace(
        "\n", "&#10;"
    )


def _cellules(ligne, entete=False):
    balise = "th" if entete else "td"
    rendu = []
    for index, cellule in enumerate(ligne):
        portee = ' scope="row"' if entete is False and index == 0 else ""
        classe = ' class="col-right"' if index and not entete else ""
        rendu.append(
            "<%s%s%s>%s</%s>" % (balise, portee, classe, cellule, balise)
        )
    return "<tr>%s</tr>" % "".join(rendu)


def table(colonnes, lignes, resume):
    """Le double textuel de la figure : exigence d'accessibilite, pas une option."""
    corps = "".join(_cellules(ligne) for ligne in lignes)
    return (
        '<details class="chart__data"><summary>Voir les données du graphique'
        "</summary><div class=\"table-wrap\"><table><caption>%s</caption>"
        "<thead>%s</thead><tbody>%s</tbody></table></div></details>"
        % (escape_html(resume), _cellules(colonnes, entete=True), corps)
    )


def legende(entrees):
    """entrees : couples (classe de marque, libelle). Absente si une seule serie."""
    if len(entrees) < 2:
        return ""
    items = "".join(
        '<li><span class="chart__puce %s" aria-hidden="true"></span>%s</li>'
        % (classe, escape_html(libelle))
        for classe, libelle in entrees
    )
    return '<ul class="chart__legend">%s</ul>' % items


def figure(cle, titre, lecture, corps, donnees, source, note=""):
    """Assemble une figure autonome.

    `titre` enonce le resultat, jamais le sujet. `lecture` est la phrase
    destinee au lecteur non expert. `donnees` est la table de substitution.
    """
    identifiant = "fig-%s" % cle
    return (
        '<figure class="chart" id="%s" role="group" aria-labelledby="%s-t">'
        '<div class="chart__head"><h3 class="chart__title" id="%s-t">%s</h3>'
        '<p class="chart__read">%s</p></div>'
        "%s"
        '<div class="chart__plot">%s</div>'
        "%s%s"
        '<figcaption class="chart__source">%s</figcaption>'
        "</figure>"
        % (
            identifiant,
            identifiant,
            identifiant,
            escape_html(titre),
            lecture,
            note and '<p class="chart__note">%s</p>' % note,
            corps,
            donnees,
            "",
            source,
        )
    )
