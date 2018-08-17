from dataclasses import dataclass
from typing import TypeVar, Generic

from monkey import ast
from monkey import lexer
from monkey import _token as token


T = TypeVar('T')

@dataclass
class Parser(Generic[T]):
    l: lexer.Lexer
    curToken: token.Token
    peekToken: token.Token

    def New(self, l: lexer.Lexer) -> T:
        p = Parser(l = l)
        p.nextToken()
        p.nextToken()
        return p

    def nextToken(self):
        self.curToken = self.peekToken
        self.peekToken = self.l.NextToken()

    def ParseProgram(self) -> ast.Program:
        return None
