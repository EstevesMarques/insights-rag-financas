# config.py

from pathlib import Path
from dotenv import load_dotenv
import os

# Carrega as variáveis do arquivo .env
load_dotenv()

# OpenAI API Key (necessária para usar as APIs)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Modelo de embedding da OpenAI a ser usado (ex: text-embedding-3-small, etc.)
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

# Modelo da OpenAI a ser usado (ex: gpt-3.5-turbo, gpt-4, etc.)
OPENAI_LLM_MODEL = os.getenv("OPENAI_LLM_MODEL", "gpt-4o-mini-2024-07-18")

# Temperatura da OpenAI a ser usado (ex: 0.2, 0.5, etc.)
OPENAI_TEMPERATURE = os.getenv("OPENAI_TEMPERATURE", "0.2")

# Nome do diretório com os arquivos PDF
DATA_DIR = Path(os.getenv("DATA_DIR", "data"))

# Tamanho dos chunks de texto
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 500))

# Overlap entre os chunks (para contexto)
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 50))
