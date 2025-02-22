from collections import defaultdict

from parsero import regex
from parsero.cfg.contextfree_grammar import ContextFreeGrammar
from parsero.common.errors import SyntacticError
from parsero.lexical.token import Token
from parsero.syntactic.syntactic_tree import Leaf, Node, SyntacticTree

IS_BLANK = regex.compiles("(( )|\n|\t|↳|↲)*")


def _first_helper(head: str, cfg: ContextFreeGrammar) -> set:
    first_set = set()
    if head in cfg.non_terminal_symbols:
        for prod in cfg.production_rules[head]:
            for i in range(len(prod)):
                nullable = False
                if prod[i] in cfg.terminal_symbols:
                    first_set.add(prod[i])
                    break
                else:
                    first_non_terminal = list(_first_helper(prod[i], cfg))
                    for symbol in first_non_terminal:
                        if symbol != "&":
                            first_set.add(symbol)
                        else:
                            nullable = True
                    if not nullable:
                        break
            if nullable:
                first_set.add("&")
    else:
        first_set.add(head)
    return first_set


def _follow_helper(cfg: ContextFreeGrammar, first_dict, follow_dict) -> dict:
    modified = False

    follow_dict[cfg.initial_symbol].add("$")

    for head, prod in cfg.production_rules.items():
        for body in prod:
            for i in range(len(body)):
                if body[i] in cfg.non_terminal_symbols:
                    if i != len(body) - 1:
                        nullable = False
                        for j in range(i, len(body)):
                            if j != len(body) - 1:
                                first_of_next = first_dict[body[j + 1]]

                                if "&" in first_of_next:
                                    first_of_next = first_of_next - {"&"}
                                    nullable = True
                                    modified |= not follow_dict[body[i]].issuperset(first_of_next)
                                    follow_dict[body[i]].update(first_of_next)
                                else:
                                    modified |= not follow_dict[body[i]].issuperset(first_of_next)
                                    follow_dict[body[i]].update(first_of_next)
                                    nullable = False
                                    break
                            else:
                                if nullable:
                                    modified |= not follow_dict[body[i]].issuperset(
                                        follow_dict[head]
                                    )
                                    follow_dict[body[i]].update(follow_dict[head])
                    else:
                        if body[i] in cfg.non_terminal_symbols:
                            modified |= not follow_dict[body[i]].issuperset(follow_dict[head])
                            follow_dict[body[i]].update(follow_dict[head])
    return modified


def calculate_first(cfg):
    first_dict = dict()
    for symbol in cfg.terminal_symbols:
        first_dict[symbol] = _first_helper(symbol, cfg)

    for symbol in cfg.non_terminal_symbols:
        first_dict[symbol] = _first_helper(symbol, cfg)
    return first_dict


def calculate_follow(cfg, first_dict=None):
    if first_dict is None:
        first_dict = calculate_first(cfg)

    follow_dict = dict()
    for symbol in cfg.non_terminal_symbols:
        follow_dict[symbol] = set()

    while True:
        modified = _follow_helper(cfg, first_dict, follow_dict)
        if not modified:
            break
    return follow_dict


def create_table(cfg: ContextFreeGrammar) -> dict:
    table = dict()
    first_dict: dict = calculate_first(cfg)
    follow_dict: dict = calculate_follow(cfg, first_dict)

    for head, prod in cfg.production_rules.items():
        for body in prod:
            first_set = first_dict[body[0]]

            if "&" in first_set:
                first_set = first_set - {"&"}
                for symbol in follow_dict[head]:
                    table[(head, symbol)] = body
            for symbol in first_set:
                table[head, symbol] = body

    return table


def ll1_parse(tokens: list[Token], table: dict, cfg: ContextFreeGrammar) -> SyntacticTree:
    stack = ["$", [cfg.initial_symbol, [None, -1]]]  # None represents the origin and 0 the level
    stacktrace = []
    stack_text = "Pilha: {} \nDesempilhado: {} Símbolo: {}"
    tree: SyntacticTree = None
    for token in tokens:
        if token.name == "comment":
            continue

        symbol = token.name
        while True:
            before_pop = str(stack)
            current = stack.pop()
            stacktrace.append(stack_text.format(before_pop[0], current[0], symbol))

            if symbol == current[0]:
                if symbol != "$":
                    tree.find_node(current[1][0], current[1][1]).add_child(
                        Leaf(symbol, token.attribute, token)
                    )
                break

            if not (current[0], symbol) in table:
                # Blank values can't cause error
                blank_symbol = IS_BLANK.evaluate(token.attribute)
                if (current[0] != "$") and blank_symbol:
                    stack.append(current[0])
                    break

                msg = f"Failed to parse token {token}. \nCurrent Stack: {stack}"
                start = token.index
                end = start + len(token.attribute)
                print(tree)
                raise SyntacticError.from_data("", msg, index=start, index_end=end)

            next_symbols = table[(current[0], symbol)]
            if tree:
                tree.find_node(current[1][0], current[1][1]).add_node(
                    Node(current[0], next_symbols, token=token)
                )
                pass
            else:
                tree = SyntacticTree(current[0], next_symbols)
            for next_symbol in reversed(next_symbols):
                if next_symbol != "&":
                    stack.append([next_symbol, [current[0], current[1][1] + 1]])

            if stack[-1] == symbol:
                tree.find_node(current[0], current[1][1] + 1).add_child(
                    Leaf(symbol, token.attribute, token)
                )  # check later
                stack.pop()
                break
    return tree
