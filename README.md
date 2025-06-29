# 📊 insights-rag-financas

Um projeto **RAG (Retrieval-Augmented Generation)** com pipeline modular em Python, que responde perguntas sobre a **taxa SELIC brasileira** utilizando dados reais do Banco Central do Brasil e modelos da OpenAI.

> 🧠 Implementa memória de conversas, persistência vetorial com FAISS, chunking customizado, e consumo real de API pública (BCB/SGS).

---

## 🚀 Funcionalidades

- 🔍 **Busca de dados reais da SELIC** via [API pública do Banco Central](https://dadosabertos.bcb.gov.br/dataset/series-temporais).
- 📚 **Pipeline RAG** completo e modular:
  - Vetorização com `OpenAI Embeddings`
  - Armazenamento com `FAISS`
  - Geração de respostas com `GPT-4o` ou `GPT-3.5`
- 🧠 **Memória resumida persistente** (com LLM) entre interações.
- 💾 **Persistência local** dos vetores e do histórico da conversa.
- 🛠️ **Estrutura baseada em estratégia (Strategy Pattern)**, facilitando testes e trocas de componentes.
- 🧪 **Prompt interativo via terminal** com comandos especiais.

---

## 🗂️ Estrutura do Projeto

```bash
insights-rag-financas/
├── main.py                  # Script principal com loop interativo
├── config.py                # Configurações globais carregadas via .env
├── .env                     # Variáveis sensíveis (OpenAI, etc)
├── requirements.txt
│
├── data/                    # Armazena índices vetoriais e memória
│   ├── vectorstore_index/
│   └── memory.txt
│
├── pipeline/
│   └── rag_pipeline.py      # Orquestração do RAG Pipeline
│
├── strategies/
│   ├── embedders/
│   │   └── openai_embedder.py
│   ├── vectorstores/
│   │   └── faiss_store.py
│   ├── llms/
│   │   └── openai_llm.py
│   ├── fetchers/
│   │   └── bcb_fetcher.py   # Busca dados da API SGS (Banco Central)
│   └── splitters/
│       └── default_splitter.py
│
├── utils/
│   ├── logger.py
│   └── memory.py            # Memória resumida com LLM
````

---

## 🧪 Exemplo de uso

```bash
$ python main.py

🤖 Bem-vindo ao Insights RAG Finanças! Faça suas perguntas sobre a taxa SELIC no Brasil.
Comandos disponíveis: 'sair', 'atualizar', 'resetar'

❓ Sua pergunta: qual a taxa selic?

🧠 Resposta: A taxa SELIC atualmente está em 10,50% ao ano, conforme os dados atualizados do Banco Central.
```

---

## 🧠 Comandos especiais disponíveis

| Comando     | Ação                                                     |
| ----------- | -------------------------------------------------------- |
| `sair`      | Encerra o programa                                       |
| `atualizar` | Refaz a chamada à API e reconstrói o índice vetorial     |
| `resetar`   | Apaga a memória de conversa (resumo interativo anterior) |

---

## ⚙️ Configuração

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/insights-rag-financas.git
cd insights-rag-financas
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o arquivo `.env`

Crie um arquivo `.env` na raiz com:

```env
OPENAI_API_KEY=sk-...
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_LLM_MODEL=gpt-4o
OPENAI_TEMPERATURE=0.2
DATA_DIR=data
CHUNK_SIZE=500
CHUNK_OVERLAP=50
```

---

## 🛠️ Tecnologias utilizadas

* [LangChain](https://www.langchain.com/)
* [OpenAI API](https://platform.openai.com/)
* [FAISS](https://github.com/facebookresearch/faiss)
* [BCB API (SGS)](https://dadosabertos.bcb.gov.br/dataset/series-temporais)

---

## ✍️ Futuras melhorias

* [ ] UI Web (Streamlit ou FastAPI)
* [ ] Suporte a múltiplas séries econômicas
* [ ] Logs com mais detalhes e exportáveis
* [ ] Salvamento de histórico em JSON

---

## 📄 Licença

Este projeto está licenciado sob a licença MIT.

---

## 👨‍💻 Autor

**Esteves Marques**
🧠 Engenheiro de software e entusiasta de IA aplicada ao mundo real.
🔗 [linkedin.com/in/estevesmarques](https://linkedin.com/in/estevesmarques)
🌐 Projeto parte do [IA Playbook](https://iaplaybook.tech/)