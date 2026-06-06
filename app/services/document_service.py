from io import BytesIO

import pdfplumber
from docx import Document as DocxDocument


def extract_text(file_bytes: bytes, file_type: str) -> str:
    if file_type in {"txt", "md"}:
        return file_bytes.decode("utf-8", errors="ignore")
    if file_type == "pdf":
        return _extract_pdf_text(file_bytes)
    if file_type == "docx":
        return _extract_docx_text(file_bytes)
    raise ValueError(f"Unsupported file type: {file_type}")


def _extract_pdf_text(file_bytes: bytes) -> str:
    parts: list[str] = []
    with pdfplumber.open(BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            parts.append(page.extract_text() or "")
    return "\n".join(parts).strip()


def _extract_docx_text(file_bytes: bytes) -> str:
    document = DocxDocument(BytesIO(file_bytes))
    return "\n".join(paragraph.text for paragraph in document.paragraphs).strip()
