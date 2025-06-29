from strategies.llms.openai_llm import OpenAILLM
import os

MEMORY_FILE = "data/memory.txt"

class ManualMemory:
    def __init__(self, persist_path=MEMORY_FILE):
        self.persist_path = persist_path
        self.llm = OpenAILLM()
        self.summary = self.load()

    def load(self):
        if os.path.exists(self.persist_path):
            with open(self.persist_path, "r", encoding="utf-8") as f:
                return f.read().strip()
        return ""

    def save(self):
        os.makedirs(os.path.dirname(self.persist_path), exist_ok=True)
        with open(self.persist_path, "w", encoding="utf-8") as f:
            f.write(self.summary.strip())

    def update_summary(self, question: str, answer: str):
        prompt = f"""
Você é responsável por manter um resumo objetivo e contínuo da conversa entre um usuário e um assistente financeiro.

Resumo atual:
{self.summary or "[vazio]"}

Nova pergunta do usuário:
{question}

Nova resposta do assistente:
{answer}

Atualize o resumo acima, incorporando essa nova troca de forma coesa e concisa. Use frases completas e objetivas.
Novo resumo:
"""
        # Usamos o método que já existe na classe OpenAILLM
        new_summary = self.llm.answer("Atualize o resumo da conversa.", prompt)
        self.summary = new_summary.strip()
        self.save()

    def get_summary(self):
        return self.summary.strip()

    def reset(self):
        self.summary = ""
        if os.path.exists(self.persist_path):
            os.remove(self.persist_path)
