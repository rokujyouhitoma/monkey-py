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
        self.skipWhitespace()
        if self.ch == '=':
            tok = self.newToken(token.ASSIGN, self.ch)
        elif self.ch == ';':
            tok = self.newToken(token.SEMICOLON, self.ch)
        elif self.ch == '(':
            tok = self.newToken(token.LPAREN, self.ch)
        elif self.ch == ')':
            tok = self.newToken(token.RPAREN, self.ch)
        elif self.ch == ',':
            tok = self.newToken(token.COMMA, self.ch)
        elif self.ch == '+':
            tok = self.newToken(token.PLUS, self.ch)
        elif self.ch == '{':
            tok = self.newToken(token.LBRACE, self.ch)
        elif self.ch == '}':
            tok = self.newToken(token.RBRACE, self.ch)
        elif self.ch == 0:
            tok = token.Token(Type = token.EOF, Literal = '')
        else:
            if self.isLetter(self.ch):
                literal = self.readIdentifier()
                tok = token.Token(Type = token.LookupIdent(literal), Literal = literal)
                return tok
            elif self.isDigit(self.ch):
                tok = token.Token(Type = token.INT, Literal = self.readNumber())
                return tok
            else:
                tok = self.newToken(token.ILLEGAL, self.ch)
        self.readChar()
        return tok

    def newToken(self, tokenType: token.TokenType, ch: bytes) -> token.Token:
        return token.Token(Type = tokenType, Literal = str(ch))

    def readIdentifier(self) -> str:
        position = self.position
        while self.isLetter(self.ch):
            self.readChar()
        return self.input[position:self.position]

    def isLetter(self, ch: bytes) -> bool:
        return ('a' <= ch and ch <= 'z') or ('A' <= ch and ch <= 'Z') or (ch == b'_')

    def skipWhitespace(self) -> None:
        while self.ch == ' ' or self.ch == '\t' or self.ch == '\n' or self.ch == '\r':
            self.readChar()

    def readNumber(self) -> str:
        position = self.position
        while self.isDigit(self.ch):
            self.readChar()
        return self.input[position:self.position]

    def isDigit(self, ch: bytes) -> bool:
        return '0' <= ch and ch <= '9'


def New(input: str) -> Lexer:
    lexer = Lexer(input = input)
    lexer.readChar()
    return lexer
