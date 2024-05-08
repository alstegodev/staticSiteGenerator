import unittest

from src.textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("This is a text node", "bold", "eineUrl")
        node2 = TextNode("This is a text node", "bold", "eineUrl")
        self.assertEqual(node, node2)

    def test_eq_fail(self):
        node = TextNode("This is a text node", "bold", "eineUrl")
        node2 = TextNode("WRONG TEXT", "bold", "eineUrl")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", "bold", "eineUrl")
        expected_result = "TextNode(This is a text node, bold, eineUrl)"
        self.assertEqual(node.__repr__(), expected_result)


if __name__ == "__main__":
    unittest.main()
