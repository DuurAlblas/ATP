# Get required support classes
from support import Token, TokenTypes

from typing import List, Union
import re

class Lexer():
    """Lexer class to tokenize a string of code
    TODO Error class
    """
    def __init__(self, code : str):
        self.source = code

    def tokenize(self) -> List[Token]:
        """Function that will split the string so we have single words. Next call __add_tokens()
        """
        source_code = self.source.split()
        return self.__add_tokens(source_code)

    def __add_tokens(self, source_code : List[str]) -> Union[List[Token]]:
        """Private function that will recursively determine the type of token of each word using __get_token()
        TODO MAP
        """
        current_word, *tail = source_code
        if not tail:
            return self.__get_token(current_word)

        result = self.__get_token(current_word)
        if isinstance(result, (List)):
            result.extend(self.__add_tokens(tail))
        return result

    def __get_token(self, word : str) -> Union[List[Token]]:
        """Function to determine the type of token a single word is.
        TODO Remove raise and return a custom error class
        """
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
                word = word[1:-1]
            elif re.match(TokenTypes.VARIABLE.value, word):
                type = TokenTypes.VARIABLE.name


        # REMOVE RAISE ERROR , RETURN ERROR CLASS OBJECT
            if type == None:
                raise TypeError(word)

        except TypeError as Unknown_Type:
            print("Couldn't find token type of ",Unknown_Type,"!")
            raise

        return [Token(word, type)]