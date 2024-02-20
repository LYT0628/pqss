from .ast import (
    Expression,
)
from pqss.env import Environment
from pqss.lex import Token


class Identifier(Expression):
    def eval(self, environment: Environment):
        val = environment.get(self.token.literal)
        if val:
            return val
        else:
            # environment.set(self.token.literal, self.value)
            return self.value

    def __init__(self, token: Token, value):
        self.token: Token | None = token
        self.value: str = ''

    def token_literal(self) -> str:
        return self.token.literal

    def expr_node(self):
        pass
