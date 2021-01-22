from typing import TypeVar, List, Union
from support import cp, cError, throw_errors, syntaxParametersDict

class Lexer:
	"""The Lexer class tokenizes a string with raw Controller Code.
	"""
	def __init__(self, raw_code : str):
		self.source_code = raw_code
	
	def tokenize(self) -> List[Union[str,int]]:
		lexed_string_list = self.__create_list(list(map(lambda line: line.split(), cp(self.source_code))))
		lexed_list = list(map(lambda value: int(value) if value.lstrip("-").isnumeric() else value, lexed_string_list))
		errors = self.__check_syntax(cp(lexed_list))
		errors += self.__check_start_instructions(cp(lexed_list))
		if errors:
			throw_errors(cp(errors))
		return lexed_list
				
	def __create_list(self, code : List[str]) -> List[str]:
		if code:
			head, *tail = code		
			return head + self.__create_list(tail)
		return []
		
	def __check_syntax(self, code : List[Union[str,int]]) -> List[Union[cError]]:
		"""This function checks the whole code for syntax errors.
		If it has found any it will put them in a list.
		The list can be used to itterate over, print every error except the last and then throw the last error which will exit the application.
		Args:
			code (List[Union[str,int]]): [description]

		Returns:
			List[Union[cError]]: [description]
		"""
		if code:
			expected_parameters = syntaxParametersDict.get(code[0])
			if expected_parameters == 0:
				head, *tail = code
				return [] + self.__check_syntax(tail)
			elif expected_parameters == 1:
				if code[0] == "BA":
					try:
						_ = code.index("AB")
					except ValueError:
						return [cError("Syntax Error: Missing a `AB` instruction to end `BA` instruction.")] + self.__check_syntax(cp(code[2:]))
					try:
						if code.index("BA", code.index("BA")+1, code.index("AB")):
							return [cError("Syntax Error: BA has a nested BA this is not allowed.")] + self.__check_syntax(cp(code[2:]))
					except:
						# If .index() cannot find a nested BA that's a good thing so we just pass this exception.
						pass
				elif code[0] in ["SELECT","XA","XB"]:
					try:
						if code[1] < 1:
							return [cError(("Syntax Error: "+ str(code[0])+" parameter cannot be 0 or less."))] + self.__check_syntax(cp(code[2:]))
					except TypeError:
						return [cError(("Syntax Error: "+ str(code[0]+" parameter has to be numeric.")))] + self.__check_syntax(cp(code[2:]))
			elif expected_parameters == 2:
				if code[0] in ["XY","AY","BY","YB","YX"]:
					try:
						if code[1] < 1 or code[2] < 1:	
							return [cError(("Syntax Error: "+ str(code[0]) +" parameters cannot be 0 or less."))] + self.__check_syntax(cp(code[3:]))
					except TypeError:
						return [cError(("Syntax Error: "+str(code[0])+" parameters have to be numeric."))]+ self.__check_syntax(cp(code[3:]))
			elif expected_parameters == 3:
				try:
					if code[1] < 1 or code[2] < 1 or code[3] < 1:
						return [cError(("Syntax Error: "+str(code[0])+" parameters cannot be 0 or less. "))]+ self.__check_syntax(cp(code[4:]))
				except TypeError:
					return [cError(("Syntax Error: "+str(code[0])+" parameters have to be numeric."))]+ self.__check_syntax(cp(code[4:]))
			elif expected_parameters == None:
				head, *tail = code
				return [cError(("Syntax Error: The instruction `"+ str(head) + "` is not supported."))] + self.__check_syntax(tail)
			
			if all(map(lambda parameter: isinstance(parameter,int), code[1:expected_parameters+1])):
				return [] + self.__check_syntax(cp(code[1+expected_parameters:]))
			else:
				return [cError(("Syntax Error: "+ str(code[0]) +" parameters must be numeric."))] + self.__check_syntax(cp(code[1+expected_parameters:]))		
		return []

	def __check_start_instructions(self, tokens : List[Union[str,int]]) -> List[Union[cError]]:
		start_identifiers = self.__find_instruction_single_parameter(cp(tokens), "START")
		ba_identifiers = self.__find_instruction_single_parameter(cp(tokens), "BA")
		
		unknown_identifiers = list(set(start_identifiers)-set(ba_identifiers))

		if unknown_identifiers:
			return self.__create_identifier_errors(unknown_identifiers)		
		return []
		
	def __find_instruction_single_parameter(self, tokens: List[Union[str,int]], instruction : str):
		if tokens:
			try:
				parameter_index = tokens.index(instruction)+1
				return [tokens[parameter_index]] + self.__find_instruction_single_parameter(cp(tokens[parameter_index:]), instruction)
			except:
				return []				
		return []
		
	def __create_identifier_errors(self, indentifiers : List[int]) -> List[Union[cError]]:
		if indentifiers:
			head, *tail = indentifiers
			return [cError(("Syntax Error: START instruction with identifier `"+str(head)+"` is invalid since there is no BA with identifier `"+str(head)+"`."))] + self.__create_errors(tail)
		return []