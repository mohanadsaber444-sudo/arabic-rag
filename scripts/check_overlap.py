from pathlib import Path

import app.ingestion.parsers  # noqa: F401  (registers the parsers)
from app.domain.errors import RagError
from app.domain.models import Document
from app.ingestion.chunking import chunk_document
from app.ingestion.detector import validate_upload
from app.ingestion.parsers.base import get_parser

SIZE, OVERLAP = 800, 120


def shared_length(previous: str, following: str) -> int:
    """How many characters at the end of `previous` are repeated at the start of `following`."""
    previous = previous.rstrip()
    for length in range(min(len(previous), len(following), OVERLAP + 20), 0, -1):
        if following.startswith(previous[-length:]):
            return length
    return 0


for path in sorted(Path("tests/fixtures").iterdir()):
    if not path.is_file():
        continue
    data = path.read_bytes()
    try:
        ext = validate_upload(path.name, data[:8], len(data), 25 * 1024 * 1024)
        parsed = get_parser(ext).parse(path)
    except RagError:
        continue
    doc = Document(id=path.stem, collection="inspect", filename=path.name, content_hash="-")
    chunks = chunk_document(doc, parsed, SIZE, OVERLAP)
    pairs = [(a, b) for a, b in zip(chunks, chunks[1:]) if a.page == b.page]
    lengths = [shared_length(a.text, b.text) for a, b in pairs]
    with_overlap = sum(1 for n in lengths if n >= 20)
    print(f"{path.name}: chunk pairs on the same page={len(pairs)} with overlap={with_overlap} lengths={lengths}")