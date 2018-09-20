from typing import List

from monkey import evaluator, lexer, object, parser

PROMPT = '>> '


def Start() -> None:
    env = object.NewEnvironment()
    while True:
        try:
            line = input(PROMPT)
        except KeyboardInterrupt:
            print('\nKeyboardInterrupt')
            continue

        if line == 'exit()':
            break

        lex = lexer.New(line)
        p = parser.New(lex)

        program = p.ParseProgram()
        if len(p.Errors()) is not 0:
            printParserErrors(p.Errors())
            continue

        evaluator.Eval(program, env)


def printParserErrors(errors: List[str]) -> None:
    for msg in errors:
        print('\t' + msg)
