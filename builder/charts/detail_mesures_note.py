"""La note sous la figure : ce que le lecteur regarde, et ce qu'il ne voit pas.

Trois choses s'y disent, et aucune ne peut manquer : la convention d'echelle ;
combien de mesures du chapitre portent un cout verifie, combien sont chiffrees
dans un ensemble plus large et combien ne portent aucun montant ; enfin l'ecart
entre la somme des mesures affichees et le total publie par la fiche.

Cet ecart penche desormais presque toujours du meme cote — la figure ne montre
que les couts attribues a une mesure nommee, quand le total du chapitre couvre
aussi ses blocs et ses enveloppes. Le taire laisserait croire a une erreur
d'addition ; on l'ecrit donc, chiffre, et on dit pourquoi.
"""

from .base import nombre
from .detail_mesures_totaux import CONJOINTS, total_publie

TROP_HAUT = (
    "<strong>Ce n'est pas une erreur d'addition</strong> : le total du "
    "chapitre retire les doubles comptes avec les autres chapitres, ne retient "
    "qu'une variante quand deux s'excluent, et transfère certaines lignes "
    "ailleurs. La somme des mesures, elle, ne retire rien."
)
TROP_BAS = (
    "<strong>Ce n'est pas une erreur d'addition</strong> : le total du "
    "chapitre couvre aussi les mesures que cette figure n'affiche pas — celles "
    "que l'analyse chiffre par blocs ou par enveloppes, sans leur attribuer de "
    "part propre. La somme ci-dessus ne porte que les coûts vérifiés mesure "
    "par mesure ; elle est donc, par construction, incomplète."
)


def _pluriel(effectif):
    return "s" if effectif > 1 else ""


def _perimetre_dit(chapitre):
    if chapitre in CONJOINTS:
        return "les chapitres %s réunis" % " et ".join(str(n) for n in CONJOINTS)
    return "le chapitre"


def phrase_ecart(chapitre, recurrentes_du_perimetre):
    """Compare la somme des mesures recurrentes au total publie de la fiche."""
    central, precision = total_publie(chapitre)
    queue = " — %s" % precision if precision else ""
    if central is None:
        return (
            "Le chapitre ne publie pas de total de dépense%s : la somme de ses "
            "mesures ne se compare à rien." % queue
        )
    if not recurrentes_du_perimetre:
        return (
            "Aucune mesure récurrente chiffrée ici, alors que la fiche publie "
            "%s Md€/an%s." % (nombre(central), queue)
        )
    somme = sum(entree["montant"] for entree in recurrentes_du_perimetre)
    ecart = somme - central
    debut = (
        "La somme des %d mesures récurrentes affichées vaut"
        % len(recurrentes_du_perimetre)
        if len(recurrentes_du_perimetre) > 1
        else "L'unique mesure récurrente affichée vaut"
    )
    return (
        "%s %s Md€/an, quand la fiche publie %s Md€/an pour %s%s : la somme "
        "des mesures %s de %s Md€/an. %s"
        % (
            debut, nombre(somme, 2), nombre(central),
            _perimetre_dit(chapitre), queue,
            "dépasse ce total" if ecart >= 0 else "reste en dessous",
            nombre(abs(ecart), 2),
            TROP_HAUT if ecart >= 0 else TROP_BAS,
        )
    )


def _non_confirmees(effectif):
    """Ce que le lecteur ne voit pas, et la raison exacte pour laquelle."""
    if not effectif:
        return ""
    return (
        " <strong>%d autre%s chiffrée%s dans un ensemble plus large</strong> — "
        "un bloc thématique, une enveloppe, un total que l'analyse ne ventile "
        "pas — et leur part propre ne s'en déduit pas : elles sont hachurées "
        "plutôt que placées sur l'échelle." % (
            effectif,
            "s sont" if effectif > 1 else " est",
            _pluriel(effectif),
        )
    )


def note_de_lecture(chapitre, groupes):
    """Convention d'echelle, ce qui est affiche, ce qui ne l'est pas, ecart."""
    chiffrees, muettes = groupes["chiffrees"], groupes["muettes"]
    non_confirmees = groupes["non_confirmees"]
    total = len(chiffrees) + len(muettes) + len(non_confirmees)
    if not chiffrees:
        return (
            "Sur les %d mesures du chapitre, <strong>aucune ne porte de coût "
            "publié à son seul nom</strong> : %d sont chiffrées dans un "
            "ensemble plus large — un bloc, une enveloppe, un scénario — et %d "
            "ne portent aucun montant. Il n'y a donc pas d'échelle ici, et "
            "aucune somme n'est proposée : la bande ci-dessus est la seule "
            "chose que le dossier permet d'affirmer mesure par mesure. %s"
            % (total, len(non_confirmees), len(muettes),
               phrase_ecart(chapitre, groupes["perimetre"]))
        )
    return (
        "<strong>Échelle logarithmique</strong> : chaque graduation vaut dix "
        "fois la précédente, sans quoi les mesures à quelques millions "
        "seraient collées à l'axe. <strong>Un montant récurrent et un montant "
        "ponctuel ne s'additionnent jamais</strong> : ils occupent deux "
        "panneaux séparés. Sur les %d mesures du chapitre, <strong>%d "
        "porte%s un coût vérifié</strong>, publié à son nom par le § 4 de "
        "l'analyse (%d récurrente%s, %d ponctuelle%s).%s <strong>%d ne "
        "porte%s aucun montant</strong> nulle part dans le dossier. %s"
        % (
            total, len(chiffrees), "nt" if len(chiffrees) > 1 else "",
            len(groupes["recurrentes"]), _pluriel(len(groupes["recurrentes"])),
            len(groupes["ponctuelles"]), _pluriel(len(groupes["ponctuelles"])),
            _non_confirmees(len(non_confirmees)),
            len(muettes), "nt" if len(muettes) > 1 else "",
            phrase_ecart(chapitre, groupes["perimetre"]),
        )
    )
