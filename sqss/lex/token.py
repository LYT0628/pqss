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

    IDENTIFIER = auto()  # id
    SEMICOLON = auto()  # ;

    LEFT_PAREN = auto()  # (
    RIGHT_PAREN = auto()  # )
    LEFT_BRACE = auto()  # {
    RIGHT_BRACE = auto()  # ｝

    NUMBER = auto()  # 1, 12, 3.0, 3.14
    STRING = auto()
    # 选择器
    GENERAL_SELECTOR = auto()
    TYPE_SELECTOR = auto()
    CLASS_SELECTOR = auto()
    ID_SELECTOR = auto()
    PROPERTY_SELECTOR = auto()
    CHILDREN_SELECTOR = auto()
    POSTERITY_SELECTOR = auto()
    PRODO_SELECTOR = auto()
    SUBWIDGET_SELECTOR = auto()
    COLOR = auto()

    # keywords
    IMPORT = auto()  # @import
    DEFAULT = auto()
    EXTEND = auto()
    MIXIN = auto()
    INCLUDE = auto()


keywords = {
    '@import': TokenType.IMPORT,
    '!default': TokenType.DEFAULT,
    '@extend': TokenType.EXTEND,
    '@mixin': TokenType.MIXIN,
    '@include': TokenType.INCLUDE
}

color = ['red', 'blue', 'white', 'yellow']


def lookup_keyword(lexeme):
    return keywords[lexeme]


class Token:
    def __init__(self, token_type: TokenType | None, lexeme):
        self.token_type = token_type
        self.lexeme = lexeme
