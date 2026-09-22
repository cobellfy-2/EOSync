"""NCBI GEO - Gene Expression Omnibus (Expressionsdatensaetze).

Docs: https://www.ncbi.nlm.nih.gov/geo/info/download.html
Nutzt dieselben E-utilities wie PubMed, nur db=gds statt db=pubmed.

Deshalb lohnt es sich, den E-utilities-Teil aus pubmed_service.py in eine
gemeinsame Helper-Funktion zu ziehen, sobald du hier ankommst. Erst duplizieren,
dann abstrahieren - in dieser Reihenfolge, nicht andersrum.
"""

from typing import Any

from backend.app.models import SourceName
from backend.services.base import BaseSource

ESEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
ESUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"


class GEOSource(BaseSource):
    name = SourceName.GEO

    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

    async def _fetch(self, gene: str) -> Any:
        """
        TODO (Phase 2):
        1. esearch mit db=gds, term=f"{gene}[Description] AND homo sapiens[Organism]"
        2. esummary mit db=gds, id=... , retmode=json
           -> Titel, Zusammenfassung, Anzahl Samples, GSE-Accession, Plattform

        Achtung: GEO teilt sich das NCBI-Rate-Limit mit PubMed. Wenn beide
        Services parallel feuern, brauchst du EINEN gemeinsamen Rate-Limiter
        fuer den Host eutils.ncbi.nlm.nih.gov - nicht einen pro Service.
        """
        raise NotImplementedError

    def parse(self, raw: Any) -> Any:
        raise NotImplementedError
