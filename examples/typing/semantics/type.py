from parsero.cfg import ContextFreeGrammar
from parsero.syntactic import Leaf, Node, SyntacticTree


class Struct:
    def __init__(self):
        self.t = None
        self.inh = None

    def __str__(self):
        return "Type = {}, Inherited = {}".format(self.t, self.inh)


class Semantics:
    def __init__(self, cfg: ContextFreeGrammar, tree: SyntacticTree):
        self.cfg = cfg
        self.tree = tree

    def t_self_t(self, head):
        head.struct.t = head.children[1].struct.t

    def t_c_inh(self, head):
        head.children[1].struct.inh = head.children[0].struct.t

    def bint_self_t(self, head):
        head.struct.t = "integer"

    def bfloat_self_t(self, head):
        head.struct.t = "float"

    def c1_self_t(self, head):
        assert head.children[1].val is not None
        assert head.children[3].struct.t is not None

        head.struct.t = [head.children[1].entry, head.children[3].struct.t]

    def c_c_inh(self, head):
        head.children[3].struct.inh = head.struct.inh

    def c2_self_t(self, head):
        head.struct.t = head.struct.inh
