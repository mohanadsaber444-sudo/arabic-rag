import pytest

from app.domain.errors import FileTooLargeError, UnsupportedFileTypeError
from app.ingestion.detector import validate_upload


def test_valid_pdf_returns_extension():
    assert validate_upload("a.PDF", b"%PDF-1.7", 100, 1000) == ".pdf"


def test_text_file_needs_no_signature():
    assert validate_upload("notes.md", b"# hello", 10, 1000) == ".md"


def test_unknown_extension_is_rejected():
    with pytest.raises(UnsupportedFileTypeError):
        validate_upload("virus.exe", b"MZ", 100, 1000)


def test_fake_pdf_is_rejected():
    with pytest.raises(UnsupportedFileTypeError):
        validate_upload("a.pdf", b"MZ", 100, 1000)


def test_too_large_file_is_rejected():
    with pytest.raises(FileTooLargeError):
        validate_upload("a.pdf", b"%PDF", 2000, 1000)