from pathlib import Path

from pypdf import PdfReader

from app.domain.models import ParsedDocument, ParsedPage
from app.ingestion.parsers.base import register


class PdfParser:
    extensions = (".pdf",)
    min_chars_per_page = 25

    def parse(self, path: Path) -> ParsedDocument:
        reader = PdfReader(str(path))
        pages = [
            ParsedPage(number=number, text=page.extract_text() or "")
            for number, page in enumerate(reader.pages, start=1)
        ]
        empty = sum(1 for p in pages if len(p.text.strip()) < self.min_chars_per_page)
        needs_ocr = bool(pages) and empty / len(pages) > 0.5
        return ParsedDocument(pages=pages, needs_ocr=needs_ocr)


register(PdfParser())