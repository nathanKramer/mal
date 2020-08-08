class SymbolNotFound(Exception):
    pass


class Env:
    def __init__(self, outer):
        self.outer = outer
        self.data = {}

    def set(self, key, val):
        self.data[key] = val
        return self.data[key]

    def find(self, key):
        if key in self.data:
            return self.data.get(key)
        elif self.outer:
            return self.outer.find(key)
        else:
            return None

    def get(self, key):
        val = self.find(key)
        if not val:
            raise SymbolNotFound(f"Symbol '{key}' not found.")
        return val
