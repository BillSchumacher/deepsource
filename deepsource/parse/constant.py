import ast
from typing import Any


def get_constant_identifier(node: ast.Constant) -> Any:
    return node.value
