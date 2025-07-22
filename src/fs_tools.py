import shutil, os

def setup_public_dir(dest_path: str):
	if os.path.exists(dest_path):
		print(f"Deleting existing {dest_path} folder...")
		shutil.rmtree(dest_path)
		print("Done...")
	print("Copying static files...")
	shutil.copytree("./static", dest_path)
