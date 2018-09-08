import unittest
from dataclasses import dataclass
from typing import Any, List

from monkey import ast, lexer, parser


class TestParser(unittest.TestCase):
    def test_return_statetments(self):
        input = '''
return 5;
return 10;
return 993322;
'''
        lex = lexer.New(input)
        p = parser.New(lex)

        program = p.ParseProgram()
        checkParserErrors(self, p)
        if len(program.Statements) != 3:
            self.fail('program.Statements does not contain 3 statements. got=%s' % len(
                program.Statements))

        for stmt in program.Statements:
            if type(stmt) != ast.ReturnStatement:
                self.fail('stmt not *ast.returnStatement. got=%s' % stmt)
                continue
            returnStmt = stmt
            if returnStmt.TokenLiteral() != 'return':
                self.fail(
                    'returnStmt.TokenLiteral not \'return\', got %s' % returnStmt.TokenLiteral())

    def test_let_statements(self):
        @dataclass
        class Test():
            input: str
            expectedIdentifier: str
            expectedValue: Any

        tests: List[Test] = [
            Test('let x = 5;', 'x', 5),
            Test('let y = true;', 'y', True),
            Test('let foobar = y;', 'foobar', 'y'),
        ]

        # let x = 5;
        # let y = 10;
        # let foobar = 838383;

        for tt in tests:
            lex = lexer.New(tt.input)
            p = parser.New(lex)
            program = p.ParseProgram()
            checkParserErrors(self, p)

            if program is None:
                self.fail('ParseProgram() returned None')
            if len(program.Statements) != 1:
                self.fail('program.Statements does not contain 1 statements. got=%s' % len(
                    program.Statements))

            stmt = program.Statements[0]
            if not testLetStatement(self, stmt, tt.expectedIdentifier):
                continue

            val = stmt.Value
            if not testLiteralExpression(self, val, tt.expectedValue):
                continue

    def test_identifier_expression(self):
        input = 'foobar;'

        lex = lexer.New(input)
        p = parser.New(lex)
        program = p.ParseProgram()
        checkParserErrors(self, p)
        if len(program.Statements) != 1:
            self.fail('program has not enough statements. got=%s' % len(program.Statements))
        stmt = program.Statements[0]

        ident = stmt.ExpressionValue
        if ident is None:
            self.fail('exp not *ast.Identifier. got=%s' % stmt.ExpressionValue)

        if ident.Value != 'foobar':
            self.fail('exp not *ast.Identifier. got=%s' % stmt.Expression)
        if ident.TokenLiteral() != 'foobar':
            self.fail('ident.TokenLiteral not %s. got=%s' % ('foobar', ident.TokenLiteral()))

    def test_integer_literal_expression(self):
        input = '5;'

        lex = lexer.New(input)
        p = parser.New(lex)
        program = p.ParseProgram()
        checkParserErrors(self, p)
        if len(program.Statements) != 1:
            self.fail('program has not enough statements. got=%s' % len(program.Statements))
        stmt = program.Statements[0]

        if stmt is None:
            self.fail('program.Statements[0] is not ast.ExpressionStatement. got=%s' % stmt)

        literal = stmt.ExpressionValue
        if literal is None:
            self.fail('exp not *ast.IntegerLiteral. got=%s' % stmt.ExpressionValue)

        if literal.Value != 5:
            self.fail('literal.Value not %s. got=%s' % (5, stmt.Expression))
        if literal.TokenLiteral() != '5':
            self.fail('literal.TokenLiteral not %s. got=%s' % ('5', literal.TokenLiteral()))

    def test_parsing_prefix_expressions(self):
        @dataclass
        class Prefix():
            input: str
            operator: str
            value: Any

        prefixTests = [
            Prefix('!5;', '!', 5),
            Prefix('-15', '-', 15),
            Prefix('!true;', '!', True),
            Prefix('!false;', '!', False),
        ]
        for tt in prefixTests:
            lex = lexer.New(tt.input)
            p = parser.New(lex)
            program = p.ParseProgram()
            checkParserErrors(self, p)
            if len(program.Statements) != 1:
                self.fail('program.Statements does not contain %s statements. got=%s' %
                          (lex, len(program.Statements)))

            stmt = program.Statements[0]

            if stmt is None:
                self.fail('program.Statements[0] is not ast.ExpressionStatement. got=%s' % stmt)

            exp = stmt.ExpressionValue
            if exp is None:
                self.fail('exp not *ast.PrefixExpression. got=%s' % stmt.ExpressionValue)
            if exp.Operator != tt.operator:
                self.fail('exp.Operator is not \'%s\'. got=%s' % (tt.operator, exp.Operator))

            if not testLiteralExpression(self, exp.Right, tt.value):
                continue

    def test_parsing_infix_expressions(self):
        @dataclass
        class Infix():
            input: str
            leftValue: Any
            operator: str
            rightValue: Any

        infixTests: List[Infix] = [
            Infix('5 + 5;', 5, '+', 5),
            Infix('5 - 5;', 5, '-', 5),
            Infix('5 * 5;', 5, '*', 5),
            Infix('5 / 5;', 5, '/', 5),
            Infix('5 > 5;', 5, '>', 5),
            Infix('5 < 5;', 5, '<', 5),
            Infix('5 == 5;', 5, '==', 5),
            Infix('5 != 5;', 5, '!=', 5),
            Infix('true == true', True, '==', True),
            Infix('true != false', True, '!=', False),
            Infix('false == false', False, '==', False),
        ]
        for tt in infixTests:
            lex = lexer.New(tt.input)
            p = parser.New(lex)
            program = p.ParseProgram()
            checkParserErrors(self, p)
            if len(program.Statements) != 1:
                self.fail('program.Statements does not contain %s statements. got=%s\n' %
                          (1, len(program.Statements)))

            stmt = program.Statements[0]
            if not stmt:
                self.fail('program.Statements[0] is not ast.ExpressionStatement. got=%s' %
                          program.Statements[0])

            exp = stmt.ExpressionValue
            if not exp:
                self.fail('exp is not ast.InfixExpression. got=%s' % stmt.ExpressionValue)

            if not testInfixExpression(self, stmt.ExpressionValue, tt.leftValue, tt.operator,
                                       tt.rightValue):
                continue

            if not testLiteralExpression(self, exp.Left, tt.leftValue):
                continue

            if exp.Operator != tt.operator:
                self.fail('exp.Operator is not \'%s\'. got=%s' % (tt.operator, exp.Operator))

            if not testLiteralExpression(self, exp.Right, tt.rightValue):
                continue

    def test_operator_precedence_parsing(self):
        @dataclass
        class Test():
            input: str
            expected: str

        tests: List[Test] = [
            Test('-a * b', '((-a) * b)'),
            Test('!-a', '(!(-a))'),
            Test('a + b + c', '((a + b) + c)'),
            Test('a + b - c', '((a + b) - c)'),
            Test('a * b * c', '((a * b) * c)'),
            Test('a * b / c', '((a * b) / c)'),
            Test('a + b / c', '(a + (b / c))'),
            Test('a + b * c + d / e - f', '(((a + (b * c)) + (d / e)) - f)'),
            Test('3 + 4; -5 * 5', '(3 + 4)((-5) * 5)'),
            Test('5 > 4 == 3 < 4', '((5 > 4) == (3 < 4))'),
            Test('5 < 4 != 3 > 4', '((5 < 4) != (3 > 4))'),
            Test('3 + 4 * 5 == 3 * 1 + 4 * 5', '((3 + (4 * 5)) == ((3 * 1) + (4 * 5)))'),
            Test('true', 'true'),
            Test('false', 'false'),
            Test('3 > 5 == false', '((3 > 5) == false)'),
            Test('3 < 5 == true', '((3 < 5) == true)'),
            Test('1 + (2 + 3) + 4', '((1 + (2 + 3)) + 4)'),
            Test('(5 + 5) * 2', '((5 + 5) * 2)'),
            Test('2 / (5 + 5)', '(2 / (5 + 5))'),
            Test('-(5 + 5)', '(-(5 + 5))'),
            Test('!(true == true)', '(!(true == true))'),
            Test('a + add(b * c) + d', '((a + add((b * c))) + d)'),
            Test('add(a, b, 1, 2 * 3, 4 + 5, add(6, 7 * 8))',
                 'add(a, b, 1, (2 * 3), (4 + 5), add(6, (7 * 8)))'),
            Test('add(a + b + c * d / f + g)', 'add((((a + b) + ((c * d) / f)) + g))'),
        ]

        for tt in tests:
            lex = lexer.New(tt.input)
            p = parser.New(lex)
            program = p.ParseProgram()
            checkParserErrors(self, p)
            actual = program.String()
            if actual != tt.expected:
                self.fail('expected=%s, got=%s' % (tt.expected, actual))

    def test_boolean_expression(self):
        input = 'true;'

        lex = lexer.New(input)
        p = parser.New(lex)
        program = p.ParseProgram()
        checkParserErrors(self, p)
        if len(program.Statements) != 1:
            self.fail('program has not enough statements. got=%s' % len(program.Statements))
        stmt = program.Statements[0]

        if stmt is None:
            self.fail('program.Statements[0] is not ast.ExpressionStatement. got=%s' % stmt)

        literal = stmt.ExpressionValue
        if literal is None:
            self.fail('exp not *ast.IntegerLiteral. got=%s' % stmt.ExpressionValue)

        if literal.Value is not True:
            self.fail('literal.Value not %s. got=%s' % (True, stmt.Expression))
        if literal.TokenLiteral() != 'true':
            self.fail('literal.TokenLiteral not %s. got=%s' % ('true', literal.TokenLiteral()))

    def test_if_expression(self):
        input = 'if (x < y) { x }'

        lex = lexer.New(input)
        p = parser.New(lex)
        program = p.ParseProgram()
        checkParserErrors(self, p)

        if len(program.Statements) != 1:
            self.fail('program.Statements does not contain %s statements. got=%s\n' %
                      (lex, len(program.Statements)))

        stmt = program.Statements[0]
        if stmt is None:
            self.fail('program.Statements[0] is not ast.ExpressionStatement. got=%s' % stmt)

        exp = stmt.ExpressionValue
        if exp is None:
            self.fail('stmt.Expression is not ast.IfExpression. got=%s' % stmt.Expression)

        if not testInfixExpression(self, exp.Condition, 'x', '<', 'y'):
            return

        if len(exp.Consequence.Statements) != 1:
            self.fail('consequence is not 1 statements. got=%s\n' % len(exp.Consequence.Statements))

        consequence = exp.Consequence.Statements[0]
        if consequence is None:
            self.fail('Statements[0] is not ast.ExpressionStatement. got=%s\n' %
                      exp.Consequence.Statements[0])

        if not testIdentifier(self, consequence.ExpressionValue, 'x'):
            return

        if exp.Alternative is not None:
            self.fail('exp.Alternative.Statements was not nil. got=%s', exp.Alternative)

    def test_if_else_expression(self):
        input = 'if (x < y) { x } else { y }'

        lex = lexer.New(input)
        p = parser.New(lex)
        program = p.ParseProgram()
        checkParserErrors(self, p)

        if len(program.Statements) != 1:
            self.fail('program.Statements does not contain %s statements. got=%s\n' %
                      (lex, len(program.Statements)))

        stmt = program.Statements[0]
        if not stmt:
            self.fail('program.Statements[0] is not ast.ExpressionStatement. got=%s' % stmt)

        exp = stmt.ExpressionValue
        if not exp:
            self.fail('stmt.Expression is not ast.IfExpression. got=%s' % stmt.Expression)

        if not testInfixExpression(self, exp.Condition, 'x', '<', 'y'):
            return

        if len(exp.Consequence.Statements) != 1:
            self.fail('consequence is not 1 statements. got=%s\n' % len(exp.Consequence.Statements))

        consequence = exp.Consequence.Statements[0]
        if not consequence:
            self.fail('Statements[0] is not ast.ExpressionStatement. got=%s\n' %
                      exp.Consequence.Statements[0])

        if not testIdentifier(self, consequence.ExpressionValue, 'x'):
            return

        if not exp.Alternative:
            self.fail('exp.Alternative.Statements was not nil. got=%s' % exp.Alternative)

    def test_function_literal_parsing(self):
        input = 'fn(x, y) { x + y; }'

        lex = lexer.New(input)
        p = parser.New(lex)
        program = p.ParseProgram()
        checkParserErrors(self, p)

        if len(program.Statements) != 1:
            self.fail('program.Statements does not contain %s statements. got=%s\n' %
                      (1, len(program.Statements)))

        stmt = program.Statements[0]
        if not stmt:
            self.fail('program.Statements[0] is not ast.ExpressionStatement. got=%s' %
                      program.Statements[0])

        function = stmt.ExpressionValue
        if not function:
            self.fail('stmt.Expression is not ast.FunctionLiteral. got=%s' % stmt.ExpressionValue)

        if len(function.Parameters) != 2:
            self.fail(
                'function literal parameters wrong. want 2, got=%s\n' % len(function.Parameters))

        testLiteralExpression(self, function.Parameters[0], 'x')
        testLiteralExpression(self, function.Parameters[1], 'y')

        if len(function.Body.Statements) != 1:
            self.fail('function.Body.Statements has not 1 statements. got=%s\n' % len(
                function.Body.Statements))

        bodyStmt = function.Body.Statements[0]
        if not bodyStmt:
            self.fail('function body stmt is not ast.ExpressionStatement. got=%s' %
                      function.Body.Statements[0])

        testInfixExpression(self, bodyStmt.ExpressionValue, 'x', '+', 'y')

    def test_function_parameter_parsing(self):
        @dataclass
        class Test():
            input: str
            expectedParams: List[str]

        tests: List[Test] = [
            Test(input='fn() {};', expectedParams=[]),
            Test(input='fn(x) {};', expectedParams=['x']),
            Test(input='fn(x, y, z) {};', expectedParams=['x', 'y', 'z']),
        ]

        for tt in tests:
            lex = lexer.New(tt.input)
            p = parser.New(lex)
            program = p.ParseProgram()
            checkParserErrors(self, p)

            stmt = program.Statements[0]
            function = stmt.ExpressionValue

            if len(function.Parameters) != len(tt.expectedParams):
                self.fail('length parameters wrong. want %d, got=%s\n' % (len(tt.expectedParams),
                                                                          len(function.Parameters)))

            for i, ident in enumerate(tt.expectedParams):
                testLiteralExpression(self, function.Parameters[i], ident)

    def test_call_expression_parsing(self):
        input = 'add(1, 2 * 3, 4 + 5);'

        lex = lexer.New(input)
        p = parser.New(lex)
        program = p.ParseProgram()
        checkParserErrors(self, p)

        if len(program.Statements) != 1:
            self.fail('program.Statements does not contain %s statements. got=%s\n' %
                      (1, len(program.Statements)))

        stmt = program.Statements[0]
        if not stmt:
            self.fail('stmt is not ast.ExpressionStatement. got=%s' % program.Statements[0])

        exp = stmt.ExpressionValue
        if not exp:
            self.fail('stmt.Expression is not ast.CallExpression. got=%s' % exp)

        if not testIdentifier(self, exp.Function, 'add'):
            return

        if len(exp.Arguments) != 3:
            self.fail('wrong length of arguments. got=%s' % len(exp.Arguments))

        testLiteralExpression(self, exp.Arguments[0], 1)
        testInfixExpression(self, exp.Arguments[1], 2, '*', 3)
        testInfixExpression(self, exp.Arguments[2], 4, '+', 5)

    def test_string_literal_expression(self):
        input = '"hello world";'

        lex = lexer.New(input)
        p = parser.New(lex)
        program = p.ParseProgram()
        checkParserErrors(self, p)

        stmt = program.Statements[0]
        literal = stmt.ExpressionValue
        if not literal:
            self.fail('exp not *ast.StringLiteral. got=%s' % stmt.Expression)

        if literal.Value != 'hello world':
            self.fail('literal.Value not %s. got=%s' % ('hello world', literal.Value))


def testLetStatement(self, s: ast.Statement, name: str) -> bool:
    if s.TokenLiteral() != 'let':
        self.fail('s.TokenLiteral not \'let\'. got=%s' % s.TokenLiteral())
        return False

    letStmt = s
    # TODO: xxx
    # print(letStmt)

    if letStmt.Name.Value != name:
        self.fail('letStmt.Name.Value not \'%s\'. got=%s' % (name, letStmt.Name.Value))
        return False

    if letStmt.Name.TokenLiteral() != name:
        self.fail(
            'letStmt.Name.TokenLiteral() not \'%s\'. got=%s' % (name, letStmt.Name.TokenLiteral()))
        return False

    return True


def testIntegerLiteral(self, il: ast.Expression, value: int) -> bool:
    integ = il
    if not integ:
        self.fail('il not *ast.IntegerLiteral. got=%s' % il)
        return False
    if integ.Value != value:
        self.fail('integ.Value not %s. got=%s' % (value, integ.Value))
        return False
    if integ.TokenLiteral() != str(value):
        self.fail('integ.TokenLiteral not %s. got=%s' % (value, integ.TokenLiteral()))
        return False
    return True


def testIdentifier(self, exp: ast.Expression, value: str) -> bool:
    ident = exp
    if ident is None:
        self.fail('exp not *ast.Identifier. got=%s' % exp)
        return False

    if ident.Value != value:
        self.fail('ident.Value not %s. got=%s' % (value, ident.Value))
        return False

    if ident.TokenLiteral() != value:
        self.fail('ident.TokenLiteral not %s. got=%s' % (value, ident.TokenLiteral()))
        return False

    return True


def testLiteralExpression(self, exp: ast.Expression, expected: Any) -> bool:
    v = type(expected)
    if v is int:
        return testIntegerLiteral(self, exp, int(expected))
    elif v is str:
        return testIdentifier(self, exp, str(expected))
    elif v is bool:
        return testBooleanLietral(self, exp, bool(expected))
    self.fail('type of exp not handled. got=%s' % exp)
    return False


def testInfixExpression(self, exp: ast.Expression, left: Any, operator: str, right: Any) -> bool:
    opExp = exp
    if opExp is None:
        self.fail('exp is not ast.InfixExpression. got=%s(%s)' % (exp, exp))
        return False

    if not testLiteralExpression(self, opExp.Left, left):
        return False

    if opExp.Operator != operator:
        self.fail('exp.Operator is not \'%s\'. got=%s' % (operator, opExp.Operator))
        return False

    if not testLiteralExpression(self, opExp.Right, right):
        return False

    return True


def testBooleanLietral(self, exp: ast.Expression, value: bool) -> bool:
    bo = exp
    if bo is None:
        self.fail('exp not *ast.Boolean. got=%s' % exp)
        return False

    if bo.Value != value:
        self.fail('bo.Value not %s. got=%s' % (value, bo.Value))
        return False

    if bo.TokenLiteral() != str(value).lower():
        self.fail('bo.TokenLiteral not %s. got=%s' % (value, bo.TokenLiteral()))
        return False

    return True


def checkParserErrors(self, p: parser.Parser) -> None:
    errors = p.Errors()
    if len(errors) == 0:
        return

    messages = []
    messages.append('parser has %s errors' % len(errors))
    for msg in errors:
        messages.append('parser error: %s' % msg)
    self.fail('\n'.join(messages))
