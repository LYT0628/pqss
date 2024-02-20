
from pqss.env import Environment
from pqss.lex import Token
from .ast import (
    Statement,
)


class Selector(Statement):
    def eval(self, environment: Environment):
        return self.token.literal

    def __init__(self, token: Token | None):
        self.token = token

    def stmt_node(self):
        pass
