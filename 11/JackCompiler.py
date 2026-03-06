# Jack Compiler program that parses Jack commands into vm commands
# The source program is supplied in a text file named filename.jack
# or directoryName containing .jack files
# The generated code is written into a single text file named filename.vm
# if single input file,
# or one .vm file for eack .jack file stored in directoryName
# Assumption: filename.jack is error-free
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine
from CompilationEngineSymbol import CompilationEngineSymbol
import os
import sys


class Main:
    """drives the tokenization process"""

    def __init__(self):
        # Check for correct number of arguments
        if len(sys.argv) > 2:
            print("Usage: python JackAnalyzer.py [directory | filename.jack]")
            sys.exit(1)

        # If no path is specified, the translator operates on the current folder
        if len(sys.argv) == 1:
            path = os.getcwd()  # use .
        else:
            path = sys.argv[1]

        # save filenames to parse
        self.filenames = []

        # Check if the path refers to a directory.
        if os.path.isdir(path):
            # Print a message indicating that it is a directory.
            print("It is a directory")
            for entry in os.scandir(path):
                if entry.is_file():  # check if it's a file
                    print(entry.path)
                    if entry.path.endswith(".jack"):
                        self.filenames.append(entry.path)

        # Check if the path refers to a regular file.
        elif os.path.isfile(path):
            # Print a message indicating that it is a normal file.
            print("It is a normal file")
            if not path.endswith(".jack"):
                print("Usage: python JackCompiler.py filename.jack | directoryName")
                sys.exit(1)
            self.filenames.append(path)

        # If the path doesn't match a directory or a regular file, assume it's a special file (e.g., socket, FIFO, device file).
        else:
            # Print a message indicating that it is a special file.
            print("Usage: python JackCompiler.py filename.jack | directoryName")
            sys.exit(1)

    def main(self):
        """For each filename.jack input file:
        1. creates a JackTokenizer from filename.jack
        2. creates an output file filename.vm and
        prepares it for writing
        3. compiler uses SymbolTable, CompilationEngine and VMWriter modules
        to write VM code into output file"""
        print("self.filenames", self.filenames)
        for filename in self.filenames:
            tokenizer = JackTokenizer(filename)
            path_wo_ext = filename.removesuffix(".jack")
            """test only SymbolTable"""
            # with open(f"{path_wo_ext}.xml", "w") as f:
            #     c_engine = CompilationEngineSymbol(tokenizer, f)
            #     tokenizer.advance()  # gets 1st token
            #     c_engine.compile_class()

            with open(f"{path_wo_ext}.vm", "w") as f:
                # use CompilationEngine
                c_engine = CompilationEngine(tokenizer, f)
                tokenizer.advance()  # gets 1st token
                c_engine.compile_class()


Main().main()
