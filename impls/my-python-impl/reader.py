import re
import datatypes


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


def maybe_parse_string(token):
    matches = re.match(r"^\"(?:\\.|[^\\\"])*\"$", token)
    if not matches:
        return None
    escaped = token[1:-1].replace('\\"', '"').replace('\\n', '\n')
    return datatypes.new_str(escaped)


def maybe_parse_int(token):
    if not re.match(r"^-*\d+$", token):
        return None
    return datatypes.new_int(token)


def maybe_parse_float(token):
    if not re.match(r"^-*\d+\.\d+$", token):
        return None
    return datatypes.new_float(token)


def parse_scalar(token):
    if token == 'nil':
        return None
    elif token == 'true':
        return True
    elif token == 'false':
        return False
    else:
        return datatypes.new_symbol(token)


def read_atom(reader):
    token = reader.next()
    if token == ")":
        raise MalSyntaxError("Unexpected token: {token}. unbalanced brackets!")
    elif token == "" or token == "\n":
        raise MalSyntaxError("expected ')', got EOF")
    i = maybe_parse_int(token)
    if i != None:
        return i
    f = maybe_parse_float(token)
    if f != None:
        return f
    s = maybe_parse_string(token)
    if s != None:
        return s
    return parse_scalar(token)


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
