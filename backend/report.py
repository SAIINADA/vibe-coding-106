from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generate_pdf(matches, percent, path="plagiarism_report.pdf"):
    c = canvas.Canvas(path, pagesize=A4)
    y = 800
    c.drawString(40, y, f"Plagiarism Percentage: {percent}%")
    y -= 30

    for m in matches:
        c.drawString(
            40, y,
            f"{m['source_file']} (Page {m['page']}) - {m['similarity']}%"
        )
        y -= 20

    c.save()
    return path
