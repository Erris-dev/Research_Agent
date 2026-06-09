# 🔬 ResearchAI — Automated Deep Research Agent

An AI-powered research pipeline that searches the web, scrapes sources, writes a structured report, and critiques it — all in one automated flow. Built with LangChain, Google Gemini, and Tavily, with a clean Streamlit UI.

---

## What It Does

You give it a topic. It handles the rest:

1. **Search** — A LangChain agent uses Tavily to find the most recent and relevant sources across the web
2. **Read** — A second agent picks the best URL from the search results and scrapes it for deeper content
3. **Write** — A writer chain synthesizes the search results and scraped content into a structured research report
4. **Critique** — A critic chain reviews the report for weak evidence, unsupported claims, and poor structure, and scores it out of 10

---

## Tech Stack

| Layer | Tools |
|---|---|
| LLM | Google Gemini 2.5 Flash via `langchain-google-genai` |
| Agents | LangChain `create_agent` with custom tools |
| Web Search | Tavily API |
| Web Scraping | `requests` + `BeautifulSoup4` |
| Chains | LangChain `ChatPromptTemplate` + `StrOutputParser` |
| UI | Streamlit |
| Env Management | `python-dotenv` |

---

## Project Structure

```
Research_Agent/
├── app.py                  # Streamlit UI
├── agents.py               # Agent + chain definitions (search, reader, writer, critic)
├── pipelines/
│   └── pipeline.py         # Orchestrates the full 4-step research pipeline
├── tools/
│   └── tools.py            # search_web (Tavily) and scrape_url (BeautifulSoup) tools
├── .env                    # API keys (not committed)
└── requirements.txt
```

---

## Setup

### 1. Clone and install dependencies

```bash
pip install streamlit langchain langchain-google-genai langchain-core \
            tavily-python beautifulsoup4 requests python-dotenv rich
```

### 2. Configure environment variables

Create a `.env` file in the project root:

```env
TAVILY_API_KEY=your_tavily_api_key
GOOGLE_API_KEY=your_google_api_key
```

Get your keys here:
- Tavily: https://app.tavily.com
- Google AI Studio: https://aistudio.google.com/app/apikey

### 3. Run the app

```bash
streamlit run app.py
```

Or if `streamlit` isn't in your PATH:

```bash
python -m streamlit run app.py
```

The app opens at `http://localhost:8501`.

---

## How the Pipeline Works

```
User Input (topic)
       │
       ▼
 ┌─────────────┐
 │ Search Agent │  ──► Tavily API (5 results: titles, URLs, snippets)
 └─────────────┘
       │
       ▼
 ┌─────────────┐
 │ Reader Agent │  ──► Picks best URL → scrapes full page text (3000 chars)
 └─────────────┘
       │
       ▼
 ┌──────────────┐
 │ Writer Chain  │  ──► Combines search + scraped content → structured report
 └──────────────┘        (Introduction, Key Findings, Conclusion, Sources)
       │
       ▼
 ┌──────────────┐
 │ Critic Chain  │  ──► Reviews report → score out of 10, strengths, improvements
 └──────────────┘
```

---

## Agents & Chains

### Search Agent
Uses a LangChain agent backed by Gemini 2.5 Flash with the `search_web` tool. Instructed to find recent, reliable, and detailed information on the given topic.

### Reader Agent
Uses the same LLM with the `scrape_url` tool. Given the search results, it picks the most relevant URL and returns clean scraped text.

### Writer Chain
A `ChatPromptTemplate` chain that takes the combined research and produces a report structured as:
- Introduction
- Key Findings (minimum 3 points)
- Conclusion
- Sources

### Critic Chain
A strict reviewer chain that scores the report and returns structured feedback across strengths, areas to improve, and a one-line verdict.

---

## Tools

### `search_web(query: str)`
Queries the Tavily search API and returns up to 5 results with titles, URLs, and content snippets.

### `scrape_url(url: str)`
Fetches a webpage, strips boilerplate (nav, scripts, footers), and returns up to 3000 characters of clean body text.

---

## UI Features

- Live 4-step pipeline tracker that animates as each stage runs
- Final report displayed in a readable card with a one-click markdown download
- Critic score surfaced as a highlighted badge
- Raw search results and scraped content available in collapsible sections
- Styled error messages if the pipeline fails

---

## Environment Variables

| Variable | Description |
|---|---|
| `TAVILY_API_KEY` | Tavily search API key |
| `GOOGLE_API_KEY` | Google AI Studio key for Gemini access |