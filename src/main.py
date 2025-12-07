import os
import shutil
import sys

from htmlnode import *
from textnode import *
from delimiter import *
from converter import *
from split import *
from regexparser import *
from text_to_text import *
from markdown_block import *
from block_to_block import *
from block_to_html import *

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    copy_static("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)

def copy_static(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)
    copy_dir(src, dst)

def copy_dir(src_dir, dst_dir):
    for name in os.listdir(src_dir):
        src_path = os.path.join(src_dir, name)
        dst_path = os.path.join(dst_dir, name)
        if os.path.isfile(src_path):
            print(f"Copying file: {src_path} -> {dst_path}")
            shutil.copy(src_path, dst_path)
        else:
            print(f"Creating directory: {dst_path}")
            os.mkdir(dst_path)
            copy_dir(src_path, dst_path)

def extract_title(markdown):
    blocks = markdown.split("\n")
    for block in blocks:
        temp1 = block.strip()
        if temp1.startswith("# "):
            return temp1[2:].strip()
    raise ValueError ("No H1 title found")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path, "r") as f:
        template = f.read()

    root = markdown_to_html_node(markdown)
    content_html = root.to_html()
    title = extract_title(markdown)
    page_html = template.replace("{{ Title }}", title).replace("{{ Content }}", content_html)
    page_html = page_html.replace('href="/', f'href="{basepath}')
    page_html = page_html.replace('src="/', f'src="{basepath}')

    
    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(page_html)

def generate_pages_recursive(from_dir, template_path, dest_dir, basepath):
    for filename in os.listdir(from_dir):
        src_path = os.path.join(from_dir, filename)
        dst_path = os.path.join(dest_dir, filename)

        if os.path.isfile(src_path) and filename.endswith(".md"):
            html_filename = filename.replace(".md", ".html")
            dst_path = os.path.join(dest_dir, html_filename)
            generate_page(src_path, template_path, dst_path, basepath)
        elif os.path.isdir(src_path):
            if not os.path.exists(dst_path):
                os.makedirs(dst_path, exist_ok=True)
            generate_pages_recursive(src_path, template_path, dst_path, basepath)


if __name__ == "__main__":
    main()