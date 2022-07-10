import ast


def get_name_identifier(node: ast.Name) -> str:
    return node.id
