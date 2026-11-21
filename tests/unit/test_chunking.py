from app.ingestion.chunking import split_text

ARABIC = "الشركة تقدم خدمات الأتمتة والمساعد الذكي للعملاء في السودان والسعودية والإمارات ومصر"


def long_text(words=400):
    return " ".join(ARABIC.split()[i % 12] for i in range(words)) + "."


def test_short_text_is_one_chunk():
    assert split_text("نص قصير", 800, 120) == ["نص قصير"]


def test_empty_text_gives_no_chunks():
    assert split_text("   \n  ", 800, 120) == []


def test_no_chunk_exceeds_the_size():
    chunks = split_text(long_text(), 800, 120)
    assert len(chunks) > 1
    assert all(len(c) <= 800 for c in chunks)


def test_consecutive_chunks_share_some_text():
    chunks = split_text(long_text(), 800, 120)
    for first, second in zip(chunks, chunks[1:]):
        assert set(first.split()[-5:]) & set(second.split()[:15])


def test_words_are_never_cut_in_the_middle():
    text = long_text()
    original = set(text.split())
    for chunk in split_text(text, 800, 120):
        assert set(chunk.split()) <= original


def test_no_word_is_lost():
    text = long_text()
    kept = {w for c in split_text(text, 800, 120) for w in c.split()}
    assert set(text.split()) <= kept


def test_paragraph_break_is_preferred_over_cutting_a_sentence():
    first = "الفقرة الأولى " * 30
    second = "الفقرة الثانية " * 30
    chunks = split_text(first.strip() + "\n\n" + second.strip(), 500, 0)
    assert chunks[0] == first.strip()


def test_one_huge_word_is_cut_by_size():
    assert [len(c) for c in split_text("x" * 2000, 800, 120)] == [800, 800, 400]


def test_same_input_gives_the_same_chunks():
    text = long_text()
    assert split_text(text, 800, 120) == split_text(text, 800, 120)