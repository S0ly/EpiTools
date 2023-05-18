import os
import re
from collections import defaultdict
from termcolor import colored

# These directories are ignored
IGNORED_DIRS = ['bonus', 'test']

# Keywords to exclude
EXCLUDED_KEYWORDS = ['if', 'while', 'for', 'switch', 'else', 'return']

def get_c_files(path='.'):
    """Get all .c files in a directory."""
    c_files = []
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for file in files:
            if file.endswith('.c'):
                c_files.append(os.path.join(root, file))
    return c_files

def get_function_declarations(file_path):
    """Get all function declarations in a .c file."""
    with open(file_path, 'r') as file:
        data = file.read()

    functions = re.findall(r'\b(\w+)\s*\([^)]*\)\s*\{', data)
    functions = [func for func in functions if func not in EXCLUDED_KEYWORDS]
    return functions

def get_function_calls(file_path):
    """Get all function calls in a .c file."""
    function_calls = defaultdict(list)
    with open(file_path, 'r') as file:
        lines = file.readlines()

    for i, line in enumerate(lines, start=1):
        calls = re.findall(r'\b(\w+)\s*\([^)]*\);', line)
        for call in calls:
            if call not in EXCLUDED_KEYWORDS:
                function_calls[call].append((file_path, i))

    return function_calls


def analyse_c_files(path='.'):
    """Analyse all .c files in a directory."""
    c_files = get_c_files(path)
    internal_functions = []
    function_calls = defaultdict(list)
    for file in c_files:
        internal_functions += get_function_declarations(file)
        calls = get_function_calls(file)
        for call, locations in calls.items():
            function_calls[call].extend(locations)

    internal_calls = defaultdict(list)
    external_calls = defaultdict(list)
    for call, locations in function_calls.items():
        if call in internal_functions:
            internal_calls[call] = locations
        else:
            external_calls[call] = locations

    print("\nFunction call locations:")
    print(colored("\nInternal function calls:", 'blue'))
    for call, locations in internal_calls.items():
        print(colored(f"\n{call}:", 'blue'))
        for location in locations:
            print(f"  {location[0]}: line {location[1]}")

    print(colored("\nExternal function calls:", 'yellow'))
    for call, locations in external_calls.items():
        print(colored(f"\n{call}:", 'yellow'))
        for location in locations:
            print(f"  {location[0]}: line {location[1]}")

    print("\nSummary:")
    print(f"Total function calls: {sum(len(locations) for locations in function_calls.values())}")
    print(colored(f"Internal function calls: {sum(len(locations) for locations in internal_calls.values())}", 'blue'))
    print(colored(f"External function calls: {sum(len(locations) for locations in external_calls.values())}", 'yellow'))

if __name__ == "__main__":
    analyse_c_files()
