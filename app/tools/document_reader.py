from pathlib import Path

from pypdf import PdfReader
from docx import Document

from app.tools.filesystem import resolve_allowed_path


MAX_DOCUMENT_SIZE = 10 * 1024 * 1024  # 10 MB


def read_pdf(path: str):

    file_path = resolve_allowed_path(path)

    if not file_path.exists():
        return {
            "success": False,
            "error": "PDF does not exist."
        }

    if not file_path.is_file():
        return {
            "success": False,
            "error": "Path is not a file."
        }

    if file_path.suffix.lower() != ".pdf":
        return {
            "success": False,
            "error": "The supplied file is not a PDF."
        }

    size = file_path.stat().st_size

    if size > MAX_DOCUMENT_SIZE:
        return {
            "success": False,
            "error": "PDF exceeds the 10 MB size limit."
        }

    try:

        reader = PdfReader(str(file_path))

        pages = []

        for index, page in enumerate(reader.pages):

            text = page.extract_text() or ""

            pages.append({
                "page": index + 1,
                "text": text
            })

        full_text = "\n\n".join(
            page["text"]
            for page in pages
        )

        return {
            "success": True,
            "type": "pdf",
            "path": str(file_path),
            "pages": len(reader.pages),
            "text": full_text
        }

    except Exception as error:

        return {
            "success": False,
            "error": str(error)
        }


def read_docx(path: str):

    file_path = resolve_allowed_path(path)

    if not file_path.exists():
        return {
            "success": False,
            "error": "DOCX does not exist."
        }

    if not file_path.is_file():
        return {
            "success": False,
            "error": "Path is not a file."
        }

    if file_path.suffix.lower() != ".docx":
        return {
            "success": False,
            "error": "The supplied file is not a DOCX."
        }

    size = file_path.stat().st_size

    if size > MAX_DOCUMENT_SIZE:
        return {
            "success": False,
            "error": "DOCX exceeds the 10 MB size limit."
        }

    try:

        document = Document(str(file_path))

        paragraphs = []

        for paragraph in document.paragraphs:

            if paragraph.text.strip():

                paragraphs.append(
                    paragraph.text
                )

        text = "\n\n".join(paragraphs)

        return {
            "success": True,
            "type": "docx",
            "path": str(file_path),
            "paragraphs": len(paragraphs),
            "text": text
        }

    except Exception as error:

        return {
            "success": False,
            "error": str(error)
        }