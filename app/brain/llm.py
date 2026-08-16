from openai import OpenAI

from app.config.settings import (
    OPENAI_API_KEY,
    MODEL_NAME
)

from app.tools.manager import create_tool_registry


class AIBrain:

    def __init__(self):

        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is missing.")

        self.client = OpenAI(api_key=OPENAI_API_KEY)

        self.model = MODEL_NAME

        self.tools = create_tool_registry()

        self.conversation = []

        self.instructions = """
You are NEXUS, a powerful personal AI assistant running on macOS.

Rules:

1. Understand the user's request accurately.
2. Use tools whenever real information from the Mac is required.
3. Never invent system information.
4. Never claim that an action happened unless a tool actually performed it.
5. Explain tool results clearly.
6. If a tool is unavailable, say so honestly.
"""

    def get_tool_definitions(self):

        return [
            {
                "type": "function",
                "name": "system_info",
                "description": (
                    "Get real-time information about the Mac, "
                    "including operating system, architecture, "
                    "processor, RAM and disk usage."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "additionalProperties": False
                },
                "strict": True
            },
            {
            "type": "function",
            "name": "open_application",
            "description": (
                "Open an installed application on macOS. "
                "Use this when the user explicitly asks to open "
                "or launch an application."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "application_name": {
                        "type": "string",
                        "description": "The exact name of the macOS application."
                    }
                },
                "required": ["application_name"],
                "additionalProperties": False
            },
            "strict": True
        }
        ]

    def ask(self, message: str):

        self.conversation.append({
            "role": "user",
            "content": message
        })

        response = self.client.responses.create(
            model=self.model,
            instructions=self.instructions,
            input=self.conversation,
            tools=self.get_tool_definitions()
        )

        return self.process_response(response)

    def process_response(self, response):

        tool_calls = [
            item
            for item in response.output
            if item.type == "function_call"
        ]

        if not tool_calls:

            answer = response.output_text

            self.conversation.append({
                "role": "assistant",
                "content": answer
            })

            return answer

        for tool_call in tool_calls:

            tool_name = tool_call.name

            if tool_name == "system_info":

                result = self.tools.execute(
                    "system_info",
                    {}
                )

                tool_result = {
                    "type": "function_call_output",
                    "call_id": tool_call.call_id,
                    "output": str(result)
                }

                response = self.client.responses.create(
                    model=self.model,
                    instructions=self.instructions,
                    previous_response_id=response.id,
                    input=[tool_result],
                    tools=self.get_tool_definitions()
             
                )
            elif tool_name == "open_application":

                import json

                arguments = json.loads(tool_call.arguments)

                result = self.tools.execute(
                    "open_application",
                    arguments
                )

                tool_result = {
                    "type": "function_call_output",
                    "call_id": tool_call.call_id,
                    "output": str(result)
                }

                response = self.client.responses.create(
                    model=self.model,
                    instructions=self.instructions,
                    previous_response_id=response.id,
                    input=[tool_result],
                    tools=self.get_tool_definitions()
    )

        answer = response.output_text

        self.conversation.append({
            "role": "assistant",
            "content": answer
        })

        return answer