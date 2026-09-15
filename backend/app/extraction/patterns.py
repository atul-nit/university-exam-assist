import re

QUESTION_RE = re.compile(r"^(?P<number>\d{1,3})\.\s*(?P<text>.*)$")
SUBQUESTION_RE = re.compile(r"^\((?P<label>[a-zA-Z])\)\s*(?P<text>.*)$")
SECTION_RE = re.compile(r"^section\s*[-–—]?\s*(?P<name>[A-Za-z]+)", re.I)
