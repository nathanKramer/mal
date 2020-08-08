import traceback
import sys
import reader
import printer
import env
import repl_env


def eval_ast(ast, repl_env):
    if type(ast) == list:
        return [EVAL(n, repl_env) for n in ast]
    elif type(ast) == str:  # hardcoded 'symobls' as strings rn cos lazy
        return repl_env.get(ast)
    else:
        return ast


def EVAL(ast, repl_env):
    if ast == []:
        return ast
    elif type(ast) == list:
        if ast[0] == "def!":
            name, definition = ast[1], ast[2]
            return repl_env.set(name, EVAL(definition, repl_env))
        elif ast[0] == "let*":
            let_env = env.Env(repl_env)
            assigns, work = ast[1], ast[2]
            for key, val in zip(assigns[::2], assigns[1::2]):
                let_env.set(key, EVAL(val, let_env))
            return EVAL(work, let_env)
        else:
            evaluated = eval_ast(ast, repl_env)
            fn = evaluated[0]
            args = evaluated[1:]
            return fn(*args)
    else:
        return eval_ast(ast, repl_env)


def read_evaluate_print(str):
    return printer.pr_str(
        EVAL(
            reader.read_str(str),
            repl_env.REPL_ENV
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
