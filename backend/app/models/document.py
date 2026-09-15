from pydantic import BaseModel, Field


class PageText(BaseModel):
    page_number: int
    text: str


class PDFDocument(BaseModel):
    file_name: str
    page_count: int
    pages: list[PageText] = Field(default_factory=list)
