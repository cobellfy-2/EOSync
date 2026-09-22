"""Erster gruener Test - beweist, dass die App ueberhaupt hochkommt.

Lauf ihn als Allererstes:  pytest backend/tests/test_health.py
"""


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_sources_endpoint_lists_all_five(client):
    response = client.get("/api/v1/sources")
    assert response.status_code == 200
    assert set(response.json()) == {"pubmed", "uniprot", "ensembl", "tcga", "geo"}


def test_search_is_not_implemented_yet(client):
    """Dieser Test wird rot, sobald du den Aggregator baust - genau so soll es
    sein. Dann ersetzt du ihn durch einen echten Test."""
    response = client.post("/api/v1/search", json={"gene": "TP53"})
    assert response.status_code == 501
