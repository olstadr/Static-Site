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

    lines = block.splitlines()

    if len(lines) == 1:
        line = lines[0].strip()
        if line.startswith("```") and line.endswith("```") and len(line) >= 6:
            return BlockType.code
    elif len(lines) >= 2 and lines[0].strip() == "```" and lines[-1].strip() == "```":
        return BlockType.code

    has_quote_line = False
    is_quote = True
    for l in lines:
        s = l.strip()
        if s == "":
            continue
        if s.startswith(">"):
            has_quote_line = True
        else:
            is_quote = False
            break
    if is_quote and has_quote_line:
        return BlockType.quote

    is_ul, has_item = True, False
    for l in lines:
        ls = l.lstrip()
        if ls == "":
            continue
        if ls.startswith("- ") or ls.startswith("* "):
            has_item = True
        else:
            is_ul = False
            break
    if is_ul and has_item:
        return BlockType.unordered_list

    expected = 1
    is_ol, has_item = True, False
    for l in lines:
        ls = l.lstrip()
        if ls == "":
            continue
        prefix = f"{expected}. "
        if ls.startswith(prefix):
            has_item = True
            expected += 1
        else:
            is_ol = False
            break
    if is_ol and has_item:
        return BlockType.ordered_list

    return BlockType.paragraph