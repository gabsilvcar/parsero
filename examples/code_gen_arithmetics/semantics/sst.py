from parsero.cfg import ContextFreeGrammar
from parsero.syntactic import SyntacticTree


class Struct:
    def __init__(self):
        self.addr = None
        self.inh = None
        self.code = ""
        self.syncode = ""

    def __str__(self):
        response = []

        if self.addr:
            response.append("Addr = {}".format(self.addr))
        if self.inh:
            response.append("Inh_addr = {}".format(self.inh))
        if self.code:
            response.append("Code = {}".format(self.code))
        if self.syncode:
            response.append("SynCode = {}".format(self.syncode))
        return ', '.join(response)


class Leaf:
    def __init__(self, val):
        self.val = val

    def __str__(self):
        return self.val


class Node:
    def __init__(self, target, operation):
        self.target = target
        self.operation = operation
    def __str__(self):
        return "Target = {} Operation = {}".format(self.target, self.operation)

class Semantics:
    def __init__(self, cfg: ContextFreeGrammar, tree: SyntacticTree):
        self.cfg = cfg
        self.tree = tree
        self.memory = []
        self.code = ""

    def get_addr(self, thing) -> int:
        self.memory.append(thing)
        return len(self.memory) - 1


    def e1minus_e1_inh(self, head):
        self._e1_inh(head, "-")

    def e1plus_e1_inh(self, head):
        self._e1_inh(head, "+")

    def _e1_inh(self, head, sign):
        E_child = head.children[2]
        T_child = head.children[1]

        expr = "{} {} {}".format(self.memory[head.struct.inh], sign, self.memory[T_child.struct.addr])
        E_child.struct.inh = self.get_addr(eval(expr))
        E_child.struct.code += head.struct.code
        E_child.struct.code += T_child.struct.code

        E_child.struct.code += "t{} = t{} {} t{}\n".format(str(E_child.struct.inh), str(head.struct.inh), sign, T_child.struct.addr)

    def e1epsilon_self_syncode(self, head):
        head.struct.syncode = head.struct.code

    def e1_self_syncode(self, head):
        E_child = head.children[2]

        assert head.val == "E1"
        assert E_child.struct.syncode is not None

        head.struct.syncode = E_child.struct.syncode

    def tbracket_self_node(self, head: Node):
        assert head.val == "T"
        head.struct.node = head.children[0].struct.node

    def t_self_addr(self, head):
        id_node = head.children[0]
        id_val = id_node.entry
        head.struct.addr = self.get_addr(id_val)

    def t_self_code(self, head):
        addr = head.struct.addr
        head.struct.code += "t{} = {}\n".format(str(addr), self.memory[addr])

    def e_e1_inh(self, head: Node):
        T = head.children[0]
        E1 = head.children[1]
        E1.struct.inh = T.struct.addr
        E1.struct.code += T.struct.code

    def e_self_syncode(self, head):
        E1 = head.children[1]
        head.struct.syncode = E1.struct.syncode
        self.code = head.struct.syncode