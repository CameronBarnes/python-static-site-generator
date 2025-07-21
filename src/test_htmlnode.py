import unittest

from htmlnode import *


class TestHTMLNode(unittest.TestCase):
	def test_props(self):
		node1 = HTMLNode(props={
			"href": "https://www.google.com",
			"target": "_blank",
		})
		node2 = HTMLNode()
		self.assertEqual(node1.props_to_html(), 'href="https://www.google.com" target="_blank"')
		self.assertEqual(node2.props_to_html(), "")
		self.assertTrue(node2.props is None and node2.tag is None and node2.value is None and node2.children is None)

class TestLeafNode(unittest.TestCase):
	def test_to_html(self):
		node1 = LeafNode("p", "text content")
		node2 = LeafNode("a", "Link!", {"href": "example.com"})
		self.assertEqual(node1.to_html(), "<p>text content</p>")
		self.assertEqual(node2.to_html(), '<a href="example.com">Link!</a>')

class TestParentNode(unittest.TestCase):
	def test_to_html(self):
		node = ParentNode(
			"p",
			[
				LeafNode("b", "Bold text"),
				LeafNode(None, "Normal text"),
				LeafNode("i", "italic text"),
				LeafNode(None, "Normal text"),
			],
		)
		self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
	
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

if __name__ == "__main__":
	unittest.main()
