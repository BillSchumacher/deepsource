import itertools
from deepsource.celery_app import app
from deepsource.util.file_operations import parse_code, get_file_content


@app.task
def scan_file(file_path):
    """
    Scan a file for suspicious content.
    """
    print(f"Scanning {file_path}.")
    imports, calls, assignments, syntax_error = parse_code(
        '\n'.join(get_file_content(file_path))
    )
    # print(imports)
    sus_imports = [
        'pickle',
        'ast',
        'importlib',
        'shlex',
        'subprocess',
        'sys',
        'tempfile',
        'zipfile'
    ]
    for (key, value), _import in itertools.product(imports.items(), sus_imports):
        if not _import:
            continue
        if (key and _import in key) or (value and _import in value):
            print(f"Suspicious import: [{_import}] @ line(s) {[_imports[0] for _imports in value]}.")
    # print(calls)
    # print(assignments)
    if syntax_error:
        print(f"Syntax Error reading file: {file_path}.")
        return False
    return True
