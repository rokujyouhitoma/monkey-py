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
            Test('-5', -5),
            Test('-10', -10),
        ]

        for tt in tests:
            evaluated = testEval(tt.input)
            testIntegerObject(self, evaluated, tt.expected)

    def test_eval_boolean_expression(self):
        @dataclass
        class Test():
            input: str
            expected: bool

        tests: List[Test] = [
            Test('true', True),
            Test('false', False),
        ]

        for tt in tests:
            evaluated = testEval(tt.input)
            testBooleanObject(self, evaluated, tt.expected)

    def test_bang_operator(self):
        @dataclass
        class Test():
            input: str
            expected: bool

        tests: List[Test] = [
            Test('!true', False),
            Test('!false', True),
            Test('!5', False),
            Test('!!true', True),
            Test('!!false', False),
            Test('!!5', True),
        ]

        for tt in tests:
            evaluated = testEval(tt.input)
            testBooleanObject(self, evaluated, tt.expected)


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


def testBooleanObject(self, obj: object.Object, expected: bool) -> bool:
    result = obj
    if not result:
        self.fail('object is not Boolean. got=%s (%s)' % (obj, obj))
        return False

    if result.Value != expected:
        self.fail('object has wrong value. got=%s, want=%s' % (result.Value, expected))
        return False

    return True
