
from pqss.env import Environment
from pqss.lex import Token, TokenType
from .ast import (
    Statement,
    Expression,
)
from .selector import Selector
from .rule import Rule
from .include import Include
from ... import util


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
        idx = 0
        while idx < len(self.selectors):
            selector = self.selectors[idx]
            res += selector.eval(environment)
            if idx < len(self.selectors) - 1:
                peek = self.selectors[idx + 1]
                if util.expect_token_type(peek.token, TokenType.UNION_SELECTOR):
                    idx += 1
                else:
                    res += ' '
            idx += 1

        return res

    def _eval_child_rulesets(self, environment):
        if len(self.child_rulesets) == 0:
            return ''

        res = ''

        idx = 0
        while idx < len(self.selectors) - 1:
            selector = self.selectors[idx]
            res += selector.eval(environment)
            if idx < len(self.selectors) - 1:
                peek = self.selectors[idx + 1]
                if util.expect_token_type(peek.token, TokenType.UNION_SELECTOR):
                    idx += 1
                else:
                    res += ' '
            idx += 1

        for ruleset in self.child_rulesets:
            val = ruleset.eval(environment)

            if val.find('&') != -1:
                val = val.replace('&', self.selectors[-1].eval(environment))
                res += ' ' + val
            else:
                res += self.selectors[-1].eval(environment) + ' ' + val

        return res

    def __init__(self):
        self.selectors: list[Selector] | None = []
        self.rules: list[Rule] = []
        self.child_rulesets: list[Ruleset] = []
        self.includes: list[Include] = []


    def stmt_node(self):
        pass
