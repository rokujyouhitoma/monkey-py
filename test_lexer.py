import unittest
import _token as token
from _lexer import New


class TestNextToken(unittest.TestCase):
    def test_next_token(self):
        input = '=+(){},;'
        tests = [
            [token.ASSIGN, '='],
            [token.PLUS, '+'],
            [token.LPAREN, '('],
            [token.RPAREN, ')'],
            [token.LBRACE, '{'],
            [token.RBRACE, '}'],
            [token.COMMA, ','],
            [token.SEMICOLON, ';'],
            [token.EOF, ''],
        ]

        l = New(input)

        for i, tt in enumerate(tests):
            tok = l.NextToken()
            if tok.Type != tt[0]:
                self.aassertLogs('tests[%d] - tokentype wrong. expected=%q, got=%q' % (i, tt[0], tok.Type))
            if tok.Literal != tt[1]:
                self.assertLogs('tests[%d] - tokentype wrong. expected=%q, got=%q' % (i, tt[0], tok.Type))


if __name__ == '__main__':
    unittest.main()
