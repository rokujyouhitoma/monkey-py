import unittest
import _token as token
from _lexer import New


class TestNextToken(unittest.TestCase):
    def test_next_token(self):
        input = '''let five = 5;
let ten = 10;
let add = fn(x, y) {
 x + y;
};
let result = add(five, ten);
'''
        tests = [
            [token.LET, "let"],
            [token.IDENT, "five"],
            [token.ASSIGN, "="],
            [token.INT, "5"],
            [token.SEMICOLON, ";"],
            [token.LET, "let"],
            [token.IDENT, "ten"],
            [token.ASSIGN, "="],
            [token.INT, "10"],
            [token.SEMICOLON, ";"],
            [token.LET, "let"],
            [token.IDENT, "add"],
            [token.ASSIGN, "="],
            [token.FUNCTION, "fn"],
            [token.LPAREN, "("],
            [token.IDENT, "x"],
            [token.COMMA, ","],
            [token.IDENT, "y"],
            [token.RPAREN, ")"],
            [token.LBRACE, "{"],
            [token.IDENT, "x"],
            [token.PLUS, "+"],
            [token.IDENT, "y"],
            [token.SEMICOLON, ";"],
            [token.RBRACE, "}"],
            [token.SEMICOLON, ";"],
            [token.LET, "let"],
            [token.IDENT, "result"],
            [token.ASSIGN, "="],
            [token.IDENT, "add"],
            [token.LPAREN, "("],
            [token.IDENT, "five"],
            [token.COMMA, ","],
            [token.IDENT, "ten"],
            [token.RPAREN, ")"],
            [token.SEMICOLON, ";"],
            [token.EOF, ''],
        ]

        l = New(input)

        for i, tt in enumerate(tests):
            tok = l.NextToken()
            if tok.Type != tt[0]:
                self.fail('tests[%d] - tokentype wrong. expected="%s", got="%s"' % (i, tt[0], tok.Type))
            if tok.Literal != tt[1]:
                self.fail('tests[%d] - tokenliter wrong. expected="%s", got="%s"' % (i, tt[0], tok.Type))


if __name__ == '__main__':
    unittest.main()
