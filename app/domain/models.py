from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class DocumentStatus(StrEnum):
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"


class Document(BaseModel):
    id: str
    collection: str
    filename: str
    content_hash: str  # sha256 of the file bytes, used for duplicate detection
    version: int = 1
    language: str | None = None
    status: DocumentStatus = DocumentStatus.PROCESSING
    error: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class ParsedPage(BaseModel):
    number: int  # 1-based page number
    text: str


class ParsedDocument(BaseModel):
    pages: list[ParsedPage]
    needs_ocr: bool = False  # True when the file is a scan with no text layer






class Chunk(BaseModel):
    id: str
    document_id: str
    document_version: int
    collection: str
    filename: str
    ordinal: int  # position of the chunk inside the document
    page: int | None = None
    section: str | None = None
    language: str | None = None
    text: str  # original text, shown to the user and the LLM


class RetrievedChunk(BaseModel):
    chunk: Chunk
    score: float


class Citation(BaseModel):
    chunk_id: str
    filename: str
    page: int | None = None
    quote: str


class Answer(BaseModel):
    text: str
    citations: list[Citation] = []
    sources: list[RetrievedChunk] = []
    grounded: bool = True  # False when the system answered "not enough information"