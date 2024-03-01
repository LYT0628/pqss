
def is_letter(ch):
    """check if a char is valid to consist identifier"""
    if type(ch) is not str:
        return False
    return ('a' <= ch <= 'z'
            or 'A' <= ch <= 'Z'
            or '0' <= ch <= '9'
            or ch in ['-', '_'])


