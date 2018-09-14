import argparse
import getpass

from monkey import evaluator, lexer, object, parser, repl


def main() -> None:
    argparser = argparse.ArgumentParser(description='')
    argparser.add_argument('infile', nargs='?', type=argparse.FileType('r'))
    args = argparser.parse_args()
    if args.infile:
        body = args.infile.read()
        if body:
            env = object.NewEnvironment()
            lex = lexer.New(body)
            p = parser.New(lex)

            program = p.ParseProgram()
            if len(p.Errors()) is not 0:
                for msg in p.Errors():
                    print('\t' + msg)
                return
            evaluated = evaluator.Eval(program, env)
            if evaluated:
                print(evaluated.Inspect)
    else:
        user = getpass.getuser()
        print('Hello {}! This is the Monkey programming language!\n'.format(user), end='')
        print('Feel free to type in commands\n', end='')
        repl.Start()


if __name__ == '__main__':
    main()
