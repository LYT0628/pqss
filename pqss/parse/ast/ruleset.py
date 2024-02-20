
from pqss.env import Environment
from pqss.lex import Token
from .ast import (
    Statement,
    Expression,
)
from .selector import Selector
from .rule import Rule
from .include import Include


class Ruleset(Statement):
    def eval(self, environment: Environment):
        res = self._eval_selectors(environment)
        res += '{'
        for rule in self.rules:
            res += rule.eval(environment)
        for inc in self.includes:
            res += inc.eval(environment)
        res += '}'

        res += self._eval_child_rulesets(environment)

        return res

    def _eval_selectors(self, environment):
        res = ''
        for selector in self.selectors:
            res += ' ' + selector.eval(environment)
        return res

    def _eval_child_rulesets(self, environment):
        res = ''

        for selector in self.selectors[:-2]:
            res += selector.eval(environment)

        for ruleset in self.child_rulesets:
            val = ruleset.eval(environment)

            if val.find('&') != -1:
                val = val.replace('&', self.selectors[-1].eval(environment))
                res += ' ' + val
            else:
                res += self.selectors[-1].eval(environment) + val

        return res

    def __init__(self):
        self.selectors: list[Selector] | None = []
        self.rules: list[Rule] = []
        self.child_rulesets: list[Ruleset] = []
        self.includes: list[Include] = []


    def stmt_node(self):
        pass
