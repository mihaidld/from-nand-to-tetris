import re
import sys
from VMWriter import VMWriter
from SymbolTable import SymbolTable

""" Used to test just Symbol table
gets its input from a JackTokenizer and writes its output using the VMWriter
Organized as a series of compile_xxx methods, xxx being a syntactical element 
in the Jack language, one for almost all non-terminal rule xxx 
(except for type, className, subroutineName, varName, statement, subroutineCall)
Out of 21 non-terminal grammar rules, there are 15 compile_xxx methods.
For the 6 remaining, the parsing logic is handled by rules that invoke them

Each compile_xxx method should read xxx from input, advance() the input exactly beyond xxx, 
and emit to the output VM code effecting the semantics of xxx.
We call compile_xxx only if xxx is current syntactic element
If xxx is part of an expression and thus has a value, the emitted VM code
should compute this value and leave it at the top of VM stack"""


class CompilationEngineSymbol:

    def __init__(self, input, output):
        """creates a new compilation engine with given input and output
        Next routine called is compile_class"""
        self.tokenizer = input
        self.target = output
        self.table = SymbolTable()

    def compile_class(self):
        """compiles complete class using 2 loops for
        compile_class_var_dec and compile_subroutine_dec"""
        self.target.write("<class>\n")
        self.__process("class")
        if self.tokenizer.token_type() == self.tokenizer.IDENTIFIER:
            # handle identifier
            self.target.write("<classDef>\n")
            self.__process(self.current_token)
            self.target.write("</classDef>\n")
        else:
            raise ValueError(f"Expected className identifier, got {self.current_token}")
        self.__process("{")

        while True:
            if self.current_token in ["static", "field"]:
                self.compile_class_var_dec()
            else:
                break

        while True:
            if self.current_token in ["constructor", "function", "method"]:
                self.compile_subroutine_dec()
            else:
                break
        self.__process("}")
        self.target.write("</class>\n")

    def compile_class_var_dec(self):
        """compiles a static variable or field declaration
        use a loop for handling all the variable declarations"""
        self.target.write("<classVarDec>\n")
        # already know that current_token is static|field
        kind = self.current_token
        self.__process(self.current_token)
        # self.__handle_type()
        data_type = self.current_token
        if (
            self.current_token in ["int", "char", "boolean"]
            or self.tokenizer.token_type() == self.tokenizer.IDENTIFIER
        ):
            if data_type not in ["int", "char", "boolean"]:
                self.target.write("<classUsage>\n")
            self.__process(self.current_token)
            if data_type not in ["int", "char", "boolean"]:
                self.target.write("</classUsage>\n")
        else:
            raise ValueError(
                f"Expected type int, char, boolean or className identifier, got {self.current_token}"
            )
        name = self.current_token
        if self.tokenizer.token_type() == self.tokenizer.IDENTIFIER:
            # add identifier
            self.table.define(name, data_type, kind)
            index = self.table.index_of(name)
            self.target.write(f"<{kind}{index}Def>\n")
            self.__process(self.current_token)
            self.target.write(f"</{kind}{index}Def>\n")
        else:
            raise ValueError(f"Expected varName identifier, got {self.current_token}")

        while True:
            if self.current_token == ",":
                self.__process(",")
                # self.__handle_var_name()
                name = self.current_token
                if self.tokenizer.token_type() == self.tokenizer.IDENTIFIER:
                    self.table.define(name, data_type, kind)
                    index = self.table.index_of(name)
                    self.target.write(f"<{kind}{index}Def>\n")
                    self.__process(self.current_token)
                    self.target.write(f"</{kind}{index}Def>\n")
                else:
                    raise ValueError(
                        f"Expected varName identifier, got {self.current_token}"
                    )
            else:
                break
        self.__process(";")
        self.target.write("</classVarDec>\n")

    def compile_subroutine_dec(self):
        """compiles a complete method, function or constructor"""
        # start new symbol table for subroutine
        self.table.start_subroutine()
        self.target.write("<subroutineDec>\n")
        # already know that current_token is constructor|function|method
        self.__process(self.current_token)

        if (
            self.current_token in ["int", "char", "boolean", "void"]
            or self.tokenizer.token_type() == self.tokenizer.IDENTIFIER
        ):
            token_type = self.tokenizer.token_type()
            if token_type == self.tokenizer.IDENTIFIER:
                # handle identifier
                self.target.write("<classUsage>\n")
            self.__process(self.current_token)
            if token_type == self.tokenizer.IDENTIFIER:
                # handle identifier
                self.target.write("</classUsage>\n")
        else:
            raise ValueError(
                f"Expected type int, char, boolean, className or void, got {self.current_token}"
            )

        # self.__handle_subroutine_name()
        if self.tokenizer.token_type() == self.tokenizer.IDENTIFIER:
            self.target.write("<subroutineDef>\n")
            self.__process(self.current_token)
            self.target.write("</subroutineDef>\n")
        else:
            raise ValueError(
                f"Expected subroutineName identifier, got {self.current_token}"
            )
        self.__process("(")
        self.compile_parameter_list()
        self.__process(")")
        self.compile_subroutine_body()
        self.target.write("</subroutineDec>\n")

    def compile_parameter_list(self):
        """compiles (possibly empty) parameter list
        Does not handle enclosing '()'"""
        self.target.write("<parameterList>\n")
        # we reach end of parameter list when current token is )
        while self.current_token != ")":
            # handle multiple parameters separated by ,
            if self.current_token == ",":
                self.__process(",")
                continue
            # self.__handle_type()
            if (
                self.current_token in ["int", "char", "boolean"]
                or self.tokenizer.token_type() == self.tokenizer.IDENTIFIER
            ):
                data_type = self.current_token
                token_type = self.tokenizer.token_type()
                if token_type == self.tokenizer.IDENTIFIER:
                    # handle identifier
                    self.target.write("<classUsage>\n")
                self.__process(self.current_token)
                if token_type == self.tokenizer.IDENTIFIER:
                    # handle identifier
                    self.target.write("</classUsage>\n")
            else:
                raise ValueError(
                    f"Expected type int, char, boolean or className identifier, got {self.current_token}"
                )
            # self.__handle_var_name()
            if self.tokenizer.token_type() == self.tokenizer.IDENTIFIER:
                name = self.current_token
                kind = "arg"
                self.table.define(name, data_type, kind)
                index = self.table.index_of(name)
                self.target.write(f"<{kind}{index}Def>\n")
                self.__process(self.current_token)
                self.target.write(f"</{kind}{index}Def>\n")
            else:
                raise ValueError(
                    f"Expected varName identifier, got {self.current_token}"
                )
        self.target.write("</parameterList>\n")

    def compile_subroutine_body(self):
        """compiles subroutine's body"""
        self.target.write("<subroutineBody>\n")
        self.__process("{")
        while self.current_token == "var":
            self.compile_var_dec()
        self.compile_statements()
        self.__process("}")
        self.target.write("</subroutineBody>\n")

    def compile_var_dec(self):
        """compiles a var declaration'"""
        self.target.write("<varDec>\n")
        # already know that current_token is var
        self.__process(self.current_token)
        # self.__handle_type()
        if (
            self.current_token in ["int", "char", "boolean"]
            or self.tokenizer.token_type() == self.tokenizer.IDENTIFIER
        ):
            data_type = self.current_token
            token_type = self.tokenizer.token_type()
            if token_type == self.tokenizer.IDENTIFIER:
                # handle identifier
                self.target.write("<classUsage>\n")
            self.__process(self.current_token)
            if token_type == self.tokenizer.IDENTIFIER:
                # handle identifier
                self.target.write("</classUsage>\n")
        else:
            raise ValueError(
                f"Expected type int, char, boolean or className identifier, got {self.current_token}"
            )
        # self.__handle_var_name()
        if self.tokenizer.token_type() == self.tokenizer.IDENTIFIER:
            name = self.current_token
            kind = "local"
            self.table.define(name, data_type, kind)
            index = self.table.index_of(name)
            self.target.write(f"<{kind}{index}Def>\n")
            self.__process(self.current_token)
            self.target.write(f"</{kind}{index}Def>\n")
        else:
            raise ValueError(f"Expected varName identifier, got {self.current_token}")
        while self.current_token == ",":
            self.__process(",")
            # self.__handle_var_name()
            if self.tokenizer.token_type() == self.tokenizer.IDENTIFIER:
                name = self.current_token
                self.table.define(name, data_type, kind)
                index = self.table.index_of(name)
                self.target.write(f"<{kind}{index}Def>\n")
                self.__process(self.current_token)
                self.target.write(f"</{kind}{index}Def>\n")
            else:
                raise ValueError(
                    f"Expected varName identifier, got {self.current_token}"
                )
        self.__process(";")
        self.target.write("</varDec>\n")

    def compile_statements(self):
        """compiles a sequence of statements
        Does not handle enclosing '{}'
        Uses loop to handle 0 or more statement, then
        invokes specific compile_if etc. depending of left-most token ('if')"""
        self.target.write("<statements>\n")
        while self.current_token in ["if", "let", "while", "do", "return"]:
            if self.current_token == "if":
                self.compile_if()
            elif self.current_token == "let":
                self.compile_let()
            elif self.current_token == "while":
                self.compile_while()
            elif self.current_token == "do":
                self.compile_do()
            elif self.current_token == "return":
                self.compile_return()
        self.target.write("</statements>\n")

    def compile_let(self):
        """compiles a let statement"""
        self.target.write("<letStatement>\n")
        self.__process("let")
        # self.__handle_var_name()
        if self.tokenizer.token_type() == self.tokenizer.IDENTIFIER:
            # lookup variable
            name = self.current_token
            kind = self.table.kind_of(name)
            if kind is not SymbolTable.NONE:
                data_type = self.table.type_of(name)
                index = self.table.index_of(name)
                self.target.write(f"<{kind}{index}Usage>\n")
            else:
                self.target.write("<classUsage>\n")
            self.__process(self.current_token)
            if kind is not SymbolTable.NONE:
                data_type = self.table.type_of(name)
                index = self.table.index_of(name)
                self.target.write(f"</{kind}{index}Usage>\n")
            else:
                self.target.write("</classUsage>\n")
        else:
            raise ValueError(f"Expected varName identifier, got {self.current_token}")
        if self.current_token == "[":
            self.__process("[")
            self.compile_expression()
            self.__process("]")
        self.__process("=")
        self.compile_expression()
        self.__process(";")
        self.target.write("</letStatement>\n")

    def compile_if(self):
        """compiles an if statement, possibly with trailing else clause"""
        self.target.write("<ifStatement>\n")
        self.__process("if")
        self.__process("(")
        self.compile_expression()
        self.__process(")")
        self.__process("{")
        self.compile_statements()
        self.__process("}")
        # optional else clause
        if self.current_token == "else":
            self.__process("else")
            self.__process("{")
            self.compile_statements()
            self.__process("}")
        self.target.write("</ifStatement>\n")

    def compile_while(self):
        """compiles a while statement
        Should be called if current token is 'while'"""
        self.target.write("<whileStatement>\n")
        self.__process("while")
        self.__process("(")
        self.compile_expression()
        self.__process(")")
        self.__process("{")
        self.compile_statements()
        self.__process("}")
        self.target.write("</whileStatement>\n")

    def compile_do(self):
        """compiles do statement"""
        self.target.write("<doStatement>\n")
        self.__process("do")

        # do subroutineCall statement parsed as if their syntax were do expression
        # wraps subroutineCall with <expression><term> ... </term></expression>
        # self.compile_expression()

        if self.tokenizer.token_type() == self.tokenizer.IDENTIFIER:
            # look ahead
            current = self.current_token
            self.tokenizer.advance()
            token_ahead = self.tokenizer.current_token[1]
            self.target.write(f"<identifier> {current} </identifier>\n")

            # subroutineCall: subroutineName '(' expressionList ')'
            if token_ahead == "(":
                self.target.write(
                    f"<subroutineUsage>\n<identifier> {current} </identifier>\n</subroutineUsage>\n"
                )
                self.__process("(")
                self.compile_expression_list()
                self.__process(")")

            # subroutineCall: className|varName '.' subroutineName '(' expressionList ')'
            elif token_ahead == ".":
                # check is current is either instance of class (in table) or class
                kind = self.table.kind_of(current)
                if kind is not SymbolTable.NONE:
                    index = self.table.index_of(current)
                    self.target.write(
                        f"<{kind}{index}Usage>\n<identifier> {current} </identifier>\n</{kind}{index}Usage>\n"
                    )
                else:
                    # must be class
                    self.target.write(
                        f"<classUsage>\n<identifier> {current} </identifier>\n</classUsage>\n"
                    )
                self.__process(".")
                # self.__handle_subroutine_name()
                if self.tokenizer.token_type() == self.tokenizer.IDENTIFIER:
                    self.target.write("<subroutineUsage>\n")
                    self.__process(self.current_token)
                    self.target.write("</subroutineUsage>\n")
                else:
                    raise ValueError(
                        f"Expected subroutineName identifier, got {self.current_token}"
                    )
                self.__process("(")
                self.compile_expression_list()
                self.__process(")")
        else:
            raise ValueError(
                f"Expected subroutineName|className|varName identifier, got {self.current_token}"
            )

        self.__process(";")
        self.target.write("</doStatement>\n")

    def compile_return(self):
        """compiles a return statement"""
        self.target.write("<returnStatement>\n")
        self.__process("return")
        # optional expression
        if self.current_token != ";":
            self.compile_expression()
        self.__process(";")
        self.target.write("</returnStatement>\n")

    def compile_expression(self):
        """compiles an expression"""
        self.target.write("<expression>\n")
        self.compile_term()
        # optional pair op term
        if self.current_token in [
            "+",
            "-",
            "*",
            "/",
            "&amp;",
            "|",
            "&lt;",
            "&gt;",
            "=",
        ]:
            self.__process(self.current_token)
            self.compile_term()
        self.target.write("</expression>\n")

    def compile_term(self):
        """compiles a term
        If current token is identifier, must distinguish between variable,
        an array entry, or a subroutine call.
        term: integerConstant|stringConstant|keywordConstant|
        '(' expression ')'| unaryOp term |
        varName|varName '[' expression ']'|subroutineCall
        A single look-ahead token, which may be one of '[', '(' or '.'
        suffices to distinguish between the possibilities.
        Any other token is not part of this term and should not be advanced over."""
        self.target.write("<term>\n")
        # '(' expression ')'
        if self.current_token == "(":
            self.__process("(")
            self.compile_expression()
            self.__process(")")
        # unaryOp term
        elif self.current_token in ["-", "~"]:
            self.__process(self.current_token)
            self.compile_term()
        # integerConstant|stringConstant|keywordConstant
        elif self.tokenizer.token_type() in [
            self.tokenizer.INT_CONST,
            self.tokenizer.STRING_CONST,
            self.tokenizer.KEYWORD,
        ]:
            self.__process(self.current_token)
        # identifier
        elif self.tokenizer.token_type() == self.tokenizer.IDENTIFIER:
            # look ahead
            current = self.current_token
            self.tokenizer.advance()
            token_ahead = self.tokenizer.current_token[1]
            # self.target.write(f"<identifier> {current} </identifier>\n")

            # varName '[' expression ']'
            if token_ahead == "[":
                kind = self.table.kind_of(current)
                if kind is not SymbolTable.NONE:
                    index = self.table.index_of(current)
                    self.target.write(
                        f"<{kind}{index}Usage>\n<identifier> {current} </identifier>\n</{kind}{index}Usage>\n"
                    )
                else:
                    raise ValueError(f"Undefined: {current}")
                self.__process("[")
                self.compile_expression()
                self.__process("]")

            # subroutineCall: subroutineName '(' expressionList ')'
            elif token_ahead == "(":
                self.target.write(
                    f"<subroutineUsage>\n<identifier> {current} </identifier>\n</subroutineUsage>\n"
                )
                self.__process("(")
                self.compile_expression_list()
                self.__process(")")

            # subroutineCall: className|varName '.' subroutineName '(' expressionList ')'
            elif token_ahead == ".":
                # check is current is either instance of class (in table) or class
                kind = self.table.kind_of(current)
                if kind is not SymbolTable.NONE:
                    index = self.table.index_of(current)
                    self.target.write(
                        f"<{kind}{index}Usage>\n<identifier> {current} </identifier>\n</{kind}{index}Usage>\n"
                    )
                else:
                    # must be class
                    self.target.write(
                        f"<classUsage>\n<identifier> {current} </identifier>\n</classUsage>\n"
                    )
                self.__process(".")
                # self.__handle_subroutine_name()
                if self.tokenizer.token_type() == self.tokenizer.IDENTIFIER:
                    self.target.write("<subroutineUsage>\n")
                    self.__process(self.current_token)
                    self.target.write("</subroutineUsage>\n")
                else:
                    raise ValueError(
                        f"Expected subroutineName identifier, got {self.current_token}"
                    )
                self.__process("(")
                self.compile_expression_list()
                self.__process(")")
            # varName
            # Any other token is not part of this term and should not be advanced over.
            else:
                kind = self.table.kind_of(current)
                if kind is not SymbolTable.NONE:
                    index = self.table.index_of(current)
                    self.target.write(
                        f"<{kind}{index}Usage>\n<identifier> {current} </identifier>\n</{kind}{index}Usage>\n"
                    )
                else:
                    raise ValueError(f"Undefined: {current}")
                self.current_token = token_ahead

        self.target.write("</term>\n")

    def compile_expression_list(self) -> int:
        """compiles (possibly empty) comma-separated list of expressions
        Returns the number of expressions in the list"""
        self.target.write("<expressionList>\n")
        # at least one expression as argument
        counter_expressions = 0
        if self.current_token != ")":
            self.compile_expression()
            counter_expressions += 1
        # optional multiple expressions separated by ,
        while self.current_token == ",":
            self.__process(",")
            self.compile_expression()
            counter_expressions += 1
        self.target.write("</expressionList>\n")

        return counter_expressions

    def __handle_type(self):
        if (
            self.current_token in ["int", "char", "boolean"]
            or self.tokenizer.token_type() == self.tokenizer.IDENTIFIER
        ):
            self.__process(self.current_token)
        else:
            raise ValueError(
                f"Expected type int, char, boolean or className identifier, got {self.current_token}"
            )

    def __handle_var_name(self):
        if self.tokenizer.token_type() == self.tokenizer.IDENTIFIER:
            self.__process(self.current_token)
        else:
            raise ValueError(f"Expected varName identifier, got {self.current_token}")

    def __handle_subroutine_name(self):
        if self.tokenizer.token_type() == self.tokenizer.IDENTIFIER:
            self.__process(self.current_token)
        else:
            raise ValueError(
                f"Expected subroutineName identifier, got {self.current_token}"
            )

    def __process(self, token: str):
        """helper routine that handles current token,
        and advances to get the next token"""
        # expect to see token
        if self.tokenizer.current_token[1] == token:
            self.__write_xml_token(token)
        else:
            raise ValueError(f"Expected {self.tokenizer.current_token[1]}, got {token}")
        # gets next token, advance the input
        self.tokenizer.advance()
        if self.tokenizer.current_token:
            self.current_token = self.tokenizer.current_token[1]
        # reached EOF
        else:
            self.current_token = None

    def __write_xml_token(self, token: str):
        """helper routine that writes XML for current token
        e.g.<keyword> while </keyword>
        or <symbol> + </symbol>"""
        tag = self.tokenizer.token_type()
        self.target.write(f"<{tag}> {token} </{tag}>\n")
