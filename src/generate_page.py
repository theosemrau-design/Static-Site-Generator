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
    for entry in os.listdir(src_abs_path):
        src_file_path: str = os.path.join(src_abs_path, entry)
        dest_file_path: str = os.path.join(dest_abs_path, entry)
        if os.path.isfile(src_file_path):
            shutil.copy(src_file_path, dest_file_path)
            print(f"Copied file: {os.path.join(source_directory, entry)} -> {os.path.join(destination_directory, entry)}")
        if os.path.isdir(src_file_path):
            dirs.append(entry)

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
    html_string: str = markdown_to_html_node(markdown=md_content).to_html()
    title: str = extract_title(md_content)
    file_content = template.replace(r"{{ Title }}", title).replace(r"{{ Content }}", html_string)
    with open(dest_path, "w") as file:
        os.makedirs(os.path.normpath(os.path.abspath(os.path.dirname(dest_path))), exist_ok=True)
        file.write(file_content)

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str) -> None:
    dirs: list[str] = []
    for entry in os.listdir(dir_path_content):
        src_file_path: str = os.path.join(dir_path_content, entry)
        dest_file_path: str = os.path.join(dest_dir_path, f"{entry.rsplit(".", 1)[0]}.html")
        if os.path.isfile(src_file_path):
            generate_page(from_path=src_file_path, template_path=template_path, dest_path=dest_file_path)
        if os.path.isdir(src_file_path):
            dirs.append(entry)

    if len(dirs) > 0:
        for dir in dirs:
            os.mkdir(os.path.join(dest_dir_path, dir))
            generate_pages_recursive(dir_path_content=os.path.join(dir_path_content, dir), template_path=template_path, dest_dir_path=os.path.join(dest_dir_path, dir))