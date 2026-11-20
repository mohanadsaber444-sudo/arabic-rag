from app.ingestion.parsers.pdf_layout import remove_repeated_lines

HEADER = "أفق للحلول الرقمية | كتالوج الأسعار · الإصدار 1.0"


def page(body, number, total=4):
    return f"{HEADER}\n{body}\nسري — للعملاء المحتملين فقط | {number} / {total}"


def test_repeated_header_and_footer_are_removed_from_later_pages():
    pages = [page("نص الصفحة الأولى", n) for n in range(1, 5)]
    pages = [p.replace("نص الصفحة الأولى", f"محتوى {n}") for n, p in enumerate(pages, start=1)]
    cleaned = remove_repeated_lines(pages)
    assert cleaned[0].splitlines()[0] == HEADER  # first page keeps it
    assert cleaned[1] == "محتوى 2"
    assert cleaned[3] == "محتوى 4"


def test_page_numbers_do_not_prevent_matching():
    pages = [page(f"محتوى {n}", n) for n in range(1, 5)]
    assert all("سري" not in p for p in remove_repeated_lines(pages)[1:])


def test_repeated_line_in_the_middle_of_a_page_is_kept():
    body = "سطر أول\nسطر متكرر\nسطر ثالث\nسطر رابع\nسطر خامس"
    pages = [f"{HEADER}\n{body}\nتذييل {n}" for n in range(3)]
    cleaned = remove_repeated_lines(pages)
    assert "سطر متكرر" in cleaned[1]


def test_a_line_that_appears_on_one_page_only_is_kept():
    pages = [page(f"محتوى {n}", n) for n in range(1, 6)]
    pages[2] = "عنوان خاص بهذه الصفحة\n" + pages[2]
    assert "عنوان خاص بهذه الصفحة" in remove_repeated_lines(pages)[2]


def test_single_page_document_is_unchanged():
    only = [page("محتوى", 1, 1)]
    assert remove_repeated_lines(only) == only