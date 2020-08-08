import functools
import env


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


REPL_ENV = env.Env(None)
REPL_ENV.set('+', addition)
REPL_ENV.set('-', subtraction)
REPL_ENV.set('*', multiplication)
REPL_ENV.set('/', division)
REPL_ENV.set('^', exponentiation)
