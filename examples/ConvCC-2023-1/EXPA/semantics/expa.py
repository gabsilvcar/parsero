from parsero.cfg import ContextFreeGrammar
from parsero.semantic.semantic_analyzer import SemanticError
from parsero.syntactic import Leaf, Node, SyntacticTree


class ValueNotDefined(SemanticError):
    def __init__(self, token: Leaf | Node, tree: SyntacticTree):
        super().__init__(f"Valor não definido em {tree.val} na produção {token.val}", tree)


class HeritageNotDefined(SemanticError):
    def __init__(self, heritage_type: str, tree: SyntacticTree):
        super().__init__(f"Nenhum valor herdado do tipo {heritage_type} em {tree.val} na produção {' '.join(tree.prod)}", tree)


class IncompatibleTypes(SemanticError):
    def __init__(self, lhs_type: str, rhs_type: str, tree: SyntacticTree):
        super().__init__(f"Tipos incompatíveis: {lhs_type} e {rhs_type}", tree)


class BreakOutsideLoopScope(SemanticError):
    def __init__(self, tree: SyntacticTree):
        super().__init__(f"Break fora de escopo de loop", tree)

class InvalidSymbol(SemanticError):
    def __init__(self, symbol: str, tree: SyntacticTree):
        super().__init__(f"Simbolo {symbol} nao encontrado na tabela de simbolos", tree)

class ScopeEntry:
    def __init__(self):
        self.type = None
        self.node = None


class Struct:
    def __init__(self):
        self.type = None
        self.id = None
        self.inh = None

        self.inhnode = None
        self.syn = None
        self.node = None

        self.paramsyn = []
        self.paraminh = []

    def __str__(self):
        response = []

        if self.type:
            response.append("Type = {}".format(self.type))
        if self.inh:
            response.append("Inherited = {}".format(self.inh))
        if self.id:
            response.append("Id = {}".format(self.id))
        if self.syn:
            response.append("syn = {}".format(self.syn))
        if self.node:
            response.append("node = {}".format(self.node))
        if self.inhnode:
            response.append("inhnode = {}".format(self.inhnode))
        return ' - '.join(response)


class Semantics:
    def __init__(self, cfg: ContextFreeGrammar, tree: SyntacticTree):
        self.cfg = cfg
        self.tree = tree
        self.code = ""
        self.scope_counter = 0
        self.loop_scope_counter = 0

        self.scope_list = [dict()]
        self.scope_keeper = dict()
        self.scope_keeper[0] = self._get_current_scope()

    def _get_current_scope(self):
        return self.scope_list[len(self.scope_list) - 1]

    def _push_scope(self, is_loop_scope):
        self.scope_counter += 1
        self.scope_list.append(dict())
        self.scope_keeper[self.scope_counter] = self._get_current_scope()

        if is_loop_scope or self.loop_scope_counter > 0:
            self.loop_scope_counter += 1

    def _pop_scope(self):
        self.scope_list.pop()

        if self.loop_scope_counter > 0:
            self.loop_scope_counter -= 1

    # TODO throw error
    def _get_from_scope(self, symbol, tree):
        for scope in self.scope_list:
            if symbol in scope:
                return scope[symbol]

        raise InvalidSymbol(symbol, tree)

    def _get_entry_from_scope(self, symbol, tree):
        try:
            scope_entry = self._get_from_scope(symbol, tree)
            return scope_entry
        except:
            self._get_current_scope()[symbol] = ScopeEntry()
            return self._get_current_scope()[symbol]

    def _check_break_forscope(self):
        return self.loop_scope_counter > 0

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
        self._get_entry_from_scope(head.children[1].entry, head).type = head.struct.type

    def alloc_self_type(self, head):
        head.struct.type = head.children[2].struct.type

    def alloc_vardecl1_inh(self,  head):
        head.children[2].struct.inh = head.children[1].struct.type

    def vardcl_vardecl1_inh(self, head):
        head.children[2].struct.inh = head.children[0].struct.type

    def vardcl1_self_type(self, head):
        if head.children[1].entry is None:
            raise ValueNotDefined(head.children[1], head)
        if head.children[3].struct.type is None:
            raise ValueNotDefined(head.children[3], head)

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
        if head.children[0].struct.type is None:
            raise ValueNotDefined(head.children[0], head)
        head.struct.type = head.children[0].struct.type

    def termtype2_self_inh(self, head):
        head.struct.type = head.struct.inh

    def unarytypeheritage_self_type(self, head):
        head.struct.type = head.children[1].struct.type

    def enforcetype_self_type(self, head: SyntacticTree):
        lhs = self._get_from_scope(head.struct.id, head).type
        rhs = head.children[2].struct.type
        head.struct.type = rhs
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
        head.struct.node = self._get_from_scope(head.struct.id, head).node
        head.struct.type = self._get_from_scope(head.struct.id, head).type

    def termtype_self_type(self, head):
        lhs = head.struct.inh
        rhs = head.children[1].struct.type
        head.struct.type = rhs
        if lhs != rhs and rhs != "null":
            raise IncompatibleTypes(lhs, rhs, head)

    def termtype_self_inh(self, head):
        if head.struct.inh is None:
            raise HeritageNotDefined('inh', head)
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
        if head.children[1].struct.syn is None:
            raise ValueNotDefined(head.children[1], head)
        head.struct.syn = head.children[1].struct.syn

    def termnode_termaux_inhnode(self, head):
        UNARYEXPR = head.children[0]
        TERMAUX = head.children[1]
        if UNARYEXPR.struct.node is None:
            raise ValueNotDefined(UNARYEXPR, head)
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
        if head.struct.inhnode is None:
            raise HeritageNotDefined('inhnode', head)
        if TERMAUX.struct.node is None:
            raise ValueNotDefined(TERMAUX, head)
        UNARYEXPR.struct.inhnode = Node(head.val, [sign, head.struct.inhnode, TERMAUX.struct.node])

    def termauxnode_self_syn(self, head):
        UNARYEXPR = head.children[2]
        if UNARYEXPR.struct.syn is None:
            raise ValueNotDefined(UNARYEXPR, head)
        head.struct.syn = UNARYEXPR.struct.syn

    def termauxepsilon_self_syn(self, head):
        if head.struct.inhnode is None:
            raise HeritageNotDefined('inhnode', head)
        head.struct.syn = head.struct.inhnode

    def termauxepsilon_self_type(self, head):
        if head.struct.inh is None:
            raise HeritageNotDefined('inh', head)
        head.struct.type = head.struct.inh

    def nodeheritage_termaux1_inhnode(self, head):
        head.children[0].struct.inhnode = head.struct.inhnode

    def nodeheritage_self_syn(self, head):
        head.struct.syn = head.children[0].struct.syn

    def typeheritage_termaux1_inh(self, head):
        head.children[0].struct.inh = head.struct.inh

    def paramlist_statelist_code(self, head):
        label = head.children[1].entry
        self.code += "{}:\n".format(label)

    def paramcollector_paramlist1_paraminh(self, head):
        head.children[1].struct.paraminh.append(head.children[0].entry)
        if head.struct.paraminh:
            head.children[1].struct.paraminh += head.struct.paraminh

    def paramcollector_paramlist_paraminh(self, head):
        head.children[1].struct.paraminh = head.struct.paraminh

    def paramcollector_paramlistcall0_paraminh(self, head):
        head.children[1].struct.paraminh.append(head.children[0].entry)
        if head.struct.paraminh:
            head.children[1].struct.paraminh += head.struct.paraminh
    def paramcollector_paramlist0_paraminh(self, head):
        head.children[1].struct.paraminh = head.struct.paraminh

    def paramcollector_paramlistcall_paraminh(self, head):
        head.children[1].struct.paraminh = head.struct.paraminh

    def paramcollector_self_paramsyn(self, head):
        head.struct.paramsyn = head.children[1].struct.paramsyn

    def paramcollectorepsilon_self_paramsyn(self, head):
        head.struct.paramsyn = head.struct.paraminh

    def scope_self_inh(self, head):
        self._pop_scope()

    def scope_statelist_inh(self, head):
        self._push_scope(False)

    def scope_funclist_inh(self, head):
        self._push_scope(False)

    def scope_paramlist_scope(self, head):
        self._push_scope(False)

    def scope_statement_for(self, head):
        self._push_scope(True)

    def break_self_inh(self, head):
        if not self._check_break_forscope():
            raise BreakOutsideLoopScope(head)

    def nodefromscope_self_node(self, head):
        head.struct.node = self._get_from_scope(head.children[0].struct.id, head).node
        head.struct.type = self._get_from_scope(head.children[0].struct.id, head).type

    def nodetoscope_self_node(self, head):
        self._get_entry_from_scope(head.children[0].struct.id, head).node = head.children[2].struct.syn

    def copy_self_struct(self, head):
        head.struct = head.children[0].struct
