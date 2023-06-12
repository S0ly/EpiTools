##
## EPITECH PROJECT, 20XX
## update_makefile.py
## File description:
## Update the Makefile with the new source and test files.
##

import os
import argparse

# Set global variables
MAKEFILE_PATH = './Makefile'
BANNED_FOLDERS = ['./tests', './bonus', './.ignore']
BANNED_FILES = ['main.c']

# Add custom exception for Makefile errors
class MakefileUpdateError(Exception):
    pass

def collect_c_files(dir_path, banned_folders, banned_files):
    """
    Collects all .c files from the specified directory and its subdirectories, excluding specified folders and files.
    """
    c_files = []
    for root, dirs, files in os.walk(dir_path):
        # Ignore files in banned folders
        if any(banned_folder in root for banned_folder in banned_folders):
            continue
        for file in files:
            # Only consider .c files that are not in the banned list
            if file.endswith('.c') and file not in banned_files:
                # Add the file path to the list, excluding the "./" at the start
                c_files.append(os.path.join(root, file)[2:])
    return c_files

def format_file_list(files):
    """
    Formats the list of files for the Makefile. Files with long paths are split into multiple lines.
    """
    formatted_files = []
    for i, file in enumerate(files):
        # Check if this is the first file
        is_first_file = i == 0

        # Split long file paths into multiple lines
        while len(file) > 70:  # 70 is chosen to accommodate the length of tab, space, and backslash
            cut_point = file.rfind('/', 0, 70)
            if cut_point == -1:  # If there's no slash within the first 73 characters
                cut_point = 70

            # Add only one tab for the first file
            formatted_files.append(("\t" if is_first_file else "\t\t") + file[:cut_point] + " \\")
            file = file[cut_point:]

            # Remaining parts are not the first file
            is_first_file = False

        # Add only one tab for the first file
        formatted_files.append(("\t" if is_first_file else "\t\t") + file + " \\")

    # Remove the backslash from the last file
    if formatted_files:
        formatted_files[-1] = formatted_files[-1][:-2]

    return '\n'.join(formatted_files)

def update_makefile(makefile_path, src, tests):
    """
    Updates the Makefile with the new source and test files.
    """
    if not os.path.exists(makefile_path):
        raise MakefileUpdateError("Makefile not found.")

    with open(makefile_path, 'r') as file:
        makefile_contents = file.read()

    # Identify the section to be replaced in the Makefile
    start_str = '## ? compilation file list\n############################################\n'
    end_str = '\n############################################'
    start_index = makefile_contents.find(start_str)
    end_index = makefile_contents.find(end_str, start_index + len(start_str))

    # Verify the start and end indexes
    if start_index == -1 or end_index == -1 or start_index >= end_index:
        raise MakefileUpdateError("The required part was not found in the Makefile.")

    # Add the length of the start string to the start index
    start_index += len(start_str)

    # Split the src and tests strings into lines to handle the first line separately
    src_lines = src.split('\n')
    tests_lines = tests.split('\n')

    # Create the new contents for the Makefile
    new_contents = makefile_contents[:start_index] + '\nSRC = ' + src_lines[0]

    for line in src_lines[1:]:
        new_contents += '\n' + line

    new_contents += '\n\nTESTS = ' + (tests_lines[0] if tests_lines else "")

    for line in tests_lines[1:]:
        new_contents += '\n' + line

    new_contents += makefile_contents[end_index:]

    # Write the new contents to the Makefile
    with open(makefile_path, 'w') as file:
        file.write(new_contents)

def main():
    # Collect all .c files, excluding those in the banned folders and files
    c_files = collect_c_files('.', BANNED_FOLDERS, BANNED_FILES)

    # Format the list of source and test files
    src_files = format_file_list([file for file in c_files if not file.startswith('./tests/') and file != './main.c'])
    test_files = format_file_list([file for file in c_files if file.startswith('./tests/')])

    # Update the Makefile
    update_makefile(MAKEFILE_PATH, src_files, test_files)
    print("Successfully updated the Makefile.")

if __name__ == '__main__':
    try:
        main()
    except MakefileUpdateError as e:
        print(f"Failed to update the Makefile. Error: {e}")
        exit(1)
