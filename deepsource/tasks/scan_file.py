import itertools
from collections import defaultdict

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
        # https://datatracker.ietf.org/doc/html/rfc4648.html#section-12
        'base64',      # Hide's strings and more.
        'cgi',         # Can be used to execute arbitrary commands.
        'logging',     # Logging Configuration uses eval()
        'pickle',      # Pickle can be used to execute arbitrary code.
        'ast',         # AST can be used to execute arbitrary code.
        'importlib',   # Importlib can be used to execute arbitrary code.
        'shelve',      # Shelve can be used to execute arbitrary code, uses pickle.
        'shlex',       # Shlex can be used to execute arbitrary code/shell commands.
        'subprocess',  # Subprocess can be used to execute arbitrary code/shell commands.
        'sys',         # sys.modules/meta_path/paths might have some risks.
        # https://docs.python.org/3/library/tempfile.html#tempfile-mktemp-deprecated
        'tempfile',
        # The XML processing modules are not secure against maliciously constructed data.
        # An attacker can abuse XML features to carry out denial of service attacks,
        # access local files, generate network connections to other machines,
        # or circumvent firewalls.
        # https://docs.python.org/3/library/xml.html#xml-vulnerabilities
        'xml',
        # https://docs.python.org/3/library/zipfile.html#zipfile-resources-limitations
        'zipfile'       # zipfile can be exploited to consume disk, memory, and CPU.
    ]
    found_imports = defaultdict(list)
    for (key, value), _import in itertools.product(imports.items(), sus_imports):
        if not _import:
            continue
        if (key and _import in key) or (value and _import in value):
            found_imports[_import].extend(tuple(_imports[0] for _imports in value))

    for key in found_imports:
        found_imports[key] = list(set(found_imports[key]))

    for _import, lines in found_imports.items():
        print(f"Suspicious import: [{_import}] @ {file_path} line(s) {lines}.")
    # print(calls)
    # print(assignments)
    if syntax_error:
        print(f"Syntax Error reading file: {file_path}.")
        return False
    return True
