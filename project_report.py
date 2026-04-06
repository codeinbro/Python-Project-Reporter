import os
from datetime import datetime

# Project folder and name of this script itself
project_folder = os.path.dirname(os.path.abspath(__file__))
current_script = os.path.basename(__file__)

# Docs folder
docs_folder = os.path.join(project_folder, "docs")
os.makedirs(docs_folder, exist_ok=True)

# Report output file
output_file = os.path.join(docs_folder, "project_report_output.txt")

# Mandatory opening text at the top
opening_text = (
    "I created a Python application on Android using Pydroid3\n"
    f"Report date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
)
# Additional text after newline
additional_text = "Here is the list of project files\n\n"

# Closing text
closing_text = "Now provide suggestions or upgrades\n"

# Function to get Project Tree
def get_project_tree(folder, prefix="", exclude_folders=None, exclude_files=None, include_ext=None):
    if exclude_folders is None: exclude_folders = ["__pycache__"]
    if exclude_files is None: exclude_files = []
    tree_lines = []

    items = sorted(os.listdir(folder))
    items = [
        i for i in items
        if i not in exclude_folders
        and i not in exclude_files
        and not i.endswith(".pyc")
        and not i.startswith(".")
        and (include_ext is None or os.path.splitext(i)[1] in include_ext or os.path.isdir(os.path.join(folder, i)))
    ]

    for index, item in enumerate(items):
        path = os.path.join(folder, item)
        pointer = '└─ ' if index == len(items)-1 else '├─ '
        line = f"{prefix}{pointer}{item}"
        tree_lines.append(line)
        if os.path.isdir(path):
            new_prefix = prefix + ("    " if pointer == '└─ ' else "│   ")
            tree_lines.extend(get_project_tree(
                path,
                prefix=new_prefix,
                exclude_folders=exclude_folders,
                exclude_files=exclude_files,
                include_ext=include_ext
            ))
    return tree_lines

# Files to skip: this generator, output file, project_tree.py
skip_files = [current_script, "project_tree.py", os.path.basename(output_file)]

# Get Project Tree (only folders and .py files)
tree_lines = get_project_tree(project_folder, exclude_files=skip_files, include_ext={'.py'})

# Write project_report_output.txt
with open(output_file, 'w', encoding='utf-8') as out_file:
    # 1️⃣ Write opening text
    out_file.write(opening_text)
    out_file.write(additional_text)

    # 2️⃣ Write Project Tree
    out_file.write("Project Tree:\n")
    for line in tree_lines:
        out_file.write(line + "\n")
    out_file.write("\n")

    # 3️⃣ Write contents of all .py files in the project with numbering
    file_counter = 1
    for item in sorted(os.listdir(project_folder)):
        if item in skip_files:
            continue
        item_path = os.path.join(project_folder, item)
        if os.path.isfile(item_path) and item.endswith(".py"):
            out_file.write(f"\n===== File {file_counter}: {item} =====\n")
            with open(item_path, 'r', encoding='utf-8', errors='ignore') as f:
                out_file.write(f.read())
            out_file.write("\n\n\n")  # 3 empty lines after file content
            file_counter += 1

    # 4️⃣ Write closing text at the bottom
    out_file.write(closing_text)

print(f"Successfully written to: {output_file}")