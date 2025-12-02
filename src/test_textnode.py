import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_noeq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_invalid_type(self):
        with self.assertRaises(ValueError):
            TextNode("This is a text node", "Not a valid type")
        
    def test_url(self):
        node = TextNode("Test node", TextType.LINK, "https://example.com")
        self.assertEqual(node.url, "https://example.com")

if __name__ == "__main__":
    unittest.main()