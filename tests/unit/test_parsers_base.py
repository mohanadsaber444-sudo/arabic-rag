from pathlib import Path

import pytest

from app.domain.errors import UnsupportedFileTypeError
from app.domain.models import ParsedDocument, ParsedPage
from app.ingestion.parsers.base import get_parser, register


class FakeParser:
    extensions = (".fake",)

    def parse(self, path: Path) -> ParsedDocument:
        return ParsedDocument(pages=[ParsedPage(number=1, text="hi")])


def test_registered_parser_is_found():
    register(FakeParser())
    assert get_parser(".fake").parse(Path("x")).pages[0].text == "hi"


def test_unknown_extension_raises():
    with pytest.raises(UnsupportedFileTypeError):
        get_parser(".nope")