
from pqss.env import Environment
from pqss.lex import Token
from .ast import (
    Expression
)


class Unit(Expression):
    def eval(self, environment: Environment):
        return self.token.literal

    def expr_node(self):
        pass

    def __init__(self, token: Token):
        self.token = token
