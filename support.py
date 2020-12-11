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

    def create_body(self, body : List[Node]):
        self.body = body

    def remaining_tokens(self):
        return self.body[-1].get_remaining_tokens()

    def updated_check_dict(self):
        return self.body[-1].get_updated_check_dict()

    def visit(self, visitor : "Visitor", check_dict :  Dict[Union[Dict, List], Node]):
        return visitor.visitIf(self, check_dict)

class While(Node):
    def __init__(self, name : str, condition : Node):
        self.name = name
        self.condition = condition
        self.body = None

    def __str__(self) -> str:
        if self.body:
            return 'While({name},{condition},{body})'.format(
                name = self.name,
                condition = self.condition,
                body = self.body
            )
        else:
            return 'While({name},{condition})'.format(
                name = self.name,
                condition = self.condition
            )

    def __repr__(self) -> str:
        return self.__str__()

    def create_body(self, body : List[Node]):
        self.body = body

    def remaining_tokens(self):
        return self.body[-1].get_remaining_tokens()

    def updated_check_dict(self):
        return self.body[-1].get_updated_check_dict()

    def visit(self, visitor : "Visitor", check_dict :  Dict[Union[Dict, List], Node]):
        return visitor.visitWhile(self, check_dict)

class End(Node):
    def __init__(self, name : str, remaining_tokens : List[Token], check_dict : Dict[Union[Dict, List], Node]):
        self.name = name
        self.remaining_tokens = remaining_tokens
        self.check_dict = check_dict

    def __str__(self) -> str:
        return 'End({name})'.format(
            name = self.name
        )

    def __repr__(self) -> str:
        return self.__str__()

    def get_remaining_tokens(self):
        try:
            tmp = copy.copy(self.remaining_tokens)
            del self.remaining_tokens
            return tmp
        except:
            return None

    def get_updated_check_dict(self):
        try:
            tmp = copy.copy(self.check_dict)
            del self.check_dict
            return tmp
        except:
            return None

    def visit(self, visitor : "Visitor", check_dict : Dict[Union[Dict, List], Node]):
        return visitor.visitEnd(self, check_dict)

class Function(Node):
    def __init__(self, name : str):
        self.name = name
        self.args = None
        self.body = None
        
    def __str__(self) -> str:
        if self.args == None and self.body == None:
            return 'Function({name})'.format(
                name = self.name
            )
        elif self.args == None:
            return 'Function({name},{body})'.format(
                name = self.name,
                body = self.body
            )
        elif self.body == None:
            return 'Function({name},{args})'.format(
                name = self.name,
                args = self.args
            )
        else :
            return 'Function({name},{args},{body})'.format(
                name = self.name,
                args = self.args,
                body = self.body
            )
    def __repr__(self) ->str:
        return self.__str__()
        
    def add_arguments(self, args : List[Node]):
        self.args = args
        
    def add_body(self, body : List[Node]):
        self.body = body
        
    def set_arguments(self, start_arguments : List[Node], check_dict : Dict[Union[Dict, List], Node]):
        if not start_arguments:
            return        
        arguments = copy.copy(start_arguments)
        current_index = len(self.args) - len(arguments)
        current_arg, *tail = arguments
        self.args[current_index].value = check_dict['variables'][current_arg.name].value
        self.set_arguments(tail, check_dict)        

    def remaining_tokens(self):
        return self.body[-1].get_remaining_tokens()

    def updated_check_dict(self):
        return self.body[-1].get_updated_check_dict()
        
    def visit(self, visitor : "Visitor", check_dict :  Dict[Union[Dict, List], Node]):
        return visitor.visitFunction(self, check_dict)

class Return(Node):
    def __init__(self, value : Node):
        self.value = value

    def __str__(self) -> str:
        return 'Return({value})'.format(
            value = self.value
        )

    def __repr__(self) -> str:
        return self.__str__()

    def visit(self, visitor : "Visitor", check_dict : Dict[Dict, Node]) -> Tuple[Union[bool],Dict[Dict,Node]]:
        return visitor.visitReturn(self, check_dict)

class Start(Node):
    def __init__(self, value : Function, parameters : List[Node]):
        self.value = value
        self.parameters = parameters
        
    def __str__(self) -> str:
        return 'Start({value},{parameters})'.format(
            value = self.value,
            parameters = self.parameters
        )
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def visit(self, visitor : "Visitor", check_dict : Dict[Dict, Node]) -> Tuple[Union[bool],Dict[Dict,Node]]:
        return visitor.visitStart(self, check_dict)    

#=====================================================================================#
# Interpreter requirements
#=====================================================================================#

import re

class Visitor():
    """The Visitor class is used to execute Nodes from a AST.
    """

    def visitLiteral(self, literalExpr : Node, check_dict : Dict[Dict,Node]) -> Tuple[Union[str, int], Dict[Union[Dict, List], Node]]:
        """Visits a Literal expression and retrieve the value

        Args:
            literalExpr (Node): A Literal object that inherits from Node
            check_dict (Dict[Dict,Node]): A Dictionary that keeps track of existing objects. Will not be used in this function.

        Returns:
            Tuple[Union[str, int], Dict[Union[Dict, List], Node]]: Return a Tuple with the first index (0) always being the value of the Literal object and the second index (1) always being the check_dict
        """
        return literalExpr.value, check_dict

    def visitVariable(self, variableExpr : Node, check_dict : Dict[Union[Dict, List], Node]) -> Tuple[Union[str, int], Dict[Union[Dict, List], Node]]:
        """Visits a Variable expression and retrieve the value that's being held

        Args:
            variableExpr (Node): A Variable object that inherits from Node
            check_dict (Dict[Union[Dict, List], Node]): A Dictionary that keeps track of existing objects. Will not be used in this function.

        Returns:
            Tuple[Union[str, int], Dict[Union[Dict, List], Node]]: Return a Tuple with the first index (0) always being the value that the Variable object holds and the second index (1) always being the check_dict
        """
        return variableExpr.value.visit(self, check_dict)

    def visitOperation(self, operationExpr : Node, check_dict : Dict[Dict,Node]) -> Tuple[Union[str, int], Dict[Union[Dict, List], Node]]:
        """Visits a Operation expression and executes the operation.

        Args:
            operationExpr (Node): A Operation object that inherits from Node
            check_dict (Dict[Dict,Node]): A Dictionary that keeps track of existing objects. Will be passed along to the left and right hand side values.

        Returns:
            Tuple[Union[str, int], Dict[Union[Dict, List], Node]]: Return a Tuple with the first index (0) always being the calculated value and the second index (1) being the check_dict.
        """
        lhs_result, _ = operationExpr.lhs.visit(self, check_dict)
        rhs_result, _ = operationExpr.rhs.visit(self, check_dict)
        operation_result = None

        if isinstance(lhs_result, (str)):
            if re.match('[0-9]', lhs_result):
                lhs_result = int(lhs_result)
                
        if isinstance(rhs_result, (str)):        
            if re.match('[0-9]', rhs_result):   
                rhs_result = int(rhs_result)

        if isinstance(lhs_result, (int)) and isinstance(rhs_result, (int)) :
            if operationExpr.operator is TokenTypes.PLUS.name:
                operation_result = lhs_result + rhs_result
            elif operationExpr.operator is TokenTypes.MINUS.name:
                operation_result = lhs_result - rhs_result
            elif operationExpr.operator is TokenTypes.TIMES.name:
                operation_result = lhs_result * rhs_result
            elif operationExpr.operator is TokenTypes.DIVIDE.name:
                operation_result = lhs_result / rhs_result
        elif isinstance(lhs_result, (str)) and isinstance(rhs_result, (str)) and operationExpr.operator is TokenTypes.PLUS.name: # String concatenation
            operation_result = lhs_result+rhs_result
        else:
            print("LHS AND RHS WERE NOT OF SAME TYPE")
            exit()

        return operation_result, check_dict

    def visitAssignment(self, assignmentExpr : Node, check_dict : Dict[Union[Dict, List], Node]) -> Tuple[Union[bool], Dict[Dict,Node]]:
        """Visits a Assignment expression which will assign it's right hand side value to the left hand side

        Args:
            assignmentExpr (Node): A Assignment object that inherits from Node
            check_dict (Dict[Union[Dict, List], Node]): A Dictionary that keeps track of existing objects. In this function we use it to retrieve the variable if it's been assigned before.

        Returns:
            Tuple[Union[bool], Dict[Dict,Node]]: Return a Tuple with the first index (0) always being True if there were no errors and the second index (1) always being the check_dict
        """
        if assignmentExpr.lhs.name not in check_dict['variables']:
            check_dict['variables'][assignmentExpr.lhs.name] = assignmentExpr.lhs
        result = assignmentExpr.rhs.visit(self, check_dict)
        check_dict['variables'][assignmentExpr.lhs.name].value = Literal(result[0])
        return True, result[1]

    def visitPrint(self, printExpr : Node, check_dict : Dict[Union[Dict, List], Node]) -> Tuple[Union[bool], Dict[Dict,Node]]: # Later on Union with error class
        """Visits a Print expression which will print the value it's holding

        Args:
            printExpr (Node): A Print object that inherits from Node
            check_dict (Dict[Union[Dict, List], Node]): A Dictionary that keeps track of existing objects. Will be passed along to the value it's holding.

        Returns:
            Tuple[Union[bool], Dict[Dict,Node]]: Return a Tuple with the first index (0) always being True if there were no errors and the second index (1) always being the check_dict
        """

        result = printExpr.value.visit(self, check_dict)
        print(result[0])
        return True, result[1]

    def visitIf(self, ifExpr : Node, check_dict : Dict[Union[Dict, List], Node]):
        result, _ = ifExpr.condition.visit(self, check_dict)
        result_dict = None
        if result:
            _, result_dict = self.__traverse_body(ifExpr.body, check_dict)
            
        if result_dict == None:
            result_dict = copy.copy(check_dict)
        return None, result_dict

    def visitWhile(self, whileExpr : Node, check_dict : Dict[Union[Dict, List], Node]):
        result, _ = whileExpr.condition.visit(self, check_dict)
        result_dict = None
        if result: 
            _, result_dict = self.__traverse_body(whileExpr.body, check_dict)
            _, result_dict = self.visitWhile(whileExpr, result_dict)
        
        if result_dict == None:
            result_dict = copy.copy(check_dict)
        return None, result_dict

    def visitFunction(self, functionExpr : Node, check_dict : Dict[Union[Dict, List], Node]):
        result_node, results_dict = self.__traverse_function_body(functionExpr.body, check_dict)
        return result_node, results_dict

    def visitReturn(self, returnExpr : Node, check_dict : Dict[Union[Dict, List], Node]):
        returnExpr.value.value = check_dict['variables'][returnExpr.value.name].value
        return returnExpr.value.visit(self, check_dict)

    def visitStart(self, startExpr : Node, check_dict : Dict[Union[Dict, List], Node]):
        # TODO zipwith gebruiken
        function_copy = copy.copy(startExpr.value)
        function_copy.set_arguments(startExpr.parameters, check_dict)
        results = function_copy.visit(self, check_dict)
        return results

    def __traverse_function_body(self, body : List[Node], check_dict : Dict[Union[Dict, List], Node]):
        if not body:
            return True, check_dict

        head, *tail = body

        if isinstance(head, (Return)):
            return head.visit(self, check_dict)

        _, result_dict = head.visit(self, check_dict)
        return self.__traverse_function_body(tail, result_dict)

    def __traverse_body(self, body : List[Node], check_dict : Dict[Union[Dict, List], Node]) -> Union[bool]:
        if not body:
            return True, check_dict

        head, *tail = body
        _, result_dict = head.visit(self, check_dict)
        return self.__traverse_body(tail, result_dict)

    def visitCondition(self, conditionExpr : Node, check_dict : Dict[Union[Dict, List], Node]):
        lhs_result, _ = conditionExpr.lhs.visit(self, check_dict)
        rhs_result, _ = conditionExpr.rhs.visit(self, check_dict)
        comparison_result = False

        if isinstance(lhs_result, (str)):
            if re.match('[0-9]', lhs_result):
                lhs_result = int(lhs_result)
                
        if isinstance(rhs_result, (str)):        
            if re.match('[0-9]', rhs_result):   
                rhs_result = int(rhs_result)
            
        if isinstance(lhs_result, (int)) and isinstance(rhs_result, (int)) :
            if conditionExpr.operator is TokenTypes.EQUAL.name:
                comparison_result = lhs_result == rhs_result
            elif conditionExpr.operator is TokenTypes.NOT_EQUAL.name:
                comparison_result = lhs_result != rhs_result
            elif conditionExpr.operator is TokenTypes.GREATER.name:
                comparison_result = lhs_result > rhs_result
            elif conditionExpr.operator is TokenTypes.NOT_GREATER.name:
                comparison_result = not (lhs_result > rhs_result)
            elif conditionExpr.operator is TokenTypes.SMALLER.name:
                comparison_result = lhs_result < rhs_result
            elif conditionExpr.operator is TokenTypes.NOT_SMALLER.name:
                comparison_result = not (lhs_result < rhs_result)
        elif isinstance(lhs_result, (str)) and isinstance(rhs_result, (str)):
            if conditionExpr.operator is TokenTypes.EQUAL.name:
                comparison_result = lhs_result == rhs_result
            elif conditionExpr.operator is TokenTypes.NOT_EQUAL.name:
                comparison_result = lhs_result != rhs_result
        else:
            print("LHS AND RHS WERE NOT OF SAME TYPE")
            exit()
        return comparison_result, check_dict


    def visitEnd(self, endExpr : Node, check_dict : Dict[Union[Dict, List], Node]):
        return None, check_dict