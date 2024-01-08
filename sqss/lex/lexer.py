from .token import Token, TokenType, lookup_keyword


class TokenUnKnownException(Exception):
    pass


def is_selector_or_property(ch):
    return 'a' <= ch <= 'z' or 'A' <= ch <= 'Z' or \
        ch == '.' or ch == '#' or ch == '*'


def is_selector_symbol(ch):
    return is_selector_or_property(ch) or \
        ch == ' ' or ch == '>' or ch == '[' or ch == ']' or ch == '='


def is_letter(ch):
    return 'a' <= ch <= 'z' or 'A' <= ch <= 'Z' or ch == '_'


def is_digit(ch):
    return '0' <= ch <= '9'


def is_white_space(ch):
    return ch == ' ' or ch == '\t' or ch == '\n' or ch == '\r'


class Lexer:
    def __init__(self, input_str: str):
        self.input_str: str = input_str
        self.cur_position: int = 0
        self.peek_position: int = 0
        self.cur_char = None
        self.peek_char = None

        self.read_char()

    def read_char(self):
        if self.peek_position >= len(self.input_str):
            self.cur_char = 0
        else:
            self.cur_char = self.input_str[self.peek_position]
        self.cur_position = self.peek_position
        self.peek_position += 1
        self.peek_char = self.input_str[self.peek_position]
        return self.cur_char

    # ':+(){}'
    def next_token(self) -> Token:
        # self.skip_white_space()
        lexeme = self.cur_char
        tok = None
        if lexeme == ' ':
            if self.is_selector():
                self.read_char()
                return Token(TokenType.GENERAL_SELECTOR, lexeme)
            # 普通空格 或者 子代选择器（到｛ 前必须为 空格，》 。 字母 # ：【】 = ）（return）

        self.skip_white_space()
        lexeme = self.cur_char
        if lexeme == ':':
            tok = Token(TokenType.ASSIGN, lexeme)
        elif lexeme == '+':
            tok = Token(TokenType.PLUS, lexeme)
        elif lexeme == '(':
            tok = Token(TokenType.LEFT_PAREN, lexeme)
        elif lexeme == ')':
            tok = Token(TokenType.RIGHT_PAREN, lexeme)
        elif lexeme == '{':
            tok = Token(TokenType.LEFT_BRACE, lexeme)
        elif lexeme == '}':
            tok = Token(TokenType.RIGHT_BRACE, lexeme)
        elif lexeme == ';':
            tok = Token(TokenType.SEMICOLON, lexeme)
        elif lexeme == '"' or lexeme == "'":
            pass  # 字符串 目前不接受插值
        # elif is_selector_or_property(lexeme):
        #     pass  # 选择器 或 属性
        elif lexeme == '%':
            pass  # 占位选择器
        elif is_digit(lexeme):
            lexeme = self.read_number()
            tok = Token(TokenType.NUMBER, float(lexeme))
        elif lexeme == '$':
            lexeme = self.read_identifier()
            tok = Token(TokenType.IDENTIFIER, lexeme)
        elif lexeme == '!' or lexeme == '@':
            tok = self.read_keyword()
        #     直接以字母开头的家伙，可能是字符串(;结尾)，颜色类型(颜色列表里)，选择器({), 属性
        else:
            raise TokenUnKnownException('Token {0} does unknown!!!'.format(lexeme))

        self.read_char()
        return tok

    def read_identifier(self):
        pos = self.cur_position
        while is_letter(self.read_char()):  # 需要预读一个$
            pass
        return self.input_str[pos:self.cur_position]

    def read_number(self):
        pos = self.cur_position
        while is_digit(self.peek_char):  # int
            self.read_char()

        if self.peek_char == '.':  # float
            while is_digit(self.peek_char):
                self.read_char()
        return self.input_str[pos:self.cur_position + 1]

    def read_keyword(self):
        pos = self.cur_position

        while not is_white_space(self.peek_char):
            self.read_char()
        lexeme = self.input_str[pos:self.peek_position]
        token_type = lookup_keyword(lexeme)
        if token_type is None:
            raise TokenUnKnownException('Token {0} does unknown!!!'.format(lexeme))
        return Token(token_type, lexeme)

    def is_selector(self) -> bool:
        pre_pos = self.peek_position
        while self.input_str[pre_pos] != '{':
            if not is_selector_symbol(self.input_str[pre_pos]) or pre_pos >= len(self.input_str):
                return False
        return True

    def skip_white_space(self):

        while is_white_space(self.cur_char):
            self.read_char()
