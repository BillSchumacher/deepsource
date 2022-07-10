import ast

from deepsource.parse.llist import get_list_identifier

from deepsource.parse.aawait import get_await_identifier
from deepsource.parse.binop import get_binop_identifier
from deepsource.parse.boolop import get_boolop_identifier
from deepsource.parse.call import get_call_identifier

from deepsource.exceptions.parsing import UnhandledAssignTargetException, \
    UnhandledAssignException
from deepsource.parse.attribute import get_attribute_identifier
from deepsource.parse.constant import get_constant_identifier
from deepsource.parse.ddict import get_dict_identifier
from deepsource.parse.joined_str import get_joined_str_identifier
from deepsource.parse.listcomp import get_listcomp_identifier
from deepsource.parse.name import get_name_identifier
from deepsource.parse.subscript import get_subscript_identifier
from deepsource.parse.ttuple import get_tuple_identifier


def get_assign_value(node):
    node_value = node.value
    match type(node_value):
        case ast.Constant:
            value = get_constant_identifier(node_value)
        case ast.Name:
            value = get_name_identifier(node_value)
        case ast.List:
            value = get_list_identifier(node_value)
        case ast.ListComp:
            value = get_listcomp_identifier(node_value)
        case ast.Call:
            value = get_call_identifier(node_value)
        case ast.Await:
            value = get_await_identifier(node_value)
        case ast.Subscript:
            value = get_subscript_identifier(node_value)
        case ast.Attribute:
            value = get_attribute_identifier(node_value)
        case ast.Dict:
            value = get_dict_identifier(node_value)
        case ast.BinOp:
            value = get_binop_identifier(node_value)
        case ast.BoolOp:
            value = get_boolop_identifier(node_value)
        case ast.Tuple:
            value = get_tuple_identifier(node_value)
        case ast.IfExp:
            # TODO: has a body attr, maybe check that too. skipping for now
            value = 'ifexp'
            # print(node_value, dir(node_value))
            # raise UnhandledAssignException(f"{node.value}")
        case ast.JoinedStr:
            value = get_joined_str_identifier(node_value)
        case _:
            raise UnhandledAssignException(f"{node.value}")
    return value


def parse_assign_target(node, target, value, assignments):
    target_type = type(target)
    match target_type:
        case ast.Name:
            target_value = get_name_identifier(target)
        case ast.Attribute:
            target_value = get_attribute_identifier(target)
        case ast.Assign:
            target_value = get_assign_value(target)
        case ast.Subscript:
            target_value = get_subscript_identifier(target)
        case ast.Tuple:
            values = []
            for elt in target.elts:
                match type(elt):
                    case ast.Constant:
                        elt_value = get_constant_identifier(elt)
                    case ast.Name:
                        elt_value = get_name_identifier(elt)
                    case _:
                        raise UnhandledAssignException(f"{elt}")
                values.append(elt_value)
            target_value = tuple(values)
        case _:
            raise UnhandledAssignTargetException(f"{node}, {target_type}")
    assignments[value].append((node.lineno, target_value))


def parse_assign(node, assignments):
    # print('assign', node.targets, dir(node))
    # print(node.value, node.type_comment, dir(node.value))
    value = get_assign_value(node)

    for target in node.targets:
        parse_assign_target(node, target, value, assignments)
