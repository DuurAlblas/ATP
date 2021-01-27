from typing import List, Union

from support import cp

#This dictionary is used to call functions that belong to instructions.
compilerDict = {
	"RIGHT" : lambda line, *params : RIGHT(line),
	"LEFT" : lambda line, *params : LEFT(line),
	"UP" : lambda line, *params : UP(line),
	"DOWN" : lambda line, *params : DOWN(line),
	"BA" : lambda line, *params : BA(line, params[0]),
	"AB" : lambda line, *params : AB(line),
	"START" : lambda line, *params : START(line, params[0]),
	"SELECT" : lambda line, *params : SELECT(line, params[0]),
	"LB" : lambda line, *params : LB(line, params[0]),
	"RB" : lambda line, *params : RB(line),
	"AX" : lambda line, *params : AX(line, params[0]),
	"XA" : lambda line, *params : XA(line, params[0]),
	"XB" : lambda line, *params : XB(line, params[0]),
	"XY" : lambda line, *params : XY(line, params[0], params[1]),
	"AY" : lambda line, *params : AY(line, params[0], params[1]),
	"BY" : lambda line, *params : BY(line, params[0], params[1]),
	"YA" : lambda line, *params : YA(line, params[0], params[1]),
	"YB" : lambda line, *params : YB(line, params[0], params[1]),
	"YX" : lambda line, *params : YX(line, params[0], params[1]),
	"BX" : lambda line, *params : BX(line)
}

def getAddress(memory_address : int, target_register : str) -> str:
	move_address		= "\nMOV "+target_register+", #"+str(memory_address)
	move_multiplier 	= "\nMOV R3, #4"
	calculate_address 	= "\nMUL "+target_register+", "+target_register+", R3"
	adjust_address 		= "\nSUB "+target_register+", R5, "+target_register
	return move_address + move_multiplier + calculate_address + adjust_address

def RIGHT(line) -> str:
	line_label 			= "\nl_"+str(line)+":"
	next 				= "\nSUB R4, #4"
	return line_label + next
	
def LEFT(line) -> str:
	line_label 			= "\nl_"+str(line)+":"
	previous 			= "\nADD R4, #4"
	return line_label + previous

def UP(line) -> str:
	line_label 			= "\nl_"+str(line)+":"
	load 				= "\nLDR R0, [R4]"
	increase 			= "\nADD R0, #1"
	store 				= "\nSTR R0, [R4]"
	return line_label + load + increase + store

def DOWN(line) -> str:
	line_label 			= "\nl_"+str(line)+":"
	load 				= "\nLDR R0, [R4]"
	decrease 			= "\nSUB R0, #1"
	store 				= "\nSTR R0, [R4]"
	return line_label + load + decrease + store

def BA(line, identifier : int) -> str:
	line_label 			= "\nl_"+str(line)+":"
	label 				= "\nf_"+str(identifier)+":"
	save_lr 			= "\nPUSH {LR}"
	return line_label + label+save_lr
	
def AB(line) -> str:
	line_label 			= "\nl_"+str(line)+":"
	load_lr 			= "\nPOP {PC}"
	return line_label + load_lr
	
def START(line, identifier : int) -> str:
	line_label 			= "\nl_"+str(line)+":"
	branch_l 			= "\nBL f_"+str(identifier)
	return line_label + branch_l
	
def SELECT(line, line_nr : int) -> str:
	line_label 			= "\nl_"+str(line)+":"
	branch 				= "\nB l_"+str(line_nr)
	return line_label + branch
	
def LB(line, memory_address : int) -> str:
	line_label 			= "\nl_"+str(line)+":"
	move_address 		= "\nMOV R0, #"+str(memory_address)
	move_multiplier 	= "\nMOV R1, #4"
	calculate_address 	= "\nMUL R0, R0, R1"
	adjust_address 		= "\nSUB R0, R5, R0"
	move_value 			= "\nMOV R4, R0"
	return line_label + move_address + move_multiplier + calculate_address + adjust_address + move_value
	
def RB(line) -> str:
	line_label 			= "\nl_"+str(line)+":"
	load_value 			= "\nLDR R0, [R4]"
	branch_l 			= "\nBL print"
	return line_label + load_value + branch_l
	
def AX(line, value : int) -> str:
	line_label 			= "\nl_"+str(line)+":"
	move_value 			= "\nMOV R0, #" + str(value)
	store_value 		= "\nSTR R0, [R4]"
	return line_label + move_value + store_value
	
def XA(line, memory_address : int) -> str:
	line_label 			= "\nl_"+str(line)+":"
	load_address 		= getAddress(memory_address, "R0")
	load_value 			= "\nLDR R1, [R0]"
	store_value 		= "\nSTR R1, [R4]"
	return line_label + load_address + load_value + store_value
	
def XB(line, memory_address : int) -> str:
	line_label 			= "\nl_"+str(line)+":"
	load_address		= getAddress(memory_address, "R0")
	load_value 			= "\nLDR R1, [R4]"
	store_value 		= "\nSTR R1, [R0]"	
	return line_label + load_address + load_value + store_value
	
def XY(line, memory_address_a : int,  memory_address_b : int) -> str:
	line_label 			= "\nl_"+str(line)+":"
	load_address_a 		= getAddress(memory_address_a, "R0")
	load_address_b		= getAddress(memory_address_b, "R1")
	load_value_a		= "\nLDR R0, [R0]"
	load_value_b		= "\nLDR R1, [R1]"	
	compare				= "\nCMP R0, R1"
	equal				= "\nBEQ l_"+str(line+1)
	not_equal			= "\nBNE l_"+str(line+2)
	return line_label + load_address_a + load_address_b + load_value_a + load_value_b + compare + equal + not_equal
	
def AY(line, memory_address_a : int,  memory_address_b : int) -> str:
	line_label 			= "\nl_"+str(line)+":"
	load_address_a		= getAddress(memory_address_a, "R0")
	load_address_b		= getAddress(memory_address_b, "R1")
	load_value_a		= "\nLDR R0, [R0]"
	load_value_b		= "\nLDR R1, [R1]"
	compare				= "\nCMP R0, R1"
	greather_than		= "\nBGT l_"+str(line+1)
	less_than_equal		= "\nBLE l_"+str(line+2)
	return line_label + load_address_a + load_address_b + load_value_a + load_value_b + compare + greather_than + less_than_equal
	
def BY(line, memory_address_a : int,  memory_address_b : int) -> str:
	line_label 			= "\nl_"+str(line)+":"
	load_address_a		= getAddress(memory_address_a, "R0")
	load_address_b		= getAddress(memory_address_b, "R1")
	load_value_a		= "\nLDR R0, [R0]"
	load_value_b		= "\nLDR R1, [R1]"
	compare				= "\nCMP R0, R1"
	less_than			= "\nBGT l_"+str(line+1)
	greater_than_equal 	= "\nBLE l_"+str(line+2)
	return line_label + load_address_a + load_address_b + load_value_a + load_value_b + compare + less_than + greater_than_equal
	
def YA(line, memory_address_a : int,  memory_address_b : int) -> str:
	line_label 			= "\nl_"+str(line)+":"
	load_address_a		= getAddress(memory_address_a, "R0")
	load_address_b		= getAddress(memory_address_b, "R1")
	load_value_a		= "\nLDR R2, [R0]"
	load_value_b		= "\nLDR R1, [R1]"
	calculate_result 	= "\nMUL R2, R1"
	save_result 		= "\nSTR R2, [R0]"
	return line_label + load_address_a + load_address_b + load_value_a + load_value_b + calculate_result + save_result
	
def YB(line, memory_address_a : int,  memory_address_b : int) -> str:
	line_label 			= "\nl_"+str(line)+":"
	load_address_a 		= getAddress(memory_address_a, "R0")
	load_address_b		= getAddress(memory_address_b, "R1")
	load_value_a		= "\nLDR R2, [R0]"
	load_value_b		= "\nLDR R1, [R1]"
	calculate_result	= "\nADD R2, R1"
	save_result 		= "\nSTR R2, [R0]"
	return line_label + load_address_a + load_address_b + load_value_a + load_value_b + calculate_result + save_result
	
def YX(line, memory_address_a : int,  memory_address_b : int) -> str:
	line_label 			= "\nl_"+str(line)+":"
	load_address_a 		= getAddress(memory_address_a, "R0")
	load_address_b		= getAddress(memory_address_b, "R1")
	load_value_a		= "\nLDR R2, [R0]"
	load_value_b		= "\nLDR R1, [R1]"
	calculate_result	= "\nSUB R2, R1"
	save_result 		= "\nSTR R2, [R0]"
	return line_label + load_address_a + load_address_b + load_value_a + load_value_b + calculate_result + save_result
	
def BX(line) -> str:
	line_label 			= "\nl_"+str(line)+":"
	load_stack_pointer 	= "\nMOV SP, R5"
	load_registers		= "\nPOP {R4,R5,R6,R7,PC}"
	return line_label + load_stack_pointer + load_registers

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
			cur_function = self.__create_lines(cp(tokens),start,end+1)
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
		return cur_body + self.__create_body(cp(tokens), cp(instruction_list), start+1)

	def __create_lines(self, tokens : List[List[Union[str,int]]], start : int, end : int) -> str:
		if start < end:
			return compilerDict.get(tokens[start][:1][0])(start+1, *cp(tokens[start][1:])) + self.__create_lines(cp(tokens), start+1, end)
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