import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
	def test_eq(self):
		node = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is a text node", TextType.BOLD)
		node3 = TextNode("Different text node", TextType.BOLD)
		node4 = TextNode("This is a text node", TextType.ITALIC)
		node5 = TextNode("This is a text node", TextType.BOLD, "example.com")
		self.assertEqual(node, node2)
		self.assertNotEqual(node, node3)
		self.assertNotEqual(node, node4)
		self.assertNotEqual(node, node5)
		self.assertEqual(node, node)
	
	def test_to_html(self):
		node1 = TextNode("Test text here!", TextType.PLAIN).to_html_node()
		self.assertEqual(f"{node1}", 'HTMLNode(None, "Test text here!", None, None)')
		self.assertEqual(node1.to_html(), "Test text here!")

		bad_node1 = TextNode("Test text here!", TextType.LINK)
		self.assertRaises(ValueError, bad_node1.to_html_node)
		bad_node2 = TextNode("Test text here!", TextType.IMAGE)
		self.assertRaises(ValueError, bad_node2.to_html_node)

		node2 = TextNode("Test text here!", TextType.LINK, "example.com").to_html_node()
		self.assertEqual(f"{node2}", 'HTMLNode(a, "Test text here!", None, {\'href\': \'example.com\'})')
		self.assertEqual(node2.to_html(), '<a href="example.com">Test text here!</a>')
		node3 = TextNode("Test text here!", TextType.IMAGE, "example.com").to_html_node()
		self.assertEqual(f"{node3}", 'HTMLNode(img, "", None, {\'src\': \'example.com\', \'alt\': \'Test text here!\'})')
		self.assertEqual(node3.to_html(), '<img src="example.com" alt="Test text here!"></img>')

if __name__ == "__main__":
	unittest.main()
