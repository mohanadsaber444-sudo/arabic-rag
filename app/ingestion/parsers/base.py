from pathlib import Path
from typing import Protocol

from app.domain.errors import UnsupportedFileTypeError
from app.domain.models import ParsedDocument


class Parser(Protocol):
    extensions: tuple[str, ...]

    def parse(self, path: Path) -> ParsedDocument: ...


_REGISTRY: dict[str, Parser] = {}


def register(parser: Parser) -> None:
    for ext in parser.extensions:
        _REGISTRY[ext] = parser


def get_parser(ext: str) -> Parser:
    try:
        return _REGISTRY[ext]
    except KeyError:
        raise UnsupportedFileTypeError(f"No parser for {ext}") from None