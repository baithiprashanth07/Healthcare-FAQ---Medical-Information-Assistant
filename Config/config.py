"""
Configuration file for API keys and settings
"""
import os
from dotenv import load_dotenv

load_dotenv()
# LLM Provider API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

# Model Names
GROQ_MODEL = "llama-3.3-70b-versatile"
OPENAI_MODEL = "gpt-4o-mini"
GOOGLE_MODEL = "gemini-1.5-flash"

# RAG Configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K_RESULTS = 3

# Response Mode Settings
CONCISE_MAX_TOKENS = 150
DETAILED_MAX_TOKENS = 500

# Vector Store Settings
VECTOR_STORE_PATH = "data/vector_store"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Web Search Settings
MAX_SEARCH_RESULTS = 3

