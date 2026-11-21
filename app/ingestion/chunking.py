# strongest first: paragraph, line, sentence end, Arabic question mark, semicolon, comma, space
import uuid

from app.domain.models import Chunk, Document, ParsedDocument
from app.ingestion.normalize import clean_text

_NAMESPACE = uuid.UUID("6f1c1b9e-3b0a-4c58-9a57-2f4c5b0d9a11")

SEPARATORS = ["\n\n", "\n", ". ", "\u061f ", "? ", "! ", "\u061b ", "; ", "\u060c ", ", ", " "]


def _pieces(text: str, size: int, separators: list[str]) -> list[str]:
    """Cut the text at the strongest separator available until every piece fits in `size`.

    Each piece keeps its separator at the end, so joining the pieces gives the text back.
    """
    if len(text) <= size:
        return [text]
    for index, sep in enumerate(separators):
        if sep in text:
            parts = text.split(sep)
            pieces: list[str] = []
            for position, part in enumerate(parts):
                piece = part + (sep if position < len(parts) - 1 else "")
                pieces.extend(_pieces(piece, size, separators[index + 1 :]))
            return pieces
    return [text[i : i + size] for i in range(0, len(text), size)]  # one huge word: hard cut


def _overlap_tail(text: str, overlap: int) -> str:
    """The last `overlap` characters of a chunk, starting at a word boundary."""
    if overlap <= 0 or len(text) <= overlap:
        return ""
    start = len(text) - overlap
    if not text[start - 1].isspace():  # we are inside a word: move to the next word
        while start < len(text) and not text[start].isspace():
            start += 1
    return text[start:].lstrip()


def _gap(carry: str, piece: str) -> int:
    """1 when two texts need a space between them, 0 when one already has it."""
    return 0 if not carry or carry[-1].isspace() or piece[:1].isspace() else 1


def split_text(text: str, size: int, overlap: int) -> list[str]:
    text = text.strip()
    if not text:
        return []
    chunks: list[str] = []
    current = ""
    for piece in _pieces(text, size, SEPARATORS):
        if current and len(current) + len(piece) > size:
            chunks.append(current.strip())
            carry = _overlap_tail(current, overlap)
            while carry and len(carry) + _gap(carry, piece) + len(piece) > size:  # drop the oldest words
                words = carry.split(None, 1)
                carry = words[1] if len(words) > 1 else ""
            current = carry + (" " * _gap(carry, piece)) + piece
        else:
            current += piece
    if current.strip():
        chunks.append(current.strip())
    return chunks




def _is_arabic(c: str) -> bool:
    return "\u0600" <= c <= "\u06ff"


def detect_language(text: str) -> str:
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return "unknown"
    ratio = sum(1 for c in letters if _is_arabic(c)) / len(letters)
    return "ar" if ratio > 0.6 else "en" if ratio < 0.2 else "mixed"


def chunk_document(doc: Document, parsed: ParsedDocument, size: int, overlap: int) -> list[Chunk]:
    """Split every page on its own, so a chunk never crosses a page and its citation stays exact."""
    chunks: list[Chunk] = []
    ordinal = 0
    for page in parsed.pages:
        for piece in split_text(clean_text(page.text), size, overlap):
            chunk_id = uuid.uuid5(_NAMESPACE, f"{doc.id}:{doc.version}:{ordinal}")
            chunks.append(
                Chunk(
                    id=str(chunk_id),
                    document_id=doc.id,
                    document_version=doc.version,
                    collection=doc.collection,
                    filename=doc.filename,
                    ordinal=ordinal,
                    page=page.number,
                    language=detect_language(piece),
                    text=piece,
                )
            )
            ordinal += 1
    return chunks