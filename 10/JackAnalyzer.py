# Jack Analyzer program that parses Jack commands into XML structured code
# The source program is supplied in a text file named filename.jack
# or directoryName containing .jack files
# The generated code is written into a single text file named filename.xml
# if single input file,
# or one .xml file for eack .jack file stored in directoryName
# Assumption: filename.jack is error-free
from JackTokenizer import JackTokenizer

from CompilationEngine import CompilationEngine
import os
import sys


class Main:
    """drives the tokenization process"""

    def __init__(self):
        # Check for correct number of arguments
        if len(sys.argv) > 2:
            print("Usage: python KackAnalyzer.py [directory | filename.jack]")
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
                print("Usage: python JackAnalyzer.py filename.jack | directoryName")
                sys.exit(1)
            self.filenames.append(path)

        # If the path doesn't match a directory or a regular file, assume it's a special file (e.g., socket, FIFO, device file).
        else:
            # Print a message indicating that it is a special file.
            print("Usage: python JackAnalyzer.py filename.jack | directoryName")
            sys.exit(1)

    def main(self):
        """For each filename.jack input file:
        1. creates a JackTokenizer from filename.jack
        2. creates an output file filename.xml and
        prepares it for writing
        3. creates and uses a CompilationEngine to compile the input
        from JackTokenizer into output file"""
        print("self.filenames", self.filenames)
        for filename in self.filenames:
            tokenizer = JackTokenizer(filename)
            path_wo_ext = filename.removesuffix(".jack")
            with open(f"{path_wo_ext}.xml", "w") as f:
                """test only Tokenizer:
                the analyzer enters a loop that advances and
                handles all the tokens in the input file,
                one token at a time, using the JackTokenizer services.
                Each token should be printed in a separate line,
                as <tokenType> token </tokenType>, where tokenType
                is an XML tag coding one of the five possible token types
                in the Jack language."""
                # f.write("<tokens>\n")
                # while True:
                #     tokenizer.advance()
                #     # reached EOF and input file closed
                #     if not tokenizer.current_token:
                #         break
                #     f.write(
                #         f"<{tokenizer.tags[tokenizer.current_token[0]]}>{tokenizer.current_token[1]}</{tokenizer.tags[tokenizer.current_token[0]]}>\n"
                #     )
                # f.write("</tokens>\n")

                # use CompilationEngine
                c_engine = CompilationEngine(tokenizer, f)
                tokenizer.advance()  # gets 1st token
                c_engine.compile_class()


Main().main()
