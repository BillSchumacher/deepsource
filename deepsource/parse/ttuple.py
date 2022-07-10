import ast

from deepsource.parse.subscript import get_subscript_identifier

from deepsource.parse.binop import get_binop_identifier

from deepsource.parse.attribute import get_attribute_identifier

from deepsource.exceptions.parsing import UnhandledTupleException
from deepsource.parse.name import get_name_identifier

from deepsource.parse.constant import get_constant_identifier


def get_tuple_identifier(node: ast.Tuple):
    values = []
    elts = node.elts
    for elt in elts:
        match type(elt):
            case ast.Call:
                from deepsource.parse.call import get_call_identifier
                elt_value = get_call_identifier(elt)
            case ast.Attribute:
                elt_value = get_attribute_identifier(elt)
            case ast.Constant:
                elt_value = get_constant_identifier(elt)
            case ast.Name:
                elt_value = get_name_identifier(elt)
            case ast.Tuple:
                elt_value = get_tuple_identifier(elt)
            case ast.BinOp:
                elt_value = get_binop_identifier(elt)
            case ast.Subscript:
                elt_value = get_subscript_identifier(elt)
            case _:
                raise UnhandledTupleException(f"{elt}")
        values.append(elt_value)
    value = tuple(values)
    return value
