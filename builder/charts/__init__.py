"""Registre des figures du site.

Une fiche markdown appelle une figure par son identifiant :

    ::: graphique chiffrage-consolide
    :::

Le dessin vit ici, en SVG ecrit a la main, et non dans la fiche : le
convertisseur markdown echappe le HTML brut, et une figure de deux cents
lignes de SVG noierait le texte qu'elle illustre.
"""

from .budget import chiffrage_consolide, cout_par_chapitre, doubles_comptes
from .capital_distribution import patrimoine_distribution
from .capital_gisements import gisements_capital
from .capital_international import fiscalite_capital_comparee
from .capital_rendement import rendement_capital
from .capital_stock import patrimoine_composition
from .decaissement import profil_decaissement
from .echelle_budget import echelle_budget
from .institutions import calendrier_legislatif, risque_constitutionnel
from .mesures import mesures_par_montant
from .murs import mur_main_doeuvre, niveaux_confiance
from .natures import natures_du_cout
from .recettes import couverture_recettes
from .sources import sources_recettes
from .variantes import variantes_rentables

FIGURES = {
    "chiffrage-consolide": chiffrage_consolide,
    "cout-par-chapitre": cout_par_chapitre,
    "natures-du-cout": natures_du_cout,
    "profil-decaissement": profil_decaissement,
    "couverture-recettes": couverture_recettes,
    "sources-recettes": sources_recettes,
    "niveaux-confiance": niveaux_confiance,
    "doubles-comptes": doubles_comptes,
    "mur-main-doeuvre": mur_main_doeuvre,
    "calendrier-legislatif": calendrier_legislatif,
    "variantes-rentables": variantes_rentables,
    "risque-constitutionnel": risque_constitutionnel,
    "patrimoine-composition": patrimoine_composition,
    "patrimoine-distribution": patrimoine_distribution,
    "rendement-capital": rendement_capital,
    "fiscalite-capital-comparee": fiscalite_capital_comparee,
    "gisements-capital": gisements_capital,
    "echelle-budget": echelle_budget,
    "mesures-par-montant": mesures_par_montant,
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
