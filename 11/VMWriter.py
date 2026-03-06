import sys

"""emits VM code to the output .vm file:
uses translation techniques to handle variables, expressions, control flow, 
objects, arrays and follows standard mapping Jack -> VM
"""


class VMWriter:
    CONST = "constant"
    ARG = "argument"
    LOCAL = "local"
    STATIC = "static"
    THIS = "this"
    THAT = "that"
    POINTER = "pointer"
    TEMP = "temp"
    ADD = "add"
    SUB = "sub"
    NEG = "neg"
    EQ = "eq"
    GT = "gt"
    LT = "lt"
    AND = "and"
    OR = "or"
    NOT = "not"

    def __init__(self, output):
        """sets output where to write to .vm file
        for each new class to be compiled"""
        self.target = output  # Open file for write
        if not self.target:
            print(f"Could not open {output}")
            sys.exit(1)

    def write_push(
        self,
        segment: {CONST, ARG, LOCAL, STATIC, THIS, THAT, POINTER, TEMP},
        index: int,
    ):
        """writes a VM push command"""
        self.target.write(f"push {segment} {index}\n")

    def write_pop(
        self,
        segment: {CONST, ARG, LOCAL, STATIC, THIS, THAT, POINTER, TEMP},
        index: int,
    ):
        """writes a VM pop command"""
        self.target.write(f"pop {segment} {index}\n")

    def write_arithmetic(self, command: {ADD, SUB, NEG, EQ, GT, LT, AND, OR, NOT}):
        """writes a VM arithmetic logical command"""
        self.target.write(f"{command}\n")

    def write_label(self, label: str):
        """writes a VM label command"""
        self.target.write(f"label {label}\n")

    def write_goto(self, label: str):
        """writes a VM goto command"""
        self.target.write(f"goto {label}\n")

    def write_if(self, label: str):
        """writes a VM if-goto command"""
        self.target.write(f"if-goto {label}\n")

    def write_call(self, name: str, n_args: int):
        """writes a VM call command"""
        self.target.write(f"call {name} {n_args}\n")

    def write_function(self, name: str, n_locals: int):
        """writes a VM function command"""
        self.target.write(f"function {name} {n_locals}\n")

    def write_return(self):
        """writes a VM return command"""
        self.target.write("return\n")

    # def close(self):
    #     """closes output file"""
    #     self.target.close()
