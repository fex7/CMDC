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

__all__ = [
	'Preprocessor',
]


class Preprocessor(BasePreprocessor):
	"""Batch language preprocessor.
	
	Constructor:
	    source_filepath: str -- source file path. (any file)
		
	"""

	def __new__(cls, source_filepath):
		if not isinstance(source_filepath, str):
			raise TypeError("Param 'source_filepath' is 'str' type")
		if not os.path.isfile(source_filepath):
			raise FileNotFoundError('Source file not found')
		return super().__new__(cls)

	def __init__(self, source_filepath):
		self._source_filepath = os.path.abspath(source_filepath)
		self._source_filevalue = self.read(source_filepath).lower()
		self._preprocessed_file = '\n' + self._source_filevalue + '\n'
		self._preproc_commands = PreprocessorCommands()
		self._includer = Includer(
				self._preproc_commands.com_include,
				self._source_filepath
		)
	
	def __repr__(self):
		repr_text = "Preprocessor(source_filepath=%s)" % (
			self._source_filepath
		)
		return repr_text
	
	def get_preprocessed_file(self):
		"""Return preprocessed file value."""
		return self._preprocessed_file
	
	def get_source_file(self):
		"""Return source file, before preprocessing."""
		return self._source_filevalue
	
	def getincluder(self):
		"""Return 'Includer' object."""
		return self._includer
	
	def preprocessize(self):
		"""This function does preprocessing."""

		start_include = self._includer.start
		is_loop = True
		while is_loop:
			included_file = start_include(self._preprocessed_file)
			if included_file != self._preprocessed_file:
				self._preprocessed_file = included_file
			else:
				break
	
	def save(self, file_path):
		"""Save preprocess result.
		
		Args:
		    file_path: str -- saved file path.

		"""

		return super().save(file_path, self._preprocessed_file[1:-1])