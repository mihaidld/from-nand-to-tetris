import os
import sys
from Parser import Parser
from CodeWriter import CodeWriter

# VM translator program that translates VM commands into
# Hack assembly programs
# The source program is supplied in a text file named filename.vm or directoryName containing vm files
# The generated code is written into a single text file named filename.asm or directoryName.asm
# Assumption: filename.vm is error-free


class Main:
    """drives the translation process"""

    def __init__(self):
        # Check for correct number of arguments
        if len(sys.argv) > 2:
            print("Usage: python VMTranslator.py [directory | filename.vm]")
            sys.exit(1)

        # If no path is specified, the translator operates on the current folder
        if len(sys.argv) == 1:
            path = os.getcwd()  # use .
        else:
            path = sys.argv[1]

        path_wo_ext = path.split(".")[0]
        # Constructs a CodeWriter to create an output file, Prog.asm, into which
        # it will write the translated assembly instructions
        self.writer = CodeWriter(path_wo_ext)
        self.parsers = []

        # Check if the path refers to a directory.
        if os.path.isdir(path):
            # Print a message indicating that it is a directory.
            print("It is a directory")
            for entry in os.scandir(path):
                if entry.is_file():  # check if it's a file
                    print(entry.path)
                    self.parsers.append(Parser(entry.path))

        # Check if the path refers to a regular file.
        elif os.path.isfile(path):
            # Print a message indicating that it is a normal file.
            print("It is a normal file")
            # constructs Parser for parsing the input file Prog.vm
            self.parsers.append(Parser(path))

        # If the path doesn't match a directory or a regular file, assume it's a special file (e.g., socket, FIFO, device file).
        else:
            # Print a message indicating that it is a special file.
            print("Usage: python VMTranslator.py filename.vm | directoryName")
            sys.exit(1)

    def main(self):
        """enters a loop that iterates through the VM commands in the input file.
        For each command, the program uses the Parser and the CodeWriter services
        for parsing the command into its fields and then generating from them a
        sequence of assembly instructions. The instructions are written into the
        output Prog.asm file."""
        for parser in self.parsers:
            # CodeWriter knows current filename parsed inside directory
            self.writer.set_filename(parser.filename)
            while True:
                parser.advance()
                # reached EOF and input file closed
                if not parser.current_command:
                    break

                self.writer.write_vm_command(parser.current_command)
                c_type = parser.command_type()
                if c_type == Parser.C_RETURN:
                    self.writer.write_return()
                    continue

                arg1 = parser.arg1()
                if c_type == Parser.C_ARITHMETIC:
                    self.writer.write_arithmetic(arg1)
                elif c_type == Parser.C_LABEL:
                    self.writer.write_label(arg1)
                elif c_type == Parser.C_GOTO:
                    self.writer.write_goto(arg1)
                elif c_type == Parser.C_IF:
                    self.writer.write_if(arg1)
                else:
                    arg2 = parser.arg2()

                    if c_type in [Parser.C_PUSH, Parser.C_POP]:
                        self.writer.write_push_pop(c_type, arg1, arg2)
                    elif c_type == Parser.C_FUNCTION:
                        self.writer.set_function_name(arg1)
                        self.writer.write_function(arg1, arg2)
                    elif c_type == Parser.C_CALL:
                        self.writer.write_call(arg1, arg2)

        self.writer.close()


Main().main()
