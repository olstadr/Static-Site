import unittest

from .textnode import TextNode, TextType
from .split_delimiter import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_simple_code_split(self):
        node = TextNode("a `b` c", TextType.PLAIN_TEXT)
        out = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        self.assertEqual([(n.text, n.text_type) for n in out], [
            ("a ", TextType.PLAIN_TEXT),
            ("b", TextType.CODE_TEXT),
            (" c", TextType.PLAIN_TEXT),
        ])

    def test_multiple_bold_splits(self):
        node = TextNode("x **y** z **w** q", TextType.PLAIN_TEXT)
        out = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        self.assertEqual([(n.text, n.text_type) for n in out], [
            ("x ", TextType.PLAIN_TEXT),
            ("y", TextType.BOLD_TEXT),
            (" z ", TextType.PLAIN_TEXT),
            ("w", TextType.BOLD_TEXT),
            (" q", TextType.PLAIN_TEXT),
        ])

    def test_unbalanced_raises(self):
        node = TextNode("start `mid end", TextType.PLAIN_TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE_TEXT)

    def test_pass_through_non_plain(self):
        bold_node = TextNode("already bold", TextType.BOLD_TEXT)
        out = split_nodes_delimiter([bold_node], "**", TextType.BOLD_TEXT)
        self.assertEqual(len(out), 1)
        self.assertIs(out[0], bold_node)

    def test_skips_empty_parts(self):
        node = TextNode("before `` after", TextType.PLAIN_TEXT)
        out = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        self.assertEqual([(n.text, n.text_type) for n in out], [
            ("before ", TextType.PLAIN_TEXT),
            (" after", TextType.PLAIN_TEXT),
        ])

if __name__ == "__main__":
    unittest.main()