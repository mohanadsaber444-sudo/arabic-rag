from pathlib import Path

import pymupdf

from app.domain.models import ParsedDocument, ParsedPage
from app.ingestion.parsers.base import register


class PdfParser:
    extensions = (".pdf",)
    min_chars_per_page = 25

    def parse(self, path: Path) -> ParsedDocument:
        pages: list[ParsedPage] = []
        with pymupdf.open(path) as doc:
            for number, page in enumerate(doc, start=1):
                pages.append(ParsedPage(number=number, text=page.get_text("text")))
        empty = sum(1 for p in pages if len(p.text.strip()) < self.min_chars_per_page)
        needs_ocr = bool(pages) and empty / len(pages) > 0.5
        return ParsedDocument(pages=pages, needs_ocr=needs_ocr)


register(PdfParser())