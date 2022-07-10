import ast
from typing import Any

from deepsource.parse.constant import get_constant_identifier

from deepsource.parse.name import get_name_identifier


def get_dict_identifier(node: ast.Dict) -> Any:
    # print(node, dir(node))
    keys = []
    for key in node.keys:
        match type(key):
            case ast.Name:
                value = get_name_identifier(key)
            case ast.Constant:
                value = get_constant_identifier(key)
            case _:
                print(key, dir(key))
                raise NotImplementedError()
        keys.append(value)

    # for value in node.values:
    #     print(value, dir(value))
    return tuple(keys)
