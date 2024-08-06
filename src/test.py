import re

from textnode import (
                        TextNode,
                        extract_markdown,
                        split_nodes_link,
                        markdownParser
)

def is_heading(text):
    regex = r"^#{1,6} .*$"
    result = re.search(regex, text)
    return result


def main():
    text = "# Header 1"
    if is_heading(text):
        print("Block is heading")
    else:
        print("Block NOT heading")
    text = "####### Paragraph"
    if is_heading(text):
        print("Block is heading")
    else:
        print("Block NOT heading")


if __name__ == "__main__":
    main()

