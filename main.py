from typing import List, Union

from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
from support import printb

def readFile(filename : str) -> List[str]:
	with open(filename) as file:
		raw_code = file.read().splitlines()
		return list(map(lambda word: word.upper(), raw_code))
		
def main():
	raw_code = readFile("sum.coco")
	printb(raw_code, "_______Raw Code_______",1)
	lexer = Lexer(raw_code)
	tokens_list = lexer.tokenize()
	printb(tokens_list, "_______Tokenized Tokens_______",1)
	parser = Parser(tokens_list)
	parsed_list = parser.parse()
	printb(parsed_list, "_______Parsed Tokens______",1)
	interpreter = Interpreter(parsed_list)
	interpreter.interpret()
	
main()