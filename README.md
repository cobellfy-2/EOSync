# EOSync

**One gene in. Five biomedical databases out.**

EOSync aggregates PubMed, UniProt, Ensembl, TCGA and GEO into a single REST
request. Instead of opening five portals and copy-pasting between them, you ask
once and get one normalized response.

```http
POST /api/v1/search
{ "gene": "TP53" }
```

```json
{
  "gene": "TP53",
  "sources": {
    "pubmed":  { "status": "ok", "count": 1523, "data": [...], "duration_ms": 812 },
    "uniprot": { "status": "ok", "count": 1,    "data": [...], "cached": true },
    "tcga":    { "status": "timeout", "error": "GDC did not respond in 20s" }
  },
  "total_duration_ms": 1104
}
```

> **Status: in active development.** The scaffold, API contract and test suite
> are in place; the source adapters are being implemented one at a time.

## Why it is built this way

| Decision | Reason |
|---|---|
| `async` end to end | Five sequential calls take ~4s. In parallel it is as slow as the slowest source. |
| Per-source result envelope | A dead upstream degrades one tab, it does not 500 the whole response. |
| Token-bucket rate limiting per host | NCBI allows 3 req/s (10 with a key). PubMed and GEO share that budget. |
| Cache per source, not per search | A cached PubMed hit must not block fresh Ensembl data. |
| Redis with SQLite fallback | No infrastructure required to run locally. |

## Data sources

| Source | API | Auth | What we pull |
|---|---|---|---|
| PubMed | NCBI E-utilities | optional key | Literature: title, authors, abstract |
| UniProt | UniProtKB REST | none | Protein names, function, length |
| Ensembl | Ensembl REST | none | Gene annotation, transcripts, location |
| TCGA | GDC API | none | Somatic mutations per gene |
| GEO | NCBI E-utilities | optional key | Expression datasets |

All five are public and free. EOSync caches aggressively to stay a good citizen.

## Quickstart

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
cp .env.example .env

uvicorn backend.app.main:app --reload
```

- API docs: http://localhost:8000/docs
- Health:   http://localhost:8000/health

```bash
pytest
```

With Docker + Redis:

```bash
docker compose up --build
```

## Project layout

```
backend/
├── app/        main.py, config.py, models.py   <- API contract
├── api/        search.py                        <- HTTP layer only
├── services/   one adapter per source + aggregator
├── core/       cache.py, rate_limiter.py
└── tests/
frontend/       React + Vite (phase 4)
```

## Roadmap

- [x] Phase 1 — Scaffold, config, health endpoint, green test suite
- [ ] Phase 2 — Source adapters (PubMed first)
- [ ] Phase 3 — Aggregator, caching, rate limiting
- [ ] Phase 4 — React frontend, CSV/JSON export
- [ ] Phase 5 — Auth, API keys, deployment

## License

MIT
