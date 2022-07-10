import ast


def get_attribute_identifier(node: ast.Attribute) -> str:
    return node.attr
