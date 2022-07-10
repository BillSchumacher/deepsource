import ast

from deepsource.exceptions.parsing import UnhandledBinOpException


def get_boolop_identifier(node: ast.BoolOp) -> str:
    match type(node.op):
        case ast.And:
            op = 'and'
        case ast.Or:
            op = 'or'
        case _:
            raise UnhandledBinOpException(f"{node.op}")
    return op
