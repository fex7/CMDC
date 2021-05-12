"""Abstract base classes."""

import abc



class BaseBpp(metaclass=abc.ABCMeta):
	"""
	Base class for all preprocessor commands,
	and for the preprocessor itself.
	
	"""

	def read(self, file_path):
		"""Read bat file.
		
		Args:
		    file_path: str -- File you need to read
		
		Return:
		    value: str -- file value

		"""
		
		with open(file_path, 'r') as file:
			return file.read()
	
	def save(self, text, file_path):
		"""Saves preprocessed result.
		
		Args:
		    text: str -- saved text
		    file_path: str -- saved file path

		"""

		with open(file_path, 'w') as file:
			file.write(text)


class BaseCommand(BaseBpp, metaclass=abc.ABCMeta):
	"""Main base class for preprocessor commands."""
	pass


class BasePreprocessor(BaseBpp, metaclass=abc.ABCMeta):
	"""Main base class for preprocessor."""
	pass


__all__ = [
	n for n in globals() if not n.startswith('_')
]