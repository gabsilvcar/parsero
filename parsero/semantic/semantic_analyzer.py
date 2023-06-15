from parsero.syntactic import SyntacticTree, Node, Leaf


class SemanticAnalyser:
    def __init__(self, semantic_handler):
        self.st_tree = None
        self.semantic_handler = semantic_handler

    # def build_tree(self):
    def parse(self, st_tree: SyntacticTree):
        self.st_tree = st_tree
        order = self.get_execution_order()
        print("ORDER \n")
        print(",".join(repr(x) for x in order))

    def get_execution_order(self):
        order = []
        self._get_node_order(self.st_tree, order)
        return order

    def _get_node_order(self, node: Node, order: list):
        for child in node.children:
            if isinstance(child, Node):
                self._get_node_order(child, order)
            if isinstance(child, Leaf):
                self._mark_ready(child, order)
            self._mark_ready(child, order)

    def _mark_ready(self, element, order: list):
        if element not in order:
            order.append(element)


