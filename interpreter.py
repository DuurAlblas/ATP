from support import Node, Visitor

from typing import List, Dict, Union

class Interpreter():
    def __init__(self, ast : List[Node]):
        self.ast = ast

    def interpret(self) -> Union[bool]:
        check_dict = dict(variables=dict(), functions=dict())
        visitor = Visitor()
        return self.__traverse(self.ast, visitor, check_dict)

    def __traverse(self, ast : List[Node], visitor : Visitor(), check_dict : Dict[Dict, Node]) -> Union[bool]:
        if not ast:
            return True

        head, *tail = ast
        # print("Current Head : ", head)
        _, result = head.visit(visitor, check_dict)
        return self.__traverse(tail, visitor, result)