"""PubMed via NCBI E-utilities.

Docs: https://www.ncbi.nlm.nih.gov/books/NBK25501/

Warum PubMed zuerst? Es ist die lehrreichste Quelle:
- zwei Requests noetig (esearch -> efetch), also echte API-Verkettung
- XML statt JSON, also musst du wirklich parsen
- hartes Rate-Limit, also brauchst du den Rate-Limiter
"""

from typing import Any

from backend.app.models import Article, SourceName
from backend.services.base import BaseSource

ESEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
EFETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"


class PubMedSource(BaseSource):
    name = SourceName.PUBMED
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

    async def _fetch(self, gene: str) -> Any:
        """
        TODO (Phase 2), Schritt fuer Schritt:

        1. esearch: GET ESEARCH_URL mit params
           db=pubmed, term=f"{gene}[Gene Name]", retmax=20,
           retmode=json, sort=relevance
           (+ api_key, tool, email aus get_settings(), wenn gesetzt)
           -> liefert esearchresult.idlist = Liste von PMIDs + count (Gesamttreffer)

        2. Wenn idlist leer ist: frueh zurueck mit leerer Liste. Kein zweiter Call.

        3. efetch: GET EFETCH_URL mit db=pubmed, id=",".join(pmids),
           retmode=xml  -> Volltext-Metadaten inkl. Abstract

        4. XML parsen (xml.etree.ElementTree reicht) und an self.parse geben.

        Stolperfalle: efetch kann KEIN JSON fuer PubMed-Abstracts. Du musst XML
        anfassen - genau das ist der Teil, den man in echten Projekten koennen muss.
        """
        raise NotImplementedError

    def parse(self, raw: Any) -> list[Article]:
        """XML -> list[Article].

        Die interessanten XML-Pfade:
          .//PubmedArticle
          .//PMID
          .//ArticleTitle
          .//Abstract/AbstractText        (kann mehrere Absaetze haben!)
          .//Author/LastName + ForeName
          .//Journal/Title
          .//PubDate/Year                 (fehlt manchmal -> MedlineDate)

        TODO: Denk an fehlende Felder. Etwa 15% der Eintraege haben keinen
        Abstract, manche keine Jahreszahl. None ist ok, ein Crash nicht.
        """
        raise NotImplementedError
