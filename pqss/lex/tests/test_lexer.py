import pytest

from pqss.lex import TokenType, Token, Lexer, TokenUnKnownException


class Example:
    def __init__(self, src_code: str, expected_token: list[Token]):
        self.src_code = src_code
        self.expected_token = expected_token


def lex_test(ts: list[Example], predicate):
    for t in ts:
        lexer = Lexer(t.src_code)
        for tok in t.expected_token:
            assert predicate(lexer.next_token(), tok)


def lex_eq_test(ts: list[Example]):
    lex_test(ts, lambda tok, expected_tok: tok == expected_tok)


def test_assign():
    ts = [Example('$a:5',
                  [Token(TokenType.IDENTIFIER, '$a'),
                   Token(TokenType.ASSIGN, ':'),
                   Token(TokenType.NUMBER, '5')])]
    lex_eq_test(ts)


def test_extend():
    ts = [Example('@extend', [Token(TokenType.EXTEND, '@extend')])]
    lex_eq_test(ts)


def test_use_variable():
    ts = [Example("""
        $number : 5;
        MyClass {
            width : $number;
        }""", [Token(TokenType.IDENTIFIER, '$number'),
               Token(TokenType.ASSIGN, ':'),
               Token(TokenType.NUMBER, '5'),
               Token(TokenType.SEMICOLON, ';'),
               Token(TokenType.CLASS_SELECTOR, 'MyClass'),
               Token(TokenType.LEFT_BRACE, '{'),
               Token(TokenType.PROPERTY, 'width'),
               Token(TokenType.ASSIGN, ':'),
               Token(TokenType.IDENTIFIER, '$number'),
               Token(TokenType.SEMICOLON, ';'),
               Token(TokenType.RIGHT_BRACE, '}')])]
    lex_eq_test(ts)


def test_next_token():
    input_str = '@extend @mixin @include'
    input_str += '//:+(){}\n'
    input_str += '$five : 5; /* 大聪明 */'
    input_str += '$ten : 10;'
    input_str += '@import '
    input_str += '#IDSelector '
    input_str += '.ClassS > #SE error[name="XXX"] a:hover '
    input_str += ' .class{left:$a;}& a::indicator QPushButton() QPushButton($a,$b,$c)'
    input_str += """
        @import "./main.pqss"   // 1. Import 语句
        @import "./panel.qss" # 导入
        @extend @mixin @include // 2. 拓展语句   3.混入语句 4. Include语句
        $var0 : 123px; // 变量    // 5. If表达式语句
        $color : red;
        QPushButton { // 6.Ruleset 语句   
            width: $var0 + 20px;    // 7. Rule语句
            background-color: $color;   
        }

        QCheckBox {
            QPushButton() // 混入 8. 混入调用语句
        }
        // 注释1
        QCheckBox {
            $height : 6px !global; # 声明为全局变量
            background-color: blue;
            &::indicator {  
                background-color: yellow;
            } // 父选择器 + 指示器
            &:checked {
                background-color: green;
            } // 父选择器 + 伪类
        }
        @mixin fn(args){
            ruleset: bbb;
        }
        /*
            注释2
        */
        .MyWidget {
            border {    // 9. 属性嵌套语句
                left: 2px;
                right: 3 px;  
            }
        } // 属性嵌套
        // 数据类型
        // 数字 字符串 颜色 布尔值 空值 数组 映射
        // 插值语法 #｛｝
        // !default
        // @extend .MyWidget
        // %error 占位选择器 @extend %error  10.占位规则集语句
        // @mixin 混入 @include， 混入参数
    """

    expected_tokens = [Token(TokenType.EXTEND, '@extend'),
                       Token(TokenType.MIXIN, '@mixin'),
                       Token(TokenType.INCLUDE, '@include'),
                       Token(TokenType.IDENTIFIER, '$five'),
                       Token(TokenType.ASSIGN, ':'),
                       Token(TokenType.NUMBER, '5'),
                       Token(TokenType.SEMICOLON, ';'),
                       Token(TokenType.IDENTIFIER, '$ten'),
                       Token(TokenType.ASSIGN, ':'),
                       Token(TokenType.NUMBER, '10'),
                       Token(TokenType.SEMICOLON, ';'),
                       Token(TokenType.IMPORT, '@import'),
                       Token(TokenType.ID_SELECTOR, '#IDSelector'),
                       Token(TokenType.TYPE_SELECTOR, '.ClassS'),
                       Token(TokenType.CHILD_SELECTOR, '>'),
                       Token(TokenType.ID_SELECTOR, '#SE'),
                       Token(TokenType.PROPERTY_SELECTOR, 'error[name="XXX"]'),
                       Token(TokenType.PRODO_SELECTOR, 'a:hover'),
                       Token(TokenType.TYPE_SELECTOR, '.class'),
                       Token(TokenType.LEFT_BRACE, '{'),
                       Token(TokenType.PROPERTY, 'left'),
                       Token(TokenType.ASSIGN, ':'),
                       Token(TokenType.IDENTIFIER, '$a'),
                       Token(TokenType.SEMICOLON, ';'),
                       Token(TokenType.RIGHT_BRACE, '}'),
                       Token(TokenType.PARENT_REFERENCE, '&'),
                       Token(TokenType.SUBWIDGET_SELECTOR, 'a::indicator'),
                       Token(TokenType.CLASS_SELECTOR, 'QPushButton')
                       ]

    # '$a : 2 .class{left:$a}'
    lexer = Lexer(input_str)
    for expected_token in expected_tokens:
        tok = lexer.next_token()
        assert tok.token_type == expected_token.token_type
        assert tok.literal == expected_token.literal

    while lexer.next_token() is not None:
        pass


def test_unknown_token():
    input_str = '~'
    lexer = Lexer(input_str)
    with pytest.raises(TokenUnKnownException):
        lexer.next_token()
