import sys

"""Stores variables information:
we never need more than 2 symbol tables -> 2 instances only of SymbolTable class:
- class-level symbol table is reset each time 
we start compiling new class
- subroutine-level symbol table is reset each time 
we start compiling new subroutine

We give each variable a running index within 
its scope (class/subroutine) and kind (local/arg)
Index starts at 0, incremented with each symbol added to table
reset to 0 when starting new scope
When compilling error-free Jack code, each symbol not found in symbol table
can be assumed to be either subroutine name or class name

1st stage to test adding symbol table we extend Syntax Analyzer with
handling of identifiers:
 - output identifier category:
local, argument, static, field, class, subroutine
- if identifier category is local, argument, static, field
outputs also running index assigned to this variable in symbol table
- output whether identifier is being defined (e.g. var command) or 
being used (getter, when evaluating expression)
"""


class SymbolTable:
    """"""

    STATIC = "static"
    FIELD = "this"
    ARG = "argument"
    LOCAL = "local"
    NONE = None

    def __init__(self):
        """creates new symbol table"""
        self.counter_static = 0
        self.counter_field = 0
        self.class_variables = {}
        self.subroutine_variables = {}

    def start_subroutine(self):
        """starts new subroutine scope (resets subroutine's symbol table)"""
        self.counter_arg = 0
        self.counter_local = 0
        self.subroutine_variables = {}

    def define(self, name: str, type: str, kind: {STATIC, FIELD, ARG, LOCAL}):
        """defines new identifier of given name, type and kind,
        and assigns it a running index.
        Adds new tuple to symbol table
        STATIC and FIELD identifiers have a class scope.
        ARG and LOCAL identifiers have a subroutine scope"""
        if kind == SymbolTable.STATIC:
            self.class_variables[name] = (type, kind, self.counter_static)
            self.counter_static += 1
        elif kind == SymbolTable.FIELD:
            self.class_variables[name] = (type, kind, self.counter_field)
            self.counter_field += 1
        elif kind == SymbolTable.ARG:
            self.subroutine_variables[name] = (type, kind, self.counter_arg)
            self.counter_arg += 1
        elif kind == SymbolTable.LOCAL:
            self.class_variables[name] = (type, kind, self.counter_local)
            self.counter_local += 1

    def var_count(self, kind: {STATIC, FIELD, ARG, LOCAL}) -> int:
        """returns # of variables of given kind already defined in current scope.
        Used for generating code for setting position"""
        if kind == SymbolTable.STATIC:
            return self.counter_static
        if kind == SymbolTable.FIELD:
            return self.counter_field
        if kind == SymbolTable.ARG:
            return self.counter_arg
        if kind == SymbolTable.LOCAL:
            return self.counter_local

    def kind_of(self, name: str) -> {STATIC, FIELD, ARG, LOCAL, NONE}:
        """returns the kind of the named identifier in the current scope.
        If the identifier is unknown in the current scope, returns NONE"""
        if name in self.subroutine_variables:
            return self.subroutine_variables[name][1]
        elif name in self.class_variables:
            return self.class_variables[name][1]
        else:
            return SymbolTable.NONE

    def type_of(self, name: str) -> str:
        """returns the type of the named identifier in the current scope"""
        if name in self.subroutine_variables:
            return self.subroutine_variables[name][0]
        elif name in self.class_variables:
            return self.class_variables[name][0]

    def index_of(self, name: str) -> int:
        """returns the index assigned to the named identifier"""
        if name in self.subroutine_variables:
            return self.subroutine_variables[name][2]
        elif name in self.class_variables:
            return self.class_variables[name][2]
