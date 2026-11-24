import os
import shutil
from converter import markdown_to_html_node

def copy_files(source_directory: str, destination_directory: str):
    src_abs_path: str = os.path.normpath(os.path.abspath(source_directory))
    dest_abs_path: str = os.path.normpath(os.path.abspath(destination_directory))

    if not os.path.exists(src_abs_path):
        raise FileNotFoundError()
    if not os.path.exists(dest_abs_path):
        os.mkdir(dest_abs_path)
    shutil.rmtree(dest_abs_path)
    os.mkdir(dest_abs_path)
    dirs: list[str] = []
    for file in os.listdir(src_abs_path):
        src_file_path: str = os.path.join(src_abs_path, file)
        dest_file_path: str = os.path.join(dest_abs_path, file)
        if os.path.isfile(src_file_path):
            shutil.copy(src_file_path, dest_file_path)
            print(f"Copied file: {os.path.join(source_directory, file)} -> {os.path.join(destination_directory, file)}")
        if os.path.isdir(src_file_path):
            dirs.append(file)

    if len(dirs) > 0:
        for dir in dirs:
            os.mkdir(os.path.join(dest_abs_path, dir))
            copy_files(source_directory=os.path.join(source_directory, dir), destination_directory=os.path.join(destination_directory, dir))
    return

def extract_title(markdown: str) -> str:
    for line in markdown.split("\n"):
        if line.removeprefix(" ").startswith("# "):
            return line.removeprefix(" ").removeprefix("# ")
    raise Exception("The title does not exist")

def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as file:
        md_content: str = file.read()
    with open(template_path, "r") as file:
        template: str = file.read()
    html_string: str = markdown_to_html_node(md_content).to_html()
    title: str = extract_title(md_content)
    file_content = template.replace(r"{{ Title }}", title).replace(r"{{ Content }}", html_string)
    with open(dest_path, "w") as file:
        os.makedirs(os.path.normpath(os.path.abspath(dest_path)), exist_ok=True)
        file.write(file_content)