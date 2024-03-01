
from pqss.env import Environment
from pqss.lex import Token
from .ast import (
    Statement,
    Expression,
    BlankNode,
)
from .unit import Unit


class Rule(Statement):
    def eval(self, environment: Environment):
        return f'{self.property.literal}:{self.value.eval(environment)}{self.unit.eval(environment)};'

    def __init__(self):
        self.property: Token | None = None
        self.value: Expression | None = None
        self.unit: Unit | BlankNode = BlankNode()

    def stmt_node(self):
        pass

