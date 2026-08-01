"""D'ou vient le cout d'un chapitre : le detail, mesure par mesure.

Le bloc de chiffres en tete de chaque fiche donne un total agrege. Cette
figure l'ouvre : quelles mesures pesent, lesquelles sont marginales,
lesquelles ne portent aucun chiffre.

Deux panneaux, jamais un seul : un cout recurrent se compte en euros par an,
un cout ponctuel en euros verses une fois. Les deux ne s'additionnent pas, et
un axe unique le suggererait.
"""

from .base import escape_html, figure, legende, table
from .detail_mesures_couverture import bande_couverture
from .detail_mesures_note import note_de_lecture
from .detail_mesures_totaux import CONJOINTS, titre
from .detail_mesures_trace import montant_lisible, panneau
from .mesures_lecture import mesures_chiffrees

SOURCE = (
    "Source : § 4 « Chiffrage consolidé » de l'analyse du chapitre, colonne du "
    "coût net, lue mesure par mesure ; milieu de la fourchette quand l'analyse "
    "en publie une. L'inventaire des mesures vient de la transverse 17 (audit "
    "de couverture), ses colonnes de montants ne sont pas utilisées. Total du "
    "chapitre : tableau récapitulatif de la page « Combien ça coûte »."
)

UNITE_RECURRENTE = "milliards d'euros par an"
UNITE_PONCTUELLE = "milliards d'euros, versés une fois"

# Le chapitre fiscal ne depense pas : ses montants sont des rendements
# attendus. Appeler « cout » le produit d'un impot inverserait le signe.
CHAPITRES_DE_RECETTES = (6,)


def _mot_montant(chapitre):
    return "rendement" if chapitre in CHAPITRES_DE_RECETTES else "coût"


def _selon_nature(entrees, nature):
    return [entree for entree in entrees if entree["nature"] == nature]


def _rang_de_la_moitie(montants):
    """Combien des plus lourdes suffisent a faire la moitie du total."""
    cible, cumul = sum(montants) / 2.0, 0.0
    for rang, montant in enumerate(sorted(montants, reverse=True), start=1):
        cumul += montant
        if cumul >= cible:
            return rang
    return len(montants)


def _pluriel(effectif):
    return "s" if effectif > 1 else ""


def _titre(chapitre, recurrentes, chiffrees, hors_figure):
    """Enonce le resultat. Sous quatre mesures recurrentes, « la moitie du
    cout » ne veut plus rien dire : on enonce alors la couverture."""
    if len(recurrentes) >= 4:
        rang = _rang_de_la_moitie([entree["montant"] for entree in recurrentes])
        return "Chapitre %d — %d mesure%s sur %d %s la moitié du %s récurrent" % (
            chapitre, rang, _pluriel(rang), len(recurrentes),
            "portent" if rang > 1 else "porte", _mot_montant(chapitre),
        )
    return "Chapitre %d — %d mesure%s au %s vérifié, %d chiffrée%s autrement " \
           "ou pas du tout" % (
               chapitre, len(chiffrees), _pluriel(len(chiffrees)),
               _mot_montant(chapitre), hors_figure, _pluriel(hors_figure),
           )


def _lede(chapitre, chiffrees):
    """Promettre des lignes survolables quand il n'y en a aucune serait faux :
    le chapitre 17 n'a pas une seule mesure au cout isolable."""
    nom = escape_html(titre(chapitre))
    if not chiffrees:
        return (
            "Aucune mesure du chapitre « %s » ne porte de %s publié à son seul "
            "nom : l'analyse le chiffre par blocs et par scénarios, jamais "
            "mesure par mesure. La bande ci-dessous est donc tout ce que cette "
            "figure peut montrer honnêtement — la couverture du chapitre, sans "
            "aucun montant individuel." % (nom, _mot_montant(chapitre))
        )
    return (
        "Chaque ligne est une mesure du chapitre « %s » <strong>dont "
        "l'analyse publie le %s à son nom</strong>, placée selon ce %s et "
        "classée de la plus lourde à la plus légère. La bande du haut donne la "
        "couverture du chapitre : ce qui est chiffré mesure par mesure, et ce "
        "qui ne l'est pas. <strong>Survolez une ligne</strong> pour lire "
        "l'intitulé complet de la mesure, sa référence, son montant et sa "
        "nature." % (nom, _mot_montant(chapitre), _mot_montant(chapitre))
    )


def _ligne_table(entree):
    montant = (
        montant_lisible(entree["montant"]) if entree["montant"] is not None else "—"
    )
    return [
        escape_html(entree["intitule"]),
        escape_html(entree["reference"]),
        montant,
        entree["nature"] or "sans chiffrage",
    ]


def _donnees(chapitre, chiffrees, non_confirmees, muettes):
    classees = sorted(chiffrees, key=lambda entree: -entree["montant"])
    lignes = [
        _ligne_table(entree) for entree in classees + non_confirmees + muettes
    ]
    return table(
        ["Mesure", "Référence", "Montant", "Nature"],
        lignes,
        "Les %d mesures du chapitre %d : d'abord celles dont l'analyse publie "
        "le coût à leur nom, puis celles qu'elle chiffre dans un ensemble plus "
        "large, puis celles qu'elle laisse sans montant. Les montants "
        "récurrents sont annuels, les ponctuels versés une fois : les deux "
        "ne s'additionnent pas." % (len(lignes), chapitre),
    )


def _corps(chapitre, recurrentes, ponctuelles, effectifs):
    """Une entree de legende par serie reellement dessinee : une puce sans
    marque dans la figure fait chercher au lecteur ce qui n'existe pas."""
    mot = _mot_montant(chapitre).capitalize()
    entrees = [
        ("mark--1", "%s récurrent, par an" % mot, recurrentes),
        ("mark--2", "%s ponctuel, une fois" % mot, ponctuelles),
        ("mark--sans-chiffrage", "Sans coût propre publié", effectifs[2][2]),
    ]
    parts = [
        bande_couverture(effectifs),
        legende([(classe, libelle) for classe, libelle, presents in entrees
                 if presents]),
    ]
    if recurrentes:
        parts.append(
            '<p class="chart__facet-title">%s récurrent, en milliards '
            "d'euros par an</p>" % mot
        )
        parts.append(panneau(recurrentes, 1, UNITE_RECURRENTE))
    if ponctuelles:
        parts.append(
            '<p class="chart__facet-title">%s ponctuel, en milliards '
            "d'euros versés une seule fois</p>" % mot
        )
        parts.append(panneau(ponctuelles, 2, UNITE_PONCTUELLE))
    return "".join(parts)


def detail_mesures(numero="1"):
    """`::: graphique detail-mesures 5` — le detail du chapitre 5."""
    chapitre = int(str(numero).strip())
    retenues, toutes_non_confirmees, toutes_muettes = mesures_chiffrees()
    chiffrees = [e for e in retenues if e["chapitre"] == chapitre]
    non_confirmees = [
        e for e in toutes_non_confirmees if e["chapitre"] == chapitre
    ]
    muettes = [e for e in toutes_muettes if e["chapitre"] == chapitre]
    if not chiffrees and not muettes and not non_confirmees:
        return ""

    recurrentes = _selon_nature(chiffrees, "récurrent")
    ponctuelles = _selon_nature(chiffrees, "ponctuel")
    # Les chapitres 12 et 13 partagent un total publie unique : comparer le
    # seul chapitre 12 a l'enveloppe des deux inventerait un ecart de 51 Md€.
    perimetre = CONJOINTS if chapitre in CONJOINTS else (chapitre,)
    groupes = {
        "chiffrees": chiffrees,
        "recurrentes": recurrentes,
        "ponctuelles": ponctuelles,
        "muettes": muettes,
        "non_confirmees": non_confirmees,
        "perimetre": _selon_nature(
            [e for e in retenues if e["chapitre"] in perimetre], "récurrent"
        ),
    }
    mot = _mot_montant(chapitre)
    effectifs = [
        ("mark--1", "Chiffrées, %s récurrent" % mot, len(recurrentes)),
        ("mark--2", "Chiffrées, %s ponctuel" % mot, len(ponctuelles)),
        ("chart__hatch", "Sans coût propre publié",
         len(muettes) + len(non_confirmees)),
    ]
    return figure(
        "detail-mesures-ch%02d" % chapitre,
        _titre(chapitre, recurrentes, chiffrees,
               len(non_confirmees) + len(muettes)),
        _lede(chapitre, chiffrees),
        _corps(chapitre, recurrentes, ponctuelles, effectifs),
        _donnees(chapitre, chiffrees, non_confirmees, muettes),
        SOURCE,
        note=note_de_lecture(chapitre, groupes),
    )
