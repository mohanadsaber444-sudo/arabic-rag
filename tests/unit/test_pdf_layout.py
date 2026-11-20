from app.ingestion.parsers.pdf_layout import group_lines, line_text

WIDTH = 5.0


def visual(*segments, x=0.0, top=0.0):
    """Build characters as a PDF stores them: left to right on the page.

    Each segment is (text, is_ltr) in LOGICAL order; Arabic segments are drawn reversed.
    """
    chars = []
    for text, ltr in reversed(segments):
        for ch in text if ltr else text[::-1]:
            chars.append({"text": ch, "x0": x, "x1": x + WIDTH, "top": top, "bottom": top + 10, "size": 10})
            x += WIDTH
    return chars


def test_arabic_words_read_right_to_left():
    chars = visual(("سياسة", False), (" ", False), ("مستوى", False), (" ", False), ("الخدمة", False))
    assert line_text(chars) == "سياسة مستوى الخدمة"


def test_latin_phrase_inside_arabic_keeps_its_order():
    chars = visual(("عبر", False), (" ", False), ("Ticket Portal", True), (" ", False), ("كتابيا", False))
    assert line_text(chars, page_rtl=True) == "عبر Ticket Portal كتابيا"


def test_number_and_currency_keep_their_order():
    chars = visual(("السعر", False), (" ", False), ("350", True), (" ", False), ("USD", True))
    assert line_text(chars) == "السعر 350 USD"


def test_numbers_with_separators_are_not_reversed():
    chars = visual(("الحد", False), (" ", False), ("1,000", True), (" ", False), ("و", False), ("08:00", True))
    assert line_text(chars) == "الحد 1,000 و08:00"


def test_page_counter_keeps_its_order():
    chars = visual(("صفحة", False), (" ", False), ("1", True), (" / ", False), ("5", True))
    assert line_text(chars) == "صفحة 1 / 5"


def test_wide_gap_marks_table_cells():
    right = visual(("البند", False), x=100)
    left = visual(("نعم", False), x=0)
    assert line_text(left + right) == "البند | نعم"


def test_diacritics_are_ignored():
    chars = visual(("يوماً", False))
    assert line_text(chars) == "يوما"


def test_english_line_reads_left_to_right():
    chars = visual(("Hello world", True))
    assert line_text(chars) == "Hello world"


def test_lines_are_split_by_vertical_position():
    first = visual(("أول", False), top=0)
    second = visual(("ثان", False), top=30)
    assert len(group_lines(second + first)) == 2


def test_english_line_on_an_arabic_page_stays_left_to_right():
    chars = visual(("Hello world", True))
    assert line_text(chars, page_rtl=True) == "Hello world"




def test_percent_sign_stays_attached_to_its_number():
    chars = visual(("خصم", False), (" ", False), ("15%", True))
    assert line_text(chars) == "خصم 15%"


def test_range_with_dash_keeps_reading_order():
    chars = visual(("المدة", False), (" ", False), ("20", True), ("–", False), ("30", True))
    assert line_text(chars) == "المدة 20–30"


def test_mirrored_brackets_are_swapped_back():
    # this PDF stores the opening bracket as ")" and the closing one as "(" (their mirrored shapes)
    chars = visual(("رسوم", False), (" ", False), (")", False), ("مرة", False), ("(", False))
    assert line_text(chars) == "رسوم (مرة)"


def test_correctly_stored_brackets_are_left_alone():
    chars = visual(("رسوم", False), (" ", False), ("(", False), ("مرة", False), (")", False))
    assert line_text(chars) == "رسوم (مرة)"


def test_a_lone_closing_bracket_is_left_alone():
    chars = visual(("أ", False), (")", False), (" ", False), ("نص", False))
    assert line_text(chars) == "أ) نص"    