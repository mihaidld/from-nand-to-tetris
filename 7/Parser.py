import re
import sys


class Parser:
    """understand what each VM command seeks to do"""

    (
        C_ARITHMETIC,
        C_PUSH,
        C_POP,
        C_LABEL,
        C_GOTO,
        C_IF,
        C_FUNCTION,
        C_RETURN,
        C_CALL,
    ) = range(9)

    def __init__(self, filename):
        """opens file stream and gets ready to parse it"""
        self.source = open(filename, "r")  # Open file for read
        if not self.source:
            print("Could not open {}".format(filename))
            sys.exit(1)

        self.current_command = None

    # def has_more_lines(self) -> bool:
    #     """are there more lines in the input?"""
    #     pass

    def advance(self):
        """reads next command from input and makes it the current command
        Should be called only if has_more_lines is true
        Initially there is no current command"""
        while True:
            current = self.source.readline()
            if not current:
                """If the stream is already at EOF, an empty string is returned"""
                self.close()
                self.current_command = None
                break
            """Process the line
            Handle comments and whitespace -> ignore whitespace and everything after //
            remove left and right whitespace and empty lines (containing only \n) with strip()
            remove comments after //"""
            current = current.strip().split("//")[0]
            # line was containing only comments and whitespace so all removed
            if not current:
                continue
            else:
                self.current_command = current
                break

    def command_type(
        self,
    ) -> {
        C_ARITHMETIC,
        C_PUSH,
        C_POP,
        C_LABEL,
        C_GOTO,
        C_IF,
        C_FUNCTION,
        C_RETURN,
        C_CALL,
    }:
        """returns constant representing type of current command
        e.g. if current arithmetic or logical returns C_ARITHMETIC"""
        first = self.current_command.split()[0]
        if first in ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]:
            return self.C_ARITHMETIC
        if first == "push":
            return self.C_PUSH
        if first == "pop":
            return self.C_POP
        if first == "label":
            return self.C_LABEL
        if first == "goto":
            return self.C_GOTO
        if first == "if-goto":
            return self.IF
        if first == "function":
            return self.C_FUNCTION
        if first == "call":
            return self.C_RETURN
        if first == "return":
            return self.C_CALL

    def arg1(self) -> str:
        """returns 1st arg of current command
        e.g.if C_ARITHMETIC returns command itself add, sub etc.
        Should not be called if current command is C_RETURN"""
        parts = self.current_command.split()
        if self.command_type() == Parser.C_ARITHMETIC:
            return parts[0]
        else:
            return parts[1]

    def arg2(self) -> int:
        """returns 2nd arg of current command
        Should be called only if current command if C_PUSH, C_POP, C_FUNCTION, C_CALL
        For example, if the current command is push local 2,
        then calling arg1() and arg2() would return, respectively, "local" and 2.
        If the current command is add,
        then calling arg1() would return "add",
        and arg2() would not be called

        """
        return int(self.current_command.split()[2])

    def close(self):
        """closes input file stream"""
        self.source.close()
