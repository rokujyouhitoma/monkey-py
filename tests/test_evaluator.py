import unittest
from dataclasses import dataclass
from typing import Any, List

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
            Test('5 + 5 + 5 + 5 - 10', 10),
            Test('2 * 2 * 2 * 2 * 2', 32),
            Test('-50 + 100 + -50', 0),
            Test('5 * 2 + 10', 20),
            Test('5 + 2 * 10', 25),
            Test('20 + 2 * -10', 0),
            Test('50 / 2 * 2 + 10', 60),
            Test('2 * (5 + 10)', 30),
            Test('3 * 3 * 3 + 10', 37),
            Test('3 * (3 * 3) + 10', 37),
            Test('(5 + 10 * 2 + 15 / 3) * 2 + -10', 50),
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
            Test('1 < 2', True),
            Test('1 > 2', False),
            Test('1 < 1', False),
            Test('1 > 1', False),
            Test('1 == 1', True),
            Test('1 != 1', False),
            Test('1 == 2', False),
            Test('1 != 2', True),
            Test('true == true', True),
            Test('false == false', True),
            Test('true == false', False),
            Test('true != false', True),
            Test('false != true', True),
            Test('(1 < 2) == true', True),
            Test('(1 < 2) == false', False),
            Test('(1 > 2) == true', False),
            Test('(1 > 2) == false', True),
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

    def test_if_else_expressions(self):
        @dataclass
        class Test():
            input: str
            expected: Any

        tests: List[Test] = [
            Test('if (true) { 10 }', 10),
            Test('if (false) { 10 }', None),
            Test('if (1) { 10 }', 10),
            Test('if (1 < 2) { 10 }', 10),
            Test('if (1 > 2) { 10 }', None),
            Test('if (1 > 2) { 10 } else { 20 }', 20),
            Test('if (1 < 2) { 10 } else { 20 }', 10),
        ]

        for tt in tests:
            evaluated = testEval(tt.input)
            integer = tt.expected
            if integer:
                testIntegerObject(self, evaluated, int(integer))
            else:
                testNullObject(self, evaluated)

    def test_return_statements(self):
        @dataclass
        class Test():
            input: str
            expected: int

        tests: List[Test] = [
            Test('return 10;', 10),
            Test('return 10; 9;', 10),
            Test('return 2 * 5; 9;', 10),
            Test('9; return 2 * 5; 9;', 10),
            Test(
                '''
            if (10 > 1) {
              if (10 > 1) {
                return 10;
              }
              return 1;
            }
            ''', 10),
        ]

        for tt in tests:
            evaluated = testEval(tt.input)
            testIntegerObject(self, evaluated, tt.expected)

    def test_error_handling(self):
        @dataclass
        class Test():
            input: str
            expectedMessage: str

        tests: List[Test] = [
            Test('5 + true;', 'type mismatch: INTEGER + BOOLEAN'),
            Test('5 + true; 5;', 'type mismatch: INTEGER + BOOLEAN'),
            Test('-true', 'unknown operator: -BOOLEAN'),
            Test('true + false;', 'unknown operator: BOOLEAN + BOOLEAN'),
            Test('5; true + false; 5', 'unknown operator: BOOLEAN + BOOLEAN'),
            Test('if (10 > 1) { true + false; }', 'unknown operator: BOOLEAN + BOOLEAN'),
            Test(
                '''
            if (10 > 1) {
              if (10 > 1) {
                return true + false;
              }
              return 1;
            }
            ''', 'unknown operator: BOOLEAN + BOOLEAN'),
            Test('foobar', 'identifier not found: foobar'),
            Test('"Hello" - "World"', 'unknown operator: STRING - STRING'),
        ]

        for tt in tests:
            evaluated = testEval(tt.input)
            errObj = evaluated
            if errObj == evaluator.NULL:
                self.fail('no error object returned. got=%s(%s)' % (evaluated, evaluated))
                continue

            if errObj.Message != tt.expectedMessage:
                print(errObj.Message)
                self.fail('wrong error message. expected=%s, got=%s' % (tt.expectedMessage,
                                                                        errObj.Message))

    def test_let_statements(self):
        @dataclass
        class Test:
            input: str
            expected: int

        tests: List[Test] = [
            Test('let a = 5; a;', 5),
            Test('let a = 5 * 5; a;', 25),
            Test('let a = 5; let b = a; b;', 5),
            Test('let a = 5; let b = a; let c = a + b + 5; c;', 15),
        ]

        for tt in tests:
            testIntegerObject(self, testEval(tt.input), tt.expected)

    def test_function_object(self):
        input = 'fn(x) { x + 2; };'
        evaluated = testEval(input)

        fn = evaluated
        if not fn:
            self.fail('object is not Function. got=%s (%s)' % (evaluated, evaluated))

        if len(fn.Parameters) != 1:
            self.fail('function has wrong parameters. Parameters=%s' % fn.Parameters)

        if fn.Parameters[0].String() != 'x':
            self.fail('parameter is not \'x\'. got=%s' % fn.Parameters[0])

        expectedBody = '(x + 2)'

        if fn.Body.String() != expectedBody:
            self.fail('body is not %s. got=%s' % (expectedBody, fn.Body.String()))

    def test_function_application(self):
        @dataclass
        class Test:
            input: str
            expected: int

        tests: List[Test] = [
            Test('let identity = fn(x) { x; }; identity(5);', 5),
            Test('let identity = fn(x) { return x; }; identity(5);', 5),
            Test('let double = fn(x) { x * 2; }; double(5);', 10),
            Test('let add = fn(x, y) { x + y; }; add(5, 5);', 10),
            Test('let add = fn(x, y) { x + y; }; add(5 + 5, add(5, 5));', 20),
            Test('fn(x) { x; }(5)', 5),
        ]

        for tt in tests:
            testIntegerObject(self, testEval(tt.input), tt.expected)

    def test_closures(self):
        input = '''
        let newAdder = fn(x) {
          fn(y) { x + y };
        };

        let addTwo = newAdder(2);
        addTwo(2);'''
        testIntegerObject(self, testEval(input), 4)

    def test_string_literal(self):
        input = '"Hello World!"'
        evaluated = testEval(input)
        if not evaluated:
            self.fail('object is not String. got=%s (%s)' % (evaluated, evaluated))
        if evaluated.Value != 'Hello World!':
            self.fail('String has wrong value. got=%s' % str.Value)


def testNullObject(self, obj: object.Object) -> bool:
    if obj != evaluator.NULL:
        self.fail('object is not NULL. got=%s (%s)' % (obj, obj))
        return False
    return True


def testEval(input: str) -> object.Object:
    lex = lexer.New(input)
    p = parser.New(lex)
    program = p.ParseProgram()
    env = object.NewEnvironment()
    return evaluator.Eval(program, env)


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
