from dataclasses import dataclass
from typing import Dict


@dataclass
class TokenType:
    TypeName: str


@dataclass
class Token:
    Type: TokenType
    Literal: str


ILLEGAL = TokenType(TypeName='ILLEGAL')
EOF = TokenType(TypeName='EOF')

IDENT = TokenType(TypeName='IDENT')
INT = TokenType(TypeName='INT')

ASSIGN = TokenType(TypeName='=')
PLUS = TokenType(TypeName='+')
MINUS = TokenType(TypeName='-')
BANG = TokenType(TypeName='!')
ASTERISK = TokenType(TypeName='*')
SLASH = TokenType(TypeName='/')

LT = TokenType(TypeName='<')
GT = TokenType(TypeName='>')

COMMA = TokenType(TypeName=',')
SEMICOLON = TokenType(TypeName=';')

LPAREN = TokenType(TypeName='(')
RPAREN = TokenType(TypeName=')')
LBRACE = TokenType(TypeName='{')
RBRACE = TokenType(TypeName='}')

EQ = TokenType(TypeName='==')
NOT_EQ = TokenType(TypeName='!=')

FUNCTION = TokenType(TypeName='FUNCTION')
LET = TokenType(TypeName='LET')
TRUE = TokenType(TypeName='TRUE')
FALSE = TokenType(TypeName='FALSE')
IF = TokenType(TypeName='IF')
ELSE = TokenType(TypeName='ELSE')
RETURN = TokenType(TypeName='RETURN')

STRING = TokenType(TypeName='STRING')

keywords: Dict[str, TokenType] = {
    'fn': FUNCTION,
    'let': LET,
    'true': TRUE,
    'false': FALSE,
    'if': IF,
    'else': ELSE,
    'return': RETURN,
}


def LookupIdent(ident: str) -> TokenType:
    if ident in keywords:
        token = keywords[ident]
        return token
    return IDENT
