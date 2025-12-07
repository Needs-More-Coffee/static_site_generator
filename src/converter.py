from textnode import *
from htmlnode import *
from text_to_text import *
from block_to_block import *

def text_node_to_html(node):
    if node.text_type == TextType.TEXT:
        return LeafNode(None, node.text)
    elif node.text_type == TextType.BOLD:
        return LeafNode("b", node.text)
    elif node.text_type == TextType.ITALIC:
        return LeafNode("i", node.text)
    elif node.text_type == TextType.CODE:
        return LeafNode("code", node.text)
    elif node.text_type == TextType.LINK:
        return LeafNode("a", node.text, props={"href": node.url})
    elif node.text_type == TextType.IMAGE:
        return LeafNode("img", "", props={"src": node.url, "alt": node.text})
    else:
        raise ValueError ("Unknown TextType")

def text_to_children(nodes):
    text_nodes = text_to_textnodes(nodes)
    html_children = []
    for node in text_nodes:
        html_children.append(text_node_to_html(node))
    return html_children

def number_of_leading_hashes(node):
    count = 0
    for char in node:
        if char == "#":
            count += 1
        else:
            break
    return count

def extract_inside_backticks(node):
    interior = node.split("\n", 1)[1]
    last_newline_index = interior.rfind("\n")
    return interior[: last_newline_index + 1]

def quote_block_to_html(node):
    lines = node.split("\n")
    clean_lines = [line[1:].lstrip() for line in lines]
    text = "\n".join(clean_lines)
    return text

def ordered_list_to_html(node):
    lines = node.split("\n")
    items = []
    for line in lines:
        idx = line.find(". ")
        item_text = line[idx + 2:].lstrip()
        items.append(item_text)

    li_nodes = []
    for text in items:
        children = text_to_children(text)
        li_nodes.append(ParentNode("li", children))

    return ParentNode("ol", li_nodes)


def unordered_list_to_html(node):
    lines = node.split("\n")
    items = [line[2:].lstrip() for line in lines]
    li_nodes = []
    for text in items:
        children = text_to_children(text)
        li_nodes.append(ParentNode("li", children))
    return ParentNode("ul", li_nodes)

def block_to_html_node(node, node_type):
    if node_type == BlockType.PARAGRAPH:
        text = node.replace("\n", " ")
        children = text_to_children(text)
        return ParentNode("p", children)
    elif node_type == BlockType.HEADING:
        count = number_of_leading_hashes(node)
        text = node[count + 1:].strip()
        children = text_to_children(text)
        return ParentNode(f"h{count}", children)
    elif node_type == BlockType.CODE:
        interior_text = extract_inside_backticks(node)
        code_node = ParentNode("code", [LeafNode(None, interior_text)])
        return ParentNode("pre", [code_node])
    elif node_type == BlockType.QUOTE:
        text = quote_block_to_html(node)
        children = text_to_children(text)
        return ParentNode("blockquote", children)
    elif node_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html(node)
    elif node_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html(node)
