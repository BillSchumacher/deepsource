class UnhandledParsingException(Exception):
    pass


class UnhandledAssignException(UnhandledParsingException):
    pass


class UnhandledListCompException(UnhandledParsingException):
    pass


class UnhandledJoinedStrException(UnhandledParsingException):
    pass


class UnhandledListException(UnhandledParsingException):
    pass


class UnhandledTupleException(UnhandledParsingException):
    pass


class UnhandledGenExpException(UnhandledParsingException):
    pass


class UnhandledAssignTargetException(UnhandledParsingException):
    pass


class UnhandledCallIdentifierException(UnhandledParsingException):
    pass


class UnhandledCallArgException(UnhandledParsingException):
    pass


class UnhandledAwaitException(UnhandledParsingException):
    pass


class UnhandledBinOpException(UnhandledParsingException):
    pass


class UnhandledSubscriptIdentifierException(UnhandledParsingException):
    pass
