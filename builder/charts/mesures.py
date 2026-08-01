"""Les 503 mesures chiffrees, une par point, chapitre par chapitre.

Les montants s'etalent de 1 million a 40 milliards : quatre ordres de
grandeur. Une echelle lineaire ecraserait 90 % des mesures contre l'axe,
d'ou l'echelle logarithmique — chaque graduation vaut dix fois la
precedente. La convention est ecrite sous la figure : tue, elle trompe.

Le survol donne l'intitule, le chapitre, le montant et la nature.
"""

from .base import escape_html, figure, infobulle, legende, nombre, table
from .mesures_lecture import mesures_chiffrees

LARGEUR = 720
GOUTTIERE = 118
MARGE_DROITE = 26
PAS = 26
RAYON = 4.0
PLANCHER = 0.001  # 1 M€ : borne basse de l'echelle logarithmique
PLAFOND = 100.0
DECADES = (0.001, 0.01, 0.1, 1.0, 10.0, 100.0)

TITRES = {
    1: "Institutions", 2: "Propriété", 3: "Entreprise et ville",
    4: "Libertés", 5: "Éducation", 6: "Partage des richesses",
    7: "Solidarité", 8: "Travail", 9: "Production", 10: "Égalité",
    11: "Culture et sport", 12: "Planification", 13: "Bifurcation",
    14: "Biens communs", 15: "Santé", 16: "International",
    17: "Europe", 18: "Nouvelles frontières",
}

SOURCE = (
    "Source : rubrique « c. Chiffrage » de chaque analyse de chapitre, "
    "consolidée par la transverse 17 (audit de couverture). Les montants "
    "font foi dans la fiche du chapitre, pas ici."
)


def _x(valeur):
    """Position logarithmique, bornee au plancher."""
    from math import log10
    borne = max(valeur, PLANCHER)
    part = (log10(borne) - log10(PLANCHER)) / (log10(PLAFOND) - log10(PLANCHER))
    return GOUTTIERE + part * (LARGEUR - GOUTTIERE - MARGE_DROITE)


def _lisible(montant):
    if montant >= 1:
        return "%s Md€" % nombre(montant, 1)
    return "%s M€" % nombre(round(montant * 1000))


def _axe(hauteur):
    traits = []
    for decade in DECADES:
        x = _x(decade)
        libelle = _lisible(decade)
        traits.append(
            '<line class="chart__grid" x1="%.1f" y1="0" x2="%.1f" y2="%d"/>'
            '<text class="chart__tick" x="%.1f" y="%d" text-anchor="middle">'
            "%s</text>" % (x, x, hauteur, x, hauteur + 16, escape_html(libelle))
        )
    return "".join(traits)


def _point(entree, y):
    serie = 1 if entree["nature"] == "récurrent" else 2
    bulle = infobulle(
        entree["intitule"][:120],
        "%s — %s" % (_lisible(entree["montant"]), entree["nature"]),
        "Chapitre %d · mesure %s" % (entree["chapitre"], entree["reference"]),
    )
    return (
        '<circle class="mark mark--%d chart__dot" cx="%.1f" cy="%.1f" r="%.1f"%s/>'
        % (serie, _x(entree["montant"]), y, RAYON, bulle)
    )


def _rangees(retenues):
    corps, y = [], 0
    for chapitre in range(1, 19):
        mesures = [e for e in retenues if e["chapitre"] == chapitre]
        if not mesures:
            continue
        centre = y + PAS / 2.0
        corps.append(
            '<text class="chart__row-label" x="%d" y="%.1f" text-anchor="end">'
            "%s</text>" % (GOUTTIERE - 10, centre + 4, escape_html(TITRES[chapitre]))
        )
        corps.extend(_point(mesure, centre) for mesure in mesures)
        y += PAS
    return "".join(corps), y


def mesures_par_montant():
    retenues, ecartees, muettes = mesures_chiffrees()
    if not retenues:
        return ""

    rangees, hauteur = _rangees(retenues)
    svg = (
        '<svg class="chart__svg" viewBox="0 0 %d %d" role="img" '
        'preserveAspectRatio="xMinYMin meet" aria-label="%s">'
        '<g transform="translate(0,10)">%s%s</g></svg>'
        % (
            LARGEUR,
            hauteur + 44,
            escape_html(
                "Nuage de %d mesures, échelle logarithmique en euros par an"
                % len(retenues)
            ),
            _axe(hauteur),
            rangees,
        )
    )

    grosses = sorted(retenues, key=lambda e: -e["montant"])[:15]
    donnees = table(
        ["Mesure", "Chapitre", "Montant", "Nature"],
        [
            [escape_html(e["intitule"][:90]), str(e["chapitre"]),
             _lisible(e["montant"]), e["nature"]]
            for e in grosses
        ],
        "Les quinze mesures les plus coûteuses. L'inventaire complet des %d "
        "mesures chiffrées est dans le dossier." % len(retenues),
    )

    note = (
        "Échelle logarithmique : chaque graduation vaut dix fois la "
        "précédente. %d mesures portent un montant exploitable ; %d n'en "
        "portent aucun dans le dossier, et %d ont été écartées parce que la "
        "valeur publiée était une grandeur de contexte — le budget d'un "
        "secteur, un stock — et non le coût de la mesure."
        % (len(retenues), muettes, len(ecartees))
    )

    return figure(
        "mesures-par-montant",
        "Neuf mesures sur dix pèsent moins d'un milliard : le coût vient d'une poignée",
        "Chaque point est une mesure du programme, placée selon son coût "
        "annuel. La médiane est à 250 millions d'euros, mais l'échelle "
        "s'étend sur quatre ordres de grandeur : quelques mesures des "
        "chapitres travail, solidarité et bifurcation écologique portent "
        "l'essentiel du total. Survolez un point pour lire la mesure.",
        legende([
            ("mark--1", "Coût récurrent, par an"),
            ("mark--2", "Coût ponctuel, une fois"),
        ]) + svg,
        donnees,
        SOURCE,
        note=note,
    )
