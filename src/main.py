import sys
from generate_page import copy_files, generate_pages_recursive

def main() -> None:
    basepath: str = sys.argv[1] if len(sys.argv) >= 2 else "/"
    copy_files(source_directory="static", destination_directory="docs")
    generate_pages_recursive(dir_path_content="content/", template_path="template.html", dest_dir_path="docs/", basepath=basepath)

main()
