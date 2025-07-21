import unittest

from parsing import *
from parsing import split_nodes_delimiter
from textnode import TextNode, TextType

class TestParsing(unittest.TestCase):
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

	def test_text_to_text_nodes(self):
		nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
		expected = [
			TextNode("This is ", TextType.PLAIN),
			TextNode("text", TextType.BOLD),
			TextNode(" with an ", TextType.PLAIN),
			TextNode("italic", TextType.ITALIC),
			TextNode(" word and a ", TextType.PLAIN),
			TextNode("code block", TextType.CODE),
			TextNode(" and an ", TextType.PLAIN),
			TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
			TextNode(" and a ", TextType.PLAIN),
			TextNode("link", TextType.LINK, "https://boot.dev"),
		]
		self.assertEqual(nodes, expected)

	def test_image_parsing(self):
		text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
		self.assertEqual(extract_markdown_images(text), [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])
	
	def test_link_parsing(self):
		# This shouldnt have any matches because these are images and not links
		text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
		self.assertEqual(extract_markdown_links(text), [])
		text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
		self.assertEqual(extract_markdown_links(text), [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])
	
	def test_link_extraction(self):
		node = TextNode(
			"This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
			TextType.PLAIN,
		)
		new_nodes = split_nodes_link([node])
		self.assertEqual(new_nodes, 
		 [
			 TextNode("This is text with a link ", TextType.PLAIN),
			 TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
			 TextNode(" and ", TextType.PLAIN),
			 TextNode(
				 "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
			 ),
		 ])

	def test_image_extraction(self):
		node = TextNode(
			"This is text with an image ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
			TextType.BOLD,
		)
		new_nodes = split_nodes_image([node])
		self.assertEqual(new_nodes, 
		 [
			 TextNode("This is text with an image ", TextType.BOLD),
			 TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
			 TextNode(" and ", TextType.BOLD),
			 TextNode(
				 "to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev"
			 ),
		 ])
	
	def test_image_and_link_extraction(self):
		node = TextNode(
			"This is text with an image ![to boot dev](https://www.boot.dev) and a link [to youtube](https://www.youtube.com/@bootdotdev). Isnt that neat?!",
			TextType.ITALIC
		)
		new_nodes1 = split_nodes_image(split_nodes_link([node]))
		new_nodes2 = split_nodes_link(split_nodes_image([node]))
		self.assertEqual(new_nodes1, new_nodes2)
		self.assertEqual(new_nodes1, 
			[
				TextNode("This is text with an image ", TextType.ITALIC),
				TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
				TextNode(" and a link ", TextType.ITALIC),
				TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
				TextNode(". Isnt that neat?!", TextType.ITALIC)
			]
		)

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
		old = new
		new = split_nodes_delimiter(old, "**", TextType.BOLD)
		self.assertEqual(old, new)
