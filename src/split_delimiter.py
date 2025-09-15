from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_list = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.PLAIN_TEXT:
            new_list.append(old_node)
            continue

        if old_node.text.count(delimiter) % 2 != 0:
            raise Exception("odd amount of delimiters found in text")
        
        parts = old_node.text.split(delimiter)
        for i, part in enumerate(parts):
            if not part:
                continue
            part_type = TextType.PLAIN_TEXT if i % 2 == 0 else text_type
            new_list.append(TextNode(part, part_type))
    return new_list