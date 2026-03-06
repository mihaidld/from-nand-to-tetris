import sys

"""handles the compiler's input:
ignores all comments and whitespace in the input stream and
serializes it into Jack-language tokens.
The token types are specified according to the Jack grammar
advances the input one token at a time
getting the value and type of current token


To allow viewing XML using browsers it wraps up content 
between <tokens> </tokens> tags and
replaces < with &lt; , > with &gt; , " with &quot; , & with &amp;
Each token is written <type>value</type>
e.g <tokens>
<keyword>if</keyword>
<symbol>(<symbol>
...
</tokens>
"""


class JackTokenizer:
    """reads from input characters and groups them into meaningfull tokens"""

    (KEYWORD, SYMBOL, IDENTIFIER, INT_CONST, STRING_CONST) = range(5)
    (
        CLASS,
        METHOD,
        FUNCTION,
        CONSTRUCTOR,
        INT,
        BOOLEAN,
        CHAR,
        VOID,
        VAR,
        STATIC,
        FIELD,
        LET,
        DO,
        IF,
        ELSE,
        WHILE,
        RETURN,
        TRUE,
        FALSE,
        NULL,
        THIS,
    ) = range(21)
    tags = ["keyword", "symbol", "identifier", "integerConstant", "stringConstant"]
    keywords = [
        "class",
        "method",
        "function",
        "constructor",
        "int",
        "boolean",
        "char",
        "void",
        "var",
        "static",
        "field",
        "let",
        "do",
        "if",
        "else",
        "while",
        "return",
        "true",
        "false",
        "null",
        "this",
    ]
    symbols = [
        "{",
        "}",
        "[",
        "]",
        "(",
        ")",
        ".",
        ",",
        ";",
        "+",
        "-",
        "*",
        "/",
        "&",
        "|",
        "<",
        ">",
        "=",
        "~",
    ]
    min_int = 0
    max_int = 32767
    # pattern_identifier = r"^[A-Za-z_][A-Za-z0-9_]*$"
    # pattern_string = r"[^\"\n]*"
    replacements = {"<": "&lt;", ">": "&gt;", '"': "&quot;", "&": "&amp;"}

    def __init__(self, filename):
        """opens the input .jack file and gets ready to tokenize it"""
        self.source = open(filename, "r")  # Open file for read
        if not self.source:
            print(f"Could not open {filename}")
            sys.exit(1)

        # tuple (<token type>, <token value>)
        self.current_token = None
        self.char_ahead = None

    # def has_more_tokens(self) -> bool:
    #     """are there more tokens in the input?"""
    #     pass

    def advance(self):
        """gets the next token from input and makes it the current token
        Should be called only if has_more_tokens is true
        Initially there is no current token"""
        while True:
            # Read new character from a file if not already read into char ahead
            if not self.char_ahead:
                current = self.source.read(1)
            else:
                current = self.char_ahead  # consume char ahead
                self.char_ahead = None

            """If the stream is already at EOF, an empty string is returned"""
            if not current:
                self.close()
                self.current_token = None
                return

            """Process the character
            Handle comments and whitespace -> ignore whitespace and everything after // or
            between /*[*] */"""
            if current.isspace():
                continue  # skip whitespace

            if current == "/":
                # need to look ahead
                current += self.source.read(1)
                # ignore line-comment till end of line
                if current == "//":
                    self.source.readline()
                    continue
                # ignore comments block /*[*] */
                elif current == "/*":
                    # read more chars looking for comment block ending */
                    current += self.source.read(2)
                    while not current.endswith("*/"):
                        current += self.source.read(1)
                    continue
                # must be division symbol
                else:
                    self.current_token = (self.SYMBOL, "/")
                    self.char_ahead = current[-1]  # store last char in char ahead
                    return

            # symbol
            if current in self.symbols:
                if current in self.replacements:
                    self.current_token = (self.SYMBOL, self.replacements[current])
                else:
                    self.current_token = (self.SYMBOL, current)
                return

            # string_constant
            if current == '"':
                current = self.source.read(1)  # ignore starting "
                while not current.endswith('"'):
                    current += self.source.read(1)
                self.current_token = (
                    self.STRING_CONST,
                    current[:-1],
                )  # ignore ending "
                return

            # int_constant
            if current.isdigit():
                while current.isdigit():
                    current += self.source.read(1)
                int_val = int(current[:-1])  # ignore ending not digit
                self.current_token = (self.INT_CONST, int_val)
                self.char_ahead = current[-1]  # store last char in char ahead
                if self.min_int <= int_val <= self.max_int:
                    return
                else:
                    print(
                        f"Integer numbers must be between {self.min_int} and {self.max_int}"
                    )
                    sys.exit(1)

            # keyword or identifier delimited to the right by whitespace or symbol
            elif current.isalpha() or current == "_":
                while current[-1] not in self.symbols and not current[-1].isspace():
                    current += self.source.read(1)
                self.char_ahead = current[-1]  # store last char in char ahead
                current = current[:-1]
                # keyword
                if current in self.keywords:
                    self.current_token = (self.KEYWORD, current)
                # must be identifier then
                else:
                    self.current_token = (self.IDENTIFIER, current)
                return

    def token_type(
        self,
    ) -> {KEYWORD, SYMBOL, IDENTIFIER, INT_CONST, STRING_CONST}:
        """returns constant representing type of current token as a constant"""
        return self.current_token[0]

    # def keyword(
    #     self,
    # ) -> {
    #     CLASS,
    #     CONSTRUCTOR,
    #     FUNCTION,
    #     METHOD,
    #     FIELD,
    #     STATIC,
    #     VAR,
    #     INT,
    #     CHAR,
    #     BOOLEAN,
    #     VOID,
    #     TRUE,
    #     FALSE,
    #     NULL,
    #     THIS,
    #     LET,
    #     DO,
    #     IF,
    #     ELSE,
    #     WHILE,
    #     RETURN,
    # }:
    #     """returns the keyword that is the current token, as a constant
    #     Should be called only if token_type is KEYWORD"""
    #     return self.keywords.index(self.current_token[1].upper())

    # def symbol(
    #     self,
    # ) -> str:
    #     """returns the character that is the current token
    #     Should be called only if token_type is SYMBOL"""
    #     return self.current_token[1]

    # def identifier(
    #     self,
    # ) -> str:
    #     """returns the identifier that is the current token
    #     Should be called only if token_type is IDENTIFIER"""
    #     return self.current_token[1]

    # def int_value(
    #     self,
    # ) -> int:
    #     """returns the integer value of the current token
    #     Should be called only if token_type is INT_CONST"""
    #     return self.current_token[1]

    # def string_val(
    #     self,
    # ) -> str:
    #     """returns the string value of the current token
    #     without the 2 enclosing double quotes
    #     Should be called only if token_type is STRING_CONST"""
    #     return self.current_token[1]

    def close(self):
        """closes input file stream"""
        self.source.close()
