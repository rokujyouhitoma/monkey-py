from typing import Any, List, Optional

from monkey import ast, object

NULL = object.Null()
TRUE = object.Boolean(Value=True)
FALSE = object.Boolean(Value=False)


def Eval(node: Any) -> Optional[object.Object]:
    if type(node) == ast.Program:
        return evalStatements(node.Statements)
    elif type(node) == ast.ExpressionStatement:
        return Eval(node.ExpressionValue)
    elif type(node) == ast.IntegerLiteral:
        return object.Integer(Value=node.Value)
    elif type(node) == ast.Boolean:
        return nativeBoolToBooleanObject(node.Value)
    elif type(node) == ast.PrefixExpression:
        right = Eval(node.Right)
        evaluated = evalPrefixExpression(node.Operator, right)
        return evaluated
    elif type(node) == ast.InfixExpression:
        left = Eval(node.Left)
        right = Eval(node.Right)
        evaluated = evalInfixExpression(node.Operator, left, right)
        return evaluated
    return None


def evalStatements(stmts: List[ast.Statement]) -> Optional[object.Object]:
    result: Optional[object.Object]
    for statement in stmts:
        result = Eval(statement)
    return result


def evalPrefixExpression(operator: str, right: Optional[object.Object]) -> object.Object:
    if operator == '!':
        return evalBangOperatorExpression(right)
    if operator == '-':
        return evalMinusPrefixOperatorExpression(right)
    else:
        return NULL


def evalBangOperatorExpression(right: Optional[object.Object]) -> object.Object:
    if right == TRUE:
        return FALSE
    elif right == FALSE:
        return TRUE
    elif right == NULL:
        return TRUE
    else:
        return FALSE


def evalMinusPrefixOperatorExpression(right: Optional[object.Object]) -> object.Object:
    if not right:
        return NULL
    if right.Type.TypeName != object.INTEGER_OBJ:
        return NULL

    value = right.Value
    return object.Integer(Value=-value)


def evalInfixExpression(operator: str, left: Optional[object.Object],
                        right: Optional[object.Object]) -> object.Object:
    if not right:
        return NULL
    if not left:
        return NULL
    if left.Type.TypeName == object.INTEGER_OBJ and right.Type.TypeName == object.INTEGER_OBJ:
        return evalIntegerInfixExpression(operator, left, right)
    elif operator == '==':
        return nativeBoolToBooleanObject(left == right)
    elif operator == '!=':
        return nativeBoolToBooleanObject(left != right)
    else:
        return NULL


def evalIntegerInfixExpression(operator: str, left: object.Object,
                               right: object.Object) -> object.Object:
    leftVal = left.Value
    rightVal = right.Value
    if operator == '+':
        return object.Integer(Value=leftVal + rightVal)
    elif operator == '-':
        return object.Integer(Value=leftVal - rightVal)
    elif operator == '*':
        return object.Integer(Value=leftVal * rightVal)
    elif operator == '/':
        return object.Integer(Value=leftVal / rightVal)
    elif operator == '<':
        return nativeBoolToBooleanObject(leftVal < rightVal)
    elif operator == '>':
        return nativeBoolToBooleanObject(leftVal > rightVal)
    elif operator == '==':
        return nativeBoolToBooleanObject(leftVal == rightVal)
    elif operator == '!=':
        return nativeBoolToBooleanObject(leftVal != rightVal)
    else:
        return NULL


def nativeBoolToBooleanObject(input: bool) -> object.Boolean:
    return TRUE if input else FALSE
