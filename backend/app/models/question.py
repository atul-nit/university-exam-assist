from pydantic import BaseModel, Field


class SubQuestion(BaseModel):
    label: str
    text: str
    marks: float | None = None
    page_number: int | None = None


class Question(BaseModel):
    question_number: int
    text: str
    marks: float | None = None
    section: str | None = None
    page_number: int | None = None
    sub_questions: list[SubQuestion] = Field(default_factory=list)


class Section(BaseModel):
    name: str
    marks: float | None = None
    instructions: list[str] = Field(default_factory=list)
    questions: list[Question] = Field(default_factory=list)


class QuestionPaper(BaseModel):
    document: dict
    sections: list[Section] = Field(default_factory=list)

    @property
    def total_questions(self) -> int:
        return sum(len(s.questions) for s in self.sections)
