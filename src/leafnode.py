from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag = None, value = None, props = None):
        super().__init__(tag = tag, value = value, props = props, children = None)

    def to_html(self):
        if self.value == None:
            raise ValueError("All leaf nodes require a value.")
        if self.tag == None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'