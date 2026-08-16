from openai import OpenAI
from app.config.settings import OPENAI_API_KEY, MODEL_NAME


class AIBrain:

    def __init__(self):
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is missing.")

        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = MODEL_NAME

    def ask(self, message: str) -> str:

        response = self.client.responses.create(
            model=self.model,
            instructions="""
You are NEXUS, a powerful personal AI assistant running on macOS.

Your responsibilities:
- Understand the user's requests accurately.
- Be concise but useful.
- Never pretend an action was performed when it was not.
- When tools become available, use the appropriate tool.
- Ask for clarification only when genuinely necessary.
- Prioritize accuracy and safety.
""",
            input=message
        )

        return response.output_text