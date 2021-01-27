from typing import List, Union, Callable, Any
import os

from copy import deepcopy

def check_existance(func : Callable[[str], Any]):
	"""Decorator that checks if a file actually exists.

	Args:
		func (Callable[[str], Any]): A function that uses a filename.
	"""
	def inner(filename):
		if not os.path.exists(filename):
			cError("File Error: The supplied file `"+filename+"` doesn't exist").throw()
		return func(filename)
	return inner
	
@check_existance
def readFile(filename : str) -> List[str]:
	"""This function will read a file containing Controller Code.
	The function will cast all the strings to upper case.
	
	Note that the map function is being used here which is a Higher Order Function.
	Note that this function is decorate to check the existance of a file.
	
	Args:
		filename (str): The file to read. Controller Code files have the extension .coco

	Returns:
		List[str]: A list of strings, a single string for each code line in the file.
	"""
	with open(filename) as file:
		raw_code = file.read().splitlines()
		return list(map(lambda word: word.upper(), raw_code)) #map 4/3

def printb(data, symbol = "=", times = 40):
	"""Small support function for printing results and keeping them together in a block for visibility.

	Args:
		data ([type]): Data can be anything that support being printed.
		symbol (str, optional): The symbol(s) that will encase the data to be printed. Defaults to "=".
		times (int, optional): The amount of times the symbol will be printed both before and after the data. Defaults to 40.
	"""
	print(times * symbol)
	print(data)
	print(times * symbol)
		
def cp(data):
	"""Small support function to deepcopy anything.

	Args:
		data ([type]): The object to be deepcopied, can be anything.

	Returns:
		[type]: A deepcopy of the object.
	"""
	return deepcopy(data)
	
class bareError:
	"""A very bare frame for error classes. 
	Could be expanded upon with code lines for example.
	"""
	def __str__(self):
		pass

	def throw(self):
		pass
	
class cError(bareError):
	"""A custom error class that inherits from bareError.
	A cError can always be printed but when a cError is thrown the application will close.
	"""
	def __init__(self, error_string : str):
		self.text = error_string
	
	def __str__(self):
		return 'Error({text})'.format(
			text = self.text
		)
		
	def throw(self):
		"""This function will print itself and then exit the application.
		"""
		print(self)
		exit()
		
def throw_errors(errors : List[cError]):
	"""Small support function to print a list of cErrors and then throw the last one.

	Args:
		errors (List[cError]): A list of cErrors.
	"""
	if errors:
		head, *tail = errors
		if tail:
			print(head)
			throw_errors(tail)
		else:
			head.throw()
	else:
		print("Warning : There were no errors to throw!")

#This dictionary contains all the instructions and the amount of parameters they need.
#This is mainly used for syntax checking.
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
	"YA":2,
	"YB":2,
	"YX":2,
	"BX":0
}