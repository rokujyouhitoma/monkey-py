from dataclasses import dataclass
import _token as token


@dataclass
class Lexer:
    input: str
    position: int = 0
    readPosition: int = 0
    ch: bytes = b''

    def readChar(self) -> None:
        if self.readPosition >= len(self.input):
            self.ch = 0
        else:
            self.ch = self.input[self.readPosition]
        self.position = self.readPosition
        self.readPosition += 1

    def NextToken(self) -> token.Token:
        tok: token.Token
        if self.ch == '=':
            tok = self.newToken(token.ASSIGN, self.ch)
        if self.ch == ';':
            tok = self.newToken(token.SEMICOLON, self.ch)
        if self.ch == '(':
            tok = self.newToken(token.LPAREN, self.ch)
        if self.ch == ')':
            tok = self.newToken(token.RPAREN, self.ch)
        if self.ch == ',':
            tok = self.newToken(token.COMMA, self.ch)
        if self.ch == '+':
            tok = self.newToken(token.PLUS, self.ch)
        if self.ch == '{':
            tok = self.newToken(token.LBRACE, self.ch)
        if self.ch == '}':
            tok = self.newToken(token.RBRACE, self.ch)
        elif self.ch == 0:
            tok = token.Token(Type = token.EOF, Literal = '')
        self.readChar()
        return tok

    def newToken(self, tokenType: token.TokenType, ch: bytes) -> token.Token:
        return token.Token(Type = tokenType, Literal = str(ch))


def New(input: str) -> Lexer:
    l = Lexer(input = input)
    l.readChar()
    return l
