from parsero.cfg import ContextFreeGrammar
from parsero.syntactic import Leaf, Node, SyntacticTree


class Struct:
    def __init__(self):
        self.node = None
        self.inh = None
        self.syn = None


class Semantics:
    EXPRESSION = "self.{}(target)"

    def __init__(self, cfg: ContextFreeGrammar, tree: SyntacticTree):
        self.cfg = cfg
        self.tree = tree

    def E(self, head: Node):
        assert head.val == "E"
        T = head.children[0]
        E1 = head.children[1]
        self.T(T)
        E1.struct.inh = T.struct.node
        self.E1(E1)
        head.struct.node = E1.struct.syn

    def E1(self, head):
        assert head.val == "E1"
        target = head
        rule = self.cfg.get_rule(head.val, head.prod)
        eval(self.EXPRESSION.format(rule))

    def E1Minus(self, head):
        assert head.val == "E1"
        self.E1Inh(head, "-")

    def E1Plus(self, head):
        assert head.val == "E1"
        self.E1Inh(head, "+")

    def E1Epsilon(self, head):
        assert head.val == "E1"
        assert head.children[0].val == "$"
        assert head.struct is not None
        assert head.struct.inh is not None

        head.struct.syn = head.struct.inh

    def E1Inh(self, head, sign):
        assert head.val == "E1"
        E_child = head.children[2]
        T_child = head.children[1]
        self.T(T_child)
        E_child.struct.inh = Node(head.val, [sign, head.struct.inh, T_child.struct.node])
        self.E1(E_child)
        self.E1Syn(head)

    def E1Syn(self, head):
        E_child = head.children[2]

        assert head.val == "E1"
        assert E_child.struct.syn is not None

        head.struct.syn = E_child.struct.syn

    def T(self, head):
        assert head.val == "T"
        rule = self.cfg.get_rule(head.val, head.prod)
        target = head.children[0]
        eval(self.EXPRESSION.format(rule))

    def TId(self, head: Node):
        id = head.val
        id_val = head.entry
        result = Leaf(id, id_val)
        head.parent.struct.node = result

    def TNumber(self, head: Node):
        id = head.val
        id_val = head.entry
        result = Leaf(id, id_val)
        head.parent.struct.node = result

    def TBrackets(self, head: Node, production: dict):
        assert head.val == "T"
        head.struct.node = head.children[0].struct.node
