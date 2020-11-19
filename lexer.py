from typing import List
import re

TOKEN_TYPES = {
    'OPERATORS': ['plus','minus','divide','times', '='],
    'CONDITIONS' : ['<','>','~','~<','~>','~~'],
    'input' : 'INPUT',
    'print' : 'PRINT',
    'function' : 'FUNCTION',
    'if' : 'IF',
    'while' : 'WHILE',
    'start' : 'START',
    'end' : 'END'
}

class Token():
    def __init__(self, value, type):
        self.value = value
        self.type = type

    def __str__(self):
        return 'Token({value}, {type})'.format(value=repr(self.value), type=self.type)

    def __repr__(self):
        return self.__str__()

class Lexer():
    def __init__(self, code : str):
        self.source = code

    def tokenize(self) -> List[Token]:
        source_code = self.source.split()
        return self.__add_tokens(source_code)

    def __add_tokens(self, source_code : List[str]) -> List[Token]:
        current_word, *tail = source_code
        if len(tail) == 0:
            return [self.__get_token(current_word)]

        result = [self.__get_token(current_word)]
        result.extend(self.__add_tokens(tail))
        return result

    def __get_token(self, word : str) -> Token:
        type = None
        try:
            if word in TOKEN_TYPES['OPERATORS']:
                type = 'OPERATOR'
            elif word in TOKEN_TYPES['CONDITIONS']:
                type = 'CONDITION'
            elif word in TOKEN_TYPES:
                type = TOKEN_TYPES[word]
            elif re.match('[0-9]', word):
                type = 'INTEGER'
            elif re.match('[a-z]', word) or re.match('[A-Z]', word):
                type = 'VARIABLE'

            if type == None:
                raise TypeError(word)

        except TypeError as Unknown_Type:
            print("Couldn't find token type of ",Unknown_Type,"!")
            raise

        return Token(word, type)