from parsero import regex
from parsero.automata import FiniteAutomata, union
from parsero.common.constants import BLANK
from parsero.common.errors import LexicalError
from parsero.common.utils import consume
from parsero.lexical.symbol_table import SymbolTable
from parsero.lexical.token import Token, TokenList


class LexicalAnalyzer:
    def __init__(self, regular_definitions_path):
        self.machine: FiniteAutomata
        self.keyword_machine: FiniteAutomata
        self.keywords: list
        self.token_ids: list
        self._generate_automata(regular_definitions_path)

    def parse(self, path: str) -> tuple[TokenList, dict]:
        """
        Reads a file and returns the token list and a symbol table
        """

        with open(path) as file:
            string = file.read()

        try:
            return self.parse_string(string)
        except LexicalError as error:
            error.filename = path
            raise error

    def parse_string(self, string) -> tuple[TokenList, dict]:
        """
        Reads a string and returns the token list and a symbol table
        """

        # scope counts the number of scopes so far
        # so we can differ the symbol tables for each scope,
        # we also check for for/while statements to know if
        # we're entering a loopable scope
        scope_counter = 0
        next_scope_loop = False
        sym_tables = dict()
        sym_tables_stack = list()

        # putting in the st stack a symbol table with
        # id scope_counter
        sym_tables_stack.append(SymbolTable(scope_counter, next_scope_loop))

        tokens = self.tokenize_string(string)

        # add all tokens into the symbols table
        # as this subject does not consider that, taking it off
        # for word in self.keywords:
        #     sym_table.insert(word, word)

        for token in tokens:
            if token.name == "id":
                sym_tables_stack[-1].insert(token.attribute, token.name)
                continue

            if token.name == "for" or token.name == "while":
                next_scope_loop = True
                continue

            if token.name == "open_curly_bracket":
                scope_counter += 1
                sym_tables_stack.append(SymbolTable(scope_counter, next_scope_loop))

                if next_scope_loop:
                    next_scope_loop = False

                # it looks bad, basically sets the previous scope as father for the newer scope
                if len(sym_tables_stack) > 1:
                    sym_tables_stack[-1].set_father_scope(sym_tables_stack[-2].get_id())

                continue

            if token.name == "close_curly_bracket":
                sym_table = sym_tables_stack.pop()
                sym_tables[sym_table.get_id()] = sym_table

        # after processing tokens, we must put the global scope
        # in the dict too
        sym_table = sym_tables_stack.pop()
        sym_tables[sym_table.get_id()] = sym_table

        for n in range(len(sym_tables)):
            print(sym_tables[n].get_id(), sym_tables[n].is_loop_scope())
            print(sym_tables[n])

        return tokens, sym_tables

    def analyze(self, path: str) -> bool:
        """
        Checks if a file is accepted by the lexical analyzer.
        """

        try:
            self.tokenize(path)
        except LexicalError:
            return False
        else:
            return True

    def analyze_string(self, string: str) -> bool:
        """
        Checks if a string is accepted by the lexical analyzer.
        """

        try:
            self.tokenize_string(string)
        except LexicalError:
            return False
        else:
            return True

    def tokenize(self, path: str) -> TokenList:
        """
        Create tokens for every lexeme recognized in the file.
        """

        try:
            with open(path) as file:
                return self.tokenize_string(file.read())
        except LexicalError as error:
            error.filename = path
            raise error

    def tokenize_string(self, string: str) -> TokenList:
        """
        Create tokens for every lexeme recognized in the string.
        """

        return TokenList(self.make_tokens(string))

    def make_tokens(self, string: str):
        """
        Generator that yields tokens it finds along a string.
        """

        iterator = enumerate(string)
        line = 1
        col = 1

        for i, char in iterator:
            remaining = string[i:]

            keyword, _ = self.keyword_machine.match(remaining)
            lexeme, state_index = self.machine.match(remaining)

            if lexeme > keyword:
                consume(len(lexeme) - 1, iterator)
                tag = self.machine.states[state_index].tag
                yield Token(tag, lexeme, i)
                continue

            if keyword:
                consume(len(keyword) - 1, iterator)
                yield Token(keyword, keyword, i)
                continue

            # it is a bit slow to ignore blank chars this far, but
            # languages like python need tokens for identation or newlines
            # so we cannot ignore spaces before checking
            # the regular definitions
            if char in BLANK:
                continue

            # it should stop before
            msg = f"Invalid expression"
            raise LexicalError.from_data(string, msg, index=i)

    def _generate_automata(self, regular_definitions_path):
        with open(regular_definitions_path) as file:
            expressions, keywords = self._read_regular_definitions(file.read())

        self.keywords = keywords
        self.token_ids = list(expressions.keys())

        # make machines
        machines = []
        for _id, _exp in expressions.items():
            machine = regex.compiles(_exp)
            for state in machine.states:
                if state.is_final:
                    state.tag = _id
            machines.append(machine)

        keyword_machines = []
        for word in keywords:
            machine = regex.compiles(word)
            for state in machine.states:
                if state.is_final:
                    state.tag = word
            keyword_machines.append(machine)

        # determinize machines
        if machines:
            nd_automata = union(*machines)
            self.machine = nd_automata.determinize()
        else:
            self.machine = FiniteAutomata.empty()

        if keyword_machines:
            nd_keyword_automata = union(*keyword_machines)
            self.keyword_machine = nd_keyword_automata.determinize()
        else:
            self.keyword_machine = FiniteAutomata.empty()

    def _read_regular_definitions(self, definitions):
        expressions = dict()
        keywords = []

        tmp_id = []
        for line in definitions.splitlines():
            line = line.strip()
            if not line:
                continue

            line = line.replace("\\n", "\n")

            # support comments
            if line[0] == "#":
                continue

            identifier, expression = line.split(":", 1)  # use only first occurence
            identifier = identifier.strip()
            expression = expression.strip()

            if identifier == expression:
                tmp_id.append(identifier)
                keywords.append(expression)
                continue

            id_size = lambda x: len(x[0])
            for _id, _exp in sorted(expressions.items(), key=id_size, reverse=True):
                replaced = expression.replace(_id, _exp)
                if replaced != expression:
                    tmp_id.append(_id)
                    expression = replaced
            expressions[identifier] = expression

        # if an expression is used inside another it doesn't becomes an automata
        for _id in tmp_id:
            expressions.pop(_id, None)  # if not found ignore

        return expressions, keywords
