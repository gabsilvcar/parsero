from parsero import Parsero


def test():
    base = "examples/code_gen_arithmetics/"
    path = base + "sst"
    parser = Parsero(
        path + ".regex",
        path + ".ghm12",
        False,
        base + "/semantics/__init__.py",
    )
    tree = parser.parse(path + ".example")
    code = parser.semantic_analysis(tree)
    print(tree)
    print(code)