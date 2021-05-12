"""Batch preprocessor command line interface."""

import textwrap



class BppCLI:
	"""This class works with a console."""
	
	parameters = {
		'--output':   ('binary', 'output'),
		'-o':         ('binary', 'output'), 
		'--source':   ('binary', 'source'),
		'-s':         ('binary', 'source'),
		'--run':      ('unary',  'run'   ),
		'run':        ('unary',  'run'   ),
		'-r':         ('unary',  'run'   ),
	}

	def __init__(self):
		self._parsered_args = {
			'output': None,
			'source': None,
			'run': None,
		}
	
	def get_parsered_args(self):
		"""Return parsered arguments."""
		return self._parsered_args
		
	def print_help(self):
		"""Printed Help."""

		help_text = textwrap.dedent("""
			This utility preprocesses bat files.
			
			Params:
			    [--output] | [-o] <output file> 
			    --source | -s <source file>
			    [--run] | [-r] | [run]
			    [--help] | [-h]
			
			Examples:
			    $ python bpp.py --output newbat.bat --source mybat.bat 
			    $ python bpp.py -o script.bat -s script2.bat --run
			    $ python bpp.py --run -s script.cmd
			    $ python bpp.py -r -s script.cmd
		""")
		print(help_text)
	
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
		
		"""

		if len(argv) <= 1 or '--help' in argv or '-h' in argv:
			self.print_help()
			return False
		output = source = run = None
		errmsg = "before param '%s' must be indicated value"
		ind = arg = 0
		while ind < len(argv):
			arg = argv[ind]
			if ind == 0:
				ind += 1
				continue
			if not self.is_supported(arg):
				raise ValueError("This argument '%s' is unsupported." % arg)
			argname = self.get_argument_info(arg)[-1]
			if argname == 'output':
				if len(argv)-1 > ind:
					output = argv[ind+1]
					ind += 2
					continue
				else:
					raise ValueError(errmsg % '-o / --output')
			if argname == 'source':
				if len(argv)-1 > ind:
					source = argv[ind+1]
					ind += 2
					continue
				else:
					raise ValueError(errmsg % '-s / --source')
			if argname == 'run':
				run = 'true'
			ind += 1
		self._parsered_args.update({
			'output': output,
			'source': source,
			'run': run
		})
		return True


__all__ = [
	n for n in globals() if not n.startswith('_')
]