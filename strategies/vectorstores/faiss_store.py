# strategies/vectorstores/faiss_store.py

import os
import faiss
import numpy as np
from langchain.schema import Document

class FaissStore:
    def __init__(self, index_path="data/vectorstore_index/faiss.index"):
        self.index_path = index_path
        self.index = None
        self.documents = []

    def build(self, vectors, documents):
        # Garante que 'documents' é uma lista de Document
        if documents and not isinstance(documents[0], Document):
            self.documents = [Document(page_content=doc) for doc in documents]
        else:
            self.documents = documents

        dim = len(vectors[0])
        self.index = faiss.IndexFlatL2(dim)

        vectors_np = np.array(vectors).astype("float32")
        self.index.add(vectors_np)

    def save(self):
        if self.index is None:
            raise RuntimeError("Índice vazio, nada para salvar.")

        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        faiss.write_index(self.index, self.index_path)

        docs_path = self.index_path + ".docs"
        with open(docs_path, "w", encoding="utf-8") as f:
            for doc in self.documents:
                f.write(doc.page_content.replace("\n", " ") + "\n<<<DOC>>>\n")

    def load(self):
        if not os.path.exists(self.index_path):
            raise FileNotFoundError(f"Índice não encontrado em {self.index_path}")

        self.index = faiss.read_index(self.index_path)

        docs_path = self.index_path + ".docs"
        if not os.path.exists(docs_path):
            raise FileNotFoundError(f"Arquivo de documentos não encontrado: {docs_path}")

        with open(docs_path, "r", encoding="utf-8") as f:
            raw = f.read()

        raw_docs = raw.split("\n<<<DOC>>>\n")
        self.documents = [Document(page_content=doc.strip()) for doc in raw_docs if doc.strip()]

    def similarity_search(self, query_embedding, k=5):
        if self.index is None:
            raise RuntimeError("Índice não carregado. Use load() ou build() primeiro.")

        xq = np.array([query_embedding]).astype("float32")
        D, I = self.index.search(xq, k)

        results = []
        for idx in I[0]:
            if idx < len(self.documents):
                results.append(self.documents[idx])

        return results
