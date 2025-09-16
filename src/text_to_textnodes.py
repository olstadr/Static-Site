from textnode import TextType, TextNode
from split_nodes import split_nodes_image, split_nodes_link
from split_delimiter import split_nodes_delimiter

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.PLAIN_TEXT)]
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD_TEXT)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC_TEXT)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)
    return nodes