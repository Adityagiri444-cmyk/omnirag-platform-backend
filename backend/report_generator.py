import re
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib import colors
import io
from datetime import datetime

def sanitize_text(text: str) -> str:
    if not text:
        return text
    replacements = {
        "\u2010": "-", "\u2011": "-", "\u2012": "-", "\u2013": "-",
        "\u2014": "-", "\u2015": "-", "\u2212": "-", "\u00ad": "-",
        "\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"',
        "\u2022": "-", "\u2026": "...", "\u00a0": " ",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    # Catch-all: strip any remaining character outside the standard font's range
    text = re.sub(r"[^\x00-\xFF]", "", text)
    return text

def generate_query_report(task_data: dict) -> io.BytesIO:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.75*inch, bottomMargin=0.75*inch)
    styles = getSampleStyleSheet()

    heading_style = ParagraphStyle(
        "SectionHeading", parent=styles["Heading2"], spaceBefore=16, spaceAfter=8,
        textColor=colors.HexColor("#1E40AF")
    )
    body_style = ParagraphStyle(
        "Body", parent=styles["Normal"], spaceAfter=8, leading=16
    )

    elements = []

    elements.append(Paragraph("OmniRAG Query Report", styles["Title"]))
    elements.append(Paragraph(
        datetime.now().strftime("Generated on %B %d, %Y at %I:%M %p"),
        styles["Normal"]
    ))
    elements.append(Spacer(1, 16))

    elements.append(Paragraph("Question", heading_style))
    elements.append(Paragraph(sanitize_text(task_data.get("question", "N/A")), body_style))

    if task_data.get("search_query"):
        elements.append(Paragraph("Refined Search Query", heading_style))
        elements.append(Paragraph(sanitize_text(task_data["search_query"]), body_style))

    elements.append(Paragraph("Retrieved Context", heading_style))
    retrieved_docs = task_data.get("retrieved_docs") or []
    if retrieved_docs:
        for i, chunk in enumerate(retrieved_docs, 1):
            clean_chunk = sanitize_text(chunk).replace("\n", "<br/>")
            elements.append(Paragraph(f"<b>Passage {i}:</b>", body_style))
            elements.append(Paragraph(clean_chunk, body_style))
            elements.append(Spacer(1, 6))
    else:
        elements.append(Paragraph("No context retrieved.", body_style))

    elements.append(Paragraph("Answer", heading_style))
    elements.append(Paragraph(sanitize_text(task_data.get("answer", "N/A")), body_style))

    elements.append(Paragraph("Evaluation", heading_style))
    elements.append(Paragraph(
        f"Result: {task_data.get('evaluation', 'N/A')} &nbsp;&nbsp;|&nbsp;&nbsp; "
        f"Attempts: {task_data.get('attempts', 'N/A')}",
        body_style
    ))

    doc.build(elements)
    buffer.seek(0)
    return buffer