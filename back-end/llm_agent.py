from utils.chat_utils import compare_with_gpt


class LLMChatAgent:
    def __init__(self):
        """
        Initialize the LLM Agent with an empty conversation history.
        """
        self.sessions = {}

    def get_history(self, session_id: str):
        """
        Retrieve or initialize conversation history for a session.
        """
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        return self.sessions[session_id]

    def reset_history(self, session_id: str):
        """
        Clear the conversation history for a given session.
        """
        if session_id in self.sessions:
            self.sessions[session_id] = []

    def process_task(self, session_id: str, task: str, file1_text: str = "", file2_text: str = ""):
        """
        Process a task using GPT with session-based conversation history.
        Args:
            session_id (str): Unique ID for the user's session.
            task (str): The task or query to perform.
            file1_text (str): Text from the first uploaded file.
            file2_text (str): Text from the second uploaded file.
        Returns:
            str: GPT analysis or response.
        """
        # Retrieve conversation history for the session
        history = self.get_history(session_id)

        # Prepare messages for GPT
        messages = [{"role": "system", "content": "You are a helpful assistant."}]
        messages += history  # Add session history to the conversation

        # Add current task and file content
        messages.append({"role": "user", "content": f"Task: {task}"})
        if file1_text:
            messages.append({"role": "user", "content": f"Example document: {file1_text}"})
        if file2_text:
            messages.append({"role": "user", "content": f"User's document: {file2_text}"})

        # Call the compare_with_gpt function (original functionality preserved)
        response = compare_with_gpt(task, file1_text, file2_text, history)

        # Update session history
        history.append({"role": "user", "content": f"Task: {task}"})
        if file1_text:
            history.append({"role": "user", "content": f"Example document: {file1_text}"})
        if file2_text:
            history.append({"role": "user", "content": f"User's document: {file2_text}"})
        history.append({"role": "assistant", "content": response})

        return response
