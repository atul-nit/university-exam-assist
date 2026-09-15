from pathlib import Path
import fitz
from app.models.document import PDFDocument, PageText


def extract_pdf(pdf_path: Path) -> PDFDocument:
    if not pdf_path.exists():
        raise FileNotFoundError(pdf_path)
    with fitz.open(pdf_path) as pdf:
        pages = [
            PageText(page_number=i, text=page.get_text("text"))
            for i, page in enumerate(pdf, 1)
        ]
        return PDFDocument(file_name=pdf_path.name, page_count=len(pdf), pages=pages)
