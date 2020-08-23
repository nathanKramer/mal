import traceback
import sys

import reader
import printer
import env
import core
import datatypes
import evaluation


def repl_env():
    ns = env.Env(None)
    for symbol, definition in core.ns.items():
        ns.set(symbol, definition)
    ns.set('eval', lambda ast: evaluation.EVAL(ast, ns))
    return ns


REPL_ENV = repl_env()


def read_evaluate_print(str):
    return printer.pr_str(
        evaluation.EVAL(
            reader.read_str(str),
            REPL_ENV
        )
    )


def main():
    read_evaluate_print(
        "(def! load-file (fn* (f) (eval (read-string (str \"(do \" (slurp f) \"\nnil)\")))))")
    read_evaluate_print("(def! not (fn* (a) (if a false true)))")
    while True:
        try:
            user_input = input("user> ")
            print(read_evaluate_print(user_input))
        except (reader.MalReaderError, env.SymbolNotFound):
            print("".join(traceback.format_exception(*sys.exc_info())))
        except EOFError:
            print("EOF Received, exiting.")
            exit()


if __name__ == "__main__":
    main()
