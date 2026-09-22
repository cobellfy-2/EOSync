# EOSync - Hinweise fuer Claude Code

## Wichtigste Regel: Der Nutzer schreibt den Code selbst

Dieses Repo ist ein Lernprojekt. Die `raise NotImplementedError`-Stellen und
TODO-Kommentare sind absichtlich da. Sie sind Uebungen.

**Nicht tun**, ausser der Nutzer bittet ausdruecklich darum ("schreib mir X",
"implementier das"):

- Einen Service, den Aggregator, den Cache oder den Rate-Limiter fertig
  implementieren
- TODO-Kommentare durch Code ersetzen
- "Hilfreich" nebenbei weitere Stubs mitfuellen

**Stattdessen:**

- Konzepte erklaeren (async, Rate-Limiting, HTTP-Header, XML-Parsing)
- Auf die passende API-Dokumentation zeigen
- Code des Nutzers reviewen: Bugs, Edge Cases, was in Produktion brechen wuerde
- Beim Debuggen helfen, Tests durchgehen
- Kleine, isolierte Beispiele zeigen (3-5 Zeilen), wenn ein Muster unklar ist

Im Zweifel fragen: "Willst du das selbst schreiben oder soll ich?"

Ausgenommen von der Regel: Struktur, Konfiguration, Doku, Docker, CI - das darf
Claude direkt erledigen.

## Projektkontext

- **Ziel:** REST-API-Integration lernen + verkaufbares Portfolio-Stueck
- **Stack:** FastAPI, httpx, Redis/SQLite, React + Vite (Phase 4)
- **Fortschritt und Reihenfolge:** siehe `LEARNING_PATH.md`

## Konventionen

- Code, Docstrings und Commit-Messages auf Englisch; Lern-Kommentare und
  Projektdoku auf Deutsch (gewachsen so, bitte beibehalten)
- Alle externen Aufrufe async, ein geteilter `httpx.AsyncClient`
- Jede Quelle liefert ein `SourceResult` - auch im Fehlerfall. Nie eine
  Exception aus einem Service nach oben durchreichen.
- Fachlogik in `services/`, HTTP-Uebersetzung in `api/`
- Tests rufen nie echte APIs auf - `respx` mockt die HTTP-Ebene

## Befehle

```bash
uvicorn backend.app.main:app --reload   # Dev-Server
pytest                                   # Tests
ruff check backend                       # Linting
docker compose up --build                # mit Redis
```
