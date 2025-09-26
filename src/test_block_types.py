import unittest

from .block_types import block_to_block_type, BlockType

class TestBlockToBlockType(unittest.TestCase):
    def test_heading_valid_levels(self):
        self.assertEqual(block_to_block_type("# A"), BlockType.heading)
        self.assertEqual(block_to_block_type("###### Z"), BlockType.heading)

    def test_heading_invalid(self):
        self.assertEqual(block_to_block_type("####### too many"), BlockType.paragraph)
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.paragraph)

    def test_code_block_simple(self):
        self.assertEqual(block_to_block_type("```\ncode\n```"), BlockType.code)

    def test_code_block_single_line(self):
        self.assertEqual(block_to_block_type("```code```"), BlockType.code)

    def test_quote_all_lines_prefixed(self):
        self.assertEqual(block_to_block_type("> a\n> b"), BlockType.quote)

    def test_quote_with_blank_quoted_line(self):
        self.assertEqual(block_to_block_type(">\n> line"), BlockType.quote)

    def test_quote_reject_unprefixed_line(self):
        self.assertEqual(block_to_block_type("> a\nnot quote"), BlockType.paragraph)

    def test_unordered_list_basic(self):
        self.assertEqual(block_to_block_type("- a\n- b"), BlockType.unordered_list)

    def test_unordered_list_blank_item_allowed(self):
        self.assertEqual(block_to_block_type("- a\n- "), BlockType.unordered_list)

    def test_unordered_list_reject_unprefixed(self):
        self.assertEqual(block_to_block_type("- a\na"), BlockType.paragraph)

    def test_ordered_list_basic(self):
        self.assertEqual(block_to_block_type("1. a\n2. b\n3. c"), BlockType.ordered_list)

    def test_ordered_list_requires_increment(self):
        self.assertEqual(block_to_block_type("1. a\n1. b"), BlockType.paragraph)
        self.assertEqual(block_to_block_type("1. a\n3. b"), BlockType.paragraph)

    def test_ordered_list_blank_item_allowed(self):
        self.assertEqual(block_to_block_type("1. a\n2. "), BlockType.ordered_list)

    def test_paragraph_fallback(self):
        self.assertEqual(block_to_block_type("just text"), BlockType.paragraph)

    def test_empty_block_is_paragraph(self):
        self.assertEqual(block_to_block_type(""), BlockType.paragraph)

if __name__ == "__main__":
    unittest.main()