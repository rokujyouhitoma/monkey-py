from dataclasses import dataclass

from monkey import token


@dataclass
class Lexer:
    input: str
    position: int = 0
    readPosition: int = 0
    ch: str = ''

    def readChar(self) -> None:
        if self.readPosition >= len(self.input):
            self.ch = ''
        else:
            self.ch = self.input[self.readPosition]
        self.position = self.readPosition
        self.readPosition += 1

    def NextToken(self) -> token.Token:
        tok: token.Token
        self.skipWhitespace()
        if self.ch == '=':
            if self.peekChar() == '=':
                ch = self.ch
                self.readChar()
                literal = str(ch) + str(self.ch)
                tok = self.newToken(token.EQ, literal)
            else:
                tok = self.newToken(token.ASSIGN, self.ch)
        elif self.ch == '+':
            tok = self.newToken(token.PLUS, self.ch)
        elif self.ch == '-':
            tok = self.newToken(token.MINUS, self.ch)
        elif self.ch == '!':
            if self.peekChar() == '=':
                ch = self.ch
                self.readChar()
                literal = str(ch) + str(self.ch)
                tok = self.newToken(token.NOT_EQ, literal)
            else:
                tok = self.newToken(token.BANG, self.ch)
        elif self.ch == '/':
            tok = self.newToken(token.SLASH, self.ch)
        elif self.ch == '*':
            tok = self.newToken(token.ASTERISK, self.ch)
        elif self.ch == '<':
            tok = self.newToken(token.LT, self.ch)
        elif self.ch == '>':
            tok = self.newToken(token.GT, self.ch)
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
        elif self.ch == '':
            tok = self.newToken(token.EOF, '')
        elif self.ch == '"':
            literal = self.readString()
            tok = self.newToken(token.STRING, literal)
        elif self.ch == '[':
            tok = self.newToken(token.LBRACKET, self.ch)
        elif self.ch == ']':
            tok = self.newToken(token.RBRACKET, self.ch)
        else:
            if self.isLetter(self.ch):
                literal = self.readIdentifier()
                tok = self.newToken(token.LookupIdent(literal), literal)
                return tok
            elif self.isDigit(self.ch):
                tok = self.newToken(token.INT, self.readNumber())
                return tok
            else:
                tok = self.newToken(token.ILLEGAL, self.ch)
        self.readChar()
        return tok

    def newToken(self, tokenType: token.TokenType, ch: str) -> token.Token:
        return token.Token(Type=tokenType, Literal=ch)

    def readIdentifier(self) -> str:
        position = self.position
        while self.isLetter(self.ch):
            self.readChar()
        return self.input[position:self.position]

    def isLetter(self, ch: str) -> bool:
        return ('a' <= ch and ch <= 'z') or ('A' <= ch and ch <= 'Z') or (ch == '_')

    def skipWhitespace(self) -> None:
        while self.ch == ' ' or self.ch == '\t' or self.ch == '\n' or self.ch == '\r':
            self.readChar()

    def readNumber(self) -> str:
        position = self.position
        while self.ch != '' and self.isDigit(self.ch):
            self.readChar()
        return self.input[position:self.position]

    def readString(self) -> str:
        position = self.position + 1
        while True:
            self.readChar()
            if self.ch == '"' or self.ch == 0:
                break
        return self.input[position:self.position]

    def isDigit(self, ch: str) -> bool:
        return '0' <= ch and ch <= '9'

    def peekChar(self) -> str:
        if self.readPosition >= len(self.input):
            return ''
        else:
            return self.input[self.readPosition]


def New(input: str) -> Lexer:
    lexer = Lexer(input=input)
    lexer.readChar()
    return lexer
