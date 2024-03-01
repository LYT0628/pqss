from enum import Enum, auto


class TokenType(Enum):
    LEFT_BRACKET = auto()
    RIGHT_BRACKET = auto()
    UNION_SELECTOR = auto()
    BUILTIN = auto()
    LITERAL = auto()
    UNIT = auto()
    ILLEGAL = auto()
    """Unknown Token"""
    EOF = auto()
    """End of File"""

    ASSIGN = auto()
    """Assign, $var: val"""
    PLUS = auto()
    """ + """
    SUB = auto()
    """ a-b, or -a """
    MUL = auto()
    """ * """
    DIV = auto()
    """ / """
    EQ = auto()
    """ == """
    NOT_EQ = auto()
    """ != """
    LT = auto()
    """ < """
    GT = auto()
    """ > """

    TRUE = auto()
    """true"""
    FALSE = auto()
    """false"""

    IF = auto()
    """@if"""
    ELSE = auto()
    """@else"""

    IDENTIFIER = auto()
    """ name of variable"""
    SEMICOLON = auto()
    """ ; """
    COMMA = auto()
    """ , """
    LEFT_PAREN = auto()
    """("""
    RIGHT_PAREN = auto()
    """)"""
    LEFT_BRACE = auto()
    """{"""
    RIGHT_BRACE = auto()
    """}"""

    NUMBER = auto()
    """Number"""
    STRING = auto()
    """String"""

    UNIVERSAL_SELECTOR = auto()  # *
    TYPE_SELECTOR = auto()  # .MyButton
    CLASS_SELECTOR = auto()  # QPushButton
    ID_SELECTOR = auto()  # #btn
    PROPERTY_SELECTOR = auto()  # QPushButton[name='abc']
    CHILD_SELECTOR = auto()  # >
    GROUP_SELECTOR = auto()  # #a, #b
    PARENT_REFERENCE = auto()
    # POSTERITY_SELECTOR = auto()
    PRODO_SELECTOR = auto()  # 伪类选择器 :hover
    SUBWIDGET_SELECTOR = auto()  # 子组件选择器 ::indicator
    PROPERTY_CONTAINS_SELECTOR = auto()
    COLOR = auto()

    # keywords
    IMPORT = auto()  # @import
    DEFAULT = auto()
    EXTEND = auto()
    MIXIN = auto()
    INCLUDE = auto()

    PROPERTY = auto()


EOF = 0

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
""" Keywords of PQSS"""

colors = ['red',
          'blue',
          'white',
          'yellow',
          'green',
          'gray',
          'black',
          'orange',
          'grown']
"""The string for color """

properties = ['alternate-background-color',
              'background',
              'background-color',
              'background-image',
              'background-repeat',
              'background-position',
              'background-attachment',
              'background-clip',
              'background-origin',
              'border',
              'border-top',
              'border-right',
              'border-bottom',
              'border-left',
              'border-color',
              'border-top-color',
              'border-right-color',
              'border-bottom-color',
              'border-left-color',
              'border-image',
              'border-radius',
              'border-top-left-radius',
              'border-top-right-radius',
              'border-bottom-right-radius',
              'border-bottom-left-radius',
              'border-style',
              'border-top-style',
              'border-right-style',
              'border-bottom-style',
              'border-left-style',
              'border-width',
              'border-top-width',
              'border-right-width',
              'border-bottom-width',
              'border-left-width',
              'bottom',
              'button-layout',
              'color',
              'dialogbuttonbox-buttons-have-icons',
              'font',
              'font-family',
              'font-family',
              'font-size',
              'font-style',
              'font-weight',
              'height',
              'icon-size',
              'image',
              'image-position',
              'lineedit-password-character',
              'margin',
              'margin-top',
              'margin-right',
              'margin-bottom',
              'margin-left',
              'max-height',
              'max-width',
              'messagebox-text-interaction-flags',
              'min-height',
              'min-width',
              'opacity',
              'padding',
              'padding-top',
              'padding-right',
              'padding-bottom',
              'padding-left',
              'paint-alternating-row-color-for-empty-area',
              'position',
              'right',
              'selection-background-color',
              'selection-color',
              'show-decoration-selected',
              'spacing',
              'subcontrol-origin',
              'text-align',
              'text-decoration',
              'top',
              'width']
"""Qss properties"""
