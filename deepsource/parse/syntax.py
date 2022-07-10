import ast

from deepsource.parse.assign import parse_assign
from deepsource.parse.call import parse_call
from deepsource.parse.imports import parse_import_from, parse_import


def parse_ast(node, imports, calls, assignments):
    match type(node):
        case ast.FunctionDef:
            for function_node in node.body:
                parse_ast(function_node, imports, calls, assignments)
        case ast.Assign:
            parse_assign(node, assignments)
        case ast.ImportFrom:
            parse_import_from(node, imports)
        case ast.Import:
            parse_import(node, imports)
        case ast.Call:
            parse_call(node, calls)
        case _:
            # print(node, dir(node))
            for child in ast.iter_child_nodes(node):
                parse_ast(child, imports, calls, assignments)
