import unittest

from markdown_converter import markdown_to_html_node

class TestMarkdownConverter(unittest.TestCase):
	def test_paragraphs(self):
		md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

		node = markdown_to_html_node(md)
		html = node.to_html()
		expected = "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
		# print(f"\nOutput: {html}")
		# print(f"Expect: {expected}")
		self.assertEqual(
			html,
			expected,
		)

	def test_codeblock(self):
		md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

		node = markdown_to_html_node(md)
		html = node.to_html()
		expected = "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>"
		# print(f"\nOutput: {html}")
		# print(f"Expect: {expected}")
		self.assertEqual(
			html,
			expected
		)
