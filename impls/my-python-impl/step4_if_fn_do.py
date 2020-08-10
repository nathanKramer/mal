import traceback
import sys

import reader
import printer
import env
import core
import datatypes


def eval_ast(ast, local_env):
    if datatypes.is_list(ast):
        return [EVAL(n, local_env) for n in ast]
    elif datatypes.is_symbol(ast):
        return local_env.get(ast)
    else:
        return ast


def EVAL(ast, local_env):
    if ast == []:
        return ast
    elif type(ast) == list:
        special_form = ast[0]
        if special_form == "def!":
            name, definition = ast[1], ast[2]
            local_env.set(name, EVAL(definition, local_env))
            return local_env.set(name, EVAL(definition, local_env))
        elif special_form == "do":
            final = None
            for form in ast[1:]:
                final = EVAL(form, local_env)
            return final
        elif special_form == "if":
            condition = EVAL(ast[1], local_env)
            if condition == None or condition is False:
                if len(ast) > 3:
                    return EVAL(ast[3], local_env)
                else:
                    return None
            else:
                return EVAL(ast[2], local_env)
        elif special_form == "fn*":
            binds, body = ast[1], ast[2]

            def fn(*args):
                return EVAL(body, env.Env(local_env, binds, args))
            return fn
        elif special_form == "let*":
            let_env = env.Env(local_env)
            assigns, work = ast[1], ast[2]
            for key, val in zip(assigns[::2], assigns[1::2]):
                let_env.set(key, EVAL(val, let_env))
            return EVAL(work, let_env)
        else:
            evaluated = eval_ast(ast, local_env)
            fn = evaluated[0]
            args = evaluated[1:]
            return fn(*args)
    else:
        return eval_ast(ast, local_env)


def repl_env():
    ns = env.Env(None)
    for symbol, definition in core.ns.items():
        ns.set(symbol, definition)
    return ns


REPL_ENV = repl_env()


def read_evaluate_print(str):
    return printer.pr_str(
        EVAL(
            reader.read_str(str),
            REPL_ENV
        )
    )


def main():
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
