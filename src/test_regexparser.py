import unittest

from regexparser import *

class TestRegexparser(unittest.TestCase):
    def test_extract_single_link(self):
        text = "This is a [link](https://example.com)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("link", "https://example.com")])

    def test_extract_multiple_links(self):
        text = "Here is a [first](https://a.com) and another [second](https://b.com)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("first", "https://a.com"), ("second", "https://b.com")])

    def test_no_link_to_extract(self):
        text = "There is no link here"
        result = extract_markdown_links(text)
        self.assertEqual(result, [])

    def test_extract_single_image(self):
        text = "This is a ![image](https://example.com/cat.png)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("image", "https://example.com/cat.png")])

    def test_extract_multiple_images(self):
        text = "Here is a ![first](https://example.com/cat.png) and a ![second](https://example.com/dog.png)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("first", "https://example.com/cat.png"), ("second", "https://example.com/dog.png")])

    def test_no_image_to_extract(self):
        text = "There is no image here"
        result = extract_markdown_images(text)
        self.assertEqual(result, [])