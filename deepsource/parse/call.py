import ast

from deepsource.parse.ttuple import get_tuple_identifier
from deepsource.parse.joined_str import get_joined_str_identifier
from deepsource.parse.ddict import get_dict_identifier
from deepsource.parse.binop import get_binop_identifier
from deepsource.parse.genexp import get_genexp_identifier
from deepsource.parse.llist import get_list_identifier
from deepsource.parse.subscript import get_subscript_identifier

from deepsource.exceptions.parsing import UnhandledCallIdentifierException,\
    UnhandledCallArgException
from deepsource.parse.attribute import get_attribute_identifier
from deepsource.parse.constant import get_constant_identifier
from deepsource.parse.name import get_name_identifier


def get_call_identifier(node: ast.Call) -> str:
    node_value = node.func
    match type(node_value):
        case ast.Name:
            name = get_name_identifier(node_value)
        case ast.Attribute:
            name = get_attribute_identifier(node_value)
        case _:
            raise UnhandledCallIdentifierException(f"{node.func}")
    return name


def parse_args(node):
    args = []
    for arg in node.args:
        match type(arg):
            case ast.Name:
                value = get_name_identifier(arg)
            case ast.Attribute:
                value = get_attribute_identifier(arg)
            case ast.Constant:
                value = get_constant_identifier(arg)
            case ast.Call:
                value = get_call_identifier(arg)
            case ast.Lambda:
                value = 'lambda'
            case ast.Subscript:
                value = get_subscript_identifier(arg)
            case ast.BinOp:
                value = get_binop_identifier(arg)
            case ast.GeneratorExp:
                value = get_genexp_identifier(arg)
            case ast.List:
                value = get_list_identifier(arg)
            case ast.Dict:
                value = get_dict_identifier(arg)
            case ast.JoinedStr:
                value = get_joined_str_identifier(arg)
            case ast.Compare:
                value = "compare"  # get_compare_identifier(arg)
            case ast.Starred:
                value = "starred"
                # TODO: handle starred
            case ast.IfExp:
                value = "ifexp"
            case ast.UnaryOp:
                value = "unaryop"
            case ast.Tuple:
                value = get_tuple_identifier(arg)
            case _:
                raise UnhandledCallArgException(f"{arg}")
        args.append(value)
    return args


def parse_call(node, calls):
    args = (node.lineno, tuple(parse_args(node)))
    name = get_call_identifier(node)
    calls[name].append(args)
    return name, args
