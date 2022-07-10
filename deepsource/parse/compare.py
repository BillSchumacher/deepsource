import ast

from deepsource.parse.constant import get_constant_identifier

from deepsource.parse.name import get_name_identifier


def get_compare_identifier(node: ast.Compare):
    # print(node, dir(node))
    # print(type(node.left), dir(node.left))
    # print(node.ops, dir(node.ops))
    left_type = type(node.left)
    match left_type:
        case ast.Name:
            left = get_name_identifier(node.left)
        case ast.Constant:
            left = get_constant_identifier(node.left)
        case _:
            raise NotImplementedError(left_type)
    ops = []
    for op in node.ops:
        op_type = type(op)
        match op_type:
            case ast.Eq:
                op = "=="
            case ast.NotEq:
                op = "!="
            case ast.Lt:
                op = "<"
            case ast.LtE:
                op = "<="
            case ast.Gt:
                op = ">"
            case ast.GtE:
                op = ">="
            case ast.Is:
                op = "is"
            case ast.IsNot:
                op = "is not"
            case ast.In:
                op = "in"
            case ast.NotIn:
                op = "not in"
            case _:
                raise NotImplementedError(op_type)
        ops.append(op)
    return left, tuple(ops)
