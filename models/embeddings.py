"""
Embedding models for RAG implementation
"""
import os
import sys
from langchain_huggingface import HuggingFaceEmbeddings

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from Config.config import EMBEDDING_MODEL


def get_embedding_model():
    """
    Initialize and return the HuggingFace embedding model
    
    Returns:
        HuggingFaceEmbeddings: Initialized embedding model
    """
    try:
        embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        return embeddings
    except Exception as e:
        raise RuntimeError(f"Failed to initialize embedding model: {str(e)}")

