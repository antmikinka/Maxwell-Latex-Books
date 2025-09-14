import re
import os
import argparse # Import the argparse module

def fix_equations_in_file(filepath):
	"""
	Reads a markdown file, finds and fixes equations, and saves a new version.
	"""
	print(f"Processing file: {filepath}...")
	try:
		with open(filepath, 'r', encoding='utf-8') as f:
			content = f.read()
	except FileNotFoundError:
		print(f"Error: The file '{filepath}' was not found.")
		return
	except Exception as e:
		print(f"An error occurred while reading the file: {e}")
		return

	# This regular expression identifies lines that are likely equations.
	# It looks for lines containing common mathematical symbols or starting with typical equation structures.
	equation_pattern = re.compile(r"^(?![{}>#\s`])(?:[a-zA-Z0-9'’]+ =.*|.*\d.*[+\-*/=^].*)$", re.MULTILINE)

	def replace_with_latex(match):
		equation_text = match.group(0).strip()
		# Do not re-format lines that already look like LaTeX
		if equation_text.startswith('$') or equation_text.startswith('\\['):
			return match.group(0)
		# Wrap the found equation in $$ ... $$ delimiters for display mode
		return f"\n$$ {equation_text} $$\n"

	# This performs the replacement on the entire file content
	fixed_content = equation_pattern.sub(replace_with_latex, content)

	# Save the corrected content to a new file with "_fixed" appended
	directory, filename = os.path.split(filepath)
	name, ext = os.path.splitext(filename)
	new_filepath = os.path.join(directory, f"{name}_fixed{ext}")

	with open(new_filepath, 'w', encoding='utf-8') as f:
		f.write(fixed_content)

	print(f"Successfully processed. Corrected file saved as: {new_filepath}\n")


#python fix_equations.py "C:\Users\YourUser\Documents\Maxwell\15773-A Treatise On Electricity And Magnetism Vol-i.md"

# --- Main execution part ---
if __name__ == "__main__":
	# 1. Set up the argument parser
	parser = argparse.ArgumentParser(description="Fix LaTeX equation formatting in markdown files.")
	
	# 2. Add an argument for the file paths
	# 'nargs='+'' means it can accept one or more file paths.
	parser.add_argument('files', nargs='+', help="The path(s) to the markdown file(s) to process.")
	
	# 3. Parse the arguments provided from the command line
	args = parser.parse_args()

	# 4. Loop through the list of files and process each one
	for file_path in args.files:
		fix_equations_in_file(file_path)