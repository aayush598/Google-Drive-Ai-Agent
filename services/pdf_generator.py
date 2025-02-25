from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
import os

def generate_pdf_from_analysis(analysis, filename="log_analysis.pdf"):
    """Creates a well-formatted PDF report from the log analysis."""
    pdf_path = os.path.join("static", "reports", filename)

    # Ensure the directory exists
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

    # Create PDF canvas
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter
    y_position = height - 50  # Start position for text

    def draw_text_block(title, content_list, font_size=12):
        """Draws a title and a list of text items with proper formatting."""
        nonlocal y_position
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y_position, title)
        y_position -= 20
        c.setFont("Helvetica", font_size)

        for item in content_list:
            wrapped_text = simpleSplit(f"- {item}", "Helvetica", font_size, width - 100)
            for line in wrapped_text:
                c.drawString(70, y_position, line)
                y_position -= 15
            y_position -= 5  # Extra space after each item

        y_position -= 10  # Extra space after each section

    # Title
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, y_position, "Log Analysis Report")
    y_position -= 30

    # Summary
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y_position, "Summary:")
    y_position -= 20
    c.setFont("Helvetica", 12)
    wrapped_summary = simpleSplit(analysis["summary"], "Helvetica", 12, width - 100)
    for line in wrapped_summary:
        c.drawString(50, y_position, line)
        y_position -= 15
    y_position -= 20  # Extra space after summary

    # Sections
    draw_text_block("Common Patterns:", analysis["common_patterns"])
    draw_text_block("Anomalies Detected:", analysis["anomalies_detected"])
    draw_text_block("Recommendations:", analysis["recommendations"])

    # Save PDF
    c.save()

    return pdf_path
