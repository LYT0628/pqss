
def is_letter(ch):
    """check if a char is valid to consist identifier"""
    if type(ch) is not str:
        return False
    return ('a' <= ch <= 'z'
            or 'A' <= ch <= 'Z'
            or '0' <= ch <= '9'
            or ch in ['-', '_'])


def is_digit(ch):
    """check if a char is a number"""
    if type(ch) is not str:
        return False
    return '0' <= ch <= '9'


def is_white_space(ch):
    """check is a char is a blank char"""
    return (ch == ' '
            or ch == '\t'
            or ch == '\n'
            or ch == '\r')
