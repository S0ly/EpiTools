import sys
import re
from collections import defaultdict

class ColoredText:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    END = '\033[0m'

error_dict = {
    'C-O1': 'Avoid compiled, temporary, or unnecessary files in the repository.',
    'C-O2': 'Sources in a C program should have .c or .h extensions.',
    'C-O3': 'Group related functions in the same file. Subdivide if there are more than 5 functions.',
    'C-O4': 'File names should define the logical entity they represent, use snake_case.',
    'C-G1': 'C files and Makefiles must start with the standard school header.',
    'C-G2': 'Separate function implementations with a single empty line.',
    'C-G3': 'Indent preprocessor directives according to the level of indirection.',
    'C-G4': 'Avoid global variables. Use only global constants.',
    'C-G5': 'Include directive should only include .h files.',
    'C-G6': 'Use UNIX style line endings (\n).',
    'C-G7': 'No trailing spaces at the end of a line.',
    'C-G8': 'No leading empty lines. Maximum of 1 trailing empty line.',
    'C-G9': 'Define non-trivial constant values as global constants or macros.',
    'C-F1': 'A function should only do one thing and respect the single-responsibility principle.',
    'C-F2': 'Function name should define its task and contain a verb.',
    'C-F3': 'Line length must not exceed 80 columns.',
    'C-F4': 'Function body must not exceed 20 lines.',
    'C-F5': 'A function must not have more than 4 parameters.',
    'C-F6': 'Nesting level in a function should not exceed 4, excluding the if, switch and for statements in a case of switch.',
    'C-V1': 'Variables must be declared at the beginning of a function, following the order of their type’s size.',
    'C-V2': 'A variable name should define the data it represents, use snake_case.',
    'C-V3': 'Each variable declaration must be at a new line.',
    'C-V4': 'Variables with a scope greater than 5 lines must be initialized upon declaration.',
    'C-C1': 'Use braces even for single-statement blocks.',
    'C-C2': 'No more than one assignment in a single statement.',
    'C-C3': 'No more than 5 function calls in a single statement.',
    'C-C4': 'No unnecessary parentheses around conditions or return values.',
    'C-L3': 'Use single space as separator. No tabs. Correct space usage around operators and structures.',
    'C-L4': 'Opening brackets at line end. Closing brackets alone on line, except for else/else if, enums, structures.',
    'C-L5': 'Declare variables at start of function. One variable per line.',
    'C-L6': 'Line break after variable declarations. No other line breaks in function scope.',
    'C-V1': 'Use English, snake_case for identifiers. Type names end with _t. UPPER_SNAKE_CASE for macros and globals.',
    'C-V2': 'Group variables in a structure only if they form a coherent entity. Keep structures small.',
    'C-V3': 'Attach pointer symbol (*) to the associated variable, no spaces.',
    'C-C1': 'Conditional block must not contain more than 3 branches. Avoid nested branches with depth 3 or more.',
    'C-C2': 'Ternary operators must be simple and readable. No nested or chained ternary operators.',
    'C-C3': 'Using the goto keyword is forbidden.',
    'C-H1': 'Headers contain only function prototypes, type declarations, global variable/constant declarations, macros, static inline functions.',
    'C-H2': 'Headers must be protected from double inclusion.',
    'C-H3': 'Macros must match only one statement, and fit on a single line.',
    'C-A1': 'Mark pointed data that should not be modified as constant (const).',
    'C-A2': 'Use the most accurate types possible according to the data use.',
    'C-A3': 'Files must end with a line break.',
    'C-A4': 'Mark global variables and functions not used outside the compilation unit as static.',
    'C-A5': 'Use volatile keyword only when interacting with hardware or when using variables that can change in an interrupt handler.'
}


def parse_error(line):
    match = re.search(r'(\./.*):(\d+): (MAJOR|MINOR|INFO):(.*)', line)
    if match:
        return match.groups()
    else:
        return None

def count_errors(file):
    error_counts = defaultdict(int)
    error_details = []

    for line in file:
        parsed_error = parse_error(line)
        if parsed_error:
            file_path, line_number, error_type, error_code = parsed_error
            error_counts[error_type] += 1
            error_details.append({
                'file_path': file_path,
                'line_number': line_number,
                'error_type': error_type,
                'error_code': error_code.strip(),
                'solution': error_dict.get(error_code.strip(), 'No solution found.')
            })

    return error_counts, error_details

def colorize_error_type(error_type):
    if error_type == 'MAJOR':
        return f'{ColoredText.RED}{error_type}{ColoredText.END}'
    elif error_type == 'MINOR':
        return f'{ColoredText.YELLOW}{error_type}{ColoredText.END}'
    elif error_type == 'INFO':
        return f'{ColoredText.GREEN}{error_type}{ColoredText.END}'

def print_errors(error_counts, error_details):
    print(f'Total: {sum(error_counts.values())}')
    print(f'Major: {error_counts["MAJOR"]}')
    print(f'Minor: {error_counts["MINOR"]}')
    print(f'Info: {error_counts["INFO"]}\n')

    for error in error_details:
        print(f'File: {error["file_path"]}:{error["line_number"]}')
        print(f'Type: {colorize_error_type(error["error_type"])}')
        print(f'Code: {error["error_code"]}')
        print(f'Solution: {error["solution"]}\n')

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <filename>")
        sys.exit(1)

    file_path = sys.argv[1]
    with open(file_path, 'r') as file:
        error_counts, error_details = count_errors(file)
        print_errors(error_counts, error_details)

if __name__ == '__main__':
    main()
