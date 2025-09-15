import unittest

from enum import Enum

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq1(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.ITALIC_TEXT)
        self.assertNotEqual(node, node2)

    def test_eq3(self):
        node = TextNode("This is a text node", TextType.CODE_TEXT)
        node2 = TextNode("This is a link node", TextType.LINK, url=None)
        self.assertNotEqual(node, node2)

    def test_eq4(self):
        node = TextNode("This is a link node", TextType.LINK, url="https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertNotEqual(node, node2)

class TestHTMLNode(unittest.TestCase):
    def test_html1(self):
        node = HTMLNode("a", "link text", None, {"href": "https://google.com"})
        result = node.props_to_html()
        expected = ' href="https://google.com"'
        print(f"Expected: '{expected}'")
        print(f"Got: '{result}'")
        self.assertEqual(result, expected)

    def test_html2(self):
        node = HTMLNode("a", "link text", None)
        result = node.props_to_html()
        expected = ''
        print(f"Expected: '{expected}'")
        print(f"Got: '{result}'")
        self.assertEqual(result, expected)

    def test_html3(self):
        node = HTMLNode("a", "link text", None, {"href": "https://google.com", "class": "external-link"})
        result = node.props_to_html()
        expected = ' href="https://google.com" class="external-link"'
        print(f"Expected: '{expected}'")
        print(f"Got: '{result}'")
        self.assertEqual(result, expected)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_none(self):
        node = LeafNode(None, "Hi")
        self.assertEqual(node.to_html(), "Hi")

    def test_leaf_to_html_href_anchor(self):
        node = LeafNode("a", "Click", props={"href":"https://x"})
        self.assertEqual(node.to_html(), '<a href="https://x">Click</a>')

    def test_leaf_to_html_multiple_props(self):
        node = LeafNode("a", "Click me", props={"href":"https://x","target":"_blank"})
        self.assertEqual(node.to_html(), '<a href="https://x" target="_blank">Click me</a>')
    
    def test_leaf_to_html_missing_value(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None).to_html()

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_with_no_props(self):
        child = LeafNode("span", "x")
        parent = ParentNode("div", [child], None)
        self.assertEqual(parent.to_html(), "<div><span>x</span></div>")

    def test_parent_missing_children_raises(self):
        with self.assertRaises(ValueError):
            ParentNode("ul", None).to_html()

    def test_parent_with_empty_children(self):
        parent = ParentNode("div", [])
        self.assertEqual(parent.to_html(), "<div></div>")

    def test_mixed_children_text_and_tagged(self):
        child1 = LeafNode(None, "Hello")
        child2 = LeafNode("b", "World")
        parent = ParentNode("p", [child1, child2])
        self.assertEqual(parent.to_html(), "<p>Hello<b>World</b></p>")

    def test_deep_nesting_multiple_siblings(self):
        a = LeafNode("i", "a")
        b = LeafNode(None, "b")
        inner = ParentNode("span", [a, b])
        outer = ParentNode("div", [inner, LeafNode("u", "c")])
        self.assertEqual(outer.to_html(), "<div><span><i>a</i>b</span><u>c</u></div>")

    def test_props_rendered(self):
        child = LeafNode(None, "x")
        parent = ParentNode("div", [child], {"class": "box", "id": "main"})
        html = parent.to_html()
        self.assertTrue(html.startswith("<div"))
        self.assertIn('class="box"', html)
        self.assertIn('id="main"', html)
        self.assertTrue(html.endswith("</div>"))

    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_plain_text_node_to_leaf(self):
        n = TextNode("hello", TextType.PLAIN_TEXT)
        h = text_node_to_html_node(n)
        self.assertIsNone(h.tag)
        self.assertEqual(h.value, "hello")

    def test_bold_text_node_to_leaf(self):
        n = TextNode("hi", TextType.BOLD_TEXT)
        h = text_node_to_html_node(n)
        self.assertEqual(h.tag, "b")
        self.assertEqual(h.value, "hi")

    def test_italic_text_node_to_leaf(self):
        n = TextNode("yo", TextType.ITALIC_TEXT)
        h = text_node_to_html_node(n)
        self.assertEqual(h.tag, "i")
        self.assertEqual(h.value, "yo")

    def test_code_text_node_to_leaf(self):
        n = TextNode("x = 1", TextType.CODE_TEXT)
        h = text_node_to_html_node(n)
        self.assertEqual(h.tag, "code")
        self.assertEqual(h.value, "x = 1")

    def test_link_text_node_to_leaf(self):
        n = TextNode("Boot.dev", TextType.LINK, url="https://boot.dev")
        h = text_node_to_html_node(n)
        self.assertEqual(h.tag, "a")
        self.assertEqual(h.value, "Boot.dev")
        self.assertEqual(h.props.get("href"), "https://boot.dev")

    def test_image_text_node_to_leaf(self):
        n = TextNode("", TextType.IMAGE, url="cat.png", alt="A cat")
        h = text_node_to_html_node(n)
        self.assertEqual(h.tag, "img")
        self.assertEqual(h.value, "")
        self.assertEqual(h.props.get("src"), "cat.png")
        self.assertEqual(h.props.get("alt"), "A cat")

    def test_raises_on_unknown_type(self):
        class FakeType(Enum):
            WEIRD = "weird"
        n = TextNode("x", FakeType.WEIRD)
        with self.assertRaises(Exception):
            text_node_to_html_node(n)
    
    if __name__ == "__main__":
        unittest.main()