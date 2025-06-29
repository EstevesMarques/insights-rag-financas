# main.py

from pipeline.rag_pipeline import RAGPipeline
from strategies.fetchers.bcb_fetcher import BCBFetcher
from strategies.splitters.default_splitter import DefaultSplitter
from strategies.embedders.openai_embedder import OpenAIEmbedder
from strategies.vectorstores.faiss_store import FaissStore
from strategies.llms.openai_llm import OpenAILLM
from utils.logger import get_logger
from utils.memory import ManualMemory

import os

logger = get_logger("main")


def build_index(pipeline):
    logger.info("📥 Coletando dados e construindo índice...")
    raw_data = pipeline.fetcher.fetch()
    chunks = pipeline.splitter.split(raw_data)
    vectors = pipeline.embedder.embed_documents(chunks)
    pipeline.vectorstore.build(vectors, chunks)
    pipeline.vectorstore.save()
    logger.info("✅ Índice construído e salvo.")


def main():
    logger.info("Iniciando execução do insights-rag-financas...")

    memory = ManualMemory()

    fetcher = BCBFetcher(
        series_id=11, data_inicial="01/01/2020", data_final="31/12/2024"
    )  # SELIC Brasil
    splitter = DefaultSplitter()
    embedder = OpenAIEmbedder()
    vectorstore = FaissStore()
    llm = OpenAILLM()

    pipeline = RAGPipeline(
        fetcher=fetcher,
        splitter=splitter,
        embedder=embedder,
        vectorstore=vectorstore,
        llm=llm,
    )

    index_path = vectorstore.index_path

    # Se índice não existe, cria um
    if not os.path.exists(index_path):
        print("Índice local não encontrado. Construindo índice...")
        build_index(pipeline)
    else:
        print("Índice local encontrado. Carregando índice...")
        pipeline.vectorstore.load()

    print(
        "\n🤖 Bem-vindo ao Insights RAG Finanças! Faça suas perguntas sobre a taxa SELIC no Brasil."
    )
    print("Comandos disponíveis: 'sair', 'atualizar', 'resetar'\n")

    while True:
        question = input("❓ Sua pergunta: ").strip()
        if question.lower() in {"sair", "exit", "quit"}:
            print("👋 Encerrando o programa. Até mais!")
            break
        if question.lower() == "atualizar":
            print("♻️ Atualizando dados e reconstruindo índice, aguarde...")
            try:
                build_index(pipeline)
                print("✅ Índice atualizado com sucesso!\n")
            except Exception as e:
                logger.error(f"Erro ao atualizar índice: {e}")
                print("⚠️ Falha ao atualizar índice. Tente novamente mais tarde.\n")
            continue
        if question.lower() == "resetar":
            memory.reset()
            print("🧽 Memória da conversa apagada com sucesso!\n")
            continue
        if not question:
            print("⚠️ Pergunta vazia. Por favor, digite algo.")
            continue

        try:
            logger.info(f"Pergunta recebida: {question}")
            query_embedding = pipeline.embedder.embed_query(question)
            docs = pipeline.vectorstore.similarity_search(query_embedding)
            context = " ".join([doc.page_content for doc in docs])

            summary = memory.get_summary()
            context_with_memory = f"Resumo da conversa até agora:\n{summary or '[sem histórico]'}\n\n{context}"

            answer = pipeline.llm.answer(question, context_with_memory)
            print("\n🧠 Resposta:", answer, "\n")
            memory.update_summary(question, answer)

        except Exception as e:
            logger.error(f"Erro durante o processamento: {e}")
            print(
                "⚠️ Ocorreu um erro ao processar sua pergunta. Por favor, tente novamente.\n"
            )


if __name__ == "__main__":
    main()
