import argparse
from pathlib import Path
from app.ingestion.pdf_loader import extract_pdf
from app.extraction.question_parser import QuestionPaperParser
from app.utils.json_writer import write_json


def process(path, out):
    result = QuestionPaperParser().parse(extract_pdf(path))
    out.mkdir(parents=True, exist_ok=True)
    dest = out / f"{path.stem}.json"
    write_json(dest, result.model_dump(mode="json"))
    print(f"Processed {path}: {result.total_questions} questions -> {dest}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--output", default="data/processed")
    a = p.parse_args()
    src = Path(a.input)
    out = Path(a.output)
    if src.is_file():
        process(src, out)
    elif src.is_dir():
        for f in sorted(src.glob("*.pdf")):
            process(f, out)
    else:
        raise FileNotFoundError(src)


if __name__ == "__main__":
    main()
