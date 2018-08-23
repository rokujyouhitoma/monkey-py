from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional

from monkey import ast, lexer, token

prefixParseFn = Callable[[], Optional[ast.Expression]]
infixParseFn = Callable[[
    ast.Expression,
], ast.Expression]

LOWEST = 0
EQUALS = 1  # ==
LESSGREATER = 2  # > or <
SUM = 3  # +
PRODUCT = 4  # *
PREFIX = 5  # -X or !X
CALL = 6  # myFunction(X)


@dataclass
class Parser():
    lex: lexer.Lexer

    curToken: token.Token
    peekToken: token.Token

    prefixParseFns: Dict[str, prefixParseFn] = field(default_factory=dict)
    infixParseFns: Dict[str, infixParseFn] = field(default_factory=dict)
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
        elif self.curToken.Type == token.RETURN:
            return self.parseReturnStatement()
        else:
            return self.parseExpressionStatement()

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

    def parseReturnStatement(self) -> Optional[ast.ReturnStatement]:
        # TODO: for ReturnValue
        stmt = ast.ReturnStatement(
            Token=self.curToken,
            ReturnValue=ast.Identifier(Token=self.curToken, Value=self.curToken.Literal))

        self.nextToken()

        while not self.curTokenIs(token.SEMICOLON):
            self.nextToken()

        return stmt

    def parseExpressionStatement(self) -> Optional[ast.ExpressionStatement]:
        stmt = ast.ExpressionStatement(
            Token=self.curToken, ExpressionValue=self.parseExpression(LOWEST))

        if self.peekTokenIs(token.SEMICOLON):
            self.nextToken()

        return stmt

    def parseExpression(self, precedence: int) -> Optional[ast.Expression]:
        prefix = self.prefixParseFns.get(self.curToken.Type.TypeName)
        if prefix is None:
            return None
        leftExp = prefix()

        return leftExp

    def parseIdentifier(self) -> ast.Expression:
        return ast.Identifier(Token=self.curToken, Value=self.curToken.Literal)

    def parseIntegerLiteral(self) -> Optional[ast.Expression]:
        try:
            value = int(self.curToken.Literal)
        except ValueError:
            msg = 'could not parse %s as integer' % self.curToken.Literal
            self.errors.append(msg)
            return None
        lit = ast.IntegerLiteral(Token=self.curToken, Value=value)
        return lit

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

    def registerPrefix(self, tokenType: token.TokenType, fn: prefixParseFn) -> None:
        self.prefixParseFns[tokenType.TypeName] = fn

    def registerInfix(self, tokenType: token.TokenType, fn: infixParseFn) -> None:
        self.infixParseFns[tokenType.TypeName] = fn


def New(lex: lexer.Lexer) -> Parser:
    p: Parser = Parser(
        lex=lex,
        curToken=token.Token(Type=token.ILLEGAL, Literal='ILLEGAL'),
        peekToken=token.Token(Type=token.ILLEGAL, Literal='ILLEGAL'))
    p.registerPrefix(token.IDENT, p.parseIdentifier)
    p.registerPrefix(token.INT, p.parseIntegerLiteral)
    p.nextToken()
    p.nextToken()
    return p
