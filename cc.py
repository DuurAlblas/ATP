import os, sys, getopt
from typing import List, Union

from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
from compiler import Compiler
from support import printb, readFile, cError
		
def main(argv):
	
	help_message = "Controller Code. cc.py\n"
	help_message += "-h or --help | This help message\n -f or --file <code.coco> | A file with the .coco extension. Contains Controller Code\n -I | Use the application in Interpreter Mode (Default)\n -C | Use the application in Compiler Mode\n -v or --verbose | Print extra information\n"
	code_file = "code.coco"
	app_mode = 1 # Mode 1 is Interpreter, Mode 0 is Compiler
	verbose = False
	
	try:
		options, _ = getopt.getopt(argv, "hf:ICv", ["help","file=","verbose"])
	except getopt.GetoptError:
		cError("GetoptError: Try cc.py -h or --help.").throw()
	
	for option, arg in options:
		if option in ("-h", "--help"):
			print(help_message)
			exit()
		elif option in ("-f", "--file"):
			if arg.endswith(".coco"):
				code_file = arg
			else:
				cError("File Error: The supplied file does not have the file extension `.coco`.").throw()
		elif option in ("-I"):
			app_mode = 1
		elif option in ("-C"):
			app_mode = 0
		elif option in ("-v", "--verbose"):
			verbose = True
	
	if not os.path.exists(code_file):
		cError("File Error: The supplied file `"+code_file+"` doesn't exist").throw()
	
	"""In the main function the following things happen in succession:
	- Read a Controller Code file so we have a list of strings, the raw code, each line of code is 1 item in the list.
	- Supply the raw code to the Lexer which will make 1 large list of all the tokens, it will also recognize strings that are integers and cast them to integers.
		This is also where the syntax checking takes place, if there are any problems in the syntax of the code the program will print them all and exit.
	- Supply the lexed code, tokens list, to the Parser. The Parser wil gather instructions with their parameters. At then end there will be a list of lists with strings, instructions, and where applicable inttegers, paramters.
	- Supply the parsed code, parsed list, to the Interpreter. The Interpreter wil execute the code. Since the `BX` instruction will stop execution the application will exit when it encounters that instruction.
	"""
	raw_code = readFile(code_file)
	if verbose:
		printb(raw_code, "_______Raw Code_______",1) 
	lexer = Lexer(raw_code)
	tokens_list = lexer.tokenize()
	if verbose:
		printb(tokens_list, "_______Tokenized Tokens_______",1) 
	parser = Parser(tokens_list)
	parsed_list = parser.parse()
	if verbose:
		printb(parsed_list, "_______Parsed Tokens______",1)
	if app_mode:
		interpreter = Interpreter(parsed_list)
		if verbose:
			print("_______Interpreted Result_______") 
		interpreter.interpret()
	else:
		compiler = Compiler(parsed_list)
		compiler.compile()
	
if __name__ == "__main__":
	main(sys.argv[1:])