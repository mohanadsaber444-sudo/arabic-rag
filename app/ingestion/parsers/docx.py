from pathlib import Path

import docx  # package name: python-docx

from app.domain.models import ParsedDocument, ParsedPage
from app.ingestion.parsers.base import register


class DocxParser:
    extensions = (".docx",)

    def parse(self, path: Path) -> ParsedDocument:
        document = docx.Document(str(path))
        paragraphs = [p.text for p in document.paragraphs if p.text.strip()]
        # DOCX has no fixed pages, so the whole file is treated as page 1
        return ParsedDocument(pages=[ParsedPage(number=1, text="\n\n".join(paragraphs))])


register(DocxParser())