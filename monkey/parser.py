from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional

from monkey import ast, lexer, token

prefixParseFn = Callable[[], Optional[ast.Expression]]
infixParseFn = Callable[[
    ast.Expression,
], Optional[ast.Expression]]

LOWEST = 0
EQUALS = 1  # ==
LESSGREATER = 2  # > or <
SUM = 3  # +
PRODUCT = 4  # *
PREFIX = 5  # -X or !X
CALL = 6  # myFunction(X)

precedences: Dict[str, int] = {
    token.EQ.TypeName: EQUALS,
    token.NOT_EQ.TypeName: EQUALS,
    token.LT.TypeName: LESSGREATER,
    token.GT.TypeName: LESSGREATER,
    token.PLUS.TypeName: SUM,
    token.MINUS.TypeName: SUM,
    token.SLASH.TypeName: PRODUCT,
    token.ASTERISK.TypeName: PRODUCT,
}


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
            self.noPrefixParseFnError(self.curToken.Type)
            return None
        leftExp = prefix()

        while (not self.peekTokenIs(token.SEMICOLON)) and (precedence < self.peekPrecedence()):
            infix = self.infixParseFns.get(self.peekToken.Type.TypeName)
            if infix is None:
                return leftExp
            self.nextToken()
            if leftExp is not None:
                leftExp = infix(leftExp)
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

    def parsePrefixExpression(self) -> Optional[ast.Expression]:
        curToken = self.curToken
        self.nextToken()
        expression = ast.PrefixExpression(
            Token=curToken, Operator=curToken.Literal, Right=self.parseExpression(PREFIX))

        return expression

    def parseInfixExpression(self, left: ast.Expression) -> Optional[ast.Expression]:
        curToken = self.curToken
        curTokenLiteral = self.curToken.Literal
        precedence = self.curPrecedence()
        self.nextToken()
        expression = ast.InfixExpression(
            Token=curToken,
            Operator=curTokenLiteral,
            Left=left,
            Right=self.parseExpression(precedence))

        return expression

    def parseBoolean(self) -> Optional[ast.Expression]:
        return ast.Boolean(Token=self.curToken, Value=self.curTokenIs(token.TRUE))

    def parseGroupedExpression(self) -> Optional[ast.Expression]:
        self.nextToken()

        exp = self.parseExpression(LOWEST)

        if not self.expectPeek(token.RPAREN):
            return None

        return exp

    def parseIfExpression(self) -> Optional[ast.Expression]:
        if not self.expectPeek(token.LPAREN):
            return None

        self.nextToken()

        condition = self.parseExpression(LOWEST)
        if not condition:
            return None

        if not self.expectPeek(token.RPAREN):
            return None

        if not self.expectPeek(token.LBRACE):
            return None

        consequence = self.parseBlockStatement()

        alternative = None
        if self.peekTokenIs(token.ELSE):
            self.nextToken()

            if not self.expectPeek(token.LBRACE):
                return None

            alternative = self.parseBlockStatement()

        expression = ast.IfExpression(
            Token=self.curToken,
            Condition=condition,
            Consequence=consequence,
            Alternative=alternative)

        return expression

    def parseBlockStatement(self) -> ast.BlockStatement:
        curToken = self.curToken

        self.nextToken()

        statements: List[ast.Statement] = []
        while (not self.curTokenIs(token.RBRACE)) and (not self.curTokenIs(token.EOF)):
            stmt = self.parseStatement()
            if stmt is not None:
                statements.append(stmt)
            self.nextToken()

        block = ast.BlockStatement(Token=curToken, Statements=statements)
        return block

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

    def noPrefixParseFnError(self, t: token.TokenType) -> None:
        msg = 'no prefix parse function for %s found' % t
        self.errors.append(msg)

    def peekPrecedence(self) -> int:
        p = precedences.get(self.peekToken.Type.TypeName)
        if p:
            return p

        return LOWEST

    def curPrecedence(self) -> int:
        p = precedences.get(self.curToken.Type.TypeName)
        if p:
            return p

        return LOWEST


def New(lex: lexer.Lexer) -> Parser:
    p: Parser = Parser(
        lex=lex,
        curToken=token.Token(Type=token.ILLEGAL, Literal='ILLEGAL'),
        peekToken=token.Token(Type=token.ILLEGAL, Literal='ILLEGAL'))
    p.registerPrefix(token.IDENT, p.parseIdentifier)
    p.registerPrefix(token.INT, p.parseIntegerLiteral)
    p.registerPrefix(token.BANG, p.parsePrefixExpression)
    p.registerPrefix(token.MINUS, p.parsePrefixExpression)
    p.registerInfix(token.PLUS, p.parseInfixExpression)
    p.registerInfix(token.MINUS, p.parseInfixExpression)
    p.registerInfix(token.SLASH, p.parseInfixExpression)
    p.registerInfix(token.ASTERISK, p.parseInfixExpression)
    p.registerInfix(token.EQ, p.parseInfixExpression)
    p.registerInfix(token.NOT_EQ, p.parseInfixExpression)
    p.registerInfix(token.LT, p.parseInfixExpression)
    p.registerInfix(token.GT, p.parseInfixExpression)
    p.registerPrefix(token.TRUE, p.parseBoolean)
    p.registerPrefix(token.FALSE, p.parseBoolean)
    p.registerPrefix(token.LPAREN, p.parseGroupedExpression)
    p.registerPrefix(token.IF, p.parseIfExpression)
    p.nextToken()
    p.nextToken()
    return p
