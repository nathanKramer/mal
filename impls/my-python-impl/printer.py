def _escape(s):
    return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')


def pr_str(data, print_readably=True):
    t = type(data)
    if t == list:
        inner = " ".join([pr_str(i, print_readably) for i in data])
        return f"({inner})"
    elif t == int or t == float:
        return str(data)
    elif data == True:
        return 'true'
    elif data == False:
        return 'false'
    elif data is None:
        return 'nil'
    elif t == str and print_readably:
        return '"' + _escape(data) + '"'
    return str(data)
