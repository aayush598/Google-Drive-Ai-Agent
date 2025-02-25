from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def generate_pdf_from_analysis(analysis, filename="log_analysis.pdf"):
    """Creates a PDF report from the log analysis."""
    pdf_path = os.path.join("static", "reports", filename)

    # Ensure the directory exists
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

    # Create a PDF
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 50, "Log Analysis Report")

    c.setFont("Helvetica", 12)
    y_position = height - 100

    # Write Summary
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, y_position, "Summary:")
    c.setFont("Helvetica", 12)
    y_position -= 20
    c.drawString(100, y_position, analysis["summary"])
    y_position -= 30

    # Write Common Patterns
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, y_position, "Common Patterns:")
    c.setFont("Helvetica", 12)
    y_position -= 20
    for pattern in analysis["common_patterns"]:
        c.drawString(120, y_position, f"- {pattern}")
        y_position -= 20

    # Write Anomalies Detected
    c.setFont("Helvetica-Bold", 14)
    y_position -= 10
    c.drawString(100, y_position, "Anomalies Detected:")
    c.setFont("Helvetica", 12)
    y_position -= 20
    for anomaly in analysis["anomalies_detected"]:
        c.drawString(120, y_position, f"- {anomaly}")
        y_position -= 20

    # Write Recommendations
    c.setFont("Helvetica-Bold", 14)
    y_position -= 10
    c.drawString(100, y_position, "Recommendations:")
    c.setFont("Helvetica", 12)
    y_position -= 20
    for recommendation in analysis["recommendations"]:
        c.drawString(120, y_position, f"- {recommendation}")
        y_position -= 20

    # Save PDF
    c.save()

    return pdf_path
