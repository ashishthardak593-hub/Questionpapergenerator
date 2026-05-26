from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet


def create_pdf(paper_text):

    filename = "question_paper.pdf"

    doc = SimpleDocTemplate(
        filename,
        pagesize=A4
    )

    styles = getSampleStyleSheet()

    story = []

    lines = paper_text.split('\n')

    for line in lines:

        if line.strip():

            story.append(
                Paragraph(
                    line,
                    styles['Normal']
                )
            )

            story.append(
                Spacer(1, 8)
            )

    doc.build(story)

    return filename