from langchain_openai import OpenAIEmbeddings
from config import OPENAI_API_KEY, OPENAI_EMBEDDING_MODEL

class OpenAIEmbedder:
    def __init__(self):
        self.embedder = OpenAIEmbeddings(
            openai_api_key=OPENAI_API_KEY,
            model=OPENAI_EMBEDDING_MODEL
        )

    def embed_documents(self, texts):
        """
        texts: List[str] - lista de textos (chunks)
        Retorna: List[List[float]] - embeddings para cada texto
        """
        return self.embedder.embed_documents(texts)

    def embed_query(self, query):
        """
        query: str - texto da pergunta
        Retorna: List[float] - embedding do texto
        """
        return self.embedder.embed_query(query)
