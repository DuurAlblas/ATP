from typing import TypeVar, List

LitType = TypeVar('LitType', int, str)

# Literal class for storing values like integers and strings
class Literal():
    def __init__(self,value : LitType):
        self.value = value

# Variable class for creating a variable based on a literal value
class Variable():
    def __init__(self, name : str, value = Literal(0)):
        self.name = name
        self.value = value

FunctionType = TypeVar('FunctionType', Variable, Literal)

# FunctionCall class to execute a body of code
class FunctionCall():
    def __init__(self, name : str, args : List[FunctionType], body):
        self.name = name
        self.args = args
        self.body = body

LeftBinaryType = TypeVar('LeftBinaryType', Variable, Literal)
RightBinaryType = TypeVar('RightBinaryType', Variable, Literal, FunctionCall)

# Binary class for applying operators on Literals, Variables and on the right side FunctionCalls
class Binary():
    def __init__(self,left : LeftBinaryType , operator ,right : RightBinaryType):
        self.left = left
        self.oprator = operator
        self.right = right

# IfStatement class for a body of code that will be executed once based on a condition
class IfStatement():
    def __init__(self, condition : Binary, body):
        self.condition = condition
        self.body = body

# WhileStatement class for a body of code that will be exectued as long as the condition is met
class WhileStatement():
    def __init__(self, condition : Binary, body):
        self.condition = condition
        self.body = body