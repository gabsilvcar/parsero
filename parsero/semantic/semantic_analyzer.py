from parsero.cfg import ContextFreeGrammar
from parsero.syntactic import Leaf, Node, SyntacticTree
from parsero.lexical import SymbolTable

class SemanticError(Exception):
    def __init__(self, message: str, tree: SyntacticTree):
        super().__init__(message)
        self.tree = tree
        print(tree.parent)


class SemanticAnalyser:
    def __init__(self, semantic_lib, cfg, tree):
        self.semantic_lib = semantic_lib
        self.semantic_handler = semantic_lib.Semantics(cfg, tree)
        self.cfg = cfg
        self.st_tree = tree
        self.symbol_tables = dict()
        self._prepare_node(tree)

    def parse(self):
        self._handle(self.st_tree)
        self._generate_symbol_tables()
        return self.semantic_handler.code, self.symbol_tables

    def _generate_symbol_tables(self):
        for identifier, symbol_table in self.semantic_handler.scope_keeper.items():
            st = SymbolTable()
            for symbol, entry in symbol_table.items():
                st.insert(symbol, entry.type)

            self.symbol_tables[identifier] = st

    def _prepare_node(self, node):
        node.struct = self.semantic_lib.Struct()
        for child in node.children:
            if not isinstance(child, Leaf):
                self._prepare_node(child)

    def _handle(self, head):
        rules = self._get_ordered_rules(head, self.cfg.get_rules(head.val, head.prod))
        for child in head.children:
            if not isinstance(child, Leaf):
                for rule in reversed(rules[child.val.lower()]):
                    self._execute_rule(rule, head)
                self._handle(child)

        for rule in reversed(rules["self"]):
            self._execute_rule(rule, head)

    # Makes sure inh rules are last
    def _get_ordered_rules(self, head, rules):
        mapped_rules = {child.lower(): [[], []] for child in head.prod}
        mapped_rules["self"] = [[], []]

        for rule in rules:
            parts = rule.split("_")
            if "self" in parts[1]:
                mapped_rules["self"][0].insert(0, rule)  # Self operations are always last
            else:
                mapped_rules[parts[1]][not "inh" in parts[2]].append(rule)

        final = dict()
        for key, value in mapped_rules.items():
            if len(value) > 0:
                final[key] = value[0] + value[1]
        return final

    def _execute_rule(self, rule, target):
        to_exec = "self.semantic_handler.{}(target)".format(rule)
        eval(to_exec)
