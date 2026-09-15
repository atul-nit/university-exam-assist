import re
from app.extraction.marks_extractor import (
    extract_first_mark,
    extract_total_from_multiplication,
)
from app.extraction.patterns import QUESTION_RE, SUBQUESTION_RE, SECTION_RE
from app.extraction.text_cleaner import normalize_lines
from app.models.question import QuestionPaper, Section, Question, SubQuestion
from app.models.document import PDFDocument


class QuestionPaperParser:
    def parse(self, document: PDFDocument) -> QuestionPaper:
        sections = []
        current_section = None
        current_question = None
        current_sub = None
        for page in document.pages:
            for line in normalize_lines(page.text):
                sm = SECTION_RE.match(line)
                if sm:
                    current_section = Section(
                        name=sm.group("name").upper(), marks=extract_first_mark(line)
                    )
                    sections.append(current_section)
                    current_question = None
                    current_sub = None
                    continue
                qm = QUESTION_RE.match(line)
                if qm and int(qm.group("number")) <= 100:
                    if current_section is None:
                        current_section = Section(name="UNKNOWN")
                        sections.append(current_section)
                    q = Question(
                        question_number=int(qm.group("number")),
                        text=qm.group("text").strip(),
                        section=current_section.name,
                        page_number=page.page_number,
                    )
                    q.marks = extract_total_from_multiplication(
                        line
                    ) or extract_first_mark(line)
                    current_section.questions.append(q)
                    current_question = q
                    current_sub = None
                    continue
                sm = SUBQUESTION_RE.match(line)
                if sm and current_question:
                    sub = SubQuestion(
                        label=sm.group("label").lower(),
                        text=sm.group("text").strip(),
                        marks=extract_first_mark(line),
                        page_number=page.page_number,
                    )
                    current_question.sub_questions.append(sub)
                    current_sub = sub
                    continue
                if current_sub:
                    current_sub.text = f"{current_sub.text} {line}".strip()
                    continue
                if current_question and not line.lower().startswith("page "):
                    current_question.text = f"{current_question.text} {line}".strip()
                    continue
                if current_section and line.lower().startswith(
                    ("attempt", "each question", "note:")
                ):
                    current_section.instructions.append(line)
        for s in sections:
            default = None
            for line in s.instructions:
                m = re.search(
                    r"each\s+question\s+carries\s+(\d+(?:\.\d+)?)\s*marks?", line, re.I
                )
                if m:
                    default = float(m.group(1))
                    break
            for q in s.questions:
                if q.marks is None:
                    q.marks = default
        # return QuestionPaper(document={"file_name":document.file_name,"page_count":document.page_count}, sections=sections)
        return QuestionPaper(
            document={
                "file_name": document.file_name,
                "page_count": document.page_count,
            },
            sections=sections,
        )
