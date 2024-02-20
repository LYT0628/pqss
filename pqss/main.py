import os.path

from pqss.lex import *
from pqss.env import *
from pqss.parse import *


def parse(source: str) -> str:
    if os.path.isfile(source):
        source = read_file(source)

    compiler = Parser(Lexer(source))
    style_sheet = compiler.parse_program()
    qss = style_sheet.eval(Environment())
    return qss


def read_file(p: str):
    res = ''
    with open(p, 'r') as f:
        res = f.read()
    return res

