"""Main class for preprocessor."""

import os

from .abcs import (
	BasePreprocessor,
)
from .precommands import (
	PreprocessorCommands,
)
from .includer import (
	Includer,
)



class Preprocessor(BasePreprocessor):
	"""Batch language preprocessor.
	
	Constructor:
	    bat_file_path: str -- bat file path. (any file)
		
	"""

	def __new__(cls, bat_file_path):
		if not isinstance(bat_file_path, str):
			raise TypeError("Param 'bat_file_path' is 'str' type")
		if not os.path.isfile(bat_file_path):
			raise FileNotFoundError('Bat file not found')
		return super().__new__(cls)

	def __init__(self, bat_file_path):
		self._bat_file_path = os.path.abspath(bat_file_path)
		self._bat_file_value = self.read(bat_file_path).lower()
		self._preprocessed_file = '\n' + self._bat_file_value + '\n'
		self._preproc_commands = PreprocessorCommands()
		self._includer = Includer(
				self._preproc_commands.com_include,
				self._bat_file_path)
	
	def __repr__(self):
		repr_text = "Preprocessor(bat_file_path=%s)" % (
			self._bat_file_path
		)
		return repr_text
	
	def get_preprocessed_file(self):
		"""Return preprocessed file value."""
		return self._preprocessed_file
	
	def get_source_file(self):
		"""Return source file, before preprocessing."""
		return self._bat_file_value
	
	def preprocessize(self):
		"""This function does preprocessing."""

		include_ = self._includer.include
		while True:
			included_file = include_(self._preprocessed_file)
			if included_file != self._preprocessed_file:
				self._preprocessed_file = included_file
			else:
				break
	
	def save(self, file_path):
		"""Save preprocess result.
		
		Args:
		    file_path: str -- saved file path.

		"""

		return super().save(self._preprocessed_file[1:-1], file_path)


__all__ = [
	'Preprocessor',
]
