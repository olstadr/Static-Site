from textnode import TextNode, TextType
from extract import extract_markdown_images, extract_markdown_links

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue

        remaining = node.text
        while True:
            imgs = extract_markdown_images(remaining)
            if not imgs:
                break

            alt, url = imgs[0]
            marker = f"![{alt}]({url})"
            before, after = remaining.split(marker, 1)

            if before:
                new_nodes.append(TextNode(before, TextType.PLAIN_TEXT))
            new_nodes.append(TextNode(None, TextType.IMAGE, url=url, alt=alt))
            remaining = after

        if remaining:
            new_nodes.append(TextNode(remaining, TextType.PLAIN_TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue

        remaining = node.text
        while True:
            lnks = extract_markdown_links(remaining)
            if not lnks:
                break

            label, url = lnks[0]
            marker = f"[{label}]({url})"
            before, after = remaining.split(marker, 1)

            if before:
                new_nodes.append(TextNode(before, TextType.PLAIN_TEXT))
            new_nodes.append(TextNode(label, TextType.LINK, url=url))
            remaining = after

        if remaining:
            new_nodes.append(TextNode(remaining, TextType.PLAIN_TEXT))
    return new_nodes