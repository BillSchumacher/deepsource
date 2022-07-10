import ast

from deepsource.parse.binop import get_binop_identifier

from deepsource.exceptions.parsing import UnhandledListException

from deepsource.parse.attribute import get_attribute_identifier


from deepsource.parse.name import get_name_identifier

from deepsource.parse.constant import get_constant_identifier


def get_list_identifier(node: ast.List) -> str:
    values = []
    for elt in node.elts:
        match type(elt):
            case ast.Constant:
                elt_value = get_constant_identifier(elt)
            case ast.Name:
                elt_value = get_name_identifier(elt)
            case ast.Call:
                from deepsource.parse.call import get_call_identifier
                elt_value = get_call_identifier(elt)
            case ast.Dict:
                from deepsource.parse.ddict import get_dict_identifier
                elt_value = get_dict_identifier(elt)
            case ast.Attribute:
                elt_value = get_attribute_identifier(elt)
            case ast.BinOp:
                elt_value = get_binop_identifier(elt)
            case _:
                raise UnhandledListException(f"{elt}")
        values.append(elt_value)
    value = tuple(values)
    return value
