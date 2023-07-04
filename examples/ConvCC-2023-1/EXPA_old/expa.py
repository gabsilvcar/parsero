from parsero.cfg import ContextFreeGrammar
from parsero.syntactic import SyntacticTree


class Struct:
    def __init__(self):
        self.inh = None
        self.syn = None

    def __str__(self):
        response = []

        if self.syn:
            response.append("Type = {}".format(self.syn))
        if self.inh:
            response.append("Inherited = {}".format(self.inh))
        return ', '.join(response)


class Semantics:
    def __init__(self, cfg: ContextFreeGrammar, tree: SyntacticTree):
        self.cfg = cfg
        self.tree = tree

    # Epsilon
    def epsilon_self_syn(self, head):
        assert head.struct is not None
        assert head.struct.inh is not None
        head.struct.syn = head.struct.inh

    ##########################################
    # Program
    def program_lvalueaux_inh(self, head):
        head.children[1].struct.inh = 'id'

    def programid_self_node(self, head):
        lvalue_aux = head.children[1]
        expression = head.children[3]
        head.struct.node = ['id', lvalue_aux.struct.syn, '=', expression.struct.syn, ';']

    def programbracket_self_node(self, head):
        statelist = head.children[1]
        head.struct.node = ['{', statelist.struct.syn, '}']

    def programepsilon_self_node(self, head):
        head.struct.node = None

    ##########################################
    # Expression
    def expr_numexpressionaux_inh(self, head):
        head.children[2].struct.inh = head.children[1].struct.syn

    def exprconst_self_syn(self, head):
        assert head.children[3].struct.syn is not None
        head.struct.syn = head.children[3].struct.syn

    def exprid_termaux_inh(self, head):
        head.children[2].struct.inh = ['id', head.children[1].struct.syn]

    def exprid_expressionaux_inh(self, head):
        head.children[4].struct.inh = head.children[3].struct.syn

    def exprid_self_syn(self, head):
        assert head.children[4].struct.syn is not None
        head.struct.syn = head.children[4].struct.syn

    def exprbracket_numexpressionaux_inh(self, head):
        head.children[4].struct.inh = head.children[3].struct.syn

    def exprbracket_expressionaux_inh(self, head):
        head.children[5].struct.inh = head.children[4].struct.syn

    def exprbracket_self_syn(self, head):
        assert head.children[5].struct.syn is not None
        head.struct.syn = head.children[5].struct.syn

    def exprop_expressionaux_inh(self, head):
        head.children[4].struct.inh = head.children[3].struct.syn

    def exprop_self_syn(self, head):
        assert head.children[4].struct.syn is not None
        head.struct.syn = head.children[4].struct.syn

    ##########################################
    # Expression_Aux
    def expressionaux_self_node(self, head):
        head.struct.node = ['comparator', head.children[1].struct.syn]

    ##########################################
    # Factor
    def factorid_self_node(self, head):
        head.struct.node = ['id', head.children[1].struct.syn]

    def factorbracket_self_node(self, head):
        head.struct.syn = ['(', head.children[1].struct.syn, ')']

    ##########################################
    # LValue_Aux
    def lvalueaux_lvalueaux_inh(self, head):
        head.children[3].struct.inh = [head.struct.inh, '[', head.children[1].struct.syn, ']']

    def lvalueaux_self_syn(self, head):
        assert head.children[3].struct.syn is not None
        head.struct.syn = head.children[3].struct.syn

    ##########################################
    # NumExpression
    def numexpr_numexpressionaux_inh(self, head):
        head.children[2].struct.inh = head.children[1].struct.syn

    def int_termaux_inh(self, head):
        head.children[1].struct.inh = 'integer'

    def str_termaux_inh(self, head):
        head.children[1].struct.inh = 'string'

    def numexpr_self_syn(self, head):
        assert head.children[2].struct.syn is not None
        head.struct.syn = head.children[2].struct.syn

    def numexprid_termaux_inh(self, head):
        head.children[2].struct.inh = ['id', head.children[1].struct.syn]

    def numexprid_self_syn(self, head):
        assert head.children[3].struct.syn is not None
        head.struct.syn = head.children[3].struct.syn

    def numexprbracket_numexpressionaux_inh(self, head):
        head.children[4].struct.inh = head.children[3].struct.syn

    def numexprbracket_self_syn(self, head):
        assert head.children[4].struct.syn is not None
        head.struct.syn = head.children[4].struct.syn

    def termaux_numexpressionaux_inh(self, head):
        head.children[3].struct.inh = head.children[2].struct.syn

    def numexprop_self_syn(self, head):
        assert head.children[4].struct.syn is not None
        head.struct.syn = head.children[4].struct.syn

    ##########################################
    # NumExpression_Aux
    def numexprauxminus_numexpressionaux_inh(self, head):
        head.children[2].struct.inh = ['-', head.struct.inh, head.children[1].struct.syn]

    def numexprauxplus_numexpressionaux_inh(self, head):
        head.children[2].struct.inh = ['+', head.struct.inh, head.children[1].struct.syn]

    def mult_numexpressionaux_inh(self, head):
        head.children[2].struct.inh = ['*', head.struct.inh, head.children[1].struct.syn]

    def div_numexpressionaux_inh(self, head):
        head.children[2].struct.inh = ['/', head.struct.inh, head.children[1].struct.syn]

    def numexpraux_self_syn(self, head):
        numexpression_aux_child = head.children[2]
        assert numexpression_aux_child.struct.syn is not None

        head.struct.syn = numexpression_aux_child.struct.syn

    ##########################################
    # StateList

    ##########################################
    # StateList_Aux

    ##########################################
    # Term
    def termconstant_self_syn(self, head):
        assert head.children[1].struct.syn is not None
        head.struct.syn = head.children[1].struct.syn

    def float_termaux_inh(self, head):
        head.children[1].struct.inh = 'float'

    def term_self_syn(self, head):
        assert head.children[2].struct.syn is not None
        head.struct.syn = head.children[2].struct.syn

    def termid_termaux_inh(self, head):
        head.children[2].struct.inh = [head.children[1].struct.syn]

    def termbracket_self_syn(self, head):
        assert head.children[3].struct.syn is not None
        head.struct.syn = head.children[3].struct.syn

    def bracket_termaux_inh(self, head):
        head.children[3].struct.inh = ['(', head.children[1].struct.syn, ')']

    def minus_termaux_inh(self, head):
        head.children[2].struct.inh = ['-', head.children[1].struct.syn]

    def plus_termaux_inh(self, head):
        head.children[2].struct.inh = ['+', head.children[1].struct.syn]

    ##########################################
    # Term_Aux
    def termauxmod_termaux_inh(self, head):
        head.children[2].struct.inh = ['%', head.struct.inh, head.children[1].struct.syn]

    def termaux_self_syn(self, head):
        assert head.children[2].struct.syn is not None
        head.struct.syn = head.children[2].struct.syn

    ##########################################
    # UnaryExpr
    def float_self_node(self, head):
        head.struct.syn = 'float'

    def int_self_node(self, head):
        head.struct.syn = 'integer'

    def string_self_node(self, head):
        head.struct.syn = 'string'

    def unaryexprbracket_self_node(self, head):
        head.struct.node = ['(', head.children[1].struct.syn, ')']

    def id_lvalueaux_inh(self, head):
        head.children[1].struct.inh = 'id'

    def unaryexprid_self_node(self, head):
        head.struct.syn = head.children[1].struct.syn

    def unaryexprplus_self_node(self, head):
        head.struct.syn = ['+', head.children[1].struct.syn]

    def unaryexprminus_self_node(self, head):
        head.struct.syn = ['-', head.children[1].struct.syn]
