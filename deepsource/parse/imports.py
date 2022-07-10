def parse_import(node, imports):
    for name in node.names:
        imports[name.name].append((node.lineno, '__module_import'))


def parse_import_from(node, imports):
    imports[node.module].append((node.lineno, tuple(name.name for name in node.names)))
