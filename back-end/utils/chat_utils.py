import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def compare_with_gpt(task: str, text1: str, text2: str, max_tokens: int = 50) -> str:
    try:
        # Constructing the chat-based messages
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Task: {task}"},
            {"role": "user", "content": f"Here is an example document: {text1}"},
            {"role": "user", "content": f"Here is the user's document: {text2}"},
            {"role": "assistant", "content": f"Please provide feedback based on the task and the provided documents."}
        ]

        # Sending request to the chat-based API
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # or "gpt-4"
            messages=messages,
            max_tokens=max_tokens
        )

        # Extracting the analysis response from the model's reply
        return response['choices'][0]['message']['content']

    except Exception as e:
        return f"Error processing files: {str(e)}"
