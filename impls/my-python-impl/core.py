import functools
import datatypes
import printer


def addition(x, *xs):
    return functools.reduce(
        lambda memo, x: memo + x,
        xs,
        x
    )


def subtraction(x, *xs):
    return functools.reduce(
        lambda memo, x: memo - x,
        xs,
        x
    )


def multiplication(x, *xs):
    return functools.reduce(
        lambda memo, x: memo * x,
        xs,
        x
    )


def division(x, *xs):
    return functools.reduce(
        lambda memo, x: memo / x,
        xs,
        x
    )


def exponentiation(x, *xs):
    return functools.reduce(
        lambda memo, x: pow(memo, x),
        xs,
        x
    )


def list_empty(l):
    return len(l) == 0


def prn(*args):
    print(" ".join(map(lambda exp: printer.pr_str(exp, True), args)))
    return None


# Tests the predicate against a and b.
# If a and b are equal lengh lists, the predicate is tested against the respective items in the lists
def _predicate(fn, a, b):
    result = fn(a, b)
    if datatypes.is_list(a) and datatypes.is_list(b) and len(a) == len(b):
        result = True
        for i, j in zip(a, b):
            result = result and fn(i, j)
    return result


def _equality(a, b):
    return _predicate(lambda a, b: a == b, a, b)


def _greater(a, b):
    return _predicate(lambda a, b: a > b, a, b)


def _greater_or_equal(a, b):
    return _predicate(lambda a, b: a >= b, a, b)


def _less_than(a, b):
    return _predicate(lambda a, b: a < b, a, b)


def _less_than_or_equal(a, b):
    return _predicate(lambda a, b: a <= b, a, b)


def _all_sequentially_n(fn, items):
    result = True
    for a, b in zip(items, items[1:]):
        result = result and fn(a, b)
    return result


def equality_n(*items):
    return _all_sequentially_n(_equality, items)


def greater_n(*items):
    return _all_sequentially_n(_greater, items)


def greater_or_equal_n(*items):
    return _all_sequentially_n(_greater_or_equal, items)


def less_than_n(*items):
    return _all_sequentially_n(_less_than, items)


def less_than_or_equal_n(*items):
    return _all_sequentially_n(_less_than_or_equal, items)


ns = {
    '+': addition,
    '-': subtraction,
    '*': multiplication,
    '/': division,
    '^': exponentiation,
    'list': lambda *args: list(args) or [],
    'list?': lambda l: datatypes.is_list(l),
    'empty?': list_empty,
    'count': lambda l: (l and len(l)) or 0,
    '=': equality_n,
    '>': greater_n,
    '>=': greater_or_equal_n,
    '<': less_than_n,
    '<=': less_than_or_equal_n,
    'prn': prn
}
