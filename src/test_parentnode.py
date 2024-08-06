import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class ParentNodeTest(unittest.TestCase):

    def test_ParentToHTML_1(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ]
        )
        actual = node.to_html()
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(actual, expected)

    def test_ParentToHTML_2(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Some bold text"),
                        LeafNode(None, "Some normal text"),
                        LeafNode("i", "Some italic text"),
                        LeafNode(None, "Some more normal text"),
                    ]
                ),
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold text in another paragraph"),
                        LeafNode(None, "Normal text in another paragraph"),
                        LeafNode("i", "Italic text in another paragraph"),
                        LeafNode(None, "Some more normal text in another paragraph"),
                    ]
                )
            ]
        )
        actual = node.to_html()
        expected = "<div><p><b>Some bold text</b>Some normal text<i>Some italic text</i>Some more normal text</p><p><b>Bold text in another paragraph</b>Normal text in another paragraph<i>Italic text in another paragraph</i>Some more normal text in another paragraph</p></div>"
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()