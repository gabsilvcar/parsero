from parsero import Parsero


def test():
    base = "examples/typing/"
    path = base + "type"
    parser = Parsero(
        path + ".regex",
        path + ".ghm12",
        base + "/semantics/__init__.py",
        False,
    )

    tree = parser.parse(path + ".example")

    parser.semantic_analysis(tree)
    print(tree)
    assert tree.struct.t == ["2", ["3", "integer"]]
