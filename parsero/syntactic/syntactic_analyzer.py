from collections import defaultdict

from parsero import regex
from parsero.cfg.contextfree_grammar import ContextFreeGrammar
from parsero.common.errors import SyntacticError
from parsero.lexical.token import Token
from parsero.lexical.symbol_table import SymbolTable
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


def ll1_parse(tokens: list, table: dict, cfg: ContextFreeGrammar) -> tuple[SyntacticTree, dict]:
    stack = ["$", [cfg.initial_symbol, [None, -1]]]  # None represents the origin and 0 the level
    stacktrace = []
    stack_text = "Pilha: {} \nDesempilhado: {} Símbolo: {}"
    tree: SyntacticTree = None
    
    # create dict with all symbol tables and fills the global scope
    symbol_tables = dict()
    scope_counter = 0
    loop_scope = False
    symbol_table_stack = list()
    symbol_table_stack.append(SymbolTable(scope_counter, loop_scope))

    # auxiliar variables to keep track of identifier info
    aux_type = None
    func_parameter_stack = list()
    prev_symbol = None
    
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
                        Leaf(symbol, token.attribute)
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
                raise SyntacticError.from_data("", msg, index=start, index_end=end)

            next_symbols = table[(current[0], symbol)]
            if tree:
                if current[1][1] == 2:
                    pass
                tree.find_node(current[1][0], current[1][1]).add_node(
                    Node(current[0], next_symbols)
                )
                pass
            else:
                tree = SyntacticTree(current[0], next_symbols)
            for next_symbol in reversed(next_symbols):
                if next_symbol != "&":
                    stack.append([next_symbol, [current[0], current[1][1] + 1]])

            if stack[-1] == symbol:
                tree.find_node(current[0], current[1][1] + 1).add_child(
                    Leaf(symbol, token.attribute)
                )  # check later
                stack.pop()
                break
        
        # if you reach this part of the token loop,
        # there's no syntactic errors, we can put
        # things in the symbol table

        # this simply means the next scope can accept break
        if symbol in ["for", "while"]:
            loop_scope = True
            continue

        # open_curly_bracket means new scope, so we create a new symbol table
        # and put it in the stack, pointing to its father scope
        if symbol == "open_curly_bracket":
            scope_counter += 1
            new_symbol_table = SymbolTable(scope_counter, loop_scope)
            loop_scope = False
            
            # if this is bigger than zero, the next symbol table is from a function
            # so we're including their parameters on the table
            if len(func_parameter_stack) > 0:
                for param_type, param_token in func_parameter_stack:
                    new_symbol_table.insert(param_token)
                    new_symbol_table.insert_additional_info(param_token.attribute, param_type)

            # should always be true, but better be safe
            if (len(symbol_table_stack) > 0):
                father_id = symbol_table_stack[-1].get_id()
                new_symbol_table.set_father(father_id)

            symbol_table_stack.append(new_symbol_table)
            
            # cleaning values
            func_parameter_stack = list()
            aux_type = None
            prev_symbol = None
            continue

        # close_curly_bracket means the scope is done, so we remove it from the stack
        # and put it in the dict using its id as key
        if symbol == "close_curly_bracket":
            pop_symbol_table = symbol_table_stack.pop()
            pop_id = pop_symbol_table.get_id()

            symbol_tables[pop_id] = pop_symbol_table
            continue

        # if we enter this condition, we're going to be declaring
        # a variable, and thus we're saving its type to fill the symbol table later
        if symbol in ["float", "int", "string", "def"] and aux_type == None:
            aux_type = symbol
            continue

        # if we enter this condition, it means we're working with a
        # variable type declaration
        if aux_type in ["float", "int", "string"]:
            # if we have an id, we must put it at the symbol table with its type
            if symbol == "id":
                prev_symbol = token.attribute
                symbol_table_stack[-1].insert(token)
                symbol_table_stack[-1].insert_additional_info(prev_symbol, aux_type)
                continue

            # if its a const, it's just extra info for our id
            if symbol == "const" and prev_symbol is not None:
                symbol_table_stack[-1].insert_additional_info(prev_symbol, symbol)
                aux_type = None
                prev_symbol = None
                continue

            # if the symbol is a semicolon, we're done here
            if symbol == "semicolon":
                aux_type = None
                prev_symbol = None
                continue

        if aux_type in ["def"]:
            # if we have an id, we must put it at the symbol table with its type
            if symbol == "id" and len(func_parameter_stack) == 0:
                prev_symbol = token.attribute
                symbol_table_stack[-1].insert(token)
                symbol_table_stack[-1].insert_additional_info(prev_symbol, aux_type)
                continue

            # if we have a type, now we're handling parameters, so we must save them
            # to put them at the symbol table of the function later
            if symbol in ["float", "int", "string"]:
                func_parameter_stack.append(list())
                func_parameter_stack[-1].append(token.name)
                continue

            # if we have an id, then it's the id after the type above
            if symbol == "id":
                func_parameter_stack[-1].append(token)
                continue

            # those are just the bracket in function def, ignore them
            if symbol in ["open_bracket", "close_bracket", "comma"]:
                continue

        # if we reach this part of the loop, we're not dealing with identifiers anymore
        # so forget everything we've done thus far
        aux_type = None
        prev_symbol = None

    # after processing tokens, we must put the global scope
    # in the dict too
    pop_symbol_table = symbol_table_stack.pop()
    pop_id = pop_symbol_table.get_id()

    symbol_tables[pop_id] = pop_symbol_table

    for n in range(len(symbol_tables)):
        print(symbol_tables[n].get_id(), symbol_tables[n].is_loop_scope(), symbol_tables[n].get_father())
        print(symbol_tables[n])

    return tree, symbol_tables
