import datatypes
import env


def eval_ast(ast, local_env):
    if datatypes.is_list(ast):
        return [EVAL(n, local_env) for n in ast]
    elif datatypes.is_symbol(ast):
        return local_env.get(ast)
    else:
        return ast  # primitive value


def EVAL(ast, local_env):
    while True:
        if not datatypes.is_list(ast):
            return eval_ast(ast, local_env)
        if ast == []:
            return ast

        special_form = ast[0]
        if special_form == "def!":
            name, definition = ast[1], ast[2]
            local_env.set(name, EVAL(definition, local_env))
            return local_env.set(name, EVAL(definition, local_env))
        elif special_form == "do":
            for form in ast[1:-1]:
                EVAL(form, local_env)  # side effects
            ast = ast[-1]  # no return, TCO
        elif special_form == "if":
            condition = EVAL(ast[1], local_env)
            if condition == None or condition is False:
                if len(ast) > 3:
                    ast = ast[3]
                else:
                    ast = None
            else:
                ast = ast[2]  # no return, TCO
        elif special_form == "fn*":
            binds, body = ast[1], ast[2]

            def fn(*args):
                return EVAL(body, env.Env(local_env, binds, args))
            fn.__meta__ = None
            fn.__ast__ = body
            fn.__gen_env__ = lambda args: env.Env(local_env, binds, args)
            return fn
        elif special_form == "let*":
            let_env = env.Env(local_env)
            assigns = ast[1]
            for key, val in zip(assigns[::2], assigns[1::2]):
                let_env.set(key, EVAL(val, let_env))

            ast = ast[2]  # no return, TCO
        else:
            evaluated = eval_ast(ast, local_env)
            fn = evaluated[0]
            args = evaluated[1:]
            if hasattr(fn, '__ast__'):
                ast = fn.__ast__
                local_env = fn.__gen_env__(args)
            else:
                return fn(*args)
