from parsero import Parsero


def test_ine5426():
    base = "examples/ConvCC-2023-1/"
    expa = base + "EXPA/"

    parser = Parsero(
        base + "regex.regex",
        expa + "gramatica_EXPA.ghm12",
        False,
        expa + "semantics/__init__.py",
    )

    tree = parser.parse(expa + "EXPA.example")
    parser.semantic_analysis(tree)
    # assert (tree.find("VARDECL") == "string")

    print(tree)