import ast

from deepsource.exceptions.parsing import UnhandledListCompException
from deepsource.parse.call import get_call_identifier

from deepsource.parse.name import get_name_identifier

from deepsource.parse.constant import get_constant_identifier


def get_listcomp_identifier(node: ast.ListComp) -> str:
    # values = []
    # print(dir(node_value))
    # for elt in node_value.elts:
    elt = node.elt
    match type(elt):
        case ast.Constant:
            value = get_constant_identifier(elt)
        case ast.Name:
            value = get_name_identifier(elt)
        case ast.Call:
            value = get_call_identifier(elt)
        case _:
            raise UnhandledListCompException(f"{elt}")
    return value
