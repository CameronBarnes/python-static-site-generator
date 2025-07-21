import re
from typing import Tuple
from textnode import TextNode, TextType

def extract_markdown_images(text: str) -> list[Tuple[str, str]]:
	return re.findall(r"!\[(.+?)\]\((.+?)\)", text)

def extract_markdown_links(text: str) -> list[Tuple[str, str]]:
	return re.findall(r"[^!]\[(.+?)\]\((.+?)\)", text)

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
