from .ast import (
    Expression,
)
from pqss.env import Environment
from pqss.lex import Token


class Builtin(Expression):
    def eval(self, environment: Environment):
        res = self.token.literal
        res += '('
        for arg in self.args:
            res += str(arg.eval(environment)) + ','
        res = res[:-1] + ');'
        return res

    def __init__(self, token: Token, args: list[Expression] | None = None):
        self.token = token
        self.args = args

    def token_literal(self) -> str:
        return self.token.literal

    def expr_node(self):
        pass
