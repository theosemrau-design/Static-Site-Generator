from generate_page import copy_files, generate_pages_recursive

def main() -> None:
    copy_files(source_directory="static", destination_directory="public")
    generate_pages_recursive(dir_path_content="/mnt/c/Users/theos/Desktop/Coding/boot.dev/static-site-generator/content/", template_path="/mnt/c/Users/theos/Desktop/Coding/boot.dev/static-site-generator/template.html", dest_dir_path="/mnt/c/Users/theos/Desktop/Coding/boot.dev/static-site-generator/public/")

main()
