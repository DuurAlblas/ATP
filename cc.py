import sys, getopt

from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
from compiler import Compiler
from support import printb, readFile, cError

def main(argv):
	help_message = "Controller Code. cc.py\n"
	help_message += "-h or --help | This help message\n -f or --file <code.coco> | A file with the .coco extension. Contains Controller Code\n -i or --input <int,int> | Give the Controller Code application input, maximum of 2 arguments\n -I | Use the application in Interpreter Mode (Default)\n -C | Use the application in Compiler Mode\n -v or --verbose | Print extra information\n -o or --output <coco.asm> | Used to specify the name of you compiled output file"
	code_file = "code.coco"
	asm_file = "coco.asm"
	app_mode = 1 # Mode 1 is Interpreter, Mode 0 is Compiler
	verbose = False
	input_list = []
	
	try:
		options, _ = getopt.getopt(argv, "hf:i:ICvo:", ["help","file=","input=","verbose","output="])
	except getopt.GetoptError:
		cError("GetoptError: Try cc.py -h or --help.").throw()
	
	for option, arg in options:
		if option in ("-h", "--help"):
			print(help_message)
			exit()
		elif option in ("-f", "--file"):
			if arg.endswith(".coco"):
				code_file = arg
				if asm_file == "coco.asm":
					asm_file = code_file.split(".")[-1] + ".asm"
			else:
				cError("File Error: The supplied input file does not have the file extension `.coco`.").throw()
		elif option in ("-i", "--input"):
			try:
				input_list = list(map(int,arg.split(',')))
			except:
				cError("ValueError: The input values have not been given correctly. Should be as follows: `-i 5,2`.").throw()
				
		elif option in ("-I"):
			app_mode = 1
		elif option in ("-C"):
			app_mode = 0
			input_list = [0,0]
		elif option in ("-v", "--verbose"):
			verbose = True
		elif option in ("-o", "--output"):
			if arg.endswith(".asm"):
				asm_file = arg
			else:
				cError("File Error: The supplied output file name does not have the file extension `.asm`.").throw()
	
	"""In the main function the following things happen in succession:
	- Read a Controller Code file so we have a list of strings, the raw code, each line of code is 1 item in the list.
	- Supply the raw code to the Lexer which will make 1 large list of all the tokens, it will also recognize strings that are integers and cast them to integers.
		This is also where the syntax checking takes place, if there are any problems in the syntax of the code the program will print them all and exit.
	- Supply the lexed code, tokens list, to the Parser. The Parser wil gather instructions with their parameters. At then end there will be a list of lists with strings, instructions, and where applicable inttegers, paramters.
	If the selected mode is Interpret:
		- Supply the parsed code, parsed list, to the Interpreter. The Interpreter wil execute the code. Since the `BX` instruction will stop execution the application will exit when it encounters that instruction.
	Elif the selected mode is Compile
		- Supply the parsed code, parsed list, to the Compiler. The Compiler will rewrite the code in assembly and export it to the supplied file name. 
	"""
	
	raw_code = readFile(code_file)
	if verbose:
		printb(raw_code, "_______Raw Code_______",1) 
	lexer = Lexer(raw_code)
	tokens_list = lexer.tokenize(input_list)
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
		interpreter.interpret(input_list)
	else:
		compiler = Compiler(parsed_list, asm_file, 64)
		compiled_code = compiler.compile()
		if verbose:
			print("_______Compiled Result_______")
			print(compiled_code)
		compiler.export(compiled_code)
	
if __name__ == "__main__":
	main(sys.argv[1:])