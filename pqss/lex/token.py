from .constants import (
    colors,
    properties,
    keywords,
    TokenType
)
"""
    
"""


def is_property(lexeme: str):
    """check if a literal is a QSS property"""
    return lexeme in properties


def is_color(lexeme: str):
    """check if a literal is a color string"""
    return lexeme in colors


def lookup_keyword(lexeme):
    """
        :param lexeme literal string
        :return if the lexeme if a keyword, return the TokenType, or return None
    """
    return keywords.get(lexeme)


class Token:
    """Token Entry"""
    def __init__(self, token_type: TokenType | None, lexeme):
        self.token_type = token_type
        self.literal = lexeme

    def __eq__(self, other):
        return (type(other) is Token
                and other.token_type == self.token_type
                and other.literal == self.literal)
