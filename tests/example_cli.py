from parsero import Parsero
from parsero.semantic.semantic_analyzer import SemanticError


if __name__ == "__main__":
    base = "examples/ConvCC-2023-1/"
    expa = base + "EXPA/"

    parser = Parsero(
        base + "regex.regex",
        expa + "gramatica_EXPA.ghm12",
        False,
        expa + "semantics/__init__.py",
    )

    tree = parser.parse(expa + "EXPA.example")
    try:
        parser.semantic_analysis(tree)
    except SemanticError as e:
        from textwrap import dedent

        token = e.tree.token

        with open(expa + "EXPA.example") as f:
            lines = f.read().splitlines()

        print(dedent(f"""
            Erro semântico no programa: {e}
                
                {lines[token.line-1]}
                {' ' * (token.col-1)}^
                
                Linha: {token.line}
                Coluna: {token.col}
        """))

        exit(1)

    print(tree)