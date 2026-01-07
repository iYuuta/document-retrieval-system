import pdfplumber
from docx import Document

def extract_pdf_data(path: str):
    text = ""
    with pdfplumber.open(path) as pdf:
         for page in pdf.pages:
            pageText = page.extract_text()
            if pageText:
                text += pageText + "\n"
    return text

def extract_docx_data(path):
    doc = Document(path)
    text = ""
    for para in doc.paragraphs:
        if para:
            text += para.text + "\n"
    return text

def extract_file_data(path):
    if path.endswith(".pdf"):
        return extract_pdf_data(path)
    elif path.endswith(".docx"):
        return extract_docx_data(path)
    elif path.endswith(".txt"):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"Error reading TXT {path}: {e}")
            return ""
    else:
        raise ValueError("Unsupported file type")

