"""Ensembl REST API - Genannotation, Orthologe, Sequenzen.

Docs: https://rest.ensembl.org
Kein Key noetig. Limit: 15 req/s, und Ensembl SAGT dir, wenn du drueber bist:
Bei 429 kommt ein Retry-After-Header zurueck.
"""

from typing import Any

from backend.app.models import SourceName
from backend.services.base import BaseSource

BASE = "https://rest.ensembl.org"


class EnsemblSource(BaseSource):
    name = SourceName.ENSEMBL
    base_url = BASE

    async def _fetch(self, gene: str) -> Any:
        """
        TODO (Phase 2):
        GET {BASE}/lookup/symbol/homo_sapiens/{gene}
          headers: {"Content-Type": "application/json"}
          params:  {"expand": 1}   -> liefert auch Transkripte mit

        Liefert u.a.: id (ENSG...), seq_region_name, start, end, strand,
        biotype, description, Transcript[]

        TODO (Bonus): Bei 429 den Retry-After-Header auswerten und genau so
        lange warten, statt blind zu wiederholen. Das ist der Unterschied
        zwischen "funktioniert meistens" und produktionsreif.
        """
        raise NotImplementedError

    def parse(self, raw: Any) -> Any:
        """TODO: Auf die Felder reduzieren, die dein Frontend wirklich zeigt."""
        raise NotImplementedError
