from textnode import *
from htmlnode import * 

def split_nodes_delimiter(old_nodes, delimiter, new_text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_text = node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise ValueError
        for index, segment in enumerate(split_text):
            if index % 2 == 0:
                if segment:
                    new_nodes.append(TextNode(segment, TextType.TEXT))
            else:
                if segment:
                    new_nodes.append(TextNode(segment, new_text_type))
    return new_nodes
