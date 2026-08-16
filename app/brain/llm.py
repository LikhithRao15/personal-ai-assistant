from openai import OpenAI
from app.brain.tool_executor import ToolExecutor

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

        self.tool_executor = ToolExecutor(self.tools)

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
        },
        {
            "type": "function",
            "name": "list_directory",
            "description": (
                "List files and folders inside an allowed directory. "
                "Allowed locations include Desktop, Documents and Downloads."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": (
                            "Directory path to inspect, such as "
                            "~/Downloads or ~/Documents."
                        )
                    }
                },
                "required": ["path"],
                "additionalProperties": False
            },
            "strict": True
        },
        {
            "type": "function",
            "name": "search_files",
            "description": (
                "Search recursively for files inside an allowed directory. "
                "Use patterns such as *.pdf, *.py, *.jpg, *.docx or resume*."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": (
                            "Allowed directory to search, such as "
                            "~/Downloads or ~/Documents."
                        )
                    },
                    "pattern": {
                        "type": "string",
                        "description": (
                            "Filename pattern such as *.pdf, *.py or resume*."
                        )
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of results to return."
                    }
                },
                "required": [
                    "directory",
                    "pattern",
                    "max_results"
                ],
                "additionalProperties": False
            },
            "strict": True
        },
        {
            "type": "function",
            "name": "read_file",
            "description": (
                "Read the contents of an allowed text-based file. "
                "Use this when the user asks to read, inspect, "
                "understand or summarize a file."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": (
                            "Path to the file, such as "
                            "~/Downloads/nexus_test.txt."
                        )
                    }
                },
                "required": [
                    "path"
                ],
                "additionalProperties": False
            },
            "strict": True
        },
        {
            "type": "function",
            "name": "read_pdf",
            "description": (
                "Extract text from a PDF document. "
                "Use this when the user asks to read, analyze, "
                "or summarize a PDF."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to the PDF document."
                    }
                },
                "required": [
                    "path"
                ],
                "additionalProperties": False
            },
            "strict": True
        },
        {
            "type": "function",
            "name": "read_docx",
            "description": (
                "Extract text from a Word DOCX document. "
                "Use this when the user asks to read, analyze, "
                "or summarize a DOCX file."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to the DOCX document."
                    }
                },
                "required": [
                    "path"
                ],
                "additionalProperties": False
            },
            "strict": True
        },
        {
            "type": "function",
            "name": "create_directory",
            "description": (
                "Create a new directory inside an allowed location. "
                "Use this when the user asks to create a folder."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": (
                            "Path for the new directory, such as "
                            "~/Documents/AI Projects."
                        )
                    }
                },
                "required": [
                    "path"
                ],
                "additionalProperties": False
            },
            "strict": True
        },
        {
            "type": "function",
            "name": "write_file",
            "description": (
                "Create or overwrite a text file inside an allowed location. "
                "Use this when the user explicitly asks to create or write "
                "content into a file."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Destination file path."
                    },
                    "content": {
                        "type": "string",
                        "description": "Complete content to write into the file."
                    }
                },
                "required": [
                    "path",
                    "content"
                ],
                "additionalProperties": False
            },
            "strict": True
        },
        {
            "type": "function",
            "name": "terminal_execute",
            "description": (
                "Execute a terminal command on the Mac. "
                "Use this when the user explicitly asks to run "
                "a command, program, test, development server, "
                "or inspect terminal output."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": (
                            "The terminal command to execute."
                        )
                    },
                    "working_directory": {
                        "type": "string",
                        "description": (
                            "Directory where the command should run. "
                            "Use ~ when no specific directory is required."
                        )
                    },
                    "timeout": {
                        "type": "integer",
                        "description": (
                            "Maximum execution time in seconds."
                        )
                    }
                },
                "required": [
                    "command",
                    "working_directory",
                    "timeout"
                ],
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

        while True:

            tool_outputs = []

            for tool_call in response.output:

                if tool_call.type != "function_call":
                    continue

                tool_output = self.tool_executor.execute(
                    tool_call
                )

                tool_outputs.append(
                    tool_output)

            if not tool_outputs:

                answer = response.output_text

                self.conversation.append({
                    "role": "assistant",
                    "content": answer
                })

                return answer

            response = self.client.responses.create(
            model=self.model,
            instructions=self.instructions,
            previous_response_id=response.id,
            input=tool_outputs,
            tools=self.get_tool_definitions()
        )