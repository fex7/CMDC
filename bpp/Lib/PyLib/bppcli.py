"""Batch preprocessor command line interface."""

import textwrap
import copy
import os

from .exceptions import (
	CLIError,
)
from .version import (
	getversion,
)



class BppCLI:
	"""This class works with a console."""
	
	parameters = {
		'--output':   ('binary', 'output'),
		'-o':         ('binary', 'output'), 
		'--source':   ('binary', 'source'),
		'-s':         ('binary', 'source'),
		'--run':      ('unary',  'run'   ),
		'-r':         ('unary',  'run'   ),
		'--help':     ('unary',  'help'  ),
		'-h':         ('unary',  'help'  ),
		'--version':  ('unary', 'version'),
	}

	def __init__(self):
		self._parsered_args = {
			'output': None,
			'source': None,
			'run': None,
		}
	
	def __repr__(self):
		repr_text = "BppCLI()"
		return repr_text
	
	def get_parsered_args(self):
		"""Return parsered arguments."""
		return copy.copy(self._parsered_args)
		
	def print_help(self):
		"""Printed Help."""

		help_text = textwrap.dedent("""
			This utility preprocesses bat files.
			
			Syntax:
			    python bpp.py -s|--source <source file> [-o|--output <output file>] [-r|--run]

			Params:
			    --source | -s <source file>
			    [--output] | [-o] <output file>
			    [--run] | [-r]
			    [--help] | [-h]
			    [--version]
			
			Examples:
			    $ python bpp.py --output newbat.bat --source mybat.bat 
			    $ python bpp.py -o script.bat -s script2.bat --run
			    $ python bpp.py --run -s script.cmd
			    $ python bpp.py -r -s script.cmd
		""")
		print(help_text)
	
	def print_version(self):
		"""Printed Bpp utility version."""
		
		version = "bpp %s" % getversion()
		print(version)
	
	def is_supported(self, argument):
		"""Checks if the parameter is supported or not.
		
		Args:
		   argument: str -- command line argument.
		
		Return:
		    value: bool -- True is supported, False is unsupported

		""" 

		if argument in self.parameters:
			return True
		else:
			return False

	def get_argument_info(self, argument):
		"""Return argument information.
		
		Args:
		    argument: str -- command line argument.
		
		Return:
		    value: tuple -- :
		        0 is 'unary' or 'binary',
		        1 is argument common name

		"""

		return self.parameters.get(argument)


	def parse(self, argv):
		"""Parsing the command line arguments.
		
		Args:
		    argv: list -- sys.argv
		
		Return:
		    value: bool -- If parsered then True, if not then False.
		
		Raises:
		    CLIError -- If incorrect command line arguments
		
		"""

		if len(argv) <= 1 or '--help' in argv or '-h' in argv:
			self.print_help()
			return False
		if '--version' in argv:
			self.print_version()
			return False
		output = source = run = None
		errmsg = "before param '%s' must be indicated value"
		ind = arg = 1
		while ind < len(argv):
			arg = argv[ind]
			if not self.is_supported(arg):
				raise CLIError("This argument '%s' is unsupported." % arg)
			argname = self.get_argument_info(arg)[-1]
			if argname == 'output':
				if len(argv)-1 > ind:
					output = argv[ind+1]
					ind += 2
					continue
				else:
					raise CLIError(errmsg % '-o / --output')
			if argname == 'source':
				if len(argv)-1 > ind:
					source = argv[ind+1]
					ind += 2
					continue
				else:
					raise CLIError(errmsg % '-s / --source')
			if argname == 'run':
				run = 'true'
			ind += 1
		self._parsered_args.update({
			'output': output,
			'source': source,
			'run': run
		})
		return True
	
	def validate(self):
		"""Validates command line arguments.
		
		Raises:
		    CLIError -- If incorrect command line arguments
		
		"""

		source = self._parsered_args.get('source', None)
		if source is None:
			raise CLIError("Param '-s / --source' must be indicated")
		if isinstance(source, str) and not os.path.isfile(source):
			raise CLIError('Source file not found')
		return None


__all__ = [
	'BppCLI',
]