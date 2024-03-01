from .. import util

from pqss.lex import *
from pqss.parse.ast import *



# TODO
class Priority:
    LOWEST = 1
    EQUALS = 2
    LESS_GREATER = 3
    SUM = 4
    PRODUCT = 5
    PREFIX = 6
    CALL = 7


precedences = {
    TokenType.EQ: Priority.EQUALS,
    TokenType.NOT_EQ: Priority.EQUALS,
    TokenType.LT: Priority.LESS_GREATER,
    TokenType.GT: Priority.LESS_GREATER,
    TokenType.PLUS: Priority.SUM,
    TokenType.SUB: Priority.SUM,
    TokenType.MUL: Priority.PRODUCT,
    TokenType.DIV: Priority.PRODUCT
}


class Parser:
    def __init__(self, lex: Lexer):
        self.code_path: str | None = None

        self.sqss: StyleSheet | None = None
        self.lexer: Lexer = lex
        self.cur_token: Token | None = None
        self.peek_token: Token | None = None

        self.next_token()
        self.next_token()

        self.prefix_parse_fns = {}
        self.infix_parse_fns = {}

        self.register_prefix_fn(TokenType.IDENTIFIER, self.parse_identifier)
        self.register_prefix_fn(TokenType.COLOR, self.parse_color)
        self.register_prefix_fn(TokenType.BUILTIN, self.parse_builtin)
        self.register_prefix_fn(TokenType.NUMBER, self.parse_integer_literal)
        self.register_prefix_fn(TokenType.SUB, self.parse_prefix_expr)
        self.register_prefix_fn(TokenType.TRUE, self.parse_boolean)
        self.register_prefix_fn(TokenType.FALSE, self.parse_boolean)
        self.register_prefix_fn(TokenType.LEFT_PAREN, self.parse_grouped_expr)

        self.register_infix_fn(TokenType.PLUS, self.parse_infix_expr)
        self.register_infix_fn(TokenType.SUB, self.parse_infix_expr)
        self.register_infix_fn(TokenType.MUL, self.parse_infix_expr)
        self.register_infix_fn(TokenType.DIV, self.parse_infix_expr)
        self.register_infix_fn(TokenType.EQ, self.parse_infix_expr)
        self.register_infix_fn(TokenType.NOT_EQ, self.parse_infix_expr)
        self.register_infix_fn(TokenType.LT, self.parse_infix_expr)
        self.register_infix_fn(TokenType.GT, self.parse_infix_expr)

    def next_token(self) -> Token:
        self.cur_token = self.peek_token
        self.peek_token = self.lexer.next_token()
        return self.cur_token

    def parse_program(self):
        self.sqss = StyleSheet()
        self.sqss.statements = []

        while self.peek_token.token_type is not TokenType.EOF:
            stmt = self.parse_stmt()
            if stmt is not None:
                self.sqss.statements.append(stmt)
            self.next_token()
        return self.sqss

    def parse_stmt(self):
        if self.cur_token.token_type == TokenType.IDENTIFIER or self.cur_token.token_type == TokenType.PROPERTY and self.peek_token.token_type == TokenType.ASSIGN:
            return self.parse_var_stmt()
        elif util.is_selector_tok(self.cur_token):
            return self.parse_ruleset()
        elif self.cur_token.token_type == TokenType.IMPORT:
            return self.parse_import()
        elif self.cur_token.token_type == TokenType.MIXIN:
            return self.parse_mixin()
        elif self.cur_token.token_type == TokenType.INCLUDE:
            return self.parse_include()
        elif self.cur_token.token_type == TokenType.EXTEND:
            return self.parse_extend()
        elif self.cur_token.token_type == TokenType.IF:
            return self.parse_if_stmt()
        else:
            return self.parse_expr_stmt()

    def parse_var_stmt(self):
        var_stmt = VarStatement()
        var_stmt.name = Identifier(self.cur_token, self.cur_token.literal)
        self.next_token()
        self.next_token()
        var_stmt.value = self.parse_expr_stmt()  # TODO 计算表达式

        return var_stmt

    def parse_prop_stmt(self):
        rule_stmt = Rule()
        rule_stmt.property = self.cur_token
        self.next_token()
        self.next_token()
        rule_stmt.value = self.parse_expr_stmt()  # TODO 计算表达式

        return rule_stmt

    def register_prefix_fn(self, token_type: TokenType, fn):
        self.prefix_parse_fns[token_type] = fn

    def register_infix_fn(self, token_type: TokenType, fn):
        self.infix_parse_fns[token_type] = fn

    def parse_expr_stmt(self):
        expr_stmt = ExpressionStatement()
        expr_stmt.expr = self.parse_expr(Priority.LOWEST)
        if self.peek_token.token_type == TokenType.SEMICOLON:
            self.next_token()
        return expr_stmt

    def parse_expr(self, precedence: int):

        prefix = self.prefix_parse_fns.get(self.cur_token.token_type)
        if not prefix:
            raise "prefix parse handler does not exists"
        left_expr = prefix()

        while self.peek_token != TokenType.SEMICOLON and precedence < self.peek_precedence():
            infix = self.infix_parse_fns.get(self.peek_token.token_type)
            if infix is None:
                return left_expr

            self.next_token()
            left_expr = infix(left_expr)
        return left_expr

    def parse_identifier(self):
        return Identifier(self.cur_token, self.cur_token.literal)

    def parse_color(self):
        return Color(self.cur_token)

    def parse_builtin(self):
        lexeme = self.cur_token
        self.next_token()
        args = self.parse_include_params()
        self.next_token()
        return Builtin(lexeme, args)

    def parse_integer_literal(self):
        lit = IntegerLiteral(self.cur_token)
        value = float(self.cur_token.literal)
        lit.value = value

        return lit

    def parse_boolean(self):
        return Boolean(self.cur_token, self.cur_token.token_type == TokenType.TRUE)

    def parse_prefix_expr(self):
        expr = PrefixExpression(self.cur_token, self.cur_token.literal)
        self.next_token()
        expr.right = self.parse_expr(Priority.PREFIX)

        return expr

    def peek_precedence(self):
        return precedences.get(self.peek_token.token_type, Priority.LOWEST)

    def cur_precedence(self):
        return precedences.get(self.cur_token.token_type, Priority.LOWEST)

    def parse_infix_expr(self, left: Expression):
        expr = InfixExpression(self.cur_token, self.cur_token.literal, left)

        precedence = self.cur_precedence()
        self.next_token()
        expr.right = self.parse_expr(precedence)

        return expr

    def parse_grouped_expr(self):
        self.next_token()

        expr = self.parse_expr(Priority.LOWEST)

        if self.peek_token.token_type != TokenType.RIGHT_PAREN:
            return None
        self.next_token()
        return expr

    def parse_import(self):
        self.next_token()
        with open(self.cur_token.literal) as f:
            lex = Lexer(f.read())
            p = Parser(lex)
            program = p.parse_program()
            self.sqss.statements.extend(program.statements)

    def parse_mixin(self):
        mixin_stmt = Mixin(self.cur_token)
        self.next_token()
        mixin_stmt.name = self.cur_token.literal

        if self.peek_token.token_type == TokenType.LEFT_PAREN:
            self.next_token()
            mixin_stmt.params = self.parse_mixin_params()
            if self.peek_token.token_type != TokenType.RIGHT_PAREN:
                return None
            self.next_token()

        mixin_stmt.body = Ruleset()
        mixin_stmt.body.selectors = []

        if self.peek_token.token_type != TokenType.LEFT_BRACE:
            return None
        self.next_token()
        rules = []
        child_ruleset_list = []
        self.next_token()
        while self.cur_token.token_type != TokenType.RIGHT_BRACE:
            if self.cur_token.token_type == TokenType.PROPERTY:
                rule = self.parse_rule()
                rules.append(rule)
            else:
                child_ruleset = self.parse_ruleset()
                child_ruleset_list.append(child_ruleset)
            self.next_token()
        # self.next_token()

        mixin_stmt.body.rules = rules
        mixin_stmt.body.child_rulesets = child_ruleset_list

        return mixin_stmt

    def parse_include(self):
        include_stmt = Include(self.cur_token)

        self.next_token()
        include_stmt.mixin_name = self.cur_token.literal

        if self.peek_token.token_type == TokenType.LEFT_PAREN:
            self.next_token()
            include_stmt.args = self.parse_include_params()

            if self.peek_token.token_type != TokenType.RIGHT_PAREN:
                return None
        self.next_token()

        return include_stmt

    def parse_extend(self):
        pass

    def parse_mixin_params(self):
        identifiers: list[Identifier] = []

        if self.peek_token.token_type == TokenType.RIGHT_PAREN:
            return identifiers

        self.next_token()

        ident = Identifier(self.cur_token, self.cur_token.literal)
        identifiers.append(ident)

        while self.peek_token.token_type == TokenType.COMMA:
            self.next_token()
            self.next_token()
            ident = Identifier(self.cur_token, self.cur_token.literal)
            identifiers.append(ident)

        if self.peek_token.token_type != TokenType.RIGHT_PAREN:
            return None

        return identifiers

    def parse_include_params(self):
        args: list[Identifier] = []

        if self.peek_token.token_type == TokenType.RIGHT_PAREN:
            return args

        self.next_token()

        arg = self.parse_expr(Priority.LOWEST)
        args.append(arg)

        while self.peek_token.token_type == TokenType.COMMA:
            self.next_token()
            self.next_token()
            arg = self.parse_expr(Priority.LOWEST)
            args.append(arg)

        if self.peek_token.token_type != TokenType.RIGHT_PAREN:
            return None

        return args

    def parse_selectors(self):
        selector_list: list[Selector] = []

        while self.peek_token.token_type != TokenType.LEFT_BRACE:
            tok = self.cur_token
            selector = Selector(tok)
            selector_list.append(selector)
            self.next_token()

        selector = Selector(self.cur_token)
        selector_list.append(selector)

        return selector_list

    def parse_ruleset(self):
        ruleset = Ruleset()
        ruleset.selectors = self.parse_selectors()

        if self.peek_token.token_type != TokenType.LEFT_BRACE:
            return None
        self.next_token()
        rules = []
        child_ruleset_list = []
        self.next_token()
        while self.cur_token.token_type != TokenType.RIGHT_BRACE:
            if self.cur_token.token_type == TokenType.PROPERTY:
                rule = self.parse_rule()
                rules.append(rule)
            elif self.cur_token.token_type == TokenType.INCLUDE:
                inc = self.parse_include()
                ruleset.includes.append(inc)
            else:
                child_ruleset = self.parse_ruleset()
                child_ruleset_list.append(child_ruleset)
            self.next_token()
        # self.next_token()

        ruleset.rules = rules
        ruleset.child_rulesets = child_ruleset_list

        return ruleset

    def parse_rule(self):
        rule = Rule()

        rule.property = self.cur_token
        self.next_token()
        self.next_token()
        rule.value = self.parse_expr(Priority.LOWEST)  # TODO 计算表达式
        if util.expect_token_type(self.peek_token, TokenType.UNIT):
            rule.unit = Unit(self.next_token())

        self.next_token()
        return rule

    def parse_if_stmt(self):
        stmt = IfStatement(self.cur_token)
        self.next_token()

        stmt.condition = self.parse_expr(Priority.LOWEST)

        if self.peek_token.token_type != TokenType.LEFT_BRACE:
            return None
        self.next_token()

        stmt.consequence = self.parse_block_stmt()

        if self.peek_token.token_type == TokenType.ELSE:
            self.next_token()
            if self.peek_token.token_type != TokenType.LEFT_BRACE:
                return None
            self.next_token()
            stmt.alternative = self.parse_block_stmt()

        return stmt

    def parse_block_stmt(self):
        block = BlockStatement(self.cur_token)
        self.next_token()

        while self.cur_token.token_type != TokenType.RIGHT_BRACE:

            stmt = self.parse_stmt()
            if stmt:
                block.statements.append(stmt)
            self.next_token()  # 分号

        return block
