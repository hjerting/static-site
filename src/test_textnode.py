import unittest

from textnode import    (TextNode,
                        markdownParser,
                        extract_markdown_images,
                        extract_markdown_links,
                        split_nodes_image,
                        split_nodes_link,
                        split_nodes_delimiter,
                        text_to_textnodes,
                        text_type_text,
                        text_type_bold,
                        text_type_italic,
                        text_type_code,
                        text_type_link,
                        text_type_image)
from leafnode import LeafNode
from htmlnode import HTMLNode



class TestTextNode(unittest.TestCase):
    def test_text_type_text(self):
        # This should become a LeafNode with no tag, just a raw text value.
        node = TextNode("This is just some text", "text")
        html = TextNode.text_node_to_html_node(node)
        self.assertEqual(html.value, "This is just some text")
        self.assertEqual(html.tag, None)
        self.assertEqual(html.children, None)
        self.assertEqual(html.props, None)

    def test_text_type_bold(self):
        # text_type_bold: This should become a LeafNode with a "b" tag and the "This is just some text".
        node = TextNode("This is just some text", "bold")
        html = TextNode.text_node_to_html_node(node)
        self.assertEqual(html.value, "This is just some text")
        self.assertEqual(html.tag, "b")
        self.assertEqual(html.children, None)
        self.assertEqual(html.props, None)

    def test_text_type_italic(self):
        # text_type_italic: "i" tag, text = "This is just some text"
        node = TextNode("This is just some text", "italic")
        html = TextNode.text_node_to_html_node(node)
        self.assertEqual(html.value, "This is just some text")
        self.assertEqual(html.tag, "i")
        self.assertEqual(html.children, None)
        self.assertEqual(html.props, None)

    def test_text_type_code(self):
        # text_type_code: "code" tag, text = "This is just some text"
        node = TextNode("This is just some text", "code")
        html = TextNode.text_node_to_html_node(node)
        self.assertEqual(html.value, "This is just some text")
        self.assertEqual(html.tag, "code")
        self.assertEqual(html.children, None)
        self.assertEqual(html.props, None)

    def test_text_type_link(self):
        # text_type_link: "a" tag, anchor text, and "href" prop
        node = TextNode("This is just some text", "link", url="https://www.google.com")
        html = TextNode.text_node_to_html_node(node)
        self.assertEqual(html.value, "This is just some text")
        self.assertEqual(html.tag, "a")
        self.assertEqual(html.children, None)
        self.assertEqual(html.props, {'href': 'https://www.google.com'})

    def test_text_type_image(self):
        # text_type_image: "img" tag, empty string value, "src" and "alt" props ("src" is the image URL, "alt" is the alt text)
        node = TextNode("This is just some text", "image")
        html = TextNode.text_node_to_html_node(node)
        self.assertEqual(html.value, "")
        self.assertEqual(html.tag, "img")
        self.assertEqual(html.children, None)
        self.assertEqual(html.props, {'src': '', 'alt': ''})

    def test_split_nodes_delimiter(self):
        text_type_text = "text"
        text_type_code = "code"
        node = TextNode("This is text with a `code block` word", text_type_text)
        actual = split_nodes_delimiter([node], "`", text_type_code)
        expected = TextNode(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" word", text_type_text),
            ], text_type_text
        )
        self.assertEqual(str(actual), str(expected))

    def test_extract_markdown_images(self):
        # [
        #   ("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
        #   ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")
        # ]
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        actual = extract_markdown_images(text)
        expected = [
            ("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")
        ]
        self.assertEqual(actual, expected)

    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_eq_2(self):
        node = TextNode("Some other text", "italic", "https://www.hjerting.com")
        node2 = TextNode("Some other text", "italic", "https://www.hjerting.com")
        self.assertEqual(node, node2)

    def test_not_eq_(self):
        node = TextNode("Some other text", "bold", "https://www.hjerting.com")
        node2 = TextNode("Some other text", "italic", "https://www.hjerting.com")
        self.assertNotEqual(node, node2)

    def test_markdownParser_1(self):
        input_text = "This is text with a **bolded** word"
        result = markdownParser(input_text)
        expected = [
            TextNode("This is text with a ", "text"),
            TextNode("bolded", "bold"),
            TextNode(" word", "text"),
        ]
        self.assertEqual(result, expected)

    def test_markdownParser_2(self):
        input_text = "This is an *italic and **bold** word*."
        result = markdownParser(input_text)
        expected = [
            TextNode("This is an ", "text"),
            TextNode(
                [
                    TextNode("italic and ", "text"),
                    TextNode("bold", "bold"),
                    TextNode(" word", "text")
                ], "italic"),
            TextNode(".", "text")
        ]
        self.assertEqual(result, expected)

    def test_extract_markdown_images_1(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        actual = extract_markdown_images(text)
        self.assertEqual(actual, expected)

    def test_extract_markdown_images_2(self):
        input_text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        actual = extract_markdown_images(input_text)
        expected = [
            ("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")
        ]
        self.assertEqual(actual, expected)

    def test_extract_markdown_links_1(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        actual = extract_markdown_links(text)
        self.assertEqual(actual, expected)

    def test_extract_markdown_links_2(self):
        input_text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        actual = extract_markdown_links(input_text)
        expected = [
            ("link", "https://www.example.com"),
            ("another", "https://www.example.com/another")
        ]
        self.assertEqual(actual, expected)

    def test_split_nodes_image(self):
        text_type_text = "text"
        text_type_image = "image"
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            text_type_text,
        )
        actual = split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", text_type_text),
            TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and another ", text_type_text),
            TextNode(
                "second image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
            ),
        ]
        self.assertEqual(actual, expected)

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            text_type_text,
        )
        actual = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", text_type_text),
            TextNode("to boot dev", text_type_link, "https://www.boot.dev"),
            TextNode(" and ", text_type_text),
            TextNode(
                "to youtube", text_type_link, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertEqual(actual, expected)

    def test_text_to_textnodes_1(self):
        text = "This is **bold text with an *italic* word**."
        actual = text_to_textnodes(text)
        expected = [
            TextNode("This is ", text_type_text),
            TextNode([
                TextNode("bold text with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word", text_type_text)
            ], text_type_bold),
            TextNode(".", text_type_text)
        ]
        self.assertEqual(actual, expected)

    def test_text_to_textnodes_2(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        actual = text_to_textnodes(text)
        expected = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode("obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
        ]
        self.assertEqual(actual, expected)

    def test_text_to_textnodes_3(self):
        text = "This is **bold text with an *italic* word, an image, ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a link [link](https://boot.dev) inside**."
        actual = text_to_textnodes(text)
        expected = [
            TextNode("This is ", text_type_text),
            TextNode(
                [
                    TextNode("bold text with an ", text_type_text),
                    TextNode("italic", text_type_italic),
                    TextNode(" word, an image, ", text_type_text),
                    TextNode("obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
                    TextNode(" and a link ", text_type_text),
                    TextNode("link", text_type_link, "https://boot.dev"),
                    TextNode(" inside", text_type_text)
                ], text_type_bold),
            TextNode(".", text_type_text)
        ]
        self.assertEqual(actual, expected)

    def test_text_to_textnodes_4(self):
        text = "[this is a link](http://www.hjerting.com) and some other text [this is another link](https://www.wolf.no)"
        actual = text_to_textnodes(text)
        expected = [
            TextNode("this is a link", text_type_link, "http://www.hjerting.com"),
            TextNode(" and some other text ", text_type_text),
            TextNode("this is another link", text_type_link, "https://www.wolf.no")
        ]
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()