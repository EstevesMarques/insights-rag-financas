class RAGPipeline:
    def __init__(self, fetcher, splitter, embedder, vectorstore, llm):
        self.fetcher = fetcher
        self.splitter = splitter
        self.embedder = embedder
        self.vectorstore = vectorstore
        self.llm = llm

    def run(self, question: str):
        print("🚀 Iniciando pipeline RAG...")

        print("📥 Coletando dados...")
        raw_data = self.fetcher.fetch()

        print("✂️ Dividindo dados em chunks...")
        chunks = self.splitter.split(raw_data)

        print("🔎 Gerando vetores e construindo o índice...")
        self.vectorstore.build(chunks, self.embedder)

        print("🔍 Buscando contexto para a pergunta...")
        context = self.vectorstore.query(question)

        print("🧠 Gerando resposta com LLM...")
        answer = self.llm.answer(question, context)

        return answer