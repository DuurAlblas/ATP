from typing import List, Union

from support import cp, getAddress

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
	"ZL" : lambda line, *params : ZL(line, params[0], params[1]),
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

def RIGHT(line : int) -> str:
	"""Writes the `RIGHT` instruction.
	Go to the next address.

	Args:
		line (int): The line number of the current instruction

	Returns:
		str: A string containing a label to the instruction and the instruction itself.
	"""
	line_label 			= "\nl_"+str(line)+":"
	next 				= "\nSUB R4, #4"
	return line_label + next
	
def LEFT(line : int) -> str:
	"""Writes the `LEFT` instruction.
	Go to the previous address.

	Args:
		line (int): The line number of the current instruction

	Returns:
		str: A string containing a label to the instruction and the instruction itself.
	"""
	line_label 			= "\nl_"+str(line)+":"
	previous 			= "\nADD R4, #4"
	return line_label + previous

def UP(line : int) -> str:
	"""Writes the `UP` instruction.
	Increase the byte of the memory address where the memory pointer is pointing

	Args:
		line (int): The line number of the current instruction

	Returns:
		str: A string containing a label to the instruction and the instruction itself.
	"""
	line_label 			= "\nl_"+str(line)+":"
	load 				= "\nLDR R0, [R4]"
	increase 			= "\nADD R0, #1"
	store 				= "\nSTR R0, [R4]"
	return line_label + load + increase + store

def DOWN(line : int) -> str:
	"""Writes the `DOWN` instruction.
	Decrease the byte of the memory address where the memory pointer is pointing

	Args:
		line (int): The line number of the current instruction

	Returns:
		str: A string containing a label to the instruction and the instruction itself.
	"""
	line_label 			= "\nl_"+str(line)+":"
	load 				= "\nLDR R0, [R4]"
	decrease 			= "\nSUB R0, #1"
	store 				= "\nSTR R0, [R4]"
	return line_label + load + decrease + store

def BA(line : int, identifier : int) -> str:
	"""Writes the `BA` instruction.
	Create labels and push the LR.

	Args:
		line (int): The line number of the current instruction
		identifier (int): The identifier of the instruction.

	Returns:
		str: A string containing a label to the instruction and the instruction itself.
	"""
	line_label 			= "\nl_"+str(line)+":"
	label 				= "\nf_"+str(identifier)+":"
	save_lr 			= "\nPUSH {LR}"
	return line_label + label+save_lr
	
def AB(line : int) -> str:
	"""Writes the `AB` instruction.
	Pop the LR back to the PC.

	Args:
		line (int): The line number of the current instruction

	Returns:
		str: A string containing a label to the instruction and the instruction itself.
	"""
	line_label 			= "\nl_"+str(line)+":"
	load_lr 			= "\nPOP {PC}"
	return line_label + load_lr
	
def START(line : int, identifier : int) -> str:
	"""Writes the `START` instruction.
	Branch link to the function label with the corresponding identifier.

	Args:
		line (int): The line number of the current instruction
		identifier (int): The identifier of the instruction.

	Returns:
		str: A string containing a label to the instruction and the instruction itself.
	"""
	line_label 			= "\nl_"+str(line)+":"
	branch_l 			= "\nBL f_"+str(identifier)
	return line_label + branch_l
	
def SELECT(line : int, line_nr : int) -> str:
	"""Writes the `SELECT` instruction.
	Branch to a line label.

	Args:
		line (int): The line number of the current instruction
		line_nr (int): The line number of the line to jump to

	Returns:
		str: A string containing a label to the instruction and the instruction itself.
	"""	
	line_label 			= "\nl_"+str(line)+":"
	branch 				= "\nB l_"+str(line_nr)
	return line_label + branch
	
def ZL(line : int, argument : int, memory_address : int) -> str:
	"""Writes the `ZL` instruction.
	Retrieves a input argument and stores it in the supplied memory address.
	WARNING! Controller Code only accepts 2 arguments. If you ask for, for example, the third argument there will be undefined behavior.

	Args:
		line (int): The line number of the current instruction
		argument (int): The number of the argument you want to store (Only 1 or 2).
		memory_address (int): The memory address in which the input argument will be stored.

	Returns:
		str: A string containing a label to the instruction and the instruction itself.
	"""
	line_label 			= "\nl_"+str(line)+":"
	load_address 		= getAddress(memory_address, "R2")
	store_argument		= "\nSTR R"+str(argument -1) + ", [R2]"
	return line_label + load_address + store_argument
	
def LB(line : int, memory_address : int) -> str:
	"""Writes the `LB` instruction.
	Jump to a memory address.

	Args:
		line (int): The line number of the current instruction
		memory_address (int): The memory address to jump to

	Returns:
		str: A string containing a label to the instruction and the instruction itself.
	"""
	line_label 			= "\nl_"+str(line)+":"
	move_address 		= "\nMOV R0, #"+str(memory_address)
	move_multiplier 	= "\nMOV R1, #4"
	calculate_address 	= "\nMUL R0, R0, R1"
	adjust_address 		= "\nSUB R0, R5, R0"
	move_value 			= "\nMOV R4, R0"
	return line_label + move_address + move_multiplier + calculate_address + adjust_address + move_value
	
def RB(line : int) -> str:
	"""Writes the `RB` instruction.
	Print whatever is stored in the memory address the memory pointer is currently pointing to.
	WARNING! To use this instruction there has to be a extern "C" print(int x) function.

	Args:
		line (int): The line number of the current instruction

	Returns:
		str: A string containing a label to the instruction and the instruction itself.
	"""
	line_label 			= "\nl_"+str(line)+":"
	load_value 			= "\nLDR R0, [R4]"
	branch_l 			= "\nBL print"
	return line_label + load_value + branch_l
	
def AX(line : int, value : int) -> str:
	"""Writes the `AX` instruction.
	Store the supplied in the memory addres the memory pointer is pointing to.

	Args:
		line (int): The line number of the current instruction
		value (int): The value to store

	Returns:
		str: A string containing a label to the instruction and the instruction itself.
	"""
	line_label 			= "\nl_"+str(line)+":"
	move_value 			= "\nMOV R0, #" + str(value)
	store_value 		= "\nSTR R0, [R4]"
	return line_label + move_value + store_value
	
def XA(line : int, memory_address : int) -> str:
	"""Writes the `XA` instruction.
	Store the value from the supplied memory address in the memory address the memory pointer is pointing to.

	Args:
		line (int): The line number of the current instruction
		memory_address (int): The memory address whose value we want to copy to the memory pointer memory address.

	Returns:
		str: A string containing a label to the instruction and the instruction itself.
	"""
	line_label 			= "\nl_"+str(line)+":"
	load_address 		= getAddress(memory_address, "R0")
	load_value 			= "\nLDR R1, [R0]"
	store_value 		= "\nSTR R1, [R4]"
	return line_label + load_address + load_value + store_value
	
def XB(line : int, memory_address : int) -> str:
	"""Writes the `XB` instruction.
	Store the value from the memory address the memory pointer is pointing to in the memory of the supplied memory address.

	Args:
		line (int): The line number of the current instruction
		memory_address (int): The memory address to where we want to copy the value of the memory pointer memory address to.

	Returns:
		str: A string containing a label to the instruction and the instruction itself.
	"""
	line_label 			= "\nl_"+str(line)+":"
	load_address		= getAddress(memory_address, "R0")
	load_value 			= "\nLDR R1, [R4]"
	store_value 		= "\nSTR R1, [R0]"	
	return line_label + load_address + load_value + store_value
	
def XY(line : int, memory_address_a : int,  memory_address_b : int) -> str:
	"""Writes the `XY` instruction.
	Compare the values of the 2 supplied memory addresses for equality. 
	If equal execute the next instruciton else execute the one after that.

	Args:
		line (int): The line number of the current instruction
		memory_address_a (int): The first memory address used to compare with
		memory_address_b (int): the second memory address to compare with

	Returns:
		str: A string containing a label to the instruction and the instruction itself.
	"""
	line_label 			= "\nl_"+str(line)+":"
	load_address_a 		= getAddress(memory_address_a, "R0")
	load_address_b		= getAddress(memory_address_b, "R1")
	load_value_a		= "\nLDR R0, [R0]"
	load_value_b		= "\nLDR R1, [R1]"	
	compare				= "\nCMP R0, R1"
	equal				= "\nBEQ l_"+str(line+1)
	not_equal			= "\nBNE l_"+str(line+2)
	return line_label + load_address_a + load_address_b + load_value_a + load_value_b + compare + equal + not_equal
	
def AY(line : int, memory_address_a : int,  memory_address_b : int) -> str:
	"""Writes the `AY` instruction.
	Compare the values of the 2 supplied memory addresses to see if a is greater than b.
	If a is greater than b execute the next instruction else execute the one after that.
	
	Args:
		line (int): The line number of the current instruction
		memory_address_a (int): The first memory address used to compare with
		memory_address_b (int): The second memory address to compare with

	Returns:
		str: A string containing a label to the instruction and the instruction itself.
	"""
	line_label 			= "\nl_"+str(line)+":"
	load_address_a		= getAddress(memory_address_a, "R0")
	load_address_b		= getAddress(memory_address_b, "R1")
	load_value_a		= "\nLDR R0, [R0]"
	load_value_b		= "\nLDR R1, [R1]"
	compare				= "\nCMP R0, R1"
	greather_than		= "\nBGT l_"+str(line+1)
	less_than_equal		= "\nBLE l_"+str(line+2)
	return line_label + load_address_a + load_address_b + load_value_a + load_value_b + compare + greather_than + less_than_equal
	
def BY(line : int, memory_address_a : int,  memory_address_b : int) -> str:
	"""Writes the `BY` instruction.
	Compare the values of the 2 supplied memory addresses to see if a is less than b.
	If a is less than b execute the next instruction else execute the one after that.

	Args:
		line (int): The line number of the current instruction
		memory_address_a (int): The first memory address used to compare with
		memory_address_b (int): The second memory address to compare with

	Returns:
		str: A string containing a label to the instruction and the instruction itself.
	"""
	line_label 			= "\nl_"+str(line)+":"
	load_address_a		= getAddress(memory_address_a, "R0")
	load_address_b		= getAddress(memory_address_b, "R1")
	load_value_a		= "\nLDR R0, [R0]"
	load_value_b		= "\nLDR R1, [R1]"
	compare				= "\nCMP R0, R1"
	less_than			= "\nBGT l_"+str(line+1)
	greater_than_equal 	= "\nBLE l_"+str(line+2)
	return line_label + load_address_a + load_address_b + load_value_a + load_value_b + compare + less_than + greater_than_equal
	
def YA(line : int, memory_address_a : int,  memory_address_b : int) -> str:
	"""Writes the `YA` instruction.
	Multiply the value of memory address a with the value of memory address b and store it in memory address a.

	Args:
		line (int): The line number of the current instruction
		memory_address_a (int): The memory address of the value to multiply and store the result in
		memory_address_b (int): The memory address of the value to multiply the value of memory addres a with

	Returns:
		str: A string containing a label to the instruction and the instruction itself.
	"""
	line_label 			= "\nl_"+str(line)+":"
	load_address_a		= getAddress(memory_address_a, "R0")
	load_address_b		= getAddress(memory_address_b, "R1")
	load_value_a		= "\nLDR R2, [R0]"
	load_value_b		= "\nLDR R1, [R1]"
	calculate_result 	= "\nMUL R2, R1"
	save_result 		= "\nSTR R2, [R0]"
	return line_label + load_address_a + load_address_b + load_value_a + load_value_b + calculate_result + save_result
	
def YB(line : int, memory_address_a : int,  memory_address_b : int) -> str:
	"""Writes the `YB` instruction.
	Adds the value of memory address b to the value stored in memory address a.

	Args:
		line (int): The line number of the current instruction
		memory_address_a (int): The memory address of the value to store the result in
		memory_address_b (int): The memory address of the value to add to the value of memory address a

	Returns:
		str: A string containing a label to the instruction and the instruction itself.
	"""
	line_label 			= "\nl_"+str(line)+":"
	load_address_a 		= getAddress(memory_address_a, "R0")
	load_address_b		= getAddress(memory_address_b, "R1")
	load_value_a		= "\nLDR R2, [R0]"
	load_value_b		= "\nLDR R1, [R1]"
	calculate_result	= "\nADD R2, R1"
	save_result 		= "\nSTR R2, [R0]"
	return line_label + load_address_a + load_address_b + load_value_a + load_value_b + calculate_result + save_result
	
def YX(line : int, memory_address_a : int,  memory_address_b : int) -> str:
	"""Writes the `YX` instruction.
	Subtracts the value of memory address b from the value stored in memory address a.

	Args:
		line (int): The line number of the current instruction
		memory_address_a (int): The memory address of the value to store the result in
		memory_address_b (int): The memory address of the value to subtract from the value of memory address a

	Returns:
		str: A string containing a label to the instruction and the instruction itself.
	"""
	line_label 			= "\nl_"+str(line)+":"
	load_address_a 		= getAddress(memory_address_a, "R0")
	load_address_b		= getAddress(memory_address_b, "R1")
	load_value_a		= "\nLDR R2, [R0]"
	load_value_b		= "\nLDR R1, [R1]"
	calculate_result	= "\nSUB R2, R1"
	save_result 		= "\nSTR R2, [R0]"
	return line_label + load_address_a + load_address_b + load_value_a + load_value_b + calculate_result + save_result
	
def BX(line : int) -> str:
	"""Writes the `BX` instruction.
	Ends the code , each file should contain this instruction.
	Places whatever the memory pointer is pointing to in R0 so it can be used as a return value. 
	Sets the Stack Pointer to it's original state en pops the registers R4 -R7 and PC. 

	Args:
		line (int): The line number of the current instruction

	Returns:
		str: A string containing a label to the instruction and the instruction itself.
	"""
	line_label 			= "\nl_"+str(line)+":"
	load_return_value 	= "\nLDR R0, [R4]"
	load_stack_pointer 	= "\nMOV SP, R5"
	load_registers		= "\nPOP {R4,R5,R6,R7,PC}"
	return line_label + load_return_value + load_stack_pointer + load_registers

class Compiler:
	"""The Compiler class is used to compile Controller Code to assembly.
	"""
	def __init__(self, parsed_tokens : List[List[Union[str,int]]], asm_file : str, memory_size : int):
		"""The init function will ask the user to supply parsed Controller Code tokens, the name of the file to export to and the size of the memory.
		This function will also create the coco_lines list which will contain just the first instruction of each line. It is used to find the index of certain instructions.

		Args:
			parsed_tokens (List[List[Union[str,int]]]): A List of parsed Controller Code tokens
			asm_file (str): The name of the file to which a string can be exported
			memory_size (int): The size of the memory stack to be used.
		"""
		self.tokens = parsed_tokens
		self.coco_lines = list(map(lambda line : line[0], parsed_tokens)) #map 5/3
		self.file = asm_file
		self.memory_size = memory_size

	def compile(self) -> str:
		"""Call this function to start the compile process.
		It will start by first setting some "options" and make the filename -.asm available as a global.
		Next it will find all the `BA` instructions and put their code behind the "options"
		After that it will write the rest of the code, the "body".

		Returns:
			str: A string containing all the supplied parsed tokens in assembly.
		"""
		code_label = self.file.split('.')[0]
		asm_code 	= self.__initialize_file(code_label)
		asm_code   += self.__create_functions(cp(self.tokens), cp(self.coco_lines))
		asm_code   += self.__initialize_code(code_label, self.memory_size)
		asm_code   += self.__create_body(cp(self.tokens), cp(self.coco_lines))
		return asm_code

	def __create_functions(self, tokens : List[List[Union[str,int]]], instruction_list : List[str], index_end = 0) -> str:
		"""This function will try to find all the `BA` instructions and corresponding `AB` instructions and create functions with all the code between them.

		Args:
			tokens (List[List[Union[str,int]]]): The list of parsed Controller Code tokens
			instruction_list (List[str]): The instruction list, this is used to find the line numbers that correspond to the `BA` and `AB` instructions.
			index_end (int, optional): This integer is used to define from where the function should start to look for `BA` instructions. Defaults to 0.

		Returns:
			str: A string containing all the `BA` and corresponding `AB` instructions and all their code
		"""
		try:
			start = instruction_list.index("BA", index_end)
			end = instruction_list.index("AB",index_end+1)
			cur_function = self.__create_lines(cp(tokens),start,end+1)
		except:
			return "\n"
		return cur_function + self.__create_functions(cp(tokens),cp(instruction_list), end)
		
	def __create_body(self, tokens : List[List[Union[str,int]]], instruction_list : List[str], index_start = 0) -> str:
		"""This function will try to find all the instruction outside of functions, aka the "body".

		Args:
			tokens (List[List[Union[str,int]]]): The list of parsed Controller Code tokens
			instruction_list (List[str]): The instruction list, this is used to find the line number that correspond to the `BA` and `AB` instructions se we can ignore those.
			index_start (int, optional): This integer is used to define from where the function should start looking for `BA` instructions. Defaults to 0.

		Returns:
			str: A string containing all the code outside of `BA` instructions and all of their code.
		"""
		try:
			end = instruction_list.index("BA", index_start)
			start = instruction_list.index("AB", index_start+1) 
			cur_body = self.__create_lines(cp(tokens), index_start, end)
		except:
			return self.__create_lines(cp(tokens), index_start, len(instruction_list))
		return cur_body + self.__create_body(cp(tokens), cp(instruction_list), start+1)

	def __create_lines(self, tokens : List[List[Union[str,int]]], start : int, end : int) -> str:
		"""This function creates the actual assembly code for a line using the compilerDict.

		Args:
			tokens (List[List[Union[str,int]]]): The list of parsed Controller Code tokens
			start (int): The start of a block of lines of which we want to create assembly code
			end (int): Then end of a block of lines of which we want to create assembly code

		Returns:
			str: A string containing all the code of the supplied block of code
		"""
		if start < end:
			return compilerDict.get(tokens[start][:1][0])(start+1, *cp(tokens[start][1:])) + self.__create_lines(cp(tokens), start+1, end)
		return ""

	def __initialize_file(self, code_label : str) -> str:
		"""This function is used to create the basic "options" for the assembly code.

		Args:
			code_label (str): The name that will be made global and can be used in for example C++ code.

		Returns:
			str: A string containing all the "options"
		"""
		section 	= "\n.section .text"
		align 		= "\n.align 4"
		external 	= "\n.global "+code_label
		return section + align + external + "\n"

	def __initialize_code(self, code_label : str, memory_size : int) -> str:
		"""This function is used to start the Controller Code and secure all the Registers so that when we return the C++ code can continue where it left off.

		Args:
			code_label (str): The name that will be made global and can be used in C++ code
			memory_size (int): The size of the memory stack that we want to use.

		Returns:
			str: A string containing the start of a files Controller Code.
		"""
		start_label 			= "\n"+code_label+":"
		save_registers 			= "\nPUSH {R4,R5,R6,R7,LR}"
		create_memory_pointer 	= "\nMOV R4, SP"
		save_stack_pointer 		= "\nMOV R5, SP"
		protect_address_zero 	= "\nSUB R4, #4"
		allocate_memory_size 	= "\nSUB SP, #"+str(memory_size * 4)
		#save_program_counter = "\nMOV R6, PC"
		return start_label+save_registers+create_memory_pointer+save_stack_pointer+protect_address_zero+allocate_memory_size

	def export(self, compiled_code : str):
		"""This function is used to export the supplied string to the file name that was supplied during creation of the Compiler Object.

		Args:
			compiled_code (str): The string that will be written to the file
		"""
		with open(self.file, "w") as file:
			file.write(compiled_code)
		return 