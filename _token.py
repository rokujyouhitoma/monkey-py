from dataclasses import dataclass

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

FUNCTION = 'FUNCTION'
LET = 'LET'
TRUE = 'TRUE'
FALSE = 'FALSE'
IF = 'IF'
ELSE = 'ELSE'
RETURN = 'RETURN'

keywords = {
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


def LookupIdent(ident: str) -> TokenType:
    if ident in keywords:
        token = keywords.get(ident)
        return token
    return IDENT
