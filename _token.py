from dataclasses import dataclass

ILLEGAL = 'ILLEGAL'
EOF = 'EOF'

IDENT = 'IDENT'
INT = 'INT'

ASSIGN = '='
PLUS = '+'

COMMA = ','
SEMICOLON = ';'

LPAREN = '('
RPAREN = ')'
LBRACE = '{'
RBRACE = '}'

FUNCTION = 'FUNCTION'
LET = 'LET'

@dataclass
class TokenType:
    TypeName: str


@dataclass
class Token:
    Type: TokenType
    Literal: str
