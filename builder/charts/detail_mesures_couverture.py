"""La bande de couverture : combien de mesures portent un chiffre, combien non.

Sans elle, la figure ne montrerait que les mesures chiffrees et laisserait
croire a un inventaire complet. Les mesures sans montant ne sont donc pas
omises : elles occupent leur part de la bande, hachurees — une hachure ne se
lit pas comme une valeur, ce qui est exactement le propos.
"""

from .base import escape_html, infobulle

LARGEUR = 720
HAUTEUR = 22
ECART = 2  # respiration a la couleur de la surface entre deux aplats
LARGEUR_MINIMALE_ETIQUETTE = 74

HACHURE = (
    '<defs><pattern id="hachure-sans-chiffrage" width="7" height="7" '
    'patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
    '<rect width="7" height="7" class="chart__hatch-bg"/>'
    '<line x1="0" y1="0" x2="0" y2="7" class="chart__hatch-line"/>'
    "</pattern></defs>"
)


def _segment(x, largeur, remplissage, libelle, effectif, total):
    part = 100.0 * effectif / total
    bulle = infobulle(
        libelle,
        "%d mesures sur %d" % (effectif, total),
        "soit %.0f %% des mesures du chapitre" % part,
    )
    etiquette = ""
    if largeur >= LARGEUR_MINIMALE_ETIQUETTE:
        etiquette = (
            '<text class="chart__seg-value" x="%.1f" y="%d">%d</text>'
            % (x + largeur / 2.0, HAUTEUR + 15, effectif)
        )
    return (
        '<g class="chart__mark-group"%s><rect class="%s" x="%.1f" y="0" '
        'width="%.1f" height="%d" rx="3"/>%s</g>'
        % (bulle, remplissage, x, max(largeur, 1.5), HAUTEUR, etiquette)
    )


def bande_couverture(effectifs):
    """`effectifs` : liste de (classe de marque, libelle, effectif).

    Les effectifs nuls disparaissent : un segment de largeur zero n'est pas
    une information, c'est un artefact de trace.
    """
    presents = [entree for entree in effectifs if entree[2] > 0]
    total = sum(entree[2] for entree in presents)
    if not total:
        return ""
    utile = LARGEUR - ECART * max(len(presents) - 1, 0)
    corps, x = [], 0.0
    for classe, libelle, effectif in presents:
        largeur = utile * effectif / float(total)
        corps.append(_segment(x, largeur, classe, libelle, effectif, total))
        x += largeur + ECART
    return (
        '<svg class="chart__svg chart__svg--bande" viewBox="0 0 %d %d" '
        'role="img" preserveAspectRatio="xMinYMin meet" aria-label="%s">%s%s</svg>'
        % (
            LARGEUR, HAUTEUR + 20,
            escape_html(
                "Répartition des %d mesures du chapitre : %s"
                % (
                    total,
                    ", ".join(
                        "%d %s" % (effectif, libelle.lower())
                        for _, libelle, effectif in presents
                    ),
                )
            ),
            HACHURE,
            "".join(corps),
        )
    )
