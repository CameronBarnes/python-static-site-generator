import re
from typing import Callable, Tuple
from textnode import TextNode, TextType
from enum import Enum

class BlockType(Enum):
	PARAGRAPH = "p",
	HEADING = "h",
	CODE = "code",
	QUOTE = "quote",
	UNORDERED_LIST = "ul",
	ORDERED_LIST = "li"

# Technicaally this doesnt catch a bunch of bad inputs, but it should still produce the desired outputs
def block_to_block_type(block: str) -> BlockType:
	if block.startswith("```") and block.endswith("```") and len(block) >= 6:
		return BlockType.CODE
	elif block.startswith(">"):
		return BlockType.QUOTE
	elif block.startswith("- "):
		return BlockType.UNORDERED_LIST
	elif re.match(r"#{1,6} .", block):
		return BlockType.HEADING
	elif re.match(r"[1-9]\d*\. ", block):
		return BlockType.ORDERED_LIST
	else:
		return BlockType.PARAGRAPH

def markdown_to_blocks(text: str) -> list[str]:
	out = []
	for item in text.split("\n\n"):
		item = item.strip()
		if item == "":
			continue
		out.append(item)
	return out

def text_to_textnodes(text: str) -> list[TextNode]:
	nodes = [TextNode(text, TextType.PLAIN)]
	nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
	nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
	nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
	return split_nodes_image(split_nodes_link(nodes))

def extract_markdown_images(text: str) -> list[Tuple[str, str]]:
	return re.findall(r"!\[(.+?)\]\((.+?)\)", text)

def extract_markdown_links(text: str) -> list[Tuple[str, str]]:
	return re.findall(r"[^!]\[(.+?)\]\((.+?)\)", text)

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
	return __split_nodes_with_extractor__(old_nodes, extract_markdown_links, TextType.LINK)

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
	return __split_nodes_with_extractor__(old_nodes, extract_markdown_images, TextType.IMAGE, "!")

def __split_nodes_with_extractor__(old_nodes: list[TextNode], extractor: Callable[[str], list[Tuple[str, str]]], text_type: TextType, prefix="") -> list[TextNode]:
	out = []
	for node in old_nodes:
		if node.text_type == TextType.LINK or node.text_type == TextType.IMAGE or "[" not in node.text or "]" not in node.text or "(" not in node.text or ")" not in node.text:
			out.append(node)
		else:
			matches = extractor(node.text)
			if len(matches) == 0:
				out.append(node)
			else:
				text = node.text
				while len(matches) > 0:
					match = f"{prefix}[{matches[0][0]}]({matches[0][1]})"
					separated = text.split(match, 1)
					if not separated[0] == "":
						out.append(TextNode(separated[0], node.text_type))
					out.append(TextNode(matches[0][0], text_type, matches[0][1]))
					text = separated[1]
					matches = extractor(text)
				if not text == "":
					out.append(TextNode(text, node.text_type))

	return out

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
	out = []
	for node in old_nodes:
		if not node.text_type == TextType.PLAIN or delimiter not in node.text:
			out.append(node)
			continue
		separated = node.text.split(delimiter)
		if len(separated) == 1:
			out.append(node)
		else:
			num = len(separated)
			extra = False
			if num & 1 == 0:
				num -= 1
				extra = True
			toggle = False
			for i in range(0, num):
				if not toggle:
					if extra and i == num - 1:
						out.append(TextNode(separated[-2] + delimiter + separated[-1], TextType.PLAIN))
					else:
						out.append(TextNode(separated[i], TextType.PLAIN))
					toggle = True
				else:
					out.append(TextNode(separated[i], text_type))
					toggle = False
	
	return out
