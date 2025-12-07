from textnode import *
from htmlnode import * 

def split_nodes_image(nodes):
    new_nodes = []
    for node in nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        while True:
            start = text.find("![")
            if start == -1:
                if text:
                    new_nodes.append(TextNode(text, TextType.TEXT))
                break
            before = text[:start]
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))    
            alt_start = start + 2
            alt_end = text.find("]", alt_start)
            alt = text[alt_start:alt_end]
            url_start = alt_end + 2 
            url_end = text.find(")", url_start)
            url = text[url_start:url_end]
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            text = text[url_end + 1:]
    return new_nodes

def split_nodes_link(nodes):
    new_nodes = []
    for node in nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        while True:
            start = text.find("[")
            if start > 0 and text[start - 1] == "!":
                start = text.find("[", start + 1)
                continue
            if start == -1:
                if text:
                    new_nodes.append(TextNode(text, TextType.TEXT))
                break
            before = text[:start]
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT)) 
            alt_start = start + 1
            alt_end = text.find("]", alt_start)
            alt = text[alt_start:alt_end]
            url_start = alt_end + 2
            url_end = text.find(")", url_start)
            url = text[url_start:url_end]
            new_nodes.append(TextNode(alt, TextType.LINK, url))
            text = text[url_end + 1:]
    return new_nodes