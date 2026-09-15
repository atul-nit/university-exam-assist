# Phase A/B implementation notes

Phase A converts a PDF into `PDFDocument`, preserving each page. Phase B converts page text into `QuestionPaper` with sections, questions, subquestions and marks.

Keep original page text available so later LLM validation can audit every extracted field against the source.

Known next improvements: OCR for scanned PDFs, alternate numbering formats, two-column layouts, tables/diagrams, repeated headers/footers, and LLM-assisted validation.
