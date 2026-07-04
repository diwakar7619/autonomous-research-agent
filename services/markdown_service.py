"""
markdown_service.py

Generate a Markdown research report.
"""

from datetime import datetime
from pathlib import Path

EXPORT_FOLDER = Path("exports")
EXPORT_FOLDER.mkdir(exist_ok=True)


def generate_markdown(query: str, summary: dict) -> str:
    """
    Generate a markdown research report.

    Args:
        query: User research topic.
        summary: Structured Gemini summary.

    Returns:
        Path to generated markdown file.
    """

    filename = EXPORT_FOLDER / "research_report.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write("# Autonomous Research Report\n\n")

        f.write(f"**Generated:** {datetime.now().strftime('%d %b %Y %H:%M')}\n\n")

        f.write(f"**Query:** {query}\n\n")

        f.write("---\n\n")

        f.write("## 📌 Key Points\n\n")

        for item in summary.get("key_points", []):
            f.write(f"- {item}\n")

        f.write("\n---\n\n")

        f.write("## 🔍 Important Findings\n\n")

        for item in summary.get("important_findings", []):
            f.write(f"- {item}\n")

        f.write("\n---\n\n")

        f.write("## 💡 Actionable Insights\n\n")

        for item in summary.get("actionable_insights", []):
            f.write(f"- {item}\n")

        f.write("\n---\n\n")

        f.write("## 🌐 Sources\n\n")

        for item in summary.get("sources", []):
            f.write(f"- {item}\n")

    return str(filename)
