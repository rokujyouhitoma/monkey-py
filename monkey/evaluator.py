from typing import Any, List, Optional, Tuple

from monkey import ast, object

NULL = object.Null()
TRUE = object.Boolean(Value=True)
FALSE = object.Boolean(Value=False)


def Eval(node: Any) -> Optional[object.Object]:
    if type(node) == ast.Program:
        return evalProgram(node)
    elif type(node) == ast.ExpressionStatement:
        return Eval(node.ExpressionValue)
    elif type(node) == ast.IntegerLiteral:
        return object.Integer(Value=node.Value)
    elif type(node) == ast.Boolean:
        return nativeBoolToBooleanObject(node.Value)
    elif type(node) == ast.PrefixExpression:
        right = Eval(node.Right)
        if right:
            if isError(right):
                return right
            return evalPrefixExpression(node.Operator, right)
        else:
            return None
    elif type(node) == ast.InfixExpression:
        left = Eval(node.Left)
        if not left:
            return None
        if isError(left):
            return left
        right = Eval(node.Right)
        if not right:
            return None
        if isError(right):
            return right
        evaluated = evalInfixExpression(node.Operator, left, right)
        return evaluated
    elif type(node) == ast.BlockStatement:
        return evalBlockStatement(node)
    elif type(node) == ast.IfExpression:
        return evalIfExpression(node)
    elif type(node) == ast.ReturnStatement:
        val = Eval(node.ReturnValue)
        if val:
            if isError(val):
                return val
            return object.ReturnValue(Value=val)
        else:
            return None
    return None


def evalStatements(stmts: List[ast.Statement]) -> Optional[object.Object]:
    result: Optional[object.Object]
    for statement in stmts:
        result = Eval(statement)
        if type(result) == object.ReturnValue:
            returnValue = result
            if returnValue:
                return returnValue.Value
    return result


def evalPrefixExpression(operator: str, right: object.Object) -> object.Object:
    if operator == '!':
        return evalBangOperatorExpression(right)
    if operator == '-':
        return evalMinusPrefixOperatorExpression(right)
    else:
        return newError('unknown operator: %s%s', (operator, right.Type.TypeName))


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
        return newError('unknown operator: -%s', (right.Type.TypeName, ))

    value = right.Value
    return object.Integer(Value=-value)


def evalInfixExpression(operator: str, left: object.Object, right: object.Object) -> object.Object:
    if left.Type.TypeName == object.INTEGER_OBJ and right.Type.TypeName == object.INTEGER_OBJ:
        return evalIntegerInfixExpression(operator, left, right)
    elif operator == '==':
        return nativeBoolToBooleanObject(left == right)
    elif operator == '!=':
        return nativeBoolToBooleanObject(left != right)
    elif left.Type.TypeName != right.Type.TypeName:
        return newError('type mismatch: %s %s %s',
                        (left.Type.TypeName, operator, right.Type.TypeName))
    else:
        return newError('unknown operator: %s %s %s',
                        (left.Type.TypeName, operator, right.Type.TypeName))


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
        return newError('unknown operator: %s %s %s',
                        (left.Type.TypeName, operator, right.Type.TypeName))


def evalIfExpression(ie: ast.IfExpression) -> object.Object:
    condition = Eval(ie.Condition)
    if not condition:
        return NULL
    if isError(condition):
        return condition
    if isTruthy(condition):
        if not ie.Consequence:
            return NULL
        evaluated = Eval(ie.Consequence)
        if not evaluated:
            return NULL
        return evaluated
    elif ie.Alternative is not None:
        if not ie.Alternative:
            return NULL
        evaluated = Eval(ie.Alternative)
        if not evaluated:
            return NULL
        return evaluated
    else:
        return NULL


def evalProgram(program: ast.Program) -> Optional[object.Object]:
    result: Optional[object.Object]
    for statement in program.Statements:
        result = Eval(statement)
        if type(result) == object.ReturnValue:
            if result is not None:
                return result.Value
        elif type(result) == object.Error:
            return result

    return result


def evalBlockStatement(block: ast.BlockStatement) -> Optional[object.Object]:
    result: Optional[object.Object]
    for statement in block.Statements:
        result = Eval(statement)

        if result is not None:
            rt = result.Type.TypeName
            if rt == object.RETURN_VALUE_OBJ or rt == object.ERROR_OBJ:
                return result

    return result


def isTruthy(obj: object.Object) -> bool:
    if obj == NULL:
        return False
    elif obj == TRUE:
        return True
    elif obj == FALSE:
        return False
    else:
        return True


def isError(obj: object.Object) -> bool:
    if obj is not None:
        return obj.Type.TypeName == object.ERROR_OBJ

    return False


def nativeBoolToBooleanObject(input: bool) -> object.Boolean:
    return TRUE if input else FALSE


def newError(template: str, a: Tuple[Any, ...]) -> object.Error:
    return object.Error(Message=template % a)
