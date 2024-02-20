import abc

from pqss.lex import TokenType, Token
from pqss.env import *


class Node:
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
    def __init__(self):
        self.statements: list[Statement] = []

    def eval(self, environment: Environment):
        qss = ''
        for stmt in self.statements:
            result = stmt.eval(environment)
            if result is not None:
                qss = qss + str(result)

        return qss


class ExpressionStatement(Statement):
    def __init__(self):
        self.expr: Expression | None = None

    def eval(self, environment: Environment):
        return self.expr.eval(environment)

    def stmt_node(self):
        pass


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


