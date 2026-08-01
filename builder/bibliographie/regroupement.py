"""Regroupement de toutes les recoltes par organisme, pour la page bibliographie.

Un meme document sert souvent dans plusieurs fiches. Il n'est publie qu'une
fois, en listant les fiches ou il sert.
"""

from .entree import url_utilisable
from .lecture import charger_tout, fiches_du_manifeste


class Document:
    """Un document unique, et les fiches du site qui s'appuient dessus."""

    def __init__(self, entree):
        self.entree = entree
        self.usages = []

    @property
    def titre_de_tri(self):
        return (self.entree.get("titre") or "").lower()


class Organisme:
    """Un organisme, presente une seule fois, et ses documents."""

    def __init__(self, nom):
        self.nom = nom
        self.explication = ""
        self.documents = {}

    @property
    def documents_tries(self):
        return sorted(self.documents.values(), key=lambda doc: doc.titre_de_tri)


SANS_ORGANISME = "Sans organisme identifié"
SANS_ORGANISME_EXPLIQUE = (
    "Ces lignes ne renvoient à aucun organisme : le dossier y constate qu’aucune "
    "institution ne produit la donnée, ou qu’aucun précédent n’existe. Elles sont "
    "publiées parce qu’un manque documenté vaut mieux qu’un silence."
)


def nom_d_organisme(entree):
    """Les mentions « Aucun… » ne sont pas des organismes : elles sont regroupees."""
    nom = (entree.get("organisme") or "").strip()
    if not nom or nom.lower().startswith("aucun"):
        return SANS_ORGANISME
    return nom


def _identite(entree):
    """Deux entrees designent le meme document si l'URL, ou le titre, coincide."""
    url = url_utilisable(entree.get("url"))
    if url:
        return url.lower()
    return "%s|%s" % (
        (entree.get("organisme") or "").strip().lower(),
        (entree.get("titre") or entree.get("id") or "").strip().lower(),
    )


def _usage(clef, fiches):
    """Le libelle et l'adresse de la fiche qui utilise la source."""
    if clef in fiches:
        return fiches[clef]
    return clef.replace("_", " "), ""


def rassembler():
    """Retourne (organismes tries par nom, toutes les entrees retenues, etats)."""
    organismes = {}
    fiches = fiches_du_manifeste()
    entrees_totales = []
    partielles = []
    for recolte in charger_tout():
        if recolte.etat != "ok":
            # Un JSON etranger au dossier de sources n'est pas une recolte en
            # retard : seules les clefs qui portent une fiche sont annoncees.
            if recolte.clef in fiches:
                partielles.append(recolte.clef)
            continue
        usage = _usage(recolte.clef, fiches)
        for entree in recolte.entrees:
            entrees_totales.append(entree)
            nom = nom_d_organisme(entree)
            organisme = organismes.setdefault(nom, Organisme(nom))
            if not organisme.explication:
                organisme.explication = (
                    SANS_ORGANISME_EXPLIQUE
                    if nom == SANS_ORGANISME
                    else (entree.get("organisme_explique") or "").strip()
                )
            document = organisme.documents.setdefault(
                _identite(entree), Document(entree)
            )
            if usage not in document.usages:
                document.usages.append(usage)
    # Le groupe des lignes sans organisme ferme la liste : il ne s'intercale pas
    # entre deux institutions a la lettre A.
    tries = sorted(
        organismes.values(),
        key=lambda org: (org.nom == SANS_ORGANISME, org.nom.lower()),
    )
    return tries, entrees_totales, sorted(partielles)
