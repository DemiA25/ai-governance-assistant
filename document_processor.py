import pdfplumber
from docx import Document
import io


def extract_text_from_pdf(file) -> str:
    """Extract text from uploaded PDF file."""
    text_chunks = []
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_chunks.append(page_text)
    return "\n\n".join(text_chunks)


def extract_text_from_docx(file) -> str:
    """Extract text from uploaded DOCX file."""
    doc = Document(io.BytesIO(file.read()))
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    return "\n\n".join(paragraphs)


def process_document(uploaded_file) -> str:
    """Route to correct extractor based on file type."""
    file_type = uploaded_file.name.split(".")[-1].lower()

    if file_type == "pdf":
        return extract_text_from_pdf(uploaded_file)
    elif file_type in ("docx", "doc"):
        return extract_text_from_docx(uploaded_file)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")


def truncate_text(text: str, max_words: int = 6000) -> str:
    """Truncate text to avoid exceeding LLM context limits."""
    words = text.split()
    if len(words) > max_words:
        return " ".join(words[:max_words]) + "\n\n[Document truncated for processing]"
    return text