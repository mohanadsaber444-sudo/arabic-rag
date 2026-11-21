from collections import Counter
from pathlib import Path

import app.ingestion.parsers  # noqa: F401  (registers the parsers)
from app.domain.errors import RagError
from app.domain.models import Document
from app.ingestion.chunking import chunk_document
from app.ingestion.detector import validate_upload
from app.ingestion.parsers.base import get_parser

FIXTURES = Path("tests/fixtures")
OUT = Path("data/inspect")
OUT.mkdir(parents=True, exist_ok=True)
SIZE, OVERLAP = 800, 120

for path in sorted(FIXTURES.iterdir()):
    if not path.is_file():
        continue
    data = path.read_bytes()
    try:
        ext = validate_upload(path.name, data[:8], len(data), 25 * 1024 * 1024)
        parsed = get_parser(ext).parse(path)
    except RagError as exc:
        print(f"{path.name}: ERROR {type(exc).__name__}: {exc}")
        continue
    doc = Document(id=path.stem, collection="inspect", filename=path.name, content_hash="-")
    chunks = chunk_document(doc, parsed, SIZE, OVERLAP)
    sizes = [len(c.text) for c in chunks] or [0]
    blocks = [f"[{c.ordinal}] page={c.page} lang={c.language} chars={len(c.text)}\n{c.text}" for c in chunks]
    (OUT / f"chunks_{path.stem}.txt").write_text("\n\n=========\n\n".join(blocks), encoding="utf-8")
    print(
        f"{path.name}: pages={len(parsed.pages)} chunks={len(chunks)} "
        f"min={min(sizes)} avg={sum(sizes) // len(sizes)} max={max(sizes)} "
        f"langs={dict(Counter(c.language for c in chunks))} needs_ocr={parsed.needs_ocr}"
    )