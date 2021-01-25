from typing import List, Union

from support import cp, syntaxParametersDict

class Parser:
    """The Parser class is used to parse tokenized Controller Code.
    """
    def __init__(self, tokens):
        self.tokens = tokens
        
    def parse(self) -> List[List[Union[str,int]]]:
        """This function parses the tokenized Controller Code.

        Returns:
            [List[List[Union[str,int]]]]: A list of parsed tokens. Each item in the list is a instructions with it's parameters.
        """
        return self.__create_list(cp(self.tokens))
        
    def __create_list(self, tokens : List[Union[str,int]]) -> List[List[Union[str,int]]]:
        """This function recursively creates the actial list of instructions.

        Args:
            tokens (List[Union[str,int]]): The Lexed tokens from which we wil create a Parsed list containing all the instructions with their parameters.

        Returns:
            List[List[Union[str,int]]]: A list of lists with instructions and their parameters.
        """
        if tokens:
            return [self.__add_instruction(cp(tokens[:1+syntaxParametersDict.get(tokens[0])]))] + self.__create_list(cp(tokens[1+syntaxParametersDict.get(tokens[0]):]))
        return []
        
    def __add_instruction(self, tokens : List[Union[str,int]]) -> List[Union[str,int]]:
        """This function adds the actual line of a instruction to the list.

        Args:
            tokens (List[Union[str,int]]): The list of tokens of which the function will get the instructions and parameters.   

        Returns:
            List[Union[str,int]]: A List with a single instruction and it's parameters.
        """
        if tokens:
            return tokens[:syntaxParametersDict.get(tokens[0])+1]
        return []