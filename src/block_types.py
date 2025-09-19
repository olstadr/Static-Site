from enum import Enum

class BlockType(Enum):
    paragraph = "paragraph"
    heading = "heading"
    code = "code"
    quote = "quote"
    unordered_list = "unordered_list"
    ordered_list = "ordered_list"

def block_to_block_type(block):
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.heading
    if block.startswith("```") and block.endswith("```"):
        return BlockType.code
    if block == "":
        return BlockType.paragraph
    split_block = block.splitlines()
    q = True
    for line in split_block:
        if not line.startswith(">"):
            q = False
            break
    if q:
        return BlockType.quote
    u = True
    for line in split_block:
        if not line.startswith("- "):
            u = False
            break
    if u:
        return BlockType.unordered_list
    i = 1
    o = True
    for line in split_block:
        if not line.startswith(f"{i}. "):
            o = False
            break
        i += 1
    if o:
        return BlockType.ordered_list
    else:
        return BlockType.paragraph
        