from support import *

from typing import List, Union

class Interpreter:
	def __init__(self, parsed_tokens : List[List[Union[str,int]]], memory_size = 128):
		self.tokens = parsed_tokens
		self.memory_size = memory_size
		
	def interpret(self):
		simulated_memory = [0] * self.memory_size
		platform = Platform(self.tokens, simulated_memory, 0, 1)
		self.__execute(platform)
		
	def __execute(self, platform : Platform):
		current_instruction = interpreterDict.get(platform.instructions[platform.instruction_pointer][0])
		parameterCount =  syntaxParametersDict.get(platform.instructions[platform.instruction_pointer][0])
		if parameterCount:
			platform = current_instruction(platform, *platform.instructions[platform.instruction_pointer][1:parameterCount+1])
		else:
			platform = current_instruction(platform)
		self.__execute(cp(platform))