# strategies/fetchers/fred_fetcher.py

import requests
from config import FRED_API_KEY

class FredFetcher:
    """
    Estratégia para buscar dados econômicos da API FRED (Federal Reserve).
    """
    BASE_URL = "https://api.stlouisfed.org/fred/series/observations"

    def __init__(self, series_id="UNRATE"):
        self.series_id = series_id  # Ex: UNRATE = Taxa de desemprego dos EUA

    def fetch(self) -> str:
        """
        Retorna uma string de dados históricos da série, formatada como texto bruto.
        """
        params = {
            "series_id": self.series_id,
            "api_key": FRED_API_KEY,
            "file_type": "json"
        }

        response = requests.get(self.BASE_URL, params=params)

        if not response.ok:
            raise RuntimeError(f"Erro ao buscar dados FRED: {response.status_code}")

        data = response.json()

        if "observations" not in data:
            raise ValueError("Resposta da FRED malformada ou vazia.")

        lines = [
            f"{obs['date']}: {obs['value']}"
            for obs in data["observations"]
            if obs["value"] != "."
        ]

        return f"Série FRED: {self.series_id}\n\n" + "\n".join(lines)
