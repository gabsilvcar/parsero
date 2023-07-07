from parsero import Parsero


def test_ine5426():
    base = "examples/ConvCC-2023-1/"
    expa = base + "EXPA/"

    parser = Parsero(
        base + "regex.regex",
        expa + "wip_expa_completo.ghm12",
        False,
        expa + "semantics/__init__.py",
    )

    tree = parser.parse(expa + "EXPA.example")
    parser.semantic_analysis(tree)
    # assert (tree.find("VARDECL") == "string")

    print(tree)

def test_ine5426_code_gen():
    base = "examples/ConvCC-2023-1/"
    expa = base + "GCI/"

    parser = Parsero(
        base + "regex.regex",
        expa + "gramatica_GCI.ghm12",
        False,
        expa + "semantics/__init__.py",
    )

    tree = parser.parse(expa + "EXPA.example")
    code = parser.semantic_analysis(tree)
    # assert (tree.find("VARDECL") == "string")

    print(tree)
    print(code)

