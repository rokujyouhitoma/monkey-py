from typing import Any, List, Optional

from monkey import ast, object


def Eval(node: Any) -> Optional[object.Object]:
    if type(node) == ast.Program:
        return evalStatements(node.Statements)
    elif type(node) == ast.ExpressionStatement:
        return Eval(node.ExpressionValue)
    elif type(node) == ast.IntegerLiteral:
        return object.Integer(Value=int(node.Value))
    return None


def evalStatements(stmts: List[ast.Statement]) -> Optional[object.Object]:
    result: Optional[object.Object]
    for statement in stmts:
        result = Eval(statement)
    return result
