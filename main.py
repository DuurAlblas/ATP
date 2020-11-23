import lexer
import parser

def readFile(filename: str) -> str:
    with open(filename) as file:
        return file.read()

def main():
    code_lines = readFile("code.tet")
    lex = lexer.Lexer(code_lines)
    print(lex.tokenize())

    print("=========================")

    i_visit = parser.Visitor()

    var_n = parser.Variable('n', parser.Literal(1))
    var_m = parser.Variable('m', parser.Binary(var_n,lexer.TokenTypes.PLUS, parser.Literal(22)))
    key_print = parser.Binary(var_m, lexer.TokenTypes.ASSIGN, parser.Print())

    key_print.visit(i_visit)

main()