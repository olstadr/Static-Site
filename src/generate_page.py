# python
import os

from .markdown_to_html_node import markdown_to_html_node
from .extract_title import extract_title

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r", encoding="utf-8") as f:
        markdown = f.read()

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    html_content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    full_html = (
        template
        .replace("{{ Title }}", title)
        .replace("{{ Content }}", html_content)
    )

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(full_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path): # dir_path_content called as ./content in src/main.py
    for item in os.listdir(dir_path_content):
        src = os.path.join(dir_path_content, item)
        dst = os.path.join(dest_dir_path, item)

        if os.path.isfile(src) and src.endswith(".md"):
            (root, ext) = os.path.splitext(dst)
            dst_html = root + ".html"
            generate_page(src, template_path, dst_html)

        elif os.path.isdir(src):
            os.makedirs(dst, exist_ok=True)
            generate_pages_recursive(src, template_path, dst)