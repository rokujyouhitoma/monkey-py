from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from monkey import _token as token


class Node(metaclass=ABCMeta):
    @abstractmethod
    def TokenLiteral(self) -> str:
        pass

    @abstractmethod
    def String(self) -> str:
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

    @abstractmethod
    def String(self) -> str:
        pass


class Expression(metaclass=ABCMeta):
    @property
    @abstractmethod
    def node(self) -> Node:
        pass

    @abstractmethod
    def expressionNode(self) -> None:
        pass

    @abstractmethod
    def String(self) -> str:
        pass


@dataclass
class Program(Node):
    Statements: List[Statement]

    def TokenLiteral(self) -> str:
        if len(self.Statements) > 0:
            return self.Statements[0].TokenLiteral()
        else:
            return ''

    def String(self) -> str:
        return ''.join([s.String() for s in self.Statements])


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

    def String(self) -> str:
        return self.Value


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

    def String(self) -> str:
        out = []
        out.append(self.TokenLiteral() + ' ')
        out.append(self.Name.String())
        out.append(' = ')

        if self.Value is not None:
            out.append(self.Value.String())

        out.append(';')

        return ''.join(out)


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

    def String(self) -> str:
        out = []
        out.append(self.TokenLiteral() + ' ')

        if self.ReturnValue is not None:
            out.append(self.ReturnValue.String())

        out.append(';')

        return ''.join(out)


@dataclass
class ExpressionStatement(Node, Statement):
    Token: token.Token
    ExpressionValue: Optional[Expression]

    @property
    def node(self) -> Node:
        pass

    def statementNode(self) -> None:
        pass

    def TokenLiteral(self) -> str:
        return self.Token.Literal

    def String(self) -> str:
        if self.ExpressionValue is not None:
            return self.ExpressionValue.String()

        return ''
