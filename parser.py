from support import Node, Operators, Variable, Literal, Assignment, Operation, Print
from lexer import Lexer, TokenTypes, Token

from typing import List, Dict, Union, Tuple
import copy

class Parser():
    def __init__(self, lexer : Lexer):
        self.lexer = lexer

    def parse(self) -> Union[List[Node]]:
        tokens = self.lexer.tokenize()
        return self.__create_ast(tokens)

    def __create_ast(self, tokens : List[Token], check_dict : Dict[Dict, Node] = dict(variables=dict(), functions=dict())) -> Union[List[Node]]:
        results = ()
        if not tokens:
            return []

        if tokens[0].type == TokenTypes.VARIABLE.name:
            results = self.__add_variable_node(tokens, check_dict)
        elif tokens[0].type == TokenTypes.IF.name:
            results = self.__add_if_node(tokens, check_dict)
        # elif tokens[0].type == TokenTypes.WHILE.name:
        #     print(tokens[0])
        # elif tokens[0].type == TokenTypes.FUNCTION.name:
        #     print(tokens[0])
        # elif tokens[0].type == TokenTypes.RETURN.name:
        #     print(tokens[0])
        # elif tokens[0].type == TokenTypes.END.name:
        #     print(tokens[0])

        # If error class returned
        if len(results) == 1:
            return results

        new_node = results[0]
        new_node.extend(self.__create_ast(results[1], results[2]))
        return new_node

    def __add_if_node(self, tokens : List[Token], check_dict : Dict[Dict, Node]):
        updated_check_dict = copy.copy(check_dict)
        tokens_left = len(tokens)-1

        # Should be IF statement
        current_head = 0

        # Should be a VARIABLE
        current_head = 1
        if tokens[current_head].type is not TokenTypes.VARIABLE.name:
            print("THROW ERROR AFTER IF TOKEN EXPECTED VARIABLE TOKEN")
            exit()

        # Should be a ASSIGN
        current_head = 2
        if tokens[current_head].type is not TokenTypes.ASSIGN.name:
            print("THROW ERROR AFTER VARIABLE EXPECTED ASSIGN TOKEN")
            exit()

        # Should be a value Token
        current_head = 3
        allowed_types = [TokenTypes.VARIABLE.name, TokenTypes.INTEGER.name, TokenTypes.STRING.name]
        if tokens[current_head].type not in allowed_types:
            print("THROW ERROR THERE MUST A TOKEN THAT CAN HOLD A VALUE")
            exit()

        # Should be a comparison Token
        current_head = 4
        allowed_comparisons = [TokenTypes.EQUAL.name, TokenTypes.NOT_EQUAL.name, TokenTypes.GREATER.name, TokenTypes.NOT_GREATER.name, TokenTypes.SMALLER.name, TokenTypes.NOT_SMALLER.name]
        if tokens[current_head].type not in allowed_comparisons:
            print("THROW ERROR THERE MUST BE A VALID COMPARISON TOKEN")
            exit()

        current_head = 5
        if tokens[current_head].type not in allowed_types:
            print("THROW ERROR THERE MUST A TOKEN THAT CAN HOLD A VALUE")
            exit()

        # Create the IF node
        # Call __create_ast() to start filling the body of the IF node
        # When we encounter END IF.name stop filling body and return the filled IF node

        return 0,1,2

    def __add_variable_node(self, tokens : List[Token], check_dict : Dict[Dict, Node]) -> Union[Tuple[List[Node], List[Token], Dict[Dict,Node]]]:
        """The __add_variable_node is used to create a node where a Variable object is being assigned some sort of value.

        Args:
            tokens (List[Token]): A List of Token object from which the function will gather Tokens that belong to the Assignment.
            check_dict (Dict[Dict, Node]): A Dictionary that keeps track of existing objects. In this function it's used to determine whether a Variable exists before the user for example tries to Print it.

        Returns:
            Union[Tuple[List[Node], List[Token], Dict[Dict,Node]]]: This function returns either a Tuple containing the following objects: A List with a single Node, a List with the remaining tokens and the updated check_dict. Or a error object in case something went wrong.
        """
        # single value assignment case : n = 1 or n = m or n = print
        # binary operation assignment case : n = 1 + 1 or n = m + 1 or n = 1 + m
        updated_check_dict = copy.copy(check_dict)
        tokens_left = len(tokens)-1
        new_variable = False
        # Retrieved the variable or create it.
        current_head = 0
        if tokens[current_head].value in check_dict['variables']:
            assignment_var = check_dict['variables'].get(tokens[current_head].value)
        else:
            assignment_var = Variable(tokens[current_head].value)
            check_dict['variables'][assignment_var.name] = assignment_var
            new_variable = True

        # Check if there are tokens remaining
        current_head = 1
        if current_head > tokens_left:
            print("EXPECTED MORE TOKENS")
            exit()

        # Make sure next token is a assignment token
        current_type = tokens[current_head].type
        if tokens[current_head].type is not TokenTypes.ASSIGN.name:
            print("A ASSIGNMENT MUST TAKE PLACE")
            exit()

        # Check if there are tokens remaining
        current_head = 2
        if current_head > tokens_left:
            print("EXPECTED MORE TOKENS")
            exit()

        # Check for a value TokenType or Print
        current_type = tokens[current_head].type
        allowed_types = [TokenTypes.VARIABLE.name, TokenTypes.INTEGER.name, TokenTypes.STRING.name]
        if current_type not in allowed_types and current_type is not TokenTypes.PRINT.name:
            print("A VALUE HOLDING OBJECT MUST COME AFTER A ASSIGNMENT OPERATOR")
            exit()
        elif current_type is TokenTypes.VARIABLE.name:
            first_rhs = updated_check_dict['variables'].get(tokens[current_head].value)
        elif current_type is TokenTypes.INTEGER.name or current_type is TokenTypes.STRING.name:
            first_rhs = Literal(tokens[current_head].value)
        elif current_type is TokenTypes.PRINT.name:
            if not new_variable:
                return [Print(assignment_var)], tokens[current_head+1:], updated_check_dict
            else:
                print("CANT PRINT A UNITIALIZED VARIABLE")
                exit()

        # Check if there are tokens remaining
        current_head = 3
        if current_head > tokens_left:
            return [Assignment(assignment_var, first_rhs)], tokens[current_head:], updated_check_dict

        # Check for allowed operators
        current_type = tokens[current_head].type
        allowed_operators = [TokenTypes.PLUS.name, TokenTypes.MINUS.name, TokenTypes.DIVIDE.name, TokenTypes.TIMES.name]
        if current_type not in allowed_operators:
            return [Assignment(assignment_var, first_rhs)], tokens[current_head:], updated_check_dict
        current_operator = current_type

        # Check if there are tokens remaining
        current_head = 4
        if current_head > tokens_left:
            print("EXPECTED MORE TOKENS")
            exit()

        # Check for a value TokenType
        current_type = tokens[current_head].type
        allowed_types = [TokenTypes.VARIABLE.name, TokenTypes.INTEGER.name, TokenTypes.STRING.name]
        if current_type not in allowed_types:
            print("A VALUE HOLDING OBJECT MUST COME AFTER A ASSIGNMENT OPERATOR")
            exit()
        elif current_type is TokenTypes.VARIABLE.name:
            second_rhs = updated_check_dict['variables'].get(tokens[current_head].value)
        elif current_type is TokenTypes.INTEGER.name or current_type is TokenTypes.STRING.name:
            second_rhs = Literal(tokens[current_head].value)

        return [Assignment(assignment_var, Operation(first_rhs, current_operator, second_rhs))], tokens[current_head+1:], updated_check_dict