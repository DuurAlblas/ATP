from support import Node, Operators, Variable, Literal, Assignment, Operation, Print, If, While, Condition, Function, Start, End
from lexer import Lexer, TokenTypes, Token

from typing import List, Dict, Union, Tuple
import copy

class Parser():
    def __init__(self, lexer : Lexer):
        self.lexer = lexer

    def parse(self) -> Union[List[Node]]:
        tokens = self.lexer.tokenize()
        return self.__create_ast(tokens,dict(variables=dict(), ifs=dict(), whiles=dict(), functions=dict(), ends=list()))

    def __create_ast(self, tokens : List[Token], check_dict : Dict[Union[Dict, List], Node]) -> Union[List[Node]]:
        results = ()
        if not tokens:
            return []

        # print("==================================")
        # print("remaining tokens : ", tokens)
        # print("==================================")

        if tokens[0].type == TokenTypes.VARIABLE.name:
            results = self.__add_variable_node(tokens, check_dict)
        elif tokens[0].type == TokenTypes.IF.name:
            results = self.__add_conditional_node(tokens, check_dict)
        elif tokens[0].type == TokenTypes.WHILE.name:
            results = self.__add_conditional_node(tokens, check_dict)
        elif tokens[0].type == TokenTypes.FUNCTION.name:
            results = self.__add_function_node(tokens, check_dict)
            
        elif tokens[0].type == TokenTypes.RETURN.name:
            results = self.__add_return_node(tokens, check_dict)
        elif tokens[0].type == TokenTypes.END.name:
            return self.__add_end_node(tokens, check_dict)

        # If error class returned
        if len(results) == 1:
            return results
        elif not results:
            print("THROW ERROR UNEXPECTED TOKEN ENCOUNTERED")
            exit()
            
        if not isinstance(results[0][0], (Function)):
            new_node = results[0]
        else:
            new_node = []
            
        new_node.extend(self.__create_ast(results[1], results[2]))
        return new_node

    def __add_function_node(self, tokens : List[Token], check_dict : Dict[Union[Dict, List], Node]):
        updated_check_dict = copy.copy(check_dict)
        # tokens_left = len(tokens)-1 TODO check for EOL
        
        # Is a FUNCTION Token
        current_head = 0
        
        # Should be a VARIABLE Token
        current_head = 1
        if tokens[current_head].type is not TokenTypes.VARIABLE.name:
            print("THROW ERROR AFTER IF TOKEN EXPECTED VARIABLE TOKEN")
            exit()
        elif self.__key_exist_in_dicts(tokens[current_head].value, [updated_check_dict['variables'], updated_check_dict['ifs'], updated_check_dict['whiles'], updated_check_dict['functions']]):
            print("THROW ERROR EXPECTED UNIQUE VARIABLE TOKEN AFTER IF TOKEN")
            exit()
            
        # Should be a ASSIGN Token
        current_head = 2
        if tokens[current_head].type is not TokenTypes.ASSIGN.name:
            print("THROW ERROR AFTER VARIABLE EXPECTED ASSIGN TOKEN")
            exit()
            
        # Should be VARIABLE Token(s)
        current_head = 3
        arguments, updated_check_dict = self.__add_arguments(tokens[current_head:], updated_check_dict)

        function_node = Function(tokens[1].value, arguments)
        updated_check_dict['ends'].append(function_node.name)
        nr_tokens = current_head + len(arguments)
        function_node.create_body(self.__create_ast(tokens[nr_tokens:], updated_check_dict))
        remaining_tokens = function_node.remaining_tokens()
        updated_check_dict = function_node.updated_check_dict()
        updated_check_dict['functions'][function_node.name] = function_node
        return [function_node], remaining_tokens, updated_check_dict
        
    def __add_arguments(self, tokens : List[Token], check_dict : Dict[Union[Dict, List], Node]) -> List[Node]:
        # tokens_left = len(tokens)-1 TODO check for EOL
        if len(tokens) < 3:
            print("THROW ERROR EXPECTED MORE TOKENS")
        current_arg, next_arg, *tail = tokens
        if self.__key_exist_in_dicts(current_arg.value, [check_dict['variables'], check_dict['ifs'], check_dict['whiles'], check_dict['functions']]):
            print("THROW ERROR VARIABLE MUST BE UNIQUE")    
            exit()
            
        ## TODO MAKE SURE IT IS NOT POSSIBLE TO NEST FUNCTIONS CUZ SCOPES
        
        # Check if the curren_arg is a VARIABLE else return no arguments
        if current_arg.type is TokenTypes.VARIABLE.name:
    
            # If it is a VARIABLE check next_arg is not ASSIGN else return no arguments
            if next_arg.type is TokenTypes.ASSIGN.name:
                return [], check_dict
                
            # If it is a VARIABLE check next_arg is not a keyword: IF WHILE FUNCTION END etc else return single argument
            not_allowed = [TokenTypes.IF.name, TokenTypes.WHILE.name, TokenTypes.END.name, TokenTypes.RETURN.name, TokenTypes.FUNCTION.name]
            if next_arg.type in not_allowed:
                arg_var = Variable(current_arg.value)
                check_dict['variables'][arg_var.name] = arg_var
                return [arg_var], check_dict
            
            # If it is a VARIABLE check next_arg is a VARIABLE if it is return __add_arguments
            if next_arg.type is TokenTypes.VARIABLE.name:
                args = [Variable(current_arg.value)]                
                check_dict['variables'][args[0].name] = args[0]
                new_arg, updated_check_dict = self.__add_arguments(tokens[2:], check_dict)
                args.extend(new_arg)
                return args, updated_check_dict

        return [], check_dict
        
    def __add_return_node(self, tokens : List[Token], check_dict : Dict[Union[Dict, List], Node]):
        return 1,2,3

    def __add_end_node(self, tokens : List[Token], check_dict : Dict[Union[Dict, List], Node]) -> End:
        updated_check_dict = copy.copy(check_dict)
    
        # Is a END Token
        current_head = 0

        # Should be either a IF, WHILE or FUNCTION Token
        current_head = 1
        allowed_endables = [TokenTypes.IF.name, TokenTypes.WHILE.name, TokenTypes.FUNCTION.name]
        if tokens[current_head].type not in allowed_endables:
            print("THROW ERROR EXPECTED A IF, WHILE OR FUNCTION TOKEN")
            exit()

        current_head = 2
        if not tokens[current_head].value == updated_check_dict['ends'][-1]:
            print("THROW ERROR EXPECTED A DIFFERENT END TOKEN")
            exit()
        else:
            updated_check_dict['ends'].pop()

        end_node = End(tokens[current_head].value, tokens[current_head+1:], updated_check_dict)

        return [end_node]

    def __add_conditional_node(self, tokens : List[Token], check_dict : Dict[Union[Dict, List], Node])-> Union[Tuple[List[Node], List[Token], Dict[Union[Dict, List], Node]]]:
        updated_check_dict = copy.copy(check_dict)
        # tokens_left = len(tokens)-1 TODO check for EOL

        # Is a IF or WHILEToken
        current_head = 0
        is_if = True
        if tokens[current_head].type is TokenTypes.WHILE.name:
            is_if = False

        # Should be a VARIABLE
        current_head = 1
        if tokens[current_head].type is not TokenTypes.VARIABLE.name:
            print("THROW ERROR AFTER IF TOKEN EXPECTED VARIABLE TOKEN")
            exit()
        elif self.__key_exist_in_dicts(tokens[current_head].value, [updated_check_dict['variables'], updated_check_dict['ifs'], updated_check_dict['whiles'], updated_check_dict['functions']]):
            print("THROW ERROR EXPECTED UNIQUE VARIABLE TOKEN AFTER IF TOKEN")
            exit()

        # Should be a ASSIGN
        current_head = 2
        if tokens[current_head].type is not TokenTypes.ASSIGN.name:
            print("THROW ERROR AFTER VARIABLE EXPECTED ASSIGN TOKEN")
            exit()

        # Should be a value Token
        current_head = 3
        allowed_types = [TokenTypes.VARIABLE.name, TokenTypes.INTEGER.name, TokenTypes.STRING.name]
        literal_types = [TokenTypes.INTEGER.name , TokenTypes.STRING.name]
        if tokens[current_head].type not in allowed_types:
            print("THROW ERROR EXPECTED A TOKEN THAT CAN HOLD A VALUE")
            exit()
        elif not self.__key_exist_in_dicts(tokens[current_head].value, [updated_check_dict['variables']]):
            print("THROW ERROR EXPECTED A VALUE HOLDING VARIABLE")
            exit()
        elif tokens[current_head].type in literal_types:
            lhs = Literal(tokens[current_head].value)
        elif tokens[current_head].type is TokenTypes.VARIABLE.name:
            lhs = updated_check_dict['variables'].get(tokens[current_head].value)

        # Should be a comparison Token
        current_head = 4
        allowed_comparisons = [TokenTypes.EQUAL.name, TokenTypes.NOT_EQUAL.name, TokenTypes.GREATER.name, TokenTypes.NOT_GREATER.name, TokenTypes.SMALLER.name, TokenTypes.NOT_SMALLER.name]
        if tokens[current_head].type not in allowed_comparisons:
            print("THROW ERROR THERE MUST BE A VALID COMPARISON TOKEN")
            exit()

        current_head = 5
        if tokens[current_head].type not in allowed_types:
            print("THROW ERROR EXPECTED A TOKEN THAT CAN HOLD A VALUE")
            exit()
        elif tokens[current_head].type in literal_types:
            rhs = Literal(tokens[current_head].value)
        elif not self.__key_exist_in_dicts(tokens[current_head].value, [updated_check_dict['variables']]):
            print("THROW ERROR EXPECTED A VALUE HOLDING VARIABLE")
            exit()
        elif tokens[current_head].type is TokenTypes.VARIABLE.name:
            rhs = updated_check_dict['variables'].get(tokens[current_head].value)

        if is_if:
            conditional_node = If(tokens[1].value, Condition(lhs, tokens[4].type, rhs))
        else:
            conditional_node = While(tokens[1].value, Condition(lhs, tokens[4].type, rhs))
            
        updated_check_dict['ends'].append(conditional_node.name)
        conditional_node.create_body(self.__create_ast(tokens[current_head+1:], updated_check_dict))

        remaining_tokens = conditional_node.remaining_tokens()
        new_dict = conditional_node.updated_check_dict()
        return [conditional_node], remaining_tokens, new_dict
        
    def __add_variable_node(self, tokens : List[Token], check_dict : Dict[Union[Dict, List], Node]) -> Union[Tuple[List[Node], List[Token], Dict[Union[Dict, List], Node]]]:
        """The __add_variable_node is used to create a node where a Variable object is being assigned some sort of value.

        Args:
            tokens (List[Token]): A List of Token object from which the function will gather Tokens that belong to the Assignment.
            check_dict (Dict[Dict, Node]): A Dictionary that keeps track of existing objects. In this function it's used to determine whether a Variable exists before the user for example tries to Print it.

        Returns:
            Union[Tuple[List[Node], List[Token], Dict[Union[Dict, List], Node]]]: This function returns either a Tuple containing the following objects: A List with a single Node, a List with the remaining tokens and the updated check_dict. Or a error object in case something went wrong.
        """
        # single value assignment case : n = 1 or n = m or n = print
        # binary operation assignment case : n = 1 + 1 or n = m + 1 or n = 1 + m
        updated_check_dict = copy.copy(check_dict)
        tokens_left = len(tokens)-1
        new_variable = False
        # Retrieved the variable or create it.
        current_head = 0
        if self.__key_exist_in_dicts(tokens[current_head].value, [check_dict['variables']]):
            assignment_var = check_dict['variables'].get(tokens[current_head].value)
        elif self.__key_exist_in_dicts(tokens[current_head].value, [check_dict['ifs'], check_dict['whiles'], check_dict['functions']]):
            print("THROW ERROR VARIABLE IS NOT UNIQUE")
            exit()
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
        allowed_types = [TokenTypes.VARIABLE.name, TokenTypes.INTEGER.name, TokenTypes.STRING.name, TokenTypes.START.name]
        if current_type not in allowed_types and current_type is not TokenTypes.PRINT.name:
            print("A VALUE HOLDING OBJECT MUST COME AFTER A ASSIGNMENT OPERATOR")
            exit()
        elif current_type is TokenTypes.VARIABLE.name:
            # TODO ADD CHECK, DOES VARIABLE EXIST?
            first_rhs = updated_check_dict['variables'].get(tokens[current_head].value)
        elif current_type is TokenTypes.INTEGER.name or current_type is TokenTypes.STRING.name:
            first_rhs = Literal(tokens[current_head].value)
        elif current_type is TokenTypes.PRINT.name:
            if not new_variable:
                return [Print(assignment_var)], tokens[current_head+1:], updated_check_dict
            else:
                print("CANT PRINT A UNITIALIZED VARIABLE")
                exit()
        elif current_type is TokenTypes.START.name:
            # Should be FUNCTION Token
            current_head = 3
            if tokens[current_head].type is not TokenTypes.FUNCTION.name:
                print("THROW ERROR EXPECTED FUNCTION TOKEN")
                exit()
                
            # Should be VARIABLE Token , the name of the FUNCTION
            current_head = 4
            if tokens[current_head].type is not TokenTypes.VARIABLE.name:
                print("THROW ERROR EXPECTED VARIABLE TOKEN, NAME OF FUNCTION")
                exit()

            nr_tokens = current_head + len(updated_check_dict['functions'][tokens[current_head].value].args) + 1
            return [Assignment(assignment_var, Start(updated_check_dict['functions'][tokens[current_head].value]))], tokens[nr_tokens:], updated_check_dict

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
            # TODO ADD CHECK, DOES VARIABLE EXIST?
            second_rhs = updated_check_dict['variables'].get(tokens[current_head].value)
        elif current_type is TokenTypes.INTEGER.name or current_type is TokenTypes.STRING.name:
            second_rhs = Literal(tokens[current_head].value)

        return [Assignment(assignment_var, Operation(first_rhs, current_operator, second_rhs))], tokens[current_head+1:], updated_check_dict

    def __key_exist_in_dicts(self, target : str, check_list : List[Dict]) -> bool:
        if not check_list:
            return False

        head, *tail = check_list
        if target in head:
            return True

        return self.__key_exist_in_dicts(target, tail)