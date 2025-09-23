from htmlnode import HTMLNode, ParentNode, LeafNode, text_node_to_html_node
from markdown_to_blocks import markdown_to_blocks
from block_types import block_to_block_type, BlockType
from text_to_textnodes import text_to_textnodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        btype = block_to_block_type(block)
        children.append(block_to_html_node(block, btype))
    return ParentNode("div", children)
        
def text_to_children(text):
    textnodes = text_to_textnodes(text)
    return [text_node_to_html_node(tn) for tn in textnodes]

def block_to_html_node(block, btype):
    if btype == BlockType.paragraph:
        text = " ".join(line.strip() for line in block.split("\n") if line.strip() != "")
        return ParentNode("p", text_to_children(text))
    
    elif btype == BlockType.heading:
        i = 0
        n = len(block)
        while i < n and i < 6 and block[i] == "#":
            i += 1
        if i == 0 or i >= n or block[i] != " ":
            return ParentNode("p", text_to_children(block))
        level = i
        text = block[i+1:]
        children = text_to_children(text)
        return ParentNode(f"h{level}", children)
    
    elif btype == BlockType.quote:
        lines = block.split("\n")
        cleaned = []
        for line in lines:
            if line.startswith("> "):
                cleaned.append(line[2:])
            elif line.startswith(">"):
                cleaned.append(line[1:])
            else:
                cleaned.append(line)
        text = "\n".join(cleaned)
        children = text_to_children(text)
        return ParentNode("blockquote", children)

    elif btype == BlockType.unordered_list:
        items = []
        for line in block.split("\n"):
            ls = line.lstrip()
            if not ls:
                continue
            if ls.startswith("- "):
                text = ls[2:]
            elif ls.startswith("* "):
                text = ls[2:]
            else:
                continue
            items.append(ParentNode("li", text_to_children(text)))
        return ParentNode("ul", items)

    elif btype == BlockType.ordered_list:
        items = []
        for line in block.split("\n"):
            ls = line.lstrip()
            if not ls:
                continue
            i = 0
            while i < len(ls) and ls[i].isdigit():
                i += 1
            if i > 0 and i + 1 < len(ls) and ls[i] == "." and ls[i+1] == " ":
                text = ls[i+2:]
                items.append(ParentNode("li", text_to_children(text)))
            else:
                continue
        return ParentNode("ol", items)

    elif btype == BlockType.code:
        lines = block.split("\n")
        if len(lines) == 1 and lines[0].startswith("```") and lines[0].endswith("```"):
            inner = lines[0][3:-3]
        else:
            inner_lines = lines[1:-1]
            non_empty = [ln for ln in inner_lines if ln != ""]
            if non_empty:
                import re
                def leading_spaces(s): return len(re.match(r"[ \t]*", s).group(0))
                common = min(leading_spaces(ln) for ln in non_empty)
                if common > 0:
                    inner_lines = [ln[common:] if len(ln) >= common else ln for ln in inner_lines]
            inner = "\n".join(inner_lines)
        if inner != "" and not inner.endswith("\n"):
            inner += "\n"
        return ParentNode("pre", [ParentNode("code", [LeafNode(None, inner)])])

    else:
        return ParentNode("p", text_to_children(block))