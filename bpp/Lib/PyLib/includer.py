"""Implements the 'include' command."""

import os
import textwrap

from .abcs import (
	BaseCommand,
)
from .exceptions import (
	IncludeError,
	IncludedSourceError,
)
from .prompts import (
	get_include_prompt,
)



class Includer(BaseCommand):
	"""'Include' command class.
	
	Constructor:
	    regexs: dict -- include command regexs.
	    source_file_path: str -- source bat file path

	"""

	def __new__(cls, regexs, source_file_path):
		error_message = "Param '%s' type is '%s', not '%s'"
		if not isinstance(regexs, dict):
			raise TypeError(
				error_message % (
					'regexs', 'dict',
					type(regexs).__name__),)
		if not isinstance(source_file_path, str):
			raise TypeError(
				error_message % (
					'source_file_path', 'str',
					type(source_file_path).__name__),)
		return super().__new__(cls)

	def __init__(self, regexs, source_file_path):
		self._regexs = regexs
		self._source_file_path = source_file_path
		self._comment_symbol = '::'
		self._file_extensions = ('.bat', '.cmd', '.hbat', '.hb')
	
	def __repr__(self):
		repr_text = "Includer(regexs=%s, source_file_path=%s)" % (
			self._regexs, self._source_file_path
		)
		return repr_text
	
	def setproperty(self, name, value):
		"""Set the property new value.
		
		The parameter 'name' for example -
		could be 'comment' OR 'extensions'.

		If name == 'extensions' then
		    set file extensions. ( ['.bat', '.cmd','.py'] )
		If name == 'comment' then
		    set comment symbol. ( '//', '#', '::', ...etc ) -
		    * the specify one option.
		
		Args:
		    name: str -- property name.
		    value: object -- new value
		
		Raises:
		    TypeError -- if incorrectly params types
		    ValueError -- if unsupported property
		    AttributeError -- if attribute not found
		
		"""
		 
		if not isinstance(name, str):
			raise TypeError("Param name is 'str'")
		if name == 'extensions' and not isinstance(value, (list, tuple)):
			errmsg = "If param name == 'extension' do the value is 'list' or 'tuple'"
			raise TypeError(errmsg)
		if name == 'comment' and not isinstance(value, str):
			errmsg = "If param name == 'comment' do the value is 'str'"
			raise TypeError(errmsg)
		if name in ('extensions', 'comment'):
			if name == 'extensions':
				self._file_extensions = value
			elif name == 'comment':
				self._comment_symbol = value
		else:
			errmsg = "This name '%s' - not supported" % name
			raise ValueError(errmsg)
	
	def getproperty(self, name):
		"""Return property value.
		
		The parameter 'name' for example -
		could be 'comment' OR 'extensions'.

		If name == 'extensions' then
		    return file extensions. ( ['.bat', '.cmd','.py'] )
		If name == 'comment' then
		    return comment symbol. ( '//', '#', '::', ...etc ) -
			* the specify one option.
		
		Args:
		    name: str -- property name.
		
		Return:
		    value: object -- property value
		
		Raises:
		    TypeError -- if incorrectly params types
		    ValueError -- if unsupported property

		"""
		
		if not isinstance(name, str):
			raise TypeError("Param name is 'str'")
		if name in ('extensions', 'comment'):
			if name == 'extensions':
				return self._file_extensions
			elif name == 'comment':
				return self._comment_symbol
		else:
			errmsg = "This name '%s' - not supported" % name
			raise ValueError(errmsg)

	def read_include_bat(self, file_path):
		"""Read include file.
		
		Args:
		    file_path: str -- bat file path
		
		Return:
		    value: str -- bat file value
			
		"""

		if not os.path.isfile(file_path):
			raise FileNotFoundError('Include file not found')
		file_ext = os.path.splitext(os.path.split(file_path)[-1])[-1]
		if file_ext not in self._file_extensions:
			raise OSError(
				"File extension must be in %s" % self._file_extensions)
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
		file_value = self.read_include_bat(variable_value)
		return (file_value, variable_value)
	
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
			* %s
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
				prompt = get_include_prompt(n)
				raise IncludeError(
					error_message % (prompt, line, match)
				)
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
			The file is trying to include itself.\n
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
		after_replacement = (
			'%s ' % self._comment_symbol + 'File - "%s"\n' +\
			'%s%s(\n\n' % (self._comment_symbol, '-'*30)
		)
		before_replacement = (
			'\n\n%s%s)\n' % (self._comment_symbol, '-'*30)
		)
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


def get_special_includer(regexs, source_file_path, lang='batch'):
	"""Return special Includer object.
	
	In 'lang' parameter, you must specify the name of the language.
	For example - 'batch', python, 'cplusplus'
	
	It will just put the file extension and comment character,
	for that language.

	A 'lang' param value is not case sensitive.
	
	Args:
	    regexs: dict -- include command regexs.
	    source_file_path: str -- source file path
	    lang: str -- language name. For example 'batch' or 'python'
	
	Return:
	    value: Includer -- Includer object
	
	Raises:
	    TypeError -- If incorrectly params types
	    ValueError -- If incorrectly params

	"""
	
	error_message = "Param '%s' type is '%s', not '%s'"
	if not isinstance(lang, str):
		raise TypeError(
			error_message % (
				'lang', 'str',
				type(lang).__name__,)
		)
	lang = lang.lower()
	includer = Includer(regexs, source_file_path)
	if lang == 'batch':
		includer._comment_symbol = '::'
		includer._file_extensions = ('.bat', '.cmd', '.hbat', '.hb')
	elif lang == 'python':
		includer._comment_symbol = '#'
		includer._file_extensions = ('.py')
	elif lang == 'c':
		includer._comment_symbol = '//'
		includer._file_extensions = ('.c', '.h')
	elif lang == 'cplusplus':
		includer._comment_symbol = '//'
		includer._file_extensions = ('.cpp', '.cxx', '.cc', '.h', '.hpp')
	elif lang == 'java':
		includer._comment_symbol = '//'
		includer._file_extensions = ('.java')
	elif lang == 'c#':
		includer._comment_symbol = '//'
		includer._file_extensions = ('.cs')
	elif lang == 'go':
		includer._comment_symbol = '//'
		includer._file_extensions = ('.go')
	elif lang == 'bash':
		includer._comment_symbol = '#'
		includer._file_extensions = ('.sh')
	elif lang == 'javascript':
		includer._comment_symbol = '//'
		includer._file_extensions = ('.js')
	else:
		raise ValueError("This lang '%s' is unsupported" % lang)
	return includer


__all__ = [
	'Includer',
	'get_special_includer',
]