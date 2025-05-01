from textnode import TextNode, TextType
import shutil
import os
from converter import *

def main():
   # node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
   # print(node)
    destination_path = "public"
    source_path = "static"
    if os.path.exists(destination_path):
        shutil.rmtree(destination_path) 

    os.mkdir(destination_path)

    copy_static_files(source_path, destination_path)
    page_source = "content"
    template_source = "template.html"
    dest_path = "public"
    generate_pages_recursive(page_source, template_source, dest_path)

def copy_static_files(current_path, destination_path):
    contents = os.listdir(current_path)
    for thing in contents:
        full_source_path = os.path.join(current_path, thing)
        full_dest_path = os.path.join(destination_path, thing)
        if os.path.isfile(full_source_path):
            print(f"Copying file: {full_source_path} to {full_dest_path}")
            shutil.copy(full_source_path, full_dest_path)
        if os.path.isdir(full_source_path):
            os.mkdir(full_dest_path)
            print(f"Creating directory: {full_dest_path}")
            copy_static_files(full_source_path, full_dest_path)

def extract_title(markdown):

    lines = markdown.split("\n")

    for line in lines:
        if line.startswith('# '):
            return line[2:].strip()
    raise Exception("No h1 header found in the markdown")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, 'r') as f:
        markdown_content = f.read()

    with open(template_path, 'r') as f:
        template_content = f.read()

    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    title = extract_title(markdown_content)

    final_html = template_content.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_content)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, 'w') as f:
        f.write(final_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    contents = os.listdir(dir_path_content)
    for thing in contents:
        base, ext = os.path.splitext(thing)
        full_content_path = os.path.join(dir_path_content, thing)
        full_dest_dir_path = os.path.join(dest_dir_path, thing)
        if os.path.isfile(full_content_path) and thing.endswith(".md"):
            html_filename = base + ".html"
            full_dest_html_path = os.path.join(dest_dir_path, html_filename)
            generate_page(full_content_path, template_path, full_dest_html_path)
        if os.path.isdir(full_content_path):
            if not os.path.exists(full_dest_dir_path):
                os.mkdir(full_dest_dir_path)
            generate_pages_recursive(full_content_path, template_path, full_dest_dir_path)

if __name__ == "__main__":
    main()