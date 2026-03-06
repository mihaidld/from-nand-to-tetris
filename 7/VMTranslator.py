import re
import sys
from Parser import Parser
from CodeWriter import CodeWriter

# VM translator program that translates VM commands into
# Hack assembly programs
# The source program is supplied in a text file named filename.vm
# The generated code is written into a text file named filename.asm
# Assumption: filename.vm is error-free


class VMTranslator:
    """drives the translation process"""

    def __init__(self):
        # Check for correct number of arguments
        if len(sys.argv) != 2:
            print("Usage: python VMTranslator.py filename.vm")
            sys.exit(1)

        # Try to open filename
        self.filename = sys.argv[1]
        # constructs Parser for parsing the input file Prog.vm
        self.parser = Parser(self.filename)
        # creates an output file, Prog.asm, into which
        # it will write the translated assembly instructions
        self.writer = CodeWriter(self.filename)

    def exec(self):
        """enters a loop that iterates through the VM commands in the input file.
        For each command, the program uses the Parser and the CodeWriter services
        for parsing the command into its fields and then generating from them a
        sequence of assembly instructions. The instructions are written into the
        output Prog.asm file."""

        while True:
            self.parser.advance()
            # reached EOF and input file closed
            if not self.parser.current_command:
                break

            c_type = self.parser.command_type()
            if c_type == Parser.C_RETURN:
                continue
            arg1 = self.parser.arg1()
            if c_type == Parser.C_ARITHMETIC:
                self.writer.write_arithmetic(arg1)
            elif c_type in [Parser.C_PUSH, Parser.C_POP]:
                arg2 = self.parser.arg2()
                self.writer.write_push_pop(c_type, arg1, arg2)
        self.writer.close()


VMTranslator().exec()
