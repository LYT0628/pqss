from pqss.lex import Lexer
from pqss.parse.ast import *
from pqss.parse.parser import Parser


def eval_test(src_code: str, test):
    environment = Environment()

    lex = Lexer(src_code)
    p = Parser(lex)
    program = p.parse_program()
    qss = program.eval(environment)

    test(qss, environment)


def eval_lex_test(src_code: str, eval_code: str):
    def lex_test(qss, environment):
        lex0 = Lexer(qss)
        lex1 = Lexer(eval_code)

        while not lex0.is_end() and not lex1.is_end():
            tok0 = lex0.next_token()
            tok1 = lex1.next_token()

            assert tok0.token_type == tok1.token_type
            assert tok0.literal == tok1.literal

        assert lex0.is_end() and lex1.is_end()

    eval_test(src_code, lex_test)


def test_mixin_parsing():
    eval_lex_test('@mixin error($arg1, $arg2) {width:30;} ', '')


def test_include_parsing2():
    eval_lex_test("""@mixin error($a) {width:$a;} QPushButton { @include error(5) }""",
                  'QPushButton{width:5.0;}')


def test_import():
    eval_lex_test('@import "D:\DEV\code\pqss\pqss\parse\\tests\code.pqss"',
                  'QPushButton{height:6.0;width:5.0;}')
