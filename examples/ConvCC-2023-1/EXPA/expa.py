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

    def program_self_node(self, head: Node):
        assert head.val == "PROGRAM"
        statement = head.children[0]
        head.struct.node = statement.struct.syn

    def statement_bracket_self_node(self, head: Node):
        assert head.val == "STATEMENT"
        statelist = head.children[1]
        head.struct.node = Node(head.val, ['{', statelist.struct.syn, '}'])

    def statement_self_node(self, head: Node):
        assert head.val == "STATEMENT"
        atribstat = head.children[0]
        head.struct.node = Node(head.val, [atribstat.struct.syn, ';'])

    def statelist_self_node(self, head: Node):
        pass

    def statelistaux_self_node(self, head: Node):
        pass

    def numexpression_self_node(self, head: Node):
        pass

    def numexpressionaux_self_node(self, head: Node):
        pass

    def expression_self_node(self, head: Node):
        pass

    def expreessionaux_self_node(self, head: Node):
        pass

    def term_self_node(self, head: Node):
        pass

    def term_symbol_aux_self_node(self, head: Node):
        pass

    def lvalue_self_node(self, head: Node):
        assert head.val == "LVALUE"
        lvalue_aux = head.children[1]
        head.struct.node = Node(head.val, ['id', lvalue_aux.struct.syn])

    def lvalueaux_bracket(self, head: Node):
        pass

    def epsilon_self_syn(self, head: Node):
        assert head.struct is not None
        assert head.struct.inh is not None

        head.struct.syn = head.struct.inh

    def epsilon_program_self_syn(self, head: Node):
        pass

    def atribstat_expression_inh(self, head: Node):
        assert head.val == "ATRIBSTAT"
        lvalue = head.children[0]
        expression = head.children[2]
        expression.struct.inh = Node(head.val, [lvalue.struct.node, '=', head.struct.inh])

    def atribstat_self_syn(self, head: Node):
        assert head.val == "ATRIBSTAT"

        expression = head.children[2]
        assert expression.struct.syn is not None

        head.struct.syn = expression.struct.syn

    def factor_self_node(self, head: Node):
        assert head.val == "FACTOR"
        lvalue = head.children[0]
        head.struct.node = lvalue.struct.syn

    def sign_unaryexpr_self_node(self, sign, head: Node):
        factor = head.children[1]
        head.struct.node = Node(head.val, [sign, factor.struct.syn])

    def minus_sign_unaryexpr_self_node(self, head: Node):
        assert head.val == "UNARYEXPR"
        self.sign_unaryexpr_self_node('-', head)

    def plus_sign_unaryexpr_self_node(self, head: Node):
        assert head.val == "UNARYEXPR"
        self.sign_unaryexpr_self_node('+', head)

    def unaryexpr_self_node(self, head: Node):
        assert head.val == "UNARYEXPR"
        factor = head.children[0]
        head.struct.node = factor.struct.syn

    def factor_int_self_node(self, head: Node):
        assert head.val == "FACTOR"
        id_node = head.children[0]
        id = id_node.val
        id_val = id_node.entry
        result = Leaf(id, id_val)
        head.struct.node = result

    def factor_float_self_node(self, head: Node):
        assert head.val == "FACTOR"
        id_node = head.children[0]
        id = id_node.val
        id_val = id_node.entry
        result = Leaf(id, id_val)
        head.struct.node = result

    def factor_string_self_node(self, head: Node):
        assert head.val == "FACTOR"
        id_node = head.children[0]
        id = id_node.val
        id_val = id_node.entry
        result = Leaf(id, id_val)
        head.struct.node = result

    def factor_bracket_self_node(self, head: Node):
        assert head.val == "FACTOR"
        numexpression = head.children[1]
        head.struct.node = Node(head.val, ['{', numexpression.struct.syn, '}'])
