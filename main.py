import lexer
import parser

def readFile(filename: str) -> str:
    with open(filename) as file:
        return file.read()

def main():
    code_lines = readFile("code.tet")
    lex = lexer.Lexer(code_lines)
    print(lex.tokenize())

main()