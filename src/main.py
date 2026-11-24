from generate_page import copy_files, generate_page

def main() -> None:
    copy_files(source_directory="static", destination_directory="public")
    generate_page(from_path="content/index.md", template_path="template.html", dest_path="public/index.html")

main()
