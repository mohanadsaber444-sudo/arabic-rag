from app.domain.models import Document, ParsedDocument, ParsedPage
from app.ingestion.chunking import chunk_document, detect_language

ARABIC = "الشركة تقدم خدمات الأتمتة والمساعد الذكي للعملاء في السودان والسعودية والإمارات ومصر"


def make_doc(version=1):
    return Document(id="doc-1", collection="hr", filename="policy.pdf", content_hash="h", version=version)


def make_parsed():
    page1 = " ".join(["صفحة أولى"] * 200) + "."
    page2 = "Second page is written in English only."
    return ParsedDocument(pages=[ParsedPage(number=1, text=page1), ParsedPage(number=2, text=page2)])


def test_language_of_arabic_english_mixed_and_numbers():
    assert detect_language(ARABIC) == "ar"
    assert detect_language("The notice period is 30 days") == "en"
    assert detect_language("الباقة Starter تكلف USD 350 شهرياً") == "mixed"
    assert detect_language("350 / 900 | 2,500") == "unknown"


def test_chunks_carry_the_metadata_of_their_document():
    chunk = chunk_document(make_doc(), make_parsed(), 800, 120)[0]
    assert (chunk.filename, chunk.collection, chunk.document_id, chunk.document_version) == ("policy.pdf", "hr", "doc-1", 1)


def test_ordinals_run_across_pages_without_gaps():
    chunks = chunk_document(make_doc(), make_parsed(), 800, 120)
    assert [c.ordinal for c in chunks] == list(range(len(chunks)))


def test_a_chunk_never_crosses_a_page():
    chunks = chunk_document(make_doc(), make_parsed(), 800, 120)
    assert {c.page for c in chunks} == {1, 2}
    assert all("Second" not in c.text for c in chunks if c.page == 1)
    assert all("أولى" not in c.text for c in chunks if c.page == 2)


def test_language_is_set_per_chunk():
    chunks = chunk_document(make_doc(), make_parsed(), 800, 120)
    assert chunks[0].language == "ar"
    assert chunks[-1].language == "en"


def test_ids_are_stable_and_unique():
    first = chunk_document(make_doc(), make_parsed(), 800, 120)
    second = chunk_document(make_doc(), make_parsed(), 800, 120)
    assert [c.id for c in first] == [c.id for c in second]
    assert len({c.id for c in first}) == len(first)


def test_a_new_version_gets_new_ids():
    v1 = chunk_document(make_doc(1), make_parsed(), 800, 120)
    v2 = chunk_document(make_doc(2), make_parsed(), 800, 120)
    assert not {c.id for c in v1} & {c.id for c in v2}


def test_blank_pages_give_no_chunks():
    parsed = ParsedDocument(pages=[ParsedPage(number=1, text="   \n "), ParsedPage(number=2, text="نص صالح")])
    chunks = chunk_document(make_doc(), parsed, 800, 120)
    assert [c.page for c in chunks] == [2]