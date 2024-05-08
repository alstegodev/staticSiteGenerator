class HTMLNode:

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"HTMLNode({self.tag},{self.value},{self.children},{self.props})"

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props is None:
            return ""
        result = ""
        for prop in self.props:
            result += " " + prop + "=\"" + self.props[prop] + "\""
        return result


class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def __repr__(self):
        return f"LeafNode({self.tag},{self.value},{self.props})"

    def to_html(self):
        if self.value is None:
            raise ValueError("Invalid HTML: no value")
        elif self.tag is None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        super().__init__(tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode: No Tag provided")
        result = f"<{self.tag}>"
        for child in self.children:
            result += child.to_html()

        result += f"</{self.tag}>"
        return result

