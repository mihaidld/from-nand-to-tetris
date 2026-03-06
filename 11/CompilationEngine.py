from VMWriter import VMWriter
from SymbolTable import SymbolTable

"""gets its input from a JackTokenizer and writes its output using the VMWriter
Organized as a series of compile_xxx methods, xxx being a syntactical element 
in the Jack language, one for almost all non-terminal rule xxx 
(except for type, className, subroutineName, varName, statement, subroutineCall)
Out of 21 non-terminal grammar rules, there are 15 compile_xxx methods.
For the 6 remaining, the parsing logic is handled by rules that invoke them

Each compile_xxx method should read xxx from input, 
advance() the input exactly beyond xxx, 
and emit to the output VM code effecting the semantics of xxx.
We call compile_xxx only if xxx is current syntactic element
If xxx is part of an expression and thus has a value, the emitted VM code
should compute this value and leave it at the top of VM stack"""


class CompilationEngine:
    binary_operators = {
        "+": "add",
        "-": "sub",
        "&": "and",
        "|": "or",
        "<": "lt",
        ">": "gt",
        "=": "eq",
    }
    binary_operators_special = {"*": ("Math.multiply", 2), "/": ("Math.divide", 2)}
    unary_operators = {"-": "neg", "~": "not"}
    # counter for unique labels in if and while statements L1_counter, L2_counter
    counter_labels = 0

    def __init__(self, input, output):
        """creates a new compilation engine with given tokenizer input
        and output file handler
        Next routine called is compile_class"""
        self.tokenizer = input
        self.target = output  # used for writing comments to vm file
        self.table = SymbolTable()
        self.writer = VMWriter(output)
        self.class_name = None  # store current class to be compiled

    def compile_class(self):
        """compiles complete class using 2 loops for
        compile_class_var_dec and compile_subroutine_dec"""
        self.target.write("// compile_class\n")
        self.__process("class")
        if self.tokenizer.token_type() == self.tokenizer.IDENTIFIER:
            # set class name for naming functions
            self.class_name = self.current_token
            self.__process(self.current_token)
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

    def compile_class_var_dec(self):
        """compiles a static variable or field declaration
        use a loop for handling all the variable declarations"""
        self.target.write("// compile_class_var_dec\n")
        # already know that current_token is static|field
        if self.current_token == "static":
            kind = SymbolTable.STATIC
        else:
            kind = SymbolTable.FIELD
        self.__process(self.current_token)
        # handle variable type
        if (
            self.current_token in ["int", "char", "boolean"]
            or self.tokenizer.token_type() == self.tokenizer.IDENTIFIER
        ):
            data_type = self.current_token
            self.__process(self.current_token)
        else:
            raise ValueError(
                f"Expected type int, char, boolean or className identifier, got {self.current_token}"
            )

        if self.tokenizer.token_type() == self.tokenizer.IDENTIFIER:
            # add identifier to symbol table
            name = self.current_token
            self.table.define(name, data_type, kind)
            self.__process(self.current_token)
        else:
            raise ValueError(f"Expected varName identifier, got {self.current_token}")

        while True:
            if self.current_token == ",":
                self.__process(",")
                # add identifier to symbol table
                if self.tokenizer.token_type() == self.tokenizer.IDENTIFIER:
                    name = self.current_token
                    self.table.define(name, data_type, kind)
                    self.__process(self.current_token)
                else:
                    raise ValueError(
                        f"Expected varName identifier, got {self.current_token}"
                    )
            else:
                break
        self.__process(";")

    def compile_subroutine_dec(self):
        """compiles a complete method, function or constructor"""
        self.target.write(f"// compile_subroutine_dec type {self.current_token}\n")
        # start new symbol table for subroutine
        self.table.start_subroutine()

        # already know that current_token is constructor|function|method
        function_type = self.current_token
        self.__process(self.current_token)

        # handle return type
        if (
            self.current_token in ["int", "char", "boolean", "void"]
            or self.tokenizer.token_type() == self.tokenizer.IDENTIFIER
        ):
            self.__process(self.current_token)
        else:
            raise ValueError(
                f"Expected type int, char, boolean, className or void, got {self.current_token}"
            )

        if self.tokenizer.token_type() == self.tokenizer.IDENTIFIER:
            function_name = f"{self.class_name}.{self.current_token}"
            self.__process(self.current_token)
        else:
            raise ValueError(
                f"Expected subroutineName identifier, got {self.current_token}"
            )

        self.__process("(")
        # if method set this as arg 0
        if function_type == "method":
            self.table.define("this", self.class_name, SymbolTable.ARG)
        # add function arguments to symbol table
        self.compile_parameter_list()
        self.__process(")")
        # pass function name and type information to its body
        # for code generation
        self.compile_subroutine_body(function_name, function_type)

    def compile_parameter_list(self):
        """compiles (possibly empty) parameter list
        Does not handle enclosing '()'"""
        self.target.write("// compile_parameter_list\n")
        # we reach end of parameter list when current token is )
        while self.current_token != ")":
            # handle multiple parameters separated by ,
            if self.current_token == ",":
                self.__process(",")
                continue
            if (
                self.current_token in ["int", "char", "boolean"]
                or self.tokenizer.token_type() == self.tokenizer.IDENTIFIER
            ):
                data_type = self.current_token
                self.__process(self.current_token)
            else:
                raise ValueError(
                    f"Expected type int, char, boolean or className identifier, got {self.current_token}"
                )
            if self.tokenizer.token_type() == self.tokenizer.IDENTIFIER:
                name = self.current_token
                kind = SymbolTable.ARG
                self.table.define(name, data_type, kind)
                self.__process(self.current_token)
            else:
                raise ValueError(
                    f"Expected varName identifier, got {self.current_token}"
                )

    def compile_subroutine_body(self, function_name: str, function_type: str):
        """compiles subroutine's body
        needs to be given function name and type since needs to declare function
        after computing number of local variables"""
        self.target.write("// compile_subroutine_body\n")
        self.__process("{")

        # declare local variables and compute their number
        n_locals = 0
        while self.current_token == "var":
            n_locals += self.compile_var_dec()

        self.writer.write_function(function_name, n_locals)

        # handle constructor memory allocation
        if function_type == "constructor":
            # consults class-level symbol table for # of fields
            n_fields = self.table.var_count(SymbolTable.FIELD)
            self.writer.write_push(VMWriter.CONST, n_fields)
            # searches for free space for n_fields words and returns base address
            self.writer.write_call("Memory.alloc", 1)
            # anchors this at base address
            self.writer.write_pop(VMWriter.POINTER, 0)
        elif function_type == "method":
            # retrieves this from argument 0
            self.writer.write_push(SymbolTable.ARG, 0)
            # anchors this at base address
            self.writer.write_pop(VMWriter.POINTER, 0)
        self.compile_statements()
        self.__process("}")

    def compile_var_dec(self) -> int:
        """compiles a var declaration and
        returns number of local variables for function declaration"""
        self.target.write("// compile_var_dec\n")
        # already know that current_token is var
        self.__process(self.current_token)

        n_locals = 0
        if (
            self.current_token in ["int", "char", "boolean"]
            or self.tokenizer.token_type() == self.tokenizer.IDENTIFIER
        ):
            data_type = self.current_token
            self.__process(self.current_token)
        else:
            raise ValueError(
                f"Expected type int, char, boolean or className identifier, got {self.current_token}"
            )

        if self.tokenizer.token_type() == self.tokenizer.IDENTIFIER:
            name = self.current_token
            kind = SymbolTable.LOCAL
            self.table.define(name, data_type, kind)
            self.__process(self.current_token)
            n_locals += 1  # increment # local variables
        else:
            raise ValueError(f"Expected varName identifier, got {self.current_token}")
        # handle remaining var variables same data type on same line
        while self.current_token == ",":
            self.__process(",")
            if self.tokenizer.token_type() == self.tokenizer.IDENTIFIER:
                name = self.current_token
                self.table.define(name, data_type, kind)
                self.__process(self.current_token)
                n_locals += 1  # increment # local variables
            else:
                raise ValueError(
                    f"Expected varName identifier, got {self.current_token}"
                )
        self.__process(";")
        return n_locals

    def compile_statements(self):
        """compiles a sequence of statements
        Does not handle enclosing '{}'
        Uses loop to handle 0 or more statement, then
        invokes specific compile_if etc. depending of left-most token ('if')"""
        self.target.write("// compile_statements\n")
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

    def compile_let(self):
        """compiles a let statement"""
        self.target.write("// compile_let\n")
        self.__process("let")
        if self.tokenizer.token_type() == self.tokenizer.IDENTIFIER:
            # lookup variable and remember it
            name = self.current_token
            kind = self.table.kind_of(name)
            if kind is not SymbolTable.NONE:
                index = self.table.index_of(name)
            self.__process(self.current_token)
        else:
            raise ValueError(f"Expected varName identifier, got {self.current_token}")

        # handle optional array element assignment
        array_assignment = False
        if self.current_token == "[":
            array_assignment = True
        if array_assignment:
            self.__process("[")
            # push arr
            self.writer.write_push(kind, index)
            # compute exp for array index
            self.compile_expression()
            # add arr + expression
            self.writer.write_arithmetic("add")
            self.__process("]")
        self.__process("=")

        # compute exp to be assigned
        self.compile_expression()

        if array_assignment:
            # save value of expression to be assigned in temp 0
            self.writer.write_pop(VMWriter.TEMP, 0)
            # align THAT segment with arr + expression
            self.writer.write_pop(VMWriter.POINTER, 1)
            # retrieve value of expression to be assigned from temp 0
            self.writer.write_push(VMWriter.TEMP, 0)
            # assign it arr[expression] which is that 0
            self.writer.write_pop(VMWriter.THAT, 0)
        else:
            # no array assignment, just pop into varName
            self.writer.write_pop(kind, index)
        self.__process(";")

    def compile_if(self):
        """compiles an if statement, possibly with trailing else clause"""
        self.target.write("// compile_if\n")
        # increment counter to ensure unique couple L1, L2 in case of nesting
        self.counter_labels += 1
        current_counter = self.counter_labels
        self.__process("if")
        self.__process("(")
        self.compile_expression()
        self.__process(")")
        self.writer.write_arithmetic("not")
        self.writer.write_if(f"{self.class_name}_L1_{current_counter}")
        self.__process("{")
        self.compile_statements()
        self.writer.write_goto(f"{self.class_name}_L2_{current_counter}")
        self.__process("}")
        self.writer.write_label(f"{self.class_name}_L1_{current_counter}")
        # optional else clause
        if self.current_token == "else":
            self.__process("else")
            self.__process("{")
            self.compile_statements()
            self.__process("}")
        self.writer.write_label(f"{self.class_name}_L2_{current_counter}")

    def compile_while(self):
        """compiles a while statement
        Should be called if current token is 'while'"""
        self.target.write("// compile_while\n")
        # increment counter to ensure unique couple L1, L2 in case of nesting
        self.counter_labels += 1
        current_counter = self.counter_labels
        self.__process("while")
        self.__process("(")
        self.writer.write_label(f"{self.class_name}_L1_{current_counter}")
        self.compile_expression()
        self.__process(")")
        self.writer.write_arithmetic("not")
        self.writer.write_if(f"{self.class_name}_L2_{current_counter}")
        self.__process("{")
        self.compile_statements()
        self.__process("}")
        self.writer.write_goto(f"{self.class_name}_L1_{current_counter}")
        self.writer.write_label(f"{self.class_name}_L2_{current_counter}")

    def compile_do(self):
        """compiles do statement"""
        self.target.write("// compile_do\n")
        self.__process("do")
        # handle subroutine call like an expression
        self.compile_expression()
        # get rid of the topmost stack element (the expression’s value)
        self.writer.write_pop(VMWriter.TEMP, 0)
        self.__process(";")

    def compile_return(self):
        """compiles a return statement"""
        self.target.write("// compile_return\n")
        self.__process("return")
        # compile optional expression first which places value on stack
        if self.current_token != ";":
            self.compile_expression()
        # no return value so place dummy value on top of stack
        else:
            self.writer.write_push(VMWriter.CONST, 0)
        self.writer.write_return()
        self.__process(";")

    def compile_expression(self):
        """compiles an expression according to grammar
        expression: term (op term)*"""
        self.target.write("// compile_expression\n")
        self.compile_term()

        # optional multiple terms separated by op
        while (
            self.current_token in CompilationEngine.binary_operators
            or self.current_token in CompilationEngine.binary_operators_special
        ):
            # remember op to use after term in order to
            # change from infix to postfix operator notation
            op = self.current_token
            self.__process(self.current_token)

            self.compile_term()
            self.__compile_op(op)

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
        self.target.write("// compile_term\n")

        # '(' expression ')'
        if self.current_token == "(":
            self.__process("(")
            self.compile_expression()
            self.__process(")")

        # unaryOp term
        elif self.current_token in CompilationEngine.unary_operators:
            op = self.current_token  # remember op
            self.__process(self.current_token)
            self.compile_term()
            # from prefix to postfix
            self.writer.write_arithmetic(CompilationEngine.unary_operators[op])

        # keywordConstant
        elif self.tokenizer.token_type() == self.tokenizer.KEYWORD:
            if self.current_token in ["null", "false"]:
                self.writer.write_push(VMWriter.CONST, 0)
            elif self.current_token == "true":
                self.writer.write_push(VMWriter.CONST, 1)
                self.writer.write_arithmetic("neg")
            # case this
            elif self.current_token == "this":
                self.writer.write_push(VMWriter.POINTER, 0)
            self.__process(self.current_token)

        # integerConstant
        elif self.tokenizer.token_type() == self.tokenizer.INT_CONST:
            self.writer.write_push(VMWriter.CONST, self.current_token)
            self.__process(self.current_token)

        # stringConstant
        elif self.tokenizer.token_type() == self.tokenizer.STRING_CONST:
            self.__compile_string(self.current_token)
            self.__process(self.current_token)

        # identifier
        elif self.tokenizer.token_type() == self.tokenizer.IDENTIFIER:
            # look ahead
            current = self.current_token
            self.tokenizer.advance()
            token_ahead = self.tokenizer.current_token[1]

            # varName '[' expression ']'
            if token_ahead == "[":
                kind = self.table.kind_of(current)
                if kind is not SymbolTable.NONE:
                    index = self.table.index_of(current)
                else:
                    raise ValueError(f"Undefined: {current}")
                self.__process("[")
                # varName is Array so set THAT to (arr + expression)
                self.writer.write_push(kind, index)
                self.compile_expression()
                # expression added on top of stack
                self.writer.write_arithmetic("add")
                # align THAT segment to (arr + expressio)
                self.writer.write_pop(VMWriter.POINTER, 1)
                # push 1st value from that segment
                self.writer.write_push(VMWriter.THAT, 0)
                self.__process("]")

            # subroutineCall: subroutineName '(' expressionList ')'
            elif token_ahead == "(":
                # must be method call applied to current object
                # with reference stored in THIS (RAM[3] or pointer 0)
                self.__process("(")
                # place this on stack as arg 0
                self.writer.write_push(VMWriter.POINTER, 0)
                # place remaining expressions arguments
                nb_args = self.compile_expression_list()
                self.__process(")")
                nb_args += 1
                self.writer.write_call(f"{self.class_name}.{current}", nb_args)

            # subroutineCall: className|varName '.' subroutineName '(' expressionList ')'
            elif token_ahead == ".":
                # check if current is either instance of class (in table) or class
                instance = None
                kind = self.table.kind_of(current)
                if kind is not SymbolTable.NONE:
                    index = self.table.index_of(current)
                    class_name = self.table.type_of(current)
                    instance = (kind, index)
                # must be class
                else:
                    class_name = current

                self.__process(".")
                if self.tokenizer.token_type() == self.tokenizer.IDENTIFIER:
                    subroutine_name = f"{class_name}.{self.current_token}"
                    self.__process(self.current_token)
                else:
                    raise ValueError(
                        f"Expected subroutineName identifier, got {self.current_token}"
                    )
                self.__process("(")
                # if method push base address on stack as arg 0
                if instance:
                    self.writer.write_push(instance[0], instance[1])
                nb_args = self.compile_expression_list()
                self.__process(")")
                # if method increment n_args
                if instance:
                    nb_args += 1
                self.writer.write_call(subroutine_name, nb_args)

            # varName
            # Any other token is not part of this term and should not be advanced over.
            else:
                kind = self.table.kind_of(current)
                if kind is not SymbolTable.NONE:
                    index = self.table.index_of(current)
                    self.writer.write_push(kind, index)
                else:
                    raise ValueError(f"Undefined: {current}")
                self.current_token = token_ahead

    def compile_expression_list(self) -> int:
        """compiles (possibly empty) comma-separated list of expressions
        Returns the number of expressions in the list"""
        self.target.write("// compile_expression_list\n")
        counter_expressions = 0

        # at least one expression as argument
        if self.current_token != ")":
            self.compile_expression()
            counter_expressions += 1

        # optional multiple expressions separated by ,
        while self.current_token == ",":
            self.__process(",")
            self.compile_expression()
            counter_expressions += 1

        return counter_expressions

    def __process(self, token: str):
        """helper routine that checks current token against
        expected grammar rules,
        and advances to get the next token and
        set it as current token"""
        # expect to see token
        if self.tokenizer.current_token[1] != token:
            raise ValueError(f"Expected {self.tokenizer.current_token[1]}, got {token}")
        # gets next token, advance the input
        self.tokenizer.advance()
        if self.tokenizer.current_token:
            self.current_token = self.tokenizer.current_token[1]
        # reached EOF
        else:
            self.current_token = None

    def __compile_op(self, op: str):
        """helper routine to write VM code for operators"""
        if op in CompilationEngine.binary_operators:
            self.writer.write_arithmetic(CompilationEngine.binary_operators[op])
        else:
            name, n_args = CompilationEngine.binary_operators_special[op]
            self.writer.write_call(name, n_args)

    def __compile_string(self, word: str):
        """helper routine to write VM code for strings"""
        length = len(word)
        self.writer.write_push(VMWriter.CONST, length)  # push length
        # call String.new  with length argument
        # returns base address placed on top of stack
        self.writer.write_call("String.new", 1)
        # sequence of calls to the String method appendChar
        # each call String.appendChar returns base address on top of stack
        for char in word:
            self.writer.write_push(VMWriter.CONST, ord(char))  # int(char)
            self.writer.write_call("String.appendChar", 2)
