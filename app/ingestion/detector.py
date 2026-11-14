from pathlib import Path

from app.domain.errors import FileTooLargeError, UnsupportedFileTypeError

ALLOWED = {".pdf", ".docx", ".txt", ".md"}
MAGIC = {".pdf": b"%PDF", ".docx": b"PK"}  # txt and md have no signature


def validate_upload(filename: str, head: bytes, size: int, max_bytes: int) -> str:
    """Return the normalized extension or raise a domain error."""
    ext = Path(filename).suffix.lower()
    if ext not in ALLOWED:
        raise UnsupportedFileTypeError(f"Unsupported file type: {ext or 'none'}")
    if size > max_bytes:
        raise FileTooLargeError(f"File is {size} bytes; limit is {max_bytes}")
    signature = MAGIC.get(ext)
    if signature and not head.startswith(signature):
        raise UnsupportedFileTypeError("File content does not match its extension")
    return ext