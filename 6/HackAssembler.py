import re
import sys
from dictionary import comp, dest, jump, symbols

# Hack Assembler program that translates Hack assembly programs
# into executable Hack binary code
# The source program is supplied in a text file named filename.asm
# The generated code is written into a text file named filename.hack
# Assumption: filename.asm is error-free

# Check for correct number of arguments
if len(sys.argv) != 2:
    print("Usage: python assembler.py filename.asm")
    sys.exit(1)

# Try to open filename
filename = sys.argv[1]

# counter used during 1st pass of label definition replacement
# not incremented if comments/whitepace/label definition
counter_instructions = 0
# counter counter_variables initialized at 16
counter_variables = 16
# Define the regex pattern for label definition to match content between the parenthesis ()
pattern_label = r"\((.*?)\)"
# Keep processed lines after 1st pass
processed = []
a_instruction = "0"  # initial value of A-instruction
c_instruction = "111"  # initial value of C-instruction

# create target file with same name, but extension .hack
target = open(f"{filename.split('.')[0]}.hack", "w")

with open(filename, "r") as f:  # Open file for read
    if not f:
        print("Could not open {}".format(filename))
        sys.exit(1)

    # First pass: remove whitespace, comments and handle label definition
    # replace (labelName) by line number of next instruction
    # look for lines of code that begin with (
    # add them into symbol table: (labelName, address next instruction)
    # Keep track of how many lines with instructions read sofar

    for line in f:  # Read line-by-line
        # Process the line

        # Handle comments and whitespace -> ignore whitespace and everything after //
        # remove left and right whitespace and empty lines (containing only \n) with strip()
        # remove internal whitespace (e.g. D = M + 1) with replace()
        # remove comments after //
        line = line.strip().replace(" ", "").split("//")[0]

        # check if there are still any characters in the line
        if line:
            # Check for label : ( as 1st character of the line
            if re.match(r"\(", line[0]):
                # Search for the pattern in the input string
                match = re.search(pattern_label, line)

                # Check if a match is found and extract the substring
                if match:
                    label = match.group(1)
                    # add label to symbol table in binary format
                    symbols[label] = format(counter_instructions, "b")
            else:
                # not label definition so increment counter_instructions and keep line
                counter_instructions += 1
                processed.append(line)
    # 2nd pass: add variable symbols, scan entire program again
    # after 1st pass we remain with A and C instructions only
    # translate each line into A/C-instructions 16 char strings with 0's and 1's
    # write instructions into target filename.hack file
    len_processed = len(processed)
    for i, instruction in enumerate(processed):
        # Check for A-instruction : @ in 1st character of the line
        # Handle A-instructions = if 1st character non-whitespace is @: @<int | variable>
        # if remaining chars make a positive int (>=0) then convert it to binary representation with
        # padded 0's to make 15 chars and concatenate 0 (opcode) to binary representation
        # else remaining chars is variable so lookup variable dict
        if re.match(r"@", instruction[0]):
            addr = instruction[1:]

            # try to convert decimal address into binary representation
            # Pad string using string.rjust(length[, fill])
            # length is the length of the final padded string,
            # and fill is the character to pad string with.
            # If omitted, fill defaults to ' ' — the space character.
            try:
                binary = format(int(addr), "b")
                binary_instruction = a_instruction + binary.rjust(15, "0")
            except ValueError:
                # Handle variables with symbols dict:
                # already inside -> check value,
                # not yet -> give it value counter_variables,
                # use counter_variables to translate instruction,
                # counter_variables++
                if addr not in symbols:
                    symbols[addr] = format(counter_variables, "b")
                    counter_variables += 1
                binary_instruction = a_instruction + symbols[addr].rjust(15, "0")
        else:
            # Handle C-instructions dest=comp;jump where only comp is mandatory
            # 111ac1c1c2c3c4c5c6d1d2d3j1j2j3
            # if not A-, then C-instruction -> pre-pend with "111" (opcode),
            # then check for separators = and ; to split string in 1-3 parts
            # depending on values of 3 parts append values from comp, dest and jump dictionaries

            # Split the string into two parts based on the = delimiter
            try:
                dest_part, part2 = instruction.split("=", 1)
            except ValueError:
                dest_part = ""
                part2 = instruction

            # Split the second part based on the ; delimiter
            try:
                comp_part, jump_part = part2.split(";", 1)
            except ValueError:
                jump_part = ""
                comp_part = part2

            binary_instruction = (
                c_instruction + comp[comp_part] + dest[dest_part] + jump[jump_part]
            )

        # write binary instruction with newline char to hack file
        if i < len_processed - 1:
            binary_instruction += "\n"
        target.write(binary_instruction)

# Close the file
target.close()

# Success
sys.exit(0)
