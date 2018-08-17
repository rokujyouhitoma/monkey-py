from monkey.lexer import New
from monkey import _token as token

PROMPT = '>> '


def Start():
    while True:
        line = input(PROMPT)
        lexer = New(line)
        tok = lexer.NextToken()
        while tok.Type != token.EOF:
            print(tok)
            tok = lexer.NextToken()
