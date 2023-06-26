from parsero import Parsero


def test():
    base = "examples/ConvCC-2023-1/"
    parser = Parsero(
        base + "regex.regex",
        base + "gramatica_EXPA.ghm12",
        False,
        "examples/simple_syntax_tree/semantics/__init__.py",
    )

    tree = parser.parse(base + "/EXPA.example")
    parser.semantic_analysis(tree)
    print(tree)
