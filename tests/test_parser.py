import unittest
from dataclasses import dataclass

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


def checkParserErrors(self, p: parser.Parser) -> None:
    errors = p.Errors()
    if len(errors) == 0:
        return

    messages = []
    messages.append('parser has %s errors' % len(errors))
    for msg in errors:
        messages.append('parser error: %s' % msg)
    self.fail(messages)
