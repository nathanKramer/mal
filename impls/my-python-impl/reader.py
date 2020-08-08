import re


class MalReaderError(Exception):
    pass


class MalSyntaxError(MalReaderError):
    pass


class Reader:
    def __init__(self, tokens=[]):
        self.pos = 0
        self.tokens = tokens

    def next(self):
        curr = self.peek()
        self.pos += 1
        return curr

    def peek(self):
        return self.tokens[self.pos]


def read_str(str):
    tokens = tokenize(str)
    reader = Reader(tokens)
    return read_form(reader)


def read_form(reader):
    if reader.peek() == "(":
        ret = read_list(reader)
        return ret
    else:
        ret = read_atom(reader)
        return ret


def read_list(reader):
    reader.next()
    l = []
    while reader.peek() != ")":
        l.append(read_form(reader))
    reader.next()

    return l


def read_atom(reader):
    nxt = reader.next()
    if nxt == ")":
        raise MalSyntaxError("Unexpected token: {nxt}. unbalanced brackets!")
    elif nxt == "" or nxt == "\n":
        raise MalSyntaxError("expected ')', got EOF")
    if re.match(r"^-*\d+$", nxt) != None:
        return int(nxt)
    elif re.match(r"^-*\d+\.\d+$", nxt) != None:
        return float(nxt)
    return nxt


# [\s,]*: Matches any number of whitespaces or commas.
# This is not captured so it will be ignored and not tokenized.

# ~@: Captures the special two-characters ~@ (tokenized).

# [\[\]{}()'`~^@]: Captures any special single character, one of []{}()'`~^@ (tokenized).

# "(?:\\.|[^\\"])*"?: Starts capturing at a double-quote and stops at the next double-quote,
# unless it was preceded by a backslash in which case it includes it until the next double-quote (tokenized).
# It will also match unbalanced strings (no ending double-quote) which should be reported as an error.

# ;.*: Captures any sequence of characters starting with ; (tokenized).

# [^\s\[\]{}('"`,;)]*: Captures a sequence of zero or more non special characters (e.g. symbols, numbers, "true", "false", and "nil")
# and is sort of the inverse of the one above that captures special characters (tokenized).

TOKENS_PATTERN = r"[\s,]*(~@|[\[\]{}()'`~^@]|\"(?:\\.|[^\\\"])*\"?|;.*|[^\s\[\]{}('\"`,;)]*)"


def tokenize(str):
    return re.findall(TOKENS_PATTERN, str)
