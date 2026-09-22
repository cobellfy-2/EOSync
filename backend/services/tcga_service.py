"""TCGA via GDC API - Krebs-Mutationsdaten.

Docs: https://docs.gdc.cancer.gov/API/Users_Guide/Search_and_Retrieval/

Die anspruchsvollste Quelle: Filter werden als verschachteltes JSON-Objekt
uebergeben, nicht als Query-String. Heb sie dir fuer den Schluss auf.
"""

from typing import Any

from backend.app.models import SourceName
from backend.services.base import BaseSource

SSMS_URL = "https://api.gdc.cancer.gov/ssms"


class TCGASource(BaseSource):
    name = SourceName.TCGA
    base_url = "https://api.gdc.cancer.gov"
    timeout_seconds = 20.0  # GDC ist spuerbar langsamer als die anderen

    async def _fetch(self, gene: str) -> Any:
        """
        TODO (Phase 2, zuletzt):
        POST SSMS_URL mit JSON-Body:
          {
            "filters": {
              "op": "in",
              "content": {
                "field": "consequence.transcript.gene.symbol",
                "value": [gene]
              }
            },
            "fields": "ssm_id,genomic_dna_change,mutation_subtype,"
                      "consequence.transcript.aa_change",
            "size": 50,
            "format": "JSON"
          }

        Lern-Detail: GET mit URL-Params vs. POST mit JSON-Body fuer eine reine
        Leseoperation - GDC macht beides. Der Grund: komplexe Filter sprengen
        die URL-Laengenbegrenzung. Gut zu wissen, wenn du mal selbst eine
        Such-API entwirfst.
        """
        raise NotImplementedError

    def parse(self, raw: Any) -> Any:
        """Nutzdaten liegen unter raw["data"]["hits"], Gesamtzahl unter
        raw["data"]["pagination"]["total"]."""
        raise NotImplementedError
