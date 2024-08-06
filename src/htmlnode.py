class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        v = self.value
        if self.value:
            v = f"'{self.value}'"
        return f"HTMLNode(tag={self.tag}, value={v}, children={self.children}, props={self.props})"

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        prop_str = ""
        if self.props:
            for key, value in self.props.items():
                prop_str += f' {key}="{value}"'
        return prop_str
