 
 - oreilly-978-4-87311-822-2e.pdf

# Requirements
  
 - Python3.7.0

# Tools

 - isort
 - yapf
 - flake8
 - mypy

# TODO

 - 4.5.4: Improvement of Dict[HashKey, HashPair] structure.

# Histories

## 2018.09.24

 - A.4.2.1: P262-264 Macro Support for Boolean.
 - A.4: P242-261 Macro Support for unquote(HashLiteral) builtin function.

## 2018.09.24

 - A.4: P242-261 Macro Support for unquote(FunctionLiteral, ArrayLiteral) builtin function.
 - Refactoring.

## 2018.09.23
 
 - A.4: P242-261 Macro Support for unquote(LetStatement) builtin function.

## 2018.09.22

 - A.4: P242-261 Macro Support for unquote(IfExpression, ReturnStatement) builtin function.

## 2018.09.21

 - A.4: P242-261 Macro Support for unquote(Program, ExpressionStatement, InfixExpression, PrefixExpression, IndexExpression) builtin function.
 - A.3: P238-242 Macro. Support for quote builtin function.

## 2018.09.20

 - 4.6: P230-231 Suppot for puts builtin function.
 - 4.5.5: P226-229 Eval. Support for Hash.

## 2018.09.19

 - 4.5.4: P223-226 Eval. Support for HashLiteral.

## 2018.09.18

 - 4.5.3: P218-223 Object. Support for Hash.

## 2018.09.17

 - 4.5.2: P213-218 Parser. Support for HashLiteral.
 - Fixed bugs at evaluator.py and Add regression test case.
 - private comment: so...Today, PyConJP 2018 has come!

## 2018.09.16

 - 4.5.1: P211-213 Lexer. Support for token.COLON.

## 2018.09.15

 - Improvement of REPL. REPL support for input-file with 4.4.7: P209-210.

## 2018.09.14

 - 4.4.6: P205-208 Support for Array BuiltinFunctions.

## 2018.09.13

 - 4.4.5: P201-205 Eval. Support for ArrayLiteral.

## 2018.09.12

 - 4.4.4: P198-201  Eval. Support for Array.
 - 4.4.3: P195-199: Parser. Support for IndexLiteral.
 - 4.4.2: P192-195: Parser. Support for ArrayLiteral.
 - 4.4.1: P190-192: Lexer. Support for Array.

## 2018.09.11

 - 4.3.1: P184-189: Support for builtin function len.

## 2018.09.10

 - 4.2.4: P182-183: Support for string concat feature.

## 2018.09.09

 - 4.2.3: P180-182: Eval. Support for ast.StringLiteral

## 2018.09.08

 - 4.2.2: P179-180: Parser. Support for token.STRING

## 2018.09.07

 - 4.2.1: P176-178: Lexer. Support for token.STRING
 - Refactoring: move environmment.Environment into object.Environment

## 2018.09.06

 - 3.10: P160-171 Eval. FunctionLiteral, CallExpression, applyFunction, EnclosedEnvironment

## 2018.09.05

 - 3.9: P155-160 Eval. LetStatement(Environment and Bind)

## 2018.09.04

 - 3.8: P149-154 Eval. Error for debug

## 2018.09.03

 - 3.7: P144-149 Eval. Return statements

## 2018.09.02

 - 3.6: P141-144 Eval. IfExpression

## 2018.09.01

 - 3.5.6: P135-141 Eval. InfixExpression
 - 3.5.5: P131-135 Eval. BangOperator
 - 3.5.4: P131 Eval. null
 - 3.5.3: P129-131 Eval. Boolean Literal
 - Refactoring test case

## 2018.08.31

 - 3.5.2: P128-129 REPL(Read, Eval, Print, Loop)
 - 3.5.1. P124-128 Eval。IntegerLiteral
 - 3.4.4: P123-124 Eval。null
 - 3.4.3: P123 Eval。Boolean
 - 3.4.2: P122 Eval。Integer
 - 3.4.1: P121-122 Eval。Object
 - 2.9: P112-113 REPLの改善。RPPL(Read, Parse, Print, Loop)

## 2018.08.30

 - 2.8.6: P109-111 Parserの改善。

## 2018.08.29

 - 2.8: P104-109 Parserの改善。呼び出し式（CallExpression）のサポート

## 2018.08.28

 - 2.8: P99-104 Parserの改善。関数リテラル（FunctionLiteral）のサポート
 - 2.8: P93-99 Parserの改善。if式（IfExpression）のサポート

## 2018.08.27

 - 2.8: P91-93 Parserの改善。GroupingExpressionのサポート
 - 2.8: P87-91 Parserの改善。真偽値リテラル（BooleanLiteral）のサポート

## 2018.08.26

 - 2.8: P85-87 test helperの拡充
 - 2.6: P73-75 Parserの中置演算子（InfixExpression）テストケースを拡充

## 2018.08.25

 - 2.6: P68-73 Parserの改善。中置演算子（InfixExpression）のサポート

## 2018.08.24

 - 2.6: P63-68 Parserの改善。前置演算子（PrefixExpression)のサポート

## 2018.08.23

 - 2.6: P60-63 Praserの改善。IntegerLiteralのサポート

## 2018.08.22

 - Refactoring: token namespace

## 2018.08.21

 - 2.6: P54-60 ExpressionStatementの実装
 - 2.6: P47-54 ASTにExpressionStatementの追加

## 2018.08.20

 - 2.5: P44-47 return statement

## 2018.08.19

 - 2.4: P41-44 Parserのエラーメッセージを拡充
 - annotate Type for mypy
 - Tools: isort, yapf, flake8, mypyを採用

## 2018.08.18

 - 2.4: P35-P41 Parserの改善。letのサポート
 - Refactoring: tests cases

## 2018.08.17

 - 2.4: P29-35 Parser(parser.py)の実装
 - 2.3: P29-32 AST(ast.py)の実装
 - 2.2: P28-29
 - 2.1: P25-28
 - Refactoring: monkeyパッケージを作成、tests/ディレクトリの作成

## 2018.08.16

 - 1.4: P21-22 REPLの実装
 - 1.4: P18-21 Lexerの改善。==、!=のサポート
 - 1.4: P17-18 Lexerの改善。キーワード（if, else, return, true, false）のサポート
 - 1.4: P14-17 Lexerの改善。演算子のサポート
 - 1.3: P12-14 Lexerの改善。Numberのサポート。let, fnのキーワードのサポート

## 2018.08.15

 - 1.3: P1-11 Lexer, tokenの最小構成の定義
