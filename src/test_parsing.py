import unittest

from parsing import split_nodes_delimiter
from textnode import TextNode, TextType

class TestParsing(unittest.TestCase):
	def test_parsing(self):
		old = [TextNode("This is text with a **bolded phrase** in the middle", TextType.PLAIN)]
		new = split_nodes_delimiter(old, "**", TextType.BOLD)
		self.assertEqual(new, [
    		TextNode("This is text with a ", TextType.PLAIN),
    		TextNode("bolded phrase", TextType.BOLD),
    		TextNode(" in the middle", TextType.PLAIN),
		])
		old = [TextNode("This is text with a **bolded phrase** in the middle**plusextrajunk", TextType.PLAIN)]
		new = split_nodes_delimiter(old, "**", TextType.BOLD)
		self.assertEqual(new, [
    		TextNode("This is text with a ", TextType.PLAIN),
    		TextNode("bolded phrase", TextType.BOLD),
    		TextNode(" in the middle**plusextrajunk", TextType.PLAIN),
		])
