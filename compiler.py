from typing import List, Union

class Compiler:
    def __init__(self, parsed_tokens : List[List[Union[str,int]]]):
        self.tokens = parsed_tokens
        
    def compile(self):
        print("Compiling! jk.")
        return