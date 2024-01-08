import pytest

from sqss.lex import TokenType, Token, Lexer, TokenUnKnownException


def test_next_token():
    input_str = ':+(){}'
    input_str += '$five : 5;'
    input_str += '$ten : 10;'
    input_str += '@import'
    input_str += """
        @import "./main.sqss"
        @import "./panel.qss" // 导入
        
        $var0 : 123px; // 变量
        $color : red;
        QPushButton {
            width: $var0 + 20px;
            background-color: $color;
        }
        
        QCheckBox {
            QPushButton() // 混入
        }
        // 注释1
        QCheckBox {
            $height : 6px !global; // 声明为全局变量
            background-color: blue;
            &::indicator {
                background-color: yellow;
            } // 父选择器 + 指示器
            &:checked {
                background-color: green;
            } // 父选择器 + 伪类
        }
        /*
            注释2
        */
        .MyWidget {
            border {
                left: 2px;
                right: 3 px;  
            }
        } // 属性嵌套
        // 数据类型
        // 数字 字符串 颜色 布尔值 空值 数组 映射
        // 插值语法 #｛｝
        // !default
        // @extend .MyWidget
        // %error 占位选择器 @extend %error
        // @mixin 混入 @include， 混入参数
    """

    expected_tokens = [Token(TokenType.ASSIGN, ':'),
                       Token(TokenType.PLUS, '+'),
                       Token(TokenType.LEFT_PAREN, '('),
                       Token(TokenType.RIGHT_PAREN, ')'),
                       Token(TokenType.LEFT_BRACE, '{'),
                       Token(TokenType.RIGHT_BRACE, '}'),
                       Token(TokenType.IDENTIFIER,'$five'),
                       Token(TokenType.ASSIGN, ':'),
                       Token(TokenType.NUMBER, 5),
                       Token(TokenType.SEMICOLON, ';'),
                       Token(TokenType.IDENTIFIER,'$ten'),
                       Token(TokenType.ASSIGN,  ':'),
                       Token(TokenType.NUMBER,  10),
                       Token(TokenType.SEMICOLON, ';'),
                       Token(TokenType.IMPORT, '@import')]

    lexer = Lexer(input_str)
    for expected_token in expected_tokens:
        tok = lexer.next_token()
        assert tok.token_type == expected_token.token_type
        assert tok.lexeme == expected_token.lexeme


def test_unknown_token():
    input_str = '~'
    lexer = Lexer(input_str)
    with pytest.raises(TokenUnKnownException):
        lexer.next_token()