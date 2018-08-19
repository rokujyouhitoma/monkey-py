from dataclasses import dataclass
from typing import Dict

ILLEGAL = 'ILLEGAL'
EOF = 'EOF'

IDENT = 'IDENT'
INT = 'INT'

ASSIGN = '='
PLUS = '+'
MINUS = '-'
BANG = '!'
ASTERISK = '*'
SLASH = '/'

LT = '<'
GT = '>'

COMMA = ','
SEMICOLON = ';'

LPAREN = '('
RPAREN = ')'
LBRACE = '{'
RBRACE = '}'

EQ = '=='
NOT_EQ = '!='

FUNCTION = 'FUNCTION'
LET = 'LET'
TRUE = 'TRUE'
FALSE = 'FALSE'
IF = 'IF'
ELSE = 'ELSE'
RETURN = 'RETURN'

keywords: Dict[str, str] = {
    'fn': FUNCTION,
    'let': LET,
    'true': TRUE,
    'false': FALSE,
    'if': IF,
    'else': ELSE,
    'return': RETURN,
}


@dataclass
class TokenType:
    TypeName: str


@dataclass
class Token:
    Type: TokenType
    Literal: str


def LookupIdent(ident: str) -> str:
    if ident in keywords:
        token = keywords[ident]
        return token
    return IDENT
