"""Registre des figures du site.

Une fiche markdown appelle une figure par son identifiant :

    ::: graphique chiffrage-consolide
    :::

Le dessin vit ici, en SVG ecrit a la main, et non dans la fiche : le
convertisseur markdown echappe le HTML brut, et une figure de deux cents
lignes de SVG noierait le texte qu'elle illustre.
"""

from .budget import chiffrage_consolide, cout_par_chapitre, doubles_comptes
from .institutions import calendrier_legislatif, risque_constitutionnel
from .murs import mur_main_doeuvre, niveaux_confiance
from .natures import natures_du_cout, profil_decaissement
from .variantes import variantes_rentables

FIGURES = {
    "chiffrage-consolide": chiffrage_consolide,
    "cout-par-chapitre": cout_par_chapitre,
    "natures-du-cout": natures_du_cout,
    "profil-decaissement": profil_decaissement,
    "niveaux-confiance": niveaux_confiance,
    "doubles-comptes": doubles_comptes,
    "mur-main-doeuvre": mur_main_doeuvre,
    "calendrier-legislatif": calendrier_legislatif,
    "variantes-rentables": variantes_rentables,
    "risque-constitutionnel": risque_constitutionnel,
}


def rendre_figure(identifiant):
    """Rend la figure demandee, ou un encadre lisible si l'identifiant est faux."""
    fabrique = FIGURES.get(identifiant.strip())
    if fabrique is None:
        return (
            '<div class="callout callout--attention"><p class="callout__title">'
            "Figure inconnue</p><p>Aucune figure ne porte l'identifiant "
            "« %s ». Figures disponibles : %s.</p></div>"
            % (identifiant.strip(), ", ".join(sorted(FIGURES)))
        )
    return fabrique()


__all__ = ["FIGURES", "rendre_figure"]
