"""Batch preprocessor.

This module preprocesses bat files.
It does operations such as:
* #include

It is a console utility.
Write this in a terminal to get help:
$ python bpp.py --help

This utility will work correctly on Windows operating systems.

"""

#import textwrap
#import abc
#import re
import random
import sys
import os
 
sys.path.insert(
	1, os.path.realpath(os.path.join(__file__, '..', 'Lib', 'PyLib'))
)

from abcs import (
	BasePreprocessor,
)
from precommands import (
	PreprocessorCommands,
)
from includer import (
	Includer,
)
from bppcli import (
	BppCLI,
)
from utils import (
	chdir_to_filedir,
	get_temp_dir,
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


def main(argc, argv):
	"""Main function."""

	bppcli = BppCLI()
	status = bppcli.parse(argv)
	if not status:
		return None
	parsered_args = bppcli.get_parsered_args()
	source = parsered_args['source']
	output = parsered_args['output']
	run = parsered_args['run']
	if source is None:
		raise ValueError("Argument '--source or -s' not specified")
	source = os.path.abspath(source)
	current_dir = os.getcwd()
	chdir_to_filedir(source)
	preprocessor = Preprocessor(source)
	preprocessor.preprocessize()
	os.chdir(current_dir)
	if output is not None:
		output = os.path.abspath(output)
		preprocessor.save(output)
	else:
		if run is not None:
			temp_file_name = '__output_%s__.bat' % random.randrange(100000, 999999)
			tmp_dir = get_temp_dir()
			output = os.path.abspath(
				os.path.join(tmp_dir, temp_file_name)
			)
			preprocessor.save(output)
		else:
			preprocessed_file = preprocessor.get_preprocessed_file()
			print(preprocessed_file)
			return None
	if run is not None:
		command = "call %s" % output
		try:
			os.system(command)
			
		finally:
			if parsered_args['output'] is None:
				os.remove(output)
	return None

def run():
	"""Runs the main function.
	
	Raises:
	    SystemExit -- calls sys.exit

	"""

	argc = len(sys.argv)
	argv = sys.argv
	current_dir = os.getcwd()
	try:
		main(argc, argv)
	
	except Exception as ex:
		error_message = '%s' % (
			'\n'.join(map(str, ex.args)),
		)
		if isinstance(ex, OSError):
			error_message += ": '%s'" % ex.filename
		print(error_message)
		sys.exit(1)
	
	else:
		sys.exit(0)
	
	finally:
		try:
			os.chdir(current_dir)
		
		except Exception:
			pass


__all__ = [
	n for n in globals()
				if n not in ('main', 'run') 
				if not n.startswith('_')
]


if __name__ == "__main__":
	try:
		run()
	
	except Exception:
		pass
