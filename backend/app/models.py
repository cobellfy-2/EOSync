"""Pydantic-Schemas = der oeffentliche Vertrag deiner REST API.

Lernziel: Ein API-Response ist ein stabiles Versprechen. Wenn du hier ein Feld
umbenennst, bricht jedes Frontend. Deshalb: erst Schema, dann Implementierung.

Diese Modelle sind bewusst schlank gehalten - erweitere sie, sobald du weisst,
was die jeweilige Quelle wirklich liefert.
"""

from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class SourceName(StrEnum):
    PUBMED = "pubmed"
    UNIPROT = "uniprot"
    ENSEMBL = "ensembl"
    TCGA = "tcga"
    GEO = "geo"


class SourceStatus(StrEnum):
    OK = "ok"
    ERROR = "error"          # Quelle hat geantwortet, aber fehlerhaft
    TIMEOUT = "timeout"
    RATE_LIMITED = "rate_limited"
    NOT_IMPLEMENTED = "not_implemented"


class Article(BaseModel):
    """Ein PubMed-Treffer."""

    pmid: str
    title: str
    authors: list[str] = Field(default_factory=list)
    journal: str | None = None
    year: int | None = None
    abstract: str | None = None
    url: str | None = None


class SourceResult(BaseModel):
    """Einheitlicher Wrapper um JEDE Quelle.

    Wichtig fuers Frontend: auch eine fehlgeschlagene Quelle liefert ein Objekt,
    kein fehlendes Feld. Graceful degradation statt 500er fuer alles.
    """

    source: SourceName
    status: SourceStatus
    data: Any | None = None
    count: int | None = None
    error: str | None = None
    duration_ms: int | None = None
    cached: bool = False


class SearchResponse(BaseModel):
    """Antwort von POST /api/v1/search."""

    gene: str
    sources: dict[SourceName, SourceResult]
    timestamp: datetime
    total_duration_ms: int


class SearchRequest(BaseModel):
    gene: str = Field(min_length=1, max_length=64, examples=["TP53"])
    sources: list[SourceName] | None = Field(
        default=None,
        description="Wenn leer: alle Quellen abfragen.",
    )
