import unittest

from monkey import ast, lexer, parser


class TestParser(unittest.TestCase):
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


def testLetStatement(self, s: ast.Statement, name: str) -> bool:
    if s.TokenLiteral() != 'let':
        self.fail('s.TokenLiteral not \'let\'. got=%s' % s.TokenLiteral())
        return False

    letStmt = s
    # TODO: xxx
    print(letStmt)

    if letStmt.Name.Value != name:
        self.fail('letStmt.Name.Value not \'%s\'. got=%s' % (name, letStmt.Name.Value))
        return False

    if letStmt.Name.TokenLiteral() != name:
        self.fail(
            'letStmt.Name.TokenLiteral() not \'%s\'. got=%s' % (name, letStmt.Name.TokenLiteral()))
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
