from typing import List, Union

from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
from support import printb, readFile
		
def main():
	"""In the main function the following things happen in succession:
	- Read a Controller Code file so we have a list of strings, the raw code, each line of code is 1 item in the list.
	- Supply the raw code to the Lexer which will make 1 large list of all the tokens, it will also recognize strings that are integers and cast them to integers.
		This is also where the syntax checking takes place, if there are any problems in the syntax of the code the program will print them all and exit.
	- Supply the lexed code, tokens list, to the Parser. The Parser wil gather instructions with their parameters. At then end there will be a list of lists with strings, instructions, and where applicable inttegers, paramters.
	- Supply the parsed code, parsed list, to the Interpreter. The Interpreter wil execute the code. Since the `BX` instruction will stop execution the application will exit when it encounters that instruction.
	"""
	raw_code = readFile("loopy.coco")
	printb(raw_code, "_______Raw Code_______",1)
	lexer = Lexer(raw_code)
	tokens_list = lexer.tokenize()
	printb(tokens_list, "_______Tokenized Tokens_______",1)
	parser = Parser(tokens_list)
	parsed_list = parser.parse()
	printb(parsed_list, "_______Parsed Tokens______",1)
	interpreter = Interpreter(parsed_list)
	print("_______Interpreted Result_______")
	interpreter.interpret()
	
main()