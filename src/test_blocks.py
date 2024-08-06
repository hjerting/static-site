import unittest

from blocks import (
    markdown_to_blocks,
    block_to_block_type
)

class LeafNodeTest(unittest.TestCase):
    def test_markdown_to_blocks(self):
        text = """

# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item

"""
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            """* This is the first list item in a list block
* This is a list item
* This is another list item"""
        ]
        actual = markdown_to_blocks(text)
        self.assertEqual(expected, actual)

    def test_block_to_block_type_heading_1(self):
        text = "# Heading 1"
        actual = block_to_block_type(text)
        expected = "heading"
        self.assertEqual(expected, actual)

    def test_block_to_block_type_heading_2(self):
        text = "###### Heading 6"
        actual = block_to_block_type(text)
        expected = "heading"
        self.assertEqual(expected, actual)

    def test_block_to_block_type_heading_3(self):
        text = "####### Paragraph"
        actual = block_to_block_type(text)
        expected = "paragraph"
        self.assertEqual(expected, actual)

    def test_block_to_block_type_code_1(self):
        text = "``` some code ```"
        actual = block_to_block_type(text)
        expected = "code"
        self.assertEqual(expected, actual)

    def test_block_to_block_type_code_2(self):
        text = """``` some code
spread on many lines
one more line
and one more ```"""
        actual = block_to_block_type(text)
        expected = "code"
        self.assertEqual(expected, actual)

    def test_block_to_block_type_quote_1(self):
        text = "> some text"
        actual = block_to_block_type(text)
        expected = "quote"
        self.assertEqual(expected, actual)

    def test_block_to_block_type_quote_2(self):
        text = """> some text
> more text
>
> final"""
        actual = block_to_block_type(text)
        expected = "quote"
        self.assertEqual(expected, actual)

    def test_block_to_block_type_quote_3(self):
        text = """> some text
> more text
>
> final
>"""
        actual = block_to_block_type(text)
        expected = "quote"
        self.assertEqual(expected, actual)

    def test_block_to_block_unordered_list_1(self):
        text = "+ unordered list"
        actual = block_to_block_type(text)
        expected = "unordered list"
        self.assertEqual(expected, actual)

    def test_block_to_block_unordered_list_2(self):
        text = "- unordered list"
        actual = block_to_block_type(text)
        expected = "unordered list"
        self.assertEqual(expected, actual)

    def test_block_to_block_unordered_list_3(self):
        text = "+ " +\
            "\n- unordered list" +\
            "\n+ some more list" +\
            "\n- some more " +\
            "\n+ " +\
            "\n- " +\
            "\n+ last line"
        actual = block_to_block_type(text)
        expected = "unordered list"
        self.assertEqual(expected, actual)

    def test_block_to_block_ordered_list_1(self):
        text = "1. Item 1" +\
            "\n2. " +\
            "\n3. Item 3" +\
            "\n4. Item 4"
        actual = block_to_block_type(text)
        expected = "ordered list"
        self.assertEqual(expected, actual)

if __name__ == "__main__":
    unittest.main()