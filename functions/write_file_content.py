import os

def write_file(working_directory, file_path, content):
    path = os.path.join(working_directory, file_path)
    absolute_path = os.path.abspath(path)

    if not absolute_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(absolute_path):
        try:
            os.mkdir(os.path.dirname(absolute_path, exist_ok=True))
        except Exception as e:
            return f'Error: creating directory: {e}'
    
    try:
        with open(path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: writing to file: {e}'