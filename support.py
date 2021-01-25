from typing import List, Union

from copy import deepcopy

def printb(data, symbol = "=", times = 40):
	print(times * symbol)
	print(data)
	print(times * symbol)
	
def cp(data):
	return deepcopy(data)
	
class cError:
	def __init__(self, error_string : str):
		self.text = error_string
	
	def __str__(self):
		return 'Error({text})'.format(
			text = self.text
		)
		
	def throw(self):
		print(self)
		exit()
		
def throw_errors(errors : List[cError]):
	if errors:
		head, *tail = errors
		if tail:
			print(head)
			throw_errors(tail)
		else:
			head.throw()
	else:
		print("Warning : There were no errors to throw!")

syntaxParametersDict = {
	"RIGHT":0,
	"LEFT":0,
	"UP":0,
	"DOWN":0,
	"BA":1,
	"AB":0,
	"START":1,
	"SELECT":1,
	"LB":1,
	"RB":0,
	"AX":1,
	"XA":1,
	"XB":1,
	"XY":2,
	"AY":2,
	"BY":2,
	"YA":3,
	"YB":2,
	"YX":2,
	"BX":0
}

interpreterDict = {
	"RIGHT" : lambda platform : RIGHT(platform),
	"LEFT" : lambda platform : LEFT(platform),
	"UP" : lambda platform : UP(platform),
	"DOWN" : lambda platform : DOWN(platform),
	"BA" : lambda platform, _ : BA(platform, _),
	"AB" : lambda platform : AB(platform),
	"START" : lambda platform , identifier : START(platform, identifier),
	"SELECT" : lambda platform, line : SELECT(platform, line),
	"LB" : lambda platform, address : LB(platform, address),
	"RB" : lambda platform : RB(platform),
	"AX" : lambda platform, value : AX(platform, value),
	"XA" : lambda platform, memory_address : XA(platform, memory_address),
	"XB" : lambda platform, memory_address : XB(platform, memory_address),
	"XY" : lambda platform, memory_address_a, memory_address_b : XY(platform, memory_address_a, memory_address_b),
	"AY" : lambda platform, memory_address_a, memory_address_b : AY(platform, memory_address_a, memory_address_b),
	"BY" : lambda platform, memory_address_a, memory_address_b : BY(platform, memory_address_a, memory_address_b),
	"YA" : lambda platform, memory_address_a, memory_address_b, memory_address_c : YA(platform, memory_address_a, memory_address_b, memory_address_c),
	"YB" : lambda platform, memory_address_a, memory_address_b : YB(platform, memory_address_a, memory_address_b),
	"YX" : lambda platform, memory_address_a, memory_address_b : YX(platform, memory_address_a, memory_address_b),
	"BX" : lambda platform : BX(platform)
}
		
class Platform:
	def __init__(self, instructions : List[List[Union[str,int]]], memory : List[int], instruction_pointer : int, memory_pointer : int):
		self.instructions = instructions
		self.memory = memory
		self.instruction_pointer = instruction_pointer
		self.memory_pointer = memory_pointer

	def __str__(self):
		return "Platform({instructions},\n{memory},\n{instruction_pointer},\n{memory_pointer})".format(
			instructions = self.instructions,
			memory = self.memory,
			instruction_pointer = self.instruction_pointer,
			memory_pointer = self.memory_pointer
		)

	def next_instruction(self, step = 1):
		self.instruction_pointer += step
		
	def previous_instruction(self):
		self.instruction_pointer -= 1

	def set_instruction_pointer(self, instruction : int):
		self.instruction_pointer = instruction

	def next_address(self):
		self.memory_pointer += 1
	
	def previous_address(self):
		self.memory_pointer -= 1

	def set_address(self, address : int):
		self.memory_pointer = address

	def set_linker(self, instruction : int):
		self.memory[0] = instruction

	def increase_byte(self):
		self.memory[self.memory_pointer] += 1
		
	def decrease_byte(self):
		self.memory[self.memory_pointer] -= 1

def RIGHT(platform : Platform)-> Platform:
	platform.next_address()
	platform.next_instruction()
	return cp(platform)

def LEFT(platform : Platform)-> Platform:
	platform.previous_address()
	platform.next_instruction()
	return cp(platform)

def UP(platform : Platform) -> Platform:
	platform.increase_byte()
	platform.next_instruction()
	return cp(platform)

def DOWN(platform : Platform) -> Platform:
	platform.decrease_byte()
	platform.next_instruction()
	return cp(platform)

def BA(platform : Platform, _ : int) -> Platform:
	platform.set_instruction_pointer(platform.instructions.index(["AB"], platform.instruction_pointer)+1)
	return cp(platform)

def AB(platform : Platform) -> Platform:
	platform.set_address(platform.memory[0])
	return cp(platform)
	
def START(platform : Platform, identifier : int) -> Platform:
	platform.set_linker(platform.instruction_pointer+1)
	platform.set_instruction_pointer(platform.instructions.index(["BA",identifier])+1)
	return cp(platform)
	
def SELECT(platform : Platform, line : int) -> Platform:
	platform.set_instruction_pointer(line -1) # WARNING: For the offset -1
	return cp(platform)
	
def LB(platform : Platform, address : int) -> Platform:
	platform.set_address(address)
	platform.next_instruction()
	return cp(platform)
	
def RB(platform : Platform) -> Platform:
	print(platform.memory[platform.memory_pointer])
	platform.next_instruction()
	return cp(platform)
	
def AX(platform : Platform, value : int) -> Platform:
	platform.memory[platform.memory_pointer] = value
	platform.next_instruction()
	return cp(platform)
	
def XA(platform : Platform, memory_address : int) -> Platform:
	platform.memory[platform.memory_pointer] = platform.memory[memory_address]
	platform.next_instruction()
	return cp(platform)
	
def XB(platform : Platform, memory_address : int) -> Platform:
	platform.memory[memory_address] = platform.memory[platform.memory_pointer]
	platform.next_instruction()
	return cp(platform)
	
def XY(platform : Platform, memory_address_a : int, memory_address_b : int) -> Platform:
	if platform.memory[memory_address_a] == platform.memory[memory_address_b]:
		platform.next_instruction()
	else:
		platform.next_instruction(2)
	return cp(platform)
	
def AY(platform : Platform, memory_address_a : int, memory_address_b : int) -> Platform:
	if platform.memory[memory_address_a] > platform.memory[memory_address_b]:
		platform.next_instruction()
	else:
		platform.next_instruction(2)
	return cp(platform)
	
def BY(platform : Platform, memory_address_a : int, memory_address_b : int) -> Platform:
	if platform.memory[memory_address_a] < platform.memory[memory_address_b]:
		platform.next_instruction()
	else:
		platform.next_instruction(2)
	return cp(platform)

def YA(platform : Platform, memory_address_a : int, memory_address_b : int, memory_address_c : int) -> Platform:
	platform.memory[memory_address_a] = platform.memory[memory_address_b] * platform.memory[memory_address_c]
	platform.next_instruction()
	return cp(platform)
	
def YB(platform : Platform, memory_address_a : int, memory_address_b : int) -> Platform:
	platform.memory[memory_address_a] += platform.memory[memory_address_b]
	platform.next_instruction()
	return cp(platform)
	
def YX(platform : Platform, memory_address_a : int, memory_address_b : int) -> Platform:
	platform.memory[memory_address_a] -= platform.memory[memory_address_b]
	platform.next_instruction()
	return cp(platform)
	
def BX(platform : Platform):
	exit()