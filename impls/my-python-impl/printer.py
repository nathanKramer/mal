def pr_str(data, _print_readably=True):
    t = type(data)
    if t == list:
        inner = " ".join([pr_str(i) for i in data])
        return f"({inner})"
    elif t == int or t == float:
        return str(data)
    elif data == True:
        return 'true'
    elif data == False:
        return 'false'
    elif data is None:
        return 'nil'
    return str(data)
