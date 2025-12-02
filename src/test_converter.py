import unittest

from converter import *

class TestConverter(unittest.TestCase):
    def test_vonert_img(self):
        node = TextNode("an image", TextType.IMAGE, url="https://example.com/img.png")
        html = text_node_to_html(node)
        self.assertEqual(html.to_html(), '<img src="https://example.com/img.png" alt="an image">')

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
