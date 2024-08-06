import unittest

from leafnode import LeafNode

class LeafNodeTest(unittest.TestCase):
    def test_LeafToHTML(self):
        leaf = LeafNode("p", "This is a paragraph of text.")
        expected = "<p>This is a paragraph of text.</p>"
        actual = leaf.to_html()
        self.assertEqual(expected, actual)

    def test_LeafToHTML_2(self):
        leaf = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        expected = '<a href="https://www.google.com">Click me!</a>'
        actual = leaf.to_html()
        self.assertEqual(expected, actual)

if __name__ == "__main__":
    unittest.main()