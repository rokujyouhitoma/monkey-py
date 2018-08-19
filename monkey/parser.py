from dataclasses import dataclass, field
from typing import List, Optional

from monkey import _token as token, ast, lexer


@dataclass
class Parser():
    lex: lexer.Lexer
    curToken: token.Token
    peekToken: token.Token
    errors: List[str] = field(default_factory=list)

    def nextToken(self) -> None:
        self.curToken = self.peekToken
        self.peekToken = self.lex.NextToken()

    def ParseProgram(self) -> ast.Program:
        program = ast.Program([])

        while self.curToken.Type != token.EOF:
            stmt = self.parseStatement()
            if stmt is not None:
                program.Statements.append(stmt)
            self.nextToken()

        return program

    def parseStatement(self) -> Optional[ast.Statement]:
        if self.curToken.Type == token.LET:
            return self.parseLetStatement()
        else:
            return None

    def parseLetStatement(self) -> Optional[ast.LetStatement]:
        stmt = ast.LetStatement(
            Token=self.curToken,
            Name=ast.Identifier(Token=self.curToken, Value=self.curToken.Literal),
            Value=ast.Identifier(Token=self.curToken, Value=self.curToken.Literal))

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
            self.peekError(t)
            return False

    def Errors(self) -> List[str]:
        return self.errors

    def peekError(self, t: token.TokenType) -> None:
        msg = 'expected next token to be %s, got %s instead' % (t, self.peekToken.Type)
        self.errors.append(msg)


def New(lex: lexer.Lexer) -> Parser:
    p: Parser = Parser(
        lex=lex,
        curToken=token.Token(Type=token.ILLEGAL, Literal='ILLEGAL'),
        peekToken=token.Token(Type=token.ILLEGAL, Literal='ILLEGAL'))
    p.nextToken()
    p.nextToken()
    return p
