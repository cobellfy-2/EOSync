"""Orchestriert alle Quellen - das Herzstueck von EOSync.

Lernziel: Sequenziell dauert die Suche 5 x 800ms = 4 Sekunden.
Parallel dauert sie so lange wie die langsamste Quelle. Das ist der ganze
Grund, warum dieses Projekt async ist.
"""

import logging

import httpx

from backend.app.models import SearchResponse, SourceName
from backend.services.base import BaseSource

logger = logging.getLogger(__name__)


class AggregatorService:
    """Faechert einen Gen-Namen auf alle registrierten Quellen auf."""

    def __init__(self, client: httpx.AsyncClient) -> None:
        self.client = client
        self.sources: dict[SourceName, BaseSource] = {}
        # TODO (Phase 3): Registry befuellen, z.B.
        #   self.sources[SourceName.PUBMED] = PubMedSource(client)
        # Importiere die Services erst hier, nicht oben - so bleibt jeder
        # Service unabhaengig testbar.

    async def search(
        self,
        gene: str,
        only: list[SourceName] | None = None,
    ) -> SearchResponse:
        """
        TODO (Phase 3):
        1. Quellen auswaehlen (alle, oder nur die aus `only`)
        2. Cache pruefen: core/cache.py, Key z.B. f"eosync:{source}:{gene.upper()}"
           Treffer -> SourceResult mit cached=True, kein HTTP-Call
        3. Fuer die uebrigen: asyncio.gather(*[s.fetch(gene) for s in ...])
           WICHTIG: return_exceptions=True. Sonst reisst die erste Exception
           alle anderen Tasks mit runter.
        4. Erfolgreiche Ergebnisse in den Cache schreiben (TTL aus den Settings)
        5. Alles zu einer SearchResponse zusammensetzen, inkl. total_duration_ms

        Denk drueber nach: Soll ein Cache-Treffer fuer PubMed die anderen vier
        Quellen daran hindern, frische Daten zu holen? (Nein - deshalb wird pro
        Quelle gecacht, nicht pro Suche.)
        """
        raise NotImplementedError

    def normalize_gene(self, gene: str) -> str:
        """Gen-Symbole sind case-sensitiv-ish: 'tp53' und 'TP53' meinen dasselbe.

        TODO: Trimmen, uppercase, und pruefen, dass nur [A-Z0-9-] drin ist.
        Ohne das hast du Cache-Misses fuer jede Schreibweise - und eine
        Injection-Flaeche in Richtung der Upstream-Queries.
        """
        raise NotImplementedError
