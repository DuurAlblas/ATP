from enum import Enum
from typing import List
import re

class TokenTypes(Enum):
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
    INTEGER='[0-9]'
    STRING='".*"'
    VARIABLE='[a-zA-Z]'

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
            if word == TokenTypes.PLUS.value:
                type = TokenTypes.PLUS.name
            elif word == TokenTypes.MINUS.value:
                type = TokenTypes.MINUS.name
            elif word == TokenTypes.DIVIDE.value:
                type =  TokenTypes.DIVIDE.name
            elif word == TokenTypes.TIMES.value:
                type = TokenTypes.TIMES.name
            elif word == TokenTypes.ASSIGN.value:
                type = TokenTypes.ASSIGN.name
            elif word == TokenTypes.SMALLER.value:
                type = TokenTypes.SMALLER.name
            elif word == TokenTypes.GREATER.value:
                type = TokenTypes.GREATER.name
            elif word == TokenTypes.NOT_EQUAL.value:
                type = TokenTypes.NOT_EQUAL.name
            elif word == TokenTypes.NOT_SMALLER.value:
                type = TokenTypes.NOT_SMALLER.name
            elif word == TokenTypes.NOT_GREATER.value:
                type =  TokenTypes.NOT_GREATER.name
            elif word == TokenTypes.EQUAL.value:
                type = TokenTypes.EQUAL.name
            elif word == TokenTypes.INPUT.value:
                type = TokenTypes.INPUT.name
            elif word == TokenTypes.PRINT.value:
                type = TokenTypes.PRINT.name
            elif word == TokenTypes.FUNCTION.value:
                type = TokenTypes.FUNCTION.name
            elif word == TokenTypes.IF.value:
                type = TokenTypes.IF.name
            elif word == TokenTypes.WHILE.value:
                type = TokenTypes.WHILE.name
            elif word == TokenTypes.START.value:
                type = TokenTypes.START.name
            elif word == TokenTypes.END.value:
                type = TokenTypes.END.name
            elif re.match(TokenTypes.INTEGER.value, word):
                type = TokenTypes.INTEGER.name
            elif re.match(TokenTypes.STRING.value, word):
                type = TokenTypes.STRING.name
            elif re.match(TokenTypes.VARIABLE.value, word):
                type = TokenTypes.VARIABLE.name

            if type == None:
                raise TypeError(word)

        except TypeError as Unknown_Type:
            print("Couldn't find token type of ",Unknown_Type,"!")
            raise

        return Token(word, type)