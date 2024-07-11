import re


def capital_to_snake(name):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
