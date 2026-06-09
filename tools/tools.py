# pyrefly: ignore [missing-import]
from asyncio import timeout
from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv
from rich import print
load_dotenv()

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def search_web(query: str)-> str:
    """Search the web for information on a topic. Returns titles, URLs and snippets"""
    try:
        results = tavily_client.search(query=query, max_results=5)
        out = []

        for r in results['results']:
            out.append(
                f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content']}\n"
            )
        return '\n'.join(out)
    except Exception as e:
        return f"Error: {e}"

@tool
def scrape_url(url: str)->str:
    """Scrape and return clean text content from a given URL for deeper reading."""
    try:
       resp = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
       soup = BeautifulSoup(resp.text, "html.parser")
       for tag in soup(["script", "style", "header", "footer", "nav", "aside"]):
          tag.decompose()
       return soup.get_text(separator="", strip=True)[:3000]
    except Exception as e:
        return f"Error: {e}"