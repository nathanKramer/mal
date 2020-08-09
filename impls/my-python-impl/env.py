class SymbolNotFound(Exception):
    pass


class Env:
    def __init__(self, outer, binds=[], exprs=[]):
        self.outer = outer
        self.data = {}
        for bind, expr in zip(binds, exprs):
            self.set(bind, expr)

    def set(self, key, val):
        self.data[key] = val
        return self.data[key]

    def find(self, key):
        if key in self.data:
            return self
        elif self.outer:
            return self.outer.find(key)
        else:
            return None

    def get(self, key):
        env = self.find(key)
        if not env:
            raise SymbolNotFound(f"Symbol '{key}' not found.")
        return env.data.get(key)
