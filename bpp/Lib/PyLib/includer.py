"""Implements the 'include' command."""

import os
import textwrap

from abcs import (
	BasePreprocessor,
)
from exceptions import (
	IncludeError,
	IncludedSourceError
)



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


__all__ = [
	n for n in globals() if not n.startswith('_')
]