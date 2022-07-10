class SuspiciousOperation(Exception):
    pass


def suspicious_operation(message):
    raise SuspiciousOperation(message)
