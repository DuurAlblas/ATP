from typing import TypeVar, List, Union
from support import cp, cError, throw_errors, syntaxParametersDict

class Lexer:
	"""The Lexer class tokenizes a string that contains raw Controller Code.
	"""
	def __init__(self, raw_code : str):
		self.source_code = raw_code
	
	def tokenize(self, input_list : List[int]) -> List[Union[str,int]]:
		"""The tokenize function tokenizes the raw code and return a list of strings, the instructions, and integers when applicable, the paramters.
		After creating the lexed list the function check the syntax and if any errors are found prints them and throws the last error which exits the application.

		Note that the map function is being used here which is a Higher Order Function.

		Returns:
			List[Union[str,int]]: The Lexed list of tokens
		"""
		lexed_string_list = self.__create_list(list(map(lambda line: line.split(), cp(self.source_code)))) #map 1/3
		lexed_list = list(map(lambda value: int(value) if value.lstrip("-").isnumeric() else value, lexed_string_list)) #map 2/3
		errors = self.__check_syntax(cp(lexed_list), cp(input_list))
		errors += self.__check_start_instructions(cp(lexed_list))
		if errors:
			throw_errors(cp(errors))
		return lexed_list
				
	def __create_list(self, code : List[str]) -> List[str]:
		"""This function creates one list out of a list with multiple lists inside it.

		Args:
			code (List[str]): List of lists containing strings.

		Returns:
			List[str]: One (token)list containing all the lists from the supplied list. Instructions and parameters are seperated in this list.
		"""
		if code:
			head, *tail = code		
			return head + self.__create_list(tail)
		return []
		
	def __check_syntax(self, code : List[Union[str,int]], input_list : List[int]) -> List[Union[cError]]:
		"""This function checks the whole code for syntax errors.
		If it has found any it will put them in a list.
		The list can be used to iterate over, print every error except the last one and then throw the last error which will exit the application.
		Args:
			code (List[Union[str,int]]): Lexed list where every instruction and parameter is seperated.
			
		Returns:
			List[Union[cError]]: A list containing either nothing or 1 or more cError objects.
		"""
		if code:
			expected_parameters = syntaxParametersDict.get(code[0])
			if expected_parameters == 0:
				head, *tail = code
				return [] + self.__check_syntax(tail, cp(input_list))
			elif expected_parameters == 1:
				if code[0] == "BA":
					try:
						_ = code.index("AB")
					except ValueError:
						return [cError("Syntax Error: Missing a `AB` instruction to end `BA` instruction.")] + self.__check_syntax(cp(code[2:]), cp(input_list))
					try:
						if code.index("BA", code.index("BA")+1, code.index("AB")):
							return [cError("Syntax Error: BA has a nested BA this is not allowed.")] + self.__check_syntax(cp(code[2:]), cp(input_list))
					except:
						# If .index() cannot find a nested BA that's a good thing so we just pass this exception.
						pass
				elif code[0] in ["SELECT","XA","XB"]:
					try:
						if code[1] < 1:
							return [cError(("Syntax Error: "+ str(code[0])+" parameter cannot be 0 or less."))] + self.__check_syntax(cp(code[2:]), cp(input_list))
					except TypeError:
						return [cError(("Syntax Error: "+ str(code[0]+" parameter has to be numeric.")))] + self.__check_syntax(cp(code[2:]), cp(input_list))
			elif expected_parameters == 2:
				if code[0] == "ZL":
					try:
						if code[1] > len(input_list) or code[1] > 2:
							return [cError(("Syntax Error: "+str(code[0])+ " cannot have more arguments than there are supplied with a maximum of 2."))] + self.__check_syntax(cp(code[3:]), cp(input_list))
						elif code[1] < 1 or code[2] < 1:
							return [cError(("Syntax Error: "+ str(code[0]) +" parameters cannot be 0 or less."))] + self.__check_syntax(cp(code[3:]), cp(input_list))
					except:
						return [cError(("Syntax Error: "+str(code[0])+" parameters have to be numeric."))]+ self.__check_syntax(cp(code[3:]), cp(input_list))
				elif code[0] in ["XY","AY","BY","YB","YX"]:
					try:
						if code[1] < 1 or code[2] < 1:	
							return [cError(("Syntax Error: "+ str(code[0]) +" parameters cannot be 0 or less."))] + self.__check_syntax(cp(code[3:]), cp(input_list))
					except TypeError:
						return [cError(("Syntax Error: "+str(code[0])+" parameters have to be numeric."))]+ self.__check_syntax(cp(code[3:]), cp(input_list))
			elif expected_parameters == 3:
				try:
					if code[1] < 1 or code[2] < 1 or code[3] < 1:
						return [cError(("Syntax Error: "+str(code[0])+" parameters cannot be 0 or less. "))]+ self.__check_syntax(cp(code[4:]), cp(input_list))
				except TypeError:
					return [cError(("Syntax Error: "+str(code[0])+" parameters have to be numeric."))]+ self.__check_syntax(cp(code[4:]), cp(input_list))
			elif expected_parameters == None:
				head, *tail = code
				return [cError(("Syntax Error: The instruction `"+ str(head) + "` is not supported."))] + self.__check_syntax(tail, cp(input_list))
			
			if all(map(lambda parameter: isinstance(parameter,int), code[1:expected_parameters+1])): #map 3/3
				return [] + self.__check_syntax(cp(code[1+expected_parameters:]), cp(input_list))
			else:
				return [cError(("Syntax Error: "+ str(code[0]) +" parameters must be numeric."))] + self.__check_syntax(cp(code[1+expected_parameters:]), cp(input_list))		
		return []

	def __check_start_instructions(self, tokens : List[Union[str,int]]) -> List[Union[cError]]:
		"""This function checks whether every `START` instruction has a matching `BA` instruction.

		Args:
			tokens (List[Union[str,int]]): All of the lexed tokens in a list.

		Returns:
			List[Union[cError]]: A list containing either nothing or 1 or more cErrors.
		"""
		start_identifiers = self.__find_instruction_single_parameter(cp(tokens), "START")
		ba_identifiers = self.__find_instruction_single_parameter(cp(tokens), "BA")
		
		unknown_identifiers = list(set(start_identifiers)-set(ba_identifiers))

		if unknown_identifiers:
			return self.__create_identifier_errors(unknown_identifiers)		
		return []
		
	def __find_instruction_single_parameter(self, tokens: List[Union[str,int]], instruction : str) -> List[Union[None]]:
		"""This function tries to find the values of instructions with a single parameter.
		It designed to find the identifiers of `BA` and `START` instructions. 

		Args:
			tokens (List[Union[str,int]]): All of the lexed tokens in a list.
			instruction (str): The instruction whose parameter values to find.

		Returns:
			List[Union[int]]: A list of values of the parameters of the supplied instruction.
		"""
		if tokens:
			try:
				parameter_index = tokens.index(instruction)+1
				return [tokens[parameter_index]] + self.__find_instruction_single_parameter(cp(tokens[parameter_index:]), instruction)
			except:
				return []				
		return []
		
	def __create_identifier_errors(self, indentifiers : List[int]) -> List[Union[cError]]:
		"""This function is used to recursively create a list of cErrors about identifier syntax errors.

		Args:
			indentifiers (List[int]): A List of identifiers that are being called by `START` instructions that do not have matching `BA` identifiers.

		Returns:
			List[Union[cError]]: A List of 1 or more cErrors.
		"""
		if indentifiers:
			head, *tail = indentifiers
			return [cError(("Syntax Error: START instruction with identifier `"+str(head)+"` is invalid since there is no BA with identifier `"+str(head)+"`."))] + self.__create_errors(tail)
		return []