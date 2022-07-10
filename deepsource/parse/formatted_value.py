import ast


def get_formatted_value_identifier(node: ast.FormattedValue) -> str:
    # print(node.value, dir(node.value))
    return node.value
