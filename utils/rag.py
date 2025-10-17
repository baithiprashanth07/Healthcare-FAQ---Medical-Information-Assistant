"""
Retrieval-Augmented Generation (RAG) implementation
"""
import os
import sys
from typing import List, Optional
from langchain_community.vectorstores import FAISS
from langchain.schema import Document

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from Config.config import TOP_K_RESULTS, VECTOR_STORE_PATH
from models.embeddings import get_embedding_model
from utils.document_loader import load_documents_from_directory, split_documents


class RAGSystem:
    """RAG system for document retrieval and question answering"""
    
    def __init__(self):
        """Initialize the RAG system"""
        self.embeddings = get_embedding_model()
        self.vector_store = None
        self.is_initialized = False
    
    def initialize_from_directory(self, directory_path: str) -> bool:
        """
        Initialize vector store from a directory of documents
        
        Args:
            directory_path (str): Path to directory containing documents
            
        Returns:
            bool: True if initialization was successful
        """
        try:
            # Load documents
            documents = load_documents_from_directory(directory_path)
            
            if not documents:
                return False
            
            # Split documents into chunks
            chunks = split_documents(documents)
            
            # Create vector store
            self.vector_store = FAISS.from_documents(chunks, self.embeddings)
            self.is_initialized = True
            
            return True
        except Exception as e:
            print(f"Error initializing RAG system: {str(e)}")
            return False
    
    def add_documents(self, documents: List[Document]) -> bool:
        """
        Add new documents to the vector store
        
        Args:
            documents (List[Document]): List of documents to add
            
        Returns:
            bool: True if documents were added successfully
        """
        try:
            chunks = split_documents(documents)
            
            if self.vector_store is None:
                # Create new vector store if it doesn't exist
                self.vector_store = FAISS.from_documents(chunks, self.embeddings)
                self.is_initialized = True
            else:
                # Add to existing vector store
                self.vector_store.add_documents(chunks)
            
            return True
        except Exception as e:
            print(f"Error adding documents: {str(e)}")
            return False
    
    def retrieve_context(self, query: str, k: int = TOP_K_RESULTS) -> List[Document]:
        """
        Retrieve relevant documents for a query
        
        Args:
            query (str): User query
            k (int): Number of documents to retrieve
            
        Returns:
            List[Document]: List of relevant documents
        """
        try:
            if not self.is_initialized or self.vector_store is None:
                return []
            
            # Perform similarity search
            results = self.vector_store.similarity_search(query, k=k)
            return results
        except Exception as e:
            print(f"Error retrieving context: {str(e)}")
            return []
    
    def retrieve_context_with_scores(self, query: str, k: int = TOP_K_RESULTS) -> List[tuple]:
        """
        Retrieve relevant documents with similarity scores
        
        Args:
            query (str): User query
            k (int): Number of documents to retrieve
            
        Returns:
            List[tuple]: List of (document, score) tuples
        """
        try:
            if not self.is_initialized or self.vector_store is None:
                return []
            
            # Perform similarity search with scores
            results = self.vector_store.similarity_search_with_score(query, k=k)
            return results
        except Exception as e:
            print(f"Error retrieving context with scores: {str(e)}")
            return []
    
    def save_vector_store(self, path: str = VECTOR_STORE_PATH) -> bool:
        """
        Save the vector store to disk
        
        Args:
            path (str): Path to save the vector store
            
        Returns:
            bool: True if save was successful
        """
        try:
            if self.vector_store is None:
                return False
            
            os.makedirs(os.path.dirname(path), exist_ok=True)
            self.vector_store.save_local(path)
            return True
        except Exception as e:
            print(f"Error saving vector store: {str(e)}")
            return False
    
    def load_vector_store(self, path: str = VECTOR_STORE_PATH) -> bool:
        """
        Load the vector store from disk
        
        Args:
            path (str): Path to load the vector store from
            
        Returns:
            bool: True if load was successful
        """
        try:
            if os.path.exists(path):
                self.vector_store = FAISS.load_local(
                    path, 
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                self.is_initialized = True
                return True
            return False
        except Exception as e:
            print(f"Error loading vector store: {str(e)}")
            return False
    
    def format_context(self, documents: List[Document]) -> str:
        """
        Format retrieved documents into a context string
        
        Args:
            documents (List[Document]): List of retrieved documents
            
        Returns:
            str: Formatted context string
        """
        if not documents:
            return ""
        
        context_parts = []
        for i, doc in enumerate(documents, 1):
            context_parts.append(f"[Source {i}]\n{doc.page_content}")
        
        return "\n\n".join(context_parts)

