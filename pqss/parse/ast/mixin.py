
from pqss.env import Environment
from pqss.lex import Token
from .ast import (
    Statement,
    BlockStatement
)
from .identifier import Identifier


class Mixin(Statement):
    def eval(self, environment: Environment):
        environment.set(self.name, self)

    def stmt_node(self):
        pass

    def __init__(self, token: Token, name: str | None = None):
        self.token = token
        self.name: str = name
        self.params: list[Identifier] = []
        self.body: BlockStatement | None = None
