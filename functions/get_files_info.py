import os

def get_files_info(working_directory, directory="."):
    content_list = []
    path = os.path.join(working_directory, directory)
    absolute_file_path = os.path.abspath(path)
    absolute_working_dir = os.path.abspath(working_directory)
    directory_contents = os.listdir(path=path)

    if directory == ".":
        print("Result for current directory:")
    else:
        print(f"Result for '{directory}' directory:")

    if not absolute_file_path.startswith(absolute_working_dir):
        return f'   Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(path):
        return f'   Error: "{directory}" is not a directory'
    
    try:
        for content in directory_contents:
            content_path = os.path.join(path, content)
            content_list.append(f"- {content}: file_size={os.path.getsize(content_path)}, is_dir={os.path.isdir(content_path)}")

        return '\n'.join(content_list)
    except Exception as e:
        return f"Error listing files: {e}"