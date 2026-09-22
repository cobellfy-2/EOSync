"""REST-Endpoints fuer die Gen-Suche.

Lernziel Router-Design:
- Der Router validiert Input und uebersetzt Fehler in HTTP-Status-Codes.
- Fachlogik gehoert in services/, nicht hierher.
"""

from fastapi import APIRouter, HTTPException, status

from backend.app.models import SearchRequest, SearchResponse, SourceName

router = APIRouter(tags=["search"])


@router.get("/sources")
async def list_sources() -> list[str]:
    """Welche Quellen kennt diese API? Nuetzlich fuers Frontend."""
    return [s.value for s in SourceName]


@router.post("/search", response_model=SearchResponse)
async def search_gene(request: SearchRequest) -> SearchResponse:
    """Fragt alle (oder ausgewaehlte) Quellen parallel zu einem Gen ab.

    TODO (Phase 3):
    1. AggregatorService aus services/aggregator.py aufrufen
    2. Ergebnis als SearchResponse zurueckgeben
    3. Wenn ALLE Quellen fehlschlagen -> 502 Bad Gateway.
       Wenn nur einzelne fehlschlagen -> 200 mit status="error" pro Quelle.
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Aggregator noch nicht implementiert - siehe services/aggregator.py",
    )


@router.get("/search/{gene}/{source}")
async def search_single_source(gene: str, source: SourceName):
    """Eine einzelne Quelle abfragen - dein bester Debug-Endpoint.

    Beim Entwickeln eines neuen Service willst du ihn isoliert testen koennen,
    ohne dass vier andere APIs mitlaufen.

    TODO (Phase 2): Service aus einer Registry holen und fetch() aufrufen.
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail=f"Service '{source.value}' noch nicht implementiert",
    )
