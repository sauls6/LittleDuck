from antlr4 import *
from gen.LittleDuckLexer import LittleDuckLexer
from gen.LittleDuckParser import LittleDuckParser

# A visitor to evaluate expressions
class EvalVisitor(ParseTreeVisitor):
    def visitProgram(self, ctx):
        return self.visit(ctx.expr())

    def visitIntExpr(self, ctx):
        return int(ctx.getText())

    def visitParensExpr(self, ctx):
        return self.visit(ctx.expr())

    def visitMulDivExpr(self, ctx):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        op = ctx.op.text
        return left * right if op == '*' else left / right

    def visitAddSubExpr(self, ctx):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        op = ctx.op.text
        return left + right if op == '+' else left - right

if __name__ == "__main__":
    input_text = input("Enter an expression: ")  # e.g., (2 + 3) * 4
    input_stream = InputStream(input_text)

    lexer = LittleDuckLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = LittleDuckParser(token_stream)

    tree = parser.program()  # Entry rule
    visitor = EvalVisitor()

    result = visitor.visit(tree)
    print("Result:", result)
