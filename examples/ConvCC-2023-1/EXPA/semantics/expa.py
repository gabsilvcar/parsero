from parsero.cfg import ContextFreeGrammar
from parsero.semantic.semantic_analyzer import SemanticError
from parsero.syntactic import Leaf, Node, SyntacticTree


class IncompatibleTypes(SemanticError):
    def __init__(self, lhs_type: str, rhs_type: str, tree: SyntacticTree):
        super().__init__(f"Tipos incompatíveis: {lhs_type} e {rhs_type}", tree)


class Struct:
    def __init__(self):
        self.type = None
        self.id = None
        self.inh = None

        self.inhnode = None
        self.syn = None
        self.node = None

    def __str__(self):
        response = []

        if self.type:
            response.append("Type = {}".format(self.type))
        if self.inh:
            response.append("Inherited = {}".format(self.inh))
        #
        if self.syn:
            response.append("syn = {}".format(self.syn))
        if self.node:
            response.append("node = {}".format(self.node))
        if self.inhnode:
            response.append("inhnode = {}".format(self.inhnode))
        return ', '.join(response)


class Semantics:
    def __init__(self, cfg: ContextFreeGrammar, tree: SyntacticTree):
        self.cfg = cfg
        self.tree = tree
        self.code = ""

        self.scope_list = [dict()]


    def _get_current_scope(self):
        return self.scope_list[len(self.scope_list) - 1]

    def _push_scope(self):
        self.scope_list.append(dict())

    def _pop_scope(self):
        self.scope_list.pop()

    # TODO throw error
    def _get_from_scope(self, symbol):
        for scope in self.scope_list:
            if symbol in scope:
                return scope[symbol]

    def int_self_type(self, head):
        head.struct.type = "integer"

    def float_self_type(self, head):
        head.struct.type = "float"

    def string_self_type(self, head):
        head.struct.type = "string"

    def vardcl1epsilon_self_t(self, head):
        head.struct.type = head.struct.inh

    def vardcl_self_type(self, head):
        head.struct.type = head.children[2].struct.type
        self._get_current_scope()[head.children[1].entry] = head.struct.type

    def vardcl_vardecl1_inh(self, head):
        head.children[2].struct.inh = head.children[0].struct.type

    def vardcl1_self_type(self, head):
        assert head.children[1].val is not None
        assert head.children[3].struct.type is not None

        head.struct.type = [head.children[1].entry, head.children[3].struct.type]

    def vardcl1_vardecl1_inh(self, head):
        head.children[3].struct.inh = head.struct.inh

    def statement_self_type(self, head):
        head.struct.type = head.children[0].struct.type

    def factorstring_self_type(self, head):
        head.struct.type = "string"

    def factorint_self_type(self, head):
        head.struct.type = "integer"

    def typeheritage_self_type(self, head):
        head.struct.type = head.children[0].struct.type

    def unarytypeheritage_self_type(self, head):
        head.struct.type = head.children[1].struct.type

    def enforcetype_self_type(self, head: SyntacticTree):
        lhs = self._get_from_scope(head.struct.id)
        rhs = head.children[2].struct.type
        if lhs != rhs and rhs != "null":
            raise IncompatibleTypes(lhs, rhs, head)

    def factorfloat_self_type(self, head):
        head.struct.type = "float"

    def factornull_self_type(self, head):
        head.struct.type = "null"

    def idheritage_self_id(self, head):
        head.struct.id = head.children[0].struct.id

    # TODO matrix access
    def getid_self_id(self, head):
        head.struct.id = head.children[0].entry

    def termtype_self_type(self, head):
        lhs = head.struct.inh
        rhs = head.children[1].struct.type
        if lhs != rhs and rhs != "null":
            raise IncompatibleTypes(lhs, rhs, head)

    def termtype_self_inh(self, head):
        assert head.struct.inh is not None
        head.children[2].struct.inh = head.struct.inh

    def typeheritage_termaux_inh(self, head):
        head.children[1].struct.inh = head.children[0].struct.type

    def typeauxheritage_termaux_inh(self, head):
        head.children[2].struct.inh = head.struct.inh

    def typeauxheritage_termaux1_inh(self, head):
        head.children[2].struct.inh = head.struct.inh

    def unaryexpr_self_node(self, head):
        id_node = head.children[0]
        id = id_node.val
        id_val = id_node.entry
        result = Leaf(id, id_val)
        head.struct.node = result

    def getnode_self_node(self, head):
        head.struct.node = head.children[0].struct.node

    def termnode_self_node(self, head):
        assert head.children[1].struct.syn is not None
        head.struct.syn = head.children[1].struct.syn

    def termnode_termaux_inhnode(self, head):
        UNARYEXPR = head.children[0]
        TERMAUX = head.children[1]
        assert UNARYEXPR.struct.node is not None
        TERMAUX.struct.inhnode = UNARYEXPR.struct.node

    def termauxnode_termaux_inhnode(self, head):
        SIGN = head.children[0]
        self._node_maker(head, SIGN.children[0].entry)

    def termauxnode_termaux1_inhnode(self, head):
        SIGN = head.children[0]
        self._node_maker(head, SIGN.children[0].entry)

    def _node_maker(self, head, sign):
        UNARYEXPR = head.children[2]
        TERMAUX = head.children[1]
        assert head.struct.inhnode is not None
        assert TERMAUX.struct.node is not None
        UNARYEXPR.struct.inhnode = Node(head.val, [sign, head.struct.inhnode, TERMAUX.struct.node])

    def termauxnode_self_syn(self, head):
        UNARYEXPR = head.children[2]
        assert UNARYEXPR.struct.syn is not None
        head.struct.syn = UNARYEXPR.struct.syn

    def termauxepsilon_self_syn(self, head):
        assert head.struct.inhnode is not None
        head.struct.syn = head.struct.inhnode

    def nodeheritage_termaux1_inhnode(self, head):
        head.children[0].struct.inhnode = head.struct.inhnode

    def nodeheritage_self_syn(self, head):
        head.struct.syn = head.children[0].struct.syn

    def typeheritage_termaux1_inh(self, head):
        head.children[0].struct.inh = head.struct.inh

    def scope_self_inh(self, head):
        self._pop_scope()

    def scope_statelist_inh(self, head):
        self._push_scope()
