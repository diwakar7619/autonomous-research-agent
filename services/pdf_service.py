"""
pdf_service.py

Generate professional PDF reports using fpdf2 2.8.7.
"""

from datetime import datetime
from pathlib import Path

from fpdf import FPDF

EXPORT_FOLDER = Path("exports")
EXPORT_FOLDER.mkdir(exist_ok=True)


def generate_pdf(query: str, summary: dict) -> str:
    pdf = FPDF()
    pdf.set_margins(left=15, top=15, right=15)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Usable width after margins
    usable_w = pdf.w - pdf.l_margin - pdf.r_margin  # noqa: E741

    # ── Title ──────────────────────────────────────────────────────────────────
    pdf.set_font("Helvetica", "B", 20)
    pdf.multi_cell(
        usable_w, 12, "Autonomous Research Report", new_x="LMARGIN", new_y="NEXT"
    )
    pdf.ln(2)

    # ── Meta ───────────────────────────────────────────────────────────────────
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(
        usable_w,
        8,
        f"Generated: {datetime.now().strftime('%d %b %Y  %H:%M')}",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    # Query can be arbitrarily long — always use multi_cell
    pdf.multi_cell(usable_w, 8, f"Query: {query}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)

    # ── Section helper ─────────────────────────────────────────────────────────
    def section(title: str, items: list, is_sources: bool = False) -> None:
        if not items:
            return

        pdf.set_font("Helvetica", "B", 14)
        pdf.multi_cell(usable_w, 10, title, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1)

        pdf.set_font("Helvetica", "", 11)
        for item in items:
            item_str = str(item).strip()
            item_str = (
                item_str.replace("’", "'")
                .replace("‘", "'")
                .replace(
                    """, '"')
            .replace(""",
                    '"',
                )
                .replace("—", "-")
                .replace("–", "-")
                .replace("…", "...")
            )
            if not item_str:
                continue

            if is_sources:
                # URLs: print as plain text with multi_cell, no pdf.write()
                # Prefix on first line, rest wraps naturally
                pdf.multi_cell(
                    usable_w,
                    7,
                    f"- {item_str}",
                    new_x="LMARGIN",
                    new_y="NEXT",
                )
            else:
                pdf.multi_cell(
                    usable_w,
                    7,
                    f"- {item_str}",
                    new_x="LMARGIN",
                    new_y="NEXT",
                )
            pdf.ln(1)

        pdf.ln(4)

    # ── Sections ───────────────────────────────────────────────────────────────
    section("Key Points", summary.get("key_points", []))
    section("Important Findings", summary.get("important_findings", []))
    section("Actionable Insights", summary.get("actionable_insights", []))
    section("Sources", summary.get("sources", []), is_sources=True)

    # ── Save ───────────────────────────────────────────────────────────────────
    filename = EXPORT_FOLDER / "research_report.pdf"
    pdf.output(str(filename))
    return str(filename)
