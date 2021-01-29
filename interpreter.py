from support import cp, syntaxParametersDict

from typing import List, Union

#This dictionary is used to call functions that belong to instructions.
interpreterDict = {
	"RIGHT" : lambda platform : RIGHT(platform),
	"LEFT" : lambda platform : LEFT(platform),
	"UP" : lambda platform : UP(platform),
	"DOWN" : lambda platform : DOWN(platform),
	"BA" : lambda platform, _ : BA(platform, _),
	"AB" : lambda platform : AB(platform),
	"START" : lambda platform , identifier : START(platform, identifier),
	"SELECT" : lambda platform, line : SELECT(platform, line),
	"ZL" : lambda platform, argument, memory_address : ZL(platform, argument, memory_address),
	"LB" : lambda platform, address : LB(platform, address),
	"RB" : lambda platform : RB(platform),
	"AX" : lambda platform, value : AX(platform, value),
	"XA" : lambda platform, memory_address : XA(platform, memory_address),
	"XB" : lambda platform, memory_address : XB(platform, memory_address),
	"XY" : lambda platform, memory_address_a, memory_address_b : XY(platform, memory_address_a, memory_address_b),
	"AY" : lambda platform, memory_address_a, memory_address_b : AY(platform, memory_address_a, memory_address_b),
	"BY" : lambda platform, memory_address_a, memory_address_b : BY(platform, memory_address_a, memory_address_b),
	"YA" : lambda platform, memory_address_a, memory_address_b : YA(platform, memory_address_a, memory_address_b),
	"YB" : lambda platform, memory_address_a, memory_address_b : YB(platform, memory_address_a, memory_address_b),
	"YX" : lambda platform, memory_address_a, memory_address_b : YX(platform, memory_address_a, memory_address_b),
	"BX" : lambda platform : BX(platform)
}
		
class Platform:
	"""This class is used to simulate a platform on which can be coded.
	It has its own memory, instruction list and pointers to both.
	It also has many "quality of life" functions.
	"""
	def __init__(self, instructions : List[List[Union[str,int]]], memory : List[int], instruction_pointer : int, memory_pointer : int, input_list : List[int]):
		self.instructions = instructions
		self.memory = memory
		self.instruction_pointer = instruction_pointer
		self.memory_pointer = memory_pointer
		self.input = input_list
		self.function_call_stack = []

	def __str__(self):
		return "Platform({instructions},\n{memory},\n{instruction_pointer},\n{memory_pointer},\n{input},\n{call_stack})".format(
			instructions = self.instructions,
			memory = self.memory,
			instruction_pointer = self.instruction_pointer,
			memory_pointer = self.memory_pointer,
			input = self.input,
			call_stack = self.function_call_stack
		)

	def next_instruction(self, step = 1):
		"""This function is used to go to the next instruction. 
		If no parameters are given the instruction pointer gets increased by one.
		By supplying a integer you can make a bigger step.

		Args:
			step (int, optional): The amount of steps the instruction pointer wil be increased by. Defaults to 1.
		"""
		self.instruction_pointer += step
		
	def previous_instruction(self):
		"""This function is used to go to the previous instruction by decreasing the instruction pointer by 1.
		"""
		self.instruction_pointer -= 1

	def set_instruction_pointer(self, instruction : int):
		"""Using this function you can set the instruction pointer to a exact value.
		By doing this you can quickly jump through the code.

		Args:
			instruction (int): The line number of the instruction to jump to.
		"""
		self.instruction_pointer = instruction

	def next_address(self):
		"""This function is used to go to the next memory address by increasing the memory pointer by 1.
		"""
		self.memory_pointer += 1
	
	def previous_address(self):
		"""This function is used to go to the previous memory address by decreasing the memory pointer by 1.
		"""
		self.memory_pointer -= 1

	def set_address(self, address : int):
		"""This function can be used to quickly jump to a memory address by changing to memory pointer to the supplied address.

		Args:
			address (int): The address of the memory you want to access.
		"""
		self.memory_pointer = address

	def set_linker(self, instruction : int):
		"""This function will set the linker register value at then end of the function_call_stack.

		Args:
			instruction (int): The line number of the instruction you want to store in the linker address.
		"""
		self.function_call_stack.append(instruction)

	def get_linker(self) -> int:
		"""This function will return the most recently added value from the function_call_stack.

		Returns:
			(int): The last value that was added to the function_call_stack.
		"""
		return self.function_call_stack.pop()

	def increase_byte(self):
		"""This function wil increase the byte the memory pointer is pointing to by 1.
		"""
		self.memory[self.memory_pointer] += 1
		
	def decrease_byte(self):
		"""This function wil decrease the byte the memory pointer is pointing to by 1.
		"""
		self.memory[self.memory_pointer] -= 1

class Interpreter:
	"""The Interpreter class executes the instructions in the parsed tokens list. 
	It is possible to change the size of the memory "stack" but since I've specified 128 in the READM.me it defaults to 128.
	"""
	def __init__(self, parsed_tokens : List[List[Union[str,int]]], memory_size = 128):
		self.tokens = parsed_tokens
		self.memory_size = memory_size
		
	def interpret(self, input_list : List[int] = []):
		"""This function can be called to start the execution process.
		It first creates a simulated memory stack to use and then created the platform "on" which we will execute all the code.
		Note that the platforms memory pointer is initialized on 1 since 0 is reserved for the linker pointer.
		WARNING: This function is not supposed to ever end. The code has been check and should contain a `BX` instruction which will immediatly close the application.
		"""
		simulated_memory = [0] * self.memory_size
		platform = Platform(self.tokens, simulated_memory, 0, 1, input_list)
		self.__execute(platform)
		
	def __execute(self, platform : Platform):
		"""Here the actual code is being executed by constantly find the current instruction in a dictionary that contains the instruction name as a key and the actual functionality as value.
		Next we find how many parameters the instruction has and then call the current instruction.
		WARNING: This function is not supposed to ever end. The code has been check and should contain a `BX` instruction which will immediatly close the application.

		Args:
			platform (Platform): [description]
		"""
		current_instruction = interpreterDict.get(platform.instructions[platform.instruction_pointer][0])
		parameterCount =  syntaxParametersDict.get(platform.instructions[platform.instruction_pointer][0])
		if parameterCount:
			platform = current_instruction(platform, *platform.instructions[platform.instruction_pointer][1:parameterCount+1])
		else:
			platform = current_instruction(platform)
		self.__execute(cp(platform))
		

def RIGHT(platform : Platform)-> Platform:
	"""Executes the `RIGHT` instruction.
	Go to the next address and the next instruction.

	Args:
		platform (Platform): The state of the platform.

	Returns:
		Platform: A deepcopy of the state of the platform after this instruction.
	"""
	platform.next_address()
	platform.next_instruction()
	return cp(platform)

def LEFT(platform : Platform)-> Platform:
	"""Executes the `LEFT` instruction.
	Go to the previous address and the next instruction.

	Args:
		platform (Platform): The state of the platform.

	Returns:
		Platform: A deepcopy of the state of the platform after this instruction.
	"""
	platform.previous_address()
	platform.next_instruction()
	return cp(platform)

def UP(platform : Platform) -> Platform:
	"""Executes the `UP` instruction.
	Increase the byte of the memory address where the memory pointer is pointing and go to the next instruction.

	Args:
		platform (Platform): The state of the platform.

	Returns:
		Platform: A deepcopy of the state of the platform after this instruction.
	"""
	platform.increase_byte()
	platform.next_instruction()
	return cp(platform)

def DOWN(platform : Platform) -> Platform:
	"""Executes the `DOWN` instruction.
	Decrease the byte of the memory address where the memory pointer is pointing and go to the next instruction.

	Args:
		platform (Platform): The state of the platform.

	Returns:
		Platform: A deepcopy of the state of the platform after this instruction.
	"""
	platform.decrease_byte()
	platform.next_instruction()
	return cp(platform)

def BA(platform : Platform, _ : int) -> Platform:
	"""Executes the `BA` instruction.
	Set the instruction pointer to the instruction after the `AB` instruction that belongs to this "function".

	Args:
		platform (Platform): The state of the platform.
		_ (int): The identifier of the `BA` instruction. Nothing is being done with it.

	Returns:
		Platform: A deepcopy of the state of the platform after this instruction.
	"""
	platform.set_instruction_pointer(platform.instructions.index(["AB"], platform.instruction_pointer)+1)
	return cp(platform)

def AB(platform : Platform) -> Platform:
	"""Executes the `AB` instruction.
	Set the instruction pointer to the instruction that is stored in the linker memory address 0.

	Args:
		platform (Platform): The state of the platform.

	Returns:
		Platform: A deepcopy of the state of the platform after this instruction.
	"""
	platform.set_instruction_pointer(platform.get_linker())
	return cp(platform)
	
def START(platform : Platform, identifier : int) -> Platform:
	"""Executes the `START` instruction.
	Set the linker value to the instruction after the current instruction.
	Then set the instruction pointer to the instruction after the matching `BA` instrcution.

	Args:
		platform (Platform): The state of the platform.
		identifier (int): The identifier of the `BA` instruction to call.

	Returns:
		Platform: A deepcopy of the state of the platform after this instruction.
	"""
	platform.set_linker(platform.instruction_pointer+1)
	platform.set_instruction_pointer(platform.instructions.index(["BA",identifier])+1)
	return cp(platform)
	
def SELECT(platform : Platform, line : int) -> Platform:
	"""Executes the `SELECT` instruction.
	Set the instruction pointer to the instruction on the supplied line number (+1 because 0 based list).

	Args:
		platform (Platform): The state of the platform.
		line (int): The line of the instruction to be executed next.

	Returns:
		Platform: A deepcopy of the state of the platform after this instruction.
	"""
	platform.set_instruction_pointer(line -1) # WARNING: For the offset -1
	return cp(platform)
	
def ZL(platform : Platform, argument : int, memory_address : int) -> Platform:
	"""Executes the `ZL` instruction.
	Store the supplied input argument in the supplied memory address.
	WARNING! The argument parameter only accepts 1 and 2, anything else will produce undefined behavior.

	Args:
		platform (Platform): The state of the platform.
		argument (int): The input argument you want to store.
		memory_address (int): The memory address in which you want to store the input argument.

	Returns:
		Platform: A deepcopy of the state of the platform after this instruction.
	"""
	platform.memory[memory_address] = platform.input[argument-1]
	platform.next_instruction()
	return cp(platform)
	
def LB(platform : Platform, address : int) -> Platform:
	"""Executes the `LB` instruction.
	Set the memory address to the supplied address.
	Then move on to the next instruction.

	Args:
		platform (Platform): The state of the platform.
		address (int): The memory address to jump to.

	Returns:
		Platform: A deepcopy of the state of the platform after this instruction.
	"""
	platform.set_address(address)
	platform.next_instruction()
	return cp(platform)
	
def RB(platform : Platform) -> Platform:
	"""Executes the `RB` instruction.
	Print the value that is stored in the memory address the memory pointer is pointing to.
	Then move on to the next instruction.

	Args:
		platform (Platform): The state of the platform.

	Returns:
		Platform: A deepcopy of the state of the platform after this instruction.
	"""
	print(platform.memory[platform.memory_pointer])
	platform.next_instruction()
	return cp(platform)
	
def AX(platform : Platform, value : int) -> Platform:
	"""Executes the `AX` instruction.
	Set the value of the memory address the memory pointer is pointing to to the supplied value.
	Then move on to the next instruction.

	Args:
		platform (Platform): The state of the platform.

	Returns:
		Platform: A deepcopy of the state of the platform after this instruction.
	"""
	platform.memory[platform.memory_pointer] = value
	platform.next_instruction()
	return cp(platform)
	
def XA(platform : Platform, memory_address : int) -> Platform:
	"""Executes the `XA` instruction.
	Copy the value of the supplied memory address to the memory address the memory pointer is pointing to.
	Then move on to the next instruction.

	Args:
		platform (Platform): The state of the platform.

	Returns:
		Platform: A deepcopy of the state of the platform after this instruction.
	"""
	platform.memory[platform.memory_pointer] = platform.memory[memory_address]
	platform.next_instruction()
	return cp(platform)
	
def XB(platform : Platform, memory_address : int) -> Platform:
	"""Executes the `XB` instruction.
	Copy the value of the memory address the memory pointer is pointing to the supplied memory address.
	Then move on to the next instruction.

	Args:
		platform (Platform): The state of the platform.

	Returns:
		Platform: A deepcopy of the state of the platform after this instruction.
	"""
	platform.memory[memory_address] = platform.memory[platform.memory_pointer]
	platform.next_instruction()
	return cp(platform)
	
def XY(platform : Platform, memory_address_a : int, memory_address_b : int) -> Platform:
	"""Executes the `XY` instruction.
	Check if the values in memory address a and b are equal. If they are move to the next instruction.
	Otherwise move to the instruction after the next instruction.

	Args:
		platform (Platform): The state of the platform.
		memory_address_a (int): The first memory address to compare with.
		memory_address_b (int): The second memory address to compare with.

	Returns:
		Platform: A deepcopy of the state of the platform after this instruction.
	"""
	if platform.memory[memory_address_a] == platform.memory[memory_address_b]:
		platform.next_instruction()
	else:
		platform.next_instruction(2)
	return cp(platform)
	
def AY(platform : Platform, memory_address_a : int, memory_address_b : int) -> Platform:
	"""Executes the `AY` instruction.
	Check if the value in memory address a is larger than the value in memory address b. If they are move to the next instruction.
	Otherwise move to the instruction after the next instruction.

	Args:
		platform (Platform): The state of the platform.
		memory_address_a (int): The first memory address to compare with.
		memory_address_b (int): The second memory address to compare with.

	Returns:
		Platform: A deepcopy of the state of the platform after this instruction.
	"""
	if platform.memory[memory_address_a] > platform.memory[memory_address_b]:
		platform.next_instruction()
	else:
		platform.next_instruction(2)
	return cp(platform)
	
def BY(platform : Platform, memory_address_a : int, memory_address_b : int) -> Platform:
	"""Executes the `AY` instruction.
	Check if the value in memory address a is smaller than the value in memory address b. If they are move to the next instruction.
	Otherwise move to the instruction after the next instruction.

	Args:
		platform (Platform): The state of the platform.
		memory_address_a (int): The first memory address to compare with.
		memory_address_b (int): The second memory address to compare with.

	Returns:
		Platform: A deepcopy of the state of the platform after this instruction.
	"""
	if platform.memory[memory_address_a] < platform.memory[memory_address_b]:
		platform.next_instruction()
	else:
		platform.next_instruction(2)
	return cp(platform)

def YA(platform : Platform, memory_address_a : int, memory_address_b : int) -> Platform:
	"""Executes the `YA` instruction.
	Store the result of multiplying the value of memory address b with the value of memory address c in memory address a.
	Then move on to the next instruction.

	Args:
		platform (Platform): The state of the platform.
		memory_address_a (int): The memory address in which the result will be stored.
		memory_address_b (int): The memory address of the value which will be multiplied.
		memory_address_c (int): The memory address of the value with which memory address b wil be multiplied.

	Returns:
		Platform: A deepcopy of the state of the platform after this instruction.
	"""
	platform.memory[memory_address_a] *= platform.memory[memory_address_b]
	platform.next_instruction()
	return cp(platform)
	
def YB(platform : Platform, memory_address_a : int, memory_address_b : int) -> Platform:
	"""Executes the `YB` instruction.
	Store the result of adding the value of memory address b to the value of memory address a in memory address a.
	Then move on to the next instruction.

	Args:
		platform (Platform): The state of the platform.
		memory_address_a (int): The memory address in which the result will be stored.
		memory_address_b (int): The memory address of the value which will be added to the value of memory address a.

	Returns:
		Platform: A deepcopy of the state of the platform after this instruction.
	"""
	platform.memory[memory_address_a] += platform.memory[memory_address_b]
	platform.next_instruction()
	return cp(platform)
	
def YX(platform : Platform, memory_address_a : int, memory_address_b : int) -> Platform:
	"""Executes the `YX` instruction.
	Store the result of subtracting the value of memory address b from the value of memory address a in memory address a.
	Then move on to the next instruction.

	Args:
		platform (Platform): The state of the platform.
		memory_address_a (int): The memory address in which the result will be stored.
		memory_address_b (int): The memory address of the value which will be subtracted from the value of memory address a.

	Returns:
		Platform: A deepcopy of the state of the platform after this instruction.
	"""
	platform.memory[memory_address_a] -= platform.memory[memory_address_b]
	platform.next_instruction()
	return cp(platform)
	
def BX(_ : Platform):
	"""Executes the `BX` instruction.
	Exit the application it's the end of the Controller Code.

	Args:
		_ (Platform): The state of the platform.
	"""
	exit()