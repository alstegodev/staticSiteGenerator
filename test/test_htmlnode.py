import unittest

from src.htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_standard(self):
        node = HTMLNode("tag", "bold", [], {"href": "link", "target": "_blank"})
        result = node.props_to_html()
        expected_result = ' href="link" target="_blank"'
        self.assertEqual(result, expected_result)

    def test_repr(self):
        node = HTMLNode("tag", "bold", ["einKind"], {"href": "link", "target": "_blank"})
        expected_result = "HTMLNode(tag,bold,['einKind'],{'href': 'link', 'target': '_blank'})"
        self.assertEqual(node.__repr__(), expected_result)


class TestLeafNode(unittest.TestCase):

    def test_to_html_p(self):
        node = LeafNode("p", "This is a paragraph of text.")
        expected_result = '<p>This is a paragraph of text.</p>'
        result = node.to_html()
        self.assertEqual(result, expected_result)

    def test_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        expected_result = '<a href="https://www.google.com">Click me!</a>'
        result = node.to_html()
        self.assertEqual(result, expected_result)


class TestParentNode(unittest.TestCase):

    def test_to_html_p(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        expected_result = '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'
        result = node.to_html()
        self.assertEqual(result, expected_result)



if __name__ == "__main__":
    unittest.main()
