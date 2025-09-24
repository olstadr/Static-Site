import unittest
from extract_title import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_simple_title(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_extract_title_not_first_line(self):
        md = "intro\n## subtitle\n# Real Title\ntext"
        self.assertEqual(extract_title(md), "Real Title")

    def test_ignores_h2_and_deeper(self):
        md = "## Not it\n### Also not\n# Yes"
        self.assertEqual(extract_title(md), "Yes")

    def test_trims_spaces_after_hash(self):
        self.assertEqual(extract_title("#    Spaced"), "Spaced")

    def test_keeps_inner_hashes(self):
        self.assertEqual(extract_title("# C# Guide"), "C# Guide")

    def test_raises_when_missing(self):
        with self.assertRaises(Exception):
            extract_title("no headers here")

if __name__ == "__main__":
    import unittest
    unittest.main()