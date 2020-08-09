def is_list(ast):
    return type(ast) == list


def is_symbol(ast):
    return type(ast) == Symbol


def new_float(token):
    return float(token)


def new_int(token):
    return int(token)


def new_str(token):
    return str(token)


class Symbol(str):
    pass


def new_symbol(token):
    return Symbol(token)
