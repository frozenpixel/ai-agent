import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file_content",
    description="Write content to a file within the working directory. Creates the file if it doesn't exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write or overwrite, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to file.",
            ),
        },
        required=["file_path", "content"],
    ),
)

def write_file(working_directory, file_path, content):
    path = os.path.join(working_directory, file_path)
    absolute_path = os.path.abspath(path)

    if not absolute_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(absolute_path):
        try:
            os.makedirs(os.path.dirname(absolute_path), exist_ok=True)
        except Exception as e:
            return f'Error: creating directory: {e}'
    
    try:
        with open(path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: writing to file: {e}'