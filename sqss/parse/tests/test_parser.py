import enum

from sqss.lex import Lexer, TokenType
from sqss.parse.ast import Statement, ExpressionStatement
from sqss.parse.parser import Parser


def test_var_statement():
    input_str = """
        $number : 5;
        $number;
    """

    lexer = Lexer(input_str)
    parser = Parser(lexer)
    sqss = parser.parse_sqss()

    tests = [('$number', '5'),
             ('$number', '$number')]

    def var_stmt_test(s, name, value):
        assert s.name.token.literal == name

    def int_literal_stmt_test(s, literal: str, value: float):
        assert s.expr.token.token_type == TokenType.NUMBER
        assert s.expr.token.literal == literal
        assert s.expr.value == value

    idx = 0
    for test in tests:
        stmt = sqss.statements[idx]
        var_stmt_test(stmt, test[0], test[1])


def test_int_literal_expr():
    input_str = """
        5;
    """

    lexer = Lexer(input_str)
    parser = Parser(lexer)
    sqss = parser.parse_sqss()

    tests = [('5', 5)]

    def int_literal_stmt_test(s, literal: str, value: float):
        assert s.expr.token.token_type == TokenType.NUMBER
        assert s.expr.token.literal == literal
        assert s.expr.value == value

    idx = 0
    for test in tests:
        stmt = sqss.statements[idx]
        int_literal_stmt_test(stmt, test[0], test[1])


def test_prefix_expr():
    tests = [('-5;', '-', '5'),
             ('-15;', '-', '15')]
    for test in tests:
        lexer = Lexer(test[0])
        parser = Parser(lexer)
        style_sheet = parser.parse_sqss()

        assert len(style_sheet.statements) == 1
        assert style_sheet.statements[0].expr.token.literal == test[1]
        assert style_sheet.statements[0].expr.right.token.literal == test[2]


def test_infix_expr():
    tests = [('5+5;', 5, '+', 5),
             ('5-5;', 5, '-', 5),
             ('5*5;', 5, '*', 5),
             ('5/5;', 5, '/', 5),
             ('5>5;', 5, '>', 5),
             ('5<5;', 5, '<', 5),
             ('5==5;', 5, '==', 5),
             ('5!=5;', 5, '!=', 5)]
    for test in tests:
        lexer = Lexer(test[0])
        parser = Parser(lexer)
        style_sheet = parser.parse_sqss()

        assert len(style_sheet.statements) == 1
        assert style_sheet.statements[0].expr.token.literal == test[2]
        assert style_sheet.statements[0].expr.left.value == test[1]
        assert style_sheet.statements[0].expr.right.value == test[3]


def test_boolean_expr():
    tests = [('$a:true;', '$a', True),
             ('$b:false;', '$b', False)]
    for test in tests:
        lexer = Lexer(test[0])
        parser = Parser(lexer)
        style_sheet = parser.parse_sqss()

        assert len(style_sheet.statements) == 1
        assert style_sheet.statements[0].name.token.literal == test[1]
        assert style_sheet.statements[0].value.expr.value == test[2]


def test_boolean_expr2():
    tests = [('$a>$b == true;', '$a', True),
             ('true != false;', '$b', False)]
    for test in tests:
        lexer = Lexer(test[0])
        parser = Parser(lexer)
        style_sheet = parser.parse_sqss()


def test_grouped_operator():
    tests = [('2 * (1 + 3);', '$a', True)]
    for test in tests:
        lexer = Lexer(test[0])
        parser = Parser(lexer)
        style_sheet = parser.parse_sqss()


def test_if_stmt_parsing():
    tests = [('@if $a>$b == true { $a:5; }', '$a', True),
             ('@if $a>$b == true {$a:true;} @else {$a:false;}', '$b', False)]
    for test in tests:
        lexer = Lexer(test[0])
        parser = Parser(lexer)
        style_sheet = parser.parse_sqss()


def test_mixin_parsing():
    tests = [('@mixin fn($arg, $arg1, $arg2){}', '$a', True),
             ('@if $a>$b == true {$a:true;} @else {$a:false;}', '$b', False)]
    for test in tests:
        lexer = Lexer(test[0])
        parser = Parser(lexer)
        style_sheet = parser.parse_sqss()

        # arg (, arg) (, arg)..


def test_include_parsing():
    tests = [('@include fn($arg, $arg1, $arg2);', '$a', True)]
    for test in tests:
        lexer = Lexer(test[0])
        parser = Parser(lexer)
        style_sheet = parser.parse_sqss()

        # arg (, arg) (, arg)...


def test_ruleset_parsing():
    test = """        
        QPushButton { 
            width: $var0 + 20;    // 单位   px  
            background-color: $color;   
        }"""
    lexer = Lexer(test)
    parser = Parser(lexer)
    style_sheet = parser.parse_sqss()
    print()
    # arg (, arg) (, arg)...
