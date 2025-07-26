import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    path = os.path.join(working_directory, file_path)
    absolute_path = os.path.abspath(path)

    if not absolute_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if os.path.isfile(path) == False:
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