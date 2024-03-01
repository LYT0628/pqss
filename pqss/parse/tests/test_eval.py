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


def eval_parse_test(src_code: str):
    eval_test(src_code,lambda qss, e: True)


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


def eval_env_test(src_code: str, pairs):
    def env_test(qss, e):
        for pair in pairs:
            assert e.get(pair[0]) == pair[1]

    eval_test(src_code, env_test)


def test_var():
    eval_env_test("$a: 5;", [('$a', 5)])
    eval_env_test("$a: 5; $b: $a;", [('$b', 5)])
    eval_env_test("$color: red;", [('$color', 'red')])
    eval_env_test("$color: #FF0000;", [('$color', '#FF0000')])
    eval_env_test("$color: rgba(255, 255, 255, 1);", [('$color', 'rgba(255.0,255.0,255.0,1.0);')])


def test_selector():
    eval_parse_test("* { width: 5px;} ")
    eval_parse_test("#id {width: 5px;}")
    eval_parse_test("QPushButton {width: 5px;}")
    eval_parse_test(".QPushButton {width: 5px;}")
    eval_parse_test("QWidget QPushButton {width: 5px;}")
    eval_parse_test("QWidget#container {width: 5px;}")
    eval_parse_test("QWidget > QPushButton {width: 5px;}")
    eval_parse_test("QWidget[color=danger] {width: 5px;}")
    eval_parse_test("QWidget[color~=danger] {width: 5px;}")
    eval_parse_test("QWidget { QPushButton {width: 5px;} }")
    eval_parse_test("QPushButton:hover {width: 5px;}")
    eval_parse_test("QCheckBox::indicator {width: 5px;}")
    eval_parse_test("QWidget { &:hover {width: 5px;} }")
    eval_parse_test("QMainWindow QWidget * {background: yellow;}")


def test_mixin_parsing():
    eval_lex_test('@mixin error($arg1, $arg2) {width:30;} ', '')


def test_include_parsing2():
    eval_lex_test("""@mixin error($a) {width:$a;} QPushButton { @include error(5) }""",
                  'QPushButton{width:5.0;}')


def test_import():
    eval_lex_test('@import "D:\DEV\code\pqss\pqss\parse\\tests\code.pqss"',
                  'QPushButton{height:6.0;width:5.0;}')
