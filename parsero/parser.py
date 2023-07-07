import importlib.util
from itertools import cycle

from termcolor import colored

from parsero import syntactic
from parsero.cfg.contextfree_grammar import ContextFreeGrammar
from parsero.common.errors import LexicalError, SyntacticError
from parsero.lexical import LexicalAnalyzer, Token, SymbolTable
from parsero.semantic.semantic_analyzer import SemanticAnalyser, SemanticError
from parsero.syntactic import (
    SyntacticTree,
    calculate_first,
    calculate_follow,
    ll1_parse,
    treat_identation,
    Leaf
)


class Parsero:
    def __init__(self, regex_path, grammar_path, adapt, semantic_path=None):
        self.lexical = LexicalAnalyzer(regex_path)
        self.cfg = ContextFreeGrammar(grammar_path)

        if adapt:
            self.adapt_grammar()

        if semantic_path:
            spec = importlib.util.spec_from_file_location("semantics", semantic_path)
            self.semantic_lib = spec.loader.load_module()

        try:
            self.table: dict = syntactic.create_table(self.cfg)
        except RecursionError as error:
            msg = "Não foi possível remover a recursão à esquerda desta gramática."
            raise SyntacticError(grammar_path, msg)

    def parse(self, path: str) -> SyntacticTree:
        with open(path) as file:
            string = file.read()

        try:
            return self.parse_string(string)
        except SyntacticError as error:
            error.filename = path
            raise error

    def semantic_analysis(self, tree: SyntacticTree):
        semantic = SemanticAnalyser(self.semantic_lib, self.cfg, tree)
        return semantic.parse()

    def check_ll1(self) -> bool:
        first_dict = calculate_first(self.cfg)
        follow_dict = calculate_follow(self.cfg, first_dict)

        for head, prod in self.cfg.production_rules.items():
            for body in prod:
                if body[0] == "&":
                    intersection = first_dict[head].intersection(follow_dict[head])
                    if intersection:
                        print(head)
                        print(intersection)
                        return False
        return True

    def parse_string(self, string) -> SyntacticTree:
        string = treat_identation(string)

        tokens = self.lexical.tokenize_string(string)
        tokens.append(Token("$", "$"))

        try:
            return ll1_parse(tokens, self.table, self.cfg)
        except SyntacticError as error:
            error.data = string
            raise error

    def analyze(self, path: str):
        try:
            self.parse(path)
        except LexicalError:
            return False
        except SyntacticError:
            return False
        else:
            return True

    def adapt_grammar(self):
        self.cfg.left_factor()
        self.cfg.refactor_left_recursion()

        self.cfg.refactor_unitary_productions()
        self.cfg.remove_useless_symbols()

        assert self.check_ll1()

    def define_colors(self):
        colors = ["blue", "white", "red", "cyan", "yellow"]
        token_dict = dict()

        for ids in self.lexical.keywords:
            token_dict[ids] = "magenta"

        for ids, color in zip(self.lexical.token_ids, cycle(colors)):
            if "bracket" in ids:
                color = "blue"

            if ids == "comment":
                color = "green"

            token_dict[ids] = color

        return token_dict

    def highlight(self, path):
        separator = "\n" + (100 * "_") + "\n\n"
        token_dict = self.define_colors()
        last_error = None

        with open(path) as file:
            string = file.read()

        string = treat_identation(string)
        remaining = ""

        tree = None
        code = None
        st = None

        try:
            tree = self.parse(path)
            code, st = self.semantic_analysis(tree)
        except LexicalError as error:
            last_error = error
            remaining = string[error.index :]
            string = string[: error.index]
        except SyntacticError as error:
            last_error = error
            remaining = string[error.index :]
            string = string[: error.index]
        except SemanticError as error:
            from textwrap import dedent

            token = error.tree.token

            with open(path) as f:
                lines = f.read().splitlines()

                ret = dedent(f"""
                    Erro semântico no programa: {error}
                
                    {lines[token.line-1]}
                    {' ' * (token.col-1)}^
                
                    Linha: {token.line}
                    Coluna: {token.col}
                """)

                return ret
    

        output = []
        last_index = 0
        tokens = self.lexical.tokenize_string(string)
        for token in tokens:
            inter_tokens = string[last_index : token.index]
            lexeme = colored(token.attribute, token_dict[token.name])
            output.append(inter_tokens)
            output.append(lexeme)
            last_index += len(inter_tokens) + len(token.attribute)

        if last_error is not None:
            error_part = colored(remaining, "white", "on_red")
            output.append(error_part)
            output.append(separator)
            output.append(colored(str(last_error), "red"))

        reconstructed = "".join(output) + "\n"

        if last_error:
            return reconstructed

        exp_trees = list()
        if tree is not None:
            self.show_expression_tree(tree, exp_trees)

        exp_trees_str = "\n\n".join([str(x) for x in exp_trees])

        symbol_tables = list()
        if st is not None:
            for identifier, table in st.items():
                if len(table.st) > 0:
                    symbol_tables.append("Tabela de simbolos do escopo " + str(identifier) + ":\n" + str(table))

        symbol_tables_str = "\n\n".join([str(x) for x in symbol_tables])

        exp_valid_str = "As expressões aritméticas do programa são válidas."
        vardecl_valid_str = "As declarações de variáveis por escopo são válidas."
        break_valid_str = "Todo break está contido dentro de um escopo de repetição."
                
        ret = ""
        ret += reconstructed + "\n"
        ret += exp_trees_str + "\n"
        ret += symbol_tables_str + "\n\n"
        ret += exp_valid_str + "\n"
        ret += vardecl_valid_str + "\n"
        ret += break_valid_str + "\n\n"
        
        if code is not None:
            ret += code

        return ret

    def show_expression_tree(self, tree, exp_trees):
        for children in tree.children:
            if children.val == "EXPRESSION":
                exp_trees.append(children)
                continue
            if not isinstance(children, Leaf):
                self.show_expression_tree(children, exp_trees)
