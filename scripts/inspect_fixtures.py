from pathlib import Path

import app.ingestion.parsers  # noqa: F401  (registers the parsers)
from app.domain.errors import RagError
from app.ingestion.detector import validate_upload
from app.ingestion.normalize import clean_text
from app.ingestion.parsers.base import get_parser

FIXTURES = Path("tests/fixtures")
OUT = Path("data/inspect")
OUT.mkdir(parents=True, exist_ok=True)


def shaped_count(text: str) -> int:
    """Letters stored as positional forms: a known symptom of PDF extraction."""
    return sum(1 for c in text if "\ufb50" <= c <= "\ufdff" or "\ufe70" <= c <= "\ufeff")


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
    raw = "\n".join(p.text for p in parsed.pages)
    cleaned = clean_text(raw)
    (OUT / f"{path.stem}.txt").write_text(cleaned, encoding="utf-8")
    print(
        f"{path.name}: pages={len(parsed.pages)} chars={len(cleaned)} "
        f"needs_ocr={parsed.needs_ocr} shaped_raw={shaped_count(raw)}"
    )