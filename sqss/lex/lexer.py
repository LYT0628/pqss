from .token import Token, TokenType, lookup_keyword, is_color, is_property


class TokenUnKnownException(Exception):
    pass


def is_letter(ch):

    return 'a' <= ch <= 'z' or 'A' <= ch <= 'Z' or '0' <= ch <= '9' or ch in ['-', '_']


def is_digit(ch):
    return '0' <= ch <= '9'


def is_white_space(ch):
    return ch == ' ' or ch == '\t' or ch == '\n' or ch == '\r'


class Lexer:
    def __init__(self, input_str: str):
        self.input_str: str = input_str
        self.cur_pos: int = 0
        self.peek_pos: int = 0
        self.cur_char = None
        self.peek_char = None

        self.read_char()

    def read_char(self):
        if self.peek_pos >= len(self.input_str):
            self.cur_char = 0
        else:
            self.cur_char = self.input_str[self.peek_pos]
            self.cur_pos = self.peek_pos
            self.peek_pos += 1
            if not self.peek_pos >= len(self.input_str):
                self.peek_char = self.input_str[self.peek_pos]

        return self.cur_char

    # ':+(){}'
    def next_token(self) -> Token:

        self.skip_white_space()
        self.skip_comment()
        self.skip_white_space()

        lexeme = self.cur_char
        tok = None
        if lexeme == 0:
            tok = Token(TokenType.EOF, lexeme)
        elif lexeme == ':':
            tok = Token(TokenType.ASSIGN, lexeme)
        elif lexeme == '+':
            tok = Token(TokenType.PLUS, lexeme)
        elif lexeme == '-':
            tok = Token(TokenType.SUB, lexeme)
        elif lexeme == '*':
            tok = Token(TokenType.MUL, lexeme)
        elif lexeme == '/':
            tok = Token(TokenType.DIV, lexeme)
        elif lexeme == '>':
            tok = Token(TokenType.GT, lexeme)
        elif lexeme == '<':
            tok = Token(TokenType.LT, lexeme)
        elif lexeme == '=':
            lexeme = '=='
            self.read_char()
            tok = Token(TokenType.EQ, lexeme)
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
        elif lexeme == ',':
            tok = Token(TokenType.COMMA, lexeme)
        elif lexeme == '"' or lexeme == "'":
            pass  # 字符串 目前不接受插值
        elif lexeme == '&':
            tok = Token(TokenType.PARENT_REFERENCE, lexeme)
        elif is_digit(lexeme):
            lexeme = self.read_number()
            tok = Token(TokenType.NUMBER, lexeme)
        elif lexeme == '$':
            lexeme = self.read_identifier()
            tok = Token(TokenType.IDENTIFIER, lexeme)
        elif lexeme == '!' or lexeme == '@':
            if self.peek_char == '=':
                lexeme = '!='
                self.read_char()
                tok = Token(TokenType.EQ, lexeme)
            else:
                tok = self.read_keyword()
        elif lexeme == '.':
            lexeme = self.read_ID_selector()
            tok = Token(TokenType.TYPE_SELECTOR, lexeme)
        elif lexeme == '#':
            lexeme = self.read_ID_selector()
            tok = Token(TokenType.ID_SELECTOR, lexeme)
        elif lexeme == '>':
            tok = Token(TokenType.CHILDREN_SELECTOR, lexeme)
        elif lexeme == '%':
            raise NotImplementedError()

        elif is_letter(lexeme):
            if is_color(lexeme):
                pass
            elif self.is_property():
                lexeme = self.read_property()
                tok = Token(TokenType.PROPERTY, lexeme)
            elif self.is_keyword():
                tok = self.read_keyword()
            elif self.is_mixin_name():
                lexeme = self.read_identifier()
                tok = Token(TokenType.IDENTIFIER, lexeme)
            else:
                tok = self.read_selector()
        else:
            raise TokenUnKnownException('Token {0} does unknown!!!'.format(lexeme))

        self.read_char()
        return tok

    def read_identifier(self):
        pos = self.cur_pos
        while is_letter(self.peek_char):
            self.read_char()
        return self.input_str[pos:self.peek_pos]

    def read_number(self):
        pos = self.cur_pos
        while is_digit(self.peek_char):  # int
            self.read_char()

        if self.peek_char == '.':  # float
            while is_digit(self.peek_char):
                self.read_char()
        return self.input_str[pos:self.cur_pos + 1]

    def is_keyword(self) -> bool:
        pos = self.cur_pos
        while is_letter(self.read_char()):
            pass
        lexeme = self.input_str[pos: self.cur_pos]
        self.cur_pos = pos
        self.cur_char = self.input_str[self.cur_pos]
        self.peek_pos = pos + 1
        self.peek_char = self.input_str[self.peek_pos]

        if lookup_keyword(lexeme):
            return True
        return False

    def read_keyword(self):
        pos = self.cur_pos

        while is_letter(self.peek_char):
            self.read_char()
        lexeme = self.input_str[pos:self.peek_pos]
        token_type = lookup_keyword(lexeme)
        if token_type is None:
            raise TokenUnKnownException('Token {0} does unknown!!!'.format(lexeme))
        return Token(token_type, lexeme)

    def skip_white_space(self):
        while is_white_space(self.cur_char):
            self.read_char()

    def read_selector(self):
        pos = self.cur_pos
        token_type = None
        while is_letter(self.read_char()):
            pass

        # 属性选择器
        if self.cur_char == '[':
            while self.cur_char != ']':
                self.read_char()
            self.read_char()  # 读掉 ]
            token_type = TokenType.PROPERTY_SELECTOR
        elif self.cur_char == ':':
            if self.read_char() == ':':
                token_type = TokenType.SUBWIDGET_SELECTOR
            else:
                token_type = TokenType.PRODO_SELECTOR
            while is_letter(self.read_char()):
                pass
        else:
            token_type = TokenType.CLASS_SELECTOR
        return Token(token_type, self.input_str[pos:self.cur_pos])

    def read_ID_selector(self):
        pos = self.cur_pos
        self.read_char()
        while is_letter(self.peek_char):
            self.read_char()
        return self.input_str[pos:self.cur_pos + 1]

    def is_property(self) -> bool:
        pos = self.cur_pos
        while is_letter(self.read_char()):
            pass
        lexeme = self.input_str[pos: self.cur_pos]
        self.cur_pos = pos
        self.cur_char = self.input_str[self.cur_pos]
        self.peek_pos = pos + 1
        self.peek_char = self.input_str[self.peek_pos]

        if is_property(lexeme):
            return True
        return False

    def read_property(self) -> str:
        pos = self.cur_pos
        while is_letter(self.peek_char):
            self.read_char()
        lexeme = self.input_str[pos: self.peek_pos]
        if is_property(lexeme):
            return lexeme
        self.cur_pos = pos
        self.cur_char = self.input_str[pos]

    def skip_comment(self):
        if self.cur_char == '/':
            if self.peek_char == '/':
                while self.cur_char != '\n':
                    self.read_char()
                self.read_char()  # skip \n
            elif self.peek_char == '*':
                stack = 1
                while stack != 0:
                    self.read_char()
                    if self.cur_char == '/' and self.peek_char == '*':
                        stack += 1
                    elif self.cur_char == '*' and self.peek_char == '/':
                        stack -= 1
                # skip */
                self.read_char()
                self.read_char()

    def is_mixin_name(self):
        i = 0
        while is_letter(self.input_str[self.cur_pos + i]):
            i += 1
        while is_white_space(self.input_str[self.cur_pos + i]):
            i += 1
        ch = self.input_str[self.cur_pos + i]
        return ch == '('
