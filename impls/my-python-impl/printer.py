def pr_str(data):
    t = type(data)
    if t == list:
        inner = " ".join([pr_str(i) for i in data])
        return f"({inner})"
    elif t == int or t == float:
        return str(data)
    return str(data)
