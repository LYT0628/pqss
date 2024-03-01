from .ast import (
    Expression,
)
from pqss.env import Environment
from pqss.lex import Token


class Color(Expression):
    def eval(self, environment: Environment):
        return self.token.literal

    def __init__(self, token: Token):
        self.token: Token | None = token

    def expr_node(self):
        pass
