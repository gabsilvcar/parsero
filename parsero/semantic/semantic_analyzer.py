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
        expression = "self.semantic_handler.{}(self.st_tree)"
        eval(expression.format(self.st_tree.val))

    def _prepare_node(self, node):
        node.struct = self.semantic_lib.Struct()
        for child in node.children:
            if not isinstance(child, Leaf):
                self._prepare_node(child)

