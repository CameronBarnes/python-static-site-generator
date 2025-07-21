class HTMLNode:
	def __init__(self, tag=None, value=None, children=None, props=None) -> None:
		self.tag = tag
		self.value = value
		self.children = children
		self.props = props
	
	def to_html(self) -> str:
		raise NotImplementedError
	
	def props_to_html(self) -> str:
		out = []
		if self.props is None:
			return ""
		for key, value in self.props.items():
			out.append(f"{key}=\"{value}\"")
		return " ".join(out)

	def __repr__(self) -> str:
		return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class ParentNode(HTMLNode):
	def __init__(self, tag, children, props=None) -> None:
		super().__init__(tag, None, children, props)
	
	def to_html(self) -> str:
		if self.tag is None:
			raise ValueError("tag is not allowed to be none")
		elif self.children is None:
			raise ValueError("ParentNodes must have children, children is None")
		elif self.props is None:
			return f'<{self.tag}>{"".join(map(lambda child: child.to_html(), self.children))}</{self.tag}>'
		else:
			return f'<{self.tag} {self.props_to_html()}>{"".join(map(lambda child: child.to_html(), self.children))}</{self.tag}>'


class LeafNode(HTMLNode):
	def __init__(self, tag, value, props=None) -> None:
		super().__init__(tag, value, None, props)
	
	def to_html(self) -> str:
		if self.value is None:
			raise ValueError("value is not allowed to be None in a LeafNode")
		if self.tag is None:
			return self.value
		elif self.props is not None:
			return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"
		else:
			return f"<{self.tag}>{self.value}</{self.tag}>"
