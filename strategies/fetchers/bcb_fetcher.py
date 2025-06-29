import requests

class BCBFetcher:
    """
    Estratégia para buscar dados do Banco Central do Brasil via API SGS.
    """
    BASE_URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs"

    def __init__(self, series_id=11, data_inicial="01/01/2020", data_final="31/12/2024"):
        self.series_id = series_id
        self.data_inicial = data_inicial
        self.data_final = data_final

    def fetch(self) -> str:
        url = f"{self.BASE_URL}.{self.series_id}/dados"
        params = {
            "formato": "json",
            "dataInicial": self.data_inicial,
            "dataFinal": self.data_final
        }
        headers = {
            "User-Agent": "insights-rag-financas/1.0 (contato@example.com)",
            "Accept": "application/json"
        }

        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()  # Levanta exceção para códigos 4xx/5xx
        except requests.exceptions.HTTPError as http_err:
            raise RuntimeError(f"Erro ao buscar série {self.series_id}: {response.status_code} - {response.text}") from http_err

        data = response.json()

        if not data:
            raise ValueError("Nenhum dado retornado da API do Banco Central.")

        lines = [f"{item['data']}: {item['valor']}" for item in data]
        return f"Série BCB ID {self.series_id}\n\n" + "\n".join(lines)