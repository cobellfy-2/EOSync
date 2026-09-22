"""Tests fuer den PubMed-Service.

Lernziel: Tests duerfen NIE echte externe APIs aufrufen. Sie waeren langsam,
flaky und wuerden dein Rate-Limit verbrennen. Stattdessen: respx mockt die
HTTP-Ebene, dein Code merkt keinen Unterschied.

Alle Tests hier sind uebersprungen, bis du den Service implementierst.
Entferne das skip, sobald du loslegst.
"""

import pytest

pytestmark = pytest.mark.skip(reason="PubMedSource noch nicht implementiert")


@pytest.mark.asyncio
async def test_parse_extracts_title_and_pmid():
    """TODO: Ein kleines PubMed-XML-Sample als Konstante hinterlegen
    (2-3 Artikel reichen), parse() aufrufen, Felder pruefen."""


@pytest.mark.asyncio
async def test_empty_search_skips_efetch():
    """TODO: esearch mit leerer idlist mocken und verifizieren, dass efetch
    gar nicht erst aufgerufen wird."""


@pytest.mark.asyncio
async def test_missing_abstract_does_not_crash():
    """TODO: XML ohne <Abstract> - abstract muss None sein, kein Fehler."""


@pytest.mark.asyncio
async def test_http_500_becomes_error_result():
    """TODO: respx antwortet mit 500. fetch() muss ein SourceResult mit
    status=ERROR liefern, statt die Exception durchzureichen."""
