#=====================================================================================#
# Lexer requirements
#=====================================================================================#
from enum import Enum

class TokenTypes(Enum):
    """ Enum Class whith all types of tokens
    """
    PLUS='plus'
    MINUS='minus'
    DIVIDE='divide'
    TIMES='times'
    ASSIGN='='
    SMALLER='<'
    GREATER='>'
    NOT_EQUAL='~'
    NOT_SMALLER='~<'
    NOT_GREATER='~>'
    EQUAL='~~'
    INPUT='input'
    PRINT='print'
    FUNCTION='function'
    IF='if'
    WHILE='while'
    START='start'
    END='end'
    RETURN='return'
    INTEGER='[0-9]'
    STRING='".*"'
    VARIABLE='[a-zA-Z]'

class Token():
    """Token class to hold information about a single token
    """
    def __init__(self, value, type):
        self.value = value
        self.type = type

    def __str__(self) -> str:
        return 'Token({value}, {type})'.format(value=repr(self.value), type=self.type)

    def __repr__(self) -> str:
        return self.__str__()

#=====================================================================================#
# Parser requirements
#=====================================================================================#

from abc import ABC
from typing import TypeVar, Dict, List, Union, Tuple
import copy

class Operators(Enum):
    PLUS='plus'
    MINUS='minus'
    DIVIDE='divide'
    TIMES='times'
    SMALLER='<'
    GREATER='>'
    NOT_EQUAL='~'
    NOT_SMALLER='~<'
    NOT_GREATER='~>'
    EQUAL='~~'

class Node(ABC):

    def __str__(self):
        pass

    def visit(self, visitor : "Visitor", check_dict : Dict[Dict, "Node"]):
        pass

class Assignment(Node):
    def __init__(self, lhs : Node, rhs : Node):
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self) -> str:
        return 'Assignment({lhs},{rhs})'.format(
            lhs = self.lhs,
            rhs = self.rhs
        )

    def __repr__(self) -> str:
        return self.__str__()

    def visit(self, visitor : "Visitor", check_dict : Dict[Dict, Node]):
        return visitor.visitAssignment(self, check_dict)

literalType = TypeVar('literalType', str, int)

class Literal(Node):
    def __init__(self, value : literalType):
        self.value = value

    def __str__(self) -> str:
        return 'Literal({value})'.format(
            value = self.value
        )

    def __repr__(self) -> str:
        return self.__str__()

    def visit(self, visitor : "Visitor", check_dict : Dict[Dict, Node]) -> Tuple[Union[str, int], Dict[Dict, Node]]:
        return visitor.visitLiteral(self, check_dict)

class Variable(Node):
    def __init__(self, name : str):
        self.name = name
        self.value = None

    def __str__(self) -> str:
        if self.value:
            return 'Variable({name},{value})'.format(
                name = self.name,
                value = self.value
            )
        else:
            return 'Variable({name})'.format(
                name = self.name
            )

    def __repr__(self) -> str:
        return self.__str__()

    def visit(self, visitor : "Visitor", check_dict : Dict[Dict, Node]) -> Tuple[Union[str, int], Dict[Dict, Node]]:
        return visitor.visitVariable(self, check_dict)

class Print(Node):
    def __init__(self, value : Node):
        self.value = value

    def __str__(self) -> str:
        return 'Print({value})'.format(
            value = self.value
        )

    def __repr__(self) -> str:
        return self.__str__()

    def visit(self, visitor : "Visitor", check_dict : Dict[Dict, Node]) -> Tuple[Union[bool],Dict[Dict,Node]]:
        return visitor.visitPrint(self, check_dict)


class Operation(Node):
    def __init__(self, lhs : Node, operator : Operators, rhs : Node):
        self.lhs = lhs
        self.operator = operator
        self.rhs = rhs

    def __str__(self) -> str:
        return 'Operation({lhs},{operator},{rhs})'.format(
            lhs = self.lhs,
            operator = self.operator,
            rhs = self.rhs
        )

    def __repr__(self) -> str:
        return self.__str__()

    def visit(self, visitor : "Visitor", check_dict : Dict[Dict, Node]):
        return visitor.visitOperation(self, check_dict)

class Condition(Node):
    def __init__(self, lhs : Node, operator : Operators, rhs : Node):
        self.lhs = lhs
        self.operator = operator
        self.rhs = rhs

    def __str__(self) -> str:
        return 'Condition({lhs},{operator},{rhs})'.format(
            lhs = self.lhs,
            operator = self.operator,
            rhs = self.rhs
        )

    def __repr__(self) -> str:
        return self.__str__()

    def visit(self, visitor : "Visitor", check_dict : Dict[Dict,Node]):
        return visitor.visitCondition(self, check_dict)

class If(Node):
    def __init__(self, name : str, condition : Node):
        self.name = name
        self.condition = condition
        self.body = None

    def __str__(self) -> str:
        if self.body:
            return 'If({name},{condition},{body})'.format(
                name = self.name,
                condition = self.condition,
                body = self.body
            )
        else:
            return 'If({name},{condition})'.format(
                name = self.name,
                condition = self.condition
            )

    def __repr__(self) -> str:
        return self.__str__()

    def addToBody(self, line : Node):
        if self.body:
            self.body.append(line)
        else:
            self.body = [line]

    def visit(self, visitor : "Visitor", check_dict :  Dict[Dict, Node]):
        return visitor.visitIf(self, check_dict)


#=====================================================================================#
# Interpreter requirements
#=====================================================================================#

import re

class Visitor():
    """The Visitor class is used to execute Nodes from a AST.
    """

    def visitLiteral(self, literalExpr : Node, check_dict : Dict[Dict,Node]) -> Tuple[Union[str, int], Dict[Dict, Node]]:
        """Visits a Literal expression and retrieve the value

        Args:
            literalExpr (Node): A Literal object that inherits from Node
            check_dict (Dict[Dict,Node]): A Dictionary that keeps track of existing objects. Will not be used in this function.

        Returns:
            Tuple[Union[str, int], Dict[Dict, Node]]: Return a Tuple with the first index (0) always being the value of the Literal object and the second index (1) always being the check_dict
        """
        return literalExpr.value, check_dict

    def visitVariable(self, variableExpr : Node, check_dict : Dict[Dict, Node]) -> Tuple[Union[str, int], Dict[Dict, Node]]:
        """Visits a Variable expression and retrieve the value that's being held

        Args:
            variableExpr (Node): A Variable object that inherits from Node
            check_dict (Dict[Dict, Node]): A Dictionary that keeps track of existing objects. Will not be used in this function.

        Returns:
            Tuple[Union[str, int], Dict[Dict, Node]]: Return a Tuple with the first index (0) always being the value that the Variable object holds and the second index (1) always being the check_dict
        """
        return variableExpr.value.visit(self, check_dict)

    def visitOperation(self, operationExpr : Node, check_dict : Dict[Dict,Node]) -> Tuple[Union[str, int], Dict[Dict, Node]]:
        """Visits a Operation expression and executes the operation.

        Args:
            operationExpr (Node): A Operation object that inherits from Node
            check_dict (Dict[Dict,Node]): A Dictionary that keeps track of existing objects. Will be passed along to the left and right hand side values.

        Returns:
            Tuple[Union[str, int], Dict[Dict, Node]]: Return a Tuple with the first index (0) always being the calculated value and the second index (1) being the check_dict.
        """
        lhs_result, _ = operationExpr.lhs.visit(self, check_dict)
        rhs_result, _ = operationExpr.rhs.visit(self, check_dict)
        operation_result = None

        if re.match('[0-9]', lhs_result) and re.match('[0-9]', rhs_result): # Main case
            lhs_result = int(lhs_result)
            rhs_result = int(rhs_result)
            if operationExpr.operator is TokenTypes.PLUS.name:
                operation_result = lhs_result + rhs_result
            elif operationExpr.operator is TokenTypes.MINUS.name:
                operation_result = lhs_result - rhs_result
            elif operationExpr.operator is TokenTypes.TIMES.name:
                operation_result = lhs_result * rhs_result
            elif operationExpr.operator is TokenTypes.DIVIDE.name:
                operation_result = lhs_result/rhs_result
        elif isinstance(lhs_result, (str)) and isinstance(rhs_result, (str)) and operationExpr.operator is TokenTypes.PLUS.name: # String concatenation
            operation_result = lhs_result+rhs_result
        else:
            print("LHS AND RHS WERE NOT OF SAME TYPE")
            exit()

        return operation_result, check_dict


    def visitAssignment(self, assignmentExpr : Node, check_dict : Dict[Dict, Node]) -> Tuple[Union[bool], Dict[Dict,Node]]:
        """Visits a Assignment expression which will assign it's right hand side value to the left hand side

        Args:
            assignmentExpr (Node): A Assignment object that inherits from Node
            check_dict (Dict[Dict, Node]): A Dictionary that keeps track of existing objects. In this function we use it to retrieve the variable if it's been assigned before.

        Returns:
            Tuple[Union[bool], Dict[Dict,Node]]: Return a Tuple with the first index (0) always being True if there were no errors and the second index (1) always being the check_dict
        """
        if assignmentExpr.lhs.name not in check_dict['variables']:
            check_dict['variables'][assignmentExpr.lhs.name] = assignmentExpr.lhs

        result = assignmentExpr.rhs.visit(self, check_dict)
        check_dict['variables'][assignmentExpr.lhs.name].value = Literal(result[0])
        return True, result[1]

    def visitPrint(self, printExpr : Node, check_dict : Dict[Dict, Node]) -> Tuple[Union[bool], Dict[Dict,Node]]: # Later on Union with error class
        """Visits a Print expression which will print the value it's holding

        Args:
            printExpr (Node): A Print object that inherits from Node
            check_dict (Dict[Dict, Node]): A Dictionary that keeps track of existing objects. Will be passed along to the value it's holding.

        Returns:
            Tuple[Union[bool], Dict[Dict,Node]]: Return a Tuple with the first index (0) always being True if there were no errors and the second index (1) always being the check_dict
        """

        result = printExpr.value.visit(self, check_dict)
        print(result[0])
        return True, result[1]

    def visitIf(self, ifExpr : Node, check_dict : Dict[Dict, Node]):
        pass

    def visitCondition(self, conditionExpr : Node, check_dict : Dict[Dict,Node]):
        pass