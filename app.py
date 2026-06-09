import streamlit as st
import time
import sys
import os

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchAI",
    page_icon="🔬",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

/* Base */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0d1117;
    color: #e6edf3;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2.5rem; padding-bottom: 3rem; max-width: 780px; }

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
    border-bottom: 1px solid #21262d;
    margin-bottom: 2rem;
}
.hero-label {
    font-size: 0.72rem;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.18em;
    color: #0d9488;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}
.hero-title {
    font-size: 2.6rem;
    font-weight: 600;
    letter-spacing: -0.03em;
    color: #f0f6fc;
    line-height: 1.1;
    margin: 0;
}
.hero-title span {
    color: #0d9488;
}
.hero-sub {
    color: #8b949e;
    font-size: 0.95rem;
    margin-top: 0.75rem;
    font-weight: 300;
}

/* ── Input card ── */
.input-card {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 14px;
    padding: 1.5rem 1.75rem;
    margin-bottom: 1.75rem;
}

/* ── Pipeline tracker ── */
.pipeline-track {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0;
    margin: 1.5rem 0 2rem;
    padding: 1.25rem 1.5rem;
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 14px;
}
.pip-step {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.4rem;
    flex: 1;
    position: relative;
}
.pip-step:not(:last-child)::after {
    content: '';
    position: absolute;
    top: 18px;
    left: calc(50% + 22px);
    width: calc(100% - 44px);
    height: 2px;
    background: #21262d;
    transition: background 0.4s ease;
}
.pip-step.done:not(:last-child)::after,
.pip-step.active:not(:last-child)::after {
    background: #0d9488;
}
.pip-icon {
    width: 38px;
    height: 38px;
    border-radius: 50%;
    border: 2px solid #30363d;
    background: #0d1117;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.05rem;
    transition: all 0.3s ease;
    position: relative;
    z-index: 1;
}
.pip-step.active .pip-icon {
    border-color: #0d9488;
    background: rgba(13, 148, 136, 0.15);
    box-shadow: 0 0 0 4px rgba(13, 148, 136, 0.12);
    animation: pulse 1.4s ease-in-out infinite;
}
.pip-step.done .pip-icon {
    border-color: #0d9488;
    background: rgba(13, 148, 136, 0.2);
}
.pip-label {
    font-size: 0.68rem;
    color: #8b949e;
    font-family: 'JetBrains Mono', monospace;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    text-align: center;
}
.pip-step.active .pip-label,
.pip-step.done .pip-label {
    color: #0d9488;
}
@keyframes pulse {
    0%, 100% { box-shadow: 0 0 0 4px rgba(13, 148, 136, 0.12); }
    50% { box-shadow: 0 0 0 8px rgba(13, 148, 136, 0.06); }
}

/* ── Result cards ── */
.result-card {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.25rem;
}
.result-card-header {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    margin-bottom: 1rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid #21262d;
}
.result-card-icon {
    width: 30px;
    height: 30px;
    border-radius: 8px;
    background: rgba(13, 148, 136, 0.15);
    border: 1px solid rgba(13, 148, 136, 0.3);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.85rem;
}
.result-card-title {
    font-size: 0.8rem;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.08em;
    color: #0d9488;
    text-transform: uppercase;
    font-weight: 500;
}

/* ── Score badge ── */
.score-badge {
    display: inline-block;
    background: rgba(200, 135, 54, 0.12);
    border: 1px solid rgba(200, 135, 54, 0.3);
    color: #c88736;
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.1rem;
    font-weight: 500;
    padding: 0.2rem 0.75rem;
    border-radius: 8px;
    margin-bottom: 1rem;
}

/* ── Pre / output text ── */
.output-pre {
    font-family: 'Inter', sans-serif;
    font-size: 0.875rem;
    line-height: 1.7;
    color: #c9d1d9;
    white-space: pre-wrap;
    word-break: break-word;
    margin: 0;
}
.output-mono {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    line-height: 1.6;
    color: #8b949e;
    white-space: pre-wrap;
    word-break: break-word;
    max-height: 220px;
    overflow-y: auto;
    margin: 0;
}

/* ── Status / error banners ── */
.banner-info {
    background: rgba(13, 148, 136, 0.08);
    border: 1px solid rgba(13, 148, 136, 0.25);
    border-radius: 10px;
    padding: 0.75rem 1rem;
    font-size: 0.85rem;
    color: #5eead4;
    margin-bottom: 1rem;
    font-family: 'JetBrains Mono', monospace;
}
.banner-error {
    background: rgba(248, 81, 73, 0.08);
    border: 1px solid rgba(248, 81, 73, 0.25);
    border-radius: 10px;
    padding: 0.75rem 1rem;
    font-size: 0.85rem;
    color: #ff7b72;
    margin-bottom: 1rem;
}

/* ── Streamlit widget overrides ── */
div[data-testid="stTextInput"] input {
    background: #0d1117 !important;
    border: 1px solid #30363d !important;
    border-radius: 10px !important;
    color: #f0f6fc !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.65rem 1rem !important;
    transition: border-color 0.2s;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #0d9488 !important;
    box-shadow: 0 0 0 3px rgba(13, 148, 136, 0.15) !important;
}
div[data-testid="stButton"] button {
    background: #0d9488 !important;
    color: #f0f6fc !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
    padding: 0.6rem 1.75rem !important;
    letter-spacing: 0.01em;
    transition: background 0.2s, transform 0.1s;
    width: 100%;
}
div[data-testid="stButton"] button:hover {
    background: #0f766e !important;
    transform: translateY(-1px);
}
div[data-testid="stButton"] button:active {
    transform: translateY(0);
}

/* Expander */
div[data-testid="stExpander"] {
    background: #161b22;
    border: 1px solid #21262d !important;
    border-radius: 12px !important;
    margin-bottom: 0.75rem;
}
div[data-testid="stExpander"] summary {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: #8b949e;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

/* Divider */
hr {
    border-color: #21262d !important;
    margin: 1.5rem 0;
}

/* Download button */
div[data-testid="stDownloadButton"] button {
    background: transparent !important;
    border: 1px solid #30363d !important;
    color: #8b949e !important;
    border-radius: 10px !important;
    font-size: 0.82rem !important;
    font-family: 'JetBrains Mono', monospace !important;
    padding: 0.45rem 1rem !important;
    width: auto !important;
    letter-spacing: 0.05em;
    transition: border-color 0.2s, color 0.2s;
}
div[data-testid="stDownloadButton"] button:hover {
    border-color: #0d9488 !important;
    color: #0d9488 !important;
    transform: none !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #0d1117; }
::-webkit-scrollbar-thumb { background: #30363d; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #484f58; }
</style>
""", unsafe_allow_html=True)


# ── Helper: render pipeline tracker ──────────────────────────────────────────
STEPS = [
    ("🔍", "Search"),
    ("📄", "Read"),
    ("✍️", "Write"),
    ("🧠", "Critique"),
]

def render_pipeline(active: int = -1, done_up_to: int = -1):
    """Render the 4-step pipeline tracker. active=step currently running (0-based), done_up_to=last completed."""
    parts = []
    for i, (icon, label) in enumerate(STEPS):
        if i <= done_up_to:
            cls = "done"
            ico = "✓"
        elif i == active:
            cls = "active"
            ico = icon
        else:
            cls = ""
            ico = icon
        parts.append(
            f'<div class="pip-step {cls}">'
            f'  <div class="pip-icon">{ico}</div>'
            f'  <span class="pip-label">{label}</span>'
            f'</div>'
        )
    html = '<div class="pipeline-track">' + "".join(parts) + "</div>"
    return html


def render_result_card(icon: str, title: str, content: str, mono: bool = False):
    cls = "output-mono" if mono else "output-pre"
    return f"""
<div class="result-card">
  <div class="result-card-header">
    <div class="result-card-icon">{icon}</div>
    <span class="result-card-title">{title}</span>
  </div>
  <pre class="{cls}">{content}</pre>
</div>
"""


def extract_score(feedback: str) -> str:
    import re
    m = re.search(r'Score:\s*(\d+\s*/\s*10)', feedback, re.IGNORECASE)
    return m.group(1).replace(" ", "") if m else None


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-label">AI-Powered Research</div>
  <h1 class="hero-title">Research<span>AI</span></h1>
  <p class="hero-sub">Search → Read → Write → Critique &nbsp;·&nbsp; Fully automated deep research</p>
</div>
""", unsafe_allow_html=True)


# ── Input ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="input-card">', unsafe_allow_html=True)
topic = st.text_input(
    label="Research topic",
    placeholder="e.g. The impact of large language models on scientific research...",
    label_visibility="collapsed",
)
run_btn = st.button("Run Research Pipeline →", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────
for key in ("results", "error", "ran"):
    if key not in st.session_state:
        st.session_state[key] = None


# ── Run pipeline ──────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.markdown('<div class="banner-error">⚠️ Please enter a research topic before running.</div>', unsafe_allow_html=True)
    else:
        st.session_state.results = None
        st.session_state.error = None
        st.session_state.ran = True

        pipeline_ph = st.empty()
        status_ph = st.empty()

        try:
            # ── Attempt import (graceful error if env not set up) ──
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            try:
                from pipelines.pipeline import run_research_pipeline
            except ImportError as ie:
                raise RuntimeError(
                    f"Could not import pipeline: {ie}\n\n"
                    "Make sure you're running from the project root with all dependencies installed."
                )

            # Step 1 — Search
            pipeline_ph.markdown(render_pipeline(active=0, done_up_to=-1), unsafe_allow_html=True)
            status_ph.markdown('<div class="banner-info">⟳ &nbsp;Step 1 · Search agent scanning the web…</div>', unsafe_allow_html=True)

            # We run the full pipeline but intercept each step via a patched version.
            # Since the original pipeline.py prints to stdout, we capture state directly.
            from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

            state = {}

            search_agent = build_search_agent()
            search_result = search_agent.invoke({
                "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
            })
            state["search_results"] = search_result["messages"][-1].content

            # Step 2 — Read
            pipeline_ph.markdown(render_pipeline(active=1, done_up_to=0), unsafe_allow_html=True)
            status_ph.markdown('<div class="banner-info">⟳ &nbsp;Step 2 · Reader agent scraping top sources…</div>', unsafe_allow_html=True)

            reader_agent = build_reader_agent()
            reader_result = reader_agent.invoke({
                "messages": [("user",
                    f"Based on the following search results about '{topic}', "
                    f"pick the most relevant URL and scrape it for deeper content.\n\n"
                    f"Search Results:\n{state['search_results'][:800]}"
                )]
            })
            state["scraped_content"] = reader_result["messages"][-1].content

            # Step 3 — Write
            pipeline_ph.markdown(render_pipeline(active=2, done_up_to=1), unsafe_allow_html=True)
            status_ph.markdown('<div class="banner-info">⟳ &nbsp;Step 3 · Writer drafting the report…</div>', unsafe_allow_html=True)

            research_combined = (
                f"SEARCH RESULTS:\n{state['search_results']}\n\n"
                f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
            )
            state["report"] = writer_chain.invoke({"topic": topic, "research": research_combined})

            # Step 4 — Critique
            pipeline_ph.markdown(render_pipeline(active=3, done_up_to=2), unsafe_allow_html=True)
            status_ph.markdown('<div class="banner-info">⟳ &nbsp;Step 4 · Critic reviewing the report…</div>', unsafe_allow_html=True)

            state["feedback"] = critic_chain.invoke({"report": state["report"]})

            # Done
            pipeline_ph.markdown(render_pipeline(active=-1, done_up_to=3), unsafe_allow_html=True)
            status_ph.empty()

            st.session_state.results = state

        except Exception as e:
            pipeline_ph.empty()
            status_ph.empty()
            st.session_state.error = str(e)


# ── Display error ─────────────────────────────────────────────────────────────
if st.session_state.error:
    st.markdown(
        f'<div class="banner-error"><strong>Pipeline error</strong><br><br>'
        f'<code style="font-size:0.78rem">{st.session_state.error}</code></div>',
        unsafe_allow_html=True
    )


# ── Display results ───────────────────────────────────────────────────────────
if st.session_state.results:
    r = st.session_state.results

    st.markdown("---")

    # ── Report (primary output) ───────────────────────────────────────────────
    st.markdown(render_result_card("📋", "Final Report", r.get("report", ""), mono=False), unsafe_allow_html=True)

    col1, col2 = st.columns([1, 3])
    with col1:
        st.download_button(
            label="⬇ Download report",
            data=r.get("report", ""),
            file_name=f"report_{topic[:30].replace(' ', '_')}.md",
            mime="text/markdown",
        )

    st.markdown("---")

    # ── Critique card ─────────────────────────────────────────────────────────
    score = extract_score(r.get("feedback", ""))
    feedback_text = r.get("feedback", "")

    st.markdown("""
<div class="result-card">
  <div class="result-card-header">
    <div class="result-card-icon">🧠</div>
    <span class="result-card-title">Critic's Review</span>
  </div>
""", unsafe_allow_html=True)

    if score:
        st.markdown(f'<div class="score-badge">Score: {score}</div>', unsafe_allow_html=True)

    st.markdown(f'<pre class="output-pre">{feedback_text}</pre>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    # ── Collapsible raw data ──────────────────────────────────────────────────
    with st.expander("RAW · Search results"):
        st.markdown(
            f'<pre class="output-mono">{r.get("search_results", "")}</pre>',
            unsafe_allow_html=True,
        )

    with st.expander("RAW · Scraped content"):
        st.markdown(
            f'<pre class="output-mono">{r.get("scraped_content", "")}</pre>',
            unsafe_allow_html=True,
        )