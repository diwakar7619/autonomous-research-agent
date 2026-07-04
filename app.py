"""
Autonomous Research Agent
Version 1
"""

import streamlit as st

from config import validate_api_keys
from services.tavily_service import search_web
from services.gemini_service import summarize_results
from utils.deduplication import clean_results
from services.pdf_service import generate_pdf

# Import Database Functions
from database.memory import initialize_database, get_history, save_search

# -------------------------------------------------
# Page Config
# -------------------------------------------------

st.set_page_config(
    page_title="Autonomous Research Agent",
    page_icon="🤖",
    layout="wide",
)

# -------------------------------------------------
# DB Initialization (Optional but Clean)
# -------------------------------------------------
if "db_initialized" not in st.session_state:
    initialize_database()
    st.session_state.db_initialized = True

# -------------------------------------------------
# Validate Configuration
# -------------------------------------------------

try:
    validate_api_keys()
except Exception as e:
    st.error(str(e))
    st.stop()

# -------------------------------------------------
# Sidebar: Search History
# -------------------------------------------------

st.sidebar.title("📚 Search History")
history = get_history(limit=10)

if history:
    for item in history:
        st.sidebar.markdown(f"🔍 **{item['query']}**")
        st.sidebar.caption(item["created_at"])
        st.sidebar.divider()
else:
    st.sidebar.info("No research history found.")

# -------------------------------------------------
# UI
# -------------------------------------------------

st.title("🤖 Autonomous Research Agent")

st.write(
    "Search the web using Tavily and generate an AI-powered research summary using Gemini."
)

query = st.text_input(
    "Enter your research topic:",
    placeholder="Example: Latest AI News",
)

# -------------------------------------------------
# Button
# -------------------------------------------------

if st.button("🔍 Research"):
    if not query.strip():
        st.warning("Please enter a research topic.")
        st.stop()

    with st.spinner("Searching the web and generating AI insights..."):
        try:
            search_results = search_web(query)
            search_results = clean_results(search_results)

            summary = summarize_results(search_results)

            # Save the successful search to SQLite Database BEFORE PDF generation (Fault Tolerance)
            save_search(query, summary)

            pdf_path = generate_pdf(query, summary)

            st.success(f"Research completed successfully for: {query}")

            st.divider()

            st.header("📌 Key Points")
            for point in summary.get("key_points", []):
                st.markdown(f"- {point}")

            st.divider()

            st.header("🔍 Important Findings")
            for finding in summary.get("important_findings", []):
                st.markdown(f"- {finding}")

            st.divider()

            st.header("💡 Actionable Insights")
            for insight in summary.get("actionable_insights", []):
                st.markdown(f"- {insight}")

            st.divider()

            st.header("🌐 Sources")
            for source in summary.get("sources", []):
                st.markdown(f"- {source}")

            st.divider()

            with open(pdf_path, "rb") as file:
                st.download_button(
                    label="📄 Download PDF Report",
                    data=file,
                    file_name="research_report.pdf",
                    mime="application/pdf",
                )

        except Exception as e:
            st.error(f"Error: {e}")
