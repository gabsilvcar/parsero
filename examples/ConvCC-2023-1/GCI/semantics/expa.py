from parsero.cfg import ContextFreeGrammar
from parsero.semantic.semantic_analyzer import SemanticError
from parsero.syntactic import Leaf, Node, SyntacticTree


class IncompatibleTypes(SemanticError):
    def __init__(self, lhs_type: str, rhs_type: str, tree: SyntacticTree):
        super().__init__(f"Tipos incompatíveis: {lhs_type} e {rhs_type}", tree)


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

        self.addr = None
        self.inhaddr = None
        self.code = ""
        self.syncode = ""

    def __str__(self):
        response = []

        if self.addr:
            response.append("addr = {}".format(self.addr))
        if self.inhaddr:
            response.append("inhaddr = {}".format(self.inhaddr))
        if self.code:
            response.append("code = {}".format(self.code))
        if self.syncode:
            response.append("syncode = {}".format(self.syncode))
        return ', '.join(response)


class Semantics:
    def __init__(self, cfg: ContextFreeGrammar, tree: SyntacticTree):
        self.cfg = cfg
        self.tree = tree
        self.code = ""

        self.scope_list = [dict()]

        self.memory = dict()
        self.memory_size = 0
        self.scope_keeper = dict()
        self.label_counter = 0

    def _get_label(self):
        self.label_counter += 1
        return self.label_counter
    def _get_addr(self, item=None) -> int:
        self.memory_size += 1
        if item : self.memory[item] = self.memory_size
        return self.memory_size

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

    def _get_entry_from_scope(self, symbol):
        if not symbol in self._get_current_scope():
            self._get_current_scope()[symbol] = ScopeEntry()
        return self._get_current_scope()[symbol]

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
        self._get_entry_from_scope(head.children[1].entry).type = head.struct.type

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

    def termtype2_self_inh(self, head):
        head.struct.type = head.struct.inh

    def unarytypeheritage_self_type(self, head):
        head.struct.type = head.children[1].struct.type

    def enforcetype_self_type(self, head: SyntacticTree):
        lhs = self._get_from_scope(head.struct.id).type
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

    def termtype_self_type(self, head):
        lhs = head.struct.inh
        rhs = head.children[1].struct.type
        head.struct.type = rhs
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

    def nodefromscope_self_node(self, head):
        head.struct.node = self._get_from_scope(head.children[0].struct.id).node

    def nodetoscope_self_node(self, head):
        self._get_entry_from_scope(head.children[0].struct.id).node = head.children[2].struct.syn

    def gettype_self_type(self, head):
        head.struct.type = self._get_entry_from_scope(head.struct.id).type

    def makecode_self_syncode(self, head):
        TERMAUX = head.children[1]
        assert TERMAUX.struct.addr is not None

        head.struct.syncode = TERMAUX.struct.syncode
        head.struct.addr = TERMAUX.struct.addr
        self.code += head.struct.syncode

    def makecode_termaux_inhcode(self, head):
        UNARYEXPR = head.children[0]
        TERMAUX = head.children[1]
        if UNARYEXPR.struct.addr is None:
            print(head.parent.parent)
        assert UNARYEXPR.struct.addr is not None
        assert UNARYEXPR.struct.code is not None

        TERMAUX.struct.inhaddr = UNARYEXPR.struct.addr
        TERMAUX.struct.code += UNARYEXPR.struct.code

    def factorint_self_code(self, head):
        id_node = head.children[0]
        id_val = id_node.entry
        addr = self._get_addr(id_val)
        head.struct.code += "t{} = {}\n".format(str(addr), id_val)
        head.struct.addr = addr

    def factorfloat_self_code(self, head):
        id_node = head.children[0]
        id_val = id_node.entry
        addr = self._get_addr(id_val)
        head.struct.code += "t{} = {}\n".format(str(addr), id_val)
        head.struct.addr = addr

    def factorstring_self_code(self, head):
        id_node = head.children[0]
        id_val = id_node.entry
        addr = self._get_addr(id_val)
        head.struct.code += "t{} = {}\n".format(str(addr), id_val)
        head.struct.addr = addr

    def factornull_self_code(self, head):
        id_node = head.children[0]
        id_val = id_node.entry
        addr = self._get_addr(id_val)
        head.struct.code += "t{} = {}\n".format(str(addr), id_val)
        head.struct.addr = addr

    def factorparenthesis_self_code(self, head):
        id_node = head.children[0]
        id_val = id_node.entry
        addr = self._get_addr(id_val)
        head.struct.code += "t{} = {}\n".format(str(addr), id_val)
        head.struct.addr = addr

    def factorlvalue_self_code(self, head):
        head.struct.addr = head.children[0].struct.id

    def termauxcode_termaux_inhcode(self, head):
        SIGN = head.children[0]
        self.make_node_code(head, SIGN.children[0].entry)

    def termauxcode_termaux1_inhcode(self, head):
        SIGN = head.children[0]
        self.make_node_code(head, SIGN.children[0].entry)

    def make_node_code(self, head, sign):
        UNARYEXPR = head.children[2]
        TERMAUX = head.children[1]
        assert head.struct.inhaddr is not ""
        assert TERMAUX.struct.code is not ""
        UNARYEXPR.struct.inhaddr = self._get_addr()
        UNARYEXPR.struct.code += head.struct.code
        UNARYEXPR.struct.code += TERMAUX.struct.code
        UNARYEXPR.struct.code += "{} = {} {} {}\n".format(self._treat_addr(UNARYEXPR.struct.inhaddr), self._treat_addr(head.struct.inhaddr),
                                                             sign, self._treat_addr(TERMAUX.struct.addr))

    def termauxcode_self_syncode(self, head):
        UNARYEXPR = head.children[2]
        assert UNARYEXPR.struct.syncode is not ""

        head.struct.syncode = UNARYEXPR.struct.syncode
        head.struct.addr = UNARYEXPR.struct.addr

    def termauxepsilon_self_syncode(self, head):
        head.struct.syncode = head.struct.code
        head.struct.addr = head.struct.inhaddr

    def unarycode_self_code(self, head):
        head.struct.code = head.children[0].struct.code
        head.struct.addr = head.children[0].struct.addr

    def codeheritage_self_syn(self, head):
        head.struct.syncode = head.children[0].struct.syncode
        head.struct.addr = head.children[0].struct.addr

    def codeheritage_termaux1_code(self, head):
        head.children[0].struct.code = head.struct.code
        head.children[0].struct.inhaddr = head.struct.inhaddr

    def codeheritage_self_syncode(self, head):
        head.struct.syncode = head.children[0].struct.syncode
        head.struct.addr = head.children[0].struct.addr

    def atribcode_self_code(self, head):
        id = head.children[0].struct.id
        taddr = head.children[2].struct.addr
        self.code += "{} = t{}\n".format(id, taddr)

    def _treat_addr(self, addr):
        tmp = str(addr)
        if tmp.isnumeric():
            return "t" + tmp
        else:
            return tmp
    def if_simpleif_code(self, head):
        label = "L" + str(self._get_label())
        self.code += "if False {} goto {}\n".format(self._treat_addr(head.children[2].struct.addr), label)
        head.struct.label = label

    def if_self_code(self, head):
        self.code += "{}:\n".format(head.struct.label)
