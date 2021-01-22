from typing import List, Union

from support import cp, syntaxParametersDict

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        
    def parse(self):
        return self.__create_list(cp(self.tokens))
        
    def __create_list(self, tokens : List[Union[str,int]]) -> List[List[Union[str,int]]]: 
        if tokens:
            return [self.__add_instruction(cp(tokens[:1+syntaxParametersDict.get(tokens[0])]))] + self.__create_list(cp(tokens[1+syntaxParametersDict.get(tokens[0]):]))
        return []
        
    def __add_instruction(self, tokens : List[Union[str,int]]) -> List[Union[str,int]]:
        if tokens:
            return tokens[:syntaxParametersDict.get(tokens[0])+1]
        return []