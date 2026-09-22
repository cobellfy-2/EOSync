"""Token-Bucket Rate-Limiter fuer ausgehende Requests.

Das hier ist der Teil, der in Bewerbungsgespraechen auffaellt. Die meisten
Hobby-Projekte streuen time.sleep() ein und hoffen. Ein Token-Bucket ist der
Algorithmus, den echte API-Clients benutzen.

Prinzip:
- Ein Eimer haelt maximal `capacity` Tokens.
- Es fliessen `rate` Tokens pro Sekunde nach.
- Jeder Request nimmt ein Token. Leerer Eimer -> warten.

Warum besser als "alle 333ms einer"? Bursts. Wenn 2 Sekunden nichts passiert
ist, darfst du danach sofort mehrere Requests feuern - genau das erlauben die
Rate-Limits der meisten APIs auch.
"""

import asyncio  # noqa: F401  - brauchst du in acquire() fuer sleep und Lock


class TokenBucket:
    """Ein Limiter pro HOST, nicht pro Service.

    PubMed und GEO teilen sich eutils.ncbi.nlm.nih.gov - und damit dasselbe
    Limit. Zwei getrennte Limiter mit je 3 req/s ergeben 6 req/s beim Server
    und fuehren zu HTTP 429.
    """

    def __init__(self, rate: float, capacity: int | None = None) -> None:
        self.rate = rate
        self.capacity = capacity or int(rate)
        # TODO (Phase 3): self._tokens, self._last_refill (monotonic clock!),
        # und ein asyncio.Lock - ohne Lock haben parallele Tasks eine Race
        # Condition auf dem Token-Zaehler.

    async def acquire(self, tokens: int = 1) -> None:
        """Wartet, bis genug Tokens da sind, und entnimmt sie.

        TODO (Phase 3):
        1. Lock nehmen
        2. Nachfuellen: elapsed = now - last_refill;
           tokens = min(capacity, tokens + elapsed * rate)
        3. Genug da -> abziehen, fertig.
           Sonst: benoetigte Wartezeit ausrechnen, asyncio.sleep(), dann abziehen.

        Nutze time.monotonic(), nicht time.time() - letztere kann bei einer
        NTP-Korrektur rueckwaerts springen.
        """
        raise NotImplementedError

    async def __aenter__(self) -> "TokenBucket":
        await self.acquire()
        return self

    async def __aexit__(self, *exc_info: object) -> None:
        return None
