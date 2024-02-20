
from pqss.env import Environment
from pqss.lex import Token
from .ast import (
    Statement,
    Expression
)
from .identifier import Identifier


class VarStatement(Statement):
    def eval(self, environment: Environment):
        environment.set(self.name.token.literal,
                        self.value.eval(environment))

    def __init__(self):
        self.token: Token | None = None  # TODO May be not needed
        self.name: Identifier | None = None
        self.value: Expression | None = None

    def stmt_node(self):
        pass
