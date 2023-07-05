from parsero.cfg import ContextFreeGrammar
from parsero.syntactic import Leaf, Node, SyntacticTree


class SemanticAnalyser:
    def __init__(self, semantic_lib, cfg, tree):
        self.semantic_lib = semantic_lib
        self.semantic_handler = semantic_lib.Semantics(cfg, tree)
        self.cfg = cfg
        self.st_tree = tree
        self._prepare_node(tree)

    def parse(self):
        self._handle(self.st_tree)
        return self.semantic_handler.code

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
        print(to_exec)
        eval(to_exec)
