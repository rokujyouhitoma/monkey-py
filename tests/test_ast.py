import unittest

from monkey import ast, token


class TestAst(unittest.TestCase):
    def test_string(self):
        program = ast.Program(Statements=[
            ast.LetStatement(
                Token=token.Token(Type=token.LET, Literal='let'),
                Name=ast.Identifier(
                    Token=token.Token(Type=token.IDENT, Literal='myVar'), Value='myVar'),
                Value=ast.Identifier(
                    Token=token.Token(Type=token.IDENT, Literal='anotherVar'), Value='anotherVar'))
        ])

        if program.String() != 'let myVar = anotherVar;':
            self.fail('program.String() wrong. got=\'%s\'' % program.String())
