
from pqss.env import Environment
from pqss.lex import Token
from .ast import (
    Expression
)


class IntegerLiteral(Expression):
    def expr_node(self):
        pass

    def eval(self, environment: Environment):
        return self.value

    def __init__(self, token: Token | None = None, value: float | None = None):
        self.token = token
        self.value = value
