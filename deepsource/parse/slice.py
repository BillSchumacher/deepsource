import ast


def get_slice_identifier(node: ast.Slice) -> str:
    return f'slice-{node.lower}:{node.upper}:{node.step}'
