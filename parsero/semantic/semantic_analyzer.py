from parsero.cfg import ContextFreeGrammar
from parsero.syntactic import Leaf, Node, SyntacticTree


class SemanticAnalyser:
    def __init__(self, semantic_handler):
        self.st_tree = None
        self.semantic_handler = semantic_handler

    def parse(self, st_tree: SyntacticTree, cfg: ContextFreeGrammar):
        self.st_tree = st_tree
        self.cfg = cfg
        expression = "self.semantic_handler.{}(st_tree)"
        eval(expression.format(st_tree.val))
