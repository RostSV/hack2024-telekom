from fastapi import FastAPI, UploadFile, File, Form, HTTPException
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
async def compare_files(
        task: str = Form(...),
        file1: UploadFile = File(None),
        file2: UploadFile = File(None)
):
    """
    Endpoint to compare two PDF files or process a single PDF with a task.
    Accepts a task and up to two files: 'file1' (example file), 'file2' (file to compare).
    """
    if not file1 and not file2 and not task:
        raise HTTPException(status_code=400, detail="At least one file or task text must be provided.")

    # Generate unique filenames for the uploaded files
    file1_path = os.path.join(UPLOAD_FOLDER, f"{uuid4()}_{file1.filename}") if file1 else None
    file2_path = os.path.join(UPLOAD_FOLDER, f"{uuid4()}_{file2.filename}") if file2 else None

    try:
        # Save the uploaded files to the server
        if file1:
            save_uploaded_file(await file1.read(), file1_path)
        if file2:
            save_uploaded_file(await file2.read(), file2_path)

        # Extract text from the PDFs using pdfplumber
        text1 = extract_text_from_pdf(file1_path) if file1 else ""
        text2 = extract_text_from_pdf(file2_path) if file2 else ""

        # Use ChatGPT to analyze the task and the provided PDFs
        analysis_result = compare_with_gpt(task, text1, text2)

        # Clean up the uploaded files after processing
        if file1:
            os.remove(file1_path)
        if file2:
            os.remove(file2_path)

        # Format the JSON response
        response_content = {
            "task": task,
            "file1_text": text1,
            "file2_text": text2,
            "analysis": analysis_result
        }

        return JSONResponse(content=response_content, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing files: {e}")
