import logging
import re

from .token import Token, TokenType, lookup_keyword, is_color, is_property
from .utils import is_letter
from ..util.char_util import is_digit, is_blank_char
from .exceptions import TokenUnKnownException
from .constants import EOF

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


class Lexer:
    """Lexer of PQSS"""

    def __init__(self, src_code: str):
        """
        :param src_code:  PQSS code
        """
        self.is_enter_selectors = False

        self.inserted_tok = None
        self.inserted = None

        self._src_code: str = src_code
        self._cur_pos: int = 0
        self._peek_pos: int = 0
        self._cur_char = None
        self._peek_char = None

        self.read_char()

    def read_char(self) -> str:
        """read a char and preview one char"""
        if self._peek_pos >= len(self._src_code):  # 到达文本末尾，全部读作EOF
            self._peek_char = EOF
            self._cur_char = EOF
        else:
            self._cur_char = self._src_code[self._peek_pos]
            self._cur_pos = self._peek_pos
            self._peek_pos += 1
            if not self._peek_pos >= len(self._src_code):  # 到达文本末尾，字符不需要再改变了， 一律EOF
                self._peek_char = self._src_code[self._peek_pos]

        return self._cur_char

    def next_token(self) -> Token:
        """parse a lexeme to Token"""

        if self.inserted:
            self.inserted = False
            return self.inserted_tok
        self._skip_blank_and_comment()

        lexeme = self._cur_char
        tok = None

        if lexeme == EOF:
            tok = Token(TokenType.EOF, lexeme)

        elif lexeme == ':':
            tok = Token(TokenType.ASSIGN, lexeme)
        elif lexeme == '(':
            tok = Token(TokenType.LEFT_PAREN, lexeme)
        elif lexeme == ')':
            tok = Token(TokenType.RIGHT_PAREN, lexeme)
        # elif lexeme == '[':
        #     tok = Token(TokenType.LEFT_BRACKET, lexeme)
        # elif lexeme == ']':
        #     tok = Token(TokenType.RIGHT_BRACKET, lexeme)
        elif lexeme == '{':
            self.is_enter_selectors = False
            tok = Token(TokenType.LEFT_BRACE, lexeme)
        elif lexeme == '}':
            tok = Token(TokenType.RIGHT_BRACE, lexeme)
        elif lexeme == ';':
            tok = Token(TokenType.SEMICOLON, lexeme)
        elif lexeme == ',':
            tok = Token(TokenType.COMMA, lexeme)

        elif lexeme == '+':
            tok = Token(TokenType.PLUS, lexeme)
        elif lexeme == '-':
            tok = Token(TokenType.SUB, lexeme)
        elif lexeme == '*':
            if self.is_infix():
                tok = Token(TokenType.MUL, lexeme)
            else:
                tok = Token(TokenType.UNIVERSAL_SELECTOR, lexeme)
                self.is_enter_selectors = True
                self.insert_union_selector_if_needed()
        elif lexeme == '/':
            tok = Token(TokenType.DIV, lexeme)
        elif lexeme == '>':
            if self.is_enter_selectors:
                tok = Token(TokenType.CHILD_SELECTOR, lexeme)
            else:
                tok = Token(TokenType.GT, lexeme)
        elif lexeme == '<':
            tok = Token(TokenType.LT, lexeme)
        elif lexeme == '=':
            lexeme = '=='
            self.read_char()
            tok = Token(TokenType.EQ, lexeme)

        elif lexeme == '"' or lexeme == "'":
            lexeme = self.read_string()
            tok = Token(TokenType.STRING, lexeme)

        elif lexeme == '&':
            tok = Token(TokenType.PARENT_REFERENCE, lexeme)
        elif lexeme == '$':
            lexeme = self.read_identifier()
            tok = Token(TokenType.IDENTIFIER, lexeme)
        elif lexeme == '!' or lexeme == '@':
            if self._peek_char == '=':
                lexeme = '!='
                self.read_char()
                tok = Token(TokenType.EQ, lexeme)
            else:
                tok = self.read_keyword()
        elif lexeme == '.':
            lexeme = self.read_ID_selector()
            tok = Token(TokenType.TYPE_SELECTOR, lexeme)
            self.is_enter_selectors = True
        elif lexeme == '#':
            if self.is_value():
                lexeme = self.read_word()
                tok = Token(TokenType.COLOR, lexeme)
            else:
                lexeme = self.read_ID_selector()
                tok = Token(TokenType.ID_SELECTOR, lexeme)
                self.is_enter_selectors = True
        elif is_digit(lexeme):
            lexeme = self.read_number()
            tok = Token(TokenType.NUMBER, lexeme)

        elif lexeme == '%':
            raise NotImplementedError()

        elif is_letter(lexeme):
            if self.peek_word() in ['px']:
                tok = Token(TokenType.UNIT, self.read_word())
            elif self.is_color():
                lexeme = self.read_word()
                tok = Token(TokenType.COLOR, lexeme)
            elif self.is_property():
                lexeme = self.read_property()
                tok = Token(TokenType.PROPERTY, lexeme)
            elif self.is_keyword():
                tok = self.read_keyword()
            elif self.is_builtin():
                lexeme = self.read_word()
                tok = Token(TokenType.BUILTIN, lexeme)
            elif self.is_mixin_name():
                lexeme = self.read_identifier()
                tok = Token(TokenType.IDENTIFIER, lexeme)
            else:
                tok = self.read_selector()
                self.is_enter_selectors = True
                self.insert_union_selector_if_needed()
        else:
            raise TokenUnKnownException(f'Token {lexeme} does unknown!!!')

        self.read_char()
        return tok

    def insert_union_selector_if_needed(self):
        if not is_blank_char(self._peek_char) and self._peek_char not in ['>', '{']:
            self.inserted = True
            self.inserted_tok = Token(TokenType.UNION_SELECTOR, '')

    def read_identifier(self):
        """read a valid identifier"""
        pos = self._cur_pos
        while is_letter(self._peek_char):
            self.read_char()
        return self._src_code[pos:self._peek_pos]

    def read_number(self):
        """read a valid number"""
        pos = self._cur_pos
        while is_digit(self._peek_char):  # int
            self.read_char()

        if self._peek_char == '.':  # float
            while is_digit(self._peek_char):
                self.read_char()
        return self._src_code[pos:self._peek_pos]

    def is_keyword(self) -> bool:
        """check the next word is a valid token for PQSS"""
        pos = self._cur_pos

        while is_letter(self._peek_char):
            self.read_char()
        lexeme = self._src_code[pos: self._cur_pos]

        # restore
        self._cur_pos = pos
        self._cur_char = self._src_code[self._cur_pos]
        self._peek_pos = pos + 1
        self._peek_char = self._src_code[self._peek_pos]

        if lookup_keyword(lexeme):
            return True
        return False

    def read_keyword(self):
        """read a keyword to Token"""
        pos = self._cur_pos

        while is_letter(self._peek_char):
            self.read_char()
        lexeme = self._src_code[pos:self._peek_pos]

        token_type = lookup_keyword(lexeme)
        if token_type is None:
            raise TokenUnKnownException(f'Token {lexeme} does not a valid keyword!!!')
        return Token(token_type, lexeme)

    def read_selector(self):
        """read the non-prefix selector"""
        pos = self._cur_pos
        token_type = None
        while is_letter(self._peek_char):
            self.read_char()

        # 属性选择器
        if self._peek_char == '[':
            while self._peek_char != ']':
                self.read_char()
            self.read_char()  # 读到 ]
            token_type = TokenType.PROPERTY_SELECTOR
        elif self._cur_char == ':':
            if self.read_char() == ':':
                token_type = TokenType.SUBWIDGET_SELECTOR
            else:
                token_type = TokenType.PRODO_SELECTOR
            while is_letter(self.read_char()):
                pass
        else:
            token_type = TokenType.CLASS_SELECTOR

        return Token(token_type, self._src_code[pos:self._peek_pos])

    def read_ID_selector(self):
        """read the selector begin with #"""
        pos = self._cur_pos
        self.read_char()
        while is_letter(self._peek_char):
            self.read_char()
        return self._src_code[pos:self._cur_pos + 1]

    def is_property(self) -> bool:
        """check if the next word is property of QSS"""
        pos = self._cur_pos
        while is_letter(self.read_char()):
            pass
        lexeme = self._src_code[pos: self._cur_pos]
        self._cur_pos = pos
        self._cur_char = self._src_code[self._cur_pos]
        self._peek_pos = pos + 1
        self._peek_char = self._src_code[self._peek_pos]

        if is_property(lexeme):
            return True
        return False

    def read_property(self) -> str:
        """read the next properties and return the lexeme"""
        pos = self._cur_pos
        while is_letter(self._peek_char):
            self.read_char()
        lexeme = self._src_code[pos: self._peek_pos]
        if is_property(lexeme):
            return lexeme
        self._cur_pos = pos
        self._cur_char = self._src_code[pos]

    def is_mixin_name(self):
        """check if the next identifier belongs to a mixin"""
        i = 0
        while is_letter(self._src_code[self._cur_pos + i]):
            i += 1
        while is_blank_char(self._src_code[self._cur_pos + i]):
            i += 1
        ch = self._src_code[self._cur_pos + i]
        return ch == '('

    def _skip_blank_char(self):
        """skip all the next black chars"""
        while is_blank_char(self._cur_char):
            self.read_char()

    def _skip_comment(self):
        """skip comments, // or /**/"""
        if self._cur_char == '/':
            if self._peek_char == '/':
                while self._cur_char != '\n':
                    self.read_char()
                self.read_char()  # skip \n
            elif self._peek_char == '*':
                stack = 1
                while stack != 0:
                    self.read_char()
                    if self._cur_char == '/' and self._peek_char == '*':
                        stack += 1
                    elif self._cur_char == '*' and self._peek_char == '/':
                        stack -= 1
                # skip */
                self.read_char()
                self.read_char()

    def _skip_blank_and_comment(self):
        self._skip_blank_char()
        self._skip_comment()
        self._skip_blank_char()

    def is_end(self):
        return self._cur_char == EOF

    def read_string(self):
        pos = self._peek_pos
        quote = self._cur_char

        while self._peek_char != quote:
            self.read_char()

        return self._src_code[pos: self._peek_pos]

    def is_color(self):
        pos = self._cur_pos

        while is_letter(self._peek_char):
            self.read_char()

        lexeme = self._src_code[pos: self._peek_pos]
        self._cur_pos = pos
        self._cur_char = self._src_code[self._cur_pos]
        self._peek_pos = pos + 1
        self._peek_char = self._src_code[self._peek_pos]

        return is_color(lexeme)

    def read_word(self):
        pos = self._cur_pos
        while is_letter(self._peek_char):
            self.read_char()
        lexeme = self._src_code[pos: self._peek_pos]

        return lexeme

    def is_value(self):
        i = 0
        while not is_blank_char(self._src_code[self._cur_pos + i]) and self._src_code[self._cur_pos + i] != ';':
            i += 1
        ch = self._src_code[self._cur_pos + i]
        return ch == ';'

    def is_builtin(self):
        pos = self._cur_pos

        while is_letter(self._peek_char):
            self.read_char()

        lexeme = self._src_code[pos: self._peek_pos]
        self._cur_pos = pos
        self._cur_char = self._src_code[self._cur_pos]
        self._peek_pos = pos + 1
        self._peek_char = self._src_code[self._peek_pos]

        return lexeme in ['rgb', 'rgba']

    def is_infix(self):
        i = 0
        while is_blank_char(self._src_code[self._peek_pos + i]):
            i += 1
        ch = self._src_code[self._peek_pos + i]
        return is_digit(ch)

    def peek_word(self):
        pos = self._cur_pos

        while is_letter(self._peek_char):
            self.read_char()

        lexeme = self._src_code[pos: self._peek_pos]
        self._cur_pos = pos
        self._cur_char = self._src_code[self._cur_pos]
        self._peek_pos = pos + 1
        self._peek_char = self._src_code[self._peek_pos]

        return lexeme
