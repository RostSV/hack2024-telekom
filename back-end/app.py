from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from uuid import uuid4
import os
from utils.file_utils import extract_text_from_pdf, extract_text_from_docx, extract_text_from_doc, save_uploaded_file
from utils.chat_utils import compare_with_gpt
from llm_agent import LLMChatAgent

# Create the FastAPI app
app = FastAPI()

# Configure the upload folder path
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize the LLM Agent
llm_agent = LLMChatAgent()


def cleanup_upload_folder():
    """
    Remove all files in the upload folder.
    """
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")


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
    Endpoint to compare two files (PDF, DOC, DOCX) or process a single file with a task.
    """
    if not session_id or not task:
        raise HTTPException(status_code=400, detail="Session ID and task must be provided.")

    file1_path = os.path.join(UPLOAD_FOLDER, f"{uuid4()}_{file1.filename}") if file1 else None
    file2_path = os.path.join(UPLOAD_FOLDER, f"{uuid4()}_{file2.filename}") if file2 else None

    try:
        # Save the uploaded files to the server
        if file1:
            save_uploaded_file(await file1.read(), file1_path)
        if file2:
            save_uploaded_file(await file2.read(), file2_path)

        # Extract text from the files
        text1 = ""
        text2 = ""
        if file1:
            if file1.filename.endswith(".pdf"):
                text1 = extract_text_from_pdf(file1_path)
            elif file1.filename.endswith(".docx"):
                text1 = extract_text_from_docx(file1_path)
            elif file1.filename.endswith(".doc"):
                text1 = extract_text_from_doc(file1_path)
        if file2:
            if file2.filename.endswith(".pdf"):
                text2 = extract_text_from_pdf(file2_path)
            elif file2.filename.endswith(".docx"):
                text2 = extract_text_from_docx(file2_path)
            elif file2.filename.endswith(".doc"):
                text2 = extract_text_from_doc(file2_path)

        # Use the LLM Agent to process the task and maintain history
        response = llm_agent.process_task(session_id, task, text1, text2)

        # Clean up the uploaded files after processing
        cleanup_upload_folder()

        # Format the JSON response without including the history
        response_content = {
#             "task": task,
#             "file1_text": text1,
#             "file2_text": text2,
            "analysis": analysis_result
        }

        return JSONResponse(content=response_content, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing files: {e}")
