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

    def lvalue_self_node(self, head: Node):
        assert head.val == "LVALUE"
        lvalue_aux = head.children[1]
        head.struct.node = Node(head.val, ['id', lvalue_aux.struct.syn])

    def lvalueaux_bracket(self, head: Node):
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

    ##########################################
    # Epsilon

    def epsilon_self_syn(self, head: Node):
        assert head.struct is not None
        assert head.struct.inh is not None

        head.struct.syn = head.struct.inh

    ##########################################
    # Program

    ##########################################
    # Expression

    ##########################################
    # Expression_Aux
    def expression_aux_comparator_self_node(self, head: Node):
        assert head.val == "EXPRESSION_AUX"

        numexpression = head.children[1]
        head.struct.node = Node(head.val, ['comparator', numexpression.struct.syn])

    ##########################################
    # Factor
    def factor_float_self_node(self, head: Node):
        assert head.val == "FACTOR"

        id_node = head.children[0]
        id = id_node.val
        id_val = id_node.entry
        head.struct.node = Leaf(id, id_val)

    def factor_int_self_node(self, head: Node):
        assert head.val == "FACTOR"

        id_node = head.children[0]
        id = id_node.val
        id_val = id_node.entry
        head.struct.node = Leaf(id, id_val)

    def factor_string_self_node(self, head: Node):
        assert head.val == "FACTOR"

        id_node = head.children[0]
        id = id_node.val
        id_val = id_node.entry
        head.struct.node = Leaf(id, id_val)

    def factor_id_self_node(self, head: Node):
        assert head.val == "FACTOR"

        lvalue_aux = head.children[1]
        head.struct.node = Node(head.val, ['id', lvalue_aux.struct.syn])

    def factor_bracket_self_node(self, head: Node):
        assert head.val == "FACTOR"

        numexpression = head.children[1]
        head.struct.node = Node(head.val, ['(', numexpression.struct.syn, ')'])

    ##########################################
    # LValue_Aux
    def lvalueaux_lvalueaux1_inh(self, head: Node):
        assert head.val == "LVALUE_AUX"

        numexpression = head.children[1]
        lvalue_aux_child = head.children[3]
        lvalue_aux_child.struct.inh = Node(head.val, [head.struct.inh, '[', numexpression.struct.syn, ']'])

    def lvalueaux_self_syn(self, head: Node):
        assert head.val == "LVALUE_AUX"

        lvalue_aux_child = head.children[3]
        assert lvalue_aux_child.struct.syn is not None

        head.struct.syn = lvalue_aux_child.struct.syn

    ##########################################
    # NumExpression
    def numexpression_float_termaux1_inh(self, head: Node):
        assert head.val == "NUMEXPRESSION"
        term_aux = head.children[1]
        id_node = head.children[0]
        id = id_node.val
        id_val = id_node.entry
        constant = Leaf(id, id_val)
        term_aux.struct.inh = Node(head.val, [constant])

    def numexpression_float_numexpressionaux1_inh(self, head: Node):
        assert head.val == "NUMEXPRESSION"
        term_aux = head.children[1]
        numexpression = head.children[2]
        numexpression.struct.inh = term_aux.struct.node

    def numexpression_int_termaux1_inh(self, head: Node):
        assert head.val == "NUMEXPRESSION"
        term_aux = head.children[1]
        id_node = head.children[0]
        id = id_node.val
        id_val = id_node.entry
        constant = Leaf(id, id_val)
        term_aux.struct.inh = Node(head.val, [constant])

    def numexpression_int_numexpressionaux1_inh(self, head: Node):
        assert head.val == "NUMEXPRESSION"
        term_aux = head.children[1]
        numexpression = head.children[2]
        numexpression.struct.inh = term_aux.struct.node

    def numexpression_string_termaux1_inh(self, head: Node):
        assert head.val == "NUMEXPRESSION"
        term_aux = head.children[1]
        id_node = head.children[0]
        id = id_node.val
        id_val = id_node.entry
        constant = Leaf(id, id_val)
        term_aux.struct.inh = Node(head.val, [constant])

    def numexpression_string_numexpressionaux1_inh(self, head: Node):
        assert head.val == "NUMEXPRESSION"
        term_aux = head.children[1]
        numexpression = head.children[2]
        numexpression.struct.inh = term_aux.struct.node

    def numexpression_self_syn(self, head: Node):
        assert head.val == "NUMEXPRESSION"

        numexpression_child = head.children[2]
        assert numexpression_child.struct.syn is not None

        head.struct.syn = numexpression_child.struct.syn

    def numexpression_id_termaux1_inh(self, head: Node):
        assert head.val == "NUMEXPRESSION"

        lvalue_aux = head.children[1]
        term_aux = head.children[2]
        term_aux.struct.inh = Node(head.val, ['id', lvalue_aux.struct.syn])

    def numexpression_id_numexpressionaux1_inh(self, head: Node):
        assert head.val == "NUMEXPRESSION"
        term_aux = head.children[2]
        numexpression_aux = head.children[3]
        numexpression_aux.struct.inh = term_aux.struct.syn

    def numexpression_id_self_syn(self, head: Node):
        assert head.val == "NUMEXPRESSION"

        numexpression_child = head.children[3]
        assert numexpression_child.struct.syn is not None

        head.struct.syn = numexpression_child.struct.syn

    def numexpression_bracket_termaux1_inh(self, head: Node):
        assert head.val == "NUMEXPRESSION"

        numexpression = head.children[1]
        termaux = head.children[3]
        termaux.struct.inh = Node(head.val, ['(', numexpression.struct.syn, ')'])

    def numexpression_bracket_numexpressionaux1_inh(self, head: Node):
        assert head.val == "NUMEXPRESSION"

        numexpression_aux = head.children[4]
        term_aux = head.children[3]
        numexpression_aux.struct.inh = term_aux.struct.syn

    def numexpression_bracket_self_syn(self, head: Node):
        assert head.val == "NUMEXPRESSION"

        numexpression_child = head.children[4]
        assert numexpression_child.struct.syn is not None

        head.struct.syn = numexpression_child.struct.syn

    def numexpression_plus_termaux1_inh(self, head: Node):
        assert head.val == "NUMEXPRESSION"

        factor = head.children[1]
        term_aux = head.children[2]
        term_aux.struct.inh = Node(head.val, ['+', factor.struct.node])

    def numexpression_minus_termaux1_inh(self, head: Node):
        assert head.val == "NUMEXPRESSION"

        factor = head.children[1]
        term_aux = head.children[2]
        term_aux.struct.inh = Node(head.val, ['-', factor.struct.node])

    def numexpression_operation_numexpression1_inh(self, head: Node):
        assert head.val == "NUMEXPRESSION"

        term_aux = head.children[2]
        numexpression_aux = head.children[3]
        numexpression_aux.struct.inh = term_aux.struct.syn

    def numexpression_operation_self_syn(self, head: Node):
        assert head.val == "NUMEXPRESSION"

        numexpression_child = head.children[4]
        assert numexpression_child.struct.syn is not None

        head.struct.syn = numexpression_child.struct.syn

    ##########################################
    # NumExpression_Aux
    def numexpraux_operation_inh(self, head: Node, operation):
        term = head.children[1]
        numexpression_aux = head.children[2]
        numexpression_aux.struct.inh = Node(head.val, [operation, head.struct.inh, term.struct.syn])

    def numexpraux_minus_numexpraux1_inh(self, head: Node):
        assert head.val == "NUMEXPRESSION_AUX"
        self.numexpraux_operation_inh(head, '-')

    def numexpraux_plus_numexpraux1_inh(self, head: Node):
        assert head.val == "NUMEXPRESSION_AUX"
        self.numexpraux_operation_inh(head, '+')

    def numexpraux_mult_numexpraux1_inh(self, head: Node):
        assert head.val == "NUMEXPRESSION_AUX"
        self.numexpraux_operation_inh(head, '*')

    def numexpraux_div_numexpraux1_inh(self, head: Node):
        assert head.val == "NUMEXPRESSION_AUX"
        self.numexpraux_operation_inh(head, '/')

    def numexpraux_self_syn(self, head: Node):
        assert head.val == "NUMEXPRESSION_AUX"

        numexpression_aux_child = head.children[2]
        assert numexpression_aux_child.struct.syn is not None

        head.struct.syn = numexpression_aux_child.struct.syn

    ##########################################
    # StateList

    ##########################################
    # StateList_Aux

    ##########################################
    # Term
    def term_constant_self_syn(self, head: Node):
        assert head.val == "TERM"

        termaux_child = head.children[1]
        assert termaux_child.struct.syn is not None

        head.struct.syn = termaux_child.struct.syn

    def term_float_termaux1_inh(self, head: Node):
        term_aux = head.children[1]
        id_node = head.children[0]
        id = id_node.val
        id_val = id_node.entry
        constant = Leaf(id, id_val)
        term_aux.struct.inh = Node(head.val, [constant])

    def term_int_termaux1_inh(self, head: Node):
        term_aux = head.children[1]
        id_node = head.children[0]
        id = id_node.val
        id_val = id_node.entry
        constant = Leaf(id, id_val)
        term_aux.struct.inh = Node(head.val, [constant])

    def term_string_termaux1_inh(self, head: Node):
        term_aux = head.children[1]
        id_node = head.children[0]
        id = id_node.val
        id_val = id_node.entry
        constant = Leaf(id, id_val)
        term_aux.struct.inh = Node(head.val, [constant])

    def term_id_self_syn(self, head: Node):
        assert head.val == "TERM"

        termaux_child = head.children[2]
        assert termaux_child.struct.syn is not None

        head.struct.syn = termaux_child.struct.syn

    def term_id_termaux1_inh(self, head: Node):
        assert head.val == "TERM"

        lvalue_aux = head.children[1]
        term_aux = head.children[2]
        term_aux.struct.inh = Node(head.val, ['id', lvalue_aux.struct.syn])

    def term_bracket_self_syn(self, head: Node):
        assert head.val == "TERM"

        termaux_child = head.children[3]
        assert termaux_child.struct.syn is not None

        head.struct.syn = termaux_child.struct.syn

    def term_bracket_termaux1_inh(self, head: Node):
        assert head.val == "TERM"
        numexpression = head.children[1]
        termaux = head.children[3]
        termaux.struct.inh = Node(head.val,
                                  ['(', numexpression.struct.syn, ')'])  # eu deveria adicionar algo depois do ')'?

    def term_op_self_syn(self, head: Node):
        assert head.val == "TERM"

        termaux_child = head.children[2]
        assert termaux_child.struct.syn is not None

        head.struct.syn = termaux_child.struct.syn

    def term_minus_termaux1_inh(self, head: Node):
        assert head.val == "TERM"
        self.term_op_termaux1_inh(head, '-')

    def term_plus_termaux1_inh(self, head: Node):
        assert head.val == "TERM"
        self.term_op_termaux1_inh(head, '+')

    def term_op_termaux1_inh(self, head: Node, operation):
        factor = head.children[1]
        term_aux = head.children[2]
        term_aux.struct.inh = Node(head.val, [operation, factor.struct.node])

    ##########################################
    # Term_Aux
    def termaux_operation(self, head: Node, operation: str):
        assert head.val == "TERM_AUX"

        unaryexpr = head.children[1]
        term_aux = head.children[2]
        term_aux.struct.inh = Node(head.val, [operation, head.struct.inh, unaryexpr.struct.node])

    def termaux_mult_termaux1_inh(self, head: Node):
        self.termaux_operation(head, '*')

    def termaux_div_termaux1_inh(self, head: Node):
        self.termaux_operation(head, '/')

    def termaux_mod_termaux1_inh(self, head: Node):
        self.termaux_operation(head, '%')

    def termaux_self_syn(self, head: Node):
        assert head.val == "TERM_AUX"

        termaux_child = head.children[2]
        assert termaux_child.struct.syn is not None

        head.struct.syn = termaux_child.struct.syn

    ##########################################
    # UnaryExpr
    def unaryexpr_float_self_node(self, head: Node):
        assert head.val == "UNARYEXPR"

        id_node = head.children[0]
        id = id_node.val
        id_val = id_node.entry
        head.struct.node = Leaf(id, id_val)

    def unaryexpr_int_self_node(self, head: Node):
        assert head.val == "UNARYEXPR"

        id_node = head.children[0]
        id = id_node.val
        id_val = id_node.entry
        head.struct.node = Leaf(id, id_val)

    def unaryexpr_string_self_node(self, head: Node):
        assert head.val == "UNARYEXPR"

        id_node = head.children[0]
        id = id_node.val
        id_val = id_node.entry
        head.struct.node = Leaf(id, id_val)

    def unaryexpr_bracket_self_node(self, head: Node):
        assert head.val == "UNARYEXPR"

        numexpression = head.children[1]
        head.struct.node = Node(head.val, ['(', numexpression.struct.syn, ')'])

    def unaryexpr_id_self_node(self, head: Node):
        assert head.val == "UNARYEXPR"

        lvalue_aux = head.children[1]
        head.struct.node = Node(head.val, ['id', lvalue_aux.struct.syn])

    def unaryexpr_plus_self_node(self, head: Node):
        assert head.val == "UNARYEXPR"

        factor = head.children[1]
        head.struct.node = Node(head.val, ['+', factor.struct.syn])

    def unaryexpr_minus_self_node(self, head: Node):
        assert head.val == "UNARYEXPR"

        factor = head.children[1]
        head.struct.node = Node(head.val, ['-', factor.struct.syn])
