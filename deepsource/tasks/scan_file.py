import itertools
from collections import defaultdict

from deepsource.celery_app import app
from deepsource.util.file_operations import get_file_content, parse_code


@app.task
def scan_file(file_path):
    """
    Scan a file for suspicious content.
    """
    print(f"Scanning {file_path}.")
    imports, calls, assignments, syntax_error = parse_code(
        "\n".join(get_file_content(file_path))
    )
    # print(imports)
    sus_imports = [
        # https://datatracker.ietf.org/doc/html/rfc4648.html#section-12
        "base64",  # Hide strings and more.
        "cgi",  # Can be used to execute arbitrary commands.
        "logging",  # Logging Configuration uses eval()
        "pickle",  # Pickle can be used to execute arbitrary code.
        "ast",  # AST can be used to execute arbitrary code.
        "importlib",  # Importlib can be used to execute arbitrary code.
        "shelve",  # Shelve can be used to execute arbitrary code, uses pickle.
        "shlex",  # Shlex can be used to execute arbitrary code/shell commands.
        "subprocess",  # Subprocess can be used to execute arbitrary
        # code/shell commands.
        "sys",  # sys.modules/meta_path/paths might have some risks.
        # https://docs.python.org/3/library/tempfile.html#tempfile-mktemp-deprecated
        "tempfile",
        # The XML processing modules are not secure against
        # maliciously constructed data.
        # An attacker can abuse XML features to carry out denial of service attacks,
        # access local files, generate network connections to other machines,
        # or circumvent firewalls.
        # https://docs.python.org/3/library/xml.html#xml-vulnerabilities
        "xml",
        # https://docs.python.org/3/library/zipfile.html#zipfile-resources-limitations
        "zipfile",  # zipfile can be exploited to consume disk, memory, and CPU.
        "py_compile",
        "codeop",
        "logging.config"
    ]
    found_import_lines = defaultdict(list)
    found_import_names = defaultdict(list)
    for (key, value), _import in itertools.product(imports.items(), sus_imports):
        if not _import:
            continue
        if (key and _import in key) or (value and _import in value):
            found_import_lines[_import].extend(tuple(_imports[0] for _imports in value))
            found_import_names[_import].extend(tuple(_imports[1:] for _imports in value))

    for key in found_import_lines:
        found_import_lines[key] = list(set(found_import_lines[key]))
    for key in found_import_names:
        found_import_names[key] = list(set(found_import_names[key]))


    for _import, lines in found_import_lines.items():
        print(f"Suspicious import: [{_import}] @ {file_path} line(s) {lines}.")

    # TODO: correlate the module to the call.
    sus_call_names = [
        'eval',
        'exec',
        'execfile',
        'compile',
        'system',
        'popen',
        'loads',
        'dumps',
        'b64decode',
        'b64encode',
        'pickle.loads',
        'pickle.dumps',
        'pickle.load',
        'pickle.dump',
    ]

    found_calls = defaultdict(list)
    for (key, value), _call in itertools.product(calls.items(), sus_call_names):
        if not _call:
            continue
        if (key and _call in key) or (value and _call in value):
            lines = tuple(_calls[0] for _calls in value)
            found_calls[_call].extend(lines)
            for _import, _names in found_import_names.items():
                # print(_call, _import, _names)
                if _call in _names:
                    # this doesn't work.
                    print(f"Extremely Suspicious call: [{_import}.{_call}] @ {file_path} line(s) {lines}.")
                    break

    for key in found_calls:
        found_calls[key] = list(set(found_calls[key]))

    for _call, lines in found_calls.items():
        print(f"Suspicious call: [{_call}] @ {file_path} line(s) {lines}.")
    # print(calls)
    # print(assignments)
    if syntax_error:
        print(f"Syntax Error reading file: {file_path}.")
        return False
    return True
