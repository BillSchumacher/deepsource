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
    # print(calls)
    # print(assignments)
    if syntax_error:
        print(f"Syntax Error reading file: {file_path}.")
        return False
    return True
