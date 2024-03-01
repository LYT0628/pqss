def is_digit(ch):
    """check if a char is a number"""
    if type(ch) is not str:
        return False
    return '0' <= ch <= '9'


def is_blank_char(ch):
    """check is a char is a blank char"""
    return (ch == ' '
            or ch == '\t'
            or ch == '\n'
            or ch == '\r')
