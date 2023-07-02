from collections import OrderedDict

from tabulate import tabulate


class SymbolTable:
    def __init__(self, id, loop_scope):
        self.st = OrderedDict()
        self.id = id
        self.loop_scope = loop_scope
        self.father_scope = None

    def insert(self, symbol, value):
        if symbol not in self.st.keys():
            self.st[symbol] = [len(self.st), value]
            return

    def lookup(self, symbol):
        if symbol in self.st.keys():
            return self.st[symbol]
        raise KeyError("Symbol doesn't exist in Symbol Table.")

    def set_father_scope(self, father_scope):
        self.father_scope = father_scope

    def get_id(self):
        return self.id

    def is_loop_scope(self):
        return self.loop_scope

    def __str__(self):
        headers = ["index", "symbol", "value"]
        data = []

        for symbol, (index, value) in self.st.items():
            data.append([index, symbol, value])

        return tabulate(data, headers=headers, tablefmt="fancy_grid")
