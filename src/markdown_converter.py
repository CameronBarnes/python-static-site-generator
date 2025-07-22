
import re
from typing import Tuple
from htmlnode import HTMLNode, LeafNode, ParentNode
from parsing import BlockType, block_to_block_type, markdown_to_blocks, text_to_textnodes
from textnode import TextNode, TextType


def markdown_to_html_node(markdown: str) -> HTMLNode:
	blocks = markdown_to_blocks(markdown)
	return ParentNode("div", list(map(block_to_html_node, blocks)))

def block_to_html_node(block: str) -> HTMLNode:
	block_type = block_to_block_type(block)
	match block_type:
		case BlockType.PARAGRAPH:
			return textnodes_to_html(text_to_textnodes(block.replace("\n", " ").strip()), "p")
		case BlockType.HEADING:
			return strip_and_inline("h" + str(block.split(" ", 1)[0].count("#")), block.replace("\n", " ").strip(), r"#{1,6} ", True)
		case BlockType.QUOTE:
			return strip_and_inline("q", block, ">")
		case BlockType.CODE:
			return ParentNode("pre", [LeafNode("code", block[3:-3].lstrip())])
		case BlockType.UNORDERED_LIST:
			return strip_and_inline("ul", block, "- ", False, True)
		case BlockType.ORDERED_LIST:
			return strip_and_inline("ol", block, r"[1-9]\d*\. ", True, True)
		case _:
			raise Exception(f"Unknown BlockType value: {block_type}")

def strip_and_inline(tag:str, markdown: str, prefix: str, regex=False, list_item=False) -> HTMLNode:
	out = []
	lines = markdown.splitlines()
	mult = len(lines) > 1
	for item in lines:
		if regex == True:
			item = re.sub(prefix, "", item, 1)
		else:
			item = item.lstrip(prefix)
		if not list_item:
			out.extend(list(map(lambda node: node.to_html_node(), text_to_textnodes(item))))
		else:
			out.append(ParentNode("li", list(map(lambda node: node.to_html_node(), text_to_textnodes(item)))))
		if mult and not list_item:
			out.append(TextNode("\n", TextType.PLAIN).to_html_node())
	return ParentNode(tag, out)

def textnodes_to_html(nodes: list[TextNode], parent="") -> HTMLNode:
	if len(nodes) == 1:
		return nodes[0].to_html_node()
	return ParentNode(parent, list(map(lambda node: node.to_html_node(), nodes)))

