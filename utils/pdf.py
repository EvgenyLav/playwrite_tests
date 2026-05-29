import re

import fitz  # PyMuPDF


def is_pdf(path: str) -> bool:
    with open(path, "rb") as f:
        return f.read(4) == b"%PDF"


def extract_text(path: str) -> str:
    doc = fitz.open(path)
    return "".join(page.get_text() for page in doc)


def digits_only(text: str) -> str:
    return re.sub(r"\D", "", text)
