import unittest

from textnode import *
from htmlnode import *
from split import *

class TestSplit(unittest.TestCase):
    def test_split_image(self):
        node = TextNode("This is a ![image](https://i.imgur.com/zjjcJKZ.png) in text", TextType.TEXT,)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([
            TextNode("This is a ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" in text", TextType.TEXT),
        ],
        new_nodes,
    )

    
    def test_split_image_multiple(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT,)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
        ],
        new_nodes,
    )

    def test_split_link(self):
        node = TextNode("This is a [link](https://example.com) in text", TextType.TEXT,)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([
            TextNode("This is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" in text", TextType.TEXT),
        ],
        new_nodes,
    )

    def test_split_link_multiple(self):
        node = TextNode("Here is [one](u1) and here is [two](u2)", TextType.TEXT,)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([
            TextNode("Here is ", TextType.TEXT),
            TextNode("one", TextType.LINK, "u1"),
            TextNode(" and here is ", TextType.TEXT),
            TextNode("two", TextType.LINK, "u2"),
        ],
        new_nodes,
    )
