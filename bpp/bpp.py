"""Batch preprocessor.

This module preprocesses bat files.
It does operations such as:
* #include

It is a console utility.
Write this in a terminal to get help:
$ python bpp.py --help

This utility will work correctly on Windows operating systems.

"""

import textwrap
import random
import abc
import sys
import os
import re



class PreprocessorError(Exception):
	"""Main exception class a preprocessor commands."""
	pass


class IncludeError(PreprocessorError):
	"""Main included errors class."""
	pass


class IncludedSourceError(IncludeError):
	"""Raises when the source file is included itself."""
	pass


class PreprocessorCommands:
	"""All preprocessor commands regexs."""
	
	com_include = {
		# Good templates.
		1:     re.compile(r'(?<=\n)[ \t]*:#include[ \t]*".+"[ \t]*(?=\n)'), # :#include "fold\lib.bat"
		2:     re.compile(r'(?<=\n)[ \t]*:#include[ \t]*".*%.*"[ \t]*(?=\n)'), # :#include "%lib_dir%\lib.bat"
		11:    re.compile(r'"(.+)"'), # included file path - "fold\lib.bat"
		21:    re.compile(r'"(.+)"'), # included file path - "%lib_dir%\lib.bat"
		# Bad templates.
		-1:    re.compile(r'(?<=\n)[ \t]*:#include[ \t]*(?!.+)'), # :#include 
		-2:    re.compile(r'(?<=\n)[ \t]*:#include[ \t]*""'), # :#include ""
		-3:    re.compile(r'(?<=\n)[ \t]*:#include[ \t]*"(?!.+)'), # :#include "
		-4:    re.compile(r'(?<=\n)[ \t]*:#include[ \t]*".+[^"](?!.+)'), # :#include "lib.bat
		-5:    re.compile(r'(?<=\n)[ \t]*:#include [^"].+"'), # :#include lib.bat"
		-6:    re.compile(r'(?<=\n)[ \t]*:#include [^"].+[^"](?!.+)'), # :#include fold\lib.bat
	}


class BasePreprocessor(metaclass=abc.ABCMeta):
	"""Base class all preprocessor commands."""

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


class Includer(BasePreprocessor):
	"""'Include' command class.
	
	Constructor:
	    regexs: dict -- include command regexs.
	    source_file_path: str -- source bat file path
	
	"""

	def __new__(cls, regexs, source_file_path):
		error_message = "Param '%s' type is '%s', not '%s'"
		if not isinstance(regexs, dict):
			raise TypeError(
				error_message % ('regexs', 'dict',
				type(regexs).__name__),
			)
		if not isinstance(source_file_path, str):
			raise TypeError(
				error_message % ('source_file_path', 'str',
				type(source_file_path).__name__),
			)
		return super().__new__(cls)

	def __init__(self, regexs, source_file_path):
		self._regexs = regexs
		self._source_file_path = source_file_path

	def read_include_bat(self, file_path):
		"""Read include file.
		
		Args:
		    file_path: str -- bat file path
		
		Return:
		    value: str -- bat file value
			
		"""

		if not os.path.isfile(file_path):
			raise FileNotFoundError('Bat file not found')
		file_ext = os.path.splitext(os.path.split(file_path)[-1])[-1]
		if file_ext not in ('.bat', '.cmd', '.hbat'):
			raise OSError("File extension is '.bat', '.cmd', '.hbat'")
		return self.read(file_path)
	
	def read_from_environ(self, environ_var):
		"""Read bat file from environment.

		Reads the file path of which is specified in environment variables.
		
		Args:
		    environ_var: str -- environment variable name
		
		Return:
		    value: tuple -- 0 is file value, 1 is unwrapped environment variable

		"""
		
		variable_value = os.popen('echo %s' % environ_var).read().strip()
		return (self.read_include_bat(variable_value), variable_value)
	
	def syntax_analyze(self, source):
		"""The syntax analyzer for the inlcude command.

		Args:
		    source: str -- source file value
		
		Return:
		    value: bool -- True, is correctly
		
		Raises:
		   IncludeError -- raises if syntax incorrectly.
		   
		"""
		
		
		error_message = textwrap.dedent("""
			Syntax Error with 'include' command:\n
			Line -- %s
			SyntaxError -- %s""")[1:]
		com_include = self._regexs
		bad_templates = (n for n in com_include if n < 0)
		for n in bad_templates:
			match = com_include[n].search(source)
			if match is not None:
				match = match.group().strip()
				if com_include[n].search('\n' + match) is None:
					continue
				try:
					line = source.splitlines().index(match)
					
				except ValueError:
					line = -1
				raise IncludeError(error_message % (line, match))
		else:
			return True
	
	def not_include_source(self, source, include_expression):
		"""Raises exceptions due to the inclusion of itself.

		You do NOT need to call this method to check -
		if the file itself is included or not,
		this method just throws an exception.

		This method must be called if the file tries to include itself.
		For example, if the file "C:\myscript.bat" does the following:
		
		:#include "C:\myscript.bat"
		This is mistake!

		Args:
		    source: str -- source file value
		    include_expression: str -- for example ":#include source.bat"
		
		Raises:
		    IncludedSourceError -- just raises
		
		"""

		error_message = textwrap.dedent("""
			Error: The file is trying to include itself.\n
			Line - %s
			IncludeError - %s""")[1:]
		try:
			line = source.splitlines().index(include_expression)
		
		except ValueError:
			line = -1
		raise IncludedSourceError(error_message % (line, include_expression))
	
	def include(self, source):
		"""include bat files in bat.

		Args:
		    source: str -- source file value
		
		Return:
		    value: str -- source includes
		
		Raises:
		    IncludeError -- raises if syntax incorrectly.

		"""
		
		# analyze
		self.syntax_analyze(source)
		after_replacement = ':: File - "%s"\n' + '::%s(\n\n' % ('-' * 31)
		before_replacement = '\n\n::%s)\n' % ('-' * 31)
		err_msg = "Syntax Error from 'include' command"
		com_include = self._regexs
		source_includes = source
		for m2 in com_include[2].finditer(source):
			m2 = m2.group()
			included_file = com_include[21].search(m2)
			if included_file is not None:
				included_file = included_file.group()[1:-1].strip()
				included_file_value, variable_value = self.read_from_environ(included_file)
				if os.path.abspath(variable_value) == self._source_file_path:
					self.not_include_source(source, m2)
				included_value = '%s %s %s' % (
					after_replacement % os.path.split(variable_value)[-1],
					included_file_value,
					before_replacement,
				)
				source_includes = source_includes.replace(m2, included_value)
			else:
				raise IncludeError(err_msg)
		for m1 in com_include[1].finditer(source_includes):
			m1 = m1.group()
			included_file = com_include[11].search(m1)
			if included_file is not None:
				included_file = included_file.group()[1:-1].strip()
				if os.path.abspath(included_file) == self._source_file_path:
					self.not_include_source(source, m1)
				included_file_value = self.read_include_bat(included_file)
				included_value = '%s %s %s' % (
					after_replacement % os.path.split(included_file)[-1],
					included_file_value,
					before_replacement,
				)
				source_includes = source_includes.replace(m1, included_value)
			else:
				raise IncludeError(err_msg)
		return source_includes


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


def chdir_to_filedir(file_path):
	"""Changed directory to file directory.
	
	Args:
	    file_path: str -- file path
	
	Return:
	    value: str -- file dir name
	
	Raises:
	    FileNotFoundError -- if file not found.

	"""

	if not os.path.isfile(file_path):
		raise FileNotFoundError("file not found")
	file_dirname = os.path.dirname(file_path)
	os.chdir(file_dirname)
	return file_dirname


def get_temp_dir():
	"""Return Temp directory path."""
	
	if os.name == 'nt':
		tmp_dir = os.getenv('Temp', '.')
	elif os.name == 'posix':
		tmp_dir = os.getenv('TMPDIR', '.')
	else:
		tmp_dir = os.getenv('TMP', '.')
	return tmp_dir


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
