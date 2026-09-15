import re


def extract_first_mark(text):
    m = re.search(r"(?P<marks>\d+(?:\.\d+)?)\s*marks?\b", text, re.I)
    return float(m.group("marks")) if m else None


def extract_total_from_multiplication(text):
    m = re.search(r"=\s*(?P<marks>\d+(?:\.\d+)?)\s*marks?\b", text, re.I)
    return float(m.group("marks")) if m else None
