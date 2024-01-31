from enum import Enum, auto


class TokenType(Enum):
    ILLEGAL = auto()  # unknown token
    EOF = auto()  # end of file

    # math
    ASSIGN = auto()  # :
    PLUS = auto()  # +
    SUB = auto()  # -
    MUL = auto()  # *
    DIV = auto()  # /
    EQ = auto()
    NOT_EQ = auto()
    LT = auto()
    GT = auto()

    TRUE = auto()
    FALSE = auto()

    IF = auto()
    ELSE = auto()

    IDENTIFIER = auto()  # id
    SEMICOLON = auto()  # ;
    COMMA = auto()

    LEFT_PAREN = auto()  # (
    RIGHT_PAREN = auto()  # )
    LEFT_BRACE = auto()  # {
    RIGHT_BRACE = auto()  # ｝

    NUMBER = auto()  # 1, 12, 3.0, 3.14
    STRING = auto()
    # 选择器   或许选择器不用分开编写， 可语义分析时候还是要用的
    GENERAL_SELECTOR = auto()  # *
    TYPE_SELECTOR = auto()  # .MyButton
    CLASS_SELECTOR = auto()  # QPushButton
    ID_SELECTOR = auto()  # #btn
    PROPERTY_SELECTOR = auto()  # QPushButton[name='abc']
    CHILDREN_SELECTOR = auto()  # >
    GROUP_SELECTOR = auto()  # #a, #b
    PARENT_REFERENCE = auto()
    # POSTERITY_SELECTOR = auto()
    PRODO_SELECTOR = auto()  # 伪类选择器 :hover
    SUBWIDGET_SELECTOR = auto()  # 子组件选择器 ::indicator
    COLOR = auto()

    # keywords
    IMPORT = auto()  # @import
    DEFAULT = auto()
    EXTEND = auto()
    MIXIN = auto()
    INCLUDE = auto()

    PROPERTY = auto()


keywords = {
    '@import': TokenType.IMPORT,
    '!default': TokenType.DEFAULT,
    '@extend': TokenType.EXTEND,
    '@mixin': TokenType.MIXIN,
    '@include': TokenType.INCLUDE,
    '@if': TokenType.IF,
    '@else': TokenType.ELSE,
    'true': TokenType.TRUE,
    'false': TokenType.FALSE
}

color = ['red', 'blue', 'white', 'yellow']
properties = ['left', 'width', 'background-color']


def is_property(lexeme: str):
    return lexeme in properties


def is_property_prefix(lexeme: str):
    return False


def is_color(lexeme: str):
    return False


def lookup_keyword(lexeme):
    return keywords.get(lexeme)


class Token:
    def __init__(self, token_type: TokenType | None, lexeme):
        self.token_type = token_type
        self.literal = lexeme
