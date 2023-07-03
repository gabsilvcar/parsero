from parsero import Parsero


def test():
    base = "examples/ConvCC-2023-1/"
    parser = Parsero(
        base + "regex.regex",
        base + "EXPA/gramatica_EXPA.ghm12",
        False,
        "examples/simple_syntax_tree/semantics/__init__.py",
    )

    tree, st = parser.parse(base + "/EXPA/EXPA.example")
    parser.semantic_analysis(tree, st)
    print(tree)

test()
