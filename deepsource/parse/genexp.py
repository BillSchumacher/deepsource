import ast

from deepsource.parse.compare import get_compare_identifier

from deepsource.parse.ttuple import get_tuple_identifier

from deepsource.exceptions.parsing import UnhandledGenExpException

from deepsource.parse.name import get_name_identifier

from deepsource.parse.constant import get_constant_identifier


def get_genexp_identifier(node: ast.GeneratorExp) -> str:
    # print(node, dir(node))
    node_elt = node.elt
    match type(node_elt):
        case ast.Constant:
            return get_constant_identifier(node_elt)
        case ast.Name:
            return get_name_identifier(node_elt)
        case ast.Call:
            from deepsource.parse.call import get_call_identifier
            return get_call_identifier(node_elt)
        case ast.Tuple:
            return get_tuple_identifier(node_elt)
        case ast.Compare:
            return get_compare_identifier(node_elt)
        case _:
            raise UnhandledGenExpException(f"{node_elt}")
