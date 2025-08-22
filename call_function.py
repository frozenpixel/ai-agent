from google.genai import types

from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python import schema_run_python, run_python_file
from functions.write_file_content import schema_write_file, write_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python,
        schema_write_file,
    ]
)

def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    function_args = {"working_directory": "calculator", **function_call_part.args}

    if verbose:
        print(f'- Calling function: {function_name}({function_args})')
    else:
        print(f'- Calling function: {function_name}')

    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={f'error: Unknown function: {function_name}'},
                )
            ],
        )
    
    function_result = function_map[function_name](**function_args)
    return types.Content(
        role="user",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={'result': function_result},
            )
        ],
    )