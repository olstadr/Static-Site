import unittest

from textnode import TextType, TextNode
from split_nodes import split_nodes_image, split_nodes_link



class TestSplitNodes(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN_TEXT),
                TextNode(None, TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png", alt="image"),
                TextNode(" and another ", TextType.PLAIN_TEXT),
                TextNode(None, TextType.IMAGE, "https://i.imgur.com/3elNhQu.png", alt="second image"),
            ],
            new_nodes,
        )
        
    def test_no_images(self):
        node = TextNode("no pics here", TextType.PLAIN_TEXT)
        self.assertEqual(split_nodes_image([node]), [node])

    def test_image_at_start(self):
        node = TextNode("![alt](u) tail", TextType.PLAIN_TEXT)
        self.assertEqual(
            split_nodes_image([node]),
            [TextNode(None, TextType.IMAGE, url="u", alt="alt"),
            TextNode(" tail", TextType.PLAIN_TEXT)]
        )

    def test_image_at_end(self):
        node = TextNode("head ![alt](u)", TextType.PLAIN_TEXT)
        self.assertEqual(
            split_nodes_image([node]),
            [TextNode("head ", TextType.PLAIN_TEXT),
            TextNode(None, TextType.IMAGE, url="u", alt="alt")]
        )

    def test_back_to_back_images(self):
        node = TextNode("![a](u1)![b](u2)", TextType.PLAIN_TEXT)
        self.assertEqual(
            split_nodes_image([node]),
            [
                TextNode(None, TextType.IMAGE, url="u1", alt="a"),
                TextNode(None, TextType.IMAGE, url="u2", alt="b"),
            ]
        )

    def test_malformed_not_split(self):
        node = TextNode("![alt](missing", TextType.PLAIN_TEXT)
        self.assertEqual(split_nodes_image([node]), [node])

    def test_pass_through_non_text(self):
        img_node = TextNode(None, TextType.IMAGE, url="u", alt="a")
        self.assertEqual(split_nodes_image([img_node]), [img_node])
        