
from pqss.env import Environment
from pqss.lex import Token
from .ast import (
    Statement,
    Expression,
    BlockStatement
)


class Include(Statement):
    def eval(self, environment: Environment):
        mixin = environment.get(self.mixin_name)
        if not mixin:
            raise "Mixin not exists!!!"
        params = mixin.params
        body = mixin.body

        return self.do_eval(params, body, environment)

    def do_eval(self, params, body, environment: Environment):
        bloc_env = Environment()
        bloc_env.parent = environment
        idx = 0
        while idx < len(params):
            key = params[idx].token.literal
            val = self.args[idx].eval(bloc_env)
            bloc_env.set(key, val)

            idx += 1

        s = body.eval(bloc_env)
        res = s[1:-1] if len(s) > 2 else ''
        return res

    def __init__(self, token: Token, mixin_name: str | None = None, args: list[Expression] | None = None):
        self.token = token
        self.mixin_name = mixin_name
        self.args = args

    def stmt_node(self):
        pass
