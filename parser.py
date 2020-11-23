from typing import TypeVar, List
import lexer

# Visitor class is used to execute code thats applicable to the type of expresion thats currently being "visited"
class Visitor():
    def visitLiteral(self, literalExpr):
        return literalExpr.value

    def visitVariable(self, variableExpr):
        return variableExpr.value.visit(self)

    def visitFunctionCall(self, funcExpr):
        return

    def visitBinary(self, binaryExpr):
        if binaryExpr.operator == lexer.TokenTypes.PLUS:
            return binaryExpr.left.visit(self) + binaryExpr.right.visit(self)
        elif binaryExpr.operator == lexer.TokenTypes.MINUS:
            return binaryExpr.left.visit(self) - binaryExpr.right.visit(self)
        elif binaryExpr.operator == lexer.TokenTypes.TIMES:
            return binaryExpr.left.visit(self) * binaryExpr.right.visit(self)
        elif binaryExpr.operator == lexer.TokenTypes.DIVIDE:
            return binaryExpr.left.visit(self) / binaryExpr.right.visit(self)
        elif binaryExpr.operator == lexer.TokenTypes.EQUAL:
            return binaryExpr.left.visit(self) == binaryExpr.right.visit(self)
        elif binaryExpr.operator == lexer.TokenTypes.GREATER:
            return binaryExpr.left.visit(self) > binaryExpr.right.visit(self)
        elif binaryExpr.operator == lexer.TokenTypes.SMALLER:
            return binaryExpr.left.visit(self) < binaryExpr.right.visit(self)
        elif binaryExpr.operator == lexer.TokenTypes.NOT_EQUAL:
            return binaryExpr.left.visit(self) != binaryExpr.right.visit(self)
        elif binaryExpr.operator == lexer.TokenTypes.NOT_GREATER:
            return not (binaryExpr.left.visit(self) > binaryExpr.right.visit(self))
        elif binaryExpr.operator == lexer.TokenTypes.NOT_SMALLER:
            return not (binaryExpr.left.visit(self) < binaryExpr.right.visit(self))
        elif binaryExpr.operator == lexer.TokenTypes.ASSIGN:
            if isinstance(binaryExpr.right,(Print)):
                binaryExpr.right.execute(binaryExpr.left.visit(self), self)
            elif isinstance(binaryExpr.left, (Variable)):
                binaryExpr.left.value = Literal(binaryExpr.right.visit(self))

    def visitIfStatement(self, ifExpr):
        return

    def visitWhileStatement(self, whileExpr):
        return

    def visitPrint(self, printExpr):
        print(printExpr.value)

LitType = TypeVar('LitType', int, str)

# Literal class for storing values like integers and strings
class Literal():
    def __init__(self,value : LitType):
        self.value = value

    def __str__(self):
        return 'Literal({value})'.format(
            value = self.value.__repr__()
        )

    def __repr__(self):
        return self.__str__()

    def visit(self, visitor : Visitor):
        return visitor.visitLiteral(self)

# Variable class for creating a variable based on a literal value
class Variable():
    def __init__(self, name : str, value = Literal(0)):
        self.name = name
        self.value = value

    def __str__(self):
        return 'Variable({name},{value})'.format(
            name = self.name,
            value = self.value.__repr__()
        )

    def __repr__(self):
        return self.__str__()

    def visit(self, visitor : Visitor):
        return visitor.visitVariable(self)

FunctionType = TypeVar('FunctionType', Variable, Literal)

# FunctionCall class to execute a body of code
class FunctionCall():
    def __init__(self, name : str, args : List[FunctionType], body):
        self.name = name
        self.args = args
        self.body = body

    def __str__(self):
        return 'Function({name},{args},{body})'.format(
            name = self.name,
            args = self.args,
            body = self.body
        )

    def __repr__(self):
        return self.__str__()

    def visit(self, visitor : Visitor):
        return visitor.visitFunctionCall(self)

LeftBinaryType = TypeVar('LeftBinaryType', Variable, Literal)
RightBinaryType = TypeVar('RightBinaryType', Variable, Literal, FunctionCall)

# Binary class for applying operators on Literals, Variables and on the right side FunctionCalls
class Binary():
    def __init__(self,left : LeftBinaryType , operator ,right : RightBinaryType):
        self.left = left
        self.operator = operator
        self.right = right

    def __str__(self):
        return 'Binary({left},{operator},{right})'.format(
            left = self.left,
            operator = self.operator,
            right = self.right
        )

    def __repr__(self):
        return self.__str__()

    def visit(self, visitor : Visitor):
        return visitor.visitBinary(self)

# IfStatement class for a body of code that will be executed once based on a condition
class IfStatement():
    def __init__(self, condition : Binary, body):
        self.condition = condition
        self.body = body

    def __str__(self):
        return 'If({condition},{body})'.format(
            condition = self.condition,
            body = self.body
        )

    def __repr__(self):
        return self.__str__()

    def visit(self, visitor : Visitor):
        return visitor.visitIfStatement(self)

# WhileStatement class for a body of code that will be exectued as long as the condition is met
class WhileStatement():
    def __init__(self, condition : Binary, body):
        self.condition = condition
        self.body = body

    def __str__(self):
        return 'While({condition},{body})'.format(
            condition = self.condition,
            body = self.body
        )

    def __repr__(self):
        return self.__str__()

    def visit(self, visitor : Visitor):
        return visitor.visitWhileStatement(self)

printType = TypeVar('printType', Literal, Variable)

# Print class for printing a stored value
class Print():
    def __init__(self):
        self.value = ''

    def __str__(self):
        return 'Print({value})'.format(
            value = self.value.__repr__()
        )

    def __repr__(self):
        return self.__str__()

    def execute(self, value : printType, visitor : Visitor):
        self.value = value
        self.visit(visitor)

    def visit(self, visitor : Visitor):
        return visitor.visitPrint(self)

# Parser class used to parse a lexer
class Parser():
    def __init__(self, lexer : lexer.Lexer):
        self.lexer = lexer

    def parse(self):
        tokens = self.lexer.tokenize