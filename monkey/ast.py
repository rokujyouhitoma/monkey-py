from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import List

from monkey import _token as token


class Node(metaclass=ABCMeta):
    @abstractmethod
    def TokenLiteral(self) -> str:
        pass


class Statement(metaclass=ABCMeta):
    @property
    @abstractmethod
    def Node(self) -> Node:
        pass

    @abstractmethod
    def statementNode(self):
        pass


class Expression(metaclass=ABCMeta):
    @property
    @abstractmethod
    def Node(self) -> Node:
        pass

    @abstractmethod
    def expressionNode(self):
        pass


@dataclass
class Program(Node):
    Statements: List[Statement]

    def TokenLiteral(self) -> str:
        if len(self.Statements) > 0:
            return self.Statements[0].TokenLiteral()
        else:
            return ''


@dataclass
class Identifier(Expression):
    Token: token.Token
    Value: str

    def expressionNode(self):
        pass

    def TokenLiteral(self) -> str:
        return self.Token.Literal


@dataclass
class LetStatement(Node, Statement):
    Token: token.Token
    Name: Identifier
    Value: Expression

    def statementNode(self):
        pass

    def TokenLiteral(self) -> str:
        return self.Token.Literal
