import traceback
import sys
import reader
import printer
import repl_env


def eval_ast(ast, repl_env):
    if type(ast) == list:
        return [EVAL(n, repl_env) for n in ast]
    elif type(ast) == str:  # hardcoded 'symobls' as strings rn cos lazy
        fn = repl_env.get(ast)
        if not fn:
            raise Exception(f"Unknown symbol: {ast}")
        return repl_env.get(ast)
    else:
        return ast


def EVAL(ast, repl_env):
    if ast == []:
        return ast
    elif type(ast) == list:
        evaluated = eval_ast(ast, repl_env)
        fn = evaluated[0]
        args = evaluated[1:]
        return fn(*args)
    else:
        return eval_ast(ast, repl_env)
    return ast


REPL_ENV = {'+': repl_env.addition,
            '-': repl_env.subtraction,
            '*': repl_env.multiplication,
            '/': repl_env.division,
            '^': repl_env.exponentiation}


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
        except reader.MalReaderError:
            print("".join(traceback.format_exception(*sys.exc_info())))
        except EOFError:
            print("EOF Received, exiting.")
            exit()


if __name__ == "__main__":
    main()
