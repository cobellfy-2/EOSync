"""UniProt REST API - Proteindaten.

Docs: https://www.uniprot.org/help/api_queries
Kein API-Key noetig, sauberes JSON, grosszuegiges Rate-Limit.
Das ist die einfachste Quelle - gut als zweite Uebung nach PubMed.
"""

from typing import Any

from backend.app.models import SourceName
from backend.services.base import BaseSource

SEARCH_URL = "https://rest.uniprot.org/uniprotkb/search"


class UniProtSource(BaseSource):
    name = SourceName.UNIPROT
    base_url = "https://rest.uniprot.org"

    async def _fetch(self, gene: str) -> Any:
        """
        TODO (Phase 2):
        GET SEARCH_URL mit params:
          query  = f"gene:{gene} AND organism_id:9606 AND reviewed:true"
                   (9606 = Mensch, reviewed:true = nur kuratierte SwissProt-Eintraege)
          fields = "accession,id,protein_name,gene_names,length,cc_function"
          format = "json"
          size   = 5

        Lern-Detail: UniProt paginiert ueber den HTTP-Link-Header, nicht ueber
        ein Feld im Body. Schau dir response.headers.get("link") an - so machen
        es viele professionelle APIs (GitHub genauso).
        """
        raise NotImplementedError

    def parse(self, raw: Any) -> Any:
        """JSON -> eigenes Protein-Modell.

        Interessante Pfade: results[].primaryAccession,
        results[].proteinDescription.recommendedName.fullName.value,
        results[].comments[] mit commentType == "FUNCTION"

        TODO: Ein eigenes Protein-Modell in app/models.py ergaenzen und hier
        befuellen. Roh-JSON durchreichen ist bequem, aber dann haengt dein
        Frontend an UniProts internem Schema.
        """
        raise NotImplementedError
