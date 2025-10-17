"""
LLM model implementations for multiple providers
"""
import os
import sys
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from Config.config import (
    GROQ_API_KEY, GROQ_MODEL,
    OPENAI_API_KEY, OPENAI_MODEL,
    GOOGLE_API_KEY, GOOGLE_MODEL
)


def get_chatgroq_model(temperature=0.7):
    """
    Initialize and return the Groq chat model
    
    Args:
        temperature (float): Temperature for response generation
        
    Returns:
        ChatGroq: Initialized Groq chat model
    """
    try:
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is not set")
        
        groq_model = ChatGroq(
            api_key=GROQ_API_KEY,
            model=GROQ_MODEL,
            temperature=temperature
        )
        return groq_model
    except Exception as e:
        raise RuntimeError(f"Failed to initialize Groq model: {str(e)}")


def get_openai_model(temperature=0.7):
    """
    Initialize and return the OpenAI chat model
    
    Args:
        temperature (float): Temperature for response generation
        
    Returns:
        ChatOpenAI: Initialized OpenAI chat model
    """
    try:
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set")
        
        openai_model = ChatOpenAI(
            api_key=OPENAI_API_KEY,
            model=OPENAI_MODEL,
            temperature=temperature
        )
        return openai_model
    except Exception as e:
        raise RuntimeError(f"Failed to initialize OpenAI model: {str(e)}")


def get_google_model(temperature=0.7):
    """
    Initialize and return the Google Gemini chat model
    
    Args:
        temperature (float): Temperature for response generation
        
    Returns:
        ChatGoogleGenerativeAI: Initialized Google chat model
    """
    try:
        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is not set")
        
        google_model = ChatGoogleGenerativeAI(
            google_api_key=GOOGLE_API_KEY,
            model=GOOGLE_MODEL,
            temperature=temperature
        )
        return google_model
    except Exception as e:
        raise RuntimeError(f"Failed to initialize Google model: {str(e)}")


def get_available_models():
    """
    Check which LLM providers are available based on API keys
    
    Returns:
        dict: Dictionary of available providers and their models
    """
    available = {}
    
    if GROQ_API_KEY:
        available["Groq"] = get_chatgroq_model
    if OPENAI_API_KEY:
        available["OpenAI"] = get_openai_model
    if GOOGLE_API_KEY:
        available["Google Gemini"] = get_google_model
    
    return available

