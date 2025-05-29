import requests
from typing import Dict
from config import TAVILY_API_KEY
from agents import function_tool

@function_tool
def tavily_search(query: str, include_images: bool = False, search_depth: str = "basic", 
                 max_results: int = 1, days: int = 3) -> Dict:
    """Search for market news using Tavily API"""
    print(f"Running function: tavily_search with query: {query}")
    url = "https://api.tavily.com/search"
    payload = {
        "query": query,
        "topic": "general",
        "search_depth": search_depth,
        "max_results": max_results,
        "days": days,
        "include_answer": True,
        "include_images": include_images
    }
    headers = {"Authorization": f"Bearer {TAVILY_API_KEY}", "Content-Type": "application/json"}
    
    response = requests.post(url, json=payload, headers=headers)
    result = response.json()
    
    summary = ""
    if results := result.get("results", []):
        for res in results:
            summary += f"Title: {res.get('title', 'No Title')}\nContent: {res.get('content', 'No Content')}\n\n"
    else:
        summary = "No text results found.\n"
    
    if include_images:
        summary += "Image Results:\n" + "\n".join(result.get("images", [])) if result.get("images") else "No images found\n"
    
    return {"formatted_summary": summary, "raw_response": result}