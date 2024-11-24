import pdfplumber
from docx import Document
import subprocess

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text content from a PDF file using pdfplumber.
    """
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

def extract_text_from_docx(docx_path: str) -> str:
    """
    Extract text content from a DOCX file using python-docx.
    """
    doc = Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_doc(doc_path: str) -> str:
    """
    Extract text content from a DOC file using antiword.
    """
    result = subprocess.run(['antiword', doc_path], stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8')

def save_uploaded_file(file, file_path: str):
    """
    Save the uploaded file to the server's file system.
    """
    with open(file_path, "wb") as f:
        f.write(file)
