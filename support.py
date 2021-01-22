from typing import List

from copy import deepcopy

syntaxParametersDict = {
    "RIGHT":0,
    "LEFT":0,
    "UP":0,
    "DOWN":0,
    "BA":1,
    "AB":0,
    "START":1,
    "SELECT":1,
    "LB":1,
    "RB":0,
    "AX":1,
    "XA":1,
    "XB":1,
    "XY":2,
    "AY":2,
    "BY":2,
    "YA":3,
    "YB":2,
    "YX":2,
    "BX":0
}

def printb(data, symbol = "=", times = 40):
    print(times * symbol)
    print(data)
    print(times * symbol)
    
def cp(data):
    return deepcopy(data)
    
class cError:
    def __init__(self, error_string : str):
        self.text = error_string
    
    def __str__(self):
        return 'Error({text})'.format(
            text = self.text
        )
        
    def throw(self):
        print(self)
        exit()
        
def throw_errors(errors : List[cError]):
    if errors:
        head, *tail = errors
        if tail:
            print(head)
            throw_errors(tail)
        else:
            head.throw()
    else:
        print("Warning : There were no errors to throw!")