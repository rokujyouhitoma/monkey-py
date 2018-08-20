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
    def node(self) -> Node:
        pass

    @abstractmethod
    def statementNode(self) -> None:
        pass

    @abstractmethod
    def TokenLiteral(self) -> str:
        pass


class Expression(metaclass=ABCMeta):
    @property
    @abstractmethod
    def node(self) -> Node:
        pass

    @abstractmethod
    def expressionNode(self) -> None:
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
class Identifier(Node, Expression):
    Token: token.Token
    Value: str

    @property
    def node(self) -> Node:
        pass

    def expressionNode(self) -> None:
        pass

    def TokenLiteral(self) -> str:
        return self.Token.Literal


@dataclass
class LetStatement(Node, Statement):
    Token: token.Token
    Name: Identifier
    Value: Expression

    @property
    def node(self) -> Node:
        pass

    def statementNode(self) -> None:
        pass

    def TokenLiteral(self) -> str:
        return self.Token.Literal


@dataclass
class ReturnStatement(Node, Statement):
    Token: token.Token
    ReturnValue: Expression

    @property
    def node(self) -> Node:
        pass

    def statementNode(self) -> None:
        pass

    def TokenLiteral(self) -> str:
        return self.Token.Literal
