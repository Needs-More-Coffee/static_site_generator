from textnode import *
from htmlnode import * 

def markdown_to_blocks(markdown):
    nodes = []
    markdown = markdown.strip()
    blocks = markdown.split("\n\n")
    for block in blocks:
        temp = block.strip()
        if temp == "":
            continue

        lines = temp.split("\n")
        clean_lines = [line.strip() for line in lines]
        clean_block = "\n".join(clean_lines)
        nodes.append(clean_block)
    return nodes
