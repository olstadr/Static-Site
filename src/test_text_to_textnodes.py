import unittest

from .textnode import TextNode, TextType
from .text_to_textnodes import text_to_textnodes

class TestTextToTextNodes(unittest.TestCase):
    def test_text_only(self):
        nodes = text_to_textnodes("hello")
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text_type, TextType.PLAIN_TEXT)
        self.assertEqual(nodes[0].text, "hello")

    def test_code_single(self):
        nodes = text_to_textnodes("`x`")
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text_type, TextType.CODE_TEXT)
        self.assertEqual(nodes[0].text, "x")

    def test_bold_single(self):
        nodes = text_to_textnodes("**y**")
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text_type, TextType.BOLD_TEXT)
        self.assertEqual(nodes[0].text, "y")

    def test_italic_single(self):
        nodes = text_to_textnodes("_z_")
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text_type, TextType.ITALIC_TEXT)
        self.assertEqual(nodes[0].text, "z")

    def test_mixed_sequence(self):
        nodes = text_to_textnodes("a `code` b **bold** c _ital_")
        kinds = [n.text_type for n in nodes]
        texts = [n.text for n in nodes]
        self.assertEqual(
            kinds,
            [
                TextType.PLAIN_TEXT, TextType.CODE_TEXT, TextType.PLAIN_TEXT,
                TextType.BOLD_TEXT, TextType.PLAIN_TEXT, TextType.ITALIC_TEXT
            ],
        )
        self.assertEqual(texts, ["a ", "code", " b ", "bold", " c ", "ital"])

    def test_code_wins_over_inner_markers(self):
        nodes = text_to_textnodes("`**bold in code**`")
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text_type, TextType.CODE_TEXT)
        self.assertEqual(nodes[0].text, "**bold in code**")

    def test_multiple_bold(self):
        nodes = text_to_textnodes("a **b** c **d** e")
        kinds = [n.text_type for n in nodes]
        texts = [n.text for n in nodes]
        self.assertEqual(
            kinds,
            [
                TextType.PLAIN_TEXT, TextType.BOLD_TEXT, TextType.PLAIN_TEXT,
                TextType.BOLD_TEXT, TextType.PLAIN_TEXT
            ],
        )
        self.assertEqual(texts, ["a ", "b", " c ", "d", " e"])

    def test_link(self):
        nodes = text_to_textnodes("[t](u)")
        self.assertEqual(len(nodes), 1)
        n = nodes[0]
        self.assertEqual(n.text_type, TextType.LINK)
        self.assertEqual(n.text, "t")
        self.assertEqual(n.url, "u")

    def test_image(self):
        nodes = text_to_textnodes("![alt](url)")
        self.assertEqual(len(nodes), 1)
        n = nodes[0]
        self.assertEqual(n.text_type, TextType.IMAGE)
        self.assertEqual(n.alt, "alt")
        self.assertEqual(n.url, "url")

    def test_combined(self):
        nodes = text_to_textnodes("x `y` and _z_ with ![a](u) and [b](v)")
        kinds = [n.text_type for n in nodes]
        texts = [n.text for n in nodes]
        urls = [getattr(n, "url", None) for n in nodes]
        alts = [getattr(n, "alt", None) for n in nodes]
        self.assertEqual(
            kinds,
            [
                TextType.PLAIN_TEXT, TextType.CODE_TEXT, TextType.PLAIN_TEXT,
                TextType.ITALIC_TEXT, TextType.PLAIN_TEXT, TextType.IMAGE,
                TextType.PLAIN_TEXT, TextType.LINK
            ],
        )
        self.assertEqual(texts, ["x ", "y", " and ", "z", " with ", None, " and ", "b"])
        self.assertEqual(urls,  [None, None, None, None, None, "u",  None,   "v"])
        self.assertEqual(alts,  [None, None, None, None, None, "a",  None,   None])

    def test_unclosed_bold_raises(self):
        with self.assertRaises(ValueError):
            text_to_textnodes("**oops")

    def test_empty_sections_skipped(self):
        nodes = text_to_textnodes("a____b")
        texts = [n.text for n in nodes]
        kinds = [n.text_type for n in nodes]
        self.assertEqual(texts, ["a", "b"])
        self.assertEqual(kinds, [TextType.PLAIN_TEXT, TextType.PLAIN_TEXT])


if __name__ == "__main__":
    unittest.main()