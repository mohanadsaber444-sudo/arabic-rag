import pymupdf

from app.ingestion.parsers import pdf  # noqa: F401  (importing registers the parser)
from app.ingestion.parsers.base import get_parser


def make_pdf(path, texts):
    doc = pymupdf.open()
    for text in texts:
        page = doc.new_page()
        if text:
            page.insert_text((72, 72), text)
    doc.save(str(path))
    doc.close()


def test_one_parsed_page_per_pdf_page(tmp_path):
    path = tmp_path / "a.pdf"
    make_pdf(path, [
        "First page has enough text to count as real text.",
        "Second page also has enough real text in it.",
    ])
    parsed = get_parser(".pdf").parse(path)
    assert [p.number for p in parsed.pages] == [1, 2]
    assert "First page" in parsed.pages[0].text
    assert parsed.needs_ocr is False


def test_pdf_without_text_needs_ocr(tmp_path):
    path = tmp_path / "scan.pdf"
    make_pdf(path, ["", ""])
    assert get_parser(".pdf").parse(path).needs_ocr is True