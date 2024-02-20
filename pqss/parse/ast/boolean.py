
from pqss.env import Environment
from pqss.lex import Token
from .ast import (
    Expression
)


class Boolean(Expression):
    def eval(self, environment: Environment):
        return self.value

    def expr_node(self):
        pass

    def __init__(self, token: Token, value: bool):
        self.token = token
        self.value = value
