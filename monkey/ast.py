from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Tuple

from monkey import token


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


@dataclass
class IntegerLiteral(Node, Expression):
    Token: token.Token
    Value: int

    @property
    def node(self) -> Node:
        pass

    def expressionNode(self) -> None:
        pass

    def TokenLiteral(self) -> str:
        return self.Token.Literal

    def String(self) -> str:
        return self.Token.Literal


@dataclass
class PrefixExpression(Node, Expression):
    Token: token.Token
    Operator: str
    Right: Optional[Expression]

    @property
    def node(self) -> Node:
        pass

    def expressionNode(self) -> None:
        pass

    def TokenLiteral(self) -> str:
        return self.Token.Literal

    def String(self) -> str:
        out: List[str] = []
        out.append('(')
        out.append(self.Operator)
        if self.Right is not None:
            out.append(self.Right.String())
        out.append(')')
        return ''.join(out)


@dataclass
class InfixExpression(Node, Expression):
    Token: token.Token
    Left: Optional[Expression]
    Operator: str
    Right: Optional[Expression]

    @property
    def node(self) -> Node:
        pass

    def expressionNode(self) -> None:
        pass

    def TokenLiteral(self) -> str:
        return self.Token.Literal

    def String(self) -> str:
        out: List[str] = []
        out.append('(')
        if self.Left is not None:
            out.append(self.Left.String())
        out.append(' ' + self.Operator + ' ')
        if self.Right is not None:
            out.append(self.Right.String())
        out.append(')')
        return ''.join(out)


@dataclass
class Boolean(Node, Expression):
    Token: token.Token
    Value: bool

    @property
    def node(self) -> Node:
        pass

    def expressionNode(self) -> None:
        pass

    def TokenLiteral(self) -> str:
        return self.Token.Literal

    def String(self) -> str:
        return self.Token.Literal


@dataclass
class BlockStatement(Node, Expression):
    Token: token.Token
    Statements: List[Statement]

    @property
    def node(self) -> Node:
        pass

    def expressionNode(self) -> None:
        pass

    def TokenLiteral(self) -> str:
        return self.Token.Literal

    def String(self) -> str:
        out: List[str] = []
        for s in self.Statements:
            out.append(s.String())
        return ''.join(out)


@dataclass
class IfExpression(Node, Expression):
    Token: token.Token
    Condition: Expression
    Consequence: BlockStatement
    Alternative: Optional[BlockStatement]

    @property
    def node(self) -> Node:
        pass

    def expressionNode(self) -> None:
        pass

    def TokenLiteral(self) -> str:
        return self.Token.Literal

    def String(self) -> str:
        out: List[str] = []
        out.append('if')
        out.append(self.Condition.String())
        out.append(' ')
        out.append(self.Consequence.String())
        if self.Alternative is not None:
            out.append('else ')
            out.append(self.Alternative.String())
        return ''.join(out)


@dataclass
class FunctionLiteral(Node, Expression):
    Token: token.Token
    Parameters: List[Identifier]
    Body: BlockStatement

    @property
    def node(self) -> Node:
        pass

    def expressionNode(self) -> None:
        pass

    def TokenLiteral(self) -> str:
        return self.Token.Literal

    def String(self) -> str:
        out: List[str] = []
        params: List[str] = []
        for p in self.Parameters:
            params.append(p.String())
        out.append(self.TokenLiteral())
        out.append('(')
        out.append(','.join(params))
        out.append(')')
        out.append(self.Body.String())
        return ''.join(out)


@dataclass
class CallExpression(Node, Expression):
    Token: token.Token
    Function: Expression
    Arguments: List[Expression]

    @property
    def node(self) -> Node:
        pass

    def expressionNode(self) -> None:
        pass

    def TokenLiteral(self) -> str:
        return self.Token.Literal

    def String(self) -> str:
        out: List[str] = []
        args: List[str] = []
        for a in self.Arguments:
            args.append(a.String())
        out.append(self.Function.String())
        out.append('(')
        out.append(', '.join(args))
        out.append(')')
        return ''.join(out)


@dataclass
class StringLiteral(Node, Expression):
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
        return self.Token.Literal


@dataclass
class ArrayLiteral(Node, Expression):
    Token: token.Token
    Elements: List[Expression]

    @property
    def node(self) -> Node:
        pass

    def expressionNode(self) -> None:
        pass

    def TokenLiteral(self) -> str:
        return self.Token.Literal

    def String(self) -> str:
        out: List[str] = []

        elements: List[str] = []
        for el in self.Elements:
            elements.append(el.String())

        out.append('[')
        out.append(', '.join(elements))
        out.append(']')

        return ''.join(out)


@dataclass
class IndexExpression(Node, Expression):
    Token: token.Token
    Left: Expression
    Index: Expression

    @property
    def node(self) -> Node:
        pass

    def expressionNode(self) -> None:
        pass

    def TokenLiteral(self) -> str:
        return self.Token.Literal

    def String(self) -> str:
        out: List[str] = []

        out.append('(')
        out.append(self.Left.String())
        out.append('[')
        out.append(self.Index.String())
        out.append('])')

        return ''.join(out)


@dataclass
class HashLiteral(Node, Expression):
    Token: token.Token
    Pairs: List[Tuple[Expression, Expression]]

    @property
    def node(self) -> Node:
        pass

    def expressionNode(self) -> None:
        pass

    def TokenLiteral(self) -> str:
        return self.Token.Literal

    def String(self) -> str:
        out: List[str] = []

        pairs: List[str] = []
        for key, value in self.Pairs:
            # value = self.Pairs[key]
            pairs.append(key.String() + ':' + value.String())

        out.append('{')
        out.append(', '.join(pairs))
        out.append('}')

        return ''.join(out)
