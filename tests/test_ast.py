import unittest

from monkey import token
from monkey.ast import Identifier, LetStatement, Program


class TestAst(unittest.TestCase):
    def test_string(self):
        program = Program(Statements=[
            LetStatement(
                Token=token.Token(Type=token.LET, Literal='let'),
                Name=Identifier(
                    Token=token.Token(Type=token.IDENT, Literal='myVar'), Value='myVar'),
                Value=Identifier(
                    Token=token.Token(Type=token.IDENT, Literal='anotherVar'), Value='anotherVar'))
        ])

        if program.String() != 'let myVar = anotherVar;':
            self.fail('program.String() wrong. got="%s"' % program.String())
