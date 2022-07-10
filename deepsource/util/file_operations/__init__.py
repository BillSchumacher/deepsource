import ast
import os

from deepsource.parse.syntax import parse_ast


def gather_file_paths(directory: str) -> list[str]:
    """
    Recursively gather all file paths in a directory.
    """
    file_paths = []
    for root, dirs, files in os.walk(directory):
        file_paths.extend(os.path.join(root, file) for file in files)
    return file_paths


def get_file_content(file_path: str) -> list[str]:
    """
    Read a requirements file and return a list of all the lines.
    """
    with open(file_path, 'r') as f:
        return f.readlines()


def parse_code(content: str):
    from collections import defaultdict

    imports = defaultdict(list)
    calls = defaultdict(list)
    assignments = defaultdict(list)
    try:
        syntax_tree = ast.parse(content)
    except SyntaxError:
        return imports, calls, assignments, True

    for item in syntax_tree.body:
        parse_ast(item, imports, calls, assignments)
    for key in imports:
        imports[key] = list(set(imports[key]))
    for key in calls:
        calls[key] = list(set(calls[key]))
    for key in assignments:
        assignments[key] = list(set(assignments[key]))

    return imports, calls, assignments, False
