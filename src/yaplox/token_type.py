from enum import Enum


class TokenType(Enum):
    """
    Tokens that are used in the Language,
    """
    # Using an Enum like this feels horrible. This can go directly to the dailywtf.com
    # @TODO Figure out a better way to do this.
    #
    # Single - character tokens.
    #
    LEFT_PAREN = 0
    RIGHT_PAREN = 1
    LEFT_BRACE = 2
    RIGHT_BRACE = 3
    COMMA = 4
    DOT = 5
    MINUS = 6
    PLUS = 7
    SEMICOLON = 8
    SLASH = 9
    STAR = 10
    #
    # One or two character tokens.
    #
    BANG = 11
    BANG_EQUAL = 12
    EQUAL = 13
    EQUAL_EQUAL = 14
    GREATER = 15
    GREATER_EQUAL = 16
    LESS = 17
    LESS_EQUAL = 18
    #
    # Literals.
    #
    IDENTIFIER = 20
    STRING = 21
    NUMBER = 22
    #
    # Keywords.
    #
    AND = 30
    CLASS = 31
    ELSE = 32
    FALSE = 33
    FUN = 34
    FOR = 35
    IF = 36
    NIL = 37
    OR = 38
    PRINT = 39
    RETURN = 40
    SUPER = 41
    THIS = 42
    TRUE = 43
    VAR = 44
    WHILE = 45

    EOF = 46
