import ast

from deepsource.exceptions.parsing import UnhandledBinOpException


def get_binop_identifier(node: ast.BinOp) -> str:
    match type(node.op):
        case ast.Add:
            return "+"
        case ast.Sub:
            return "-"
        case ast.Mult:
            return "*"
        case ast.Div:
            return "/"
        case ast.Mod:
            return "%"
        case ast.Pow:
            return "**"
        case ast.LShift:
            return "<<"
        case ast.RShift:
            return ">>"
        case ast.BitOr:
            return "|"
        case ast.BitXor:
            return "^"
        case ast.BitAnd:
            return "&"
        case ast.FloorDiv:
            return "//"
        case _:
            raise UnhandledBinOpException(f"{node.op}")
