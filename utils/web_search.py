"""
Web search functionality for real-time information retrieval
"""
import os
import sys
from typing import List, Dict
from duckduckgo_search import DDGS

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from Config.config import MAX_SEARCH_RESULTS


def search_web(query: str, max_results: int = MAX_SEARCH_RESULTS) -> List[Dict[str, str]]:
    """
    Perform a web search using DuckDuckGo
    
    Args:
        query (str): Search query
        max_results (int): Maximum number of results to return
        
    Returns:
        List[Dict[str, str]]: List of search results with title, body, and href
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
            return results
    except Exception as e:
        print(f"Error performing web search: {str(e)}")
        return []


def format_search_results(results: List[Dict[str, str]]) -> str:
    """
    Format search results into a readable string
    
    Args:
        results (List[Dict[str, str]]): List of search results
        
    Returns:
        str: Formatted search results
    """
    if not results:
        return "No search results found."
    
    formatted_parts = []
    for i, result in enumerate(results, 1):
        title = result.get('title', 'No title')
        body = result.get('body', 'No description')
        url = result.get('href', '')
        
        formatted_parts.append(
            f"[Result {i}]\n"
            f"Title: {title}\n"
            f"Description: {body}\n"
            f"URL: {url}"
        )
    
    return "\n\n".join(formatted_parts)


def search_and_format(query: str, max_results: int = MAX_SEARCH_RESULTS) -> str:
    """
    Search the web and return formatted results
    
    Args:
        query (str): Search query
        max_results (int): Maximum number of results to return
        
    Returns:
        str: Formatted search results
    """
    try:
        results = search_web(query, max_results)
        return format_search_results(results)
    except Exception as e:
        return f"Error searching the web: {str(e)}"

