from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

def readFile(filename: str) -> str:
    with open(filename) as file:
        return file.read()

def main():
    code_lines = readFile("code.tet")
    lexer = Lexer(code_lines)
    print(lexer.tokenize())

    print("=========================")

    parser = Parser(lexer)
    ast = parser.parse()
    for item in ast:
        print(item)

    print("=========================")

    interpreter = Interpreter(ast)
    # interpreter.interpret()

main()