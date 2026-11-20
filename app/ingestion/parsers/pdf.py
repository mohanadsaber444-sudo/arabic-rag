from pathlib import Path

import pdfplumber

from app.domain.models import ParsedDocument, ParsedPage
from app.ingestion.parsers.base import register
from app.ingestion.parsers.pdf_layout import page_text, remove_repeated_lines


class PdfParser:
    extensions = (".pdf",)
    min_chars_per_page = 25

    def parse(self, path: Path) -> ParsedDocument:
        with pdfplumber.open(path) as pdf:
            texts = [page_text(page) for page in pdf.pages]
        pages = [
            ParsedPage(number=number, text=text)
            for number, text in enumerate(remove_repeated_lines(texts), start=1)
        ]
        empty = sum(1 for p in pages if len(p.text.strip()) < self.min_chars_per_page)
        needs_ocr = bool(pages) and empty / len(pages) > 0.5
        return ParsedDocument(pages=pages, needs_ocr=needs_ocr)


register(PdfParser())