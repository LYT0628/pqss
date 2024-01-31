import abc

from sqss.lex import TokenType, Token
from sqss.env import *


class Node(abc.ABC):
    @abc.abstractmethod
    def token_literal(self) -> str:
        pass

    @abc.abstractmethod
    def eval(self, environment: Environment):
        pass


class Statement(Node):
    @abc.abstractmethod
    def stmt_node(self):
        pass


class Expression(Node):
    @abc.abstractmethod
    def expr_node(self):
        pass


class StyleSheet(Node):
    def eval(self, environment: Environment):
        qss = ''
        for stmt in self.statements:
            result = stmt.eval(environment)
            if result is not None:
                qss = qss + str(result)

        return qss

    def __init__(self):
        self.statements: list[Statement] = []

    def token_literal(self):
        if len(self.statements) > 0:
            return self.statements[0].token_literal()
        else:
            return ''


class VarStatement(Statement):
    def eval(self, environment: Environment):
        environment.set(self.name.token.literal,
                        self.value.eval(environment))

    def __init__(self):
        self.token: Token | None = None  # TODO May be not needed
        self.name: Identifier | None = None
        self.value: Expression | None = None

    def token_literal(self) -> str:
        return self.token.literal

    def stmt_node(self):
        pass


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


class ExpressionStatement(Statement):

    def eval(self, environment: Environment):
        return self.expr.eval(environment)

    def __init__(self):
        self.token: Token | None = None
        self.expr: Expression | None = None

    def token_literal(self) -> str:
        return self.token.literal

    def stmt_node(self):
        pass


class IntegerLiteral(Expression):
    def expr_node(self):
        pass

    def eval(self, environment: Environment):
        return self.value

    def token_literal(self) -> str:
        return self.token.literal

    def __init__(self, token: Token | None = None, value: float | None = None):
        self.token = token
        self.value = value


class PrefixExpression(Expression):
    def eval(self, environment: Environment):
        right = self.right.eval(environment)
        if self.token.token_type == TokenType.SUB:
            return -right

    def __init__(self, token: Token | None, operator: str | None = None, right: Expression | None = None):
        self.token = token
        self.operator = operator
        self.right = right

    def expr_node(self):
        pass

    def token_literal(self) -> str:
        pass


class InfixExpression(Expression):
    def eval(self, environment: Environment):
        left = self.left.eval(environment)
        right = self.right.eval(environment)
        if self.token.token_type == TokenType.PLUS:
            return left + right
        if self.token.token_type == TokenType.SUB:
            return left - right
        if self.token.token_type == TokenType.MUL:
            return left * right
        else:
            # self.token.token_type == TokenType.DIV:
            return left / right

    def __init__(self, token: Token, operator: str, left: Expression = None, right: Expression = None):
        self.token = token
        self.left = left
        self.operator = operator
        self.right = right

    def expr_node(self):
        pass

    def token_literal(self) -> str:
        pass


class Color(Expression):
    def eval(self, environment: Environment):
        return self.token.literal

    def __init__(self):
        self.token: Token | None = None

    def expr_node(self):
        pass

    def token_literal(self) -> str:
        pass


class HexColor(Expression):
    def eval(self, environment: Environment):
        return self.token.literal

    def __init__(self):
        self.token: Token | None = None

    def expr_node(self):
        pass

    def token_literal(self) -> str:
        pass


class Selector(Statement):
    def eval(self, environment: Environment):
        return self.token.literal

    def __init__(self, token: Token | None):
        self.token = token

    def stmt_node(self):
        pass

    def token_literal(self) -> str:
        pass


class Rule(Statement):
    def eval(self, environment: Environment):
        res = ''
        res += self.property.literal
        res += ':'
        res += str(self.value.eval(environment))
        res += ';'
        return res

    def __init__(self):
        self.property: Token | None = None
        self.value: Expression | None = None

    def stmt_node(self):
        pass

    def token_literal(self) -> str:
        pass


class Ruleset(Statement):
    def eval(self, environment: Environment):
        res = ''
        selectors = ''
        for selector in self.selector_list:
            selectors += ' ' + selector.eval(environment)
        res += selectors
        res += '{'
        for rule in self.rule_list:
            res += rule.eval(environment)
        res += '}'

        def eval_child(sec, children):
            res = ''
            s = ''
            for se in sec:
                s += ' ' + se.eval(environment)
            s = s.replace(' ', '')
            for child_ruleset in children:
                val = child_ruleset.eval(environment)

                if val.find('&') != -1:
                    val = val.replace('&', s.split(' ')[-1])
                    val = val.replace(' ', '')
                    s = s.split(s.split(' ')[-1])[0]
                    res += s + val
                else:
                    res += s + ' '
                    res += val

            return res

        child_rules = eval_child(self.selector_list, self.child_ruleset)

        res += child_rules
        return res

    def __init__(self):
        self.selector_list: list[Selector] | None = []
        self.rule_list: list[Rule] = []
        self.child_ruleset: list[Ruleset] = []

    def stmt_node(self):
        pass

    def token_literal(self) -> str:
        pass


class Boolean(Expression):
    def eval(self, environment: Environment):
        return self.value

    def expr_node(self):
        pass

    def token_literal(self) -> str:
        pass

    def __init__(self, token: Token, value: bool):
        self.token = token
        self.value = value


class BlockStatement(Statement):
    def eval(self, environment: Environment):
        res = '{'
        for stmt in self.statements:
            res += str(stmt.eval(environment))
        res += '}'
        return res

    def __init__(self, token: Token | None):
        self.token = token
        self.statements: list[Statement] = []

    def stmt_node(self):
        pass

    def token_literal(self) -> str:
        pass


class IfStatement(Statement):
    def eval(self, environment: Environment):
        pass

    def __init__(self, token: Token, expr: Expression | None = None,
                 consequence: BlockStatement | None = None,
                 alternative: BlockStatement | None = None):
        self.token = token
        self.condition = expr
        self.consequence = consequence
        self.alternative = alternative

    def stmt_node(self):
        pass

    def token_literal(self) -> str:
        pass


class Mixin(Statement):
    def eval(self, environment: Environment):
        pass

    def stmt_node(self):
        pass

    def token_literal(self) -> str:
        pass

    def __init__(self, token: Token, name: str | None = None):
        self.token = token
        self.name: str = name
        self.params: list[Identifier] = []
        self.body: BlockStatement | None = None


class Include(Statement):
    def eval(self, environment: Environment):
        pass

    def __init__(self, token: Token, mixin_name: str | None = None, args: list[Expression] | None = None):
        self.token = token
        self.mixin_name = mixin_name
        self.args = args

    def stmt_node(self):
        pass

    def token_literal(self) -> str:
        pass
