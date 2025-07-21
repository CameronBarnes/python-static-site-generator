from enum import Enum

from htmlnode import LeafNode

class TextType(Enum):
	PLAIN = "plain",
	BOLD = "bold",
	ITALIC = "italic",
	CODE = "code",
	LINK = "link",
	IMAGE = "image"

class TextNode:
	def __init__(self, text: str, text_type: TextType, url=None) -> None:
		self.text = text
		self.text_type = text_type
		self.url = url
	
	def __eq__(self, value: object, /) -> bool:
		return isinstance(value, TextNode) and self.text == value.text and self.text_type == value.text_type and self.url == value.url
	
	def __repr__(self) -> str:
		return f"TextNode({self.text}, {self.text_type}, {self.url})"
	
	def to_html_node(self) -> LeafNode:
		match (self.text_type):
			case TextType.PLAIN:
				return LeafNode(None, self.text)
			case TextType.BOLD:
				return LeafNode("b", self.text)
			case TextType.ITALIC:
				return LeafNode("i", self.text)
			case TextType.CODE:
				return LeafNode("code", self.text)
			case TextType.LINK:
				if self.url is None:
					raise ValueError("url may not be None for TextType.LINK")
				return LeafNode("a", self.text, {"href": self.url})
			case TextType.IMAGE:
				if self.url is None:
					raise ValueError("url may not be None for TextType.IMAGE")
				return LeafNode("img", "", {"src": self.url, "alt": self.text})
			case None:
				raise ValueError("TextType may not be None")
			case _:
				raise ValueError(f"Invalid or unimplemented text_type: {self.text_type}")
