import unittest

from htmlnode import *
from textnode import *
from delimiter import *
from converter import *
from split import *
from regexparser import *
from text_to_text import *


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

class TestDelimiter(unittest.TestCase):
    def test_single_bold(self):
        old_nodes = [TextNode("This is **bold** text", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)

        self.assertEqual(len(new_nodes), 3)

        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)

        self.assertEqual(new_nodes[2].text, " text")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_double_bold(self):
        old_nodes = [TextNode("This is **bold** text and this is **bold** text", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)

        self.assertEqual(len(new_nodes), 5)

        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)

        self.assertEqual(new_nodes[2].text, " text and this is ")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

        self.assertEqual(new_nodes[3].text, "bold")
        self.assertEqual(new_nodes[3].text_type, TextType.BOLD)

        self.assertEqual(new_nodes[4].text, " text")
        self.assertEqual(new_nodes[4].text_type, TextType.TEXT)

    def test_no_delimiter(self):
        old_nodes = [TextNode("This is the text", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)

        self.assertEqual(len(new_nodes), 1)

        self.assertEqual(new_nodes[0].text, "This is the text")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

    def test_odd_delimiter(self):
        old_nodes = [TextNode("This is **bold text", TextType.TEXT)]
        with self.assertRaises(ValueError):
            split_nodes_delimiter(old_nodes, "**", TextType.BOLD)

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

class TestTextToText(unittest.TestCase):
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