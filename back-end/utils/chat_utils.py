import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def compare_with_gpt(task: str, text1: str, text2: str, history : list) -> str:
    try:
        # Constructing the chat-based messages
        if task and not text1 and not text2:
            messages = [
                {'role': 'system', 'content': f"Here is our conversation history - {history}."},
                {"role": "system", "content": "You are a helpful assistant capable of answering general questions or providing explanations."},
                {"role": "user", "content": f"Task: {task}"},
                {"role": "assistant", "content": "Answer the user's task or question directly, without requiring additional context from documents."}
            ]
        else:
            messages = [
                {'role': 'system', 'content': f"Here is our conversation history - {history}."},
                {"role": "system", "content": "You are an expert in validating documents or facilitating conversations."},
                {"role": "user", "content": f"Task: {task}"},
                {"role": "user", "content": f"Template Document:\n{text1}"},
                {"role": "user", "content": f"User's Document:\n{text2}"},
                {"role": "assistant", "content": (
                    "Please validate the user's document against the template or continue the conversation based on the context provided. "
                    "If this is a validation task, focus on missing sections, formatting inconsistencies, and suggestions for improvement."
                )}
            ]

        # Sending request to the chat-based API
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # or "gpt-4"
            messages=messages,
        )

        # Extracting the analysis response from the model's reply
        return response['choices'][0]['message']['content']

    except Exception as e:
        return f"Error processing files: {str(e)}"
