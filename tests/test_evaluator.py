import unittest
from dataclasses import dataclass
from typing import List

from monkey import evaluator, lexer, object, parser


class TestEvaluator(unittest.TestCase):
    def test_eval_integer_expression(self):
        @dataclass
        class Test():
            input: str
            expected: int

        tests: List[Test] = [
            Test('5', 5),
            Test('10', 10),
        ]

        for tt in tests:
            evaluated = testEval(tt.input)
            testIntegerObject(self, evaluated, tt.expected)


def testEval(input: str) -> object.Object:
    lex = lexer.New(input)
    p = parser.New(lex)
    program = p.ParseProgram()
    return evaluator.Eval(program)


def testIntegerObject(self, obj: object.Object, expected: int) -> bool:
    result = obj
    if not result:
        self.fail('object is not Integer. got=%s (%s)' % (obj, obj))
        return False

    if result.Value != expected:
        self.fail('object has wrong value. got=%s, want=%s' % (result.Value, expected))
        return False

    return True
