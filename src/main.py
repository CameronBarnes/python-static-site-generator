from fs_tools import setup_public_dir
from markdown_converter import extract_title, markdown_to_html_node

import os
import sys

def main():
	basepath = "/"
	if len(sys.argv) >= 2:
		basepath = sys.argv[1]
	setup_public_dir("./docs")
	generate_pages_recursive("./content", "./template.html", "./docs", basepath)

def generate_pages_recursive(from_dir: str, template_path: str, dest_dir: str, basepath: str):
	if not os.path.exists(from_dir) or not os.path.isdir(from_dir):
		raise ValueError(f"invalid from_dir: {from_dir}")
	if os.path.exists(dest_dir) and not os.path.isdir(dest_dir):
		raise ValueError(f"invalid dest_dir: {dest_dir}")
	if not os.path.exists(template_path) or not os.path.isfile(template_path):
		raise ValueError(f"invalid template_path: {template_path}")
	for entry in os.listdir(from_dir):
		from_path = os.path.join(from_dir, entry)
		dest_path = os.path.join(dest_dir, entry)
		if os.path.isdir(from_path):
			generate_pages_recursive(from_path, template_path, dest_path, basepath)
		else:
			generate_page(from_path, template_path, dest_path.replace("md", "html"), basepath)

def generate_page(from_path: str, template_path: str, dest_path: str, basepath):
	print(f"Generating page from {from_path} to {dest_path} using {template_path}")
	with open(from_path) as f: from_content = f.read()
	with open(template_path) as f: template_content = f.read()
	title = extract_title(from_content)
	content = markdown_to_html_node(from_content).to_html()
	out_content = template_content.replace("{{ Title }}", title).replace("{{ Content }}", content).replace("href=\"/", f"href=\"{basepath}").replace("src=\"/", f"src=\"{basepath}")
	dest_path = os.path.abspath(dest_path)
	os.makedirs(os.path.dirname(dest_path), exist_ok=True)
	with open(dest_path, "w") as f: f.write(out_content)

if __name__ == "__main__":
	main()
