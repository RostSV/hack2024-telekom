import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key here
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Directory to store uploaded files
UPLOAD_FOLDER = "uploads"
