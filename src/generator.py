import os.path

from markdown_blocks import markdown_to_html_node, extract_title


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    from_markdown_text = ""
    template_text = ""

    with open(from_path) as from_file:
        from_markdown_text = from_file.read()

    with open(template_path) as template_file:
        template_text = template_file.read()

    html_content = markdown_to_html_node(from_markdown_text).to_html()

    title = extract_title(from_markdown_text)

    template_text = template_text.replace("{{ Title }}", title)
    template_text = template_text.replace("{{ Content }}", html_content)

    directory = os.path.dirname(dest_path)
    os.makedirs(directory, exist_ok=True)

    with open(dest_path, "w") as dest:
        dest.write(template_text)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if os.path.isfile(dir_path_content):
        if dir_path_content.endswith(".md"):
            dest_dir_path = dest_dir_path.replace(".md", ".html")
            generate_page(dir_path_content, template_path, dest_dir_path)
    else:
        list_dir = os.listdir(dir_path_content)
        for directory in list_dir:
            new_dir_path = dir_path_content + "/" + directory
            new_dest_path = dest_dir_path + "/" + directory
            generate_pages_recursive(new_dir_path, template_path, new_dest_path)
