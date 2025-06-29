# strategies/llms/openai_llm.py

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.schema import Document
from config import OPENAI_API_KEY, OPENAI_LLM_MODEL, OPENAI_TEMPERATURE

class OpenAILLM:
    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=OPENAI_API_KEY,
            model=OPENAI_LLM_MODEL,
            temperature=float(OPENAI_TEMPERATURE)
        )

        self.prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="""
Você é um assistente financeiro especializado. Com base no contexto abaixo, responda de forma clara e objetiva à pergunta do usuário.

Contexto:
{context}

Pergunta:
{question}
"""
        )

        # NOVA FORMA RECOMENDADA
        self.qa_chain = create_stuff_documents_chain(
            llm=self.llm,
            prompt=self.prompt,
            document_variable_name="context"
        )

    def answer(self, question: str, context: str) -> str:
        documents = [Document(page_content=context)]
        result = self.qa_chain.invoke({
            "context": documents,
            "question": question
        })
        return result.strip()
