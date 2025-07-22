import shutil

def setup_public_dir():
	print("Deleting existing public folder...")
	shutil.rmtree("./public")
	print("Done...")
	print("Copying static files...")
	shutil.copytree("./static", "./public")
