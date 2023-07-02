from parsero.cfg import ContextFreeGrammar
from parsero.syntactic import SyntacticTree


class Struct:
    def __init__(self):
        self.node = None
        self.inh = None
        self.syn = None


class Leaf:
    def __init__(self, val: str, entry: str):
        self.val = val
        self.entry = entry


class Element:
    def __init__(self, val):
        self.val = val
        self.struct = None


class Node:
    def __init__(self, val: str, elements: list[Element] = None):
        self.val = val
        self.struct = None
        if elements:
            self.children = elements
        else:
            self.children = []


class Semantics:
    def __init__(self, cfg: ContextFreeGrammar, tree: SyntacticTree):
        self.cfg = cfg
        self.tree = tree

    ##########################################
    # Epsilon

    def epsilon_self_syn(self, head: Node):
        assert head.struct is not None
        assert head.struct.inh is not None

        head.struct.syn = head.struct.inh

    ##########################################
    # Program
    def program_lvalueaux_inh(self, head: Node):
        assert head.val == "PROGRAM"
        lvalue_aux = head.children[1]
        lvalue_aux.struct.inh = Node(head.val, ['id'])

    def programid_self_node(self, head: Node):
        assert head.val == "PROGRAM"

        lvalue_aux = head.children[1]
        expression = head.children[3]
        head.struct.node = Node(head.val, ['id', lvalue_aux.struct.syn, '=', expression.struct.syn, ';'])

    def programbracket_self_node(self, head: Node):
        assert head.val == "PROGRAM"

        statelist = head.children[1]
        head.struct.node = Node(head.val, ['{', statelist.struct.syn, '}'])

    def programepsilon_self_node(self, head: Node):
        assert head.val == "PROGRAM"
        head.struct.node = None

    ##########################################
    # Expression
    def exprfloat_termaux_inh(self, head: Node):
        assert head.val == "EXPRESSION"
        term_aux = head.children[1]
        id_node = head.children[0]
        id = id_node.val
        id_val = id_node.entry
        constant = Leaf(id, id_val)
        term_aux.struct.inh = Node(head.val, [constant])

    def exprfloat_numexpressionaux_inh(self, head: Node):
        assert head.val == "EXPRESSION"
        term_aux = head.children[1]
        numexpression_aux = head.children[2]
        numexpression_aux.struct.inh = term_aux.struct.syn

    def exprfloat_expressionaux_inh(self, head: Node):
        assert head.val == "EXPRESSION"
        numexpression_aux = head.children[2]
        expression_aux = head.children[3]
        expression_aux.struct.inh = numexpression_aux.struct.syn

    def exprint_termaux_inh(self, head: Node):
        assert head.val == "EXPRESSION"
        term_aux = head.children[1]
        id_node = head.children[0]
        id = id_node.val
        id_val = id_node.entry
        constant = Leaf(id, id_val)
        term_aux.struct.inh = Node(head.val, [constant])

    def exprint_numexpressionaux_inh(self, head: Node):
        assert head.val == "EXPRESSION"
        term_aux = head.children[1]
        numexpression_aux = head.children[2]
        numexpression_aux.struct.inh = term_aux.struct.syn

    def exprint_expressionaux_inh(self, head: Node):
        assert head.val == "EXPRESSION"
        numexpression_aux = head.children[2]
        expression_aux = head.children[3]
        expression_aux.struct.inh = numexpression_aux.struct.syn

    def exprstr_termaux_inh(self, head: Node):
        assert head.val == "EXPRESSION"
        term_aux = head.children[1]
        id_node = head.children[0]
        id = id_node.val
        id_val = id_node.entry
        constant = Leaf(id, id_val)
        term_aux.struct.inh = Node(head.val, [constant])

    def exprstr_numexpressionaux_inh(self, head: Node):
        assert head.val == "EXPRESSION"
        term_aux = head.children[1]
        numexpression_aux = head.children[2]
        numexpression_aux.struct.inh = term_aux.struct.syn

    def exprstr_expressionaux_inh(self, head: Node):
        assert head.val == "EXPRESSION"
        numexpression_aux = head.children[2]
        expression_aux = head.children[3]
        expression_aux.struct.inh = numexpression_aux.struct.syn

    def exprconst_self_syn(self, head: Node):
        assert head.val == "EXPRESSION"

        expression_aux_child = head.children[3]
        assert expression_aux_child.struct.syn is not None

        head.struct.syn = expression_aux_child.struct.syn

    def exprid_lvalueaux_inh(self, head: Node):
        assert head.val == "EXPRESSION"

        id = head.children[0]
        lvalue_aux = head.children[1]
        lvalue_aux.struct.inh = Leaf(id.val, id.entry)

    def exprid_termaux_inh(self, head: Node):
        assert head.val == "EXPRESSION"

        lvalue_aux = head.children[1]
        term_aux = head.children[2]
        term_aux.struct.inh = Node(head.val, ['id', lvalue_aux.struct.syn])

    def exprid_numexpressionaux_inh(self, head: Node):
        assert head.val == "EXPRESSION"

        term_aux = head.children[2]
        numexpression_aux = head.children[3]
        numexpression_aux.struct.inh = term_aux.struct.syn

    def exprid_expressionaux_inh(self, head: Node):
        assert head.val == "EXPRESSION"

        numexpression_aux = head.children[3]
        expression_aux = head.children[4]
        expression_aux.struct.inh = numexpression_aux.struct.syn

    def exprid_self_syn(self, head: Node):
        assert head.val == "EXPRESSION"

        expression_aux_child = head.children[4]
        assert expression_aux_child.struct.syn is not None

        head.struct.syn = expression_aux_child.struct.syn

    def exprbracket_termaux_inh(self, head: Node):
        assert head.val == "EXPRESSION"

        numexpression = head.children[1]
        termaux = head.children[3]
        termaux.struct.inh = Node(head.val, ['(', numexpression.struct.syn, ')'])

    def exprbracket_numexpressionaux_inh(self, head: Node):
        assert head.val == "EXPRESSION"

        term_aux = head.children[3]
        numexpression_aux = head.children[4]
        numexpression_aux.struct.inh = term_aux.struct.syn

    def exprbracket_expressionaux_inh(self, head: Node):
        assert head.val == "EXPRESSION"

        numexpression_aux = head.children[4]
        expression_aux = head.children[5]
        expression_aux.struct.inh = numexpression_aux.struct.syn

    def exprbracket_self_syn(self, head: Node):
        assert head.val == "EXPRESSION"

        expression_aux_child = head.children[5]
        assert expression_aux_child.struct.syn is not None

        head.struct.syn = expression_aux_child.struct.syn

    def expr_op_termaux1_inh(self, head: Node, operation):
        factor = head.children[1]
        term_aux = head.children[2]
        term_aux.struct.inh = Node(head.val, [operation, factor.struct.node])

    def exprminus_termaux_inh(self, head: Node):
        assert head.val == "EXPRESSION"
        self.expr_op_termaux1_inh(head, '-')

    def exprplus_termaux_inh(self, head: Node):
        assert head.val == "EXPRESSION"
        self.expr_op_termaux1_inh(head, '+')

    def exprop_numexpressionaux_inh(self, head: Node):
        assert head.val == "EXPRESSION"

        term_aux = head.children[2]
        numexpression_aux = head.children[3]
        numexpression_aux.struct.inh = term_aux.struct.syn

    def exprop_expressionaux_inh(self, head: Node):
        assert head.val == "EXPRESSION"

        numexpression_aux = head.children[3]
        expression_aux = head.children[4]
        expression_aux.struct.inh = numexpression_aux.struct.syn

    def exprop_self_syn(self, head: Node):
        assert head.val == "EXPRESSION"

        expression_aux_child = head.children[4]
        assert expression_aux_child.struct.syn is not None

        head.struct.syn = expression_aux_child.struct.syn

    ##########################################
    # Expression_Aux
    def expressionaux_self_node(self, head: Node):
        assert head.val == "EXPRESSION_AUX"

        numexpression = head.children[1]
        head.struct.node = Node(head.val, ['comparator', numexpression.struct.syn])

    ##########################################
    # Factor
    def factorfloat_self_node(self, head: Node):
        assert head.val == "FACTOR"

        id_node = head.children[0]
        id = id_node.val
        id_val = id_node.entry
        head.struct.node = Leaf(id, id_val)

    def factorint_self_node(self, head: Node):
        assert head.val == "FACTOR"

        id_node = head.children[0]
        id = id_node.val
        id_val = id_node.entry
        head.struct.node = Leaf(id, id_val)

    def factorstr_self_node(self, head: Node):
        assert head.val == "FACTOR"

        id_node = head.children[0]
        id = id_node.val
        id_val = id_node.entry
        head.struct.node = Leaf(id, id_val)

    def factorid_self_node(self, head: Node):
        assert head.val == "FACTOR"

        lvalue_aux = head.children[1]
        head.struct.node = Node(head.val, ['id', lvalue_aux.struct.syn])

    def factorbracket_self_node(self, head: Node):
        assert head.val == "FACTOR"

        numexpression = head.children[1]
        head.struct.node = Node(head.val, ['(', numexpression.struct.syn, ')'])

    ##########################################
    # LValue_Aux
    def lvalueaux_lvalueaux_inh(self, head: Node):
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
    def numexprfloat_termaux_inh(self, head: Node):
        assert head.val == "NUMEXPRESSION"
        term_aux = head.children[1]
        id_node = head.children[0]
        id = id_node.val
        id_val = id_node.entry
        constant = Leaf(id, id_val)
        term_aux.struct.inh = Node(head.val, [constant])

    def numexprfloat_numexpressionaux_inh(self, head: Node):
        assert head.val == "NUMEXPRESSION"
        term_aux = head.children[1]
        numexpression = head.children[2]
        numexpression.struct.inh = term_aux.struct.syn

    def numexprint_termaux_inh(self, head: Node):
        assert head.val == "NUMEXPRESSION"
        term_aux = head.children[1]
        id_node = head.children[0]
        id = id_node.val
        id_val = id_node.entry
        constant = Leaf(id, id_val)
        term_aux.struct.inh = Node(head.val, [constant])

    def numexprint_numexpressionaux_inh(self, head: Node):
        assert head.val == "NUMEXPRESSION"
        term_aux = head.children[1]
        numexpression = head.children[2]
        numexpression.struct.inh = term_aux.struct.syn

    def numexprstr_termaux_inh(self, head: Node):
        assert head.val == "NUMEXPRESSION"
        term_aux = head.children[1]
        id_node = head.children[0]
        id = id_node.val
        id_val = id_node.entry
        constant = Leaf(id, id_val)
        term_aux.struct.inh = Node(head.val, [constant])

    def numexprstr_numexpressionaux_inh(self, head: Node):
        assert head.val == "NUMEXPRESSION"
        term_aux = head.children[1]
        numexpression = head.children[2]
        numexpression.struct.inh = term_aux.struct.syn

    def numexpr_self_syn(self, head: Node):
        assert head.val == "NUMEXPRESSION"

        numexpression_child = head.children[2]
        assert numexpression_child.struct.syn is not None

        head.struct.syn = numexpression_child.struct.syn

    def numexprid_termaux_inh(self, head: Node):
        assert head.val == "NUMEXPRESSION"

        lvalue_aux = head.children[1]
        term_aux = head.children[2]
        term_aux.struct.inh = Node(head.val, ['id', lvalue_aux.struct.syn])

    def numexprid_numexpressionaux_inh(self, head: Node):
        assert head.val == "NUMEXPRESSION"
        term_aux = head.children[2]
        numexpression_aux = head.children[3]
        numexpression_aux.struct.inh = term_aux.struct.syn

    def numexprid_self_syn(self, head: Node):
        assert head.val == "NUMEXPRESSION"

        numexpression_child = head.children[3]
        assert numexpression_child.struct.syn is not None

        head.struct.syn = numexpression_child.struct.syn

    def numexprbracket_termaux_inh(self, head: Node):
        assert head.val == "NUMEXPRESSION"

        numexpression = head.children[1]
        termaux = head.children[3]
        termaux.struct.inh = Node(head.val, ['(', numexpression.struct.syn, ')'])

    def numexprbracket_numexpressionaux_inh(self, head: Node):
        assert head.val == "NUMEXPRESSION"

        numexpression_aux = head.children[4]
        term_aux = head.children[3]
        numexpression_aux.struct.inh = term_aux.struct.syn

    def numexprbracket_self_syn(self, head: Node):
        assert head.val == "NUMEXPRESSION"

        numexpression_child = head.children[4]
        assert numexpression_child.struct.syn is not None

        head.struct.syn = numexpression_child.struct.syn

    def numexprplus_termaux_inh(self, head: Node):
        assert head.val == "NUMEXPRESSION"

        factor = head.children[1]
        term_aux = head.children[2]
        term_aux.struct.inh = Node(head.val, ['+', factor.struct.node])

    def numexprminus_termaux_inh(self, head: Node):
        assert head.val == "NUMEXPRESSION"

        factor = head.children[1]
        term_aux = head.children[2]
        term_aux.struct.inh = Node(head.val, ['-', factor.struct.node])

    def numexprop_numexpressionaux_inh(self, head: Node):
        assert head.val == "NUMEXPRESSION"

        term_aux = head.children[2]
        numexpression_aux = head.children[3]
        numexpression_aux.struct.inh = term_aux.struct.syn

    def numexprop_self_syn(self, head: Node):
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

    def numexprauxminus_numexpressionaux_inh(self, head: Node):
        assert head.val == "NUMEXPRESSIONAUX"
        self.numexpraux_operation_inh(head, '-')

    def numexprauxplus_numexpressionaux_inh(self, head: Node):
        assert head.val == "NUMEXPRESSIONAUX"
        self.numexpraux_operation_inh(head, '+')

    def numexprauxmult_numexpressionaux_inh(self, head: Node):
        assert head.val == "NUMEXPRESSIONAUX"
        self.numexpraux_operation_inh(head, '*')

    def numexprauxdiv_numexpressionaux_inh(self, head: Node):
        assert head.val == "NUMEXPRESSIONAUX"
        self.numexpraux_operation_inh(head, '/')

    def numexpraux_self_syn(self, head: Node):
        assert head.val == "NUMEXPRESSIONAUX"

        numexpression_aux_child = head.children[2]
        assert numexpression_aux_child.struct.syn is not None

        head.struct.syn = numexpression_aux_child.struct.syn

    ##########################################
    # StateList

    ##########################################
    # StateList_Aux

    ##########################################
    # Term
    def termconstant_self_syn(self, head: Node):
        assert head.val == "TERM"

        termaux_child = head.children[1]
        assert termaux_child.struct.syn is not None

        head.struct.syn = termaux_child.struct.syn

    def termfloat_termaux_inh(self, head: Node):
        term_aux = head.children[1]
        id_node = head.children[0]
        id = id_node.val
        id_val = id_node.entry
        constant = Leaf(id, id_val)
        term_aux.struct.inh = Node(head.val, [constant])

    def termint_termaux_inh(self, head: Node):
        term_aux = head.children[1]
        id_node = head.children[0]
        id = id_node.val
        id_val = id_node.entry
        constant = Leaf(id, id_val)
        term_aux.struct.inh = Node(head.val, [constant])

    def termstring_termaux_inh(self, head: Node):
        term_aux = head.children[1]
        id_node = head.children[0]
        id = id_node.val
        id_val = id_node.entry
        constant = Leaf(id, id_val)
        term_aux.struct.inh = Node(head.val, [constant])

    def termid_self_syn(self, head: Node):
        assert head.val == "TERM"

        termaux_child = head.children[2]
        assert termaux_child.struct.syn is not None

        head.struct.syn = termaux_child.struct.syn

    def termid_lvalueaux_inh(self, head: Node):
        assert head.val == "TERM"
        lvalue_aux = head.children[1]
        id = head.children[0]
        lvalue_aux.struct.inh = Leaf(id.val, id.entry)

    def termid_termaux_inh(self, head: Node):
        assert head.val == "TERM"

        lvalue_aux = head.children[1]
        term_aux = head.children[2]
        term_aux.struct.inh = Node(head.val, [lvalue_aux.struct.syn])

    def termbracket_self_syn(self, head: Node):
        assert head.val == "TERM"

        termaux_child = head.children[3]
        assert termaux_child.struct.syn is not None

        head.struct.syn = termaux_child.struct.syn

    def termbracket_termaux_inh(self, head: Node):
        assert head.val == "TERM"
        numexpression = head.children[1]
        termaux = head.children[3]
        termaux.struct.inh = Node(head.val, ['(', numexpression.struct.syn, ')']) # eu deveria adicionar algo depois do ')'?

    def termop_self_syn(self, head: Node):
        assert head.val == "TERM"

        termaux_child = head.children[2]
        assert termaux_child.struct.syn is not None

        head.struct.syn = termaux_child.struct.syn

    def termminus_termaux_inh(self, head: Node):
        assert head.val == "TERM"
        self.term_op_termaux1_inh(head, '-')

    def termplus_termaux_inh(self, head: Node):
        assert head.val == "TERM"
        self.term_op_termaux1_inh(head, '+')

    def term_op_termaux1_inh(self, head: Node, operation):
        factor = head.children[1]
        term_aux = head.children[2]
        term_aux.struct.inh = Node(head.val, [operation, factor.struct.node])

    ##########################################
    # Term_Aux
    def termaux_operation(self, head: Node, operation: str):
        assert head.val == "TERMAUX"

        unaryexpr = head.children[1]
        term_aux = head.children[2]
        term_aux.struct.inh = Node(head.val, [operation, head.struct.inh, unaryexpr.struct.node])

    def termauxmult_termaux_inh(self, head: Node):
        self.termaux_operation(head, '*')

    def termauxdiv_termaux_inh(self, head: Node):
        self.termaux_operation(head, '/')

    def termauxmod_termaux_inh(self, head: Node):
        self.termaux_operation(head, '%')

    def termaux_self_syn(self, head: Node):
        assert head.val == "TERMAUX"

        termaux_child = head.children[2]
        assert termaux_child.struct.syn is not None

        head.struct.syn = termaux_child.struct.syn

    ##########################################
    # UnaryExpr
    def unaryexprfloat_self_node(self, head: Node):
        assert head.val == "UNARYEXPR"

        id_node = head.children[0]
        id = id_node.val
        id_val = id_node.entry
        head.struct.node = Leaf(id, id_val)

    def unaryexprint_self_node(self, head: Node):
        assert head.val == "UNARYEXPR"

        id_node = head.children[0]
        id = id_node.val
        id_val = id_node.entry
        head.struct.node = Leaf(id, id_val)

    def unaryexprstring_self_node(self, head: Node):
        assert head.val == "UNARYEXPR"

        id_node = head.children[0]
        id = id_node.val
        id_val = id_node.entry
        head.struct.node = Leaf(id, id_val)

    def unaryexprbracket_self_node(self, head: Node):
        assert head.val == "UNARYEXPR"

        numexpression = head.children[1]
        head.struct.node = Node(head.val, ['(', numexpression.struct.syn, ')'])

    def unaryexprid_self_node(self, head: Node):
        assert head.val == "UNARYEXPR"

        lvalue_aux = head.children[1]
        head.struct.node = Node(head.val, ['id', lvalue_aux.struct.syn])

    def unaryexprplus_self_node(self, head: Node):
        assert head.val == "UNARYEXPR"

        factor = head.children[1]
        head.struct.node = Node(head.val, ['+', factor.struct.syn])

    def unaryexprminus_self_node(self, head: Node):
        assert head.val == "UNARYEXPR"

        factor = head.children[1]
        head.struct.node = Node(head.val, ['-', factor.struct.syn])
