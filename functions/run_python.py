import os
import subprocess
from google.genai import types

schema_run_python = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output from the interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to execute from, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file."
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    path = os.path.join(working_directory, file_path)
    absolute_file_path = os.path.abspath(path)
    absolute_working_dir = os.path.abspath(working_directory)

    if not absolute_file_path.startswith(absolute_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(path):
        return f'Error: File "{file_path}" not found.'
    
    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        process_args = ["python3", absolute_file_path]
        process_args.extend(args)
        result = subprocess.run(
            args=process_args, 
            capture_output=True,
            text=True, 
            cwd=absolute_working_dir, 
            timeout=30)

        output = []
        if result.stdout:
            output.append(f'STDOUT:\n{result.stdout}')
        if result.stderr:
            output.append(f'STDERR:\n{result.stderr}')
        if output == None:
            return f'No output produced'
        
        if result.returncode != 0:
            return f'Process exited with code {result.returncode}'
        
        return "\n".join(output)
    
    except Exception as e:
        return f'Error: executing Python file: {e}'