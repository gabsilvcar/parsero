from parsero.cfg import ContextFreeGrammar
from parsero.syntactic import Leaf, Node, SyntacticTree


class Struct:
    def __init__(self):
        self.type = None
        self.inh = None

    def __str__(self):
        response = []

        if self.type:
            response.append("Type = {}".format(self.type))
        if self.inh:
            response.append("Inherited = {}".format(self.inh))
        return ', '.join(response)

class Semantics:
    def __init__(self, cfg: ContextFreeGrammar, tree: SyntacticTree):
        self.cfg = cfg
        self.tree = tree
        self.code = ""

