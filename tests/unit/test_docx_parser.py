import docx

from app.ingestion.parsers import docx as docx_parser  # noqa: F401  (registers the parser)
from app.ingestion.parsers.base import get_parser


def test_reads_arabic_paragraphs_and_skips_empty_ones(tmp_path):
    path = tmp_path / "a.docx"
    doc = docx.Document()
    doc.add_paragraph("الفقرة الأولى")
    doc.add_paragraph("")
    doc.add_paragraph("الفقرة الثانية")
    doc.save(str(path))

    parsed = get_parser(".docx").parse(path)

    assert len(parsed.pages) == 1
    assert parsed.pages[0].text == "الفقرة الأولى\n\nالفقرة الثانية"