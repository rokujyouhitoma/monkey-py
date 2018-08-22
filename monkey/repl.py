from monkey import token
from monkey.lexer import New

PROMPT = '>> '


def Start() -> None:
    while True:
        line = input(PROMPT)
        lexer = New(line)
        tok = lexer.NextToken()
        while tok.Type != token.EOF:
            print(tok)
            tok = lexer.NextToken()
