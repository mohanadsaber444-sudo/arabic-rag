from app.ingestion.normalize import clean_text


def test_presentation_forms_become_normal_letters():
    shaped = "\ufee3\ufeae\ufea3\ufe92\ufe8e"  # "مرحبا" written with positional forms
    assert shaped != "مرحبا"
    assert clean_text(shaped) == "مرحبا"


def test_joins_words_split_by_hyphen_at_line_end():
    assert clean_text("inter-\nnational") == "international"


def test_collapses_spaces_and_blank_lines():
    assert clean_text("a    b\n\n\n\nc") == "a b\n\nc"


def test_windows_newlines_are_unified():
    assert clean_text("a\r\nb") == "a\nb"