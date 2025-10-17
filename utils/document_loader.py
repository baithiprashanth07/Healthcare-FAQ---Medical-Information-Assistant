"""
Document loading and processing utilities
"""
import os
import sys
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    DirectoryLoader
)
from langchain.schema import Document

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from Config.config import CHUNK_SIZE, CHUNK_OVERLAP


def load_documents_from_directory(directory_path: str) -> List[Document]:
    """
    Load all documents from a directory
    
    Args:
        directory_path (str): Path to the directory containing documents
        
    Returns:
        List[Document]: List of loaded documents
    """
    try:
        documents = []
        
        # Load text files
        if os.path.exists(directory_path):
            txt_loader = DirectoryLoader(
                directory_path,
                glob="**/*.txt",
                loader_cls=TextLoader
            )
            documents.extend(txt_loader.load())
            
            # Load PDF files
            pdf_files = [f for f in os.listdir(directory_path) if f.endswith('.pdf')]
            for pdf_file in pdf_files:
                pdf_path = os.path.join(directory_path, pdf_file)
                pdf_loader = PyPDFLoader(pdf_path)
                documents.extend(pdf_loader.load())
        
        return documents
    except Exception as e:
        raise RuntimeError(f"Failed to load documents: {str(e)}")


def load_document_from_file(file_path: str) -> List[Document]:
    """
    Load a single document from a file
    
    Args:
        file_path (str): Path to the document file
        
    Returns:
        List[Document]: List containing the loaded document
    """
    try:
        if file_path.endswith('.pdf'):
            loader = PyPDFLoader(file_path)
        elif file_path.endswith('.txt'):
            loader = TextLoader(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_path}")
        
        return loader.load()
    except Exception as e:
        raise RuntimeError(f"Failed to load document from {file_path}: {str(e)}")


def split_documents(documents: List[Document]) -> List[Document]:
    """
    Split documents into chunks for embedding
    
    Args:
        documents (List[Document]): List of documents to split
        
    Returns:
        List[Document]: List of document chunks
    """
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        chunks = text_splitter.split_documents(documents)
        return chunks
    except Exception as e:
        raise RuntimeError(f"Failed to split documents: {str(e)}")


def process_uploaded_file(uploaded_file) -> List[Document]:
    """
    Process an uploaded file from Streamlit
    
    Args:
        uploaded_file: Streamlit UploadedFile object
        
    Returns:
        List[Document]: List of processed document chunks
    """
    try:
        # Save uploaded file temporarily
        temp_path = f"/tmp/{uploaded_file.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Load and process the document
        documents = load_document_from_file(temp_path)
        chunks = split_documents(documents)
        
        # Clean up temporary file
        os.remove(temp_path)
        
        return chunks
    except Exception as e:
        raise RuntimeError(f"Failed to process uploaded file: {str(e)}")

