from typing import TypeVar, List, Union, Tuple
from enum import Enum
import abc, copy
import lexer

class Node():
    """A abstract class of which every type of node must inherit.
    The one thing all nodes must have in common is the visit function.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def visit(self, visitor : "Visitor") -> Union["Node", str, int, bool]:
        """Abstract function used to retrieve the value of a node or execute certain code when a node is being "visited".
        """
        pass

class Visitor():
    """ The Visitor class is used to execute code that's applicable to the type of expression that is currently being "visited"
    """
    def visitLiteral(self, literalExpr : Node) -> Union[str,int]:
        """This function returns the value of a node that is Literal.
        """
        return literalExpr.value

    def visitVariable(self, variableExpr : Node) -> Node:
        """This function recusively returns the value of a node that is a variable.
        """
        return variableExpr.value.visit(self)

    def visitFunctionCall(self, funcExpr : Node):
        """TODO Implement function visit to recursively visit it's body.
        """
        return

    def visitBinary(self, binaryExpr)-> Union[str, int, bool]:
        """This function returns the value of a node that is binary using the stored operator.
        """
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
                binaryExpr.left.value = binaryExpr.right.visit(self)

    def visitIfStatement(self, ifExpr):
        """TODO Implement If visit to recursively visit it's body.
        """
        return

    def visitWhileStatement(self, whileExpr):
        """TODO Implement While visit to recursively visit it's body.
        """
        return

    def visitPrint(self, printExpr) -> None:
        """This function prints the value to the terminal.
        """
        print(printExpr.value)

LitType = TypeVar('LitType', int, str)

class Literal(Node):
    """The Literal class stores a integer or string type value
    """
    def __init__(self,value : LitType):
        self.value = value

    def __str__(self) -> str:
        return 'Literal({value})'.format(
            value = self.value.__repr__()
        )

    def __repr__(self) -> str:
        return self.__str__()

    def visit(self, visitor : Visitor) -> Node:
        return visitor.visitLiteral(self)

class Variable(Node):
    """The Variable class stores (a) node(s) so it can later be used again.
    """
    def __init__(self, name : str, value = Literal(0)):
        self.name = name
        self.value = copy.copy(value)

    def __str__(self) -> str:
        return 'Variable({name},{value})'.format(
            name = self.name,
            value = self.value.__repr__()
        )

    def __repr__(self) -> str:
        return self.__str__()

    def visit(self, visitor : Visitor) -> Node:
        return visitor.visitVariable(self)

FunctionType = TypeVar('FunctionType', Variable, Literal)

class FunctionCall(Node):
    """TODO Implement the Function node.
    """
    def __init__(self, name : str, args : List[FunctionType], body):
        self.name = name
        self.args = args
        self.body = body

    def __str__(self) -> str:
        return 'Function({name},{args},{body})'.format(
            name = self.name,
            args = self.args,
            body = self.body
        )

    def __repr__(self) -> str:
        return self.__str__()

    def visit(self, visitor : Visitor) -> Node:
        return visitor.visitFunctionCall(self)

LeftBinaryType = TypeVar('LeftBinaryType', Variable, Literal)
RightBinaryType = TypeVar('RightBinaryType', Variable, Literal, FunctionCall)

class Binary(Node):
    """ The Binary class is used to store a operation with a left and right node.
    """
    def __init__(self,left : LeftBinaryType , operator ,right : RightBinaryType):
        self.left = copy.copy(left)
        self.operator = operator
        self.right = copy.copy(right)

    def __str__(self) -> str:
        return 'Binary({left},{operator},{right})'.format(
            left = self.left,
            operator = self.operator,
            right = self.right
        )

    def __repr__(self) -> str:
        return self.__str__()

    def visit(self, visitor : Visitor) -> Node:
        return visitor.visitBinary(self)

class IfStatement(Node):
    """TODO Implement the If node.
    """
    def __init__(self, condition : Binary, body):
        self.condition = condition
        self.body = body

    def __str__(self) -> str:
        return 'If({condition},{body})'.format(
            condition = self.condition,
            body = self.body
        )

    def __repr__(self) -> str:
        return self.__str__()

    def visit(self, visitor : Visitor) -> Node:
        return visitor.visitIfStatement(self)

class WhileStatement(Node):
    """TODO Implement the Function node.
    """
    def __init__(self, condition : Binary, body):
        self.condition = condition
        self.body = body

    def __str__(self) -> str:
        return 'While({condition},{body})'.format(
            condition = self.condition,
            body = self.body
        )

    def __repr__(self) -> str:
        return self.__str__()

    def visit(self, visitor : Visitor) -> Node:
        return visitor.visitWhileStatement(self)

printType = TypeVar('printType', Literal, Variable)

class Print(Node):
    """The Print class is used to store a node that can later be printed to the user terminal.
    """
    def __init__(self):
        self.value = ''

    def __str__(self) -> str:
        return 'Print({value})'.format(
            value = self.value.__repr__()
        )

    def __repr__(self) -> str:
        return self.__str__()

    def execute(self, value : printType, visitor : Visitor) -> None:
        self.value = value
        self.visit(visitor)

    def visit(self, visitor : Visitor) -> Node:
        return visitor.visitPrint(self)

class Parser():
    """The Parser class is used to parse tokens made by the lexer class.
    The class has 2 functions : parse(), run()
    """
    def __init__(self, lexer : lexer.Lexer):
        self.lexer = lexer

    def parse(self) -> List[Node]:
        """This function parses a list of tokens created by the lexer class' tokenize() function.
        Next the function will call __create_ast() to create the AST based on the tokens and a (empty) variable list.
        """
        tokens = self.lexer.tokenize()
        return self.__create_ast(tokens, [])

    def __create_ast(self, tokens : List[lexer.Token], variables : List[Variable]) -> List[Node]:
        """This function will recursively create nodes using __create_node() and add them to a list which will be returned.

        """
        if not tokens:
            return []

        node, nr_tokens, updated_variables = self.__create_node(tokens, variables)
        result = [node]
        result.extend(self.__create_ast(tokens[nr_tokens:], updated_variables))
        return result

    def __create_node(self, tokens : List[lexer.Token], variables : List[Variable]) -> Union[Node, int, List[Variable]]:
        """This function creates nodes based on a list of tokens and variables.
        First find out what kind of statement the new line will be then act on that.
        """
        current_head = 0
        current_type = tokens[current_head].type
        #if current_head == VARIABLE NEXT must be ASSIGN THEN: VARIABLE || LITERAL || START || INPUT || PRINT
        if current_type == lexer.TokenTypes.VARIABLE.name:
            return self.__create_node_VAR(tokens, variables)
        # elif current_type == lexer.TokenTypes.IF.name:

        # elif current_type == lexer.TokenTypes.END.name:

        # elif current_type == lexer.TokenTypes.WHILE.name:

        # elif current_type == lexer.TokenTypes.FUNCTION.name:

        # elif current_type == lexer.TokenTypes.RETURN.name:

        else:
            print("THROW ERROR Uknown starting word")
            exit()

    def __create_node_VAR(self, tokens : List[lexer.Token], variables : List[Variable]) -> Union[Node, int, List[Variable]]:
        """This function creates a node which will assign something to a variable.
        For example:
        m = 10
        n = m plus 5
        n = print

        TODO check of een variable bestaat MAAR haal hem niet op

        """
        acceptable_values = [lexer.TokenTypes.VARIABLE.name, lexer.TokenTypes.INTEGER.name, lexer.TokenTypes.STRING.name]
        acceptable_operators = [lexer.TokenTypes.PLUS.name, lexer.TokenTypes.MINUS.name, lexer.TokenTypes.TIMES.name, lexer.TokenTypes.DIVIDE.name]

        # Check if VARIABLE exists if so assign it to a variable

        prime_var = self.__find_variable(tokens[0].value, variables)
        current_head = 1
        current_type = tokens[current_head].type

        if current_type == lexer.TokenTypes.ASSIGN.name:

            first_rhs = False
            current_head = 2
            current_type = tokens[current_head].type

            # if current_head == VARIABLE | INTEGER | STRING NEXT can be : TIMES, DIVIDE, PLUS, MINUS
            if(current_type in acceptable_values):

                if current_type == lexer.TokenTypes.VARIABLE.name:
                    first_rhs = self.__find_variable(tokens[current_head].value, variables)
                elif current_type == lexer.TokenTypes.INTEGER.name:
                    first_rhs = Literal(int(tokens[current_head].value))
                else:
                    first_rhs = Literal(tokens[current_head].value)

                if not first_rhs:
                        print("THROW ERROR VARIABLE DOESNT EXISTS")
                        quit()

                current_head = 3
                current_type = tokens[current_head].type
                # if current_head == TIMES | DIVIDE | PLUS | MINUS NEXT can be : VARIABLE | INTEGER | STRING
                if(current_type in acceptable_operators):

                    current_operator = current_type
                    second_rhs = False
                    current_head = 4
                    current_type = tokens[current_head].type

                    # if current_head == VARIABLE | INTEGER | STRING there is no NEXT, eol
                    if(current_type in acceptable_values): # Binary assignment

                        # Check if VARIABLE exists if so assign it to a variable
                        if current_type == lexer.TokenTypes.VARIABLE.name:
                            second_rhs = self.__find_variable(tokens[current_head].value, variables)
                        elif current_type == lexer.TokenTypes.INTEGER.name:
                            second_rhs = Literal(int(tokens[current_head].value))
                        else:
                            second_rhs = Literal(tokens[current_head].value)

                        if not second_rhs:
                                print("THROW ERROR VARIABLE DOESNT EXISTS")
                                quit()


                        current_head = 5

                        if prime_var:
                            prime_var.value = Binary(first_rhs, current_operator, second_rhs)
                        else:
                            prime_var = Variable(tokens[0].value, Binary(first_rhs, current_operator, second_rhs))
                            variables.append(prime_var)
                        return prime_var, current_head, variables

                    else:

                        print("#THROW ERROR THERE MUST BE A VALUE HOLDING OBJECT AFTER A OPERATOR")
                        quit()

                else: # Assignment
                    if prime_var:
                       prime_var.value = first_rhs
                    else:
                        prime_var = Variable(tokens[0].value, first_rhs)
                        variables.append(prime_var)
                    return prime_var, current_head, variables

            elif current_type == lexer.TokenTypes.PRINT.name: # Print

                if not prime_var:
                    print("THROW ERROR UNKNOWN VARIABLE CANT PRINT")
                    quit()

                current_head = 3
                return Binary(prime_var.value, lexer.TokenTypes.ASSIGN.name, Print()), current_head, variables

            else:

                print("#THROW ERROR THERE MUST BE A VALUE HOLDING OBJECT AFTER A ASSIGNATION OR PRINT")
                quit()

        else:

            print("# THROW ERROR THERE MUST BE A ASSIGNATION")
            quit()

    def run(self, ast : List[Node]) -> Union[bool]:
        """This function creates a Visitor and will recursively start to execute the nodes using __execute_node()
        """
        visitor = Visitor()
        return self.__execute_node(ast, visitor)

    def __execute_node(self, ast : List[Node], visitor : Visitor) -> Union[bool]:
        """This function takes the first node in the AST and then "visits" it.
        Once "visited" the function recursively calls itself to execute the rest of the nodes.
        """
        if not ast:
            return True

        head, *tail = ast
        head.visit(visitor)
        return self.__execute_node(tail, visitor)

    def __find_variable(self, target : str, variables : List[Variable]) -> Union[Variable, bool]:
        """This function is used to recursively go through a list of Variables to see if the target is stored in the list.
        TODO FILTER 
        """
        if not variables:
            return False

        head, *tail = variables
        if head.name == target:
            return head

        return self.__find_variable(target, tail)
