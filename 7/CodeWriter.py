import re
import sys
from Parser import Parser


class CodeWriter:
    """translate the parsed VM command into assembly instructions"""

    def __init__(self, filename):
        """opens output file stream and gets ready to write into it"""
        f = filename.split(".")[0]
        self.target = open(f"{f}.asm", "w")
        self.counter_condition = (
            0  # used for creating labels for branching in eq, lt, gt
        )
        self.symbols = {
            "local": "LCL",
            "argument": "ARG",
            "this": "THIS",
            "that": "THAT",
            "constant": 0,  # constants are virtual
            "temp": 5,  # TEMP segment starts at RAM5
            "pointer": 3,  # pointer segment starts at RAM3
            "static": f"{f[0].upper()+f[1:]}.",  # static vars named Filename.i
            "addr": "R13",
        }

    def write_arithmetic(self, command: str):
        """writes to output file ASM code that implements
        given arithmetic-logic command
        e.g. write_arithmetic("add") would result in generating
        assembly instructions that pop the two topmost elements
        from stack, add them up, and push the result onto the stack"""
        self.target.write(f"\n// {command}\n")  # write in comments also vm instruction
        if command == "add":
            self.__add()
        elif command == "sub":
            self.__sub()
        elif command == "neg":
            self.__negate_arit()
        elif command in ["eq", "gt", "lt"]:
            self.__eq_gt_lt(command)
        elif command == "and":
            self.__and()
        elif command == "or":
            self.__or()
        elif command == "not":
            self.__negate_log()

    def write_push_pop(
        self, command: {Parser.C_PUSH, Parser.C_POP}, segment: str, index: int
    ):
        """command is C_PUSH, C_POP,
        writes to output file ASM code that implements given push-pop command
        e.g. write_push_pop (C_PUSH,"local",2) would result in
        generating assembly instructions that implement the VM command
        push local 2."""
        if command == Parser.C_PUSH:
            # write in comments also vm instruction
            self.target.write(f"\n// push {segment} {index}\n")
            self.__push(segment, index)
        elif command == Parser.C_POP:
            self.target.write(f"\n// pop {segment} {index}\n")
            self.__pop(segment, index)

    def close(self):
        """closes output file stream"""
        self.__add_final_loop()
        self.target.close()

    def __add(self):
        self.__pop_two()
        self.target.write("M=D+M\n")

    def __sub(self):
        self.__pop_two()
        self.target.write("M=M-D\n")

    def __and(self):
        self.__pop_two()
        self.target.write("M=D&M\n")

    def __or(self):
        self.__pop_two()
        self.target.write("M=D|M\n")

    def __eq_gt_lt(self, command: str):
        self.__pop_two()
        self.__before_check()

        # check and conditional jump
        if command == "eq":
            comparison = "JEQ"
        elif command == "gt":
            comparison = "JGT"
        else:
            comparison = "JLT"
        self.target.write(f"D;{comparison}\n")

        self.__after_check()

    def __negate_arit(self):
        self.__pop_one()
        self.target.write("M=-M\n")

    def __negate_log(self):
        self.__pop_one()
        self.target.write("M=!M\n")

    def __pop(self, segment: str, index: int):
        if segment in ["local", "argument", "this", "that"]:
            self.__store_location(segment, index)
        self.__decrement_stack()
        if segment in ["local", "argument", "this", "that"]:
            self.target.write(
                """@R13
A=M
M=D
"""
            )
        else:
            # string concatenation for static, int addition for rest
            if segment == "static":
                index = str(index)
            self.target.write(
                f"""@{self.symbols[segment] + index}
M=D
"""
            )

    def __push(self, segment: str, index: int):
        if segment in ["local", "argument", "this", "that"]:
            self.__store_location(segment, index)
            self.target.write(
                """A=D
D=M
"""
            )
        else:
            # string concatenation for static, int addition for rest
            if segment == "static":
                index = str(index)
            self.target.write(f"@{self.symbols[segment] + index}\n")
            if segment == "constant":
                self.target.write("D=A\n")
            else:
                self.target.write("D=M\n")

        self.__increment_stack()

    def __pop_one(self):
        """helper to access top of stack, // check (set address) towards first operand"""
        self.target.write(
            """@SP
A=M-1
"""
        )

    def __pop_two(self):
        """helper to access top two of stack"""
        self.target.write(
            """@SP
AM=M-1
D=M
A=A-1
"""
        )

    def __store_location(self, segment: str, index: int):
        # local, argument, this, that
        seg = self.symbols[segment]
        self.target.write(
            f"""@{seg}
D=M
@{index}
D=D+A
@R13
M=D
"""
        )

    def __decrement_stack(self):
        self.target.write(
            """@SP
AM=M-1
D=M
"""
        )

    def __increment_stack(self):
        self.target.write(
            """@SP
AM=M+1
A=A-1
M=D
"""
        )

    def __before_check(self):
        self.target.write(
            f"""D=M-D
@TRUE{self.counter_condition}
"""
        )

    def __after_check(self):
        self.target.write(
            f"""@SP
A=M-1
M=0
@STOP{self.counter_condition}
0;JMP
(TRUE{self.counter_condition})
@SP
A=M-1
M=-1
(STOP{self.counter_condition})
"""
        )
        # increment counter for next usage
        self.counter_condition += 1

    def __add_final_loop(self):
        """private routine that writes the infinite loop code in assembly"""
        self.target.write(
            """\n(END)
@END
0;JMP"""
        )
