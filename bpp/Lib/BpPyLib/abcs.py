"""Abstract base classes."""

import abc

__all__ = [
	'BaseBpp',
	'BaseCommand',
	'BasePreprocessor',
]


class BaseBpp(metaclass=abc.ABCMeta):
	"""
	Base class for all preprocessor commands,
	and for the preprocessor itself.
	
	"""

	def read(self, file_path):
		"""Reads the file and returns its value.
		
		Args:
		    file_path: str -- file path a need to read
		
		Return:
		    value: str -- file value
		
		Raises:
		    OSError -- If problem in operating system
		    TypeError -- If incorrect types

		"""
		
		if not isinstance(file_path, str):
			raise TypeError("Param 'file_path' must be 'str'")
		with open(file_path, 'r') as file:
			return file.read()
	
	def save(self, file_path, text):
		"""Saves text to file.
		
		Args:
		    file_path: str -- saved file path
		    text: str -- saved text
		
		Return:
		     value: int -- the number of characters stored.
		
		Raises:
		    OSError -- If problem in operating system
		    TypeError -- If incorrect types

		"""

		if not isinstance(file_path, str):
			raise TypeError("Param 'file_path' must be 'str'")
		if not isinstance(text, str):
			raise TypeError("Param 'text' must be 'str'")
		with open(file_path, 'w') as file:
			return file.write(text)


class BaseCommand(BaseBpp, metaclass=abc.ABCMeta):
	"""Main base class for preprocessor commands."""

	@abc.abstractmethod
	def start(self):
		"""This method performs the main logic.

		It is an abstract method and therefore -
		needs to be overridden in subclasses.

		For example, in the class 'Includer',
		it is a subclass of 'BaseCommand',
		there this method does all the 'include' operations.

		In subclasses, it can take any parameters,
		and return any objects as well.
		But it is recommended to return a string.

		Note. It may take no parameters at all and may not return a value.
		
		"""

		raise NotImplementedError


class BasePreprocessor(BaseBpp, metaclass=abc.ABCMeta):
	"""Main base class for preprocessor."""
	
	@abc.abstractmethod
	def preprocessize(self):
		"""This method executes the main preprocessor logic.

		It is an abstract method and needs to be overridden in subclasses.

		For example, in the 'Preprocessor' class,
		this is a subclass of 'BasePreprocessor',
		there this method performs all preprocessor operations.

		In subclasses, it can take any parameters,
		and also return any object.

		Note. It may take no parameters at all and may not return a value.

		"""
		
		raise NotImplementedError