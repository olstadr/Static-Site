import unittest

from .markdown_to_html_node import markdown_to_html_node, text_to_children, block_to_html_node

class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading_levels(self):
        md = "# H1\n\n###### H6\n"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(html, "<div><h1>H1</h1><h6>H6</h6></div>")

    def test_heading_invalid_too_many_hashes(self):
        md = "####### Too many\n"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(html, "<div><p>####### Too many</p></div>")

    def test_heading_invalid_no_space(self):
        md = "######NoSpace\n"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(html, "<div><p>######NoSpace</p></div>")

    def test_paragraph_multiline_inline(self):
        md = "This is **bold** and _it_ with `code`.\nStill same paragraph line.\n"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bold</b> and <i>it</i> with <code>code</code>. Still same paragraph line.</p></div>",
        )

    def test_blockquote_multiline_inline(self):
        md = "> hello **bold**\n> and _italic_\n"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><blockquote>hello <b>bold</b>\nand <i>italic</i></blockquote></div>",
        )

    def test_unordered_list_mixed_markers(self):
        md = "- one\n* two with **bold**\n- three\n"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><ul><li>one</li><li>two with <b>bold</b></li><li>three</li></ul></div>",
        )

    def test_ordered_list_numbers_multi_digit(self):
        md = "1. a\n2. b\n3. c\n"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><ol><li>a</li><li>b</li><li>c</li></ol></div>",
        )

    def test_code_block_literal(self):
        md = "```\n_text_ **bold** `code`\n```\n"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><pre><code>_text_ **bold** `code`\n</code></pre></div>",
        )

    def test_fallback_unknown_as_paragraph(self):
        md = "::not a known block::\n"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(html, "<div><p>::not a known block::</p></div>")

if __name__ == "__main__":
    unittest.main()