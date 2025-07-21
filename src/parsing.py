import re
from typing import Callable, Tuple
from textnode import TextNode, TextType

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
