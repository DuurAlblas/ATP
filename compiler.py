from typing import List, Union

from support import cp

#This dictionary is used to call functions that belong to instructions.
compilerDict = {
	"RIGHT" : lambda *params : RIGHT(),
	"LEFT" : lambda *params : LEFT(),
	"UP" : lambda *params : UP(),
	"DOWN" : lambda *params : DOWN(),
	"BA" : lambda *params : BA(params[0]),
	"AB" : lambda *params : AB(),
	"START" : lambda *params : START(params[0]),
	"SELECT" : lambda *params : SELECT(params[0]),
	"LB" : lambda *params : LB(params[0]),
	"RB" : lambda *params : RB(),
	"AX" : lambda *params : AX(params[0]),
	"XA" : lambda *params : XA(params[0]),
	"XB" : lambda *params : XB(params[0]),
	"XY" : lambda *params : XY(params[0], params[1]),
	"AY" : lambda *params : AY(params[0], params[1]),
	"BY" : lambda *params : BY(params[0], params[1]),
	"YA" : lambda *params : YA(params[0], params[1], params[2]),
	"YB" : lambda *params : YB(params[0], params[1]),
	"YX" : lambda *params : YX(params[0], params[1]),
	"BX" : lambda *params : BX()
}

def RIGHT():
	return "\nRIGHT"
	
def LEFT():
	return "\nLEFT"

def UP():
	return "\nUP"

def DOWN():
	return "\nDOWN"

def BA(identifier : int):
	return "\nBA" + " param " + str(identifier)
	
def AB():
	return "\nAB"
	
def START(identifier : int):
	return "\nSTART" + " param " + str(identifier)
	
def SELECT(line_nr : int):
	return "\nSELECT" + " param " + str(line_nr)
	
def LB(memory_address : int):
	return "\nLB" + " param " + str(memory_address)
	
def RB():
	return "\nRB"
	
def AX(value : int):
	return "\nAX" + " param " + str(value)
	
def XA(memory_address : int):
	return "\nXA" + " param " + str(memory_address)
	
def XB(memory_address):
	return "\nXB" + " param " + str(memory_address)
	
def XY(memory_address_a : int,  memory_address_b : int):
	return "\nXY" + " param a " + str(memory_address_a) + " param b " + str(memory_address_b)
	
def AY(memory_address_a : int,  memory_address_b : int):
	return "\nAY" + " param a " + str(memory_address_a) + " param b " + str(memory_address_b)
	
def BY(memory_address_a : int,  memory_address_b : int):
	return "\nBY" + " param a " + str(memory_address_a) + " param b " + str(memory_address_b)
	
def YA(memory_address_a : int,  memory_address_b : int, memory_address_c : int):
	return "\nYA" + " param a " + str(memory_address_a) + " param b " + str(memory_address_b) + " param c " + str(memory_address_c)
	
def YB(memory_address_a : int,  memory_address_b : int):
	return "\nYB" + " param a " + str(memory_address_a) + " param b " + str(memory_address_b)
	
def YX(memory_address_a : int,  memory_address_b : int):
	return "\nYX" + " param a " + str(memory_address_a) + " param b " + str(memory_address_b)
	
def BX():
	return "\nBX"
		
class Compiler:
	def __init__(self, parsed_tokens : List[List[Union[str,int]]], asm_file : str, memory_size : int):
		self.tokens = parsed_tokens
		self.coco_lines = list(map(lambda line : line[0], parsed_tokens)) #map 5/3
		self.file = asm_file
		self.memory_size = memory_size

	def compile(self) -> str:
		code_label = self.file.split('.')[0]
		asm_code 	= self.__initialize_file(code_label)
		asm_code   += self.__create_functions(cp(self.tokens), cp(self.coco_lines))
		asm_code   += self.__initialize_code(code_label, self.memory_size)
		asm_code   += self.__create_body(cp(self.tokens), cp(self.coco_lines))
		return asm_code

	def __create_functions(self, tokens : List[List[Union[str,int]]], instruction_list : List[str], index_end = 0) -> str:
		try:
			start = instruction_list.index("BA", index_end)
			end = instruction_list.index("AB",index_end+1)
			cur_function = self.__create_lines(cp(tokens),start,end)
		except:
			return "\n"
		return cur_function + self.__create_functions(cp(tokens),cp(instruction_list), end)
		
	def __create_body(self, tokens : List[List[Union[str,int]]], instruction_list : List[str], index_start = 0) -> str:
		try:
			end = instruction_list.index("BA", index_start)
			start = instruction_list.index("AB", index_start+1) 
			cur_body = self.__create_lines(cp(tokens), index_start, end)
		except:
			return self.__create_lines(cp(tokens), index_start, len(instruction_list))
		return cur_body + self.__create_body(cp(tokens), cp(instruction_list), start)

	def __create_lines(self, tokens : List[List[Union[str,int]]], start : int, end : int) -> str:
		if start < end:
			return "\nl_"+str(start+1)+":" +compilerDict.get(tokens[start][:1][0])(*cp(tokens[start][1:])) + self.__create_lines(cp(tokens), start+1, end)
		return ""

	def __initialize_file(self, code_label : str) -> str:
		section 	= "\n.section .text"
		align 		= "\n.align 4"
		external 	= "\n.global "+code_label
		return section + align + external + "\n"

	def __initialize_code(self, code_label : str, memory_size : int) -> str:
		start_label 			= "\n"+code_label+":"
		save_registers 			= "\nPUSH {R4,R5,R6,R7,LR}"
		create_memory_pointer 	= "\nMOV R4, SP"
		save_stack_pointer 		= "\nMOV R5, SP"
		protect_address_zero 	= "\nSUB R4, #4"
		allocate_memory_size 	= "\nSUB SP, #"+str(memory_size * 4)
		#save_program_counter = "\nMOV R6, PC"
		return start_label+save_registers+create_memory_pointer+save_stack_pointer+protect_address_zero+allocate_memory_size

	def export(self, compiled_code : str):
		with open(self.file, "w") as file:
			file.write(compiled_code)
		return 