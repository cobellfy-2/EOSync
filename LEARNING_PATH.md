# EOSync - Lernpfad

Dieses Projekt hat zwei Ziele: eine API, die man verkaufen kann, und du, der
REST-APIs wirklich versteht. Deshalb ist der Code absichtlich unfertig.
Jedes `raise NotImplementedError` ist eine Uebung, kein Versehen.

**Regel fuer Claude Code in diesem Repo:** Konzepte erklaeren, Fehler finden,
reviewen - ja. Ganze Services fertig hinschreiben - nein, ausser du bittest
ausdruecklich darum. Das steht so auch in `CLAUDE.md`.

---

## Session 1 - Es laeuft (30 Min)

- [ ] venv anlegen, `pip install -r requirements.txt`
- [ ] `cp .env.example .env`
- [ ] `uvicorn backend.app.main:app --reload`
- [ ] http://localhost:8000/docs oeffnen und alle drei Endpoints anschauen
- [ ] `pytest` - drei gruene Tests

**Verstanden, wenn du erklaeren kannst:** Was macht `--reload`? Warum liegt
`/health` ausserhalb von `/api/v1`?

## Session 2 - PubMed, Teil 1: esearch

- [ ] `PubMedSource._fetch` bis zur PMID-Liste implementieren
- [ ] Vorher im Browser ausprobieren:
      `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=TP53[Gene Name]&retmode=json&retmax=5`
- [ ] Den Debug-Endpoint `GET /api/v1/search/TP53/pubmed` zum Laufen bringen

**Neu gelernt:** Query-Parameter, `httpx.AsyncClient`, JSON-Response-Handling.

## Session 3 - PubMed, Teil 2: efetch und XML

- [ ] Zweiten Request bauen, Ergebnis an `parse()` geben
- [ ] XML mit `xml.etree.ElementTree` in `Article`-Objekte verwandeln
- [ ] Die Faelle abfangen: kein Abstract, kein Jahr, keine Autoren
- [ ] `test_pubmed.py` entsperren und die ersten Tests schreiben

**Neu gelernt:** Verkettete Requests, XML-Parsing, defensives Mapping.

## Session 4 - Fehler sind auch Daten

- [ ] `BaseSource.fetch` implementieren: Timing, Timeout, Exception-Mapping
- [ ] Testen, indem du `base_url` absichtlich kaputt machst
- [ ] Ergebnis muss ein `SourceResult` mit `status=error` sein - kein Stacktrace

**Neu gelernt:** Template-Method-Pattern, graceful degradation, `asyncio.wait_for`.

## Session 5 - UniProt und Ensembl

- [ ] Beide Services implementieren (nach PubMed fuehlt sich das leicht an)
- [ ] Bei UniProt in den `link`-Response-Header schauen: so paginieren echte APIs
- [ ] Bei Ensembl einen 429 provozieren und `Retry-After` auswerten

**Neu gelernt:** Response-Header als Steuerdaten, Pagination, Retry-Logik.

## Session 6 - Parallelitaet

- [ ] `AggregatorService.search` mit `asyncio.gather(..., return_exceptions=True)`
- [ ] Die Zeiten vergleichen: sequenziell vs. parallel, in `total_duration_ms`
- [ ] `normalize_gene` implementieren

**Neu gelernt:** Warum das ganze Projekt async ist. Hier wird es sichtbar.

## Session 7 - Rate Limiting

- [ ] `TokenBucket.acquire` implementieren
- [ ] EINEN Limiter fuer `eutils.ncbi.nlm.nih.gov` an PubMed und GEO geben
- [ ] Testen: 20 Requests abfeuern, Zeitstempel loggen, Limit pruefen

**Neu gelernt:** Der Algorithmus hinter jedem professionellen API-Client.

## Session 8 - Caching

- [ ] `SQLiteCache` implementieren (blockierendes sqlite3 in `asyncio.to_thread`)
- [ ] Cache in den Aggregator einhaengen, `cached=True` korrekt setzen
- [ ] Danach `RedisCache` - dasselbe Interface, anderes Backend

**Neu gelernt:** Interface vs. Implementierung, TTL, Event-Loop nicht blockieren.

## Session 9+ - GEO, TCGA, Frontend

- [ ] GEO (E-utilities-Code aus PubMed gemeinsam nutzen)
- [ ] TCGA (POST mit JSON-Filtern - die komplexeste Quelle)
- [ ] React-Frontend, siehe `frontend/README.md`

---

## Fragen, die dich weiterbringen

Wenn du in einer Session nicht weiterkommst, frag Claude Code nach dem **Warum**,
nicht nach dem Code:

- "Warum braucht der TokenBucket einen Lock?"
- "Was passiert bei `asyncio.gather` ohne `return_exceptions=True`?"
- "Wieso ist `sqlite3` in einer async-App ein Problem?"
- "Review meinen PubMed-Service - was wuerde in Produktion brechen?"
