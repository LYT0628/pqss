from sqss.lex import Lexer
from sqss.parse.ast import *
from sqss.parse.parser import Parser


def test_mixin_parsing():
    tests = [('$a : 5; MyClass { width: $a; &:hover { width: $a + 3 * 5; &::indicator { width: $a + 3 * 5; } } } }', '$a', True)]
    for test in tests:
        lexer = Lexer(test[0])
        parser = Parser(lexer)
        style_sheet = parser.parse_sqss()
        qss = style_sheet.eval(Environment())
        print(qss)
