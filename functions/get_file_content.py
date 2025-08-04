import os
from config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Read and returns the first {MAX_CHARS} characters of the content from the specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read the content from, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)

def get_file_content(working_directory, file_path):
    path = os.path.join(working_directory, file_path)
    absolute_file_path = os.path.abspath(path)
    absolute_working_dir = os.path.abspath(working_directory)

    if not absolute_file_path.startswith(absolute_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(path, "r") as f:
            file_content = f.read()
            check_content = file_content.strip().split()
            char_len = sum(len(word) for word in check_content)

            if char_len > MAX_CHARS:
                return file_content + f'[...File "{file_path}" truncated at 10000 characters]'
            
    except Exception as e:
        return f'Error: {e}'
    
    try:
        with open(path, "r") as f:
            file_content = f.read(MAX_CHARS)

            return file_content
    except Exception as e:
        return f'Error: {e}'