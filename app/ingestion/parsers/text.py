from pathlib import Path

from app.domain.models import ParsedDocument, ParsedPage
from app.ingestion.parsers.base import register


class TextParser:
    extensions = (".txt", ".md")

    def parse(self, path: Path) -> ParsedDocument:
        raw = path.read_bytes()
        for encoding in ("utf-8-sig", "cp1256"):  # cp1256 = legacy Windows Arabic
            try:
                text = raw.decode(encoding)
                break
            except UnicodeDecodeError:
                continue
        else:
            text = raw.decode("utf-8", errors="replace")
        return ParsedDocument(pages=[ParsedPage(number=1, text=text)])


register(TextParser())