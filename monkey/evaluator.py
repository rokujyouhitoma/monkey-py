import copy
from typing import Any, Dict, List, Optional, Tuple, cast

from monkey import ast, object

NULL = object.Null()
TRUE = object.Boolean(Value=True)
FALSE = object.Boolean(Value=False)


def Eval(node: Any, env: object.Environment) -> Optional[object.Object]:
    if type(node) == ast.Program:
        return evalProgram(node, env)
    elif type(node) == ast.ExpressionStatement:
        return Eval(node.ExpressionValue, env)
    elif type(node) == ast.IntegerLiteral:
        return object.Integer(Value=node.Value)
    elif type(node) == ast.Boolean:
        return nativeBoolToBooleanObject(node.Value)
    elif type(node) == ast.PrefixExpression:
        right = Eval(node.Right, env)
        if right:
            if isError(right):
                return right
            return evalPrefixExpression(node.Operator, right)
        else:
            return None
    elif type(node) == ast.InfixExpression:
        left = Eval(node.Left, env)
        if not left:
            return None
        if isError(left):
            return left
        right = Eval(node.Right, env)
        if not right:
            return None
        if isError(right):
            return right
        evaluated = evalInfixExpression(node.Operator, left, right)
        return evaluated
    elif type(node) == ast.BlockStatement:
        return evalBlockStatement(node, env)
    elif type(node) == ast.IfExpression:
        return evalIfExpression(node, env)
    elif type(node) == ast.ReturnStatement:
        val = Eval(node.ReturnValue, env)
        if val:
            if isError(val):
                return val
            return object.ReturnValue(Value=val)
        else:
            return None
    elif type(node) == ast.LetStatement:
        val = Eval(node.Value, env)
        if val:
            if isError(val):
                return val
            env.Set(node.Name.Value, val)
        else:
            return None
    elif type(node) == ast.Identifier:
        return evalIdentifier(node, env)
    elif type(node) == ast.FunctionLiteral:
        params = node.Parameters
        body = node.Body
        return object.Function(Parameters=params, Env=env, Body=body)
    elif type(node) == ast.CallExpression:
        if node.Function.TokenLiteral() == 'quote':
            return quote(node.Arguments[0])
        function = Eval(node.Function, env)
        if function:
            if isError(function):
                return function
        args = evalExpressions(node.Arguments, env)
        if len(args) == 1 and isError(args[0]):
            return args[0]
        if not function:
            return None
        return applyFunction(function, args)
    elif type(node) == ast.StringLiteral:
        return object.String(Value=node.Value)
    elif type(node) == ast.ArrayLiteral:
        elements = evalExpressions(node.Elements, env)
        if len(elements) == 1 and isError(elements[0]):
            return elements[0]
        return object.Array(Elements=elements)
    elif type(node) == ast.IndexExpression:
        left = Eval(node.Left, env)
        if not left:
            return None
        if isError(left):
            return left
        index = Eval(node.Index, env)
        if not index:
            return None
        if isError(index):
            return index
        return evalIndexExpression(left, index)
    elif type(node) == ast.HashLiteral:
        return evalHashLiteral(node, env)
    return None


def evalStatements(stmts: List[ast.Statement], env: object.Environment) -> Optional[object.Object]:
    result: Optional[object.Object]
    for statement in stmts:
        result = Eval(statement, env)
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
    elif left.Type.TypeName == object.STRING_OBJ and right.Type.TypeName == object.STRING_OBJ:
        return evalStringInfixExpression(operator, left, right)
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


def evalStringInfixExpression(operator: str, left: object.Object,
                              right: object.Object) -> object.Object:
    if operator != '+':
        return newError('unknown operator: %s %s %s',
                        (left.Type.TypeName, operator, right.Type.TypeName))

    leftVal = left.Value
    rightVal = right.Value
    return object.String(Value=leftVal + rightVal)


def evalIfExpression(ie: ast.IfExpression, env: object.Environment) -> object.Object:
    condition = Eval(ie.Condition, env)
    if not condition:
        return NULL
    if isError(condition):
        return condition
    if isTruthy(condition):
        if not ie.Consequence:
            return NULL
        evaluated = Eval(ie.Consequence, env)
        if not evaluated:
            return NULL
        return evaluated
    elif ie.Alternative is not None:
        if not ie.Alternative:
            return NULL
        evaluated = Eval(ie.Alternative, env)
        if not evaluated:
            return NULL
        return evaluated
    else:
        return NULL


def evalProgram(program: ast.Program, env: object.Environment) -> Optional[object.Object]:
    result: Optional[object.Object] = None
    for statement in program.Statements:
        result = Eval(statement, env)
        if type(result) == object.ReturnValue:
            if result is not None:
                return result.Value
        elif type(result) == object.Error:
            return result

    return result


def evalBlockStatement(block: ast.BlockStatement,
                       env: object.Environment) -> Optional[object.Object]:
    result: Optional[object.Object]
    for statement in block.Statements:
        result = Eval(statement, env)

        if result is not None:
            rt = result.Type.TypeName
            if rt == object.RETURN_VALUE_OBJ or rt == object.ERROR_OBJ:
                return result

    return result


def evalIdentifier(node: ast.Identifier, env: object.Environment) -> Optional[object.Object]:
    val = env.Get(node.Value)
    if val:
        return val

    builtin = builtins.get(node.Value)
    if builtin:
        return builtin

    return newError('identifier not found: ' + node.Value, tuple())


def evalExpressions(exps: List[ast.Expression], env: object.Environment) -> List[object.Object]:
    result: List[object.Object] = []

    for e in exps:
        evaluated = Eval(e, env)
        if evaluated:
            if isError(evaluated):
                return [object.AnyObject(evaluated)]
            result.append(evaluated)

    return result


def evalIndexExpression(left: object.Object, index: object.Object) -> object.Object:
    if left.Type.TypeName == object.ARRAY_OBJ and index.Type.TypeName == object.INTEGER_OBJ:
        value = evalArrayIndexExpression(left, index)
        if not value:
            return NULL
        return value
    elif left.Type.TypeName == object.HASH_OBJ:
        value = evalHashIndexExpression(left, index)
        if not value:
            return NULL
        return value
    else:
        return newError('index operator not supported: %s', (left.Type.TypeName, ))


def evalArrayIndexExpression(array: object.Object, index: object.Object) -> Optional[object.Object]:
    arrayObject = cast(object.Array, array)
    idx = index.Value
    max = int(len(arrayObject.Elements) - 1)

    if idx < 0 or idx > max:
        return None

    return arrayObject.Elements[idx]


def evalHashLiteral(node: ast.HashLiteral, env: object.Environment) -> object.Object:
    pairs: List[Tuple[object.HashKey, object.HashPair]] = []

    for keyNode, valueNode in node.Pairs:
        key = Eval(keyNode, env)
        if key:
            if isError(key):
                return key

        hashKey = key
        if not hashKey:
            if key:
                return newError('unusable as hash key: %s', (key.Type.TypeName, ))

        value = Eval(valueNode, env)
        if value:
            if isError(value):
                return value

        if hashKey:
            hashed = object.GetHashKey(hashKey)
            if key and value:
                pairs.append((hashed, object.HashPair(Key=key, Value=value)))

    return object.Hash(Pairs=pairs)


def evalHashIndexExpression(hash: object.Object, index: object.Object) -> Optional[object.Object]:
    hashObject = hash
    key = index
    if not key:
        return newError('unusable as hash key: %s', (index.Type.TypeName, ))
    # TODO: not hashable
    if not type(key) in (object.String, object.Integer, object.Boolean):
        return newError('unusable as hash key: %s', (index.Type.TypeName, ))

    hash = cast(object.Hash, hashObject)
    pair = object.GetHashPair(hash, object.GetHashKey(key))
    if not pair:
        return NULL

    return pair.Value


def applyFunction(fn: object.Object, args: List[object.Object]) -> Optional[object.Object]:
    if type(fn) == object.Function:
        function = cast(object.Function, fn)
        if not function:
            return newError('not a function: %s', (fn.Type.TypeName, ))

        extendedEnv = extendFunctionEnv(function, args)
        evaluated = Eval(function.Body, extendedEnv)
        if evaluated is not None:
            return unwrapReturnValue(evaluated)
        else:
            return None
    elif type(fn) == object.Builtin:
        builtin = cast(object.Builtin, fn)
        return builtin.Fn(args)
    else:
        return newError('not a function: %s', (fn.Type.TypeName, ))


def quote(node: ast.Node) -> object.Object:
    return object.Quote(Node=node)


def extendFunctionEnv(fn: object.Function, args: List[object.Object]) -> object.Environment:
    env = object.NewEnclosedEnvironment(fn.Env)

    for paramIdx, param in enumerate(fn.Parameters):
        env.Set(param.Value, args[paramIdx])

    return env


def unwrapReturnValue(obj: object.Object) -> object.Object:
    if type(obj) == object.ReturnValue:
        return obj.Value

    return obj


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


def builtin_len(args: List[object.Object]) -> object.Object:
    if len(args) != 1:
        return newError('wrong number of arguments. got=%s, want=1', (len(args), ))

    arg = args[0]
    if type(arg) == object.Array:
        arg = cast(object.Array, arg)
        return object.Integer(Value=int(len(arg.Elements)))
    elif type(arg) == object.String:
        return object.Integer(Value=int(len(arg.Value)))
    else:
        return newError('argument to \'len\' not supported, got %s', (args[0].Type.TypeName, ))


def builtin_first(args: List[object.Object]) -> object.Object:
    if len(args) != 1:
        return newError('wrong number of arguments. got=%s, want=1', (len(args), ))

    arg = args[0]
    if arg.Type.TypeName != object.ARRAY_OBJ:
        return newError('argument to `first` must be ARRAY, got %s', (args[0].Type.TypeName, ))

    arr = cast(object.Array, arg)
    if len(arr.Elements) > 0:
        return arr.Elements[0]

    return NULL


def builtin_last(args: List[object.Object]) -> object.Object:
    if len(args) != 1:
        return newError('wrong number of arguments. got=%s, want=1', (len(args), ))

    arg = args[0]
    if arg.Type.TypeName != object.ARRAY_OBJ:
        return newError('argument to `last` must be ARRAY, got %s', (args[0].Type.TypeName, ))

    arr = cast(object.Array, arg)
    length = len(arr.Elements)
    if length > 0:
        return arr.Elements[length - 1]

    return NULL


def builtin_rest(args: List[object.Object]) -> object.Object:
    if len(args) != 1:
        return newError('wrong number of arguments. got=%s, want=1', (len(args), ))

    arg = args[0]
    if arg.Type.TypeName != object.ARRAY_OBJ:
        return newError('argument to `rest` must be ARRAY, got %s', (args[0].Type.TypeName, ))

    arr = cast(object.Array, arg)
    length = len(arr.Elements)
    if length > 0:
        newElements = copy.deepcopy(arr.Elements[1:])
        return object.Array(Elements=newElements)

    return NULL


def builtin_push(args: List[object.Object]) -> object.Object:
    if len(args) != 2:
        return newError('wrong number of arguments. got=%s, want=2', (len(args), ))

    arg = args[0]
    if arg.Type.TypeName != object.ARRAY_OBJ:
        return newError('argument to `push` must be ARRAY, got %s', (args[0].Type.TypeName, ))

    arr = cast(object.Array, arg)

    newElements = copy.deepcopy(arr.Elements)
    newElements.append(args[1])

    return object.Array(Elements=newElements)


def builtin_puts(args: List[object.Object]) -> object.Object:
    for arg in args:
        print(arg.Inspect)

    return NULL


builtins: Dict[str, object.Builtin] = {
    'len': object.Builtin(Fn=builtin_len),
    'first': object.Builtin(Fn=builtin_first),
    'last': object.Builtin(Fn=builtin_last),
    'rest': object.Builtin(Fn=builtin_rest),
    'push': object.Builtin(Fn=builtin_push),
    'puts': object.Builtin(Fn=builtin_puts),
}
