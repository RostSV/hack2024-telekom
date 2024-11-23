import pdfplumber

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text content from a PDF file using pdfplumber.
    """
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

def save_uploaded_file(file, file_path: str):
    """
    Save the uploaded file to the server's file system.
    """
    with open(file_path, "wb") as f:
        f.write(file)
