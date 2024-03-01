from ..lex import Token, TokenType


def expect_token_type(tok: Token | None, expected_type: TokenType):
    return tok.token_type == expected_type


def is_selector_tok(tok: Token | None):
    """

    :param tok:
    :return:
    """
    return tok.token_type in [TokenType.UNIVERSAL_SELECTOR,
                              TokenType.TYPE_SELECTOR,
                              TokenType.PROPERTY_SELECTOR,
                              TokenType.PROPERTY_CONTAINS_SELECTOR,
                              TokenType.PRODO_SELECTOR,
                              TokenType.CLASS_SELECTOR,
                              TokenType.ID_SELECTOR,
                              TokenType.CHILD_SELECTOR,
                              TokenType.SUBWIDGET_SELECTOR]
    # 子代选择器和并选择器直接由字面量解析得出
