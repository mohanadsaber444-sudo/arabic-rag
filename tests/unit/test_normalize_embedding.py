from app.ingestion.normalize import normalize_for_embedding


def test_diacritics_and_alef_forms_are_unified():
    assert normalize_for_embedding("\u0623\u064e\u062d\u0652\u0645\u064e\u062f") == "\u0627\u062d\u0645\u062f"


def test_tatweel_is_removed():
    assert normalize_for_embedding("\u0645\u0640\u062d\u0645\u0640\u062f") == "\u0645\u062d\u0645\u062f"


def test_arabic_indic_digits_become_western():
    assert normalize_for_embedding("\u0662\u0660\u0662\u0666") == "2026"


def test_alef_maqsura_becomes_ya():
    assert normalize_for_embedding("\u0645\u0635\u0631\u0649") == "\u0645\u0635\u0631\u064a"


def test_taa_marbuta_is_not_changed():
    word = "\u0645\u062f\u0631\u0633\u0629"
    assert normalize_for_embedding(word) == word