from app.ingestion.parsers import text  # noqa: F401  (importing registers the parser)
from app.ingestion.parsers.base import get_parser

ARABIC = "مرحبا بالعالم"


def test_reads_utf8_arabic(tmp_path):
    f = tmp_path / "a.txt"
    f.write_bytes(ARABIC.encode("utf-8"))
    assert get_parser(".txt").parse(f).pages[0].text == ARABIC


def test_reads_legacy_windows_arabic(tmp_path):
    f = tmp_path / "b.txt"
    f.write_bytes(ARABIC.encode("cp1256"))
    assert get_parser(".txt").parse(f).pages[0].text == ARABIC


def test_md_is_registered_too():
    assert get_parser(".md") is get_parser(".txt")