"""L'echelle des barres horizontales : cadrage, graduations, gouttiere.

Le zero n'est pas toujours au bord gauche du cadre. Des qu'une valeur passe
sous zero, le plancher de l'echelle descend d'un cran rond et le zero prend
sa place a l'interieur du plot. Une serie entierement positive garde un
plancher a zero, donc exactement le cadrage d'avant.
"""

LARGEUR = 720
MARGE_DROITE = 96
LARGEUR_CARACTERE = 6.4  # approximation a 12px : sert a dimensionner la gouttiere

PAS_JOLIS = (1, 2, 2.5, 5, 10, 20, 25, 50, 100, 200, 250, 500, 1000, 2000)

BANDE_MINI = 8.0  # px : sous cette largeur, la part negative ne se voit plus
BANDE_GRADUEE = 22.0  # px : en deca, la graduation du plancher collerait au zero


def _pas_rond(maximum, cible=6):
    """Le cran de graduation : le premier pas rond qui tient la cible."""
    brut = maximum / float(cible)
    return next((p for p in PAS_JOLIS if p >= brut), PAS_JOLIS[-1])


def graduations(maximum, cible=6):
    """Choisit un pas rond ; la derniere graduation couvre toujours le maximum.

    Sans cette garantie la barre la plus longue depasserait le plafond de
    l'echelle et sortirait du cadre.
    """
    pas = _pas_rond(maximum, cible)
    valeurs, courant = [0], pas
    while courant < maximum - pas * 0.001:
        valeurs.append(courant)
        courant += pas
    valeurs.append(courant)
    return valeurs


def _plancher(besoin, plafond, largeur_plot):
    """Le cran rond sous zero : le plus petit qui couvre la valeur negative
    ET laisse une bande assez large pour qu'on la voie.

    Descendre d'un cran de l'axe positif gaspillerait le cadre — sur un axe a
    600, une valeur a −2,26 reservait cent unites de vide et comprimait toutes
    les autres barres. S'arreter au strict necessaire la rendrait invisible.
    Le plus petit cran qui tienne les deux contraintes fait l'affaire.
    """
    for cran in PAS_JOLIS:
        assez_large = largeur_plot * cran / (plafond + cran) >= BANDE_MINI
        if cran >= besoin and assez_large:
            return -cran
    return -max(besoin, PAS_JOLIS[-1])


def bornes(lignes, maximum, largeur_plot):
    """(plancher, plafond, graduations) de l'echelle, lus sur la serie.

    Le plafond et le pas restent ceux d'avant : une serie entierement
    positive garde un plancher a zero, donc la meme echelle au pixel pres.

    Sous zero, l'axe ne porte qu'un cran, et seulement s'il reste la place de
    l'ecrire sans le coller au zero : la bande negative est etroite par
    construction, elle sert a montrer le franchissement, pas a le mesurer.
    Le montant exact vit au bout de la barre et dans le tableau de donnees.
    """
    haut = maximum or max(ligne.get("haut", ligne["bas"]) for ligne in lignes)
    valeurs = graduations(haut)
    plafond = valeurs[-1]
    plus_basse = min(
        min(ligne["bas"], ligne.get("haut", ligne["bas"])) for ligne in lignes
    )
    if plus_basse >= 0:
        return 0, plafond, valeurs
    plancher = _plancher(-plus_basse, plafond, largeur_plot)
    bande = largeur_plot * -plancher / (plafond - plancher)
    crans = [plancher] if bande >= BANDE_GRADUEE else []
    return plancher, plafond, crans + valeurs


def largeur_gouttiere(lignes):
    """Largeur reservee aux libelles, mesuree sur le plus long d'entre eux.

    Une gouttiere fixe rognait les libelles longs — « Orange » devenait
    « range ». Un libelle n'est jamais tronque : c'est la gouttiere qui cede.
    """
    plus_long = max(len(ligne["libelle"]) for ligne in lignes)
    return int(min(324, max(120, plus_long * LARGEUR_CARACTERE + 18)))


def abscisse(valeur, domaine, gouttiere):
    """Abscisse d'une valeur.

    Le plancher tombe sur le bord gauche du plot, et lui seul : aucun aplat
    n'empiete donc jamais sur la gouttiere des libelles, quel que soit le
    signe des valeurs.
    """
    plancher, plafond = domaine
    largeur_plot = LARGEUR - gouttiere - MARGE_DROITE
    return gouttiere + ((float(valeur) - plancher) / (plafond - plancher)) * largeur_plot
