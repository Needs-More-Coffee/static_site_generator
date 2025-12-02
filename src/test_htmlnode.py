import unittest

from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_formating(self):
        node = HTMLNode("This is a formatting test", props={"href": "https://example.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com" target="_blank"')

    def test_if_empty(self):
        node = HTMLNode("p")
        self.assertEqual(node.props_to_html(), "")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_parent_child_render(self):
        node = ParentNode("div", [LeafNode("b", "hello")])
        self.assertEqual(node.to_html(), "<div><b>hello</b></div>")

    def test_parent_w_props(self):
        node = ParentNode("div", [LeafNode("p", "hey")], props={"class": "container"})
        self.assertEqual(node.to_html(), '<div class="container"><p>hey</p></div>')

    def test_parent_config(self):
        node = ParentNode("div", [LeafNode("p", "hi")])
        node.value = "not allowed"
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode("p", "hi")]).to_html()
        with self.assertRaises(ValueError):
            ParentNode("div", None).to_html()
        with self.assertRaises(ValueError):
            node.to_html()