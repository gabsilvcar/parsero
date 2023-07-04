from parsero.cfg import ContextFreeGrammar
from parsero.syntactic import Leaf, Node, SyntacticTree


class Struct:
    def __init__(self):
        self.type = None
        self.inh = None
        self.id = None

    def __str__(self):
        response = []

        if self.type:
            response.append("Type = {}".format(self.type))
        if self.inh:
            response.append("Inherited = {}".format(self.inh))
        return ', '.join(response)

class Semantics:
    def __init__(self, cfg: ContextFreeGrammar, tree: SyntacticTree):
        self.cfg = cfg
        self.tree = tree
        self.code = ""
        self.scope = dict()
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
        self.scope[head.children[1].entry] = head.struct.type

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

    def enforcetype_self_type(self, head):
        # TODO pretty message for error
        assert (self.scope[head.struct.id] == head.children[2].struct.type) or (head.children[2].struct.type == "null")
        pass

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
        assert head.struct.type == head.children[1].struct.type

    def typeheritage_termaux_type(self, head):
        head.children[1].struct.type = head.children[0].struct.type