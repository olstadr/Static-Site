

def markdown_to_blocks(markdown):
    text = markdown.replace("\r\n", "\n")
    pieces = text.split("\n\n")
    blocks = []
    for p in pieces:
        b = p.strip()
        if b:
            blocks.append(b)
    return blocks