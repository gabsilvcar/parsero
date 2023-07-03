from collections import OrderedDict
from tabulate import tabulate
from parsero.lexical.token import Token


class SymbolTable:
    def __init__(self, id, loop_scope = False):
        self.st = OrderedDict()
        self.id = id
        self.loop_scope = loop_scope
        self.father = None

    def insert(self, token):
        if token.attribute not in self.st.keys():
            self.st[token.attribute] = [token.line]
            return

        raise KeyError(f"Symbol {token.attribute} already exists in SymbolTable (line {token.line})")

    def insert_additional_info(self, symbol, info):
        self.lookup(symbol).append(info)

    def lookup(self, symbol):
        if symbol in self.st.keys():
            return self.st[symbol]
        raise KeyError(f"Symbol {symbol} doesn't exist in Symbol Table.")

    def is_loop_scope(self):
        return self.loop_scope

    def get_id(self):
        return self.id

    def set_father(self, father):
        self.father = father

    def get_father(self):
        return self.father

    def __str__(self):
        headers = ["symbol", "line", "type"]
        data = []

        for symbol, info in self.st.items():
            symbol_line = info[0]
            symbol_type = None
            
            if len(info) > 1:
                symbol_type = info[1]

            data.append([symbol, symbol_line, symbol_type])

        return tabulate(data, headers=headers, tablefmt="fancy_grid")
