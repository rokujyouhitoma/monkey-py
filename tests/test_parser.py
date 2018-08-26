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
        input = '''
let x = 5;
let y = 10;
let foobar = 838383;
'''
        lex = lexer.New(input)
        p = parser.New(lex)

        program = p.ParseProgram()
        checkParserErrors(self, p)
        if program is None:
            self.fail('ParseProgram() returned None')
        if len(program.Statements) != 3:
            self.fail('program.Statements does not contain 3 statements. got=%s' % len(
                program.Statements))

        tests = [
            ['x'],
            ['y'],
            ['foobar'],
        ]

        for i, tt in enumerate(tests):
            stmt = program.Statements[i]
            if not testLetStatement(self, stmt, tt[0]):
                return

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
            integerValue: str

        prefixTests = [
            Prefix('!5;', '!', 5),
            Prefix('-15', '-', 15),
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

            if not testIntegerLiteral(self, exp.Right, tt.integerValue):
                return

    def test_parsing_infix_expressions(self):
        @dataclass
        class Infix():
            input: str
            leftValue: int
            operator: str
            rightValue: int

        infixTests: List[Infix] = [
            Infix('5 + 5;', 5, '+', 5),
            Infix('5 - 5;', 5, '-', 5),
            Infix('5 * 5;', 5, '*', 5),
            Infix('5 / 5;', 5, '/', 5),
            Infix('5 > 5;', 5, '>', 5),
            Infix('5 < 5;', 5, '<', 5),
            Infix('5 == 5;', 5, '==', 5),
            Infix('5 != 5;', 5, '!=', 5),
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

            if not testIntegerLiteral(self, exp.Left, tt.leftValue):
                return

            if exp.Operator != tt.operator:
                self.fail('exp.Operator is not \'%s\'. got=%s' % (tt.operator, exp.Operator))

            if not testIntegerLiteral(self, exp.Right, tt.rightValue):
                return

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
        ]

        for tt in tests:
            lex = lexer.New(tt.input)
            p = parser.New(lex)
            program = p.ParseProgram()
            checkParserErrors(self, p)
            actual = program.String()
            if actual != tt.expected:
                self.fail('expected=%s, got=%s' % (tt.expected, actual))


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


def checkParserErrors(self, p: parser.Parser) -> None:
    errors = p.Errors()
    if len(errors) == 0:
        return

    messages = []
    messages.append('parser has %s errors' % len(errors))
    for msg in errors:
        messages.append('parser error: %s' % msg)
    self.fail(messages)
