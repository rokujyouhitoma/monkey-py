from dataclasses import dataclass
from typing import Generic, TypeVar

from monkey import _token as token, ast, lexer

T = TypeVar('T')


@dataclass
class Parser(Generic[T]):
    lexer: lexer.Lexer
    curToken: token.Token
    peekToken: token.Token

    @classmethod
    def New(cls, lexer: lexer.Lexer) -> T:
        p = Parser(lexer=lexer, curToken=None, peekToken=None)
        p.nextToken()
        p.nextToken()
        return p

    def nextToken(self):
        self.curToken = self.peekToken
        self.peekToken = self.lexer.NextToken()

    def ParseProgram(self) -> ast.Program:
        program = ast.Program([])

        while self.curToken.Type != token.EOF:
            stmt = self.parseStatement()
            if stmt is not None:
                program.Statements.append(stmt)
            self.nextToken()

        return program

    def parseStatement(self) -> ast.Statement:
        if self.curToken.Type == token.LET:
            return self.parseLetStatement()
        else:
            return None

    def parseLetStatement(self) -> ast.LetStatement:
        stmt = ast.LetStatement(Token=self.curToken, Name=None, Value=None)

        if not self.expectPeek(token.IDENT):
            return None

        stmt.Name = ast.Identifier(Token=self.curToken, Value=self.curToken.Literal)

        if not self.expectPeek(token.ASSIGN):
            return None

        while not self.curTokenIs(token.SEMICOLON):
            self.nextToken()

        return stmt

    def curTokenIs(self, t: token.TokenType) -> bool:
        return self.curToken.Type == t

    def peekTokenIs(self, t: token.TokenType) -> bool:
        return self.peekToken.Type == t

    def expectPeek(self, t: token.TokenType) -> bool:
        if self.peekTokenIs(t):
            self.nextToken()
            return True
        else:
            return False
