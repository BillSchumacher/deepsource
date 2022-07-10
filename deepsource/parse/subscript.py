import ast

from deepsource.parse.binop import get_binop_identifier

from deepsource.parse.constant import get_constant_identifier

from deepsource.exceptions.parsing import UnhandledSubscriptIdentifierException

from deepsource.parse.name import get_name_identifier
from deepsource.parse.slice import get_slice_identifier


def get_subscript_identifier(node: ast.Subscript) -> str:
    # print(node.slice, dir(node.slice))

    node_slice = node.slice
    match type(node_slice):
        case ast.Name:
            return get_name_identifier(node_slice)
        case ast.Constant:
            return get_constant_identifier(node_slice)
        case ast.Slice:
            return get_slice_identifier(node_slice)
        case ast.Subscript:
            return get_subscript_identifier(node_slice)
        case ast.BinOp:
            return get_binop_identifier(node_slice)
        case _:
            raise UnhandledSubscriptIdentifierException(f"{node_slice}")
