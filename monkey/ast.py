from dataclasses import dataclass
from typing import Callable, List, Optional, Tuple, cast

from monkey import token


class Node:
    def TokenLiteral(self) -> str:
        pass

    def String(self) -> str:
        pass


class Statement(Node):
    def statementNode(self) -> None:
        pass

    def TokenLiteral(self) -> str:
        pass

    def String(self) -> str:
        pass


class Expression(Node):
    def node(self) -> Node:
        pass

    def expressionNode(self) -> None:
        pass

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
class Identifier(Expression):
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
class LetStatement(Statement):
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
class ReturnStatement(Statement):
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
class ExpressionStatement(Statement):
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
class IntegerLiteral(Expression):
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
class PrefixExpression(Expression):
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
class InfixExpression(Expression):
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
class Boolean(Expression):
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
class BlockStatement(Statement):
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
class IfExpression(Expression):
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
class FunctionLiteral(Expression):
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
class CallExpression(Expression):
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
class StringLiteral(Expression):
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
class ArrayLiteral(Expression):
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
class IndexExpression(Expression):
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
class HashLiteral(Expression):
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
            pairs.append(key.String() + ':' + value.String())

        out.append('{')
        out.append(', '.join(pairs))
        out.append('}')

        return ''.join(out)


ModifierFunc = Callable[[Node], Node]


def Modify(node: Node, modifier: ModifierFunc) -> Node:
    if type(node) == Program:
        node = cast(Program, node)
        for i, statement in enumerate(node.Statements):
            value = Modify(statement, modifier)
            value = cast(Statement, value)
            node.Statements[i] = value
    elif type(node) == ExpressionStatement:
        node = cast(ExpressionStatement, node)
        expression = node.ExpressionValue
        if expression:
            modified = Modify(expression, modifier)
            modified = cast(Expression, modified)
            node.ExpressionValue = modified
    elif type(node) == InfixExpression:
        node = cast(InfixExpression, node)
        if node.Left:
            modified = Modify(node.Left, modifier)
            modified = cast(Expression, modified)
            node.Left = modified
        if node.Right:
            modified = Modify(node.Right, modifier)
            modified = cast(Expression, modified)
            node.Right = modified
    elif type(node) == PrefixExpression:
        node = cast(PrefixExpression, node)
        if node.Right:
            modified = Modify(node.Right, modifier)
            modified = cast(Expression, modified)
            node.Right = modified
    elif type(node) == IndexExpression:
        node = cast(IndexExpression, node)
        if node.Left:
            node.Left = cast(Expression, Modify(node.Left, modifier))
        if node.Index:
            node.Index = cast(Expression, Modify(node.Index, modifier))
    elif type(node) == IfExpression:
        node = cast(IfExpression, node)
        node.Condition = cast(Expression, Modify(node.Condition, modifier))
        node.Consequence = cast(BlockStatement, Modify(node.Consequence, modifier))
        if node.Alternative is not None:
            node.Alternative = cast(BlockStatement, Modify(node.Alternative, modifier))
    elif type(node) == BlockStatement:
        node = cast(BlockStatement, node)
        for i, _ in enumerate(node.Statements):
            node.Statements[i] = cast(Statement, Modify(node.Statements[i], modifier))
    elif type(node) == ReturnStatement:
        node = cast(ReturnStatement, node)
        node.ReturnValue = cast(Expression, Modify(node.ReturnValue, modifier))
    elif type(node) == LetStatement:
        node = cast(LetStatement, node)
        node.Value = cast(Expression, Modify(node.Value, modifier))

    node = modifier(node)
    return node
