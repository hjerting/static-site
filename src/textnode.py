from leafnode import LeafNode
import re

tokens = {
    '*': {
        1: 'italic',
        2: 'bold'
    }
}

# Text types
text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"


class TextNode:
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other_node):
        if self.text != other_node.text:
            return False
        if self.text_type != other_node.text_type:
            return False
        if self.url != other_node.url:
            return False
        return True

    def to_html_node(self):
        text_type = self.text_type
        text = self.text
        url = self.url
        # text_type_text = "text"
        # This should become a LeafNode with no tag, just a raw text value.
        if text_type == "text":
            return LeafNode(value=text)

        # text_type_bold = "bold"
        # This should become a LeafNode with a "b" tag and the text
        if text_type == "bold":
            return LeafNode(tag="b", value=text)

        # text_type_italic = "italic"
        # "i" tag, text
        if text_type == "italic":
            return LeafNode(tag="i", value=text)

        # text_type_code = "code"
        # "code" tag, text
        if text_type == "code":
            return LeafNode(tag="code", value=text)

        # text_type_link = "link"
        # "a" tag, anchor text, and "href" prop
        if text_type == "link":
            return LeafNode(tag="a", value=text, props={"href": url})

        # text_type_image = "image"
        # "img" tag, empty string value, "src" and "alt" props
        # ("src" is the image URL, "alt" is the alt text)
        if text_type == "image":
            return LeafNode(tag="img", value="", props={"src": "", "alt": ""})

        # If it gets a TextNode that is none of those types, it should raise an exception.
        raise ValueError("Invalid TextNode")

    @staticmethod
    def text_node_to_html_node(text_node):
        return text_node.to_html_node()

    def __repr__(self):
        url = ""
        if self.url:
            url = f', "{self.url}"'
        text = self.text
        if isinstance(text, str):
            text = f'"{text}"'
        return f'TextNode({text}, "{self.text_type}"{url})'

def findToken(c, count, text):
    i = count
    length = len(text)
    while (i < length):
        currentCount = 0
        while i < length and text[i] != c:
            i += 1
        while i < length and text[i] == c:
            currentCount += 1
            i += 1
        if currentCount == count:
            return i - count
    return -1

def textEnd(text):
    i = 0
    length = len(text)
    while i < length and text[i] not in tokens:
        i += 1
    return i

def tokenCount(c, text):
    count = 1
    length = len(text)
    while (count < length and text[count] == c):
        count += 1
    return count

def parsePart(text, parseType):
    tokenFound = False
    for t in tokens:
        if t in text:
            tokenFound = True
            break
    if not tokenFound:
        return TextNode(text, parseType)
    return TextNode(markdownParser(text), parseType)

def markdownParser(text):
    parsed = []
    while len(text) > 0:
        c = text[0]
        if c not in tokens:
            index = textEnd(text)
            parsed.append(TextNode(text[:index], "text"))
            text = text[index:]
        else:
            count = tokenCount(c, text)
            index = findToken(c, count, text)
            type = tokens[c][count]
            parsed.append(parsePart(text[count:index], type))
            text = text[index + count:]
    return parsed

def split_nodes_delimiter(nodes, delimiter, text_type):
    delimiter_length = len(delimiter)
    if delimiter not in tokens:
        tokens[delimiter] = {}
    tokens[delimiter][delimiter_length] = text_type
    result = []
    for node in nodes:
        result.append(TextNode(markdownParser(node.text), "text"))
    if len(result) == 1:
        return result[0]
    return TextNode(result, "text")

def extract_markdown(text, regexp):
    matches = re.findall(regexp, text)
    return matches

def extract_markdown_images(text):
    regexp = r"!\[([\w ]+)\]\(([^()]+)\)"
    return extract_markdown(text, regexp)

def extract_markdown_links(text):
    regexp = r"(?<!\!)\[(.*?)\]\((.*?)\)"
    return extract_markdown(text, regexp)

def split_nodes(nodes, node_function, text_node_type):
    new_nodes = []
    for node in nodes:
        text_type = node.text_type
        if type(node.text) == list:
            insert = split_nodes(node.text, node_function, text_node_type)
            new_nodes.append(TextNode(insert, text_type))
        else:
            if text_type == text_type_link or text_type == text_type_image:
                new_nodes.append(node)
            else:
                text = node.text
                elements = node_function(text)
                for element in elements:
                    search_str = f"{'!' if text_node_type == 'image' else ''}[{element[0]}]({element[1]})"
                    index = text.find(search_str)
                    if index >= 0:
                        if index > 0:
                            text_node = text[:index]
                            new_nodes.append(TextNode(text_node, text_type))
                            text = text[index:]
                        text = text[len(search_str):]
                        new_nodes.append(TextNode(element[0], text_node_type, element[1]))
                if len(text) > 0:
                    new_nodes.append(TextNode(text, text_type))
    return new_nodes

def split_nodes_image(nodes):
    result = split_nodes(nodes, extract_markdown_images, text_type_image)
    return result

def split_nodes_link(nodes):
    return split_nodes(nodes, extract_markdown_links, text_type_link)

def text_to_textnodes(text):
    nodes = markdownParser(text)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def main():
    """
    node = TextNode(
        "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
        text_type_text,
    )
    actual = split_nodes_image([node])

    expected = [
        TextNode("This is text with an ", text_type_text),
        TextNode(
            "image",
            text_type_image,
            "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"
        ),
        TextNode(" and another ", text_type_text),
        TextNode(
            "second image",
            text_type_image,
            "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
        ),
    ]

    print(actual)
    #print("---------")
    #print(expected)
    """
    pass

if __name__ == "__main__":
    main()