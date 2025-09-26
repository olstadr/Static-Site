from .textnode import TextNode, TextType

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        string = ""
        if self.props != None:
            pairs = self.props.items()
            for key, value in pairs:
                string += (f' {key}="{value}"')
        return string

    def __repr__(self):
        return f"""
        tag = {self.tag},
        value = {self.value},
        children = {self.children},
        props = {self.props}
        """
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value == None:
            raise ValueError("node has no value")
        if self.tag is None:
            return self.value
        else:
            return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
        
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("node has no tag")
        if self.children is None:
            raise ValueError("node has no children")
        else:
            opening_tag = f"<{self.tag}{self.props_to_html()}>"
            closing_tag = f"</{self.tag}>"
            inner = "".join(child.to_html() for child in self.children)
            return opening_tag + inner + closing_tag
        
def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.PLAIN_TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD_TEXT:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC_TEXT:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE_TEXT:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.alt})
    else:
        raise Exception(f"Unknown TextType: {text_node.text_type}")