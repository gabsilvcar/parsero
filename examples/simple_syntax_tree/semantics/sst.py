from parsero.cfg import ContextFreeGrammar
from parsero.syntactic import Leaf, Node, SyntacticTree


class Struct:
    def __init__(self):
        self.node = None
        self.inh = None
        self.syn = None


class Semantics:
    def __init__(self, cfg: ContextFreeGrammar, tree: SyntacticTree):
        self.cfg = cfg
        self.tree = tree

    def e_e1_inh(self, head: Node):
        assert head.val == "E"
        T = head.children[0]
        E1 = head.children[1]
        E1.struct.inh = T.struct.node

    def e_self_node(self, head):
        E1 = head.children[1]
        head.struct.node = E1.struct.syn

    def e1minus_e1_inh(self, head):
        assert head.val == "E1"
        self._e1_inh(head, "-")

    def e1plus_e1_inh(self, head):
        assert head.val == "E1"
        self._e1_inh(head, "+")

    def _e1_inh(self, head, sign):
        E_child = head.children[2]
        T_child = head.children[1]
        E_child.struct.inh = Node(head.val, [sign, head.struct.inh, T_child.struct.node])

    def e1epsilon_self_syn(self, head):
        assert head.val == "E1"
        assert head.children[0].val == "$"
        assert head.struct is not None
        assert head.struct.inh is not None

        head.struct.syn = head.struct.inh

    def e1_inh(self, head, sign):
        assert head.val == "E1"
        E_child = head.children[2]
        T_child = head.children[1]
        E_child.struct.inh = Node(head.val, [sign, head.struct.inh, T_child.struct.node])

    def e1_self_syn(self, head):
        E_child = head.children[2]

        assert head.val == "E1"
        assert E_child.struct.syn is not None

        head.struct.syn = E_child.struct.syn

    def tid_self_node(self, head: Node):
        id_node = head.children[0]
        id = id_node.val
        id_val = id_node.entry
        result = Leaf(id, id_val)
        head.struct.node = result

    def tnumber_self_node(self, head: Node):
        id_node = head.children[0]
        id = id_node.val
        id_val = id_node.entry
        result = Leaf(id, id_val)
        head.struct.node = result

    def tbracket_self_node(self, head: Node):
        assert head.val == "T"
        head.struct.node = head.children[0].struct.node
