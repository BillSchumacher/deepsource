import ast
from typing import Any

from deepsource.exceptions.parsing import UnhandledJoinedStrException
from deepsource.parse.formatted_value import get_formatted_value_identifier
from deepsource.parse.name import get_name_identifier

from deepsource.parse.constant import get_constant_identifier


def get_joined_str_identifier(node: ast.JoinedStr) -> Any:
    values = []
    for value in node.values:
        match type(value):
            case ast.Constant:
                value = get_constant_identifier(value)
            case ast.Name:
                value = get_name_identifier(value)
            case ast.FormattedValue:
                value = get_formatted_value_identifier(value)
            case _:
                print(value, dir(value))
                raise UnhandledJoinedStrException(f"{value}")
        values.append(value)
    return tuple(values)
