"""Caching-Layer mit Redis und SQLite-Fallback.

Warum ueberhaupt cachen?
- NCBI & Co. sind oeffentliche, kostenlose Infrastruktur. Ungecachte Requests
  im Sekundentakt sind schlechter Stil und fuehren zu Sperren.
- TP53 wird von jedem zweiten Nutzer gesucht. Der zweite Request soll 5ms
  dauern, nicht 3 Sekunden.

Lernziel: Ein Interface, zwei Backends. Lokal brauchst du keinen Redis laufen
zu haben, in Produktion willst du ihn.
"""

from abc import ABC, abstractmethod
from typing import Any


class CacheBackend(ABC):
    @abstractmethod
    async def get(self, key: str) -> Any | None: ...

    @abstractmethod
    async def set(self, key: str, value: Any, ttl_seconds: int) -> None: ...

    @abstractmethod
    async def close(self) -> None: ...


class RedisCache(CacheBackend):
    """TODO (Phase 3): redis.asyncio.

    - Werte als JSON serialisieren (Redis speichert nur bytes/str)
    - TTL ueber den ex-Parameter von set(), nicht selbst mitschreiben
    - Verbindungsfehler duerfen die App NICHT killen: wenn Redis weg ist,
      soll EOSync langsamer werden, nicht kaputtgehen.
    """

    async def get(self, key: str) -> Any | None:
        raise NotImplementedError

    async def set(self, key: str, value: Any, ttl_seconds: int) -> None:
        raise NotImplementedError

    async def close(self) -> None:
        raise NotImplementedError


class SQLiteCache(CacheBackend):
    """TODO (Phase 3): Fallback fuer lokale Entwicklung.

    Tabelle:  cache(key TEXT PRIMARY KEY, value TEXT, expires_at REAL)
    get():    Zeile holen, expires_at gegen time.time() pruefen, abgelaufene
              Zeilen loeschen und None liefern.

    Stolperfalle: sqlite3 ist blockierend. In einer async-App entweder
    asyncio.to_thread() nutzen oder aiosqlite einsetzen - sonst blockierst du
    den Event-Loop und machst genau die Parallelitaet kaputt, fuer die du das
    ganze Projekt async gebaut hast.
    """

    def __init__(self, db_path: str = "backend/.cache.db") -> None:
        self.db_path = db_path

    async def get(self, key: str) -> Any | None:
        raise NotImplementedError

    async def set(self, key: str, value: Any, ttl_seconds: int) -> None:
        raise NotImplementedError

    async def close(self) -> None:
        raise NotImplementedError


def build_cache() -> CacheBackend:
    """TODO: REDIS_URL gesetzt -> RedisCache, sonst SQLiteCache."""
    raise NotImplementedError
