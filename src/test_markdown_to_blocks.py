import unittest

from markdown_to_blocks import markdown_to_blocks

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
            )

    def test_leading_trailing_blank_lines(self):
        md = """

This is a paragraph

"""
        self.assertEqual(
            markdown_to_blocks(md),
            ["This is a paragraph"],
        )

    def test_multiple_consecutive_blank_lines(self):
        md = """First


Second"""
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "First",
                "Second"
             ],
        )

    def test_strip_spaces_in_blocks(self):
        md = """   First block    

Second block   """
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "First block",
                "Second block",
             ],
        )

    def test_single_block_no_separators(self):
        md = "Just one block with no separators"
        self.assertEqual(
            markdown_to_blocks(md),
            ["Just one block with no separators"],
        )

    def test_only_whitespace(self):
        md = """


"""
        self.assertEqual(
            markdown_to_blocks(md),
            [],
        )

    def test_windows_newlines(self):
        md = "# Title\r\n\r\nBody line 1\r\nBody line 2"
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "# Title",
                "Body line 1\nBody line 2",
             ],
        )

    def test_internal_single_newlines_stay_in_block(self):
        md = """Line 1
Line 2
Line 3"""
        self.assertEqual(
            markdown_to_blocks(md),
            ["Line 1\nLine 2\nLine 3"],
        )

    def test_empty_space_only_block_removed(self):
        md = """A

    
B"""
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "A",
                "B",
             ],
        )

if __name__ == "__main__":
    unittest.main()
        