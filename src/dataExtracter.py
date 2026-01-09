import os
import csv
import pdfplumber
from docx import Document
from bs4 import BeautifulSoup

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
    if (os.path.exists(path)):
        if path.endswith(".pdf"):
            return extract_pdf_data(path)
        elif path.endswith(".docx"):
            return extract_docx_data(path)
        elif path.endswith(".txt") or path.endswith(".json") or path.endswith(".md"):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception as e:
                print(f"Error reading {path}: {e}")
                return ""
        elif path.endswith(".csv"):
            try:
                 with open(path, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    return '\n'.join([', '.join(row) for row in reader])
            except Exception as e:
                print(f"Error reading {path}: {e}")
                return ""
        elif path.endswith(".html"):
            try:
                 with open(path, 'r', encoding='utf-8') as f:
                    with open(path, 'r', encoding='utf-8') as f:
                        html = f.read()
                    soup = BeautifulSoup(html, 'html.parser')
                    return soup.get_text(separator='\n', strip=True)
            except Exception as e:
                print(f"Error reading {path}: {e}")
                return ""
        else:
            raise ValueError("Unsupported file type")
    else:
        print("Error: file doesn't exist")
        return ""

