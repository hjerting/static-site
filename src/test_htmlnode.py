import unittest

from htmlnode import HTMLNode

class HTMLNodeTest(unittest.TestCase):
    def test_PropsToHTML(self):
        HTMLn = HTMLNode(
            tag = "a",
            value = "This is a link",
            children = None,
            props = {"href": "https://www.google.com", "target": "_blank"}
        )
        expected = ' href="https://www.google.com" target="_blank"'
        actual = HTMLn.props_to_html()
        self.assertEqual(expected, actual)

if __name__ == "__main__":
    unittest.main()