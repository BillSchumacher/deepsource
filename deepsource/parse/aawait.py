import ast

from deepsource.exceptions.parsing import UnhandledAwaitException
from deepsource.parse.call import get_call_identifier
from deepsource.parse.name import get_name_identifier


def get_await_identifier(node: ast.Await) -> str:
    node_value = node.value
    match type(node_value):
        case ast.Call:
            value = get_call_identifier(node_value)
        case ast.Name:
            value = get_name_identifier(node_value)
        case _:
            raise UnhandledAwaitException(f"{node_value}")
    return value
