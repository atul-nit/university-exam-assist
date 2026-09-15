from app.models.document import PDFDocument, PageText
from app.extraction.question_parser import QuestionPaperParser


def test_sample_layout():
    text = """Section –A 30 Marks\n(Each question carries 6 marks)\n1. What is join dependency?\n2. What is object identifier?\n6. Explain constraints. (2*3=6 Marks)\n(a) Cardinality constraints.\n(b) Participation constraints.\n(c) Entity integrity.\nSection – B 20 Marks\n(Each question carries 10 marks)\n7. What is distributed deadlock?\nSection C 20 Marks\n10. (a) Difference between objects and entities. (5 Marks)\n(b) SQL schema. (10 Marks)\n(c) Explain keys. (5 Marks)"""
    r = QuestionPaperParser().parse(
        PDFDocument(
            file_name="x.pdf", page_count=1, pages=[PageText(page_number=1, text=text)]
        )
    )
    assert [s.name for s in r.sections] == ["A", "B", "C"]
    assert r.total_questions == 5
    assert r.sections[0].questions[0].marks == 6
    assert len(r.sections[0].questions[2].sub_questions) == 3
    assert r.sections[1].questions[0].marks == 10
    assert r.sections[2].questions[0].sub_questions[0].marks == 5
