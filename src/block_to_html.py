from block_to_block import *
from markdown_block import *
from converter import *

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_children = []

    for block in blocks:
        block_type = block_to_block_type(block)
        block_node = block_to_html_node(block, block_type)
        html_children.append(block_node)

    root = ParentNode("div", html_children)
    return root
