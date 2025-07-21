import unittest

from parsing import extract_markdown_images, extract_markdown_links, split_nodes_delimiter
from textnode import TextNode, TextType

class TestParsing(unittest.TestCase):
	def test_image_parsing(self):
		text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
		self.assertEqual(extract_markdown_images(text), [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])
	
	def test_link_parsing(self):
		# This shouldnt have any matches because these are images and not links
		text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
		self.assertEqual(extract_markdown_links(text), [])
		text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
		self.assertEqual(extract_markdown_links(text), [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

	def test_delimiter_parsing(self):
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
