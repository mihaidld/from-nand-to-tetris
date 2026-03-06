import re
import sys
from Parser import Parser


class CodeWriter:
    """translate the parsed VM command into assembly instructions"""

    def __init__(self, filename_out):
        """opens output file stream and gets ready to write into it"""
        self.filename_out = filename_out
        # for directory default initial value of directory name
        self.filename_in = filename_out
        self.current_function_name = "Initial"
        self.target = open(f"{filename_out}.asm", "w")
        self.counter_condition = (
            0  # used for creating labels for branching in eq, lt, gt
        )
        self.counter_return = (
            0  # used for creating return address labels for call / return
        )
        self.symbols = {
            "local": "LCL",
            "argument": "ARG",
            "this": "THIS",
            "that": "THAT",
            "constant": 0,  # constants are virtual
            "temp": 5,  # temp segment starts at RAM5
            "pointer": 3,  # pointer segment starts at RAM3
        }
        self.write_init()

    def set_filename(self, filename: str):
        """informs CodeWriter that translation of new VM file has started"""
        self.filename_in = filename.split("/")[-1]  # retrieves only filename from path

    def set_function_name(self, function_name: str):
        """informs CodeWriter that current command is part of function_name"""
        self.current_function_name = function_name
        # reset counter for label conditions inside function
        self.counter_condition = 0

    def close(self):
        """closes output file stream"""
        # self.__add_final_loop()
        self.target.close()

    def write_init(self):
        """writes asm instructions that effect boostrap code that initializes the VM
        to be placed at the beginning of generated .asm code
        SP=256
        Call Sys.init"""
        self.target.write(
            """// SP=256
@256
D=A
@SP
M=D

// call Sys.Init
"""
        )
        self.write_call(
            "Sys.init", 0
        )  # call Sys.init from OS without args, which will call Main.main (main function from Main.vm file)

    def write_vm_command(self, command: str):
        """writes in comments also vm instruction"""
        self.target.write(f"\n// {command}\n")

    def write_arithmetic(self, command: str):
        """writes to output file ASM code that implements
        given arithmetic-logic command
        e.g. write_arithmetic("add") would result in generating
        assembly instructions that pop the two topmost elements
        from stack, add them up, and push the result onto the stack"""
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
            self.__push(segment, index)
        elif command == Parser.C_POP:
            self.__pop(segment, index)

    def write_label(self, label: str):
        """writes asm code that effects label command"""
        self.target.write(f"({self.__function_prefix()}{label})\n")

    def write_goto(self, label: str):
        """writes asm code that effects goto command: unconditional jump"""
        self.target.write(f"@{self.__function_prefix()}{label}\n0;JMP\n")

    def write_if(self, label: str):
        """writes asm code that effects if-goto command: conditional jump"""
        self.target.write(
            f"""@SP
AM=M-1
D=M
@{self.__function_prefix()}{label}
D;JNE
"""
        )

    def write_function(self, function_name: str, n_vars: int):
        """writes asm code that effects function command"""
        self.target.write(f"({function_name})\n")
        for i in range(n_vars):
            self.write_push_pop(Parser.C_PUSH, "constant", 0)

    def write_call(self, function_name: str, n_vars: int):
        """writes asm code that effects call command"""
        # @returnAddress D=A  followed by pushing D onto the stack
        self.target.write(
            f"""@{self.current_function_name}$ret{self.counter_return}
D=A
"""
        )
        self.__increment_stack()

        # save caller LCL, ARG, THIS, THAT
        self.target.write(
            """@LCL
D=M
"""
        )
        self.__increment_stack()
        self.target.write(
            """@ARG
D=M
"""
        )
        self.__increment_stack()
        self.target.write(
            """@THIS
D=M
"""
        )
        self.__increment_stack()
        self.target.write(
            """@THAT
D=M
"""
        )
        self.__increment_stack()

        # reposition ARG for callee: ARG = SP - 5 -nArgs
        # reposition LCL: LCL = SP
        # goto functionName
        # declare label for returnAddress: (returnAddress)
        self.target.write(
            f"""@{5 + n_vars}
D=A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@{function_name}
0;JMP
({self.current_function_name}$ret{self.counter_return})
"""
        )
        self.counter_return += 1  # increment return address for next call

    def write_return(self):
        """writes asm code that effects return command"""
        # endFrame (R13) = LCL
        self.target.write(
            """@LCL
D=M
@R13
M=D
@5
"""
        )
        # returnAddress (R14) = *(endFrame - 5)
        self.__saved_frame()
        self.target.write(
            """@R14
M=D
"""
        )
        # pop return value from stack to argument 0
        self.write_push_pop(Parser.C_POP, "argument", 0)

        # restore SP
        self.target.write(
            """@ARG
D=M+1
@SP
M=D
"""
        )

        # restore THAT
        self.target.write("@1\n")
        self.__saved_frame()
        self.target.write(
            """@THAT
M=D
"""
        )
        # restore THIS
        self.target.write("@2\n")
        self.__saved_frame()
        self.target.write(
            """@THIS
M=D
"""
        )
        # restore ARG
        self.target.write("@3\n")
        self.__saved_frame()
        self.target.write(
            """@ARG
M=D
"""
        )
        # restore LCL
        self.target.write("@4\n")
        self.__saved_frame()
        self.target.write(
            """@LCL
M=D
"""
        )

        # goto returnAddress saved in R14
        self.target.write(
            """@R14
A=M
0;JMP
"""
        )

    def __saved_frame(self):
        self.target.write(
            """D=A
@R13
D=M-D
A=D
D=M
"""
        )

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
                """@R15
A=M
M=D
"""
            )
        else:
            # string concatenation for static, int addition for rest
            if segment == "static":
                self.target.write(
                    f"""@{self.__static_prefix()}{index}
M=D
"""
                )
            else:
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
                self.target.write(f"@{self.__static_prefix()}{index}\n")
            else:
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
@R15
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

    def __function_prefix(self):
        return f"{self.current_function_name}$" if self.current_function_name else ""

    def __static_prefix(self):
        """static vars named Filename.i"""
        return f"{self.filename_in[0].upper()+self.filename_in[1:]}."

    def __before_check(self):

        self.target.write(
            f"""D=M-D
@{self.__function_prefix()}TRUE{self.counter_condition}
"""
        )

    def __after_check(self):
        func = self.__function_prefix()
        self.target.write(
            f"""@SP
A=M-1
M=0
@{func}STOP{self.counter_condition}
0;JMP
({func}TRUE{self.counter_condition})
@SP
A=M-1
M=-1
({func}STOP{self.counter_condition})
"""
        )
        # increment counter for next label usage inside same function
        self.counter_condition += 1


#     def __add_final_loop(self):
#         """private routine that writes the infinite loop code in assembly"""
#         self.target.write(
#             """\n(END)
# @END
# 0;JMP"""
#         )
