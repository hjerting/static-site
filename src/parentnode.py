from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag = None, children = None, props = None):
        super().__init__(tag = tag, value = None, children = children, props = props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Parent node must have a tag value.")
        if self.children == None:
            raise ValueError("Parent node must have at least one child node.")
        childrenHTML = ""
        for child in self.children:
            childrenHTML += child.to_html()
        return f'<{self.tag}>{childrenHTML}</{self.tag}>'