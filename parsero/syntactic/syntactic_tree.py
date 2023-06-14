from __future__ import annotations


class Element:
    def __init__(self, val):
        self.val = val

    def __str__(self):
        return str(self.val)


class Leaf(Element):
    def __init__(self, val: str):
        super().__init__(val)

    def __str__(self, level=0):
        return "\t" * level + self.val + "\n"


class Node(Element):
    def __init__(self, val: str, prod, elements: list[Element] = None):
        super().__init__(val)
        if elements:
            self.children = elements
        else:
            self.children = []
        self.prod = prod

    def add_child(self, child: Element) -> Element:
        self.children.append(child)
        return child

    def add_node(self, child: Node) -> Node:
        self.add_child(child)
        return child

    def itself(self) -> Node:
        return self

    def __str__(self, level=0):
        ret = "\t" * level + repr(self.val) + " : " + ",".join(str(x) for x in self.prod) + "\n"
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret

    def find(self, head: str, desired_level=0, current_level=0):
        if self.val == head and desired_level == current_level:
            return self
        if len(self.children) == 0:
            return None
        for child in self.children:
            if isinstance(child, Leaf):
                continue
            result = child.find(head, desired_level, current_level + 1)
            # if result and desired_level==current_level:
            if result:
                return result


class SyntacticTree(Node):
    def __init__(self, root: str, prod: list):
        super().__init__(root, prod)

    def add_node(self, child: Node) -> Node:
        return super().add_node(child)

    def add_child(self, child: Element) -> Element:
        return super().add_child(child)

    def __str__(self):
        result = repr(self.val) + " : " + ",".join(str(x) for x in self.prod) + "\n"
        for i in range(0, len(self.children)):
            result += str(self.children[i].__str__(1))
        return result

    def find_node(self, head: str, desired_level=0, current_level=0) -> Node:
        if self.val == head and desired_level == current_level:
            return self.itself()  # Inheritance in python is fucking strange
        if len(self.children) == 0:
            return None
        for child in self.children:
            result = child.find(head, desired_level, current_level + 1)
            if result:
                return result


if __name__ == "__main__":
    st = SyntacticTree("Root", "r")

    a = Node("A", "a")
    b = Node("B", "b")
    c = Node("C", "c")
    d = Node("D", "d")
    b.add_node(d)
    st.add_node(a).add_node(b).add_node(c)

    print(st.find("D").add_node(Node("X", "a")))
    print(st)
