from typing import List, Union

class Interpreter:
    def __init__(self, parsed_tokens : List[List[Union[str,int]]]):
        self.tokens = parsed_tokens
        
    def interpret(self):
        return