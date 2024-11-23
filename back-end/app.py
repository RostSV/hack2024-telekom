from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from uuid import uuid4
import os
from utils.file_utils import extract_text_from_pdf, save_uploaded_file
from utils.chat_utils import compare_with_gpt

# Create the FastAPI app
app = FastAPI()

# Configure the upload folder path
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI ChatGPT Backend!"}

@app.post("/compare")
async def compare_files(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    """
    Endpoint to compare two PDF files, return differences and improvement suggestions.
    Accepts two files: 'file1' (example file), 'file2' (file to compare).
    """
    # Ensure both files are PDFs
    if file1.content_type != 'application/pdf' or file2.content_type != 'application/pdf':
        raise HTTPException(status_code=400, detail="Both files must be PDFs.")

    # Generate unique filenames for the uploaded files
    file1_path = os.path.join(UPLOAD_FOLDER, f"{uuid4()}_{file1.filename}")
    file2_path = os.path.join(UPLOAD_FOLDER, f"{uuid4()}_{file2.filename}")

    try:
        # Save the uploaded files to the server
        save_uploaded_file(await file1.read(), file1_path)
        save_uploaded_file(await file2.read(), file2_path)

        # Extract text from both PDFs using pdfplumber
        text1 = extract_text_from_pdf(file1_path)
        text2 = extract_text_from_pdf(file2_path)

        # Use ChatGPT to analyze the differences and suggest improvements
        analysis_result = compare_with_gpt(text1, text2)

        # Clean up the uploaded files after processing
        os.remove(file1_path)
        os.remove(file2_path)

        return JSONResponse(content={"analysis": analysis_result}, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing files: {e}")
