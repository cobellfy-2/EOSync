"""Gemeinsamer Vertrag fuer alle Datenquellen-Services.

Lernziel: Wenn jede Quelle das gleiche Interface hat, kann der Aggregator sie
alle gleich behandeln - egal ob PubMed XML liefert und UniProt JSON.
Das ist das Adapter-Pattern, und es ist der Grund, warum diese App wartbar bleibt.
"""

from abc import ABC, abstractmethod
from typing import Any

import httpx

from backend.app.models import SourceName, SourceResult


class BaseSource(ABC):
    """Basisklasse fuer jede externe API.

    Jede Subklasse setzt `name` und `base_url` und implementiert `_fetch`.
    Timing, Fehlerbehandlung und Ergebnis-Wrapping passieren hier oben - einmal,
    statt fuenfmal kopiert.
    """

    name: SourceName
    base_url: str
    timeout_seconds: float = 10.0

    def __init__(self, client: httpx.AsyncClient) -> None:
        # Der Client kommt von aussen (Dependency Injection): der Aggregator
        # teilt EINEN Connection-Pool mit allen Services.
        self.client = client

    async def fetch(self, gene: str) -> SourceResult:
        """Template-Methode: ruft _fetch auf und verpackt das Ergebnis.

        TODO (Phase 2):
        1. Startzeit merken (time.perf_counter)
        2. self._fetch(gene) mit asyncio.wait_for(timeout=self.timeout_seconds)
        3. Erfolg  -> SourceResult(status=OK, data=..., duration_ms=...)
        4. httpx.HTTPStatusError / TimeoutError / Exception jeweils in ein
           SourceResult mit passendem SourceStatus uebersetzen - NIE nach oben
           durchwerfen. Eine kaputte Quelle darf die anderen vier nicht killen.
        """
        raise NotImplementedError

    @abstractmethod
    async def _fetch(self, gene: str) -> Any:
        """Die eigentliche Abfrage. Gibt rohe, aber schon geparste Daten zurueck."""

    @abstractmethod
    def parse(self, raw: Any) -> Any:
        """Uebersetzt das quellenspezifische Format in unsere eigenen Modelle."""
