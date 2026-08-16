from app.tools.registry import ToolRegistry
from app.tools.system import get_system_info
from app.tools.applications import open_application
from app.tools.filesystem import (list_directory,search_files)
from app.tools.file_reader import read_file
from app.tools.document_reader import (read_pdf,read_docx)
from app.tools.file_writer import (create_directory,write_file)

def create_tool_registry():

    registry = ToolRegistry()

    registry.register(
        name="system_info",
        description=(
            "Get information about the Mac including operating system, "
            "architecture, processor, RAM and disk usage."
        ),
        function=get_system_info
    )

    registry.register(
        name="open_application",
        description=(
            "Open an installed macOS application by its application name."
        ),
        function=open_application
    )

    registry.register(
        name="list_directory",
        description=(
            "List files and folders inside an allowed macOS directory. "
            "Use this when the user wants to inspect the contents of "
            "Desktop, Documents, or Downloads."
        ),
    function=list_directory
    )

    registry.register(
    name="search_files",
    description=(
        "Search recursively for files inside an allowed directory. "
        "Supports patterns such as *.pdf, *.py and resume*."
    ),
    function=search_files
    )

    registry.register(
    name="read_file",
    description=(
        "Read the contents of an allowed text-based file. "
        "Supports TXT, Markdown, Python, JSON and CSV files."
    ),
    function=read_file
    )

    registry.register(
    name="read_pdf",
    description=(
        "Extract text from a PDF document located inside "
        "an allowed directory."
    ),
    function=read_pdf
    )

    registry.register(
    name="read_docx",
    description=(
        "Extract text from a Microsoft Word DOCX document "
        "located inside an allowed directory."
    ),
    function=read_docx
    )
    
    registry.register(
    name="create_directory",
    description=(
        "Create a new directory inside an allowed location."
    ),
    function=create_directory
    )

    registry.register(
        name="write_file",
        description=(
        "Create or overwrite a text file inside an allowed location."
    ),
    function=write_file
    )
    return registry