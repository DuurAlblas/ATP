from typing import TypeVar, List
from enum import Enum
import abc
import lexer

# Visitor class is used to execute code thats applicable to the type of expresion thats currently being "visited"
class Visitor():
    def visitLiteral(self, literalExpr):
        # print("Visited Lit : ", literalExpr.value)
        return literalExpr.value

    def visitVariable(self, variableExpr):
        # print("Visited Var : ",variableExpr.name, " | ", variableExpr.value)
        return variableExpr.value.visit(self)

    def visitFunctionCall(self, funcExpr):
        return

    def visitBinary(self, binaryExpr):
        if binaryExpr.operator == lexer.TokenTypes.PLUS.name:
            return binaryExpr.left.visit(self) + binaryExpr.right.visit(self)
        elif binaryExpr.operator == lexer.TokenTypes.MINUS.name:
            return binaryExpr.left.visit(self) - binaryExpr.right.visit(self)
        elif binaryExpr.operator == lexer.TokenTypes.TIMES.name:
            return binaryExpr.left.visit(self) * binaryExpr.right.visit(self)
        elif binaryExpr.operator == lexer.TokenTypes.DIVIDE.name:
            return binaryExpr.left.visit(self) / binaryExpr.right.visit(self)
        elif binaryExpr.operator == lexer.TokenTypes.EQUAL.name:
            return binaryExpr.left.visit(self) == binaryExpr.right.visit(self)
        elif binaryExpr.operator == lexer.TokenTypes.GREATER.name:
            return binaryExpr.left.visit(self) > binaryExpr.right.visit(self)
        elif binaryExpr.operator == lexer.TokenTypes.SMALLER.name:
            return binaryExpr.left.visit(self) < binaryExpr.right.visit(self)
        elif binaryExpr.operator == lexer.TokenTypes.NOT_EQUAL.name:
            return binaryExpr.left.visit(self) != binaryExpr.right.visit(self)
        elif binaryExpr.operator == lexer.TokenTypes.NOT_GREATER.name:
            return not (binaryExpr.left.visit(self) > binaryExpr.right.visit(self))
        elif binaryExpr.operator == lexer.TokenTypes.NOT_SMALLER.name:
            return not (binaryExpr.left.visit(self) < binaryExpr.right.visit(self))
        elif binaryExpr.operator == lexer.TokenTypes.ASSIGN.name:
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

class Node():
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def visit(self, visitor : Visitor):
        return

LitType = TypeVar('LitType', int, str)

# Literal class for storing values like integers and strings
class Literal(Node):
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
class Variable(Node):
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
class FunctionCall(Node):
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
class Binary(Node):
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
class IfStatement(Node):
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
class WhileStatement(Node):
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
class Print(Node):
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

# States in which the parser can be
class States(Enum):
    NEW_LINE = 0
    MATH = 2
    ASSIGNMENT = 1
    IF = 3
    WHILE = 4
    FUNCTION = 5

# Parser class used to parse a lexer
class Parser():
    def __init__(self, lexer : lexer.Lexer):
        self.lexer = lexer

    def parse(self) -> List[Node]:
        tokens = self.lexer.tokenize()
        return self.__create_ast(tokens, [])

    def __create_ast(self, tokens : List[lexer.Token], variables : List[Variable]) -> List[Node]:
        if not tokens:
            return []

        node, nr_tokens, updated_variables = self.__create_node(tokens, variables)
        result = [node]
        result.extend(self.__create_ast(tokens[nr_tokens:], updated_variables))
        return result

    def __create_node(self, tokens : List[lexer.Token], variables : List[Variable]):
        current_head = 0
        #if current_head == VARIABLE NEXT must be ASSIGN THEN: VARIABLE || LITERAL || START || INPUT || PRINT
        if tokens[current_head].type == lexer.TokenTypes.VARIABLE.name:
            return self.__create_node_VAR(tokens, variables)
        # elif tokens[current_head].type == lexer.TokenTypes.IF:

        # elif tokens[current_head].type == lexer.TokenTypes.END:

        # elif tokens[current_head].type == lexer.TokenTypes.WHILE:

        # elif tokens[current_head].type == lexer.TokenTypes.FUNCTION:

        # elif tokens[current_head].type == lexer.TokenTypes.RETURN:

        else:
            print("THROW ERROR Uknown starting word")
            exit()

    def __create_node_VAR(self, tokens : List[lexer.Token], variables : List[Variable]):

        # Check if VARIABLE exists if so assign it to a variable

        prime_var = self.__find_variable(tokens[0].value, variables)
        current_head = 1

        if tokens[current_head].type == lexer.TokenTypes.ASSIGN.name:

            first_rhs = False
            current_head = 2
            # if current_head == VARIABLE | INTEGER | STRING NEXT can be : TIMES, DIVIDE, PLUS, MINUS
            if(tokens[current_head].type == lexer.TokenTypes.VARIABLE.name
            or tokens[current_head].type == lexer.TokenTypes.INTEGER.name
            or tokens[current_head].type == lexer.TokenTypes.STRING.name):

                if tokens[current_head].type == lexer.TokenTypes.VARIABLE.name:
                    first_rhs = self.__find_variable(tokens[current_head].value, variables)
                elif tokens[current_head].type == lexer.TokenTypes.INTEGER.name:
                    first_rhs = Literal(int(tokens[current_head].value))
                else:
                    first_rhs = Literal(tokens[current_head].value)

                if not first_rhs:
                        print("THROW ERROR VARIABLE DOESNT EXISTS")

                current_head = 3

                # if current_head == TIMES | DIVIDE | PLUS | MINUS NEXT can be : VARIABLE | INTEGER | STRING
                if(tokens[current_head].type == lexer.TokenTypes.TIMES.name
                or tokens[current_head].type == lexer.TokenTypes.DIVIDE.name
                or tokens[current_head].type == lexer.TokenTypes.PLUS.name
                or tokens[current_head].type == lexer.TokenTypes.MINUS.name):

                    current_operator = tokens[current_head].type
                    second_rhs = False
                    current_head = 4

                    # if current_head == VARIABLE | INTEGER | STRING there is no NEXT, eol
                    if(tokens[current_head].type == lexer.TokenTypes.VARIABLE.name
                    or tokens[current_head].type == lexer.TokenTypes.INTEGER.name
                    or tokens[current_head].type == lexer.TokenTypes.STRING.name): # Binary assignment

                        # Check if VARIABLE exists if so assign it to a variable
                        if tokens[current_head].type == lexer.TokenTypes.VARIABLE.name:
                            second_rhs = self.__find_variable(tokens[current_head].value, variables)
                        elif tokens[current_head].type == lexer.TokenTypes.INTEGER.name:
                            second_rhs = Literal(int(tokens[current_head].value))
                        else:
                            second_rhs = Literal(tokens[current_head].value)

                        if not second_rhs:
                                print("THROW ERRO VARIABLE DOESNT EXISTS")


                        current_head = 5
                        prime_var = Variable(tokens[0].value, Binary(first_rhs, current_operator, second_rhs))
                        variables.append(prime_var)
                        return prime_var, current_head, variables

                    else:

                        print("#THROW ERROR THERE MUST BE A VALUE HOLDING OBJECT AFTER A OPERATOR")
                        return

                else: # Assignment
                    prime_var = Variable(tokens[0].value, first_rhs)
                    variables.append(prime_var)
                    return prime_var, current_head, variables

            elif tokens[current_head].type == lexer.TokenTypes.PRINT.name: # Print

                if not prime_var:
                    print("THROW ERROR UNKNOWN VARIABLE CANT PRINT")
                current_head = 3
                return Binary(prime_var.value, lexer.TokenTypes.ASSIGN.name, Print()), current_head, variables

            else:

                print("#THROW ERROR THERE MUST BE A VALUE HOLDING OBJECT AFTER A ASSIGNATION OR PRINT")
                exit()

        else:

            print("# THROW ERROR THERE MUST BE A ASSIGNATION")
            exit()

    def run(self, ast : List[Node]) -> bool:
        # Run the ast IDEA: List of trees "roots", every tree can get visited and then we move to the next tree
        visitor = Visitor()
        return self.__execute_node(ast, visitor)

    def __execute_node(self, ast : List[Node], visitor : Visitor) -> bool:
        if not ast:
            return True

        head, *tail = ast
        head.visit(visitor)
        self.__execute_node(tail, visitor)

    def __find_variable(self, target : str, variables : List[Variable]):
        if not variables:
            return False

        head, *tail = variables
        if head.name == target:
            return head

        return self.__find_variable(target, tail)
