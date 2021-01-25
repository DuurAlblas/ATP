from support import *

from typing import List, Union

class Interpreter:
	"""The Interpreter class executes the instructions in the parsed tokens list. 
	It is possible to change the size of the memory "stack" but since I've specified 128 in the READM.me it defaults to 128.
	"""
	def __init__(self, parsed_tokens : List[List[Union[str,int]]], memory_size = 128):
		self.tokens = parsed_tokens
		self.memory_size = memory_size
		
	def interpret(self):
		"""This function can be called to start the execution process.
		It first creates a simulated memory stack to use and then created the platform "on" which we will execute all the code.
		Note that the platforms memory pointer is initialized on 1 since 0 is reserved for the linker pointer.
		WARNING: This function is not supposed to ever end. The code has been check and should contain a `BX` instruction which will immediatly close the application.
		"""
		simulated_memory = [0] * self.memory_size
		platform = Platform(self.tokens, simulated_memory, 0, 1)
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