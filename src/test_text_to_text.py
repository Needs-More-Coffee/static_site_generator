import unittest

from textnode import *
from htmlnode import *
from text_to_text import *

class TestSplit(unittest.TestCase):
    def test_plain_text(self):
        new_nodes = text_to_textnodes("Hello World")
        self.assertListEqual([TextNode("Hello World", TextType.TEXT)], new_nodes)

    def test_link_and_image(self):
        new_nodes = text_to_textnodes("Test ![img](u1) and [link](u2) done")
        self.assertListEqual(
            [
                TextNode("Test ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "u1"),
                TextNode(" and ", TextType.TEXT),
                TextNode("link", TextType.LINK, "u2"),
                TextNode(" done", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_multiple_text_types(self):
        new_nodes = text_to_textnodes("This is **bold** text *italic* and `code` here")
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" and ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" here", TextType.TEXT),
            ],
            new_nodes,
        )



    def test_value_error(self):
        with self.assertRaises(ValueError):
            text_to_textnodes("This is **bold text")

    def test_everything(self):
        new_nodes = text_to_textnodes("Start **bold** text ![alt](img.jpg) and [lnk](url) *it* `code` end")
        self.assertListEqual(
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text ", TextType.TEXT),
                TextNode("alt", TextType.IMAGE, "img.jpg"),
                TextNode(" and ", TextType.TEXT),
                TextNode("lnk", TextType.LINK, "url"),
                TextNode(" ", TextType.TEXT),
                TextNode("it", TextType.ITALIC),
                TextNode(" ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" end", TextType.TEXT),
            ],
            new_nodes,
        )